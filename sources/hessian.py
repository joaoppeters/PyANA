# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import reshape, zeros
from sympy import Symbol, symbols
from sympy.functions import cos, sin

from calc import pcalcsym, qcalcsym
from ctrl import controlhess

def hessian_init(
    powerflow,
):
    '''cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variáveis Simbólicas
    v = [symbols('v%d' % i) for i in range(powerflow.nbus)]
    t = [symbols('t%d' % i) for i in range(powerflow.nbus)]
    l = [symbols('l%d' % i) for i in range(1)]
    w = [symbols('w%s' % i) for i in range(2*powerflow.nbus)]
    dxfw = zeros((2*powerflow.nbus, 1), dtype=Symbol)
    powerflow.hessian = zeros((2*powerflow.nbus, 2*powerflow.nbus), dtype=Symbol)

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value['estado']:
            de = value['de'] - 1
            para = value['para'] - 1

            # elementos de,para
            h1 = (
                v[de]
                * v[para]
                * (
                    -powerflow.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
            )
            n1 = -v[de] * (
                powerflow.admitancia[idx].real
                * cos(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    t[de] - t[para]
                )
            )
            m1 = (
                v[de]
                * v[para]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
            )
            l1 = v[de] * (
                -powerflow.admitancia[idx].real
                * sin(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    t[de] - t[para]
                )
            )

            # elementos para,de
            h2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
            )
            n2 = v[para] * (
                -powerflow.admitancia[idx].real
                * cos(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    t[de] - t[para]
                )
            )
            m2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    - powerflow.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
            )
            l2 = v[para] * (
                powerflow.admitancia[idx].real
                * sin(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    t[de] - t[para]
                )
            )
            
            dxfw[de] += h1*w[para] +n1*w[para+powerflow.nbus]
            dxfw[para] += h2*w[de] +n2*w[de+powerflow.nbus]
            dxfw[de+powerflow.nbus] += m1*w[para] +l1*w[para+powerflow.nbus]
            dxfw[para+powerflow.nbus] += m2*w[de] +l2*w[de+powerflow.nbus]

    # Elementos da diagonal principal da matriz jacobiana
    for idx, value in powerflow.dbarraDF.iterrows():
        hk = -(v[idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx)

        nk = (
            pcalcsym(powerflow=powerflow, v=v, t=t, idx=idx)
            + (v[idx] ** 2) * powerflow.gdiag[idx]
        ) / v[idx]

        mk = -(v[idx] ** 2) * powerflow.gdiag[idx] + qcalcsym(
            powerflow=powerflow, v=v, t=t, idx=idx
        )

        lk = (
            qcalcsym(powerflow=powerflow, v=v, t=t,idx=idx)
            - (v[idx] ** 2) * powerflow.bdiag[idx]
        ) / v[idx]

        dxfw[idx] += hk*w[idx] + nk*w[idx+powerflow.nbus]
        dxfw[idx+powerflow.nbus] += mk*w[idx] + lk*w[idx+powerflow.nbus]


    keys = t + v + l + w

    return dxfw, keys

def hessian(
        powerflow,
        dxfw,
        var,
        keys,
):
    
    ## Inicialização
    t = keys[:powerflow.nbus]
    v = keys[powerflow.nbus:2*powerflow.nbus]

    for k, kvalue in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            powerflow.hessian[k,m] = dxfw[k][0].diff(t[m]).subs(var)
            powerflow.hessian[k,m+powerflow.nbus] = dxfw[k][0].diff(v[m]).subs(var)
            powerflow.hessian[k+powerflow.nbus,m] = dxfw[k+powerflow.nbus][0].diff(t[m]).subs(var)
            powerflow.hessian[k+powerflow.nbus,m+powerflow.nbus] = dxfw[k+powerflow.nbus][0].diff(v[m]).subs(var)

        if kvalue['tipo'] == 2:
            powerflow.hessian[k,k] = 1e20
        
        if (powerflow.maskQ[k] == False) and (
            ("QLIM" not in powerflow.control)
            or ("QLIMs" not in powerflow.control)
            or ("QLIMn" not in powerflow.control)
        ):
            powerflow.hessian[k+powerflow.nbus,k+powerflow.nbus] = 1e20

        dxfw[k][0] = dxfw[k][0].subs(var)
        dxfw[k+powerflow.nbus][0] = dxfw[k+powerflow.nbus][0].subs(var)

    powerflow.dxfw = reshape(dxfw, (2*powerflow.nbus))
    powerflow.hessian = powerflow.hessian.astype(float)

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controlhess(
            powerflow,
        )

def hessian_init2(
    powerflow,
):
    '''cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variáveis Simbólicas
    v = [symbols('v%d' % i) for i in range(powerflow.nbus)]
    t = [symbols('t%d' % i) for i in range(powerflow.nbus)]
    l = [symbols('l%d' % i) for i in range(1)]
    w = [symbols('w%s' % i) for i in range(2*powerflow.nbus)]
    powerflow.hessiansymb = zeros((2*powerflow.nbus, 2*powerflow.nbus), dtype=Symbol)

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value['estado']:
            de = value['de'] - 1
            para = value['para'] - 1

            # elementos de,para
            h1 = (
                v[de]
                * v[para]
                * (
                    -powerflow.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
            )
            n1 = -v[de] * (
                powerflow.admitancia[idx].real
                * cos(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    t[de] - t[para]
                )
            )
            m1 = (
                v[de]
                * v[para]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
            )
            l1 = v[de] * (
                -powerflow.admitancia[idx].real
                * sin(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    t[de] - t[para]
                )
            )

            # elementos para,de
            h2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
            )
            n2 = v[para] * (
                -powerflow.admitancia[idx].real
                * cos(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * sin(
                    t[de] - t[para]
                )
            )
            m2 = (
                v[para]
                * v[de]
                * (
                    powerflow.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    - powerflow.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
            )
            l2 = v[para] * (
                powerflow.admitancia[idx].real
                * sin(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    t[de] - t[para]
                )
            )
            
            powerflow.hessiansymb[de, para] = h1
            powerflow.hessiansymb[para, de] = h2

            powerflow.hessiansymb[de, para+powerflow.nbus] = n1
            powerflow.hessiansymb[para, de+powerflow.nbus] = n2

            powerflow.hessiansymb[de+powerflow.nbus, para] = m1
            powerflow.hessiansymb[para+powerflow.nbus, de] = m2

            powerflow.hessiansymb[de+powerflow.nbus, para+powerflow.nbus] = l1
            powerflow.hessiansymb[para+powerflow.nbus, de+powerflow.nbus] = l2

    # Elementos da diagonal principal da matriz jacobiana
    for idx, value in powerflow.dbarraDF.iterrows():
        hk = -(v[idx] ** 2) * powerflow.bdiag[
            idx
        ] - qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx)

        nk = (
            pcalcsym(powerflow=powerflow, v=v, t=t, idx=idx)
            + (v[idx] ** 2) * powerflow.gdiag[idx]
        ) / v[idx]

        mk = -(v[idx] ** 2) * powerflow.gdiag[idx] + qcalcsym(
            powerflow=powerflow, v=v, t=t, idx=idx
        )

        lk = (
            qcalcsym(powerflow=powerflow, v=v, t=t,idx=idx)
            - (v[idx] ** 2) * powerflow.bdiag[idx]
        ) / v[idx]

        powerflow.hessiansymb[idx, idx] = hk
        powerflow.hessiansymb[idx, idx+powerflow.nbus] = nk
        powerflow.hessiansymb[idx+powerflow.nbus, idx] = mk
        powerflow.hessiansymb[idx+powerflow.nbus, idx+powerflow.nbus] = lk

    powerflow.dxfwsymb = powerflow.hessiansymb @ w

    keys = t + v + l + w

    return keys

def hessian2(
        powerflow,
        var,
        keys,
):
    
    ## Inicialização
    powerflow.dxfw = zeros((2*powerflow.nbus, 1), dtype=Symbol)
    powerflow.hessian = zeros((2*powerflow.nbus, 2*powerflow.nbus), dtype=Symbol)
    t = keys[:powerflow.nbus]
    v = keys[powerflow.nbus:2*powerflow.nbus]

    for k,_ in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            powerflow.hessian[k,m] = powerflow.dxfwsymb[k].diff(t[m]).subs(var)
            powerflow.hessian[k,m+powerflow.nbus] = powerflow.dxfwsymb[k].diff(v[m]).subs(var)
            powerflow.hessian[k+powerflow.nbus,m] = powerflow.dxfwsymb[k+powerflow.nbus].diff(t[m]).subs(var)
            powerflow.hessian[k+powerflow.nbus,m+powerflow.nbus] = powerflow.dxfwsymb[k+powerflow.nbus].diff(v[m]).subs(var)

        powerflow.dxfw[k] = powerflow.dxfwsymb[k].subs(var)
        powerflow.dxfw[k+powerflow.nbus] = powerflow.dxfwsymb[k+powerflow.nbus].subs(var)

    powerflow.dxfw = reshape(powerflow.dxfw, (2*powerflow.nbus))
    powerflow.hessian = powerflow.hessian.astype(float)

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controlhess(
            powerflow,
        )
