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
    '''classe para construção da matriz Hessiana'''

    def hessian(
        self,
        powerflow,
    ):
        '''cálculo das submatrizes da matriz Hessiana

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Variáveis Simbólicas
        v = [symbols('v%d' % i) for i in range(powerflow.nbusnbus)]
        t = [symbols('t%d' % i) for i in range(powerflow.nbusnbus)]
        powerflow.jacosymb = empty((2*powerflow.nbusnbus, 2*powerflow.nbusnbus), dtype=Symbol)

        for idx, value in powerflow.dlinhaDF.iterrows():
            if value['estado']:
                de = value['de'] - 1
                para = value['para'] - 1

                # elementos de,para
                h1 = (
                    v[de]
                    * v[para]
                    * (
                        -powerflow.nbusadmitancia[idx].real
                        * sin(
                            t[de]
                            - t[para]
                        )
                        + powerflow.nbusadmitancia[idx].imag
                        * cos(
                            t[de]
                            - t[para]
                        )
                    )
                )
                n1 = -v[de] * (
                    powerflow.nbusadmitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.nbusadmitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
                m1 = (
                    v[de]
                    * v[para]
                    * (
                        powerflow.nbusadmitancia[idx].real
                        * cos(
                            t[de]
                            - t[para]
                        )
                        + powerflow.nbusadmitancia[idx].imag
                        * sin(
                            t[de]
                            - t[para]
                        )
                    )
                )
                l1 = v[de] * (
                    -powerflow.nbusadmitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.nbusadmitancia[idx].imag
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
                        powerflow.nbusadmitancia[idx].real
                        * sin(
                            t[de]
                            - t[para]
                        )
                        + powerflow.nbusadmitancia[idx].imag
                        * cos(
                            t[de]
                            - t[para]
                        )
                    )
                )
                n2 = v[para] * (
                    -powerflow.nbusadmitancia[idx].real
                    * cos(
                        t[de]
                        - t[para]
                    )
                    + powerflow.nbusadmitancia[idx].imag
                    * sin(
                        t[de]
                        - t[para]
                    )
                )
                m2 = (
                    v[para]
                    * v[de]
                    * (
                        powerflow.nbusadmitancia[idx].real
                        * cos(
                            t[de]
                            - t[para]
                        )
                        - powerflow.nbusadmitancia[idx].imag
                        * sin(
                            t[de]
                            - t[para]
                        )
                    )
                )
                l2 = v[para] * (
                    powerflow.nbusadmitancia[idx].real
                    * sin(
                        t[de]
                        - t[para]
                    )
                    + powerflow.nbusadmitancia[idx].imag
                    * cos(
                        t[de]
                        - t[para]
                    )
                )
                
                powerflow.jacobsymb[de][para] = h1
                powerflow.jacobsymb[de][para + powerflow.nbusnbus] = n1
                powerflow.jacobsymb[de + powerflow.nbusnbus][para] = m1
                powerflow.jacobsymb[de + powerflow.nbusnbus][para + powerflow.nbusnbus] = l1  
                
                powerflow.jacobsymb[para][de] = h2
                powerflow.jacobsymb[para][de + powerflow.nbusnbus] = n2
                powerflow.jacobsymb[para + powerflow.nbusnbus][de] = m2
                powerflow.jacobsymb[para + powerflow.nbusnbus][de + powerflow.nbusnbus] = l2  

        # Elementos da diagonal principal da matriz jacobiana
        for idx, value in powerflow.dbarraDF.iterrows():
            # Submatriz H
            if (
                powerflow.nbusmaskP[idx] == False
            ):  # A presença do módulo se deve ao tratamento de limites (QLIM), que pode converter barra tipo 2 em -2
                hk = oo

            else:
                hk = -(v[idx] ** 2) * powerflow.nbusbdiag[
                    idx
                ] - PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,)

            # Submatriz N
            nk = (PQCalc().pcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,) + (v[idx] ** 2) * powerflow.nbusgdiag[
                    idx
                ]) / v[idx]

            # Submatriz M
            mk = -(v[idx] ** 2) * powerflow.nbusgdiag[
                    idx
                ] + PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,)

            # Submatriz L
            if (powerflow.nbusmaskQ[idx] == False) and (
                ('QLIM' not in powerflow.control)
                or ('QLIMs' not in powerflow.control)
                or ('QLIMn' not in powerflow.control)
            ):
                lk = oo
            else:
                lk = (PQCalc().qcalcsym(powerflow=powerflow, v=v, t=t, idx=idx,) - (v[idx] ** 2) * powerflow.nbusbdiag[
                    idx
                ]) / v[idx]
                    
        w = Matrix(
            ([[symbols('w%s' % i)] for i in range(2*powerflow.nbusnbus)]), 
        )
        
        powerflow.jacobsymb = powerflow.jacobsymb * w

        # Submatrizes de controles ativos
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow,).controljac(
                powerflow,
            )