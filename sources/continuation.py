# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from matplotlib import pyplot as plt
from numpy import abs, all, append, argmax, around, array, concatenate, cos, dot, max, ndarray, ones, sin, sum, zeros
from numpy.linalg import det, eig, solve, inv

from ctrl import Control
from jacobian import Jacobi
from loading import Loading
from newtonraphson import NewtonRaphson
from pwf import PWF

class Continuation:
    """classe para cálculo do fluxo de potência não-linear via método newton-raphson"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Newton-Raphson
        NewtonRaphson(powerflow,)

        # Continuado
        self.continuationpowerflow(powerflow,)

        # Geração e armazenamento de gráficos de perfil de tensão e autovalores
        Loading(powerflow,)



    def continuationpowerflow(
        self,
        powerflow,
    ):
        """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
        powerflow.cpfsol = {
            'pmc': False,
            'v2l': False,
            'div': 0,
            'beta': deepcopy(powerflow.setup.options['cpfBeta']),
            'step': 0.,
            'stepsch': 0.,
            'vsch': 0.,
            'stepmax': 0.,
            'varstep': 'lambda',
            'potencia_ativa': deepcopy(powerflow.setup.dbarraDF['potencia_ativa']),
            'demanda_ativa': deepcopy(powerflow.setup.dbarraDF['demanda_ativa']),
            'demanda_reativa': deepcopy(powerflow.setup.dbarraDF['demanda_reativa']),
        }

        # Variável para armazenamento da solução do fluxo de potência continuado
        powerflow.case = dict()

        # Armazenamento da solução inicial
        powerflow.case[0] = {**deepcopy(powerflow.sol), **deepcopy(powerflow.cpfsol)}

        # Variável para armazenamento de solução por casos do continuado (previsão e correção)
        self.case = 0

        # Armazenamento de determinante e autovalores
        self.eigensens(powerflow,)

        # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
        powerflow.setup.mask = append(powerflow.setup.mask, False)

        # Dimensão da matriz Jacobiana
        powerflow.setup.jdim = powerflow.setup.jacob.shape[0]

        # Barra com maior variação de magnitude de tensão - CASO BASE
        powerflow.setup.nodevarvolt = argmax(abs(powerflow.sol['voltage'] - powerflow.setup.dbarraDF['tensao'] * 1E-3))

        # Loop de Previsão - Correção
        self.cpfloop(powerflow,)



    def cpfloop(
        self,
        powerflow,
    ):
        """loop do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        while all((powerflow.sol['voltage'] >= 0.)) and (sum(powerflow.setup.dbarraDF['demanda_ativa']) >= 0.99 * sum(powerflow.cpfsol['demanda_ativa'])):
            # Incremento de Caso
            self.case += 1

            # Variável de armazenamento
            powerflow.case[self.case] = dict()

            # Previsão
            self.prediction(powerflow,)

            # Correção
            self.correction(powerflow,)

            # Avaliação
            self.evaluate(powerflow,)

            # Heurísticas
            self.heuristics(powerflow,)

            print(powerflow.cpfsol['pmc'])
            
            if (powerflow.cpfsol['varstep'] == 'volt'):
                print('Var: ', powerflow.case[self.case]['corr']['varstep'], '  ', powerflow.setup.options['cpfVolt'] * (0.5 ** powerflow.cpfsol['div']))
            else:
                print('Var: ', powerflow.case[self.case]['corr']['varstep'], '  ', powerflow.setup.options['cpfLambda'] * (0.5 ** powerflow.cpfsol['div']))

            print('Step: ', powerflow.cpfsol['step'])
            print('Stepsch: ', powerflow.cpfsol['stepsch'])

            print(powerflow.sol['iter'], powerflow.sol['convergence'])
            print((1 + powerflow.case[self.case]['corr']['step'])*sum(powerflow.cpfsol['demanda_ativa']), 'MW ', (1 + powerflow.case[self.case]['corr']['step'])*sum(powerflow.cpfsol['demanda_reativa']), 'Mvar')
            print('\n')

            # Break Curva de Carregamento - Somente Parte Estável
            if (not powerflow.setup.options['full']) and (powerflow.cpfsol['pmc']):
                break


    
    def prediction(
        self,
        powerflow,
    ):
        """etapa de previsão do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Incremento do Nível de Carregamento e Geração
        self.increment(powerflow,)

        # Variáveis Especificadas
        self.scheduled(powerflow,)

        # Resíduos
        self.residue(powerflow, stage='prev',)

        # Atualização da Matriz Jacobiana
        Jacobi(powerflow,)

        # Expansão Jacobiana
        self.exjac(powerflow,)

        # Variáveis de estado
        powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)

        # Atualização das Variáveis de estado
        self.update_statevar(powerflow, stage='prev',)

        # Fluxo em linhas de transmissão
        self.line_flow(powerflow,)

        # Armazenamento de Solução
        self.storage(powerflow, stage='prev',)



    def correction(
        self,
        powerflow,
    ):
        """etapa de correção do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento de solução
        powerflow.sol = {
            'iter': 0,
            'voltage': deepcopy(powerflow.case[self.case]['prev']['voltage']),
            'theta': deepcopy(powerflow.case[self.case]['prev']['theta']),
            'active': deepcopy(powerflow.case[self.case]['prev']['active']),
            'reactive': deepcopy(powerflow.case[self.case]['prev']['reactive']),
            'freq': deepcopy(powerflow.case[self.case]['prev']['freq']),
            'freqiter': array([]),
            'convP': array([]),
            'busP': array([]),
            'convQ': array([]),
            'busQ': array([]),
            'convY': array([]),
            'busY': array([]),
            'active_flow_F2': zeros(powerflow.setup.nlin),
            'reactive_flow_F2': zeros(powerflow.setup.nlin),
            'active_flow_2F': zeros(powerflow.setup.nlin),
            'reactive_flow_2F': zeros(powerflow.setup.nlin),
        }

        # Adição de variáveis de controle na variável de armazenamento de solução
        Control(powerflow, powerflow.setup,).controlcorrsol(powerflow, self.case,)

        # Incremento do Nível de Carregamento e Geração
        self.increment(powerflow,)

        # Variáveis Especificadas
        self.scheduled(powerflow,)

        # Resíduos
        self.residue(powerflow, stage='corr',)

        while ((max(abs(powerflow.setup.deltaP)) >= powerflow.setup.options['tolP']) or (max(abs(powerflow.setup.deltaQ)) >= powerflow.setup.options['tolQ']) or (max(abs(powerflow.setup.deltaY)) >= powerflow.setup.options['tolY'])):
            # Armazenamento da trajetória de convergência
            self.convergence(powerflow,)

            # Atualização da Matriz Jacobiana
            Jacobi(powerflow,)

            # Expansão Jacobiana
            self.exjac(powerflow,)

            # Variáveis de estado
            powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)

            # Atualização das Variáveis de estado
            self.update_statevar(powerflow, stage='corr',)

            # Condição de variável de passo
            if (powerflow.cpfsol['varstep'] == 'volt'):
                # Incremento do Nível de Carregamento e Geração
                self.increment(powerflow,)

                # Variáveis Especificadas
                self.scheduled(powerflow,)

            # Atualização dos resíduos
            self.residue(powerflow, stage='corr',)

            # Incremento de iteração
            powerflow.sol['iter'] += 1

            # Condição de Divergência por iterações
            if (powerflow.sol['iter'] > powerflow.setup.options['itermx']):
                powerflow.sol['convergence'] = 'SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)'
                break

        ## Condição
        # Iteração Adicional em Caso de Convergência
        if (self.case == 1):
            if (powerflow.sol['iter'] < powerflow.setup.options['itermx']):
                # Armazenamento da trajetória de convergência
                self.convergence(powerflow,)

                # Atualização da Matriz Jacobiana
                Jacobi(powerflow,)

                # Expansão Jacobiana
                self.exjac(powerflow,)

                # Variáveis de estado
                powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)

                # Atualização das Variáveis de estado
                self.update_statevar(powerflow, stage='corr',)

                # Atualização dos resíduos
                self.residue(powerflow, stage='corr',)

                # Fluxo em linhas de transmissão
                self.line_flow(powerflow,)

                # Armazenamento de Solução
                self.storage(powerflow, stage='corr',)

                # Convergência
                powerflow.sol['convergence'] = 'SISTEMA CONVERGENTE'

            # Reconfiguração dos Dados de Solução em Caso de Divergência
            elif (powerflow.sol['iter'] >= powerflow.setup.options['itermx']) or (all((powerflow.sol['voltage'] - powerflow.case[0]['voltage'] > 0))):
                # Reconfiguração do caso
                self.case -= 1

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['corr']['voltage'])
                powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['corr']['theta'])

                # Reconfiguração da variável de passo
                powerflow.cpfsol['div'] += 1

                # Reconfiguração do valor da variável de passo
                powerflow.cpfsol['step'] = deepcopy(powerflow.case[self.case]['corr']['step'])
                powerflow.cpfsol['stepsch'] = deepcopy(powerflow.case[self.case]['corr']['stepsch'])
                powerflow.cpfsol['vsch'] = deepcopy(powerflow.case[self.case]['corr']['vsch'])

        # Iteração Adicional em Caso de Convergência
        if (self.case > 1):
            if (powerflow.sol['iter'] < powerflow.setup.options['itermx']):
                # Armazenamento da trajetória de convergência
                self.convergence(powerflow,)

                # Atualização da Matriz Jacobiana
                Jacobi(powerflow,)

                # Expansão Jacobiana
                self.exjac(powerflow,)

                # Variáveis de estado
                powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)

                # Atualização das Variáveis de estado
                self.update_statevar(powerflow, stage='corr',)

                # Atualização dos resíduos
                self.residue(powerflow, stage='corr',)

                # Fluxo em linhas de transmissão
                self.line_flow(powerflow,)

                # Armazenamento de Solução
                self.storage(powerflow, stage='corr',)

                # Convergência
                powerflow.sol['convergence'] = 'SISTEMA CONVERGENTE'

            # Reconfiguração dos Dados de Solução em Caso de Divergência
            elif (powerflow.sol['iter'] >= powerflow.setup.options['itermx']) or (all((powerflow.sol['voltage'] - powerflow.case[self.case - 1]['corr']['voltage'] > 0))):
                # Reconfiguração do caso
                self.case -= 1

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['corr']['voltage'])
                powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['corr']['theta'])

                # Reconfiguração da variável de passo
                powerflow.cpfsol['div'] += 1

                # Reconfiguração do valor da variável de passo
                powerflow.cpfsol['step'] = deepcopy(powerflow.case[self.case]['corr']['step'])
                powerflow.cpfsol['stepsch'] = deepcopy(powerflow.case[self.case]['corr']['stepsch'])
                powerflow.cpfsol['vsch'] = deepcopy(powerflow.case[self.case]['corr']['vsch'])



    def increment(
        self,
        powerflow,
    ):
        """realiza incremento no nível de carregamento (e geração)

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Incremento do Carregamento
        powerflow.setup.dbarraDF['demanda_ativa'] = powerflow.cpfsol['demanda_ativa'] * (1 + powerflow.cpfsol['stepsch'])
        powerflow.setup.dbarraDF['demanda_reativa'] = powerflow.cpfsol['demanda_reativa'] * (1 + powerflow.cpfsol['stepsch'])

        # Incremento da Geração
        powerflow.setup.dbarraDF['potencia_ativa'] = powerflow.cpfsol['potencia_ativa'] * (1 + powerflow.cpfsol['beta'] * powerflow.cpfsol['stepsch'])



    def scheduled(
        self,
        powerflow,
    ):
        """método para armazenamento dos parâmetros especificados

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento das potências ativa e reativa especificadas
        powerflow.setup.pqsch = {
            'potencia_ativa_especificada': zeros(powerflow.setup.nbus),
            'potencia_reativa_especificada': zeros(powerflow.setup.nbus),
        }

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.setup.pqsch['potencia_ativa_especificada'][idx] += value['potencia_ativa']
            powerflow.setup.pqsch['potencia_ativa_especificada'][idx] -= value['demanda_ativa']

            # Potência reativa especificada
            powerflow.setup.pqsch['potencia_reativa_especificada'][idx] += value['potencia_reativa']
            powerflow.setup.pqsch['potencia_reativa_especificada'][idx] -= value['demanda_reativa']

        # Tratamento
        powerflow.setup.pqsch['potencia_ativa_especificada'] /= powerflow.setup.options['sbase']
        powerflow.setup.pqsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']

        # Variáveis especificadas de controle ativos
        if (powerflow.setup.ctrlcount > 0):
            Control(powerflow, powerflow.setup).controlsch(powerflow,)



    def residue(
        self,
        powerflow,
        stage: str=None,
    ):
        """cálculo de resíduos das equações diferenciáveis

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # Vetores de resíduo
        powerflow.setup.deltaP = zeros(powerflow.setup.nbus)
        powerflow.setup.deltaQ = zeros(powerflow.setup.nbus)

        # Resíduo de equação de controle adicional
        powerflow.setup.deltaY = array([])

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if (value['tipo'] != 2):
                powerflow.setup.deltaP[idx] += powerflow.setup.pqsch['potencia_ativa_especificada'][idx]
                powerflow.setup.deltaP[idx] -= self.pcalc(powerflow, idx,)

            # Tipo PQ - Resíduo Potência Reativa
            if ('QLIM' in powerflow.setup.control) or (value['tipo'] == 0):
                powerflow.setup.deltaQ[idx] += powerflow.setup.pqsch['potencia_reativa_especificada'][idx]
                powerflow.setup.deltaQ[idx] -= self.qcalc(powerflow, idx,)

        # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
        self.checkresidue(powerflow,)

        # Resíduos de variáveis de estado de controle
        if (powerflow.setup.ctrlcount > 0):
            Control(powerflow, powerflow.setup).controlres(powerflow,)
            self.checkresidue(powerflow,)
            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaPQY, powerflow.setup.deltaY), axis=0)

        # Resíduo de Fluxo de Potência Continuado
        # Condição de previsão
        if (stage == 'prev'):
            powerflow.setup.deltaPQY = zeros(powerflow.setup.deltaPQY.shape[0] + 1)
            # Condição de variável de passo
            if (powerflow.cpfsol['varstep'] == 'lambda'):
                if (not powerflow.cpfsol['pmc']):
                    powerflow.setup.deltaPQY[-1] = powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])

                elif (powerflow.cpfsol['pmc']):
                    powerflow.setup.deltaPQY[-1] = -1 * powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])

            elif (powerflow.cpfsol['varstep'] == 'volt'):
                powerflow.setup.deltaPQY[-1] = -1 * powerflow.setup.options['cpfVolt'] * (5E-1 ** powerflow.cpfsol['div'])

        # Condição de correção
        elif (stage == 'corr'):
            # Condição de variável de passo
            if (powerflow.cpfsol['varstep'] == 'lambda'):
                powerflow.setup.deltaY = array([powerflow.cpfsol['stepsch'] - powerflow.cpfsol['step']])

            elif (powerflow.cpfsol['varstep'] == 'volt'):
                powerflow.setup.deltaY = array([powerflow.cpfsol['vsch'] - powerflow.sol['voltage'][powerflow.setup.nodevarvolt]])

            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaPQY, powerflow.setup.deltaY), axis=0)



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

        Retorno
            p: float
                potência ativa calculada para o barramento `idx`
        """

        ## Inicialização
        # Variável de potência ativa calculada para o barramento `idx`
        p = 0

        for bus in range(0, powerflow.setup.nbus):
            p += powerflow.sol['voltage'][bus] * (powerflow.setup.ybus[idx][bus].real * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) + powerflow.setup.ybus[idx][bus].imag * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        p *= powerflow.sol['voltage'][idx]

        # Armazenamento da potência ativa gerada equivalente do barramento
        powerflow.sol['active'][idx] = (p * powerflow.setup.options['sbase']) + powerflow.setup.dbarraDF['demanda_ativa'][idx]

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

        Retorno
            q: float
                potência reativa calculada para o barramento `idx`
        """

        ## Inicialização
        # Variável de potência reativa calculada para o barramento `idx`
        q = 0

        for bus in range(0, powerflow.setup.nbus):
            q += powerflow.sol['voltage'][bus] * (powerflow.setup.ybus[idx][bus].real * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) - powerflow.setup.ybus[idx][bus].imag * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        q *= powerflow.sol['voltage'][idx]

        # Armazenamento da potência ativa gerada equivalente do barramento
        powerflow.sol['reactive'][idx] = (q * powerflow.setup.options['sbase']) + powerflow.setup.dbarraDF['demanda_reativa'][idx]

        return q



    def checkresidue(
        self,
        powerflow,
    ):
        """determinação do vetor de resíduos

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # configuração completa
        if (powerflow.jacobi == 'COMPLETA'):
            powerflow.setup.deltaPQY  = concatenate((powerflow.setup.deltaP, powerflow.setup.deltaQ), axis=0)

        # configuração alternada
        elif (powerflow.jacobi == 'ALTERNADA'):
            powerflow.setup.deltaPQY: ndarray = zeros(shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype='float')
            pq = -1
            for row in range(0, powerflow.setup.nbus):
                if (row % 2 == 0):
                    pq += 1
                    powerflow.setup.deltaPQY[row] = deepcopy(powerflow.setup.deltaP[pq])
                elif (row % 2 != 0):
                    powerflow.setup.deltaPQY[row] = deepcopy(powerflow.setup.deltaQ[pq])

        # configuração reduzida
        elif (powerflow.jacobi == 'REDUZIDA'):
            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaP, powerflow.setup.deltaQ), axis=0)
            powerflow.setup.mask = ones(2*powerflow.setup.nbus, bool)
            for idx, value in powerflow.setup.dbarraDF.iterrows():
                if (value['tipo'] == 2) or (value['tipo'] == 1):
                    powerflow.setup.mask[powerflow.setup.nbus+idx] = False
                    if (value['tipo'] == 2):
                        powerflow.setup.mask[idx] = False
            powerflow.setup.deltaPQY[powerflow.setup.mask]

        ## ERROR
        else:
            raise ValueError('\033[91mERROR: Falha na escolha da formulação para montagem da matriz Jacobiana.\nRevise as opções disponíveis e rode novamente o programa!\033[0m')



    def exjac(
        self,
        powerflow,
    ):
        """expansão da matriz jacobiana para o método continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização       
        # Arrays adicionais
        rowarray = zeros([1, powerflow.setup.jdim])
        colarray = zeros([powerflow.setup.jdim, 1])
        stepvar = zeros(1)

        # Condição de variável de passo
        if (powerflow.cpfsol['varstep'] == 'lambda'):
            stepvar[0] = 1

        elif (powerflow.cpfsol['varstep'] == 'volt'):
            rowarray[0, (powerflow.setup.nbus + powerflow.setup.nodevarvolt)] = 1

        # Demanda
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if (value['tipo'] != 2):
                colarray[idx, 0] = powerflow.cpfsol['demanda_ativa'][idx] - powerflow.cpfsol['potencia_ativa'][idx]
                if (value['tipo'] == 0):
                    colarray[(idx + powerflow.setup.nbus), 0] = powerflow.cpfsol['demanda_reativa'][idx]

        colarray /= powerflow.setup.options['sbase']

        # Expansão Inferior
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, colarray), axis=1)

        # Expansão Lateral
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((rowarray, [stepvar]), axis=1)), axis=0)



    def convergence(
        self,
        powerflow,
    ):
        """armazenamento da trajetória de convergência do processo de solução do fluxo de potência

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Trajetória de convergência da frequência
        powerflow.sol['freqiter'] = append(powerflow.sol['freqiter'], powerflow.sol['freq'] * powerflow.setup.options['fbase'])

        # Trajetória de convergência da potência ativa
        powerflow.sol['convP'] = append(powerflow.sol['convP'], max(abs(powerflow.setup.deltaP)))
        powerflow.sol['busP'] = append(powerflow.sol['busP'], argmax(abs(powerflow.setup.deltaP)))

        # Trajetória de convergência da potência reativa
        powerflow.sol['convQ'] = append(powerflow.sol['convQ'], max(abs(powerflow.setup.deltaQ)))
        powerflow.sol['busQ'] = append(powerflow.sol['busQ'], argmax(abs(powerflow.setup.deltaQ)))

        # Trajetória de convergência referente a cada equação de controle adicional
        if (powerflow.setup.deltaY.size != 0):
            powerflow.sol['convY'] = append(powerflow.sol['convY'], max(abs(powerflow.setup.deltaY)))
            powerflow.sol['busY'] = append(powerflow.sol['busY'], argmax(abs(powerflow.setup.deltaY)))

        elif (powerflow.setup.deltaY.size == 0):
            powerflow.sol['convY'] = append(powerflow.sol['convY'], 0.)
            powerflow.sol['busY'] = append(powerflow.sol['busY'], 0.)



    def update_statevar(
        self,
        powerflow,
        stage: str=None,
    ):
        """atualização das variáveis de estado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # configuração completa
        if (powerflow.jacobi == 'COMPLETA'):
            powerflow.sol['theta'] += powerflow.setup.statevar[0:(powerflow.setup.nbus)]
            # Condição de previsão
            if (stage == 'prev'):
                # Condição de variável de passo
                if (powerflow.cpfsol['varstep'] == 'lambda'):
                    powerflow.sol['voltage'] += powerflow.setup.statevar[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]
                    powerflow.cpfsol['stepsch'] += powerflow.setup.statevar[-1]

                elif (powerflow.cpfsol['varstep'] == 'volt'):
                    powerflow.cpfsol['step'] += powerflow.setup.statevar[-1]
                    powerflow.cpfsol['stepsch'] += powerflow.setup.statevar[-1]
                    powerflow.cpfsol['vsch'] = powerflow.sol['voltage'][powerflow.setup.nodevarvolt] + powerflow.setup.statevar[(powerflow.setup.nbus + powerflow.setup.nodevarvolt)]

                # Verificação do Ponto de Máximo Carregamento
                if (self.case > 0):
                    if (self.case == 1):
                        powerflow.cpfsol['stepmax'] = deepcopy(powerflow.cpfsol['stepsch'])

                    elif (self.case != 1):
                        if (powerflow.cpfsol['stepsch'] > powerflow.case[self.case - 1]['corr']['step']) and (not powerflow.cpfsol['pmc']):
                            powerflow.cpfsol['stepmax'] = deepcopy(powerflow.cpfsol['stepsch'])

                        elif (not powerflow.cpfsol['pmc']):
                            powerflow.cpfsol['pmc'] = True
                            powerflow.setup.pmcidx = deepcopy(self.case)

            # Condição de correção
            elif (stage == 'corr'):
                powerflow.sol['voltage'] += powerflow.setup.statevar[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]
                powerflow.cpfsol['step'] += powerflow.setup.statevar[-1]

                if (powerflow.cpfsol['varstep'] == 'volt'):
                    powerflow.cpfsol['stepsch'] += powerflow.setup.statevar[-1]

        # configuração alternada
        elif (powerflow.jacobi == 'ALTERNADA'):
            for idx in range(0, powerflow.setup.nbus):
                powerflow.sol['theta'][idx] += powerflow.setup.statevar[idx]
                powerflow.sol['voltage'][idx] += powerflow.setup.statevar[idx+1]

        # configuração reduzida
        elif (powerflow.jacobi == 'REDUZIDA'):
            for idx, value in powerflow.setup.dbarraDF.iterrows():
                if (value['tipo'] == 1) or (value['tipo'] == 0):
                    powerflow.sol['theta'][idx] += powerflow.setup.statevar[idx]
                    if (value['tipo'] == 0):
                        powerflow.sol['voltage'][idx] += powerflow.setup.statevar[idx + powerflow.setup.nbus]

        # Atualização das variáveis de estado adicionais para controles ativos
        if (powerflow.setup.ctrlcount > 0):
            Control(powerflow, powerflow.setup).controlupdt(powerflow,)



    def line_flow(
        self,
        powerflow,
        ):
        """cálculo do fluxo de potência nas linhas de transmissão

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização 
        for idx, value in powerflow.setup.dlinhaDF.iterrows():
            k = int(value['de']) - 1
            m = int(value['para']) - 1
            yline = 1 / ((value['resistencia'] / 100) + 1j * (value['reatancia'] / 100))

            # Verifica presença de transformadores com tap != 1.
            if (value['tap'] != 0):
                yline /= value['tap']

            # Potência ativa k -> m
            powerflow.sol['active_flow_F2'][idx] = yline.real * (powerflow.sol['voltage'][k] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa k -> m
            powerflow.sol['reactive_flow_F2'][idx] = -((value['susceptancia'] / (2*powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][k] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência ativa m -> k
            powerflow.sol['active_flow_2F'][idx] = yline.real * (powerflow.sol['voltage'][m] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa m -> k
            powerflow.sol['reactive_flow_2F'][idx] = -((value['susceptancia'] / (2*powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][m] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

        powerflow.sol['active_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['active_flow_2F'] *= powerflow.setup.options['sbase']

        powerflow.sol['reactive_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['reactive_flow_2F'] *= powerflow.setup.options['sbase']
    


    def storage(
        self,
        powerflow,
        stage: str=None,
    ):
        """armazenamento dos resultados de fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # Armazenamento das variáveis de solução do fluxo de potência
        powerflow.case[self.case][stage] = {**deepcopy(powerflow.sol), **deepcopy(powerflow.cpfsol)}

        # Armazenamento do índice do barramento com maior variação de magnitude de tensão
        powerflow.case[self.case]['nodevarvolt'] = deepcopy(powerflow.setup.nodevarvolt)

        # Análise de sensibilidade e armazenamento 
        self.eigensens(powerflow, stage=stage,)



    def eigensens(
        self,
        powerflow,
        stage: str=None,
    ):
        """análise de autovalores e autovetores

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado
        """

        ## Inicialização
        # Jacobiana reduzida - sensibilidade PT
        powerflow.setup.jacobPT = powerflow.setup.pt[powerflow.setup.maskP, :][:, powerflow.setup.maskP] - dot(dot(powerflow.setup.pv[powerflow.setup.maskP, :][:, powerflow.setup.maskQ], inv(powerflow.setup.qv[powerflow.setup.maskQ, :][:, powerflow.setup.maskQ])), powerflow.setup.qt[powerflow.setup.maskQ, :][:, powerflow.setup.maskP])

        # Jacobiana reduzida - sensibilidade QV
        powerflow.setup.jacobQV = powerflow.setup.qv[powerflow.setup.maskQ, :][:, powerflow.setup.maskQ] - dot(dot(powerflow.setup.qt[powerflow.setup.maskQ, :][:, powerflow.setup.maskP], inv(powerflow.setup.pt[powerflow.setup.maskP, :][:, powerflow.setup.maskP])), powerflow.setup.pv[powerflow.setup.maskP, :][:, powerflow.setup.maskQ])

        # Condição
        if (stage == None):
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.case[self.case]['jacobian'] = powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask]

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.case[self.case]['determinant'] = det(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            rightvalues, rightvector = eig(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])
            powerflow.case[self.case]['eigenvalues'] = rightvalues
            powerflow.case[self.case]['eigenvectors'] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.case[self.case]['participation_factor'] = dot(rightvector, inv(rightvector))

            # Armazenamento da matriz de sensibilidade PT
            powerflow.case[self.case]['jacobian-PT'] = powerflow.setup.jacobPT

            # Armazenamento do determinante da matriz de sensibilidade PT
            powerflow.case[self.case]['determinant-PT'] = det(powerflow.setup.jacobPT)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade PT
            rightvaluesPT, rightvectorPT = eig(powerflow.setup.jacobPT)
            powerflow.case[self.case]['eigenvalues-PT'] = rightvaluesPT
            powerflow.case[self.case]['eigenvectors-PT'] = rightvectorPT

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade PT
            powerflow.case[self.case]['participation_factor-PT'] = dot(rightvectorPT, inv(rightvectorPT))

            # Armazenamento da matriz de sensibilidade QV
            powerflow.case[self.case]['jacobian-QV'] = powerflow.setup.jacobQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.case[self.case]['determinant-QV'] = det(powerflow.setup.jacobQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            rightvaluesQV, rightvectorQV = eig(powerflow.setup.jacobQV)
            powerflow.case[self.case]['eigenvalues-QV'] = rightvaluesQV
            powerflow.case[self.case]['eigenvectors-QV'] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.case[self.case]['participation_factor-QV'] = dot(rightvectorQV, inv(rightvectorQV))

        elif (stage != None):
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.case[self.case][stage]['jacobian'] = powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask]

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.case[self.case][stage]['determinant'] = det(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            rightvalues, rightvector = eig(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])
            powerflow.case[self.case][stage]['eigenvalues'] = rightvalues
            powerflow.case[self.case][stage]['eigenvectors'] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.case[self.case][stage]['participation_factor'] = dot(rightvector, inv(rightvector))

            # Armazenamento da matriz de sensibilidade PT
            powerflow.case[self.case][stage]['jacobian-PT'] = powerflow.setup.jacobPT

            # Armazenamento do determinante da matriz de sensibilidade PT
            powerflow.case[self.case][stage]['determinant-PT'] = det(powerflow.setup.jacobPT)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade PT
            rightvaluesPT, rightvectorPT = eig(powerflow.setup.jacobPT)
            powerflow.case[self.case][stage]['eigenvalues-PT'] = rightvaluesPT
            powerflow.case[self.case][stage]['eigenvectors-PT'] = rightvectorPT

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade PT
            powerflow.case[self.case][stage]['participation_factor-PT'] = dot(rightvectorPT, inv(rightvectorPT))

            # Armazenamento da matriz de sensibilidade QV
            powerflow.case[self.case][stage]['jacobian-QV'] = powerflow.setup.jacobQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.case[self.case][stage]['determinant-QV'] = det(powerflow.setup.jacobQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            rightvaluesQV, rightvectorQV = eig(powerflow.setup.jacobQV)
            powerflow.case[self.case][stage]['eigenvalues-QV'] = rightvaluesQV
            powerflow.case[self.case][stage]['eigenvectors-QV'] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.case[self.case][stage]['participation_factor-QV'] = dot(rightvectorQV, inv(rightvectorQV))




    def evaluate(
        self,
        powerflow,
    ):
        """avaliação para determinação do passo do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Condição Inicial
        if (self.case == 1):
            # Lambda
            self.varlambda = abs((powerflow.cpfsol['step'] - 0) / (powerflow.cpfsol['step']))

            # Voltage
            powerflow.setup.nodevarvolt = argmax(abs(powerflow.sol['voltage'] - powerflow.case[0]['voltage']))
            self.varvolt = abs((powerflow.sol['voltage'][powerflow.setup.nodevarvolt] - powerflow.case[0]['voltage'][powerflow.setup.nodevarvolt]) / powerflow.sol['voltage'][powerflow.setup.nodevarvolt])

        # Condição Durante
        elif (self.case != 1):
            # Lambda
            self.varlambda = abs((powerflow.case[self.case]['corr']['step'] - powerflow.case[self.case - 1]['corr']['step']) / powerflow.case[self.case]['corr']['step'])

            # Voltage
            powerflow.setup.nodevarvolt = argmax(abs(powerflow.sol['voltage'] - powerflow.case[self.case - 1]['corr']['voltage']))
            self.varvolt = abs((powerflow.case[self.case]['corr']['voltage'][powerflow.setup.nodevarvolt] - powerflow.case[self.case - 1]['corr']['voltage'][powerflow.setup.nodevarvolt]) / powerflow.case[self.case]['corr']['voltage'][powerflow.setup.nodevarvolt])

        # Avaliação
        if (self.varlambda > self.varvolt) and (powerflow.cpfsol['varstep'] == 'lambda'):
            powerflow.cpfsol['varstep'] = 'lambda'

        else:
            if (powerflow.cpfsol['pmc']):
                if (powerflow.cpfsol['step'] < (powerflow.setup.options['cpfV2L'] * powerflow.cpfsol['stepmax'])) and (self.varlambda > self.varvolt) and (not powerflow.cpfsol['v2l']):
                    powerflow.cpfsol['varstep'] = 'lambda'
                    powerflow.setup.options['cpfLambda'] = deepcopy(powerflow.case[1]['corr']['step'])
                    powerflow.cpfsol['v2l'] = True
                    powerflow.setup.v2lidx = deepcopy(self.case)

                elif (not powerflow.cpfsol['v2l']):
                    powerflow.cpfsol['varstep'] = 'volt'

            elif (not powerflow.cpfsol['pmc']) and (powerflow.cpfsol['varstep'] == 'lambda') and ((powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])) <= powerflow.setup.options['icmn']):
                powerflow.cpfsol['varstep'] = 'volt'
                powerflow.cpfsol['div'] = 0



    def heuristics(
        self,
        powerflow,
    ):
        """heurísticas para determinação do funcionamento do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.service = False

        # Condição de caso para sistema != ieee24 (pq nesse sistema há aumento de magnitude de tensão na barra 17 PQ)
        if (self.case == 1) and (not powerflow.cpfsol['pmc']) and (powerflow.setup.name != 'ieee24'):
            if (not all((powerflow.sol['voltage'] - powerflow.case[0]['voltage'] <= 0))):
                # Reconfiguração do caso
                self.case -= 1

                # Reconfiguração das variáveis de passo
                cpfkeys = {'system', 'pmc', 'v2l', 'div', 'beta', 'step', 'stepsch', 'vsch', 'varstep', 'potencia_ativa', 'demanda_ativa', 'demanda_reativa', 'stepmax',}
                powerflow.cpfsol = {key: deepcopy(powerflow.case[self.case][key]) for key in powerflow.cpfsol.keys() & cpfkeys}
                powerflow.setup.options['cpfLambda'] *= 1E-1

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['voltage'])
                powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['theta'])
        
        elif (self.case == 2) and (not powerflow.cpfsol['pmc']) and (powerflow.setup.name != 'ieee24'):
            if (not all((powerflow.sol['voltage'] - powerflow.case[self.case - 1]['corr']['voltage'] <= 0))):
                # Reconfiguração do caso
                self.case -= 2

                # Reconfiguração das variáveis de passo
                cpfkeys = {'system', 'pmc', 'v2l', 'div', 'beta', 'step', 'stepsch', 'vsch', 'varstep', 'potencia_ativa', 'demanda_ativa', 'demanda_reativa', 'stepmax',}
                powerflow.cpfsol = {key: deepcopy(powerflow.case[self.case][key]) for key in powerflow.cpfsol.keys() & cpfkeys}
                powerflow.setup.options['cpfLambda'] *= 1E-1

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['voltage'])
                powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['theta'])

        elif (self.case > 2) and (not powerflow.cpfsol['pmc']) and (powerflow.setup.name != 'ieee24'):
            if (not all((powerflow.sol['voltage'] - powerflow.case[self.case - 1]['corr']['voltage'] <= 0))):
                # Reconfiguração do caso
                self.case -= 2

                # Reconfiguração das variáveis de passo
                cpfkeys = {'system', 'pmc', 'v2l', 'div', 'beta', 'step', 'stepsch', 'vsch', 'varstep', 'potencia_ativa', 'demanda_ativa', 'demanda_reativa', 'stepmax',}
                powerflow.cpfsol = {key: deepcopy(powerflow.case[self.case]['corr'][key]) for key in powerflow.cpfsol.keys() & cpfkeys}
                powerflow.setup.options['cpfLambda'] *= 1E-1

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['corr']['voltage'])
                powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['corr']['theta'])

        # Condição de divergência na etapa de previsão por excesso de iterações
        if (powerflow.case[self.case]['prev']['iter'] > powerflow.setup.options['itermx']):
            self.service = True

            # Reconfiguração do caso
            self.case -= 1

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.sol['voltage'] = deepcopy(powerflow.case[self.case]['corr']['voltage'])
            powerflow.sol['theta'] = deepcopy(powerflow.case[self.case]['corr']['theta'])

            # Reconfiguração da variável de passo
            powerflow.cpfsol['div'] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.cpfsol['step'] = deepcopy(powerflow.case[self.case]['corr']['step'])
            powerflow.cpfsol['stepsch'] = deepcopy(powerflow.case[self.case]['corr']['stepsch'])
            powerflow.cpfsol['vsch'] = deepcopy(powerflow.case[self.case]['corr']['vsch'])

        # Condição de atingimento do PMC caso varstep volt pequeno
        if (not powerflow.cpfsol['pmc']) and (powerflow.cpfsol['varstep'] == 'volt') and (powerflow.setup.options['cpfVolt'] * (5E-1 ** powerflow.cpfsol['div']) < powerflow.setup.options['icmn'] ** 2):
            # Reconfiguração de caso (se previsão falhar)
            if (self.service):
                self.case += 1

            # Deletando último caso
            del powerflow.case[self.case]

            # Reconfiguração de caso
            self.case -= 1

            # Reconfiguração da variável de passo
            powerflow.cpfsol['div'] = 0

            # Condição de máximo carregamento atingida
            powerflow.cpfsol['pmc'] = True
            powerflow.case[self.case]['corr']['pmc'] = True
            powerflow.setup.pmcidx = deepcopy(self.case)