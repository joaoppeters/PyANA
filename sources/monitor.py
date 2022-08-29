# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from datetime import datetime as dt

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
        
        else:
            # Arquivo
            self.filedirname = powerflow.setup.dirRreports + powerflow.setup.name + '-monitor.txt'

            # Manipulação
            self.file = open(self.filedirname, 'w')

            # Cabeçalho
            self.rheader(powerflow,)

            # Relatórios Extras - ordem de prioridade
            if powerflow.setup.monitor:
                for r in powerflow.setup.monitor:
                    # monitoramento de fluxo de potência ativa em linhas de transmissão
                    if r == 'PFLOW':
                        self.monitorpflow(powerflow,)
                    # monitoramento de potência ativa gerada
                    elif r == 'PGMON':
                        self.monitorpgmon(powerflow,)
                    # monitoramento de potência reativa gerada
                    elif r == 'QGMON' and powerflow.method != 'LINEAR':
                        self.monitorqgmon(powerflow,)
                    # monitoramento de magnitude de tensão de barramentos
                    elif r == 'VMON':
                        self.monitorvmon(powerflow,)

            self.file.write('fim do relatório de monitoramento do sistema ' + powerflow.setup.name)
            self.file.close()



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



    def rheader(
        self,
        powerflow,
    ):
        """cabeçalho do relatório
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('{} {}, {}'.format(dt.now().strftime('%B'), dt.now().strftime('%d'), dt.now().strftime('%Y')))
        self.file.write('\n\n\n')
        self.file.write('relatório de monitoramento do sistema ' + powerflow.setup.name)
        self.file.write('\n')
        self.file.write('solução do fluxo de potência via método ')
        # Chamada específica método de Newton-Raphson Não-Linear
        if powerflow.method == 'NEWTON':
            self.file.write('newton-raphson')
        # Chamada específica método de Gauss-Seidel
        elif powerflow.method == 'GAUSS':
            self.file.write('gauss-seidel')
        # Chamada específica método de Newton-Raphson Linearizado
        elif powerflow.method == 'LINEAR':
            self.file.write('linearizado')
        # Chamada específica método Desacoplado
        elif powerflow.method == 'DECOUP':
            self.file.write('desacoplado')
        # Chamada específica método Desacoplado Rápido
        elif powerflow.method == 'fDECOUP':
            self.file.write('desacoplado rápido')
        # Chamada específica método Continuado
        elif powerflow.method == 'CPF':
            self.file.write('do fluxo de potência continuado')
        self.file.write('\n\n')
        self.file.write('opções de monitoramento ativadas: ')
        for k in powerflow.setup.monitor:
            self.file.write(f'{k} ')
        self.file.write('\n\n\n')



    def monitorpflow(
        self,
        powerflow,
    ):
        """monitoramento de fluxo de potência ativa em linhas de transmissão
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        pass



    def monitorpgmon(
        self,
        powerflow,
    ):
        """monitoramento de potência ativa gerada
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        pass



    def monitorqgmon(
        self,
        powerflow,
    ):
        """monitoramento de potência reativa gerada
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('vv monitoramento de potência reativa gerada vv')
        self.file.write('\n\n')
        qgmon = 0
        for i in range(0, powerflow.setup.nbus):
            if powerflow.setup.dbarraDF['tipo'][i] != 0:
                if powerflow.sol['reactive'][i] >= powerflow.setup.dbarraDF['potencia_reativa_maxima'][i]:
                    self.file.write('A geração de potência reativa da ' + powerflow.setup.dbarraDF['nome'][i] + ' violou o limite máximo estabelecido para análise ( {:.2f} >= {} ).'.format(powerflow.sol['reactive'][i], powerflow.setup.dbarraDF['potencia_reativa_maxima'][i]))
                    self.file.write('\n')
                elif powerflow.sol['reactive'][i] <= powerflow.setup.dbarraDF['potencia_reativa_minima'][i]:
                    self.file.write('A geração de potência reativa da ' + powerflow.setup.dbarraDF['nome'][i] + ' violou o limite mínimo estabelecido para análise ( {:.2f} <= {} ).'.format(powerflow.sol['reactive'][i], powerflow.setup.dbarraDF['potencia_reativa_minima'][i]))
                    self.file.write('\n')
                else:
                    qgmon += 1
        if qgmon == (powerflow.setup.npv + 1):
            self.file.write('Nenhuma barra de geração violou os limites máximo e mínimo de geração de potência reativa!')
        self.file.write('\n\n\n')



    def monitorvmon(
        self,
        powerflow,
    ):
        """monitoramento de magnitude de tensão de barramentos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('vv monitoramento de magnitude de tensão de barramentos vv')
        self.file.write('\n\n')
        vmon = 0
        for i in range(0, powerflow.setup.nbus):
            if powerflow.sol['voltage'][i] >= powerflow.setup.options['vmax']:
                self.file.write('A magnitude de tensão da ' + powerflow.setup.dbarraDF['nome'][i] + ' violou o limite máximo estabelecido para análise ( {:.3f} >= {} ).'.format(powerflow.sol['voltage'][i], powerflow.setup.options['vmax']))
                self.file.write('\n')
            elif powerflow.sol['voltage'][i] <= powerflow.setup.options['vmin']:
                self.file.write('A magnitude de tensão da ' + powerflow.setup.dbarraDF['nome'][i] + ' violou o limite mínimo estabelecido para análise ( {:.3f} <= {} ).'.format(powerflow.sol['voltage'][i], powerflow.setup.options['vmin']))
                self.file.write('\n')
            else:
                vmon += 1
        if vmon == powerflow.setup.nbus:
            self.file.write('Nenhum barramento violou os limites máximo e mínimo de magnitude de tensão!')
        self.file.write('\n\n\n')