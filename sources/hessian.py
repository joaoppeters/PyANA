# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import concatenate, reshape, zeros
from sympy import Symbol, symbols
from sympy.functions import cos, sin

from calc import pcalctk, pcalctm, pcalcvk, pcalcvm, qcalctk, qcalctm, qcalcvk, qcalcvm
from ctrl import controlhess, controljacsym


def hessian(
    powerflow,
):
    """cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.hessian = zeros((2 * powerflow.nbus, 2 * powerflow.nbus))

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            de = value["de"] - 1
            para = value["para"] - 1

            # elementos de,para
            h1tk = (
                powerflow.solution["voltage"][de]
                * powerflow.solution["voltage"][para]
                * (
                    -powerflow.admitancia[idx].real
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
            h1tm = (
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
            h1vk = powerflow.solution["voltage"][para] * (
                -powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            h1vm = powerflow.solution["voltage"][de] * (
                -powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            n1tk = -powerflow.solution["voltage"][de] * (
                -powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            n1tm = -powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            n1vk = -(
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            n1vm = 0.0

            m1tk = (
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
            m1tm = (
                powerflow.solution["voltage"][de]
                * powerflow.solution["voltage"][para]
                * (
                    powerflow.admitancia[idx].real
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    - powerflow.admitancia[idx].imag
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            m1vk = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            m1vm = powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            l1tk = powerflow.solution["voltage"][de] * (
                -powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            l1tm = powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            l1vk = -powerflow.admitancia[idx].real * sin(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            ) + powerflow.admitancia[idx].imag * cos(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            )
            l1vm = 0.0

            # elementos para,de
            h2tk = (
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
            h2tm = (
                powerflow.solution["voltage"][para]
                * powerflow.solution["voltage"][de]
                * (
                    -powerflow.admitancia[idx].real
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
            h2vk = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            h2vm = powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            n2tk = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            n2tm = powerflow.solution["voltage"][para] * (
                -powerflow.admitancia[idx].real
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            n2vk = 0.0
            n2vm = -powerflow.admitancia[idx].real * cos(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            ) + powerflow.admitancia[idx].imag * sin(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            )

            m2tk = (
                powerflow.solution["voltage"][para]
                * powerflow.solution["voltage"][de]
                * (
                    -powerflow.admitancia[idx].real
                    * sin(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                    - powerflow.admitancia[idx].imag
                    * cos(
                        powerflow.solution["theta"][de]
                        - powerflow.solution["theta"][para]
                    )
                )
            )
            m2tm = (
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
            m2vk = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            m2vm = powerflow.solution["voltage"][de] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )

            l2tk = powerflow.solution["voltage"][para] * (
                powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                - powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            l2tm = powerflow.solution["voltage"][para] * (
                -powerflow.admitancia[idx].real
                * cos(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
                )
            )
            l2vk = 0.0
            l2vm = powerflow.admitancia[idx].real * sin(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            ) + powerflow.admitancia[idx].imag * cos(
                powerflow.solution["theta"][de] - powerflow.solution["theta"][para]
            )

            powerflow.hessian[de, de] = (
                h1tk * powerflow.sol["eigen"][para]
                + n1tk * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de, para] = (
                h1tm * powerflow.sol["eigen"][para]
                + n1tm * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de, de + powerflow.nbus] = (
                h1vk * powerflow.sol["eigen"][para]
                + n1vk * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de, para + powerflow.nbus] = (
                h1vm * powerflow.sol["eigen"][para]
                + n1vm * powerflow.sol["eigen"][para + powerflow.nbus]
            )

            powerflow.hessian[para, de] = (
                h2tk * powerflow.sol["eigen"][de]
                + n2tk * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para, para] = (
                h2tm * powerflow.sol["eigen"][de]
                + n2tm * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para, de + powerflow.nbus] = (
                h2tm * powerflow.sol["eigen"][de]
                + n2tm * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para, para + powerflow.nbus] = (
                h2tm * powerflow.sol["eigen"][de]
                + n2tm * powerflow.sol["eigen"][de + powerflow.nbus]
            )

            powerflow.hessian[de + powerflow.nbus, de] = (
                m1tk * powerflow.sol["eigen"][para]
                + l1tk * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de + powerflow.nbus, para] = (
                m1tm * powerflow.sol["eigen"][para]
                + l1tm * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de + powerflow.nbus, de + powerflow.nbus] = (
                m1vk * powerflow.sol["eigen"][para]
                + l1vk * powerflow.sol["eigen"][para + powerflow.nbus]
            )
            powerflow.hessian[de + powerflow.nbus, para + powerflow.nbus] = (
                m1vm * powerflow.sol["eigen"][para]
                + l1vm * powerflow.sol["eigen"][para + powerflow.nbus]
            )

            powerflow.hessian[para + powerflow.nbus, de] = (
                m2tk * powerflow.sol["eigen"][de]
                + l2tk * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para + powerflow.nbus, para] = (
                m2tm * powerflow.sol["eigen"][de]
                + l2tm * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para + powerflow.nbus, de + powerflow.nbus] = (
                m2vk * powerflow.sol["eigen"][de]
                + l2vk * powerflow.sol["eigen"][de + powerflow.nbus]
            )
            powerflow.hessian[para + powerflow.nbus, para + powerflow.nbus] = (
                m2vm * powerflow.sol["eigen"][de]
                + l2vm * powerflow.sol["eigen"][de + powerflow.nbus]
            )

    # Elementos da diagonal principal da matriz jacobiana
    for idx, value in powerflow.dbarraDF.iterrows():
        hktk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalctk(powerflow=powerflow, idx=idx)
        hktm = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalctm(powerflow=powerflow, idx=idx)
        hkvk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalctk(powerflow=powerflow, idx=idx)
        hkvm = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalcvm(powerflow=powerflow, idx=idx)

        # Submatriz N
        nktk = (
            pcalctk(powerflow=powerflow, idx=idx)
            + (powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        nktm = (
            pcalctm(powerflow=powerflow, idx=idx)
            + (powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        nkvk = (
            pcalcvk(powerflow=powerflow, idx=idx)
            + (powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        nkvm = (
            pcalcvm(powerflow=powerflow, idx=idx)
            + (powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[idx]
        ) / powerflow.solution["voltage"][idx]

        # Submatriz M
        mktk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[
            idx
        ] + qcalctk(powerflow=powerflow, idx=idx)
        mktm = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[
            idx
        ] + qcalctm(powerflow=powerflow, idx=idx)
        mkvk = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[
            idx
        ] + qcalcvk(powerflow=powerflow, idx=idx)
        mkvm = -(powerflow.solution["voltage"][idx] ** 2) * powerflow.gdiag[
            idx
        ] + qcalcvm(powerflow=powerflow, idx=idx)

        # Submatriz L
        lktk = (
            qcalctk(powerflow=powerflow, idx=idx)
            - (powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        lktm = (
            qcalctm(powerflow=powerflow, idx=idx)
            - (powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        lkvk = (
            qcalcvk(powerflow=powerflow, idx=idx)
            - (powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[idx]
        ) / powerflow.solution["voltage"][idx]
        lkvm = (
            qcalcvm(powerflow=powerflow, idx=idx)
            - (powerflow.solution["voltage"][idx] ** 2) * powerflow.bdiag[idx]
        ) / powerflow.solution["voltage"][idx]

        powerflow.jacobiansym[idx, idx] = hk
        powerflow.jacobiansym[idx, idx + powerflow.nbus] = nk
        powerflow.jacobiansym[idx + powerflow.nbus, idx] = mk
        powerflow.jacobiansym[idx + powerflow.nbus, idx + powerflow.nbus] = lk

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controljacsym(
            powerflow,
        )

    w = [symbols("w%s" % i) for i in range(powerflow.jacobiansym.shape[0])]
    powerflow.dxfwsym = powerflow.jacobiansym.T @ w

    for k, _ in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            powerflow.hessiansym[k, m] = powerflow.dxfwsym[k].diff(t[m])
            powerflow.hessiansym[k, m + powerflow.nbus] = powerflow.dxfwsym[k].diff(
                v[m]
            )
            powerflow.hessiansym[k + powerflow.nbus, m] = powerflow.dxfwsym[
                k + powerflow.nbus
            ].diff(t[m])
            powerflow.hessiansym[
                k + powerflow.nbus, m + powerflow.nbus
            ] = powerflow.dxfwsym[k + powerflow.nbus].diff(v[m])

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controlhess(
            powerflow,
        )

    return t + v + l + w


def hessian(
    powerflow,
):

    ## Inicialização
    powerflow.dxfw = zeros((powerflow.dxfwsym.shape[0], 1), dtype=Symbol)
    powerflow.jacobian = zeros(
        (powerflow.jacobiansym.shape[0], powerflow.jacobiansym.shape[0]), dtype=Symbol
    )
    powerflow.hessian = zeros(
        (powerflow.hessiansym.shape[0], powerflow.hessiansym.shape[0]), dtype=Symbol
    )

    for k, _ in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            try:
                powerflow.jacobian[k, m] = powerflow.jacobiansym[k, m].subs(
                    powerflow.hessvar
                )
                powerflow.jacobian[k, m + powerflow.nbus] = powerflow.jacobiansym[
                    k, m + powerflow.nbus
                ].subs(powerflow.hessvar)
                powerflow.jacobian[k + powerflow.nbus, m] = powerflow.jacobiansym[
                    k + powerflow.nbus, m
                ].subs(powerflow.hessvar)
                powerflow.jacobian[
                    k + powerflow.nbus, m + powerflow.nbus
                ] = powerflow.jacobiansym[k + powerflow.nbus, m + powerflow.nbus].subs(
                    powerflow.hessvar
                )
            except:
                pass

            powerflow.hessian[k, m] = powerflow.hessiansym[k, m].subs(powerflow.hessvar)
            powerflow.hessian[k, m + powerflow.nbus] = powerflow.hessiansym[
                k, m + powerflow.nbus
            ].subs(powerflow.hessvar)
            powerflow.hessian[k + powerflow.nbus, m] = powerflow.hessiansym[
                k + powerflow.nbus, m
            ].subs(powerflow.hessvar)
            powerflow.hessian[
                k + powerflow.nbus, m + powerflow.nbus
            ] = powerflow.hessiansym[k + powerflow.nbus, m + powerflow.nbus].subs(
                powerflow.hessvar
            )

        powerflow.dxfw[k] = powerflow.dxfwsym[k].subs(powerflow.hessvar)
        powerflow.dxfw[k + powerflow.nbus] = powerflow.dxfwsym[k + powerflow.nbus].subs(
            powerflow.hessvar
        )

    powerflow.dxfw = reshape(powerflow.dxfw, (powerflow.dxfw.shape[0])).astype(float)
    powerflow.jacobian = powerflow.jacobian.astype(float)
    powerflow.hessian = powerflow.hessian.astype(float)
