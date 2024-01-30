# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    abs,
    absolute,
    all,
    append,
    argmax,
    array,
    concatenate,
    cos,
    dot,
    max,
    sin,
    sum,
    zeros,
)
from numpy.linalg import det, eig, solve, inv

from calc import PQCalc
from ctrl import Control
from jacobian import Jacobi
from loading import Loading
from newtonraphson import NewtonRaphson
from smooth import Smooth


class FastContinuation:
    '''classe para cálculo do fluxo de potência não-linear via método newton-raphson'''

    def __init__(
        self,
        powerflow,
        entender,
    ):
        '''inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
            outro parametro
        '''

        ## Inicialização
        # Newton-Raphson
        NewtonRaphson(
            powerflow,
        )

        # Continuado
        self.fastcontinuationpowerflow(
            powerflow,
            entender,
        )

        del powerflow.case[len(powerflow.case) - 1]

        # # Geração e armazenamento de gráficos de perfil de tensão e autovalores
        # Loading(powerflow,)

        # # Smooth
        # if ('QLIMs' in powerflow.nbuscontrol):
        #     for k, v in powerflow.nbusqlimkeys.items():
        #         v.popitem()
        #     Smooth(powerflow,).qlimstorage(powerflow,)
        # if ('SVCs' in powerflow.nbuscontrol):
        #     for k, v in powerflow.nbussvckeys.items():
        #         v.popitem()
        #     Smooth().svcstorage(powerflow,)

    def fastcontinuationpowerflow(
        self,
        powerflow,
        entender,
    ):
        '''análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

        Parâmetros
            powerflow: self do arquivo powerflow.py
            outro parametro
        '''

        ## Inicialização
        # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
        powerflow.cpfsolution = {
            'pmc': False,
            'v2l': False,
            'div': 0,
            'beta': deepcopy(powerflow.nbusoptions['cpfBeta']),
            'step': 0.0,
            'stepsch': 0.0,
            'vsch': 0.0,
            'stepmax': 0.0,
            'varstep': 'lambda',
            'potencia_ativa': deepcopy(powerflow.nbusdbarraDF['potencia_ativa']),
            'demanda_ativa': deepcopy(powerflow.nbusdbarraDF['demanda_ativa']),
            'demanda_reativa': deepcopy(powerflow.nbusdbarraDF['demanda_reativa']),
        }

        # Variável para armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
        Control(powerflow, powerflow,).controlcpf(
            powerflow,
        )

        # Variável para armazenamento da solução do fluxo de potência continuado
        powerflow.case = dict()

        # Variável para armazenamento de solução por casos do continuado (previsão e correção)
        self.case = 0

        # Armazenamento da solução inicial
        powerflow.case[self.case] = {
            **deepcopy(powerflow.solution),
            **deepcopy(powerflow.cpfsolution),
        }

        # # Armazenamento de determinante e autovalores
        # self.eigensens(powerflow,)

        # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
        powerflow.nbusmask = append(powerflow.nbusmask, False)

        # Dimensão da matriz Jacobiana
        powerflow.nbusjdim = powerflow.jacob.shape[0]

        # Barra com maior variação de magnitude de tensão - CASO BASE
        powerflow.nbusnodevarvolt = argmax(
            abs(
                powerflow.solution['voltage']
                - powerflow.nbusdbarraDF['tensao'] * 1e-3
            )
        )

        # Loop de Previsão - Correção
        self.cpfloop(
            powerflow,
        )

    def cpfloop(
        self,
        powerflow,
    ):
        '''loop do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Condição de parada do fluxo de potência continuado -> Estável & Instável
        while all((powerflow.solution['voltage'] >= 0.0)) and (
            sum(powerflow.nbusdbarraDF['demanda_ativa'])
            >= 0.99 * sum(powerflow.cpfsolution['demanda_ativa'])
        ):
            self.active_heuristic = False

            # Incremento de Caso
            self.case += 1

            # Variável de armazenamento
            powerflow.case[self.case] = dict()

            # Previsão
            self.prediction(
                powerflow,
            )

            # Correção
            self.correction(
                powerflow,
            )

            if (powerflow.solution['convergence'] == 'SISTEMA CONVERGENTE') and (
                self.case > 0
            ):
                print('Aumento Sistema (%): ', powerflow.cpfsolution['step'] * 1e2)
                if powerflow.cpfsolution['varstep'] == 'volt':
                    print(
                        'Passo (%): ',
                        powerflow.case[self.case]['c']['varstep'],
                        '  ',
                        powerflow.nbusoptions['cpfVolt']
                        * (
                            (1 / powerflow.nbusoptions['FDIV'])
                            ** powerflow.cpfsolution['div']
                        )
                        * 1e2,
                    )
                else:
                    print(
                        'Passo (%): ',
                        powerflow.case[self.case]['c']['varstep'],
                        '  ',
                        powerflow.nbusoptions['LMBD']
                        * (
                            (1 / powerflow.nbusoptions['FDIV'])
                            ** powerflow.cpfsolution['div']
                        )
                        * 1e2,
                    )
                print('\n')

            # Break Curva de Carregamento - Parte Estável
            if (not powerflow.nbusoptions['FULL']) and (powerflow.cpfsolution['pmc']):
                break

    def prediction(
        self,
        powerflow,
    ):
        '''etapa de previsão do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        powerflow.solution['iter'] = 0

        # Incremento do Nível de Carregamento e Geração
        self.increment(
            powerflow,
        )

        # Variáveis Especificadas
        self.scheduled(
            powerflow,
        )

        # Resíduos
        self.residue(
            powerflow,
            stage='p',
        )

        # Atualização da Matriz Jacobiana
        Jacobi(
            powerflow,
        )

        # Expansão Jacobiana
        self.exjac(
            powerflow,
        )

        # Variáveis de estado
        powerflow.nbusstatevar = solve(
            powerflow.jacob, powerflow.deltaPQY
        )

        # Atualização das Variáveis de estado
        self.update_statevar(
            powerflow,
            stage='p',
        )

        # Fluxo em linhas de transmissão
        self.line_flow(
            powerflow,
        )

        # Armazenamento de Solução
        self.storage(
            powerflow,
            stage='p',
        )

    def correction(
        self,
        powerflow,
    ):
        '''etapa de correção do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Variável para armazenamento de solução
        powerflow.solution = {
            'iter': 0,
            'voltage': deepcopy(powerflow.case[self.case]['p']['voltage']),
            'theta': deepcopy(powerflow.case[self.case]['p']['theta']),
            'active': deepcopy(powerflow.case[self.case]['p']['active']),
            'reactive': deepcopy(powerflow.case[self.case]['p']['reactive']),
            'freq': deepcopy(powerflow.case[self.case]['p']['freq']),
            'freqiter': array([]),
            'convP': array([]),
            'busP': array([]),
            'convQ': array([]),
            'busQ': array([]),
            'convY': array([]),
            'busY': array([]),
            'active_flow_F2': zeros(powerflow.nbusnlin),
            'reactive_flow_F2': zeros(powerflow.nbusnlin),
            'active_flow_2F': zeros(powerflow.nbusnlin),
            'reactive_flow_2F': zeros(powerflow.nbusnlin),
        }

        # Adição de variáveis de controle na variável de armazenamento de solução
        Control(powerflow, powerflow,).controlcorrsol(
            powerflow,
            self.case,
        )

        # Incremento do Nível de Carregamento e Geração
        self.increment(
            powerflow,
        )

        # Variáveis Especificadas
        self.scheduled(
            powerflow,
        )

        # Resíduos
        self.residue(
            powerflow,
            stage='c',
        )

        while (
            (max(abs(powerflow.deltaP)) >= powerflow.nbusoptions['TEPA'])
            or (max(abs(powerflow.deltaQ)) >= powerflow.nbusoptions['TEPR'])
            or Control(powerflow, powerflow).controldelta(
                powerflow,
            )
        ):
            # Armazenamento da trajetória de convergência
            self.convergence(
                powerflow,
            )

            # Atualização da Matriz Jacobiana
            Jacobi(
                powerflow,
            )

            # Expansão Jacobiana
            self.exjac(
                powerflow,
            )

            # Variáveis de estado
            powerflow.nbusstatevar = solve(
                powerflow.jacob, powerflow.deltaPQY
            )

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage='c',
            )

            # Condição de variável de passo
            if powerflow.cpfsolution['varstep'] == 'volt':
                # Incremento do Nível de Carregamento e Geração
                self.increment(
                    powerflow,
                )

                # Variáveis Especificadas
                self.scheduled(
                    powerflow,
                )

            # Atualização dos resíduos
            self.residue(
                powerflow,
                stage='c',
            )

            # Incremento de iteração
            powerflow.solution['iter'] += 1

            # Condição de Divergência por iterações
            if powerflow.solution['iter'] > powerflow.nbusoptions['ACIT']:
                powerflow.solution[
                    'convergence'
                ] = 'SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)'
                break

        ## Condição
        # Iteração Adicional em Caso de Convergência
        if powerflow.solution['iter'] < powerflow.nbusoptions['ACIT']:
            # Armazenamento da trajetória de convergência
            self.convergence(
                powerflow,
            )

            # Atualização da Matriz Jacobiana
            Jacobi(
                powerflow,
            )

            # Expansão Jacobiana
            self.exjac(
                powerflow,
            )

            # Variáveis de estado
            powerflow.nbusstatevar = solve(
                powerflow.jacob, powerflow.deltaPQY
            )

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage='c',
            )

            # Atualização dos resíduos
            self.residue(
                powerflow,
                stage='c',
            )

            # Fluxo em linhas de transmissão
            self.line_flow(
                powerflow,
            )

            # Armazenamento de Solução
            self.storage(
                powerflow,
                stage='c',
            )

            # Convergência
            powerflow.solution['convergence'] = 'SISTEMA CONVERGENTE'

            # Avaliação
            self.evaluate(
                powerflow,
            )

            # Heurísticas
            self.heuristics(
                powerflow,
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.solution['iter'] >= powerflow.nbusoptions['ACIT'])) and (
            self.case == 1
        ):
            self.active_heuristic = True
            powerflow.solution['convergence'] = 'SISTEMA DIVERGENTE'

            # Reconfiguração do caso
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution['voltage'] = deepcopy(
                powerflow.case[self.case]['c']['voltage']
            )
            powerflow.solution['theta'] = deepcopy(
                powerflow.case[self.case]['c']['theta']
            )

            # Reconfiguração da variável de passo
            powerflow.cpfsolution['div'] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.cpfsolution['step'] = deepcopy(
                powerflow.case[self.case]['c']['step']
            )
            powerflow.cpfsolution['stepsch'] = deepcopy(
                powerflow.case[self.case]['c']['stepsch']
            )
            powerflow.cpfsolution['vsch'] = deepcopy(
                powerflow.case[self.case]['c']['vsch']
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.solution['iter'] >= powerflow.nbusoptions['ACIT'])) and (
            self.case > 1
        ):
            self.active_heuristic = True
            powerflow.solution['convergence'] = 'SISTEMA DIVERGENTE'

            # Reconfiguração do caso
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution['voltage'] = deepcopy(
                powerflow.case[self.case]['c']['voltage']
            )
            powerflow.solution['theta'] = deepcopy(
                powerflow.case[self.case]['c']['theta']
            )

            # Reconfiguração da variável de passo
            powerflow.cpfsolution['div'] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.cpfsolution['step'] = deepcopy(
                powerflow.case[self.case]['c']['step']
            )
            powerflow.cpfsolution['stepsch'] = deepcopy(
                powerflow.case[self.case]['c']['stepsch']
            )
            powerflow.cpfsolution['vsch'] = deepcopy(
                powerflow.case[self.case]['c']['vsch']
            )

    def increment(
        self,
        powerflow,
    ):
        '''realiza incremento no nível de carregamento (e geração)

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Variável
        self.preincrement = sum(powerflow.nbusdbarraDF['demanda_ativa'].to_numpy())

        # Incremento de carga
        for idxinc, valueinc in powerflow.nbusdincDF.iterrows():
            if valueinc['tipo_incremento_1'] == 'AREA':
                for idxbar, valuebar in powerflow.nbusdbarraDF.iterrows():
                    if valuebar['area'] == valueinc['identificacao_incremento_1']:
                        # Incremento de Carregamento
                        powerflow.nbusdbarraDF.at[
                            idxbar, 'demanda_ativa'
                        ] = powerflow.cpfsolution['demanda_ativa'][idxbar] * (
                            1 + powerflow.cpfsolution['stepsch']
                        )
                        powerflow.nbusdbarraDF.at[
                            idxbar, 'demanda_reativa'
                        ] = powerflow.cpfsolution['demanda_reativa'][idxbar] * (
                            1 + powerflow.cpfsolution['stepsch']
                        )

            elif valueinc['tipo_incremento_1'] == 'BARR':
                # Reconfiguração da variável de índice
                idxinc = valueinc['identificacao_incremento_1'] - 1

                # Incremento de Carregamento
                powerflow.nbusdbarraDF.at[
                    idxinc, 'demanda_ativa'
                ] = powerflow.cpfsolution['demanda_ativa'][idxinc] * (
                    1 + powerflow.cpfsolution['stepsch']
                )
                powerflow.nbusdbarraDF.at[
                    idxinc, 'demanda_reativa'
                ] = powerflow.cpfsolution['demanda_reativa'][idxinc] * (
                    1 + powerflow.cpfsolution['stepsch']
                )

        self.deltaincrement = (
            sum(powerflow.nbusdbarraDF['demanda_ativa'].to_numpy())
            - self.preincrement
        )

        # Incremento de geração
        if powerflow.nbuscodes['DGER']:
            for idxger, valueger in powerflow.nbusdgeraDF.iterrows():
                idx = valueger['numero'] - 1
                powerflow.nbusdbarraDF.at[
                    idx, 'potencia_ativa'
                ] = powerflow.nbusdbarraDF['potencia_ativa'][idx] + (
                    self.deltaincrement * valueger['fator_participacao']
                )

            powerflow.cpfsolution['potencia_ativa'] = deepcopy(
                powerflow.nbusdbarraDF['potencia_ativa']
            )

        # Condição de atingimento do máximo incremento do nível de carregamento
        if (
            powerflow.cpfsolution['stepsch']
            == powerflow.nbusdincDF.loc[0, 'maximo_incremento_potencia_ativa']
        ):
            powerflow.cpfsolution['pmc'] = True

    def scheduled(
        self,
        powerflow,
    ):
        '''método para armazenamento dos parâmetros especificados

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Variável para armazenamento das potências ativa e reativa especificadas
        powerflow.pqsch = {
            'potencia_ativa_especificada': zeros(powerflow.nbusnbus),
            'potencia_reativa_especificada': zeros(powerflow.nbusnbus),
        }

        # Loop
        for idx, value in powerflow.nbusdbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.pqsch['potencia_ativa_especificada'][idx] += value[
                'potencia_ativa'
            ]
            powerflow.pqsch['potencia_ativa_especificada'][idx] -= value[
                'demanda_ativa'
            ]

            # Potência reativa especificada
            powerflow.pqsch['potencia_reativa_especificada'][idx] += value[
                'potencia_reativa'
            ]
            powerflow.pqsch['potencia_reativa_especificada'][idx] -= value[
                'demanda_reativa'
            ]

        # Tratamento
        powerflow.pqsch['potencia_ativa_especificada'] /= powerflow.nbusoptions[
            'BASE'
        ]
        powerflow.pqsch[
            'potencia_reativa_especificada'
        ] /= powerflow.nbusoptions['BASE']

        # Variáveis especificadas de controle ativos
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow).controlsch(
                powerflow,
            )

    def residue(
        self,
        powerflow,
        stage: str = None,
    ):
        '''cálculo de resíduos das equações diferenciáveis

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        '''

        ## Inicialização
        # Vetores de resíduo
        powerflow.deltaP = zeros(powerflow.nbusnbus)
        powerflow.deltaQ = zeros(powerflow.nbusnbus)

        # Resíduo de equação de controle adicional
        powerflow.deltaY = array([])

        # Loop
        for idx, value in powerflow.nbusdbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if value['tipo'] != 2:
                powerflow.deltaP[idx] += powerflow.pqsch[
                    'potencia_ativa_especificada'
                ][idx]
                powerflow.deltaP[idx] -= PQCalc().pcalc(
                    powerflow,
                    idx,
                )

            # Tipo PQ - Resíduo Potência Reativa
            if (
                ('QLIM' in powerflow.nbuscontrol)
                or ('QLIMs' in powerflow.nbuscontrol)
                or (value['tipo'] == 0)
            ):
                powerflow.deltaQ[idx] += powerflow.pqsch[
                    'potencia_reativa_especificada'
                ][idx]
                powerflow.deltaQ[idx] -= PQCalc().qcalc(
                    powerflow,
                    idx,
                )

        # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
        self.concatresidue(
            powerflow,
        )

        # Resíduos de variáveis de estado de controle
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow).controlres(
                powerflow,
                self.case,
            )
            self.concatresidue(
                powerflow,
            )
            powerflow.deltaPQY = concatenate(
                (powerflow.deltaPQY, powerflow.deltaY), axis=0
            )

        # Resíduo de Fluxo de Potência Continuado
        # Condição de previsão
        if stage == 'p':
            powerflow.deltaPQY = zeros(powerflow.deltaPQY.shape[0] + 1)
            # Condição de variável de passo
            if powerflow.cpfsolution['varstep'] == 'lambda':
                if not powerflow.cpfsolution['pmc']:
                    powerflow.deltaPQY[-1] = powerflow.nbusoptions[
                        'LMBD'
                    ] * (5e-1 ** powerflow.cpfsolution['div'])

                elif powerflow.cpfsolution['pmc']:
                    powerflow.deltaPQY[-1] = (
                        -1
                        * powerflow.nbusoptions['LMBD']
                        * (5e-1 ** powerflow.cpfsolution['div'])
                    )

            elif powerflow.cpfsolution['varstep'] == 'volt':
                powerflow.deltaPQY[-1] = (
                    -1
                    * powerflow.nbusoptions['cpfVolt']
                    * (5e-1 ** powerflow.cpfsolution['div'])
                )

        # Condição de correção
        elif stage == 'c':
            # Condição de variável de passo
            if powerflow.cpfsolution['varstep'] == 'lambda':
                powerflow.deltaY = array(
                    [powerflow.cpfsolution['stepsch'] - powerflow.cpfsolution['step']]
                )

            elif powerflow.cpfsolution['varstep'] == 'volt':
                powerflow.deltaY = array(
                    [
                        powerflow.cpfsolution['vsch']
                        - powerflow.solution['voltage'][powerflow.nbusnodevarvolt]
                    ]
                )

            powerflow.deltaPQY = concatenate(
                (powerflow.deltaPQY, powerflow.deltaY), axis=0
            )

    def concatresidue(
        self,
        powerflow,
    ):
        '''determinação do vetor de resíduos

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # configuração completa
        powerflow.deltaPQY = concatenate(
            (powerflow.deltaP, powerflow.deltaQ), axis=0
        )

    def exjac(
        self,
        powerflow,
    ):
        '''expansão da matriz jacobiana para o método continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Arrays adicionais
        rowarray = zeros([1, powerflow.nbusjdim])
        colarray = zeros([powerflow.nbusjdim, 1])
        stepvar = zeros(1)

        # Condição de variável de passo
        if powerflow.cpfsolution['varstep'] == 'lambda':
            stepvar[0] = 1

        elif powerflow.cpfsolution['varstep'] == 'volt':
            rowarray[0, (powerflow.nbusnbus + powerflow.nbusnodevarvolt)] = 1

        # Demanda
        for idx, value in powerflow.nbusdbarraDF.iterrows():
            if value['tipo'] != 2:
                colarray[idx, 0] = (
                    powerflow.cpfsolution['demanda_ativa'][idx]
                    - powerflow.cpfsolution['potencia_ativa'][idx]
                )
                if value['tipo'] == 0:
                    colarray[(idx + powerflow.nbusnbus), 0] = powerflow.cpfsolution[
                        'demanda_reativa'
                    ][idx]

        colarray /= powerflow.nbusoptions['BASE']

        # Expansão Inferior
        powerflow.jacob = concatenate((powerflow.jacob, colarray), axis=1)

        # Expansão Lateral
        powerflow.jacob = concatenate(
            (powerflow.jacob, concatenate((rowarray, [stepvar]), axis=1)), axis=0
        )

    def convergence(
        self,
        powerflow,
    ):
        '''armazenamento da trajetória de convergência do processo de solução do fluxo de potência

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Trajetória de convergência da frequência
        powerflow.solution['freqiter'] = append(
            powerflow.solution['freqiter'],
            powerflow.solution['freq'] * powerflow.nbusoptions['FBASE'],
        )

        # Trajetória de convergência da potência ativa
        powerflow.solution['convP'] = append(
            powerflow.solution['convP'], max(abs(powerflow.deltaP))
        )
        powerflow.solution['busP'] = append(
            powerflow.solution['busP'], argmax(abs(powerflow.deltaP))
        )

        # Trajetória de convergência da potência reativa
        powerflow.solution['convQ'] = append(
            powerflow.solution['convQ'], max(abs(powerflow.deltaQ))
        )
        powerflow.solution['busQ'] = append(
            powerflow.solution['busQ'], argmax(abs(powerflow.deltaQ))
        )

        # Trajetória de convergência referente a cada equação de controle adicional
        if powerflow.deltaY.size != 0:
            powerflow.solution['convY'] = append(
                powerflow.solution['convY'], max(abs(powerflow.deltaY))
            )
            powerflow.solution['busY'] = append(
                powerflow.solution['busY'], argmax(abs(powerflow.deltaY))
            )

        elif powerflow.deltaY.size == 0:
            powerflow.solution['convY'] = append(powerflow.solution['convY'], 0.0)
            powerflow.solution['busY'] = append(powerflow.solution['busY'], 0.0)

    def update_statevar(
        self,
        powerflow,
        stage: str = None,
    ):
        '''atualização das variáveis de estado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        '''

        ## Inicialização
        # configuração completa
        powerflow.solution['theta'] += powerflow.nbusstatevar[
            0 : (powerflow.nbusnbus)
        ]
        # Condição de previsão
        if stage == 'p':
            # Condição de variável de passo
            if powerflow.cpfsolution['varstep'] == 'lambda':
                powerflow.solution['voltage'] += powerflow.nbusstatevar[
                    (powerflow.nbusnbus) : (2 * powerflow.nbusnbus)
                ]
                powerflow.cpfsolution['stepsch'] += powerflow.nbusstatevar[-1]

            elif powerflow.cpfsolution['varstep'] == 'volt':
                powerflow.cpfsolution['step'] += powerflow.nbusstatevar[-1]
                powerflow.cpfsolution['stepsch'] += powerflow.nbusstatevar[-1]
                powerflow.cpfsolution['vsch'] = (
                    powerflow.solution['voltage'][powerflow.nbusnodevarvolt]
                    + powerflow.nbusstatevar[
                        (powerflow.nbusnbus + powerflow.nbusnodevarvolt)
                    ]
                )

            # Verificação do Ponto de Máximo Carregamento
            if self.case > 0:
                if self.case == 1:
                    powerflow.cpfsolution['stepmax'] = deepcopy(
                        powerflow.cpfsolution['stepsch']
                    )

                elif self.case != 1:
                    if (
                        powerflow.cpfsolution['stepsch']
                        > powerflow.case[self.case - 1]['c']['step']
                    ) and (not powerflow.cpfsolution['pmc']):
                        powerflow.cpfsolution['stepmax'] = deepcopy(
                            powerflow.cpfsolution['stepsch']
                        )

                    elif (
                        powerflow.cpfsolution['stepsch']
                        < powerflow.case[self.case - 1]['c']['step']
                    ) and (not powerflow.cpfsolution['pmc']):
                        powerflow.cpfsolution['pmc'] = True
                        powerflow.nbuspmcidx = deepcopy(self.case)

        # Condição de correção
        elif stage == 'c':
            powerflow.solution['voltage'] += powerflow.nbusstatevar[
                (powerflow.nbusnbus) : (2 * powerflow.nbusnbus)
            ]
            powerflow.cpfsolution['step'] += powerflow.nbusstatevar[-1]

            if powerflow.cpfsolution['varstep'] == 'volt':
                powerflow.cpfsolution['stepsch'] += powerflow.nbusstatevar[-1]

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow).controlupdt(
                powerflow,
            )

    def line_flow(
        self,
        powerflow,
    ):
        '''cálculo do fluxo de potência nas linhas de transmissão

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        for idx, value in powerflow.nbusdlinhaDF.iterrows():
            k = powerflow.nbusdbarraDF.index[
                powerflow.nbusdbarraDF['numero'] == value['de']
            ][0]
            m = powerflow.nbusdbarraDF.index[
                powerflow.nbusdbarraDF['numero'] == value['para']
            ][0]
            yline = 1 / ((value['resistencia'] / 100) + 1j * (value['reatancia'] / 100))

            # Verifica presença de transformadores com tap != 1.
            if value['tap'] != 0:
                yline /= value['tap']

            # Potência ativa k -> m
            powerflow.solution['active_flow_F2'][idx] = yline.real * (
                powerflow.solution['voltage'][k] ** 2
            ) - powerflow.solution['voltage'][k] * powerflow.solution['voltage'][m] * (
                yline.real
                * cos(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
                + yline.imag
                * sin(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
            )

            # Potência reativa k -> m
            powerflow.solution['reactive_flow_F2'][idx] = -(
                (value['susceptancia'] / (2 * powerflow.nbusoptions['BASE']))
                + yline.imag
            ) * (powerflow.solution['voltage'][k] ** 2) + powerflow.solution['voltage'][
                k
            ] * powerflow.solution[
                'voltage'
            ][
                m
            ] * (
                yline.imag
                * cos(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
                - yline.real
                * sin(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
            )

            # Potência ativa m -> k
            powerflow.solution['active_flow_2F'][idx] = yline.real * (
                powerflow.solution['voltage'][m] ** 2
            ) - powerflow.solution['voltage'][k] * powerflow.solution['voltage'][m] * (
                yline.real
                * cos(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
                - yline.imag
                * sin(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
            )

            # Potência reativa m -> k
            powerflow.solution['reactive_flow_2F'][idx] = -(
                (value['susceptancia'] / (2 * powerflow.nbusoptions['BASE']))
                + yline.imag
            ) * (powerflow.solution['voltage'][m] ** 2) + powerflow.solution['voltage'][
                k
            ] * powerflow.solution[
                'voltage'
            ][
                m
            ] * (
                yline.imag
                * cos(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
                + yline.real
                * sin(powerflow.solution['theta'][k] - powerflow.solution['theta'][m])
            )

        powerflow.solution['active_flow_F2'] *= powerflow.nbusoptions['BASE']
        powerflow.solution['active_flow_2F'] *= powerflow.nbusoptions['BASE']

        powerflow.solution['reactive_flow_F2'] *= powerflow.nbusoptions['BASE']
        powerflow.solution['reactive_flow_2F'] *= powerflow.nbusoptions['BASE']

    def storage(
        self,
        powerflow,
        stage: str = None,
    ):
        '''armazenamento dos resultados de fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        '''

        ## Inicialização
        # Armazenamento das variáveis de solução do fluxo de potência
        powerflow.case[self.case][stage] = {
            **deepcopy(powerflow.solution),
            **deepcopy(powerflow.cpfsolution),
        }

        if 'SVCs' in powerflow.nbuscontrol:
            powerflow.case[self.case][stage]['svc_reactive_generation'] = deepcopy(
                powerflow.solution['svc_reactive_generation']
            )

        # Armazenamento do índice do barramento com maior variação de magnitude de tensão
        powerflow.case[self.case]['nodevarvolt'] = deepcopy(powerflow.nbusnodevarvolt)

        # # Análise de sensibilidade e armazenamento
        # self.eigensens(powerflow, stage=stage,)

    def eigensens(
        self,
        powerflow,
        stage: str = None,
    ):
        '''análise de autovalores e autovetores

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado
        '''

        ## Inicialização
        # Reorganização da Matriz Jacobiana Expandida
        self.jacob = deepcopy(powerflow.jacob)

        if self.case > 0:
            self.jacob = self.jacob[:-1, :-1]

        # # Submatrizes Jacobianas
        self.pt = deepcopy(
            self.jacob[: (2 * powerflow.nbusnbus), :][:, : (2 * powerflow.nbusnbus)]
        )
        self.pv = deepcopy(
            self.jacob[: (2 * powerflow.nbusnbus), :][
                :,
                (2 * powerflow.nbusnbus) : (
                    2 * powerflow.nbusnbus + powerflow.nbustotaldevicescontrol
                ),
            ]
        )
        self.qt = deepcopy(
            self.jacob[
                (2 * powerflow.nbusnbus) : (
                    2 * powerflow.nbusnbus + powerflow.nbustotaldevicescontrol
                ),
                :,
            ][:, : (2 * powerflow.nbusnbus)]
        )
        self.qv = deepcopy(
            self.jacob[
                (2 * powerflow.nbusnbus) : (
                    2 * powerflow.nbusnbus + powerflow.nbustotaldevicescontrol
                ),
                :,
            ][
                :,
                (2 * powerflow.nbusnbus) : (
                    2 * powerflow.nbusnbus + powerflow.nbustotaldevicescontrol
                ),
            ]
        )

        try:
            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            rightvalues, rightvector = eig(
                powerflow.jacob[powerflow.nbusmask, :][:, powerflow.nbusmask]
            )
            powerflow.PF = zeros(
                [
                    powerflow.jacob[powerflow.nbusmask, :][
                        :, powerflow.nbusmask
                    ].shape[0],
                    powerflow.jacob[powerflow.nbusmask, :][
                        :, powerflow.nbusmask
                    ].shape[1],
                ]
            )

            # Jacobiana reduzida - sensibilidade QV
            powerflow.jacobQV = self.qv - dot(dot(self.qt, inv(self.pt)), self.pv)
            rightvaluesQV, rightvectorQV = eig(powerflow.jacobQV)
            rightvaluesQV = absolute(rightvaluesQV)
            powerflow.PFQV = zeros(
                [powerflow.jacobQV.shape[0], powerflow.jacobQV.shape[1]]
            )
            for row in range(0, powerflow.jacobQV.shape[0]):
                for col in range(0, powerflow.jacobQV.shape[1]):
                    powerflow.PFQV[col, row] = (
                        rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                    )

            # Condição
            if stage == None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.case[self.case]['jacobian'] = powerflow.jacob[
                    powerflow.nbusmask, :
                ][:, powerflow.nbusmask]

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.case[self.case]['determinant'] = det(
                    powerflow.jacob[powerflow.nbusmask, :][
                        :, powerflow.nbusmask
                    ]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.case[self.case]['eigenvalues'] = rightvalues
                powerflow.case[self.case]['eigenvectors'] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.case[self.case]['participation_factor'] = powerflow.PF

                # Armazenamento da matriz de sensibilidade QV
                powerflow.case[self.case]['jacobian-QV'] = powerflow.jacobQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.case[self.case]['determinant-QV'] = det(
                    powerflow.jacobQV
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.case[self.case]['eigenvalues-QV'] = rightvaluesQV
                powerflow.case[self.case]['eigenvectors-QV'] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.case[self.case][
                    'participationfactor-QV'
                ] = powerflow.PFQV

            elif stage != None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.case[self.case][stage]['jacobian'] = powerflow.jacob

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.case[self.case][stage]['determinant'] = det(
                    powerflow.jacob[powerflow.nbusmask, :][
                        :, powerflow.nbusmask
                    ]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.case[self.case][stage]['eigenvalues'] = rightvalues
                powerflow.case[self.case][stage]['eigenvectors'] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.case[self.case][stage][
                    'participationfactor'
                ] = powerflow.PF

                # Armazenamento da matriz de sensibilidade QV
                powerflow.case[self.case][stage][
                    'jacobian-QV'
                ] = powerflow.jacobQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.case[self.case][stage]['determinant-QV'] = det(
                    powerflow.jacobQV
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.case[self.case][stage]['eigenvalues-QV'] = rightvaluesQV
                powerflow.case[self.case][stage]['eigenvectors-QV'] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.case[self.case][stage][
                    'participationfactor-QV'
                ] = powerflow.PFQV

        # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
        # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
        except:
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
                powerflow,
            )

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                'system',
                'pmc',
                'v2l',
                'div',
                'beta',
                'step',
                'stepsch',
                'vsch',
                'varstep',
                'potencia_ativa',
                'demanda_ativa',
                'demanda_reativa',
                'stepmax',
            }
            powerflow.cpfsolution = {
                key: deepcopy(powerflow.case[self.case]['c'][key])
                for key in powerflow.cpfsolution.keys() & cpfkeys
            }
            powerflow.cpfsolution['div'] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution['voltage'] = deepcopy(
                powerflow.case[self.case]['c']['voltage']
            )
            powerflow.solution['theta'] = deepcopy(
                powerflow.case[self.case]['c']['theta']
            )

            # # Loop
            # pass

    def evaluate(
        self,
        powerflow,
    ):
        '''avaliação para determinação do passo do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Condição Inicial
        if self.case == 1:
            # Lambda
            self.varlambda = abs(
                (powerflow.cpfsolution['step'] - 0) / (powerflow.cpfsolution['step'])
            )

            # Voltage
            powerflow.nbusnodevarvolt = argmax(
                abs(powerflow.solution['voltage'] - powerflow.case[0]['voltage'])
            )
            self.varvolt = abs(
                (
                    powerflow.solution['voltage'][powerflow.nbusnodevarvolt]
                    - powerflow.case[0]['voltage'][powerflow.nbusnodevarvolt]
                )
                / powerflow.solution['voltage'][powerflow.nbusnodevarvolt]
            )

        # Condição Durante
        elif self.case != 1:
            # Lambda
            self.varlambda = abs(
                (
                    powerflow.case[self.case]['c']['step']
                    - powerflow.case[self.case - 1]['c']['step']
                )
                / powerflow.case[self.case]['c']['step']
            )

            # Voltage
            powerflow.nbusnodevarvolt = argmax(
                abs(
                    powerflow.solution['voltage']
                    - powerflow.case[self.case - 1]['c']['voltage']
                )
            )
            self.varvolt = abs(
                (
                    powerflow.case[self.case]['c']['voltage'][
                        powerflow.nbusnodevarvolt
                    ]
                    - powerflow.case[self.case - 1]['c']['voltage'][
                        powerflow.nbusnodevarvolt
                    ]
                )
                / powerflow.case[self.case]['c']['voltage'][
                    powerflow.nbusnodevarvolt
                ]
            )

        # Avaliação
        if (self.varlambda > self.varvolt) and (
            powerflow.cpfsolution['varstep'] == 'lambda'
        ):
            powerflow.cpfsolution['varstep'] = 'lambda'

        else:
            if powerflow.cpfsolution['pmc']:
                if (
                    (
                        powerflow.cpfsolution['step']
                        < (
                            powerflow.nbusoptions['cpfV2L']
                            * powerflow.cpfsolution['stepmax']
                        )
                    )
                    and (self.varlambda > self.varvolt)
                    and (not powerflow.cpfsolution['v2l'])
                ):
                    powerflow.cpfsolution['varstep'] = 'lambda'
                    powerflow.nbusoptions['LMBD'] = deepcopy(
                        powerflow.case[1]['c']['step']
                    )
                    powerflow.cpfsolution['v2l'] = True
                    powerflow.cpfsolution['div'] = 0
                    powerflow.nbusv2lidx = deepcopy(self.case)

                elif not powerflow.cpfsolution['v2l']:
                    powerflow.cpfsolution['varstep'] = 'volt'

            elif (
                (not powerflow.cpfsolution['pmc'])
                and (powerflow.cpfsolution['varstep'] == 'lambda')
                and (
                    (
                        powerflow.nbusoptions['LMBD']
                        * (
                            (1 / powerflow.nbusoptions['FDIV'])
                            ** powerflow.cpfsolution['div']
                        )
                    )
                    <= powerflow.nbusoptions['ICMN']
                )
            ):
                powerflow.cpfsolution['pmc'] = True
                powerflow.nbuspmcidx = deepcopy(self.case)
                powerflow.cpfsolution['varstep'] = 'volt'
                powerflow.cpfsolution['div'] = 0

    def heuristics(
        self,
        powerflow,
    ):
        '''heurísticas para determinação do funcionamento do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        ## Afundamento de tensão não desejado (em i+1) e retorno ao valor esperado (em i+2) -> correção: voltar duas casas
        # Condição de caso para sistema != ieee24 (pq nesse sistema há aumento de magnitude de tensão na barra 17 PQ)
        if (
            (powerflow.nbusname != 'ieee24')
            and (powerflow.nbusname != 'ieee118')
            and (powerflow.nbusname != 'ieee118-collapse')
            and (self.case == 1)
            and (not powerflow.cpfsolution['pmc'])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution['voltage'] - powerflow.case[0]['voltage']
                    <= powerflow.nbusoptions['VVAR']
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                self.case -= 1
                Control(powerflow, powerflow,).controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    'system',
                    'pmc',
                    'v2l',
                    'div',
                    'beta',
                    'step',
                    'stepsch',
                    'vsch',
                    'varstep',
                    'potencia_ativa',
                    'demanda_ativa',
                    'demanda_reativa',
                    'stepmax',
                }
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.case[self.case][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution['div'] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution['voltage'] = deepcopy(
                    powerflow.case[self.case]['voltage']
                )
                powerflow.solution['theta'] = deepcopy(
                    powerflow.case[self.case]['theta']
                )

        elif (
            (powerflow.nbusname != 'ieee24')
            and (powerflow.nbusname != 'ieee118')
            and (powerflow.nbusname != 'ieee118-collapse')
            and (self.case == 2)
            and (not powerflow.cpfsolution['pmc'])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution['voltage']
                    - powerflow.case[self.case - 1]['c']['voltage']
                    <= powerflow.nbusoptions['VVAR']
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow,
                ).controlpop(powerflow, pop=2)

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    'system',
                    'pmc',
                    'v2l',
                    'div',
                    'beta',
                    'step',
                    'stepsch',
                    'vsch',
                    'varstep',
                    'potencia_ativa',
                    'demanda_ativa',
                    'demanda_reativa',
                    'stepmax',
                }
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.case[self.case][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution['div'] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution['voltage'] = deepcopy(
                    powerflow.case[self.case]['voltage']
                )
                powerflow.solution['theta'] = deepcopy(
                    powerflow.case[self.case]['theta']
                )

        elif (
            (powerflow.nbusname != 'ieee24')
            and (powerflow.nbusname != 'ieee118')
            and (powerflow.nbusname != 'ieee118-collapse')
            and (self.case > 2)
            and (not powerflow.cpfsolution['pmc'])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution['voltage']
                    - powerflow.case[self.case - 1]['c']['voltage']
                    <= powerflow.nbusoptions['VVAR']
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow,
                ).controlpop(powerflow, pop=2)

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    'system',
                    'pmc',
                    'v2l',
                    'div',
                    'beta',
                    'step',
                    'stepsch',
                    'vsch',
                    'varstep',
                    'potencia_ativa',
                    'demanda_ativa',
                    'demanda_reativa',
                    'stepmax',
                }
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.case[self.case]['c'][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution['div'] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution['voltage'] = deepcopy(
                    powerflow.case[self.case]['c']['voltage']
                )
                powerflow.solution['theta'] = deepcopy(
                    powerflow.case[self.case]['c']['theta']
                )

        if self.case > 0:
            # Condição de divergência na etapa de previsão por excesso de iterações
            if (
                (
                    powerflow.case[self.case]['p']['iter']
                    > powerflow.nbusoptions['ACIT']
                )
                and (not self.active_heuristic)
                and (powerflow.nbusname != 'ieee118')
                and (powerflow.nbusname != 'ieee118-collapse')
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                self.case -= 1
                Control(powerflow, powerflow,).controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    'system',
                    'pmc',
                    'v2l',
                    'div',
                    'beta',
                    'step',
                    'stepsch',
                    'vsch',
                    'varstep',
                    'potencia_ativa',
                    'demanda_ativa',
                    'demanda_reativa',
                    'stepmax',
                }
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.case[self.case]['c'][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution['div'] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution['voltage'] = deepcopy(
                    powerflow.case[self.case]['c']['voltage']
                )
                powerflow.solution['theta'] = deepcopy(
                    powerflow.case[self.case]['c']['theta']
                )

            # Condição de atingimento do PMC para varstep volt pequeno
            if (
                (not powerflow.cpfsolution['pmc'])
                and (powerflow.cpfsolution['varstep'] == 'volt')
                and (
                    powerflow.nbusoptions['cpfVolt']
                    * (5e-1 ** powerflow.cpfsolution['div'])
                    < powerflow.nbusoptions['ICMN']
                )
                and (not self.active_heuristic)
            ):
                self.active_heuristic = True

                # Reconfiguração de caso
                self.case -= 1
                Control(powerflow, powerflow,).controlpop(
                    powerflow,
                )

                # Reconfiguração da variável de passo
                powerflow.cpfsolution['div'] = 0

                # Condição de máximo carregamento atingida
                powerflow.cpfsolution['pmc'] = True
                powerflow.case[self.case]['c']['pmc'] = True
                powerflow.nbuspmcidx = deepcopy(self.case)

            # Condição de valor de tensão da barra slack variar
            if (
                (
                    powerflow.solution['voltage'][powerflow.nbusslackidx]
                    < (
                        powerflow.nbusdbarraDF.loc[powerflow.nbusslackidx, 'tensao']
                        * 1e-3
                    )
                    - 1e-8
                )
                or (
                    powerflow.solution['voltage'][powerflow.nbusslackidx]
                    > (
                        powerflow.nbusdbarraDF.loc[powerflow.nbusslackidx, 'tensao']
                        * 1e-3
                    )
                    + 1e-8
                )
            ) and (not self.active_heuristic):

                # variação de tensão da barra slack
                if (powerflow.nbusname == 'ieee118') and (
                    sum(powerflow.nbusdbarraDF.demanda_ativa.to_numpy()) > 5400
                ):
                    pass

                else:
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                    self.case -= 1
                    Control(powerflow, powerflow,).controlpop(
                        powerflow,
                    )

                    # Reconfiguração das variáveis de passo
                    cpfkeys = {
                        'system',
                        'pmc',
                        'v2l',
                        'div',
                        'beta',
                        'step',
                        'stepsch',
                        'vsch',
                        'varstep',
                        'potencia_ativa',
                        'demanda_ativa',
                        'demanda_reativa',
                        'stepmax',
                    }
                    powerflow.cpfsolution = {
                        key: deepcopy(powerflow.case[self.case]['c'][key])
                        for key in powerflow.cpfsolution.keys() & cpfkeys
                    }
                    powerflow.cpfsolution['div'] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.solution['voltage'] = deepcopy(
                        powerflow.case[self.case]['c']['voltage']
                    )
                    powerflow.solution['theta'] = deepcopy(
                        powerflow.case[self.case]['c']['theta']
                    )

            # Condição de Heurísticas para controle
            if powerflow.nbuscontrolcount > 0:
                Control(powerflow, powerflow,).controlheuristics(
                    powerflow,
                )

                # Condição de violação de limite máximo de geração de potência reativa
                if (powerflow.nbuscontrolheur) and (not self.active_heuristic):
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.cpfsolution['div']) + 1
                    self.case -= 1
                    Control(powerflow, powerflow,).controlpop(
                        powerflow,
                    )

                    # Reconfiguração das variáveis de passo
                    cpfkeys = {
                        'system',
                        'pmc',
                        'v2l',
                        'div',
                        'beta',
                        'step',
                        'stepsch',
                        'vsch',
                        'varstep',
                        'potencia_ativa',
                        'demanda_ativa',
                        'demanda_reativa',
                        'stepmax',
                    }
                    powerflow.cpfsolution = {
                        key: deepcopy(powerflow.case[self.case]['c'][key])
                        for key in powerflow.cpfsolution.keys() & cpfkeys
                    }
                    powerflow.cpfsolution['div'] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.solution['voltage'] = deepcopy(
                        powerflow.case[self.case]['c']['voltage']
                    )
                    powerflow.solution['theta'] = deepcopy(
                        powerflow.case[self.case]['c']['theta']
                    )

                # Condição de atingimento de ponto de bifurcação
                if (powerflow.nbusbifurcation) and (not powerflow.cpfsolution['pmc']):
                    powerflow.cpfsolution['pmc'] = True
                    powerflow.nbuspmcidx = deepcopy(self.case)
                    powerflow.cpfsolution['varstep'] = 'volt'
                    powerflow.cpfsolution['div'] = 0
