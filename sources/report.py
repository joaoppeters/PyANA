# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from datetime import datetime as dt
from numpy import abs, argsort, column_stack, degrees, savetxt, sum

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
            if powerflow.method == 'CPF':
                self.rcpf(powerflow,)
                self.tobecontinued(powerflow,)

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
        self.file.write('\n\n')
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
        self.file.write('opções de controle ativadas: ')
        if powerflow.setup.control:
            for k in powerflow.setup.control:
                self.file.write(f'{k} ')
        else:
            self.file.write('Nenhum controle ativo!')
        self.file.write('\n\n')
        self.file.write('opções de relatório ativadas: ')
        if powerflow.setup.report:
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
        if powerflow.method != 'LINEAR':
            self.file.write('\n\n')
            self.file.write('       |  FREQ  |  ERROR  | BARRA |  ERROR  | BARRA |  ERROR  | BARRA |')
            self.file.write('\n')
            self.file.write('| ITER |    Hz  |     MW  |   NUM |   Mvar  |   NUM |   CTRL  |   NUM |')
            self.file.write('\n')
            self.file.write('-'*71)
            if powerflow.method != 'CPF':
                for i in range(0, powerflow.sol['iter']):
                    self.file.write('\n')
                    self.file.write(f"| {(i+1):^4d} | {powerflow.sol['freqiter'][i]:^6.3f} | {powerflow.sol['convP'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busP'][i]]:^5d} | {powerflow.sol['convQ'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busQ'][i]]:^5d} | {powerflow.sol['convY'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busY'][i]]:^5d} |")
            
            elif powerflow.method == 'CPF':
                for i in range(0, powerflow.case[0]['iter']):
                    self.file.write('\n')
                    self.file.write(f"| {(i+1):^4d} | {powerflow.case[0]['freqiter'][i]:^6.3f} | {powerflow.case[0]['convP'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busP'][i]]:^5d} | {powerflow.case[0]['convQ'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busQ'][i]]:^5d} | {powerflow.case[0]['convY'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busY'][i]]:^5d} |")
            
            self.file.write('\n')
            self.file.write('-'*71)
        if powerflow.method == 'LINEAR':
            i = powerflow.sol['iter'] - 2
        self.file.write('\n\n')
        self.file.write(' * * * * ' + powerflow.sol['convergence'] + ' * * * * ')
        self.file.write('\n\n')
        self.file.write('       |  FREQ  |  ERROR  | BARRA |  ERROR  | BARRA |  ERROR  | BARRA |')
        self.file.write('\n')
        self.file.write('| ITER |    Hz  |     MW  |   NUM |   Mvar  |   NUM |   CTRL  |   NUM |')
        self.file.write('\n')
        self.file.write('-'*71)
        self.file.write('\n')
        if powerflow.method != 'CPF':
            self.file.write(f"| {(i+1):^4d} | {powerflow.sol['freqiter'][i]:^6.3f} | {powerflow.sol['convP'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busP'][i]]:^5d} | {powerflow.sol['convQ'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busQ'][i]]:^5d} | {powerflow.sol['convY'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.sol['busY'][i]]:^5d} |")
    
        elif powerflow.method == 'CPF':
            self.file.write(f"| {(i+1):^4d} | {powerflow.case[0]['freqiter'][i]:^6.3f} | {powerflow.case[0]['convP'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busP'][i]]:^5d} | {powerflow.case[0]['convQ'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busQ'][i]]:^5d} | {powerflow.case[0]['convY'][i]*powerflow.setup.options['sbase']:^7.3f} | {powerflow.setup.dbarraDF['numero'][powerflow.case[0]['busY'][i]]:^5d} |")
        
        self.file.write('\n')
        self.file.write('-'*71)
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
        # Loop por área
        for area in powerflow.setup.dbarraDF['area'].unique():
            self.file.write('vv relatório de barras vv área {} vv'.format(area))
            self.file.write('\n\n')
            self.file.write('|          BARRA          |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |')
            self.file.write('\n')
            self.file.write('| NUM |     NOME    |  T  |    MOD    |    ANG   |    MW    |   Mvar   |    MW    |   Mvar   |    Mvar  |')
            self.file.write('\n')
            self.file.write('-'*105)
            for i in range(0, powerflow.setup.nbus):
                if powerflow.setup.dbarraDF['area'][i] == area:
                    if i % 10 == 0 and i != 0:
                        self.file.write('\n\n')
                        self.file.write('|          BARRA          |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |')
                        self.file.write('\n')
                        self.file.write('| NUM |     NOME    |  T  |    MOD    |    ANG   |    MW    |   Mvar   |    MW    |   Mvar   |    Mvar  |')
                        self.file.write('\n')
                        self.file.write('-'*105)

                    self.file.write('\n')
                    if powerflow.method != 'CPF':
                        self.file.write(f"| {powerflow.setup.dbarraDF['numero'][i]:^3d} | {powerflow.setup.dbarraDF['nome'][i]:^11} | {powerflow.setup.dbarraDF['tipo'][i]:^3} |  {powerflow.sol['voltage'][i]:^8.3f} | {degrees(powerflow.sol['theta'][i]):^+8.2f} | {powerflow.sol['active'][i]:^8.3f} | {powerflow.sol['reactive'][i]:^8.3f} | {powerflow.setup.dbarraDF['demanda_ativa'][i]:^8.3f} | {powerflow.setup.dbarraDF['demanda_reativa'][i]:^8.3f} | {(powerflow.sol['voltage'][i]**2)*powerflow.setup.dbarraDF['shunt_barra'][i]:^8.3f} |")

                    elif powerflow.method == 'CPF':
                        self.file.write(f"| {powerflow.setup.dbarraDF['numero'][i]:^3d} | {powerflow.setup.dbarraDF['nome'][i]:^11} | {powerflow.setup.dbarraDF['tipo'][i]:^3} |  {powerflow.case[0]['voltage'][i]:^8.3f} | {degrees(powerflow.case[0]['theta'][i]):^+8.2f} | {powerflow.case[0]['active'][i]:^8.3f} | {powerflow.case[0]['reactive'][i]:^8.3f} | {powerflow.setup.dbarraDF['demanda_ativa'][i]:^8.3f} | {powerflow.setup.dbarraDF['demanda_reativa'][i]:^8.3f} | {(powerflow.sol['voltage'][i]**2)*powerflow.setup.dbarraDF['shunt_barra'][i]:^8.3f} |")

                    self.file.write('\n')
                    self.file.write('-'*105)
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
        self.file.write('|           BARRA           |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |')
        self.file.write('\n')
        self.file.write('|     DE      |     PARA    |   Pkm[MW]  |  Qkm[Mvar] |   Pmk[MW]  |  Qmk[Mvar] |    MW   |  Mvar  |')
        self.file.write('\n')
        self.file.write('-'*100)
        for i in range(0, powerflow.setup.nlin):
            if i % 10 == 0 and i != 0:
                self.file.write('\n\n')
                self.file.write('|           BARRA           |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |')
                self.file.write('\n')
                self.file.write('|     DE      |     PARA    |   Pkm[MW]  |  Qkm[Mvar] |   Pmk[MW]  |  Qmk[Mvar] |    MW   |  Mvar  |')
                self.file.write('\n')
                self.file.write('-'*100)

            self.file.write('\n')
            if powerflow.method != 'CPF':
                self.file.write(f"| {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['de'][i] - 1]:^11} | {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['para'][i] - 1]:^11} | {powerflow.sol['active_flow_F2'][i]:^+10.3f} | {powerflow.sol['reactive_flow_F2'][i]:^+10.3f} | {powerflow.sol['active_flow_2F'][i]:^+10.3f} | {powerflow.sol['reactive_flow_2F'][i]:^+10.3f} | {abs(abs(powerflow.sol['active_flow_F2'][i])-abs(powerflow.sol['active_flow_2F'][i])):^7.3f} | {abs(abs(powerflow.sol['reactive_flow_F2'][i])-abs(powerflow.sol['reactive_flow_2F'][i])):^6.3f} |")

            elif powerflow.method == 'CPF':
                self.file.write(f"| {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['de'][i] - 1]:^11} | {powerflow.setup.dbarraDF['nome'][powerflow.setup.dlinhaDF['para'][i] - 1]:^11} | {powerflow.case[0]['active_flow_F2'][i]:^+10.3f} | {powerflow.case[0]['reactive_flow_F2'][i]:^+10.3f} | {powerflow.case[0]['active_flow_2F'][i]:^+10.3f} | {powerflow.case[0]['reactive_flow_2F'][i]:^+10.3f} | {abs(abs(powerflow.case[0]['active_flow_F2'][i])-abs(powerflow.case[0]['active_flow_2F'][i])):^7.3f} | {abs(abs(powerflow.case[0]['reactive_flow_F2'][i])-abs(powerflow.case[0]['reactive_flow_2F'][i])):^6.3f} |")

            self.file.write('\n')
            self.file.write('-'*100)

        self.file.write('\n\n')
        self.file.write('|  GERACAO |   CARGA  |    SHUNT |   PERDAS |')
        self.file.write('\n')
        self.file.write('|       MW |       MW |       MW |       MW | ')
        self.file.write('\n')
        if powerflow.method != 'LINEAR':
            self.file.write('|     Mvar |     Mvar |     Mvar |     Mvar |')
            self.file.write('\n')
        self.file.write('-'*45)
        self.file.write('\n')
        if powerflow.method != 'CPF':
            self.file.write(f"| {sum(powerflow.sol['active']):^+8.3f} | {sum(powerflow.setup.dbarraDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(abs(abs(powerflow.sol['active_flow_F2'])-abs(powerflow.sol['active_flow_2F']))):^8.3f} |")
        
        elif powerflow.method == 'CPF':
            self.file.write(f"| {sum(powerflow.case[0]['active']):^+8.3f} | {sum(powerflow.setup.dbarraDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(abs(abs(powerflow.case[0]['active_flow_F2'])-abs(powerflow.case[0]['active_flow_2F']))):^8.3f} |")
        
        self.file.write('\n')
        if powerflow.method != 'LINEAR':
            if powerflow.method != 'CPF':
                self.file.write(f"| {sum(powerflow.sol['reactive']):^+8.3f} | {sum(powerflow.setup.dbarraDF['demanda_reativa']):^+8.3f} | {sum((powerflow.sol['voltage']**2)*powerflow.setup.dbarraDF['shunt_barra'].values.T):^8.3f} | {sum(abs(abs(powerflow.sol['reactive_flow_F2'])-abs(powerflow.sol['reactive_flow_2F']))):^8.3f} |")
            
            elif powerflow.method == 'CPF':
                self.file.write(f"| {sum(powerflow.case[0]['reactive']):^+8.3f} | {sum(powerflow.setup.dbarraDF['demanda_reativa']):^+8.3f} | {sum((powerflow.case[0]['voltage']**2)*powerflow.setup.dbarraDF['shunt_barra'].values.T):^8.3f} | {sum(abs(abs(powerflow.case[0]['reactive_flow_F2'])-abs(powerflow.case[0]['reactive_flow_2F']))):^8.3f} |")
            
            self.file.write('\n')
        self.file.write('-'*45)
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
        pass


    
    def rsvc(
        self,
        powerflow,
    ):
        """relatório de compensadores estáticos de potência reativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        pass


    
    def rcpf(
        self,
        powerflow,
    ):
        """relatório de fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.var = False
        self.file.write('vv relatório de execução do fluxo de potência continuado vv')
        self.file.write('\n\n')
        self.file.write('              | INCREMENTO DE CARGA |     CARGA TOTAL     |         PASSO        |')
        self.file.write('\n')
        self.file.write('| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIÁVEL | VALOR [%] |')
        self.file.write('\n')
        self.file.write('-'*82)
        for key, value in powerflow.case.items():
            self.file.write('\n')
            if key == 0:
                self.file.write(f"| {key:^4} | {value['iter']:^4} |   0.0    |   0.0    | {sum(powerflow.cpfsol['demanda_ativa']):^8.3f} | {sum(powerflow.cpfsol['demanda_reativa']):^8.3f} |  lambda  | {(powerflow.setup.options['cpfLambda'] * 100):^9} |")

            elif (key != list(powerflow.case.keys())[-1]):
                if key % 5 == 0:
                    self.file.write('\n')
                    self.file.write('              | INCREMENTO DE CARGA |     CARGA TOTAL     |         PASSO        |')
                    self.file.write('\n')
                    self.file.write('| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIÁVEL | VALOR [%] |')
                    self.file.write('\n')
                    self.file.write('-'*82)
                    self.file.write('\n')
                
                if not self.var and (value['corr']['varstep'] == 'lambda'):
                    self.file.write(f"| {key:^4} | {value['corr']['iter']:^4} | {(value['corr']['step'] * 100):^8.3f} | {(value['corr']['step'] * 100):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])):^8.3f} | {value['corr']['varstep']:^8} | {(powerflow.setup.options['cpfLambda'] * 100):^+9.2f} |")
            
                else:
                    self.var = True
                    if (value['corr']['varstep'] == 'volt'):
                        self.file.write(f"| {key:^4} | {value['corr']['iter']:^4} | {(value['corr']['step'] * 100):^8.3f} | {(value['corr']['step'] * 100):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])):^8.3f} | {value['corr']['varstep']:^8} | {(-1 * powerflow.setup.options['cpfVolt'] * 100):^+9.2f} |")

                    elif (value['corr']['varstep'] == 'lambda'):
                            self.file.write(f"| {key:^4} | {value['corr']['iter']:^4} | {(value['corr']['step'] * 100):^8.3f} | {(value['corr']['step'] * 100):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])):^8.3f} | {((1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])):^8.3f} | {value['corr']['varstep']:^8} | {(-1 * powerflow.setup.options['cpfLambda'] * 100):^+9.2f} |")
            
            self.file.write('\n')
            self.file.write('-'*82)
            
        self.file.write('\n\n\n\n')



    def tobecontinued(
        self,
        powerflow,
    ):
        """armazena o resultado do fluxo de potência continuado em formato txt e formato png
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.var = False

        # Manipulação
        self.filevtan = open(powerflow.setup.dircpfsys + powerflow.setup.name + '-tangent.txt', 'w')
        self.filevarv = open(powerflow.setup.dircpfsys + powerflow.setup.name + '-voltagevar.txt', 'w')
        self.filedeteigen = open(powerflow.setup.dircpfsys + powerflow.setup.name + '-det&eigen.txt', 'w')

        # Cabeçalho FILEVTAN
        self.filevtan.write('{} {}, {}'.format(dt.now().strftime('%B'), dt.now().strftime('%d'), dt.now().strftime('%Y')))
        self.filevtan.write('\n\n\n')
        self.filevtan.write('relatório de análise da variação do vetor tangente do sistema ' + powerflow.setup.name)
        self.filevtan.write('\n\n')
        self.filevtan.write('opções de controle ativadas: ')
        if powerflow.setup.control:
            for k in powerflow.setup.control:
                self.filevtan.write(f'{k} ')
        else:
            self.filevtan.write('Nenhum controle ativo!')
        self.filevtan.write('\n\n')
        self.filevtan.write('opções de relatório ativadas: ')
        if powerflow.setup.report:
            for k in powerflow.setup.report:
                self.filevtan.write(f'{k} ')
        self.filevtan.write('\n\n')

        # Cabeçalho FILEVARV
        self.filevarv.write('{} {}, {}'.format(dt.now().strftime('%B'), dt.now().strftime('%d'), dt.now().strftime('%Y')))
        self.filevarv.write('\n\n\n')
        self.filevarv.write('relatório de análise da variação da magnitude de tensão do sistema ' + powerflow.setup.name)
        self.filevarv.write('\n\n')
        self.filevarv.write('opções de controle ativadas: ')
        if powerflow.setup.control:
            for k in powerflow.setup.control:
                self.filevarv.write(f'{k} ')
        else:
            self.filevarv.write('Nenhum controle ativo!')
        self.filevarv.write('\n\n')
        self.filevarv.write('opções de relatório ativadas: ')
        if powerflow.setup.report:
            for k in powerflow.setup.report:
                self.filevarv.write(f'{k} ')
        self.filevarv.write('\n\n')

        # Cabeçalho FILEDETEIGEN
        self.filedeteigen.write('{} {}, {}'.format(dt.now().strftime('%B'), dt.now().strftime('%d'), dt.now().strftime('%Y')))
        self.filedeteigen.write('\n\n\n')
        self.filedeteigen.write('relatório de análise da variação do valor do determinante e autovalores da matriz de sensibilidade QV do sistema ' + powerflow.setup.name)
        self.filedeteigen.write('\n\n')
        self.filedeteigen.write('opções de controle ativadas: ')
        if powerflow.setup.control:
            for k in powerflow.setup.control:
                self.filedeteigen.write(f'{k} ')
        else:
            self.filedeteigen.write('Nenhum controle ativo!')
        self.filedeteigen.write('\n\n')
        self.filedeteigen.write('opções de relatório ativadas: ')
        if powerflow.setup.report:
            for k in powerflow.setup.report:
                self.filedeteigen.write(f'{k} ')
        self.filedeteigen.write('\n\n')

        # Loop
        for key, value in powerflow.case.items():
            if key == 0:
                # Variável de variação de tensão
                self.varv = value['voltage'] - (powerflow.setup.dbarraDF['tensao'] * 1E-3)
                self.argsort = argsort(self.varv)

                # FILEVARV
                self.filevarv.write('\n\n')
                self.filevarv.write(f"Carregamento do Sistema: {sum(powerflow.cpfsol['demanda_ativa'])} MW  | {sum(powerflow.cpfsol['demanda_reativa'])} Mvar")
                self.filevarv.write('\n\n')
                self.filevarv.write('|      BARRA        |        TENSÃO       |')
                self.filevarv.write('\n')
                self.filevarv.write('| NUM |     NOME    |    MOD   | VARIAÇÃO |')
                self.filevarv.write('\n')
                self.filevarv.write('-'*43)
                self.filevarv.write('\n')

                # LOOP
                for n in range(0, powerflow.setup.nbus):
                    self.filevarv.write(f"| {powerflow.setup.dbarraDF['numero'][self.argsort[n]]:^3d} | {powerflow.setup.dbarraDF['nome'][self.argsort[n]]:^11} | {value['voltage'][self.argsort[n]]:^8.4f} | {self.varv[self.argsort[n]]:^+8.4f} |")
                    self.filevarv.write('\n')
                    self.filevarv.write('-'*43)
                    self.filevarv.write('\n')

                # FILEDETEIGEN
                self.filedeteigen.write('\n\n')
                self.filedeteigen.write(f"Carregamento do Sistema: {sum(powerflow.cpfsol['demanda_ativa'])} MW  | {sum(powerflow.cpfsol['demanda_reativa'])} Mvar")
                self.filedeteigen.write('\n')
                self.filedeteigen.write(f"Determinante: {powerflow.case[key]['determinant-QV']}")
                self.filedeteigen.write('\n')
                self.filedeteigen.write(f"Autovalores: {abs(powerflow.case[key]['eigenvalues-QV'])}")
                self.filedeteigen.write('\n')
            
            elif (key != list(powerflow.case.keys())[-1]):
                # Variável de variação de tensão
                if key == 1:
                    self.varv = value['corr']['voltage'] - powerflow.case[0]['voltage']

                elif key > 1:
                    self.varv = value['corr']['voltage'] - powerflow.case[key-1]['corr']['voltage']

                self.argsort = argsort(self.varv)

                # FILEVTAN
                self.filevtan.write('\n\n')
                self.filevtan.write(f"Carregamento do Sistema: {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])} MW  | {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])} Mvar")
                self.filevtan.write('\n')
                if not self.var and (value['corr']['varstep'] == 'lambda'):
                    self.filevtan.write(f"Variável de Continuação: {value['corr']['varstep']}, {powerflow.setup.options['cpfLambda'] * 100:.2f}% ")
                else:
                    self.var = True
                    if value['corr']['varstep'] == 'lambda':
                        self.filevtan.write(f"Variável de Continuação: {value['corr']['varstep']}, {-1 * powerflow.setup.options['cpfLambda'] * 100:.2f}% ")
                    
                    elif value['corr']['varstep'] == 'volt':
                        self.filevtan.write(f"Variável de Continuação: {value['corr']['varstep']}, {-1 * powerflow.setup.options['cpfVolt'] * 100:.2f}% ")

                self.filevtan.write('\n\n')
                self.filevtan.write('|      BARRA        |    VETOR TANGENTE   |       CORREÇÃO      |')
                self.filevtan.write('\n')
                self.filevtan.write('| NUM |     NOME    |    MOD   |    ANG   |    MOD   |    ANG   |')
                self.filevtan.write('\n')
                self.filevtan.write('-'*65)
                self.filevtan.write('\n')

                # FILEVARV
                self.filevarv.write('\n\n')
                self.filevarv.write(f"Carregamento do Sistema: {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])} MW  | {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])} Mvar")
                self.filevarv.write('\n\n')
                self.filevarv.write('|      BARRA        |        TENSÃO       |')
                self.filevarv.write('\n')
                self.filevarv.write('| NUM |     NOME    |    MOD   | VARIAÇÃO |')
                self.filevarv.write('\n')
                self.filevarv.write('-'*43)
                self.filevarv.write('\n')

                # LOOP
                for n in range(0, powerflow.setup.nbus):
                    # FILEVTAN
                    self.filevtan.write(f"| {powerflow.setup.dbarraDF['numero'][n]:^3d} | {powerflow.setup.dbarraDF['nome'][n]:^11} | {value['prev']['voltage'][n]:^8.4f} | {degrees(value['prev']['theta'][n]):^+8.4f} | {value['corr']['voltage'][n]:^8.4f} | {degrees(value['corr']['theta'][n]):^+8.4f} |")
                    self.filevtan.write('\n')
                    self.filevtan.write('-'*65)
                    self.filevtan.write('\n')

                    # FILEVARV
                    if key == 1:
                        self.filevarv.write(f"| {powerflow.setup.dbarraDF['numero'][self.argsort[n]]:^3d} | {powerflow.setup.dbarraDF['nome'][self.argsort[n]]:^11} | {value['corr']['voltage'][self.argsort[n]]:^8.4f} | {self.varv[self.argsort[n]]:^+8.4f} |")
                    elif key > 1:
                        self.filevarv.write(f"| {powerflow.setup.dbarraDF['numero'][self.argsort[n]]:^3d} | {powerflow.setup.dbarraDF['nome'][self.argsort[n]]:^11} | {value['corr']['voltage'][self.argsort[n]]:^8.4f} | {self.varv[self.argsort[n]]:^+8.4f} |")
                    self.filevarv.write('\n')
                    self.filevarv.write('-'*43)
                    self.filevarv.write('\n')

                # FILEDETEIGEN
                self.filedeteigen.write('\n\n')
                self.filedeteigen.write(f"Carregamento do Sistema: {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])} MW  | {(1 + value['corr']['step']) * sum(powerflow.cpfsol['demanda_reativa'])} Mvar")
                self.filedeteigen.write('\n')
                self.filedeteigen.write(f"Determinante: {powerflow.case[key]['corr']['determinant-QV']}")
                self.filedeteigen.write('\n')
                self.filedeteigen.write(f"Autovalores: {abs(powerflow.case[key]['corr']['eigenvalues-QV'])}")
                self.filedeteigen.write('\n')

        # FILEVTAN
        self.filevtan.write('\n\n\n\n')
        self.filevtan.write('fim do relatório de análise da variação do vetor tangente do sistema ' + powerflow.setup.name)
        self.filevtan.close()

        # FILEVARV
        self.filevarv.write('\n\n\n\n')
        self.filevarv.write('fim do relatório de análise da variação da magnitude de tensão do sistema ' + powerflow.setup.name)
        self.filevarv.close()

        # FILEDETEIGEN
        self.filedeteigen.write('\n\n\n\n')
        self.filedeteigen.write('fim do relatório de análise da variação do valor do determinante e autovalores da matriz de sensibilidade QV do sistema ' + powerflow.setup.name)
        self.filedeteigen.close()

        # Arquivos em Loop
        for key, value in powerflow.setup.pqtv.items():
            savetxt(powerflow.setup.dircpfsystxt + powerflow.setup.name + '-' + key + '.txt', column_stack([powerflow.setup.mw, value]))
                 