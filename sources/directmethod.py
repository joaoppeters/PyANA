# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    array,
    concatenate,
    radians,
    sum,
    zeros,
)
from calc import PQCalc
from ctrl import Control
from hessian import Hessian
from jacobian import Jacobi


class DirectMethod:
    '''classe para cálculo do fluxo de potência não-linear via método direto (Canizares, 1993)'''

    def directmethod(
        self,
        powerflow,
    ):
        '''análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Variável para armazenamento de solução
        powerflow.solution = {
            'system': powerflow.nbusname,
            'iter': 0,
            'voltage': array(powerflow.dbarraDF['tensao'] * 1e-3),
            'theta': array(radians(powerflow.dbarraDF['angulo'])),
            'active': zeros(powerflow.nbusnbus),
            'reactive': zeros(powerflow.nbusnbus),
            'freq': 1.0,
            'freqiter': array([]),
            'convP': array([]),
            'busP': array([]),
            'convQ': array([]),
            'busQ': array([]),
            'convY': array([]),
            'busY': array([]),
            'step': 0.0,
            'stepsch': 0.0,
            'potencia_ativa': deepcopy(powerflow.dbarraDF['potencia_ativa']),
            'demanda_ativa': deepcopy(powerflow.dbarraDF['demanda_ativa']),
            'demanda_reativa': deepcopy(powerflow.dbarraDF['demanda_reativa']),
        }

        # Controles
        Control(powerflow, powerflow).controlsol(
            powerflow,
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
        )
        
        # Matriz Jacobiana
        Jacobi().jacobi(
            powerflow,
        )
        
        # Matriz Hessiana
        Hessian().hessian(
            powerflow,
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
        self.preincrement = sum(powerflow.dbarraDF['demanda_ativa'].to_numpy())

        # Incremento de carga
        for idxinc, valueinc in powerflow.dincDF.iterrows():
            if valueinc['tipo_incremento_1'] == 'AREA':
                for idxbar, valuebar in powerflow.dbarraDF.iterrows():
                    if valuebar['area'] == valueinc['identificacao_incremento_1']:
                        # Incremento de Carregamento
                        powerflow.dbarraDF.at[
                            idxbar, 'demanda_ativa'
                        ] = powerflow.solution['demanda_ativa'][idxbar] * (
                            1 + powerflow.solution['stepsch']
                        )
                        powerflow.dbarraDF.at[
                            idxbar, 'demanda_reativa'
                        ] = powerflow.solution['demanda_reativa'][idxbar] * (
                            1 + powerflow.solution['stepsch']
                        )

            elif valueinc['tipo_incremento_1'] == 'BARR':
                # Reconfiguração da variável de índice
                idxinc = valueinc['identificacao_incremento_1'] - 1

                # Incremento de Carregamento
                powerflow.dbarraDF.at[
                    idxinc, 'demanda_ativa'
                ] = powerflow.solution['demanda_ativa'][idxinc] * (
                    1 + powerflow.solution['stepsch']
                )
                powerflow.dbarraDF.at[
                    idxinc, 'demanda_reativa'
                ] = powerflow.solution['demanda_reativa'][idxinc] * (
                    1 + powerflow.solution['stepsch']
                )

        self.deltaincrement = (
            sum(powerflow.dbarraDF['demanda_ativa'].to_numpy())
            - self.preincrement
        )

        # Incremento de geração
        if powerflow.nbuscodes['DGER']:
            for idxger, valueger in powerflow.nbusdgeraDF.iterrows():
                idx = valueger['numero'] - 1
                powerflow.dbarraDF.at[
                    idx, 'potencia_ativa'
                ] = powerflow.dbarraDF['potencia_ativa'][idx] + (
                    self.deltaincrement * valueger['fator_participacao']
                )

            powerflow.solution['potencia_ativa'] = deepcopy(
                powerflow.dbarraDF['potencia_ativa']
            )

        # Condição de atingimento do máximo incremento do nível de carregamento
        if (
            powerflow.solution['stepsch']
            == powerflow.dincDF.loc[0, 'maximo_incremento_potencia_ativa']
        ):
            powerflow.solution['pmc'] = True

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
        for idx, value in powerflow.dbarraDF.iterrows():
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
        powerflow.pqsch['potencia_ativa_especificada'] /= powerflow.options[
            'BASE'
        ]
        powerflow.pqsch[
            'potencia_reativa_especificada'
        ] /= powerflow.options['BASE']

        # Variáveis especificadas de controle ativos
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow).controlsch(
                powerflow,
            )

    def residue(
        self,
        powerflow,
    ):
        '''cálculo de resíduos das equações diferenciáveis

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # Vetores de resíduo
        powerflow.deltaP = zeros(powerflow.nbusnbus)
        powerflow.deltaQ = zeros(powerflow.nbusnbus)

        # Loop
        for idx, value in powerflow.dbarraDF.iterrows():
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
                ('QLIM' in powerflow.control)
                or ('QLIMs' in powerflow.control)
                or ('QLIMn' in powerflow.control)
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
            )
            self.concatresidue(
                powerflow,
            )
            powerflow.deltaPQY = concatenate(
                (powerflow.deltaPQY, powerflow.deltaY), axis=0
            )
        else:
            powerflow.deltaY = array([0])

    def concatresidue(
        self,
        powerflow,
    ):
        '''concatenação de resíduos de potências ativa e reativa

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # configuração completa
        powerflow.deltaPQY = concatenate(
            (powerflow.deltaP, powerflow.deltaQ), axis=0
        )
    
    def update_statevar(
        self,
        powerflow,
    ):
        '''atualização das variáveis de estado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        '''

        ## Inicialização
        # configuração completa
        powerflow.solution['theta'] += powerflow.nbusstatevar[
            0 : (powerflow.nbusnbus)
        ]
        powerflow.solution['voltage'] += powerflow.nbusstatevar[
            (powerflow.nbusnbus) : (2 * powerflow.nbusnbus)
        ]

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.nbuscontrolcount > 0:
            Control(powerflow, powerflow).controlupdt(
                powerflow,
            )

    