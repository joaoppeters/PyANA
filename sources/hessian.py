# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import reshape, zeros
from sympy import Symbol, symbols
from sympy.functions import cos, sin

from calc import pcalcsym, qcalcsym
from ctrl import controlhess, controljacsym

def hessiansym(
    powerflow,
):
    '''cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # powerflow.hessvariáveis Simbólicas
    v = [symbols('v%d' % i) for i in range(powerflow.nbus)]
    t = [symbols('t%d' % i) for i in range(powerflow.nbus)]
    l = [symbols('l%d' % i) for i in range(1)]
    powerflow.jacobiansym = zeros((2*powerflow.nbus, 2*powerflow.nbus), dtype=Symbol)
    powerflow.hessiansym = zeros((2*powerflow.nbus, 2*powerflow.nbus), dtype=Symbol)

    for idx, value in powerflow.dlinhaDF.iterrows():
        if value['estado']:
            de = value['de'] - 1
            para = value['para'] - 1

            # elementos de,para
            h1 = (
                v[de]
                * v[para]
                * (
                    - powerflow.admitancia[idx].real
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
            n1 = v[de] * (
                - powerflow.admitancia[idx].real
                * cos(
                    t[de] - t[para]
                )
                - powerflow.admitancia[idx].imag
                * sin(
                    t[de] - t[para]
                )
            )
            m1 = (
                v[de]
                * v[para]
                * (
                    + powerflow.admitancia[idx].real
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
                - powerflow.admitancia[idx].real
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
                    + powerflow.admitancia[idx].real
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
                - powerflow.admitancia[idx].real
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
                    + powerflow.admitancia[idx].real
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
                + powerflow.admitancia[idx].real
                * sin(
                    t[de] - t[para]
                )
                + powerflow.admitancia[idx].imag
                * cos(
                    t[de] - t[para]
                )
            )
            
            powerflow.jacobiansym[de, para] = h1
            powerflow.jacobiansym[para, de] = h2

            powerflow.jacobiansym[de, para+powerflow.nbus] = n1
            powerflow.jacobiansym[para, de+powerflow.nbus] = n2

            powerflow.jacobiansym[de+powerflow.nbus, para] = m1
            powerflow.jacobiansym[para+powerflow.nbus, de] = m2

            powerflow.jacobiansym[de+powerflow.nbus, para+powerflow.nbus] = l1
            powerflow.jacobiansym[para+powerflow.nbus, de+powerflow.nbus] = l2

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

        powerflow.jacobiansym[idx, idx] = hk
        powerflow.jacobiansym[idx, idx+powerflow.nbus] = nk
        powerflow.jacobiansym[idx+powerflow.nbus, idx] = mk
        powerflow.jacobiansym[idx+powerflow.nbus, idx+powerflow.nbus] = lk
    
    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controljacsym(
            powerflow,
        )
    
    w = [symbols('w%s' % i) for i in range(powerflow.jacobiansym.shape[0])]
    powerflow.dxfwsym = powerflow.jacobiansym.T @ w

    for k,_ in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            powerflow.hessiansym[k,m] = powerflow.dxfwsym[k].diff(t[m])
            powerflow.hessiansym[k,m+powerflow.nbus] = powerflow.dxfwsym[k].diff(v[m])
            powerflow.hessiansym[k+powerflow.nbus,m] = powerflow.dxfwsym[k+powerflow.nbus].diff(t[m])
            powerflow.hessiansym[k+powerflow.nbus,m+powerflow.nbus] = powerflow.dxfwsym[k+powerflow.nbus].diff(v[m])

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
    powerflow.jacobian = zeros((powerflow.jacobiansym.shape[0], powerflow.jacobiansym.shape[0]), dtype=Symbol)
    powerflow.hessian = zeros((powerflow.hessiansym.shape[0], powerflow.hessiansym.shape[0]), dtype=Symbol)

    for k, _ in powerflow.dbarraDF.iterrows():
        for m, _ in powerflow.dbarraDF.iterrows():
            try:
                powerflow.jacobian[k,m] = powerflow.jacobiansym[k,m].subs(powerflow.hessvar)
                powerflow.jacobian[k,m+powerflow.nbus] = powerflow.jacobiansym[k,m+powerflow.nbus].subs(powerflow.hessvar)
                powerflow.jacobian[k+powerflow.nbus,m] = powerflow.jacobiansym[k+powerflow.nbus,m].subs(powerflow.hessvar)
                powerflow.jacobian[k+powerflow.nbus,m+powerflow.nbus] = powerflow.jacobiansym[k+powerflow.nbus,m+powerflow.nbus].subs(powerflow.hessvar)
            except:
                pass
                
            powerflow.hessian[k,m] = powerflow.hessiansym[k,m].subs(powerflow.hessvar)
            powerflow.hessian[k,m+powerflow.nbus] = powerflow.hessiansym[k,m+powerflow.nbus].subs(powerflow.hessvar)
            powerflow.hessian[k+powerflow.nbus,m] = powerflow.hessiansym[k+powerflow.nbus,m].subs(powerflow.hessvar)
            powerflow.hessian[k+powerflow.nbus,m+powerflow.nbus] = powerflow.hessiansym[k+powerflow.nbus,m+powerflow.nbus].subs(powerflow.hessvar)

        powerflow.dxfw[k] = powerflow.dxfwsym[k].subs(powerflow.hessvar)
        powerflow.dxfw[k+powerflow.nbus] = powerflow.dxfwsym[k+powerflow.nbus].subs(powerflow.hessvar)

    powerflow.dxfw = reshape(powerflow.dxfw, (powerflow.dxfw.shape[0])).astype(float)
    powerflow.jacobian = powerflow.jacobian.astype(float)
    powerflow.hessian = powerflow.hessian.astype(float)
