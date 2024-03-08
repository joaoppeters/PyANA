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
    """classe para cálculo do fluxo de potência não-linear via método newton-raphson"""

    def __init__(
        self,
        powerflow,
        entender,
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
            outro parametro
        """

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

        del powerflow.point[len(powerflow.point) - 1]

        # # Geração e armazenamento de gráficos de perfil de tensão e autovalores
        # Loading(powerflow,)

        # # Smooth
        # if ('QLIMs' in powerflow.control):
        #     for k, v in powerflow.nbusqlimkeys.items():
        #         v.popitem()
        #     Smooth(powerflow,).qlimstorage(powerflow,)
        # if ('SVCs' in powerflow.control):
        #     for k, v in powerflow.nbussvckeys.items():
        #         v.popitem()
        #     Smooth().svcstorage(powerflow,)

    def fastcontinuationpowerflow(
        self,
        powerflow,
        entender,
    ):
        """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

        Parâmetros
            powerflow: self do arquivo powerflow.py
            outro parametro
        """

        ## Inicialização
        # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
        powerflow.solution = {
            "pmc": False,
            "v2l": False,
            "div": 0,
            "beta": deepcopy(powerflow.options["cpfBeta"]),
            "step": 0.0,
            "stepsch": 0.0,
            "vsch": 0.0,
            "stepmax": 0.0,
            "varstep": "lambda",
            "potencia_ativa": deepcopy(powerflow.dbarraDF["potencia_ativa"]),
            "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
        }

        # Variável para armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
        Control(powerflow, powerflow,).controlcpf(
            powerflow,
        )

        # Variável para armazenamento da solução do fluxo de potência continuado
        powerflow.point = dict()

        # Variável para armazenamento de solução por casos do continuado (previsão e correção)
        self.case = 0

        # Armazenamento da solução inicial
        powerflow.point[self.case] = {
            **deepcopy(powerflow.solution),
            **deepcopy(powerflow.solution),
        }

        # # Armazenamento de determinante e autovalores
        # self.eigensens(powerflow,)

        # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
        powerflow.mask = append(powerflow.mask, False)

        # Dimensão da matriz Jacobiana
        powerflow.nbusjdim = powerflow.jacobian.shape[0]

        # Barra com maior variação de magnitude de tensão - CASO BASE
        powerflow.nbusnodevarvolt = argmax(
            abs(powerflow.solution["voltage"] - powerflow.dbarraDF["tensao"] * 1e-3)
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
        while all((powerflow.solution["voltage"] >= 0.0)) and (
            sum(powerflow.dbarraDF["demanda_ativa"])
            >= 0.99 * sum(powerflow.solution["demanda_ativa"])
        ):
            self.active_heuristic = False

            # Incremento de Caso
            self.case += 1

            # Variável de armazenamento
            powerflow.point[self.case] = dict()

            # Previsão
            self.prediction(
                powerflow,
            )

            # Correção
            self.correction(
                powerflow,
            )

            if (powerflow.solution["convergence"] == "SISTEMA CONVERGENTE") and (
                self.case > 0
            ):
                print("Aumento Sistema (%): ", powerflow.solution["step"] * 1e2)
                if powerflow.solution["varstep"] == "volt":
                    print(
                        "Passo (%): ",
                        powerflow.point[self.case]["c"]["varstep"],
                        "  ",
                        powerflow.options["cpfVolt"]
                        * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["div"])
                        * 1e2,
                    )
                else:
                    print(
                        "Passo (%): ",
                        powerflow.point[self.case]["c"]["varstep"],
                        "  ",
                        powerflow.options["LMBD"]
                        * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["div"])
                        * 1e2,
                    )
                print("\n")

            # Break Curva de Carregamento - Parte Estável
            if (not powerflow.options["FULL"]) and (powerflow.solution["pmc"]):
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
        powerflow.solution["iter"] = 0

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
            stage="p",
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
        powerflow.statevar = solve(powerflow.jacobian, powerflow.deltaPQY)

        # Atualização das Variáveis de estado
        self.update_statevar(
            powerflow,
            stage="p",
        )

        # Fluxo em linhas de transmissão
        self.line_flow(
            powerflow,
        )

        # Armazenamento de Solução
        self.storage(
            powerflow,
            stage="p",
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
        powerflow.solution = {
            "iter": 0,
            "voltage": deepcopy(powerflow.point[self.case]["p"]["voltage"]),
            "theta": deepcopy(powerflow.point[self.case]["p"]["theta"]),
            "active": deepcopy(powerflow.point[self.case]["p"]["active"]),
            "reactive": deepcopy(powerflow.point[self.case]["p"]["reactive"]),
            "freq": deepcopy(powerflow.point[self.case]["p"]["freq"]),
            "freqiter": array([]),
            "convP": array([]),
            "busP": array([]),
            "convQ": array([]),
            "busQ": array([]),
            "convY": array([]),
            "busY": array([]),
            "active_flow_F2": zeros(powerflow.nbusnlin),
            "reactive_flow_F2": zeros(powerflow.nbusnlin),
            "active_flow_2F": zeros(powerflow.nbusnlin),
            "reactive_flow_2F": zeros(powerflow.nbusnlin),
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
            stage="c",
        )

        while (
            (max(abs(powerflow.deltaP)) >= powerflow.options["TEPA"])
            or (max(abs(powerflow.deltaQ)) >= powerflow.options["TEPR"])
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
            powerflow.statevar = solve(powerflow.jacobian, powerflow.deltaPQY)

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage="c",
            )

            # Condição de variável de passo
            if powerflow.solution["varstep"] == "volt":
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
                stage="c",
            )

            # Incremento de iteração
            powerflow.solution["iter"] += 1

            # Condição de Divergência por iterações
            if powerflow.solution["iter"] > powerflow.options["ACIT"]:
                powerflow.solution[
                    "convergence"
                ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
                break

        ## Condição
        # Iteração Adicional em Caso de Convergência
        if powerflow.solution["iter"] < powerflow.options["ACIT"]:
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
            powerflow.statevar = solve(powerflow.jacobian, powerflow.deltaPQY)

            # Atualização das Variáveis de estado
            self.update_statevar(
                powerflow,
                stage="c",
            )

            # Atualização dos resíduos
            self.residue(
                powerflow,
                stage="c",
            )

            # Fluxo em linhas de transmissão
            self.line_flow(
                powerflow,
            )

            # Armazenamento de Solução
            self.storage(
                powerflow,
                stage="c",
            )

            # Convergência
            powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"

            # Avaliação
            self.evaluate(
                powerflow,
            )

            # Heurísticas
            self.heuristics(
                powerflow,
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.solution["iter"] >= powerflow.options["ACIT"])) and (
            self.case == 1
        ):
            self.active_heuristic = True
            powerflow.solution["convergence"] = "SISTEMA DIVERGENTE"

            # Reconfiguração do caso
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.point[self.case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.point[self.case]["c"]["theta"]
            )

            # Reconfiguração da variável de passo
            powerflow.solution["div"] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.solution["step"] = deepcopy(
                powerflow.point[self.case]["c"]["step"]
            )
            powerflow.solution["stepsch"] = deepcopy(
                powerflow.point[self.case]["c"]["stepsch"]
            )
            powerflow.solution["vsch"] = deepcopy(
                powerflow.point[self.case]["c"]["vsch"]
            )

        # Reconfiguração dos Dados de Solução em Caso de Divergência
        elif ((powerflow.solution["iter"] >= powerflow.options["ACIT"])) and (
            self.case > 1
        ):
            self.active_heuristic = True
            powerflow.solution["convergence"] = "SISTEMA DIVERGENTE"

            # Reconfiguração do caso
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
                powerflow,
            )

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.point[self.case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.point[self.case]["c"]["theta"]
            )

            # Reconfiguração da variável de passo
            powerflow.solution["div"] += 1

            # Reconfiguração do valor da variável de passo
            powerflow.solution["step"] = deepcopy(
                powerflow.point[self.case]["c"]["step"]
            )
            powerflow.solution["stepsch"] = deepcopy(
                powerflow.point[self.case]["c"]["stepsch"]
            )
            powerflow.solution["vsch"] = deepcopy(
                powerflow.point[self.case]["c"]["vsch"]
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
        self.preincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy())

        # Incremento de carga
        for idxinc, valueinc in powerflow.dincDF.iterrows():
            if valueinc["tipo_incremento_1"] == "AREA":
                for idxbar, valuebar in powerflow.dbarraDF.iterrows():
                    if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                        # Incremento de Carregamento
                        powerflow.dbarraDF.at[
                            idxbar, "demanda_ativa"
                        ] = powerflow.solution["demanda_ativa"][idxbar] * (
                            1 + powerflow.solution["stepsch"]
                        )
                        powerflow.dbarraDF.at[
                            idxbar, "demanda_reativa"
                        ] = powerflow.solution["demanda_reativa"][idxbar] * (
                            1 + powerflow.solution["stepsch"]
                        )

            elif valueinc["tipo_incremento_1"] == "BARR":
                # Reconfiguração da variável de índice
                idxinc = valueinc["identificacao_incremento_1"] - 1

                # Incremento de Carregamento
                powerflow.dbarraDF.at[idxinc, "demanda_ativa"] = powerflow.solution[
                    "demanda_ativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])
                powerflow.dbarraDF.at[idxinc, "demanda_reativa"] = powerflow.solution[
                    "demanda_reativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])

        self.deltaincrement = (
            sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - self.preincrement
        )

        # Incremento de geração
        if powerflow.codes["DGER"]:
            for idxger, valueger in powerflow.dgeraDF.iterrows():
                idx = valueger["numero"] - 1
                powerflow.dbarraDF.at[idx, "potencia_ativa"] = powerflow.dbarraDF[
                    "potencia_ativa"
                ][idx] + (self.deltaincrement * valueger["fator_participacao"])

            powerflow.solution["potencia_ativa"] = deepcopy(
                powerflow.dbarraDF["potencia_ativa"]
            )

        # Condição de atingimento do máximo incremento do nível de carregamento
        if (
            powerflow.solution["stepsch"]
            == powerflow.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
        ):
            powerflow.solution["pmc"] = True

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
        powerflow.pqsch = {
            "potencia_ativa_especificada": zeros(powerflow.nbus),
            "potencia_reativa_especificada": zeros(powerflow.nbus),
        }

        # Loop
        for idx, value in powerflow.dbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.psch[idx] += value["potencia_ativa"]
            powerflow.psch[idx] -= value["demanda_ativa"]

            # Potência reativa especificada
            powerflow.qsch[idx] += value["potencia_reativa"]
            powerflow.qsch[idx] -= value["demanda_reativa"]

        # Tratamento
        powerflow.psch /= powerflow.options["BASE"]
        powerflow.qsch /= powerflow.options["BASE"]

        # Variáveis especificadas de controle ativos
        if powerflow.controlcount > 0:
            Control(powerflow, powerflow).controlsch(
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
        powerflow.deltaP = zeros(powerflow.nbus)
        powerflow.deltaQ = zeros(powerflow.nbus)

        # Resíduo de equação de controle adicional
        powerflow.deltaY = array([])

        # Loop
        for idx, value in powerflow.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if value["tipo"] != 2:
                powerflow.deltaP[idx] += powerflow.psch[idx]
                powerflow.deltaP[idx] -= PQCalc().pcalc(
                    powerflow,
                    idx,
                )

            # Tipo PQ - Resíduo Potência Reativa
            if (
                ("QLIM" in powerflow.control)
                or ("QLIMs" in powerflow.control)
                or (value["tipo"] == 0)
            ):
                powerflow.deltaQ[idx] += powerflow.pqsch[
                    "potencia_reativa_especificada"
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
        if powerflow.controlcount > 0:
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
        if stage == "p":
            powerflow.deltaPQY = zeros(powerflow.deltaPQY.shape[0] + 1)
            # Condição de variável de passo
            if powerflow.solution["varstep"] == "lambda":
                if not powerflow.solution["pmc"]:
                    powerflow.deltaPQY[-1] = powerflow.options["LMBD"] * (
                        5e-1 ** powerflow.solution["div"]
                    )

                elif powerflow.solution["pmc"]:
                    powerflow.deltaPQY[-1] = (
                        -1
                        * powerflow.options["LMBD"]
                        * (5e-1 ** powerflow.solution["div"])
                    )

            elif powerflow.solution["varstep"] == "volt":
                powerflow.deltaPQY[-1] = (
                    -1
                    * powerflow.options["cpfVolt"]
                    * (5e-1 ** powerflow.solution["div"])
                )

        # Condição de correção
        elif stage == "c":
            # Condição de variável de passo
            if powerflow.solution["varstep"] == "lambda":
                powerflow.deltaY = array(
                    [powerflow.solution["stepsch"] - powerflow.solution["step"]]
                )

            elif powerflow.solution["varstep"] == "volt":
                powerflow.deltaY = array(
                    [
                        powerflow.solution["vsch"]
                        - powerflow.solution["voltage"][powerflow.nbusnodevarvolt]
                    ]
                )

            powerflow.deltaPQY = concatenate(
                (powerflow.deltaPQY, powerflow.deltaY), axis=0
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
        powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)

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
        rowarray = zeros([1, powerflow.nbusjdim])
        colarray = zeros([powerflow.nbusjdim, 1])
        stepvar = zeros(1)

        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            stepvar[0] = 1

        elif powerflow.solution["varstep"] == "volt":
            rowarray[0, (powerflow.nbus + powerflow.nbusnodevarvolt)] = 1

        # Demanda
        for idx, value in powerflow.dbarraDF.iterrows():
            if value["tipo"] != 2:
                colarray[idx, 0] = (
                    powerflow.solution["demanda_ativa"][idx]
                    - powerflow.solution["potencia_ativa"][idx]
                )
                if value["tipo"] == 0:
                    colarray[(idx + powerflow.nbus), 0] = powerflow.solution[
                        "demanda_reativa"
                    ][idx]

        colarray /= powerflow.options["BASE"]

        # Expansão Inferior
        powerflow.jacobian = concatenate((powerflow.jacobian, colarray), axis=1)

        # Expansão Lateral
        powerflow.jacobian = concatenate(
            (powerflow.jacobian, concatenate((rowarray, [stepvar]), axis=1)), axis=0
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
        powerflow.solution["freqiter"] = append(
            powerflow.solution["freqiter"],
            powerflow.solution["freq"] * powerflow.options["FBASE"],
        )

        # Trajetória de convergência da potência ativa
        powerflow.solution["convP"] = append(
            powerflow.solution["convP"], max(abs(powerflow.deltaP))
        )
        powerflow.solution["busP"] = append(
            powerflow.solution["busP"], argmax(abs(powerflow.deltaP))
        )

        # Trajetória de convergência da potência reativa
        powerflow.solution["convQ"] = append(
            powerflow.solution["convQ"], max(abs(powerflow.deltaQ))
        )
        powerflow.solution["busQ"] = append(
            powerflow.solution["busQ"], argmax(abs(powerflow.deltaQ))
        )

        # Trajetória de convergência referente a cada equação de controle adicional
        if powerflow.deltaY.size != 0:
            powerflow.solution["convY"] = append(
                powerflow.solution["convY"], max(abs(powerflow.deltaY))
            )
            powerflow.solution["busY"] = append(
                powerflow.solution["busY"], argmax(abs(powerflow.deltaY))
            )

        elif powerflow.deltaY.size == 0:
            powerflow.solution["convY"] = append(powerflow.solution["convY"], 0.0)
            powerflow.solution["busY"] = append(powerflow.solution["busY"], 0.0)

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
        powerflow.solution["theta"] += powerflow.statevar[0 : (powerflow.nbus)]
        # Condição de previsão
        if stage == "p":
            # Condição de variável de passo
            if powerflow.solution["varstep"] == "lambda":
                powerflow.solution["voltage"] += powerflow.statevar[
                    (powerflow.nbus) : (2 * powerflow.nbus)
                ]
                powerflow.solution["stepsch"] += powerflow.statevar[-1]

            elif powerflow.solution["varstep"] == "volt":
                powerflow.solution["step"] += powerflow.statevar[-1]
                powerflow.solution["stepsch"] += powerflow.statevar[-1]
                powerflow.solution["vsch"] = (
                    powerflow.solution["voltage"][powerflow.nbusnodevarvolt]
                    + powerflow.statevar[(powerflow.nbus + powerflow.nbusnodevarvolt)]
                )

            # Verificação do Ponto de Máximo Carregamento
            if self.case > 0:
                if self.case == 1:
                    powerflow.solution["stepmax"] = deepcopy(
                        powerflow.solution["stepsch"]
                    )

                elif self.case != 1:
                    if (
                        powerflow.solution["stepsch"]
                        > powerflow.point[self.case - 1]["c"]["step"]
                    ) and (not powerflow.solution["pmc"]):
                        powerflow.solution["stepmax"] = deepcopy(
                            powerflow.solution["stepsch"]
                        )

                    elif (
                        powerflow.solution["stepsch"]
                        < powerflow.point[self.case - 1]["c"]["step"]
                    ) and (not powerflow.solution["pmc"]):
                        powerflow.solution["pmc"] = True
                        powerflow.nbuspmcidx = deepcopy(self.case)

        # Condição de correção
        elif stage == "c":
            powerflow.solution["voltage"] += powerflow.statevar[
                (powerflow.nbus) : (2 * powerflow.nbus)
            ]
            powerflow.solution["step"] += powerflow.statevar[-1]

            if powerflow.solution["varstep"] == "volt":
                powerflow.solution["stepsch"] += powerflow.statevar[-1]

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.controlcount > 0:
            Control(powerflow, powerflow).controlupdt(
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
        for idx, value in powerflow.dlinhaDF.iterrows():
            k = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["de"]][0]
            m = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["para"]][
                0
            ]
            yline = 1 / ((value["resistencia"] / 100) + 1j * (value["reatancia"] / 100))

            # Verifica presença de transformadores com tap != 1.
            if value["tap"] != 0:
                yline /= value["tap"]

            # Potência ativa k -> m
            powerflow.solution["active_flow_F2"][idx] = yline.real * (
                powerflow.solution["voltage"][k] ** 2
            ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
                yline.real
                * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
                + yline.imag
                * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            )

            # Potência reativa k -> m
            powerflow.solution["reactive_flow_F2"][idx] = -(
                (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
            ) * (powerflow.solution["voltage"][k] ** 2) + powerflow.solution["voltage"][
                k
            ] * powerflow.solution[
                "voltage"
            ][
                m
            ] * (
                yline.imag
                * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
                - yline.real
                * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            )

            # Potência ativa m -> k
            powerflow.solution["active_flow_2F"][idx] = yline.real * (
                powerflow.solution["voltage"][m] ** 2
            ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
                yline.real
                * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
                - yline.imag
                * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            )

            # Potência reativa m -> k
            powerflow.solution["reactive_flow_2F"][idx] = -(
                (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
            ) * (powerflow.solution["voltage"][m] ** 2) + powerflow.solution["voltage"][
                k
            ] * powerflow.solution[
                "voltage"
            ][
                m
            ] * (
                yline.imag
                * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
                + yline.real
                * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            )

        powerflow.solution["active_flow_F2"] *= powerflow.options["BASE"]
        powerflow.solution["active_flow_2F"] *= powerflow.options["BASE"]

        powerflow.solution["reactive_flow_F2"] *= powerflow.options["BASE"]
        powerflow.solution["reactive_flow_2F"] *= powerflow.options["BASE"]

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
        powerflow.point[self.case][stage] = {
            **deepcopy(powerflow.solution),
            **deepcopy(powerflow.solution),
        }

        if "SVCs" in powerflow.control:
            powerflow.point[self.case][stage]["svc_reactive_generation"] = deepcopy(
                powerflow.solution["svc_reactive_generation"]
            )

        # Armazenamento do índice do barramento com maior variação de magnitude de tensão
        powerflow.point[self.case]["nodevarvolt"] = deepcopy(powerflow.nbusnodevarvolt)

        # # Análise de sensibilidade e armazenamento
        # self.eigensens(powerflow, stage=stage,)

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
        self.jacob = deepcopy(powerflow.jacobian)

        if self.case > 0:
            self.jacob = self.jacob[:-1, :-1]

        # # Submatrizes Jacobianas
        self.pt = deepcopy(
            self.jacob[: (2 * powerflow.nbus), :][:, : (2 * powerflow.nbus)]
        )
        self.pv = deepcopy(
            self.jacob[: (2 * powerflow.nbus), :][
                :,
                (2 * powerflow.nbus) : (
                    2 * powerflow.nbus + powerflow.nbustotaldevicescontrol
                ),
            ]
        )
        self.qt = deepcopy(
            self.jacob[
                (2 * powerflow.nbus) : (
                    2 * powerflow.nbus + powerflow.nbustotaldevicescontrol
                ),
                :,
            ][:, : (2 * powerflow.nbus)]
        )
        self.qv = deepcopy(
            self.jacob[
                (2 * powerflow.nbus) : (
                    2 * powerflow.nbus + powerflow.nbustotaldevicescontrol
                ),
                :,
            ][
                :,
                (2 * powerflow.nbus) : (
                    2 * powerflow.nbus + powerflow.nbustotaldevicescontrol
                ),
            ]
        )

        try:
            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            rightvalues, rightvector = eig(
                powerflow.jacobian[powerflow.mask, :][:, powerflow.mask]
            )
            powerflow.jacpfactor = zeros(
                [
                    powerflow.jacobian[powerflow.mask, :][:, powerflow.mask].shape[0],
                    powerflow.jacobian[powerflow.mask, :][:, powerflow.mask].shape[1],
                ]
            )

            # Jacobiana reduzida - sensibilidade QV
            powerflow.jacQV = self.qv - dot(dot(self.qt, inv(self.pt)), self.pv)
            rightvaluesQV, rightvectorQV = eig(powerflow.jacQV)
            rightvaluesQV = absolute(rightvaluesQV)
            powerflow.jacQVpfactor = zeros(
                [powerflow.jacQV.shape[0], powerflow.jacQV.shape[1]]
            )
            for row in range(0, powerflow.jacQV.shape[0]):
                for col in range(0, powerflow.jacQV.shape[1]):
                    powerflow.jacQVpfactor[col, row] = (
                        rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                    )

            # Condição
            if stage == None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.point[self.case]["jacobian"] = powerflow.jacobian[
                    powerflow.mask, :
                ][:, powerflow.mask]

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.point[self.case]["determinant"] = det(
                    powerflow.jacobian[powerflow.mask, :][:, powerflow.mask]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.point[self.case]["eigenvalues"] = rightvalues
                powerflow.point[self.case]["eigenvectors"] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.point[self.case][
                    "participation_factor"
                ] = powerflow.jacpfactor

                # Armazenamento da matriz de sensibilidade QV
                powerflow.point[self.case]["jacobian-QV"] = powerflow.jacQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.point[self.case]["determinant-QV"] = det(powerflow.jacQV)

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.point[self.case]["eigenvalues-QV"] = rightvaluesQV
                powerflow.point[self.case]["eigenvectors-QV"] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.point[self.case][
                    "participationfactor-QV"
                ] = powerflow.jacQVpfactor

            elif stage != None:
                # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
                powerflow.point[self.case][stage]["jacobian"] = powerflow.jacobian

                # Armazenamento do determinante da matriz Jacobiana reduzida
                powerflow.point[self.case][stage]["determinant"] = det(
                    powerflow.jacobian[powerflow.mask, :][:, powerflow.mask]
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
                powerflow.point[self.case][stage]["eigenvalues"] = rightvalues
                powerflow.point[self.case][stage]["eigenvectors"] = rightvector

                # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
                powerflow.point[self.case][stage][
                    "participationfactor"
                ] = powerflow.jacpfactor

                # Armazenamento da matriz de sensibilidade QV
                powerflow.point[self.case][stage]["jacobian-QV"] = powerflow.jacQV

                # Armazenamento do determinante da matriz de sensibilidade QV
                powerflow.point[self.case][stage]["determinant-QV"] = det(
                    powerflow.jacQV
                )

                # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
                powerflow.point[self.case][stage]["eigenvalues-QV"] = rightvaluesQV
                powerflow.point[self.case][stage]["eigenvectors-QV"] = rightvectorQV

                # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
                powerflow.point[self.case][stage][
                    "participationfactor-QV"
                ] = powerflow.jacQVpfactor

        # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
        # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
        except:
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
            self.case -= 1
            Control(powerflow, powerflow,).controlpop(
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
            powerflow.solution = {
                key: deepcopy(powerflow.point[self.case]["c"][key])
                for key in powerflow.solution.keys() & cpfkeys
            }
            powerflow.solution["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.point[self.case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.point[self.case]["c"]["theta"]
            )

            # # Loop
            # pass

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
        if self.case == 1:
            # Lambda
            self.varlambda = abs(
                (powerflow.solution["step"] - 0) / (powerflow.solution["step"])
            )

            # Voltage
            powerflow.nbusnodevarvolt = argmax(
                abs(powerflow.solution["voltage"] - powerflow.point[0]["voltage"])
            )
            self.varvolt = abs(
                (
                    powerflow.solution["voltage"][powerflow.nbusnodevarvolt]
                    - powerflow.point[0]["voltage"][powerflow.nbusnodevarvolt]
                )
                / powerflow.solution["voltage"][powerflow.nbusnodevarvolt]
            )

        # Condição Durante
        elif self.case != 1:
            # Lambda
            self.varlambda = abs(
                (
                    powerflow.point[self.case]["c"]["step"]
                    - powerflow.point[self.case - 1]["c"]["step"]
                )
                / powerflow.point[self.case]["c"]["step"]
            )

            # Voltage
            powerflow.nbusnodevarvolt = argmax(
                abs(
                    powerflow.solution["voltage"]
                    - powerflow.point[self.case - 1]["c"]["voltage"]
                )
            )
            self.varvolt = abs(
                (
                    powerflow.point[self.case]["c"]["voltage"][
                        powerflow.nbusnodevarvolt
                    ]
                    - powerflow.point[self.case - 1]["c"]["voltage"][
                        powerflow.nbusnodevarvolt
                    ]
                )
                / powerflow.point[self.case]["c"]["voltage"][powerflow.nbusnodevarvolt]
            )

        # Avaliação
        if (self.varlambda > self.varvolt) and (
            powerflow.solution["varstep"] == "lambda"
        ):
            powerflow.solution["varstep"] = "lambda"

        else:
            if powerflow.solution["pmc"]:
                if (
                    (
                        powerflow.solution["step"]
                        < (powerflow.options["cpfV2L"] * powerflow.solution["stepmax"])
                    )
                    and (self.varlambda > self.varvolt)
                    and (not powerflow.solution["v2l"])
                ):
                    powerflow.solution["varstep"] = "lambda"
                    powerflow.options["LMBD"] = deepcopy(
                        powerflow.point[1]["c"]["step"]
                    )
                    powerflow.solution["v2l"] = True
                    powerflow.solution["div"] = 0
                    powerflow.nbusv2lidx = deepcopy(self.case)

                elif not powerflow.solution["v2l"]:
                    powerflow.solution["varstep"] = "volt"

            elif (
                (not powerflow.solution["pmc"])
                and (powerflow.solution["varstep"] == "lambda")
                and (
                    (
                        powerflow.options["LMBD"]
                        * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["div"])
                    )
                    <= powerflow.options["ICMN"]
                )
            ):
                powerflow.solution["pmc"] = True
                powerflow.nbuspmcidx = deepcopy(self.case)
                powerflow.solution["varstep"] = "volt"
                powerflow.solution["div"] = 0

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
            (powerflow.name != "ieee24")
            and (powerflow.name != "ieee118")
            and (powerflow.name != "ieee118-collapse")
            and (self.case == 1)
            and (not powerflow.solution["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution["voltage"] - powerflow.point[0]["voltage"]
                    <= powerflow.options["VVAR"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                self.case -= 1
                Control(powerflow, powerflow,).controlpop(
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
                powerflow.solution = {
                    key: deepcopy(powerflow.point[self.case][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[self.case]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[self.case]["theta"]
                )

        elif (
            (powerflow.name != "ieee24")
            and (powerflow.name != "ieee118")
            and (powerflow.name != "ieee118-collapse")
            and (self.case == 2)
            and (not powerflow.solution["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution["voltage"]
                    - powerflow.point[self.case - 1]["c"]["voltage"]
                    <= powerflow.options["VVAR"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow,
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
                powerflow.solution = {
                    key: deepcopy(powerflow.point[self.case][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[self.case]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[self.case]["theta"]
                )

        elif (
            (powerflow.name != "ieee24")
            and (powerflow.name != "ieee118")
            and (powerflow.name != "ieee118-collapse")
            and (self.case > 2)
            and (not powerflow.solution["pmc"])
            and (not self.active_heuristic)
        ):
            if not all(
                (
                    powerflow.solution["voltage"]
                    - powerflow.point[self.case - 1]["c"]["voltage"]
                    <= powerflow.options["VVAR"]
                )
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                self.case -= 2
                Control(
                    powerflow,
                    powerflow,
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
                powerflow.solution = {
                    key: deepcopy(powerflow.point[self.case]["c"][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[self.case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[self.case]["c"]["theta"]
                )

        if self.case > 0:
            # Condição de divergência na etapa de previsão por excesso de iterações
            if (
                (powerflow.point[self.case]["p"]["iter"] > powerflow.options["ACIT"])
                and (not self.active_heuristic)
                and (powerflow.name != "ieee118")
                and (powerflow.name != "ieee118-collapse")
            ):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                self.case -= 1
                Control(powerflow, powerflow,).controlpop(
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
                powerflow.solution = {
                    key: deepcopy(powerflow.point[self.case]["c"][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[self.case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[self.case]["c"]["theta"]
                )

            # Condição de atingimento do PMC para varstep volt pequeno
            if (
                (not powerflow.solution["pmc"])
                and (powerflow.solution["varstep"] == "volt")
                and (
                    powerflow.options["cpfVolt"] * (5e-1 ** powerflow.solution["div"])
                    < powerflow.options["ICMN"]
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
                powerflow.solution["div"] = 0

                # Condição de máximo carregamento atingida
                powerflow.solution["pmc"] = True
                powerflow.point[self.case]["c"]["pmc"] = True
                powerflow.nbuspmcidx = deepcopy(self.case)

            # Condição de valor de tensão da barra slack variar
            if (
                (
                    powerflow.solution["voltage"][powerflow.nbusslackidx]
                    < (powerflow.dbarraDF.loc[powerflow.nbusslackidx, "tensao"] * 1e-3)
                    - 1e-8
                )
                or (
                    powerflow.solution["voltage"][powerflow.nbusslackidx]
                    > (powerflow.dbarraDF.loc[powerflow.nbusslackidx, "tensao"] * 1e-3)
                    + 1e-8
                )
            ) and (not self.active_heuristic):

                # variação de tensão da barra slack
                if (powerflow.name == "ieee118") and (
                    sum(powerflow.dbarraDF.demanda_ativa.to_numpy()) > 5400
                ):
                    pass

                else:
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                    self.case -= 1
                    Control(powerflow, powerflow,).controlpop(
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
                    powerflow.solution = {
                        key: deepcopy(powerflow.point[self.case]["c"][key])
                        for key in powerflow.solution.keys() & cpfkeys
                    }
                    powerflow.solution["div"] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.solution["voltage"] = deepcopy(
                        powerflow.point[self.case]["c"]["voltage"]
                    )
                    powerflow.solution["theta"] = deepcopy(
                        powerflow.point[self.case]["c"]["theta"]
                    )

            # Condição de Heurísticas para controle
            if powerflow.controlcount > 0:
                Control(powerflow, powerflow,).controlheuristics(
                    powerflow,
                )

                # Condição de violação de limite máximo de geração de potência reativa
                if (powerflow.nbuscontrolheur) and (not self.active_heuristic):
                    self.active_heuristic = True

                    # Reconfiguração do caso
                    self.auxdiv = deepcopy(powerflow.solution["div"]) + 1
                    self.case -= 1
                    Control(powerflow, powerflow,).controlpop(
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
                    powerflow.solution = {
                        key: deepcopy(powerflow.point[self.case]["c"][key])
                        for key in powerflow.solution.keys() & cpfkeys
                    }
                    powerflow.solution["div"] = self.auxdiv

                    # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                    powerflow.solution["voltage"] = deepcopy(
                        powerflow.point[self.case]["c"]["voltage"]
                    )
                    powerflow.solution["theta"] = deepcopy(
                        powerflow.point[self.case]["c"]["theta"]
                    )

                # Condição de atingimento de ponto de bifurcação
                if (powerflow.nbusbifurcation) and (not powerflow.solution["pmc"]):
                    powerflow.solution["pmc"] = True
                    powerflow.nbuspmcidx = deepcopy(self.case)
                    powerflow.solution["varstep"] = "volt"
                    powerflow.solution["div"] = 0
