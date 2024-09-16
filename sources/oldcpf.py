# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    abs,
    absolute,
    all,
    append,
    argmax,
    arange,
    array,
    concatenate,
    cos,
    dot,
    insert,
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
from newton import newton
from smooth import Smooth


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
        newton(
            powerflow,
        )

        # Continuado
        self.continuationpowerflow(
            powerflow,
        )

        del powerflow.case[len(powerflow.case) - 1]

        # Geração e armazenamento de gráficos de perfil de tensão e autovalores
        Loading(
            powerflow,
        )

        # # Smooth
        # if ('QLIMs' in powerflow.setting.control):
        #     for k, v in powerflow.setting.qlimkeys.items():
        #         v.popitem()
        #     Smooth(powerflow,).qlimstorage(powerflow,)
        if "SVCs" in powerflow.setting.control:
            for k, v in powerflow.setting.svckeys.items():
                v.popitem()
            Smooth(
                powerflow,
            ).svcstorage(
                powerflow,
            )

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
            "pmc": False,
            "v2l": False,
            "div": 0,
            "beta": deepcopy(powerflow.setting.options["cpfBeta"]),
            "step": 0.0,
            "stepsch": 0.0,
            "vsch": 0.0,
            "stepmax": 0.0,
            "varstep": "lambda",
            "potencia_ativa": deepcopy(powerflow.setting.dbarraDF["potencia_ativa"]),
            "demanda_ativa": deepcopy(powerflow.setting.dbarraDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(powerflow.setting.dbarraDF["demanda_reativa"]),
        }

        # Variável para armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
        Control(
            powerflow,
            powerflow.setting,
        ).controlcpf(
            powerflow,
        )

        # Variável para armazenamento da solução do fluxo de potência continuado
        powerflow.case = dict()

        # Variável para armazenamento de solução por casos do continuado (previsão e correção)
        self.case = 0

        # Armazenamento da solução inicial
        powerflow.case[self.case] = {
            **deepcopy(powerflow.sol),
            **deepcopy(powerflow.cpfsol),
        }

        # Armazenamento de determinante e autovalores
        self.eigensens(
            powerflow,
        )

        # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
        powerflow.setting.mask = append(powerflow.setting.mask, False)

        # Dimensão da matriz Jacobiana
        powerflow.setting.jdim = powerflow.setting.jacob.shape[0]

        # Barra com maior variação de magnitude de tensão - CASO BASE
        powerflow.setting.nodevarvolt = argmax(
            abs(powerflow.sol["voltage"] - powerflow.setting.dbarraDF["tensao"] * 1e-3)
        )

        # Loop de Previsão - Correção
        self.cpfloop(
            powerflow,
        )

    def cpfloop(
        self,
        powerflow,
    ):
        """loop do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Condição de parada do fluxo de potência continuado -> Estável & Instável
        while all((powerflow.sol["voltage"] >= 0.0)) and (
            sum(powerflow.setting.dbarraDF["demanda_ativa"])
            >= 0.99 * sum(powerflow.cpfsol["demanda_ativa"])
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

            if (powerflow.sol["convergence"] == "SISTEMA CONVERGENTE") and (
                self.case > 0
            ):
                print("Aumento Sistema (%): ", powerflow.cpfsol["step"] * 1e2)
                if powerflow.cpfsol["varstep"] == "volt":
                    print(
                        "Passo (%): ",
                        powerflow.case[self.case]["corr"]["varstep"],
                        "  ",
                        powerflow.setting.options["cpfVolt"]
                        * (5e-1 ** powerflow.cpfsol["div"])
                        * 1e2,
                    )
                else:
                    print(
                        "Passo (%): ",
                        powerflow.case[self.case]["corr"]["varstep"],
                        "  ",
                        powerflow.setting.options["cpfLambda"]
                        * (5e-1 ** powerflow.cpfsol["div"])
                        * 1e2,
                    )
                print("\n")

            if (powerflow.setting.name == "2b-milano") and (
                (1 + powerflow.case[self.case]["prev"]["step"])
                * sum(powerflow.cpfsol["demanda_ativa"])
                >= 190.0
            ):
                print("")

            # Break Curva de Carregamento - Parte Estável
            if (not powerflow.setting.options["full"]) and (powerflow.cpfsol["pmc"]):
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
            stage="prev",
        )

        # Atualização da Matriz Jacobiana
        Jacobi(
            powerflow,
        )

        # Expansão Jacobiana
        self.exicjacobian(
            powerflow,
        )

        # Variáveis de estado
        powerflow.setting.statevar = solve(
            powerflow.setting.jacob, powerflow.setting.deltaPQY
        )

        # Atualização das Variáveis de estado
        self.update_statevar(
            powerflow,
            stage="prev",
        )

        # Fluxo em linhas de transmissão
        self.line_flow(
            powerflow,
        )

        # Armazenamento de Solução
        self.storage(
            powerflow,
            stage="prev",
        )

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
            "iter": 0,
            "voltage": deepcopy(powerflow.case[self.case]["prev"]["voltage"]),
            "theta": deepcopy(powerflow.case[self.case]["prev"]["theta"]),
            "active": deepcopy(powerflow.case[self.case]["prev"]["active"]),
            "reactive": deepcopy(powerflow.case[self.case]["prev"]["reactive"]),
            "freq": deepcopy(powerflow.case[self.case]["prev"]["freq"]),
            "freqiter": array([]),
            "convP": array([]),
            "busP": array([]),
            "convQ": array([]),
            "busQ": array([]),
            "convY": array([]),
            "busY": array([]),
            "active_flow_F2": zeros(powerflow.setting.nlin),
            "reactive_flow_F2": zeros(powerflow.setting.nlin),
            "active_flow_2F": zeros(powerflow.setting.nlin),
            "reactive_flow_2F": zeros(powerflow.setting.nlin),
        }

        # Adição de variáveis de controle na variável de armazenamento de solução
        Control(
            powerflow,
            powerflow.setting,
        ).controlcorrsol(
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
            stage="corr",
        )

        while (
            (max(abs(powerflow.setting.deltaP)) >= powerflow.setting.options["tolP"])
            or (max(abs(powerflow.setting.deltaQ)) >= powerflow.setting.options["tolQ"])
            or (max(abs(powerflow.setting.deltaY)) >= powerflow.setting.options["tolY"])
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
            self.exicjacobian(
                powerflow,
            )

            # Variáveis de estado
            powerflow.setting.statevar = solve(
                powerflow.setting.jacob, powerflow.setting.deltaPQY
            )

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage="corr",
            )

            # Condição de variável de passo
            if powerflow.cpfsol["varstep"] == "volt":
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
                stage="corr",
            )

            # Incremento de iteração
            powerflow.sol["iter"] += 1

            # Condição de Divergência por iterações
            if powerflow.sol["iter"] > powerflow.setting.options["itermx"]:
                powerflow.sol["convergence"] = (
                    "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
                )
                break

        ## Condição
        # Iteração Adicional em Caso de Convergência
        if powerflow.sol["iter"] < powerflow.setting.options["itermx"]:
            # Armazenamento da trajetória de convergência
            self.convergence(
                powerflow,
            )

            # Atualização da Matriz Jacobiana
            Jacobi(
                powerflow,
            )

            # Expansão Jacobiana
            self.exicjacobian(
                powerflow,
            )

            # Variáveis de estado
            powerflow.setting.statevar = solve(
                powerflow.setting.jacob, powerflow.setting.deltaPQY
            )

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage="corr",
            )

            # Atualização dos resíduos
            self.residue(
                powerflow,
                stage="corr",
            )

            # Fluxo em linhas de transmissão
            self.line_flow(
                powerflow,
            )

            # Armazenamento de Solução
            self.storage(
                powerflow,
                stage="corr",
            )

            # Convergência
            powerflow.sol["convergence"] = "SISTEMA CONVERGENTE"

            # Avaliação
            self.exicevaluate(
                powerflow,
            )

            # Heurísticas
            self.heuristics(
                powerflow,
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.sol["iter"] >= powerflow.setting.options["itermx"])) and (
            self.case == 1
        ):
            self.active_heuristic = True
            powerflow.sol["convergence"] = "SISTEMA DIVERGENTE"

            # Reconfiguração do caso
            self.case -= 1
            Control(
                powerflow,
                powerflow.setting,
            ).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.sol["voltage"] = deepcopy(
                powerflow.case[self.case]["corr"]["voltage"]
            )
            powerflow.sol["theta"] = deepcopy(
                powerflow.case[self.case]["corr"]["theta"]
            )

            # Reconfiguração da variável de passo
            powerflow.cpfsol["div"] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.cpfsol["step"] = deepcopy(
                powerflow.case[self.case]["corr"]["step"]
            )
            powerflow.cpfsol["stepsch"] = deepcopy(
                powerflow.case[self.case]["corr"]["stepsch"]
            )
            powerflow.cpfsol["vsch"] = deepcopy(
                powerflow.case[self.case]["corr"]["vsch"]
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.sol["iter"] >= powerflow.setting.options["itermx"])) and (
            self.case > 1
        ):
            self.active_heuristic = True
            powerflow.sol["convergence"] = "SISTEMA DIVERGENTE"

            # Reconfiguração do caso
            self.case -= 1
            Control(
                powerflow,
                powerflow.setting,
            ).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.sol["voltage"] = deepcopy(
                powerflow.case[self.case]["corr"]["voltage"]
            )
            powerflow.sol["theta"] = deepcopy(
                powerflow.case[self.case]["corr"]["theta"]
            )

            # Reconfiguração da variável de passo
            powerflow.cpfsol["div"] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.cpfsol["step"] = deepcopy(
                powerflow.case[self.case]["corr"]["step"]
            )
            powerflow.cpfsol["stepsch"] = deepcopy(
                powerflow.case[self.case]["corr"]["stepsch"]
            )
            powerflow.cpfsol["vsch"] = deepcopy(
                powerflow.case[self.case]["corr"]["vsch"]
            )

    def increment(
        self,
        powerflow,
    ):
        """realiza incremento no nível de carregamento (e geração)

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        self.preincrement = sum(powerflow.setting.dbarraDF["demanda_ativa"].to_numpy())

        # Incremento de carga
        for idxinc, valueinc in powerflow.setting.dincDF.iterrows():
            if valueinc["tipo_incremento_1"] == "AREA":
                for idxbar, valuebar in powerflow.setting.dbarraDF.iterrows():
                    if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                        # Incremento de Carregamento
                        powerflow.setting.dbarraDF.at[idxbar, "demanda_ativa"] = (
                            powerflow.cpfsol["demanda_ativa"][idxbar]
                            * (1 + powerflow.cpfsol["stepsch"])
                        )
                        powerflow.setting.dbarraDF.at[idxbar, "demanda_reativa"] = (
                            powerflow.cpfsol["demanda_reativa"][idxbar]
                            * (1 + powerflow.cpfsol["stepsch"])
                        )

            elif valueinc["tipo_incremento_1"] == "BARR":
                # Reconfiguração da variável de índice
                idxinc = valueinc["identificacao_incremento_1"] - 1

                # Incremento de Carregamento
                powerflow.setting.dbarraDF.at[idxinc, "demanda_ativa"] = powerflow.cpfsol[
                    "demanda_ativa"
                ][idxinc] * (1 + powerflow.cpfsol["stepsch"])
                powerflow.setting.dbarraDF.at[idxinc, "demanda_reativa"] = (
                    powerflow.cpfsol["demanda_reativa"][idxinc]
                    * (1 + powerflow.cpfsol["stepsch"])
                )

        self.deltaincrement = (
            sum(powerflow.setting.dbarraDF["demanda_ativa"].to_numpy())
            - self.preincrement
        )

        # Incremento de geração
        if hasattr(powerflow.setting, "dgeraDF"):
            for idxger, valueger in powerflow.setting.dgeraDF.iterrows():
                idx = valueger["numero"] - 1
                powerflow.setting.dbarraDF.at[idx, "potencia_ativa"] = (
                    powerflow.setting.dbarraDF["potencia_ativa"][idx]
                    + (self.deltaincrement * valueger["fator_participacao"])
                )

            powerflow.cpfsol["potencia_ativa"] = deepcopy(
                powerflow.setting.dbarraDF["potencia_ativa"]
            )

        # Condição de atingimento do máximo incremento do nível de carregamento
        if (
            powerflow.cpfsol["stepsch"]
            == powerflow.setting.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
        ):
            powerflow.cpfsol["pmc"] = True

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
        powerflow.setting.pqsch = {
            "potencia_ativa_especificada": zeros(powerflow.setting.nbus),
            "potencia_reativa_especificada": zeros(powerflow.setting.nbus),
        }

        # Loop
        for idx, value in powerflow.setting.dbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.setting.pqsch["potencia_ativa_especificada"][idx] += value[
                "potencia_ativa"
            ]
            powerflow.setting.pqsch["potencia_ativa_especificada"][idx] -= value[
                "demanda_ativa"
            ]

            # Potência reativa especificada
            powerflow.setting.pqsch["potencia_reativa_especificada"][idx] += value[
                "potencia_reativa"
            ]
            powerflow.setting.pqsch["potencia_reativa_especificada"][idx] -= value[
                "demanda_reativa"
            ]

        # Tratamento
        powerflow.setting.pqsch["potencia_ativa_especificada"] /= powerflow.setting.options[
            "sbase"
        ]
        powerflow.setting.pqsch[
            "potencia_reativa_especificada"
        ] /= powerflow.setting.options["sbase"]

        # Variáveis especificadas de controle ativos
        if powerflow.setting.controlcount > 0:
            Control(powerflow, powerflow.setting).controlsch(
                powerflow,
            )

    def residue(
        self,
        powerflow,
        stage: str = None,
    ):
        """cálculo de resíduos das equações diferenciáveis

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # Vetores de resíduo
        powerflow.setting.deltaP = zeros(powerflow.setting.nbus)
        powerflow.setting.deltaQ = zeros(powerflow.setting.nbus)

        # Resíduo de equação de controle adicional
        powerflow.setting.deltaY = array([])

        # Loop
        for idx, value in powerflow.setting.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if value["tipo"] != 2:
                powerflow.setting.deltaP[idx] += powerflow.setting.pqsch[
                    "potencia_ativa_especificada"
                ][idx]
                powerflow.setting.deltaP[idx] -= PQCalc().pcalc(
                    powerflow,
                    idx,
                )

            # Tipo PQ - Resíduo Potência Reativa
            if (
                ("QLIM" in powerflow.setting.control)
                or ("QLIMs" in powerflow.setting.control)
                or (value["tipo"] == 0)
            ):
                powerflow.setting.deltaQ[idx] += powerflow.setting.pqsch[
                    "potencia_reativa_especificada"
                ][idx]
                powerflow.setting.deltaQ[idx] -= PQCalc().qcalc(
                    powerflow,
                    idx,
                )

        # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
        self.concatresidue(
            powerflow,
        )

        # Resíduos de variáveis de estado de controle
        if powerflow.setting.controlcount > 0:
            Control(powerflow, powerflow.setting).controlres(
                powerflow,
                self.case,
            )
            self.concatresidue(
                powerflow,
            )
            powerflow.setting.deltaPQY = concatenate(
                (powerflow.setting.deltaPQY, powerflow.setting.deltaY), axis=0
            )

        # Resíduo de Fluxo de Potência Continuado
        # Condição de previsão
        if stage == "prev":
            powerflow.setting.deltaPQY = zeros(powerflow.setting.deltaPQY.shape[0] + 1)
            # Condição de variável de passo
            if powerflow.cpfsol["varstep"] == "lambda":
                if not powerflow.cpfsol["pmc"]:
                    powerflow.setting.deltaPQY[-1] = powerflow.setting.options[
                        "cpfLambda"
                    ] * (5e-1 ** powerflow.cpfsol["div"])

                elif powerflow.cpfsol["pmc"]:
                    powerflow.setting.deltaPQY[-1] = (
                        -1
                        * powerflow.setting.options["cpfLambda"]
                        * (5e-1 ** powerflow.cpfsol["div"])
                    )

            elif powerflow.cpfsol["varstep"] == "volt":
                powerflow.setting.deltaPQY[-1] = (
                    -1
                    * powerflow.setting.options["cpfVolt"]
                    * (5e-1 ** powerflow.cpfsol["div"])
                )

        # Condição de correção
        elif stage == "corr":
            # Condição de variável de passo
            if powerflow.cpfsol["varstep"] == "lambda":
                powerflow.setting.deltaY = array(
                    [powerflow.cpfsol["stepsch"] - powerflow.cpfsol["step"]]
                )

            elif powerflow.cpfsol["varstep"] == "volt":
                powerflow.setting.deltaY = array(
                    [
                        powerflow.cpfsol["vsch"]
                        - powerflow.sol["voltage"][powerflow.setting.nodevarvolt]
                    ]
                )

            powerflow.setting.deltaPQY = concatenate(
                (powerflow.setting.deltaPQY, powerflow.setting.deltaY), axis=0
            )

    def concatresidue(
        self,
        powerflow,
    ):
        """determinação do vetor de resíduos

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # configuração completa
        powerflow.setting.deltaPQY = concatenate(
            (powerflow.setting.deltaP, powerflow.setting.deltaQ), axis=0
        )

    def exicjacobian(
        self,
        powerflow,
    ):
        """expansão da matriz jacobiana para o método continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Arrays adicionais
        rowarray = zeros([1, powerflow.setting.jdim])
        colarray = zeros([powerflow.setting.jdim, 1])
        stepvar = zeros(1)

        # Condição de variável de passo
        if powerflow.cpfsol["varstep"] == "lambda":
            stepvar[0] = 1

        elif powerflow.cpfsol["varstep"] == "volt":
            rowarray[0, (powerflow.setting.nbus + powerflow.setting.nodevarvolt)] = 1

        # Demanda
        for idx, value in powerflow.setting.dbarraDF.iterrows():
            if value["tipo"] != 2:
                colarray[idx, 0] = (
                    powerflow.cpfsol["demanda_ativa"][idx]
                    - powerflow.cpfsol["potencia_ativa"][idx]
                )
                if value["tipo"] == 0:
                    colarray[(idx + powerflow.setting.nbus), 0] = powerflow.cpfsol[
                        "demanda_reativa"
                    ][idx]

        colarray /= powerflow.setting.options["sbase"]

        # Expansão Inferior
        powerflow.setting.jacob = concatenate((powerflow.setting.jacob, colarray), axis=1)

        # Expansão Lateral
        powerflow.setting.jacob = concatenate(
            (powerflow.setting.jacob, concatenate((rowarray, [stepvar]), axis=1)), axis=0
        )

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
        powerflow.sol["freqiter"] = append(
            powerflow.sol["freqiter"],
            powerflow.sol["freq"] * powerflow.setting.options["fbase"],
        )

        # Trajetória de convergência da potência ativa
        powerflow.sol["convP"] = append(
            powerflow.sol["convP"], max(abs(powerflow.setting.deltaP))
        )
        powerflow.sol["busP"] = append(
            powerflow.sol["busP"], argmax(abs(powerflow.setting.deltaP))
        )

        # Trajetória de convergência da potência reativa
        powerflow.sol["convQ"] = append(
            powerflow.sol["convQ"], max(abs(powerflow.setting.deltaQ))
        )
        powerflow.sol["busQ"] = append(
            powerflow.sol["busQ"], argmax(abs(powerflow.setting.deltaQ))
        )

        # Trajetória de convergência referente a cada equação de controle adicional
        if powerflow.setting.deltaY.size != 0:
            powerflow.sol["convY"] = append(
                powerflow.sol["convY"], max(abs(powerflow.setting.deltaY))
            )
            powerflow.sol["busY"] = append(
                powerflow.sol["busY"], argmax(abs(powerflow.setting.deltaY))
            )

        elif powerflow.setting.deltaY.size == 0:
            powerflow.sol["convY"] = append(powerflow.sol["convY"], 0.0)
            powerflow.sol["busY"] = append(powerflow.sol["busY"], 0.0)

    def update_statevar(
        self,
        powerflow,
        stage: str = None,
    ):
        """atualização das variáveis de estado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # configuração completa
        powerflow.sol["theta"] += powerflow.setting.statevar[0 : (powerflow.setting.nbus)]
        # Condição de previsão
        if stage == "prev":
            # Condição de variável de passo
            if powerflow.cpfsol["varstep"] == "lambda":
                powerflow.sol["voltage"] += powerflow.setting.statevar[
                    (powerflow.setting.nbus) : (2 * powerflow.setting.nbus)
                ]
                powerflow.cpfsol["stepsch"] += powerflow.setting.statevar[-1]

            elif powerflow.cpfsol["varstep"] == "volt":
                powerflow.cpfsol["step"] += powerflow.setting.statevar[-1]
                powerflow.cpfsol["stepsch"] += powerflow.setting.statevar[-1]
                powerflow.cpfsol["vsch"] = (
                    powerflow.sol["voltage"][powerflow.setting.nodevarvolt]
                    + powerflow.setting.statevar[
                        (powerflow.setting.nbus + powerflow.setting.nodevarvolt)
                    ]
                )

            # Verificação do Ponto de Máximo Carregamento
            if self.case > 0:
                if self.case == 1:
                    powerflow.cpfsol["stepmax"] = deepcopy(powerflow.cpfsol["stepsch"])

                elif self.case != 1:
                    if (
                        powerflow.cpfsol["stepsch"]
                        > powerflow.case[self.case - 1]["corr"]["step"]
                    ) and (not powerflow.cpfsol["pmc"]):
                        powerflow.cpfsol["stepmax"] = deepcopy(
                            powerflow.cpfsol["stepsch"]
                        )

                    elif (
                        powerflow.cpfsol["stepsch"]
                        < powerflow.case[self.case - 1]["corr"]["step"]
                    ) and (not powerflow.cpfsol["pmc"]):
                        powerflow.cpfsol["pmc"] = True
                        powerflow.setting.pmcidx = deepcopy(self.case)

        # Condição de correção
        elif stage == "corr":
            powerflow.sol["voltage"] += powerflow.setting.statevar[
                (powerflow.setting.nbus) : (2 * powerflow.setting.nbus)
            ]
            powerflow.cpfsol["step"] += powerflow.setting.statevar[-1]

            if powerflow.cpfsol["varstep"] == "volt":
                powerflow.cpfsol["stepsch"] += powerflow.setting.statevar[-1]

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.setting.controlcount > 0:
            Control(powerflow, powerflow.setting).controlupdt(
                powerflow,
            )

    def line_flow(
        self,
        powerflow,
    ):
        """cálculo do fluxo de potência nas linhas de transmissão

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        for idx, value in powerflow.setting.dlinhaDF.iterrows():
            k = powerflow.setting.dbarraDF.index[
                powerflow.setting.dbarraDF["numero"] == value["de"]
            ][0]
            m = powerflow.setting.dbarraDF.index[
                powerflow.setting.dbarraDF["numero"] == value["para"]
            ][0]
            yline = 1 / ((value["resistencia"] / 100) + 1j * (value["reatancia"] / 100))

            # Verifica presença de transformadores com tap != 1.
            if value["tap"] != 0:
                yline /= value["tap"]

            # Potência ativa k -> m
            powerflow.sol["active_flow_F2"][idx] = yline.real * (
                powerflow.sol["voltage"][k] ** 2
            ) - powerflow.sol["voltage"][k] * powerflow.sol["voltage"][m] * (
                yline.real * cos(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
                + yline.imag
                * sin(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
            )

            # Potência reativa k -> m
            powerflow.sol["reactive_flow_F2"][idx] = -(
                (value["susceptancia"] / (2 * powerflow.setting.options["sbase"]))
                + yline.imag
            ) * (powerflow.sol["voltage"][k] ** 2) + powerflow.sol["voltage"][
                k
            ] * powerflow.sol[
                "voltage"
            ][
                m
            ] * (
                yline.imag * cos(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
                - yline.real
                * sin(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
            )

            # Potência ativa m -> k
            powerflow.sol["active_flow_2F"][idx] = yline.real * (
                powerflow.sol["voltage"][m] ** 2
            ) - powerflow.sol["voltage"][k] * powerflow.sol["voltage"][m] * (
                yline.real * cos(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
                - yline.imag
                * sin(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
            )

            # Potência reativa m -> k
            powerflow.sol["reactive_flow_2F"][idx] = -(
                (value["susceptancia"] / (2 * powerflow.setting.options["sbase"]))
                + yline.imag
            ) * (powerflow.sol["voltage"][m] ** 2) + powerflow.sol["voltage"][
                k
            ] * powerflow.sol[
                "voltage"
            ][
                m
            ] * (
                yline.imag * cos(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
                + yline.real
                * sin(powerflow.sol["theta"][k] - powerflow.sol["theta"][m])
            )

        powerflow.sol["active_flow_F2"] *= powerflow.setting.options["sbase"]
        powerflow.sol["active_flow_2F"] *= powerflow.setting.options["sbase"]

        powerflow.sol["reactive_flow_F2"] *= powerflow.setting.options["sbase"]
        powerflow.sol["reactive_flow_2F"] *= powerflow.setting.options["sbase"]

    def storage(
        self,
        powerflow,
        stage: str = None,
    ):
        """armazenamento dos resultados de fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
        """

        ## Inicialização
        # Armazenamento das variáveis de solução do fluxo de potência
        powerflow.case[self.case][stage] = {
            **deepcopy(powerflow.sol),
            **deepcopy(powerflow.cpfsol),
        }

        if "SVCs" in powerflow.setting.control:
            powerflow.case[self.case][stage]["svc_generation"] = deepcopy(
                powerflow.sol["svc_generation"]
            )

        # Armazenamento do índice do barramento com maior variação de magnitude de tensão
        powerflow.case[self.case]["nodevarvolt"] = deepcopy(powerflow.setting.nodevarvolt)

        # Análise de sensibilidade e armazenamento
        self.eigensens(
            powerflow,
            stage=stage,
        )

    def eigensens(
        self,
        powerflow,
        stage: str = None,
    ):
        """análise de autovalores e autovetores

        Parâmetros
            powerflow: self do arquivo powerflow.py
            stage: string de identificação da etapa do fluxo de potência continuado
        """

        ## Inicialização
        # Reorganização da Matriz Jacobiana Expandida
        self.jacob = deepcopy(powerflow.setting.jacob)

        if self.case > 0:
            self.jacob = self.jacob[:-1, :-1]

        # # Submatrizes Jacobianas
        self.pt = deepcopy(
            self.jacob[: (2 * powerflow.setting.nbus), :][:, : (2 * powerflow.setting.nbus)]
        )
        self.pv = deepcopy(
            self.jacob[: (2 * powerflow.setting.nbus), :][
                :,
                (2 * powerflow.setting.nbus) : (
                    2 * powerflow.setting.nbus + powerflow.setting.totaldevicescontrol
                ),
            ]
        )
        self.qt = deepcopy(
            self.jacob[
                (2 * powerflow.setting.nbus) : (
                    2 * powerflow.setting.nbus + powerflow.setting.totaldevicescontrol
                ),
                :,
            ][:, : (2 * powerflow.setting.nbus)]
        )
        self.qv = deepcopy(
            self.jacob[
                (2 * powerflow.setting.nbus) : (
                    2 * powerflow.setting.nbus + powerflow.setting.totaldevicescontrol
                ),
                :,
            ][
                :,
                (2 * powerflow.setting.nbus) : (
                    2 * powerflow.setting.nbus + powerflow.setting.totaldevicescontrol
                ),
            ]
        )

        try:
            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            rightvalues, rightvector = eig(
                powerflow.setting.jacob[powerflow.setting.mask, :][:, powerflow.setting.mask]
            )
            powerflow.setting.PF = zeros(
                [
                    powerflow.setting.jacob[powerflow.setting.mask, :][
                        :, powerflow.setting.mask
                    ].shape[0],
                    powerflow.setting.jacob[powerflow.setting.mask, :][
                        :, powerflow.setting.mask
                    ].shape[1],
                ]
            )

            # Jacobiana reduzida - sensibilidade QV
            powerflow.setting.jacobQV = self.qv - dot(dot(self.qt, inv(self.pt)), self.pv)
            rightvaluesQV, rightvectorQV = eig(powerflow.setting.jacobQV)
            rightvaluesQV = absolute(rightvaluesQV)
            powerflow.setting.PFQV = zeros(
                [powerflow.setting.jacobQV.shape[0], powerflow.setting.jacobQV.shape[1]]
            )
            for row in range(0, powerflow.setting.jacobQV.shape[0]):
                for col in range(0, powerflow.setting.jacobQV.shape[1]):
                    powerflow.setting.PFQV[col, row] = (
                        rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                    )

            # Condição
            if stage == None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.case[self.case]["jacobian"] = powerflow.setting.jacob[
                    powerflow.setting.mask, :
                ][:, powerflow.setting.mask]

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.case[self.case]["determinant"] = det(
                    powerflow.setting.jacob[powerflow.setting.mask, :][
                        :, powerflow.setting.mask
                    ]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.case[self.case]["eigenvalues"] = rightvalues
                powerflow.case[self.case]["eigenvectors"] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.case[self.case]["participation_factor"] = powerflow.setting.PF

                # Armazenamento da matriz de sensibilidade QV
                powerflow.case[self.case]["jacobian-QV"] = powerflow.setting.jacobQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.case[self.case]["determinant-QV"] = det(
                    powerflow.setting.jacobQV
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.case[self.case]["eigenvalues-QV"] = rightvaluesQV
                powerflow.case[self.case]["eigenvectors-QV"] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.case[self.case][
                    "participationfactor-QV"
                ] = powerflow.setting.PFQV

            elif stage != None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.case[self.case][stage]["jacobian"] = powerflow.setting.jacob

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.case[self.case][stage]["determinant"] = det(
                    powerflow.setting.jacob[powerflow.setting.mask, :][
                        :, powerflow.setting.mask
                    ]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.case[self.case][stage]["eigenvalues"] = rightvalues
                powerflow.case[self.case][stage]["eigenvectors"] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.case[self.case][stage][
                    "participationfactor"
                ] = powerflow.setting.PF

                # Armazenamento da matriz de sensibilidade QV
                powerflow.case[self.case][stage][
                    "jacobian-QV"
                ] = powerflow.setting.jacobQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.case[self.case][stage]["determinant-QV"] = det(
                    powerflow.setting.jacobQV
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.case[self.case][stage]["eigenvalues-QV"] = rightvaluesQV
                powerflow.case[self.case][stage]["eigenvectors-QV"] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.case[self.case][stage][
                    "participationfactor-QV"
                ] = powerflow.setting.PFQV

        # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
        # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
        except:
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
            self.case -= 1
            Control(
                powerflow,
                powerflow.setting,
            ).controlpop(
                powerflow,
            )

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                "system",
                "pmc",
                "v2l",
                "div",
                "beta",
                "step",
                "stepsch",
                "vsch",
                "varstep",
                "potencia_ativa",
                "demanda_ativa",
                "demanda_reativa",
                "stepmax",
            }
            powerflow.cpfsol = {
                key: deepcopy(powerflow.case[self.case]["corr"][key])
                for key in powerflow.cpfsol.keys() & cpfkeys
            }
            powerflow.cpfsol["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.sol["voltage"] = deepcopy(
                powerflow.case[self.case]["corr"]["voltage"]
            )
            powerflow.sol["theta"] = deepcopy(
                powerflow.case[self.case]["corr"]["theta"]
            )

            # # Loop
            # pass

    def exicevaluate(
        self,
        powerflow,
    ):
        """avaliação para determinação do passo do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Condição Inicial
        if self.case == 1:
            # Lambda
            self.varlambda = abs(
                (powerflow.cpfsol["step"] - 0) / (powerflow.cpfsol["step"])
            )

            # Voltage
            powerflow.setting.nodevarvolt = argmax(
                abs(powerflow.sol["voltage"] - powerflow.case[0]["voltage"])
            )
            self.varvolt = abs(
                (
                    powerflow.sol["voltage"][powerflow.setting.nodevarvolt]
                    - powerflow.case[0]["voltage"][powerflow.setting.nodevarvolt]
                )
                / powerflow.sol["voltage"][powerflow.setting.nodevarvolt]
            )

        # Condição Durante
        elif self.case != 1:
            # Lambda
            self.varlambda = abs(
                (
                    powerflow.case[self.case]["corr"]["step"]
                    - powerflow.case[self.case - 1]["corr"]["step"]
                )
                / powerflow.case[self.case]["corr"]["step"]
            )

            # Voltage
            powerflow.setting.nodevarvolt = argmax(
                abs(
                    powerflow.sol["voltage"]
                    - powerflow.case[self.case - 1]["corr"]["voltage"]
                )
            )
            self.varvolt = abs(
                (
                    powerflow.case[self.case]["corr"]["voltage"][
                        powerflow.setting.nodevarvolt
                    ]
                    - powerflow.case[self.case - 1]["corr"]["voltage"][
                        powerflow.setting.nodevarvolt
                    ]
                )
                / powerflow.case[self.case]["corr"]["voltage"][
                    powerflow.setting.nodevarvolt
                ]
            )

        # Avaliação
        if (self.varlambda > self.varvolt) and (
            powerflow.cpfsol["varstep"] == "lambda"
        ):
            powerflow.cpfsol["varstep"] = "lambda"

        else:
            if powerflow.cpfsol["pmc"]:
                if (
                    (
                        powerflow.cpfsol["step"]
                        < (
                            powerflow.setting.options["cpfV2L"]
                            * powerflow.cpfsol["stepmax"]
                        )
                    )
                    and (self.varlambda > self.varvolt)
                    and (not powerflow.cpfsol["v2l"])
                ):
                    powerflow.cpfsol["varstep"] = "lambda"
                    powerflow.setting.options["cpfLambda"] = deepcopy(
                        powerflow.case[1]["corr"]["step"]
                    )
                    powerflow.cpfsol["v2l"] = True
                    powerflow.cpfsol["div"] = 0
                    powerflow.setting.v2lidx = deepcopy(self.case)

                elif not powerflow.cpfsol["v2l"]:
                    powerflow.cpfsol["varstep"] = "volt"

            elif (
                (not powerflow.cpfsol["pmc"])
                and (powerflow.cpfsol["varstep"] == "lambda")
                and (
                    (
                        powerflow.setting.options["cpfLambda"]
                        * (5e-1 ** powerflow.cpfsol["div"])
                    )
                    <= powerflow.setting.options["icmn"]
                )
            ):
                powerflow.cpfsol["pmc"] = True
                powerflow.setting.pmcidx = deepcopy(self.case)
                powerflow.cpfsol["varstep"] = "volt"
                powerflow.cpfsol["div"] = 0

    def heuristics(
        self,
        powerflow,
    ):
        """heurísticas para determinação do funcionamento do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        ## Afundamento de tensão não desejado (em i+1) e retorno ao valor esperado (em i+2) -> correção: voltar duas casas
        # Condição de caso para sistema != ieee24 (pq nesse sistema há aumento de magnitude de tensão na barra 17 PQ)
        if (
            (powerflow.setting.name != "ieee24")
            and (powerflow.setting.name != "ieee118")
            and (powerflow.setting.name != "ieee118-collapse")
            and (self.case == 1)
            and (not powerflow.cpfsol["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.sol["voltage"] - powerflow.case[0]["voltage"]
                    <= powerflow.setting.options["vvar"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                self.case -= 1
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "div",
                    "beta",
                    "step",
                    "stepsch",
                    "vsch",
                    "varstep",
                    "potencia_ativa",
                    "demanda_ativa",
                    "demanda_reativa",
                    "stepmax",
                }
                powerflow.cpfsol = {
                    key: deepcopy(powerflow.case[self.case][key])
                    for key in powerflow.cpfsol.keys() & cpfkeys
                }
                powerflow.cpfsol["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol["voltage"] = deepcopy(
                    powerflow.case[self.case]["voltage"]
                )
                powerflow.sol["theta"] = deepcopy(powerflow.case[self.case]["theta"])

        elif (
            (powerflow.setting.name != "ieee24")
            and (powerflow.setting.name != "ieee118")
            and (powerflow.setting.name != "ieee118-collapse")
            and (self.case == 2)
            and (not powerflow.cpfsol["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.sol["voltage"]
                    - powerflow.case[self.case - 1]["corr"]["voltage"]
                    <= powerflow.setting.options["vvar"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlpop(powerflow, pop=2)

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "div",
                    "beta",
                    "step",
                    "stepsch",
                    "vsch",
                    "varstep",
                    "potencia_ativa",
                    "demanda_ativa",
                    "demanda_reativa",
                    "stepmax",
                }
                powerflow.cpfsol = {
                    key: deepcopy(powerflow.case[self.case][key])
                    for key in powerflow.cpfsol.keys() & cpfkeys
                }
                powerflow.cpfsol["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol["voltage"] = deepcopy(
                    powerflow.case[self.case]["voltage"]
                )
                powerflow.sol["theta"] = deepcopy(powerflow.case[self.case]["theta"])

        elif (
            (powerflow.setting.name != "ieee24")
            and (powerflow.setting.name != "ieee118")
            and (powerflow.setting.name != "ieee118-collapse")
            and (self.case > 2)
            and (not powerflow.cpfsol["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.sol["voltage"]
                    - powerflow.case[self.case - 1]["corr"]["voltage"]
                    <= powerflow.setting.options["vvar"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlpop(powerflow, pop=2)

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "div",
                    "beta",
                    "step",
                    "stepsch",
                    "vsch",
                    "varstep",
                    "potencia_ativa",
                    "demanda_ativa",
                    "demanda_reativa",
                    "stepmax",
                }
                powerflow.cpfsol = {
                    key: deepcopy(powerflow.case[self.case]["corr"][key])
                    for key in powerflow.cpfsol.keys() & cpfkeys
                }
                powerflow.cpfsol["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol["voltage"] = deepcopy(
                    powerflow.case[self.case]["corr"]["voltage"]
                )
                powerflow.sol["theta"] = deepcopy(
                    powerflow.case[self.case]["corr"]["theta"]
                )

        if self.case > 0:
            # Condição de divergência na etapa de previsão por excesso de iterações
            if (
                (
                    powerflow.case[self.case]["prev"]["iter"]
                    > powerflow.setting.options["itermx"]
                )
                and (not self.active_heuristic)
                and (powerflow.setting.name != "ieee118")
                and (powerflow.setting.name != "ieee118-collapse")
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                self.case -= 1
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "div",
                    "beta",
                    "step",
                    "stepsch",
                    "vsch",
                    "varstep",
                    "potencia_ativa",
                    "demanda_ativa",
                    "demanda_reativa",
                    "stepmax",
                }
                powerflow.cpfsol = {
                    key: deepcopy(powerflow.case[self.case]["corr"][key])
                    for key in powerflow.cpfsol.keys() & cpfkeys
                }
                powerflow.cpfsol["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.sol["voltage"] = deepcopy(
                    powerflow.case[self.case]["corr"]["voltage"]
                )
                powerflow.sol["theta"] = deepcopy(
                    powerflow.case[self.case]["corr"]["theta"]
                )

            # Condição de atingimento do PMC para varstep volt pequeno
            if (
                (not powerflow.cpfsol["pmc"])
                and (powerflow.cpfsol["varstep"] == "volt")
                and (
                    powerflow.setting.options["cpfVolt"]
                    * (5e-1 ** powerflow.cpfsol["div"])
                    < powerflow.setting.options["icmn"]
                )
                and (not self.active_heuristic)
            ):
                self.active_heuristic = True

                # Reconfiguração de caso
                self.case -= 1
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlpop(
                    powerflow,
                )

                # Reconfiguração da variável de passo
                powerflow.cpfsol["div"] = 0

                # Condição de máximo carregamento atingida
                powerflow.cpfsol["pmc"] = True
                powerflow.case[self.case]["corr"]["pmc"] = True
                powerflow.setting.pmcidx = deepcopy(self.case)

            # Condição de valor de tensão da barra slack variar
            if (
                (
                    powerflow.sol["voltage"][powerflow.setting.slackidx]
                    < (
                        powerflow.setting.dbarraDF.loc[powerflow.setting.slackidx, "tensao"]
                        * 1e-3
                    )
                    - 1e-8
                )
                or (
                    powerflow.sol["voltage"][powerflow.setting.slackidx]
                    > (
                        powerflow.setting.dbarraDF.loc[powerflow.setting.slackidx, "tensao"]
                        * 1e-3
                    )
                    + 1e-8
                )
            ) and (not self.active_heuristic):

                # variação de tensão da barra slack
                if (powerflow.setting.name == "ieee118") and (
                    sum(powerflow.setting.dbarraDF.demanda_ativa.to_numpy()) > 5400
                ):
                    pass

                else:
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                    self.case -= 1
                    Control(
                        powerflow,
                        powerflow.setting,
                    ).controlpop(
                        powerflow,
                    )

                    # Reconfiguração das variáveis de passo
                    cpfkeys = {
                        "system",
                        "pmc",
                        "v2l",
                        "div",
                        "beta",
                        "step",
                        "stepsch",
                        "vsch",
                        "varstep",
                        "potencia_ativa",
                        "demanda_ativa",
                        "demanda_reativa",
                        "stepmax",
                    }
                    powerflow.cpfsol = {
                        key: deepcopy(powerflow.case[self.case]["corr"][key])
                        for key in powerflow.cpfsol.keys() & cpfkeys
                    }
                    powerflow.cpfsol["div"] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.sol["voltage"] = deepcopy(
                        powerflow.case[self.case]["corr"]["voltage"]
                    )
                    powerflow.sol["theta"] = deepcopy(
                        powerflow.case[self.case]["corr"]["theta"]
                    )

            # Condição de Heurísticas para controle
            if powerflow.setting.controlcount > 0:
                Control(
                    powerflow,
                    powerflow.setting,
                ).controlheuristics(
                    powerflow,
                )

                # Condição de violação de limite máximo de geração de potência reativa
                if (powerflow.setting.controlheur) and (not self.active_heuristic):
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.cpfsol["div"]) + 1
                    self.case -= 1
                    Control(
                        powerflow,
                        powerflow.setting,
                    ).controlpop(
                        powerflow,
                    )

                    # Reconfiguração das variáveis de passo
                    cpfkeys = {
                        "system",
                        "pmc",
                        "v2l",
                        "div",
                        "beta",
                        "step",
                        "stepsch",
                        "vsch",
                        "varstep",
                        "potencia_ativa",
                        "demanda_ativa",
                        "demanda_reativa",
                        "stepmax",
                    }
                    powerflow.cpfsol = {
                        key: deepcopy(powerflow.case[self.case]["corr"][key])
                        for key in powerflow.cpfsol.keys() & cpfkeys
                    }
                    powerflow.cpfsol["div"] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.sol["voltage"] = deepcopy(
                        powerflow.case[self.case]["corr"]["voltage"]
                    )
                    powerflow.sol["theta"] = deepcopy(
                        powerflow.case[self.case]["corr"]["theta"]
                    )

                # Condição de atingimento de ponto de bifurcação
                if (powerflow.setting.bifurcation) and (not powerflow.cpfsol["pmc"]):
                    powerflow.cpfsol["pmc"] = True
                    powerflow.setting.pmcidx = deepcopy(self.case)
                    powerflow.cpfsol["varstep"] = "volt"
                    powerflow.cpfsol["div"] = 0
