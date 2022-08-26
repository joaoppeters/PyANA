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
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        if powerflow.mon:
            ## Inicialização
            self.monitor = {
                'PFLOW': False, 
                'PGMON': False, 
                'QGMON': False, 
                'VMON': False,
                }

            print('\033[96mOpções de monitoramento escolhidas: ', end='')
            for k, _ in self.monitor.items():
                if k in powerflow.mon:
                    self.monitor[k] = True
                    print(f'{k}', end=' ')
            print('\033[0m')
            print('\n')

            powerflow.mon = self.monitor

        else:
            print('\033[96mNenhuma opção de monitoramento foi escolhida.\033[0m')