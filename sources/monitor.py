# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

class Monitor:
    """classe para determinar a realização de monitoramento de valores"""

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
            if powerflow.monitor:
                setup.monitor = dict()
                # if not setup.monitor:
                self.monitor = {
                    'PFLOW': False, 
                    'PGMON': False, 
                    'QGMON': False, 
                    'VMON': False,
                    }
                
                self.checkmonitor(powerflow, setup,)

            else:
                setup.monitor = dict()
                print('\033[96mNenhuma opção de monitoramento foi escolhida.\033[0m')



    def checkmonitor(
        self,
        powerflow,
        setup,
    ):
        """verificação das opções de monitoramento escolhidas
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """
        
        ## Inicialização
        if powerflow.monitor:
            print('\033[96mOpções de monitoramento escolhidas: ', end='')
            for k, _ in self.monitor.items():
                if k in powerflow.monitor:
                    setup.monitor[k] = True
                    print(f'{k}', end=' ')
            print('\033[0m')
            print('\n')



    def monitorpflow(
        self,
        powerflow,
        method,
    ):
        """"""

        ## Inicialização
        pass



    def monitorpgmon(
        self,
        powerflow,
        method,
    ):
        """"""

        ## Inicialização
        pass



    def monitorqgmon(
        self,
        powerflow,
        method,
    ):
        """"""

        ## Inicialização
        pass



    def monitorvmon(
        self,
        powerflow,
        method,
    ):
        """"""

        ## Inicialização
        pass