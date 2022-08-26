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
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        if powerflow.control:
            ## Inicialização
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
            
            print('\033[96mOpções de controle escolhidas: ', end='')
            for k, _ in self.control.items():
                if k in powerflow.control:
                    self.control[k] = True
                    print(f'{k}', end=' ')
            print('\033[0m')

            powerflow.control = self.control

        else:
            print('\033[96mNenhuma opção de controle foi escolhida.\033[0m')