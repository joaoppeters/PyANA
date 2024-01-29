# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import abs, append, array, delete, insert, ndarray, ones, zeros
from numpy.linalg import solve


class LinearPF:
    """classe para cálculo do fluxo de potência não-linear via método linearizado"""

    def linear(
        self,
        powerflow,
    ):
        """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento de solução
        powerflow.solution = {
            "system": powerflow.setup.name,
            "iter": 1,
            'voltage': ones(powerflow.setup.nbus),
            'theta': zeros(powerflow.setup.nbus),
            "active": zeros(powerflow.setup.nbus),
            "reactive": zeros(powerflow.setup.nbus),
            "freq": array([]),
            "convP": array([]),
            "busP": array([]),
            "convQ": zeros([]),
            "busQ": zeros([]),
            "active_flow_F2": zeros(powerflow.setup.nlin),
            "reactive_flow_F2": zeros(powerflow.setup.nlin),
            "active_flow_2F": zeros(powerflow.setup.nlin),
            "reactive_flow_2F": zeros(powerflow.setup.nlin),
        }

        # Variáveis Especificadas
        self.scheduled(
            powerflow,
        )

        # Resíduos
        self.residue(
            powerflow,
        )

        # Armazenamento da trajetória de convergência
        self.convergence(
            powerflow,
        )

        # Matriz B
        self.linearadmit(
            powerflow,
        )
        self.B = deepcopy(powerflow.setup.bbus.imag)
        for i in range(0, powerflow.setup.nbus):
            if powerflow.setup.dbarraDF['tipo'][i] == 2:
                powerflow.setup.slackline = i
                self.B[i, :] = 0
                self.B[:, i] = 0
                self.B[i, i] = 1
                break

        # Variáveis de estado
        powerflow.setup.statevar = solve(
            -self.B, self.sch['potencia_ativa_especificada']
        )

        # Atualização das Variáveis de estado
        self.update_statevar(
            powerflow,
        )

        # Fluxo em linhas de transmissão
        self.line_flow(
            powerflow,
        )

        # Convergência
        powerflow.solution['convergence'] = "SISTEMA CONVERGENTE"

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
        self.sch = {
            'potencia_ativa_especificada': zeros(powerflow.setup.nbus),
            'potencia_reativa_especificada': zeros(powerflow.setup.nbus),
        }

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Potência ativa especificada
            self.sch['potencia_ativa_especificada'][idx] += float(
                value['potencia_ativa']
            )
            self.sch['potencia_ativa_especificada'][idx] -= float(
                value['demanda_ativa']
            )

        # Tratamento
        self.sch['potencia_ativa_especificada'] /= powerflow.setup.options['BASE']

    def residue(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações diferenciáveis"""

        ## Inicialização
        # Vetores de resíduo
        powerflow.deltaP = zeros(powerflow.setup.nbus)
        powerflow.deltaQ = zeros(powerflow.setup.nbus)

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
        powerflow.solution['freq'] = append(powerflow.solution['freq'], 0.0)

        # Trajetória de convergência da potência ativa
        powerflow.solution['convP'] = append(powerflow.solution['convP'], 0.0)
        powerflow.solution['busP'] = append(powerflow.solution['busP'], 0)

        # Trajetória de convergência da potência reativa
        powerflow.solution['convQ'] = append(powerflow.solution['convQ'], 0.0)
        powerflow.solution['busQ'] = append(powerflow.solution['busQ'], 0)

    def linearadmit(
        self,
        powerflow,
    ):
        """cálculo da matriz admitância com considerações lineares

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        ## Inicialização
        # Matriz B
        powerflow.setup.bbus: ndarray = zeros(
            shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype="complex_"
        )
        # Linhas de transmissão e transformadores
        for _, value in powerflow.setup.dlinhaDF.iterrows():
            # Elementos fora da diagonal (elemento série)
            if value['tap'] == 0.0:
                powerflow.setup.bbus[
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['de']
                    ][0],
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['para']
                    ][0],
                ] -= (
                    1 / complex(real=0.0, imag=value['reatancia'])
                ) * powerflow.setup.options[
                    "BASE"
                ]
                powerflow.setup.bbus[
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['para']
                    ][0],
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['de']
                    ][0],
                ] -= (
                    1 / complex(real=0.0, imag=value['reatancia'])
                ) * powerflow.setup.options[
                    "BASE"
                ]
            else:
                powerflow.setup.bbus[
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['de']
                    ][0],
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['para']
                    ][0],
                ] -= (
                    (1 / complex(real=0.0, imag=value['reatancia']))
                    * powerflow.setup.options['BASE']
                ) / float(
                    value['tap']
                )
                powerflow.setup.bbus[
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['para']
                    ][0],
                    powerflow.setup.dbarraDF.index[
                        powerflow.setup.dbarraDF['numero'] == value['de']
                    ][0],
                ] -= (
                    (1 / complex(real=0.0, imag=value['reatancia']))
                    * powerflow.setup.options['BASE']
                ) / float(
                    value['tap']
                )

        # Bancos de capacitores e reatores
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            powerflow.setup.bbus[idx, idx] = sum(-powerflow.setup.bbus[:, idx])

    def update_statevar(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # atualização dos ângulos dos barramentos
        powerflow.solution['theta'] = deepcopy(powerflow.setup.statevar)

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
            k = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['de']
            ][0]
            m = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['para']
            ][0]

            # Potência ativa k -> m
            powerflow.solution['active_flow_F2'][idx] = abs(
                powerflow.setup.bbus[k, m]
            ) * (powerflow.solution['theta'][k] - powerflow.solution['theta'][m])

            # Potência ativa m -> k
            powerflow.solution['active_flow_2F'][idx] = abs(
                powerflow.setup.bbus[k, m]
            ) * (powerflow.solution['theta'][m] - powerflow.solution['theta'][k])

            # Potência ativa gerada pela barra k
            powerflow.solution['active'][k] += powerflow.solution['active_flow_F2'][idx]
            powerflow.solution['active'][m] += powerflow.solution['active_flow_2F'][idx]

        powerflow.solution['active_flow_F2'] *= powerflow.setup.options['BASE']
        powerflow.solution['active_flow_2F'] *= powerflow.setup.options['BASE']

        powerflow.solution['active'] *= powerflow.setup.options['BASE']
        powerflow.solution['active'] += powerflow.setup.dbarraDF['demanda_ativa'].values
