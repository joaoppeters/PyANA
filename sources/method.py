# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from continuation import Continuation
from convergence import Convergence
from folder import Folder
from linear import LinearPowerFlow
from monitor import Monitor
from newtonraphson import NewtonRaphson
from report import Reports
from statevar import StateVar

class Method():
    """classe para aplicação do método selecionado para análise de fluxo de potência"""

    def __init__(
        self,
        powerflow,
        ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        if (not hasattr(powerflow, 'sol')):
            # Chamada automática do método de solução selecionado
            self.method(powerflow,)



    def method(
        self,
        powerflow,
    ):
        """chamada automática do método de solução selecionado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Chamada específica método de Newton-Raphson Não-Linear
        if (powerflow.method == 'NEWTON'):
            NewtonRaphson(powerflow,)

        # Chamada específica método de Gauss-Seidel
        elif (powerflow.method == 'GAUSS'):
            self.gaussseidel(powerflow,)

        # Chamada específica método de Newton-Raphson Linearizado
        elif (powerflow.method == 'LINEAR'):
            LinearPowerFlow(powerflow,)

        # Chamada específica método Desacoplado
        elif (powerflow.method == 'DECOUP'):
            self.decoupledpowerflow(powerflow,)

        # Chamada específica método Desacoplado Rápido
        elif (powerflow.method == 'fDECOUP'):
            self.fastdecoupledpowerflow(powerflow,)

        # Chamada específica método Continuado
        elif (powerflow.method == 'CPF'):
            Continuation(powerflow,)


        # Armazenamento dos resultados
        Folder(powerflow.setup,).reports(powerflow.setup,)
        Reports(powerflow, powerflow.setup,)
        if (powerflow.method != 'CPF'):
            Monitor(powerflow, powerflow.setup,)
            Convergence(powerflow, powerflow.setup,)
            StateVar(powerflow, powerflow.setup,)