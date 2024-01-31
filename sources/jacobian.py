# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, cos, sin, zeros
from scipy.sparse import csc_matrix

from calc import pcalc, qcalc
from ctrl import controljac


def jacobi(
    powerflow,
):
    """cálculo das submatrizes da matriz Jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    nnz = int(powerflow.apont[-1])
    data = zeros([4 * nnz], dtype=float)
    indx = zeros([4 * nnz], dtype=int)
    indp = concatenate((deepcopy(powerflow.apont), zeros(powerflow.nbus, dtype=int)))

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            de = value["de"] - 1
            para = value["para"] - 1

            # elementos de,para
            h1 = (
                powerflow.solution["voltage"][de]
                * powerflow.solution["voltage"][para]
                * (
                    -powerflow.admitancia[idx].real
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            n1 = -powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            m1 = (
                powerflow.solution["voltage"][de]
                * powerflow.solution["voltage"][para]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    + powerflow.admitancia[idx].imag
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            l1 = powerflow.solution["voltage"][de] * (
                -powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            # elementos para,de
            h2 = (
                powerflow.solution["voltage"][para]
                * powerflow.solution["voltage"][de]
                * (
                    powerflow.admitancia[idx].real
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            n2 = powerflow.solution["voltage"][para] * (
                -powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            m2 = (
                powerflow.solution["voltage"][para]
                * powerflow.solution["voltage"][de]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    - powerflow.admitancia[idx].imag
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            l2 = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            # preenchimento vetores de,para
            if para == 0:
                aux_h1 = int(indp[para] - 1)
                aux_n1 = int(indp[para] - 1) + 2 * nnz
                aux_m1 = int(indp[para] - 1) + int(powerflow.apont[para])
                aux_l1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.apont[para])
            else:
                aux_h1 = int(indp[para] - 1) + int(powerflow.apont[para - 1])
                aux_n1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.apont[para - 1])
                aux_m1 = int(indp[para] - 1) + int(powerflow.apont[para])
                aux_l1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.apont[para])
            data[aux_h1] = h1  # Submatriz H
            data[aux_n1] = n1  # Submatriz N
            data[aux_m1] = m1  # Submatriz M
            data[aux_l1] = l1  # Submatriz L
            indx[aux_h1] = de  # Submatriz H
            indx[aux_n1] = de  # Submatriz N
            indx[aux_m1] = de + powerflow.nbus  # Submatriz M
            indx[aux_l1] = de + powerflow.nbus  # Submatriz L
            indp[para] += -1

            # Preencher vetores de construção com elementos da posição [para, de]
            if de == 0:
                aux_h2 = int(indp[de] - 1)
                aux_n2 = int(indp[de] - 1) + 2 * nnz
                aux_m2 = int(indp[de] - 1) + int(powerflow.apont[de])
                aux_l2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.apont[de])
            else:
                aux_h2 = int(indp[de] - 1) + int(powerflow.apont[de - 1])
                aux_n2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.apont[de - 1])
                aux_m2 = int(indp[de] - 1) + int(powerflow.apont[de])
                aux_l2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.apont[de])
            data[aux_h2] = h2  # Submatriz H
            data[aux_n2] = n2  # Submatriz N
            data[aux_m2] = m2  # Submatriz M
            data[aux_l2] = l2  # Submatriz L
            indx[aux_h2] = para  # Submatriz H
            indx[aux_n2] = para  # Submatriz N
            indx[aux_m2] = para + powerflow.nbus  # Submatriz M
            indx[aux_l2] = para + powerflow.nbus  # Submatriz L
            indp[de] += -1

    # Elementos da diagonal principal da matriz jacobiana
    for idx, value in powerflow.dbarraDF.iterrows():
        # Submatriz H
        if (
            powerflow.maskP[idx] == False
        ):  # A presença do módulo se deve ao tratamento de limites (QLIM), que pode converter barra tipo 2 em -2
            hk = 1e20
            if 'FREQ' in powerflow.control and value['tipo'] != 0:
                hk = - (powerflow.solution['voltage'][idx] ** 2) * powerflow.bdiag[idx] - qcalc(powerflow=powerflow, idx=idx)

        else:
            hk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[
                idx
            ] - qcalc(powerflow=powerflow, idx=idx)

        # Submatriz N
        nk = (
            pcalc(powerflow=powerflow, idx=idx)
            + (powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx]
        ) / powerflow.solution["voltage"][idx]

        # Submatriz M
        mk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx] + qcalc(
            powerflow=powerflow, idx=idx
        )

        # Submatriz L
        if (powerflow.maskQ[idx] == False) and (
            ("QLIM" not in powerflow.control)
            or ("QLIMs" not in powerflow.control)
            or ("QLIMn" not in powerflow.control)
        ):
            lk = 1e20
        else:
            lk = (
                qcalc(powerflow=powerflow, idx=idx)
                - (powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[idx]
            ) / powerflow.solution["voltage"][idx]

        # Preencher vetor  de construção com elementos da posição [k, k]
        if idx == 0:
            aux_h = int(indp[idx] - 1)
            aux_n = int(indp[idx] - 1) + 2 * nnz
            aux_m = int(indp[idx] - 1) + int(powerflow.apont[idx])
            aux_l = int(indp[idx] - 1) + 2 * nnz + int(powerflow.apont[idx])
        else:
            aux_h = int(indp[idx] - 1) + int(powerflow.apont[idx - 1])
            aux_n = int(indp[idx] - 1) + 2 * nnz + int(powerflow.apont[idx - 1])
            aux_m = int(indp[idx] - 1) + int(powerflow.apont[idx])
            aux_l = int(indp[idx] - 1) + 2 * nnz + int(powerflow.apont[idx])
        data[aux_h] = hk  # Submatriz H
        data[aux_n] = nk  # Submatriz N
        data[aux_m] = mk  # Submatriz M
        data[aux_l] = lk  # Submatriz L
        indx[aux_h] = idx  # Submatriz H
        indx[aux_n] = idx  # Submatriz N
        indx[aux_m] = idx + powerflow.nbus  # Submatriz M
        indx[aux_l] = idx + powerflow.nbus  # Submatriz L
        indp[idx] += -1

        # Atualizar vetor 'indprt' para estrutura final
        indp[idx] = 2 * indp[idx]
        indp[idx + powerflow.nbus] = 2 * nnz + indp[idx]

    # Adicionar comprimento do vetor 'incices' como último elemento do vetor 'indprt'
    indp = append(indp, len(indx))

    # Criação da jacobiana como matriz CSC
    powerflow.jacob = csc_matrix(
        (data, indx, indp),
        shape=(2 * powerflow.nbus, 2 * powerflow.nbus),
    )

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controljac(
            powerflow,
        )
