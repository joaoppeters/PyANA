# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import Folder
from monitor import Monitor
from report import Reports

class Method:
    """classe para aplicação do método selecionado para análise de fluxo de potência"""

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
        if powerflow.method == "NEWTON":
            from admittance import Ybus
            from newtonraphson import NewtonRaphson
            
            Ybus(powerflow,).admit(
                powerflow,
            )
            
            NewtonRaphson().newtonraphson(
                powerflow,
            )

        # Chamada específica método de Gauss-Seidel
        elif powerflow.method == "GAUSS":
            self.gaussseidel(
                powerflow,
            )

        # Chamada específica método de Newton-Raphson Linearizado
        elif powerflow.method == "LINEAR":
            from admittance import Ybus
            from linear import LinearPF

            Ybus(powerflow,).admitLinear(
                powerflow,
            )
            
            LinearPF().linear(
                powerflow,
            )

        # Chamada específica método Desacoplado
        elif powerflow.method == "DECOUP":
            self.decoupledpowerflow(
                powerflow,
            )

        # Chamada específica método Desacoplado Rápido
        elif powerflow.method == "fDECOUP":
            self.fastdecoupledpowerflow(
                powerflow,
            )

        # Chamada específica método Continuado
        elif powerflow.method == "CPF":
            from admittance import Ybus
            from continuation import Continuation
            from newtonraphson import NewtonRaphson
                    
            Ybus(powerflow,).admit(
                powerflow,
            )
            
            NewtonRaphson().newtonraphson(
                powerflow,
            )
            
            Continuation().cpf(
                powerflow,
            )

        # Chamada especifica metodo Cross-Entropy
        elif powerflow.method == "CENT":
            from admittance import Ybus
            from crossentropy import CrossEntropy
            
            Ybus(powerflow,).admit(
                powerflow,
            )
            
            CrossEntropy(
                powerflow,
            )

        # Chamada especifica geracao estocastica inicial de valores
        if powerflow.method == "STOCH":
            from admittance import Ybus
            from stochastic import Stochastic
            
            Ybus(powerflow,).admit(
                powerflow,
            )
            
            Stochastic(
                powerflow.method,
                self,
            )
            
        # Chamada especifica metodo direto (Canizares, 1993)
        if powerflow.method == 'CANI':
            from admittance import Ybus
            from directmethod import DirectMethod
            
            Ybus(powerflow,).admit(
                powerflow,
            )
            
            DirectMethod().directmethod(
                powerflow,
            )

        # Armazenamento dos resultados
        Folder(powerflow.setup,).reports(
            powerflow.setup,
        )
        Reports(
            powerflow,
            powerflow.setup,
        )
        if powerflow.method != "CPF":
            Monitor(
                powerflow,
                powerflow.setup,
            )
            # Convergence(powerflow, powerflow.setup,)
            # StateVar(powerflow, powerflow.setup,)