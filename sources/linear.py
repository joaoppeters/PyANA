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
            "system": powerflow.name,
            "iter": 1,
            "voltage": ones(powerflow.nbus),
            "theta": zeros(powerflow.nbus),
            "active": zeros(powerflow.nbus),
            "reactive": zeros(powerflow.nbus),
            "freq": array([]),
            "convP": array([]),
            "busP": array([]),
            "convQ": zeros([]),
            "busQ": zeros([]),
            "active_flow_F2": zeros(powerflow.nbusnlin),
            "reactive_flow_F2": zeros(powerflow.nbusnlin),
            "active_flow_2F": zeros(powerflow.nbusnlin),
            "reactive_flow_2F": zeros(powerflow.nbusnlin),
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
        self.B = deepcopy(powerflow.nbusbbus.imag)
        for i in range(0, powerflow.nbus):
            if powerflow.dbarDF["tipo"][i] == 2:
                powerflow.nbusslackline = i
                self.B[i, :] = 0
                self.B[:, i] = 0
                self.B[i, i] = 1
                break

        # Variáveis de estado
        powerflow.statevar = solve(-self.B, self.sch["potencia_ativa_especificada"])

        # Atualização das Variáveis de estado
        self.update_statevar(
            powerflow,
        )

        # Fluxo em linhas de transmissão
        self.line_flow(
            powerflow,
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"

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
            "potencia_ativa_especificada": zeros(powerflow.nbus),
            "potencia_reativa_especificada": zeros(powerflow.nbus),
        }

        # Loop
        for idx, value in powerflow.dbarDF.iterrows():
            # Potência ativa especificada
            self.sch["potencia_ativa_especificada"][idx] += float(
                value["potencia_ativa"]
            )
            self.sch["potencia_ativa_especificada"][idx] -= float(
                value["demanda_ativa"]
            )

        # Tratamento
        self.sch["potencia_ativa_especificada"] /= powerflow.options["BASE"]

    def residue(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações diferenciáveis"""

        ## Inicialização
        # Vetores de resíduo
        powerflow.deltaP = zeros(powerflow.nbus)
        powerflow.deltaQ = zeros(powerflow.nbus)

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
        powerflow.solution["freq"] = append(powerflow.solution["freq"], 0.0)

        # Trajetória de convergência da potência ativa
        powerflow.solution["convP"] = append(powerflow.solution["convP"], 0.0)
        powerflow.solution["busP"] = append(powerflow.solution["busP"], 0)

        # Trajetória de convergência da potência reativa
        powerflow.solution["convQ"] = append(powerflow.solution["convQ"], 0.0)
        powerflow.solution["busQ"] = append(powerflow.solution["busQ"], 0)

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
        powerflow.nbusbbus: ndarray = zeros(
            shape=[powerflow.nbus, powerflow.nbus], dtype="complex_"
        )
        # Linhas de transmissão e transformadores
        for _, value in powerflow.dlinDF.iterrows():
            # Elementos fora da diagonal (elemento série)
            if value["tap"] == 0.0:
                powerflow.nbusbbus[
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["de"]][
                        0
                    ],
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["para"]][
                        0
                    ],
                ] -= (
                    1 / complex(real=0.0, imag=value["reatancia"])
                ) * powerflow.options[
                    "BASE"
                ]
                powerflow.nbusbbus[
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["para"]][
                        0
                    ],
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["de"]][
                        0
                    ],
                ] -= (
                    1 / complex(real=0.0, imag=value["reatancia"])
                ) * powerflow.options[
                    "BASE"
                ]
            else:
                powerflow.nbusbbus[
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["de"]][
                        0
                    ],
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["para"]][
                        0
                    ],
                ] -= (
                    (1 / complex(real=0.0, imag=value["reatancia"]))
                    * powerflow.options["BASE"]
                ) / float(
                    value["tap"]
                )
                powerflow.nbusbbus[
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["para"]][
                        0
                    ],
                    powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["de"]][
                        0
                    ],
                ] -= (
                    (1 / complex(real=0.0, imag=value["reatancia"]))
                    * powerflow.options["BASE"]
                ) / float(
                    value["tap"]
                )

        # Bancos de capacitores e reatores
        for idx, value in powerflow.dbarDF.iterrows():
            powerflow.nbusbbus[idx, idx] = sum(-powerflow.nbusbbus[:, idx])

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
        powerflow.solution["theta"] = deepcopy(powerflow.statevar)

    def line_flow(
        self,
        powerflow,
    ):
        """cálculo do fluxo de potência nas linhas de transmissão

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        ## Inicialização
        for idx, value in powerflow.dlinDF.iterrows():
            k = powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["de"]][0]
            m = powerflow.dbarDF.index[powerflow.dbarDF["numero"] == value["para"]][0]

            # Potência ativa k -> m
            powerflow.solution["active_flow_F2"][idx] = abs(
                powerflow.nbusbbus[k, m]
            ) * (powerflow.solution["theta"][k] - powerflow.solution["theta"][m])

            # Potência ativa m -> k
            powerflow.solution["active_flow_2F"][idx] = abs(
                powerflow.nbusbbus[k, m]
            ) * (powerflow.solution["theta"][m] - powerflow.solution["theta"][k])

            # Potência ativa gerada pela barra k
            powerflow.solution["active"][k] += powerflow.solution["active_flow_F2"][idx]
            powerflow.solution["active"][m] += powerflow.solution["active_flow_2F"][idx]

        powerflow.solution["active_flow_F2"] *= powerflow.options["BASE"]
        powerflow.solution["active_flow_2F"] *= powerflow.options["BASE"]

        powerflow.solution["active"] *= powerflow.options["BASE"]
        powerflow.solution["active"] += powerflow.dbarDF["demanda_ativa"].values
