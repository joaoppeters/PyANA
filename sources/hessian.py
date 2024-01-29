# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, zeros, empty
from scipy.sparse import csc_matrix
from sympy import oo, Symbol, symbols, MatrixSymbol, Matrix
from sympy.functions import cos, sin


from calc import PQCalc
from ctrl import Control


class Hessian:
    """classe para construção da matriz Hessiana"""

    def hessian(
        self,
        powerflow,
    ):
        """cálculo das submatrizes da matriz Hessiana

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis Simbólicas
        v = [symbols('v%d' % i) for i in range(powerflow.setup.nbus)]
        t = [symbols('t%d' % i) for i in range(powerflow.setup.nbus)]
        powerflow.jacosymb = empty((2*powerflow.setup.nbus, 2*powerflow.setup.nbus), dtype=Symbol)

        for idx, value in powerflow.setup.dlinhaDF.iterrows():
            if value['estado']:
                de = value['de'] - 1
                para = value['para'] - 1

                # elementos de,para
                h1 = (
                    v[de]
                    * v[para]
                    * (
                        -powerflow.setup.admitancia[idx].real
                        * sin(
                            t[de]
                            - t[para]
                        )
                        + powerflow.setup.admitancia[idx].imag
                        * cos(
                            t[de]
                            - t[para]
                        )
                    )
                )
                n1 = -v[de] * (
                    powerflow.setup.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.setup.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
                m1 = (
                    v[de]
                    * v[para]
                    * (
                        powerflow.setup.admitancia[idx].real
                        * cos(
                            t[de]
                            - t[para]
                        )
                        + powerflow.setup.admitancia[idx].imag
                        * sin(
                            t[de]
                            - t[para]
                        )
                    )
                )
                l1 = v[de] * (
                    -powerflow.setup.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.setup.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )

                # elementos para,de
                h2 = (
                    v[para]
                    * v[de]
                    * (
                        powerflow.setup.admitancia[idx].real
                        * sin(
                            t[de]
                            - t[para]
                        )
                        + powerflow.setup.admitancia[idx].imag
                        * cos(
                            t[de]
                            - t[para]
                        )
                    )
                )
                n2 = v[para] * (
                    -powerflow.setup.admitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.setup.admitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
                m2 = (
                    v[para]
                    * v[de]
                    * (
                        powerflow.setup.admitancia[idx].real
                        * cos(
                            t[de]
                            - t[para]
                        )
                        - powerflow.setup.admitancia[idx].imag
                        * sin(
                            t[de]
                            - t[para]
                        )
                    )
                )
                l2 = v[para] * (
                    powerflow.setup.admitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.setup.admitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
                
                powerflow.jacobsymb[de][para] = h1
                powerflow.jacobsymb[de][para + powerflow.setup.nbus] = n1
                powerflow.jacobsymb[de + powerflow.setup.nbus][para] = m1
                powerflow.jacobsymb[de + powerflow.setup.nbus][para + powerflow.setup.nbus] = l1  
                
                powerflow.jacobsymb[para][de] = h2
                powerflow.jacobsymb[para][de + powerflow.setup.nbus] = n2
                powerflow.jacobsymb[para + powerflow.setup.nbus][de] = m2
                powerflow.jacobsymb[para + powerflow.setup.nbus][de + powerflow.setup.nbus] = l2  

        # Elementos da diagonal principal da matriz jacobiana
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Submatriz H
            if (
                powerflow.setup.maskP[idx] == False
            ):  # A presença do módulo se deve ao tratamento de limites (QLIM), que pode converter barra tipo 2 em -2
                hk = oo

            else:
                hk = -(v[idx] ** 2) * powerflow.setup.bdiag[
                    idx
                ] - PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,)

            # Submatriz N
            nk = (PQCalc().pcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,) + (v[idx] ** 2) * powerflow.setup.gdiag[
                    idx
                ]) / v[idx]

            # Submatriz M
            mk = -(v[idx] ** 2) * powerflow.setup.gdiag[
                    idx
                ] + PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,)

            # Submatriz L
            if (powerflow.setup.maskQ[idx] == False) and (
                ("QLIM" not in powerflow.setup.control)
                or ("QLIMs" not in powerflow.setup.control)
                or ("QLIMn" not in powerflow.setup.control)
            ):
                lk = oo
            else:
                lk = (PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,) - (v[idx] ** 2) * powerflow.setup.bdiag[
                    idx
                ]) / v[idx]
                    
        w = Matrix(
            ([[symbols('w%s' % i)] for i in range(2*powerflow.setup.nbus)]), 
        )
        
        powerflow.jacobsymb = powerflow.jacobsymb * w

        # Submatrizes de controles ativos
        if powerflow.setup.controlcount > 0:
            Control(powerflow, powerflow.setup,).controljac(
                powerflow,
            )
