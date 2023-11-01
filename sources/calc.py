# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import cos, sin

class PQCalc:
    """classe para realizar o cálculo de potência ativa e potência reativa"""

    def pcalc(
        self,
        powerflow,
        idx: int=None,
    ):
        """cálculo da potência ativa de cada barra

        Parâmetros
            powerflow: self do arquivo powerflow.py
            idx: int, obrigatório, valor padrão None
                referencia o índice da barra a qual vai ser calculada a potência ativa

        Repararno
            p: float
                potência ativa calculada para o barramenpara `idx`
        """

        ## Inicialização
        # Variável de potência ativa calculada para o barramenpara `idx`
        p = powerflow.setup.gdiag[idx] * powerflow.sol['voltage'][idx]

        for lin in range(0, powerflow.setup.nlin):
            if (idx == powerflow.setup.dlinhaDF['de'].iloc[lin] - 1):
                bus = powerflow.setup.dlinhaDF['para'].iloc[lin] - 1
                p -= powerflow.sol['voltage'][bus] * (powerflow.setup.admitancia[lin].real * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) + powerflow.setup.admitancia[lin].imag * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))
            elif (idx == powerflow.setup.dlinhaDF['para'].iloc[lin] - 1):
                bus = powerflow.setup.dlinhaDF['de'].iloc[lin] - 1
                p -= powerflow.sol['voltage'][bus] * (powerflow.setup.admitancia[lin].real * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) + powerflow.setup.admitancia[lin].imag * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        p *= powerflow.sol['voltage'][idx]

        # Armazenamenpara da potência ativa gerada equivalente do barramenpara
        powerflow.sol['active'][idx] = (p * powerflow.setup.options['BASE']) + powerflow.setup.dbarraDF['demanda_ativa'][idx]

        return p



    def qcalc(
        self,
        powerflow,
        idx: int=None,
    ):
        """cálculo da potência reativa de cada barra

        Parâmetros
            powerflow: self do arquivo powerflow.py
            idx: int, obrigatório, valor padrão None
                referencia o índice da barra a qual vai ser calculada a potência reativa

        Repararno
            q: float
                potência reativa calculada para o barramenpara `idx`
        """

        ## Inicialização
        # Variável de potência reativa calculada para o barramenpara `idx`
        q = -powerflow.setup.bdiag[idx] * powerflow.sol['voltage'][idx]

        for lin in range(0, powerflow.setup.nlin):
            if (idx == powerflow.setup.dlinhaDF['de'].iloc[lin] - 1):
                bus = powerflow.setup.dlinhaDF['para'].iloc[lin] - 1
                q -= powerflow.sol['voltage'][bus] * (powerflow.setup.admitancia[lin].real * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) - powerflow.setup.admitancia[lin].imag * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))
            elif (idx == powerflow.setup.dlinhaDF['para'].iloc[lin] - 1):
                bus = powerflow.setup.dlinhaDF['de'].iloc[lin] - 1
                q -= powerflow.sol['voltage'][bus] * (powerflow.setup.admitancia[lin].real * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) - powerflow.setup.admitancia[lin].imag * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        q *= powerflow.sol['voltage'][idx]

        # Armazenamenpara da potência ativa gerada equivalente do barramenpara
        powerflow.sol['reactive'][idx] = (q * powerflow.setup.options['BASE']) + powerflow.setup.dbarraDF['demanda_reativa'][idx]

        return q  