# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

class Control:
    """classe para determinar a realização das opções de controle escolhidas"""

    def __init__(
        self,
        powerflow,
        setup,
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        if not hasattr(powerflow, 'setup'):
            if powerflow.control:
                setup.control = dict()
                # if not setup.control:
                self.control = {
                    'CREM': False, 
                    'CST': False,
                    'CTAP': False,
                    'CTAPd': False,
                    'FREQ': False,
                    'QLIM': False,
                    'SVC' : False,
                    'VCTRL': False,
                    }
                
                self.checkcontrol(powerflow, setup,)

            else:
                setup.control = dict()
                print('\033[96mNenhuma opção de controle foi escolhida.\033[0m')



    def checkcontrol(
        self,
        powerflow,
        setup,
    ):
        """verificação das opções de controle escolhidas
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """
        
        ## Inicialização
        print('\033[96mOpções de controle escolhidas: ', end='')
        for k, _ in self.control.items():
            if k in powerflow.control:
                setup.control[k] = True
                print(f'{k}', end=' ')
        print('\033[0m')



    def ctrlcrem(
        self,
        powerflow,
    ):
        """controle remoto de tensão"""
        
        ## Inicialização
        pass



    def ctrlcst(
        self,
        powerflow,
    ):
        """controle secundário de tensão"""

        ## Inicialização
        pass



    def ctrlctap(
        self,
        powerflow,
    ):
        """controle de tap variável de transformador"""

        ## Inicialização
        pass



    def ctrlctapd(
        self,
        powerflow,
    ):
        """controle de ângulo de transformador defasador"""

        ## Inicialização
        pass



    def ctrlfreq(
        self,
        powerflow,
    ):
        """controle de regulação primária de frequência"""

        ## Inicialização
        pass



    def ctrlqlim(
        self,
        powerflow,
    ):
        """controle de limite de potência reativa"""

        ## Inicialização
        pass



    def ctrlsvc(
        self,
        powerflow,
    ):
        """controle de compensadores estáticos de potência reativa"""

        ## Inicialização
        pass



    def ctrlvctrl(
        self,
        powerflow,
    ):
        """controle de tensão de barramentos"""

        ## Inicialização
        pass