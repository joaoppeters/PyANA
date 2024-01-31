# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros
from sympy import oo, Symbol, symbols, Matrix
from sympy.functions import cos, sin

from calc import pcalcsym, qcalcsym
from ctrl import controljac


def hessian(
    powerflow,
):
    """cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis Simbólicas
    v = [symbols("v%d" % i) for i in range(powerflow.nbus)]
    t = [symbols("t%d" % i) for i in range(powerflow.nbus)]
    w = [symbols("w%s" % i) for i in range(2 * powerflow.nbus)]
    dxfw = zeros((2 * powerflow.nbus, 1), dtype=Symbol)

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            de = value["de"] - 1
            para = value["para"] - 1

            # elementos de,para
            h1 = (
                v[de]
                * v[para]
                * (
                    -powerflow.admitancia[idx].real * sin(t[de] - t[para])
                    + powerflow.admitancia[idx].imag * cos(t[de] - t[para])
                )
            )
            n1 = -v[de] * (
                powerflow.admitancia[idx].real * cos(t[de] - t[para])
                + powerflow.admitancia[idx].imag * sin(t[de] - t[para])
            )
            m1 = (
                v[de]
                * v[para]
                * (
                    powerflow.admitancia[idx].real * cos(t[de] - t[para])
                    + powerflow.admitancia[idx].imag * sin(t[de] - t[para])
                )
            )
            l1 = v[de] * (
                -powerflow.admitancia[idx].real * sin(t[de] - t[para])
                + powerflow.admitancia[idx].imag * cos(t[de] - t[para])
            )

            # elementos para,de
            h2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real * sin(t[de] - t[para])
                    + powerflow.admitancia[idx].imag * cos(t[de] - t[para])
                )
            )
            n2 = v[para] * (
                -powerflow.admitancia[idx].real * cos(t[de] - t[para])
                + powerflow.admitancia[idx].imag * sin(t[de] - t[para])
            )
            m2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real * cos(t[de] - t[para])
                    - powerflow.admitancia[idx].imag * sin(t[de] - t[para])
                )
            )
            l2 = v[para] * (
                powerflow.admitancia[idx].real * sin(t[de] - t[para])
                + powerflow.admitancia[idx].imag * cos(t[de] - t[para])
            )

            dxfw[de] += (
                -h1 * w[para]
                - n1 * w[para + powerflow.nbus]
                + h1 * w[de]
                - n1 * w[de + powerflow.nbus] * v[para] / v[de]
            )
            dxfw[de + powerflow.nbus] += (
                -m1 * w[para]
                - l1 * w[para + powerflow.nbus]
                + m1 * w[de]
                + l1 * w[de + powerflow.nbus]
            )
            dxfw[para] += (
                -h2 * w[de]
                - n2 * w[de + powerflow.nbus]
                + h2 * w[para]
                + n2 * w[para + powerflow.nbus]
            )
            dxfw[para + powerflow.nbus] += (
                -m2 * w[de]
                - l2 * w[de + powerflow.nbus]
                + m2 * w[para]
                - l2 * w[para + powerflow.nbus] * v[para] / v[de]
            )

    # Elementos da diagonal principal da matriz jacobiana
    for idx, value in powerflow.dbarraDF.iterrows():
        # Submatriz H
        if (
            powerflow.maskP[idx] == False
        ):  # A presença do módulo se deve ao tratamento de limites (QLIM), que pode converter barra tipo 2 em -2
            hk = oo

        else:
            hk = -(v[idx] ** 2) * powerflow.bdiag[idx] - qcalcsym(
                powerflow=powerflow,
                v=v,
                t=t,
                idx=idx,
            )

        # Submatriz N
        nk = (
            pcalcsym(
                powerflow=powerflow,
                v=v,
                t=t,
                idx=idx,
            )
            + (v[idx] ** 2) * powerflow.gdiag[idx]
        ) / v[idx]

        # Submatriz M
        mk = -(v[idx] ** 2) * powerflow.gdiag[idx] + qcalcsym(
            powerflow=powerflow,
            v=v,
            t=t,
            idx=idx,
        )

        # Submatriz L
        if (powerflow.maskQ[idx] == False) and (
            ("QLIM" not in powerflow.control)
            or ("QLIMs" not in powerflow.control)
            or ("QLIMn" not in powerflow.control)
        ):
            lk = oo
        else:
            lk = (
                qcalcsym(
                    powerflow=powerflow,
                    v=v,
                    t=t,
                    idx=idx,
                )
                - (v[idx] ** 2) * powerflow.bdiag[idx]
            ) / v[idx]

        powerflow.jacobsymb[idx][idx] = hk
        powerflow.jacobsymb[idx][idx + powerflow.nbus] = nk
        powerflow.jacobsymb[idx + powerflow.nbus][idx] = mk
        powerflow.jacobsymb[idx + powerflow.nbus][idx + powerflow.nbus] = lk

    powerflow.jacobsymb = powerflow.jacobsymb * w

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controljac(
            powerflow,
        )
