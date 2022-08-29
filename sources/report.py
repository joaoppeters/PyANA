# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from datetime import datetime as dt
from numpy import abs, degrees, sum

class Reports:
    """classe para geração e armazenamento automático de relatórios"""

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
            if powerflow.report:
                setup.report = dict()
                # if not setup.report:
                self.report = {
                    'RBARRA': False, 
                    'RLINHA': False, 
                    'RGERA': False, 
                    'RSVC': False,
                    'RCPF': False,
                    }
                
                self.checkreport(powerflow, setup,)

            else:
                setup.report = dict()
                print('\033[96mNenhuma opção de relatório foi escolhida.\033[0m')

        else:
            # Arquivo
            self.filedirname = powerflow.setup.dirRreports + powerflow.setup.name + '-report.txt'

            # Manipulação
            self.file = open(self.filedirname, 'w')

            # Cabeçalho
            self.rheader(powerflow,)

            # Relatório de Convergência
            self.rconv(powerflow,)

            # Relatórios Extras - ordem de prioridade
            if powerflow.setup.report:
                for r in powerflow.setup.report:
                    # relatório de barra
                    if r == 'RBARRA':
                        self.rbarra(powerflow,)
                    # relatório de linha
                    elif r == 'RLINHA':
                        self.rlinha(powerflow,)
                    # relatório de geradores
                    elif r == 'RGERA':
                        self.rgera(powerflow,)
                    # relatório de compensadores estáticos de potência reativa
                    elif r == 'RSVC':
                        self.rsvc(powerflow,)
                    # relatório de fluxo de potência continuado
                    elif r == 'RCPF':
                        self.rcpf(powerflow,)

            self.file.write('fim do relatório do sistema ' + powerflow.setup.name)
            self.file.close()



    def checkreport(
        self,
        powerflow,
        setup,
    ):
        """verificação das opções de relatório escolhidas
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """
        
        ## Inicialização
        if powerflow.report:
            print('\033[96mOpções de relatório escolhidas: ', end='')
            for k, _ in self.report.items():
                if k in powerflow.report:
                    setup.report[k] = True
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
        self.file.write('relatório do sistema ' + powerflow.setup.name)
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
        self.file.write('opções de relatório ativadas: ')
        for k in powerflow.setup.report:
            self.file.write(f'{k} ')
        self.file.write('\n\n\n\n')



    def rconv(
        self,
        powerflow,
    ):
        """relatório de convergência
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('vv relatório de convergência vv')
        self.file.write('\n\n')
        self.file.write('       | FREQ | ERROR | BARRA | ERROR | BARRA |')
        self.file.write('\n')
        self.file.write('| ITER |   Hz |    MW |   NUM |  Mvar |   NUM |')
        self.file.write('\n')
        self.file.write('-'*47)
        for i in range(0, powerflow.sol['iter']):
            self.file.write('\n')
            self.file.write(f"| {(i+1):>4d} | {powerflow.sol['freq'][i]:^4.1f} | {powerflow.sol['convP'][i]*powerflow.setup.options['sbase']:>5.2f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busP'][i]]:>5d} | {powerflow.sol['convQ'][i]*powerflow.setup.options['sbase']:>5.2f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busQ'][i]]:>5d} |")
        self.file.write('\n')
        self.file.write('-'*47)
        self.file.write('\n\n')
        self.file.write(powerflow.sol['convergence'])
        self.file.write('\n\n')
        self.file.write('       | FREQ | ERROR | BARRA | ERROR | BARRA |')
        self.file.write('\n')
        self.file.write('| ITER |   Hz |    MW |   NUM |  Mvar |   NUM |')
        self.file.write('\n')
        self.file.write('-'*47)
        self.file.write('\n')
        self.file.write(f"| {(i+1):>4d} | {powerflow.sol['freq'][i+1]:^4.1f} | {powerflow.sol['convP'][i+1]*powerflow.setup.options['sbase']:>5.2f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busP'][i+1]]:>5d} | {powerflow.sol['convQ'][i+1]*powerflow.setup.options['sbase']:>5.2f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busQ'][i+1]]:>5d} |")
        self.file.write('\n')
        self.file.write('-'*47)
        self.file.write('\n\n\n\n')



    def rbarra(
        self,
        powerflow,
    ):
        """relatório de barra
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('vv relatório de barras vv')
        self.file.write('\n\n')
        self.file.write('|        BARRA       |      TENSAO     |        GERACAO      |       CARGA      |  SHUNT  |')
        self.file.write('\n')
        self.file.write('| NUM |   NOME   | T |   MOD  |   ANG  |    MW    |   Mvar   |   MW   |   Mvar  |   Mvar  |')
        self.file.write('\n')
        self.file.write('-'*91)
        for i in range(0, powerflow.setup.nbus):
            if i % 10 == 0 and i != 0:
                self.file.write('\n\n')
                self.file.write('|        BARRA       |      TENSAO     |        GERACAO      |       CARGA      |  SHUNT  |')
                self.file.write('\n')
                self.file.write('| NUM |   NOME   | T |   MOD  |   ANG  |    MW    |   Mvar   |   MW   |   Mvar  |   Mvar  |')
                self.file.write('\n')
                self.file.write('-'*91)

            self.file.write('\n')
            self.file.write(f"| {powerflow.setup.dbarraDF['numero'][i]:^3d} | {powerflow.setup.dbarraDF['nome'][i]:<8} | {powerflow.setup.dbarraDF['tipo'][i]:^1} |  {powerflow.sol['voltage'][i]:<5.3f} | {degrees(powerflow.sol['theta'][i]):>+6.2f} | {powerflow.sol['active'][i]:>8.2f} | {powerflow.sol['reactive'][i]:>8.2f} | {powerflow.setup.dbarraDF['demanda_ativa'][i]:>6.2f} | {powerflow.setup.dbarraDF['demanda_reativa'][i]:>7.2f} | {(powerflow.sol['voltage'][i]**2)*powerflow.setup.dbarraDF['shunt_barra'][i]:>7.2f} |")
            self.file.write('\n')
            self.file.write('-'*91)
        self.file.write('\n\n\n\n')



    def rlinha(
        self,
        powerflow,
    ):
        """relatório de linha
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.file.write('vv relatório de linhas vv')
        self.file.write('\n\n')
        self.file.write('|        BARRA        |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |')
        self.file.write('\n')
        self.file.write('|    DE    |   PARA   |   Pkm[MW]  |  Qkm[Mvar] |   Pmk[MW]  |  Qmk[Mvar] |    MW   |  Mvar  |')
        self.file.write('\n')
        self.file.write('-'*94)
        # self.file.write('\n')
        for i in range(0, powerflow.setup.nlin):
            if i % 10 == 0 and i != 0:
                self.file.write('\n\n')
                self.file.write('|        BARRA        |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |')
                self.file.write('\n')
                self.file.write('|    DE    |   PARA   |   Pkm[MW]  |  Qkm[Mvar] |   Pmk[MW]  |  Qmk[Mvar] |    MW   |  Mvar  |')
                self.file.write('\n')
                self.file.write('-'*94)

            self.file.write('\n')
            self.file.write(f"| {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['de'][i] - 1]:<8} | {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['para'][i] - 1]:<8} | {powerflow.sol['active_flow_F2'][i]:>+10.3f} | {powerflow.sol['reactive_flow_F2'][i]:>+10.3f} | {powerflow.sol['active_flow_2F'][i]:>+10.3f} | {powerflow.sol['reactive_flow_2F'][i]:>+10.3f} | {abs(abs(powerflow.sol['active_flow_F2'][i])-abs(powerflow.sol['active_flow_2F'][i])):>7.3f} | {abs(abs(powerflow.sol['reactive_flow_F2'][i])-abs(powerflow.sol['reactive_flow_2F'][i])):>6.3f} |")
            self.file.write('\n')
            self.file.write('-'*94)
        self.file.write('\n\n')
        self.file.write('| GERACAO |  CARGA  | SHUNT | PERDAS |')
        self.file.write('\n')
        self.file.write('|      MW |      MW |    MW |     MW | ')
        self.file.write('\n')
        self.file.write('|    Mvar |    Mvar |  Mvar |   Mvar |')
        self.file.write('\n')
        self.file.write('-'*38)
        self.file.write('\n')
        self.file.write(f"| {sum(powerflow.sol['active']):>+7.2f} | {sum(powerflow.setup.dbarraDF['demanda_ativa']):>+7.2f} |   0.0 | {sum(abs(abs(powerflow.sol['active_flow_F2'])-abs(powerflow.sol['active_flow_2F']))):>6.3f} |")
        self.file.write('\n')
        self.file.write(f"| {sum(powerflow.sol['reactive']):>+7.2f} | {sum(powerflow.setup.dbarraDF['demanda_reativa']):>+7.2f} | {sum((powerflow.sol['voltage']**2)*powerflow.setup.dbarraDF['shunt_barra'].values.T):>5.2f} | {sum(abs(abs(powerflow.sol['reactive_flow_F2'])-abs(powerflow.sol['reactive_flow_2F']))):>6.3f} |")
        self.file.write('\n')
        self.file.write('-'*38)
        self.file.write('\n')
        self.file.write('\n\n\n\n')



    def rgera(
        self,
        powerflow,
    ):
        """relatório de geradores
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização


    
    def rsvc(
        self,
        powerflow,
    ):
        """relatório de compensadores estáticos de potência reativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização


    
    def rcpf(
        self,
        powerflow,
    ):
        """relatório de fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização