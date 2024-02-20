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
    dot,
    max,
    sum,
    zeros,
)
from numpy.linalg import det, eig, inv
from scipy.sparse import hstack, vstack
from scipy.sparse.linalg import spsolve

from calc import pcalc, qcalc
from ctrl import (
    controlcpf,
    controlcorrsol,
    controlsch,
    controlupdt,
    controlpop,
    controldelta,
    controlres,
    controlheuristics,
)
from jacobian import jacobi
from loading import loading


def cpf(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
    powerflow.cpfsolution = {
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
        "eigencalculation": True,
    }

    # Variável para armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
    controlcpf(
        powerflow,
    )

    # Variável para armazenamento da solução do fluxo de potência continuado
    powerflow.point = dict()

    # Variável para armazenamento de solução por casos do continuado (previsão e correção)
    case = 0

    # Armazenamento da solução inicial
    powerflow.point[case] = {
        **deepcopy(powerflow.solution),
        **deepcopy(powerflow.cpfsolution),
    }

    # Armazenamento de determinante e autovalores
    eigensens(
        case,
        powerflow,
    )

    # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
    powerflow.mask = append(powerflow.mask, False)

    # Dimensão da matriz Jacobiana
    powerflow.jdim = powerflow.jacob.shape[0]

    # Barra com maior variação de magnitude de tensão - CASO BASE
    powerflow.nodevarvolt = argmax(
        abs(powerflow.solution["voltage"] - powerflow.dbarraDF["tensao"] * 1e-3)
    )

    # Loop de Previsão - Correção
    cpfloop(
        case,
        powerflow,
    )

    del powerflow.point[len(powerflow.point) - 1]

    # Geração e armazenamento de gráficos de perfil de tensão e autovalores
    loading(
        powerflow,
    )

    # Smooth storage
    if "QLIMs" in powerflow.control:
        for _, v in powerflow.qlimkeys.items():
            v.popitem()
        from smooth import qlimstorage

        qlimstorage(
            powerflow,
        )
    if "SVCs" in powerflow.control:
        for _, v in powerflow.svckeys.items():
            v.popitem()
        from smooth import svcstorage

        svcstorage(
            powerflow,
        )


def cpfloop(
    case,
    powerflow,
):
    """loop do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição de parada do fluxo de potência continuado -> Estável & Instável
    while (
        powerflow.options["LMBD"]
        * ((1 / powerflow.options["FDIV"]) ** powerflow.cpfsolution["div"])
        * 1e2
        >= powerflow.options["ICMN"]
        and powerflow.cpfsolution["div"] <= powerflow.options["DMAX"]
        and case <= powerflow.options["ICIT"]
    ):
        # self.active_heuristic = False

        # Incremento de Caso
        case += 1

        # Variável de armazenamento
        powerflow.point[case] = dict()

        # Previsão
        prediction(
            case,
            powerflow,
        )

        # Correção
        case = correction(
            case,
            powerflow,
        )

        if (powerflow.solution["convergence"] == "SISTEMA CONVERGENTE") and (case > 0):
            print("Aumento Sistema (%): ", powerflow.cpfsolution["step"] * 1e2)
            if powerflow.cpfsolution["varstep"] == "volt":
                print(
                    "Passo (%): ",
                    powerflow.point[case]["c"]["varstep"],
                    "  ",
                    powerflow.options["ICMV"]
                    * ((1 / powerflow.options["FDIV"]) ** powerflow.cpfsolution["div"])
                    * 1e2,
                )
            else:
                print(
                    "Passo (%): ",
                    powerflow.point[case]["c"]["varstep"],
                    "  ",
                    powerflow.options["LMBD"]
                    * ((1 / powerflow.options["FDIV"]) ** powerflow.cpfsolution["div"])
                    * 1e2,
                )
            print("\n")

        if case > 110:
            print()

        # Break Curva de Carregamento - Parte Estável
        if (not powerflow.options["FULL"]) and (powerflow.cpfsolution["pmc"]):
            break


def prediction(
    case,
    powerflow,
):
    """etapa de previsão do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.solution["iter"] = 0

    # Incremento do Nível de Carregamento e Geração
    increment(
        powerflow,
    )

    # Variáveis Especificadas
    scheduled(
        powerflow,
    )

    # Resíduos
    residue(
        case,
        powerflow,
        stage="p",
    )

    # Atualização da Matriz Jacobiana
    jacobi(
        powerflow,
    )

    # Expansão Jacobiana
    exjac(
        powerflow,
    )

    # Variáveis de estado
    powerflow.statevar = spsolve(powerflow.jacob, powerflow.deltaPQY, use_umfpack=True)

    # Atualização das Variáveis de estado
    update_statevar(
        case,
        powerflow,
        stage="p",
    )

    # Armazenamento de Solução
    storage(
        case,
        powerflow,
        stage="p",
    )


def correction(
    case,
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
        "voltage": deepcopy(powerflow.point[case]["p"]["voltage"]),
        "theta": deepcopy(powerflow.point[case]["p"]["theta"]),
        "active": deepcopy(powerflow.point[case]["p"]["active"]),
        "reactive": deepcopy(powerflow.point[case]["p"]["reactive"]),
        "freq": deepcopy(powerflow.point[case]["p"]["freq"]),
        "freqiter": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": array([]),
        "busQ": array([]),
        "convY": array([]),
        "busY": array([]),
        "active_flow_F2": zeros(powerflow.nlin),
        "reactive_flow_F2": zeros(powerflow.nlin),
        "active_flow_2F": zeros(powerflow.nlin),
        "reactive_flow_2F": zeros(powerflow.nlin),
    }

    # Adição de variáveis de controle na variável de armazenamento de solução
    controlcorrsol(
        case,
        powerflow,
    )

    # Incremento do Nível de Carregamento e Geração
    increment(
        powerflow,
    )

    # Variáveis Especificadas
    scheduled(
        powerflow,
    )

    # Resíduos
    residue(
        case,
        powerflow,
        stage="c",
    )

    while (
        (max(abs(powerflow.deltaP)) >= powerflow.options["TEPA"])
        or (max(abs(powerflow.deltaQ)) >= powerflow.options["TEPR"])
        or controldelta(
            powerflow,
        )
    ):
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Atualização da Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Expansão Jacobiana
        exjac(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update_statevar(
            case,
            powerflow,
            stage="c",
        )

        # Condição de variável de passo
        if powerflow.cpfsolution["varstep"] == "volt":
            # Incremento do Nível de Carregamento e Geração
            increment(
                powerflow,
            )

            # Variáveis Especificadas
            scheduled(
                powerflow,
            )

        # Atualização dos resíduos
        residue(
            case,
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
        convergence(
            powerflow,
        )

        # Atualização da Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Expansão Jacobiana
        exjac(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update_statevar(
            case,
            powerflow,
            stage="c",
        )

        # Atualização dos resíduos
        residue(
            case,
            powerflow,
            stage="c",
        )

        # Armazenamento de Solução
        storage(
            case,
            powerflow,
            stage="c",
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"

        # Avaliação
        evaluate(
            case,
            powerflow,
        )

    # Reconfiguração dos Dados de Solução em Caso de Divergência
    elif ((powerflow.solution["iter"] >= powerflow.options["ACIT"])) and (case == 1):
        # self.active_heuristic = True
        powerflow.solution["convergence"] = "SISTEMA DIVERGENTE"

        # Reconfiguração do caso
        case -= 1
        controlpop(
            powerflow,
        )

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        powerflow.solution["voltage"] = deepcopy(powerflow.point[case]["c"]["voltage"])
        powerflow.solution["theta"] = deepcopy(powerflow.point[case]["c"]["theta"])

        # Reconfiguração da variável de passo
        powerflow.cpfsolution["div"] += 1

        # Reconfiguração do valor da variável de passo
        powerflow.cpfsolution["step"] = deepcopy(powerflow.point[case]["c"]["step"])
        powerflow.cpfsolution["stepsch"] = deepcopy(
            powerflow.point[case]["c"]["stepsch"]
        )
        powerflow.cpfsolution["vsch"] = deepcopy(powerflow.point[case]["c"]["vsch"])

    # Reconfiguração dos Dados de Solução em Caso de Divergência
    elif ((powerflow.solution["iter"] >= powerflow.options["ACIT"])) and (case > 1):
        # self.active_heuristic = True
        powerflow.solution["convergence"] = "SISTEMA DIVERGENTE"

        # Reconfiguração do caso
        case -= 1
        controlpop(
            powerflow,
        )

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        powerflow.solution["voltage"] = deepcopy(powerflow.point[case]["c"]["voltage"])
        powerflow.solution["theta"] = deepcopy(powerflow.point[case]["c"]["theta"])

        # Reconfiguração da variável de passo
        powerflow.cpfsolution["div"] += 1

        # Reconfiguração do valor da variável de passo
        powerflow.cpfsolution["step"] = deepcopy(powerflow.point[case]["c"]["step"])
        powerflow.cpfsolution["stepsch"] = deepcopy(
            powerflow.point[case]["c"]["stepsch"]
        )
        powerflow.cpfsolution["vsch"] = deepcopy(powerflow.point[case]["c"]["vsch"])
    return case


def increment(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy())

    # Incremento de carga
    for idxinc, valueinc in powerflow.dincDF.iterrows():
        # Incremento de carregamento específico por AREA
        if valueinc["tipo_incremento_1"] == "AREA":
            for idxbar, valuebar in powerflow.dbarraDF.iterrows():
                if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                    # Incremento de Carregamento
                    powerflow.dbarraDF.at[
                        idxbar, "demanda_ativa"
                    ] = powerflow.cpfsolution["demanda_ativa"][idxbar] * (
                        1 + powerflow.cpfsolution["stepsch"]
                    )
                    powerflow.dbarraDF.at[
                        idxbar, "demanda_reativa"
                    ] = powerflow.cpfsolution["demanda_reativa"][idxbar] * (
                        1 + powerflow.cpfsolution["stepsch"]
                    )

        # Incremento de carregamento específico por BARRA
        elif valueinc["tipo_incremento_1"] == "BARR":
            # Reconfiguração da variável de índice
            idxinc = valueinc["identificacao_incremento_1"] - 1
            powerflow.dbarraDF.at[idxinc, "demanda_ativa"] = powerflow.cpfsolution[
                "demanda_ativa"
            ][idxinc] * (1 + powerflow.cpfsolution["stepsch"])
            powerflow.dbarraDF.at[idxinc, "demanda_reativa"] = powerflow.cpfsolution[
                "demanda_reativa"
            ][idxinc] * (1 + powerflow.cpfsolution["stepsch"])

    deltaincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - preincrement

    # Incremento de geração
    if powerflow.codes["DGER"]:
        for _, valueger in powerflow.dgeraDF.iterrows():
            idx = valueger["numero"] - 1
            powerflow.dbarraDF.at[idx, "potencia_ativa"] = powerflow.dbarraDF[
                "potencia_ativa"
            ][idx] + (deltaincrement * valueger["fator_participacao"])

        powerflow.cpfsolution["potencia_ativa"] = deepcopy(
            powerflow.dbarraDF["potencia_ativa"]
        )

    # Condição de atingimento do máximo incremento do nível de carregamento delimitado
    if (
        powerflow.cpfsolution["stepsch"]
        == powerflow.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
    ):
        powerflow.cpfsolution["pmc"] = True


def scheduled(
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
        controlsch(
            powerflow,
        )


def residue(
    case,
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
            powerflow.deltaP[idx] -= pcalc(
                powerflow,
                idx,
            )

        # Tipo PQ - Resíduo Potência Reativa
        if (
            ("QLIM" in powerflow.control)
            or ("QLIMs" in powerflow.control)
            or (value["tipo"] == 0)
        ):
            powerflow.deltaQ[idx] += powerflow.qsch[idx]
            powerflow.deltaQ[idx] -= qcalc(
                powerflow,
                idx,
            )

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    concatresidue(
        powerflow,
    )

    # Resíduos de variáveis de estado de controle
    if powerflow.controlcount > 0:
        controlres(
            powerflow,
            case,
        )
        concatresidue(
            powerflow,
        )
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)

    # Resíduo de Fluxo de Potência Continuado
    # Condição de previsão
    if stage == "p":
        powerflow.deltaPQY = zeros(powerflow.deltaPQY.shape[0] + 1)
        # Condição de variável de passo
        if powerflow.cpfsolution["varstep"] == "lambda":
            if not powerflow.cpfsolution["pmc"]:
                powerflow.deltaPQY[-1] = powerflow.options["LMBD"] * (
                    5e-1 ** powerflow.cpfsolution["div"]
                )

            elif powerflow.cpfsolution["pmc"]:
                powerflow.deltaPQY[-1] = (
                    -1
                    * powerflow.options["LMBD"]
                    * (5e-1 ** powerflow.cpfsolution["div"])
                )

        elif powerflow.cpfsolution["varstep"] == "volt":
            powerflow.deltaPQY[-1] = (
                -1 * powerflow.options["ICMV"] * (5e-1 ** powerflow.cpfsolution["div"])
            )

    # Condição de correção
    elif stage == "c":
        # Condição de variável de passo
        if powerflow.cpfsolution["varstep"] == "lambda":
            powerflow.deltaY = array(
                [powerflow.cpfsolution["stepsch"] - powerflow.cpfsolution["step"]]
            )

        elif powerflow.cpfsolution["varstep"] == "volt":
            powerflow.deltaY = array(
                [
                    powerflow.cpfsolution["vsch"]
                    - powerflow.solution["voltage"][powerflow.nodevarvolt]
                ]
            )

        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)


def concatresidue(
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
    powerflow,
):
    """expansão da matriz jacobiana para o método continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Arrays adicionais
    rowarray = zeros([1, powerflow.jdim])
    colarray = zeros([powerflow.jdim, 1])
    stepvar = zeros(1)

    # Condição de variável de passo
    if powerflow.cpfsolution["varstep"] == "lambda":
        stepvar[0] = 1

    elif powerflow.cpfsolution["varstep"] == "volt":
        rowarray[0, (powerflow.nbus + powerflow.nodevarvolt)] = 1

    # Demanda
    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 2:
            colarray[idx, 0] = (
                powerflow.cpfsolution["demanda_ativa"][idx]
                - powerflow.cpfsolution["potencia_ativa"][idx]
            )
            if value["tipo"] == 0:
                colarray[(idx + powerflow.nbus), 0] = powerflow.cpfsolution[
                    "demanda_reativa"
                ][idx]

    colarray /= powerflow.options["BASE"]

    # Expansão Jacobiana Continuada
    powerflow.jacob = hstack([powerflow.jacob, colarray], format="csc")
    powerflow.jacob = vstack(
        [powerflow.jacob, concatenate((rowarray, [stepvar]), axis=1)],
        format="csc",
    )


def convergence(
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
    case,
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
        if powerflow.cpfsolution["varstep"] == "lambda":
            powerflow.solution["voltage"] += powerflow.statevar[
                (powerflow.nbus) : (2 * powerflow.nbus)
            ]
            powerflow.cpfsolution["stepsch"] += powerflow.statevar[-1]

        elif powerflow.cpfsolution["varstep"] == "volt":
            powerflow.cpfsolution["step"] += powerflow.statevar[-1]
            powerflow.cpfsolution["stepsch"] += powerflow.statevar[-1]
            powerflow.cpfsolution["vsch"] = (
                powerflow.solution["voltage"][powerflow.nodevarvolt]
                + powerflow.statevar[(powerflow.nbus + powerflow.nodevarvolt)]
            )

        # Verificação do Ponto de Máximo Carregamento
        if case > 0:
            if case == 1:
                powerflow.cpfsolution["stepmax"] = deepcopy(
                    powerflow.cpfsolution["stepsch"]
                )

            elif case != 1:
                if (
                    powerflow.cpfsolution["stepsch"]
                    > powerflow.point[case - 1]["c"]["step"]
                ) and (not powerflow.cpfsolution["pmc"]):
                    powerflow.cpfsolution["stepmax"] = deepcopy(
                        powerflow.cpfsolution["stepsch"]
                    )

                elif (
                    powerflow.cpfsolution["stepsch"]
                    < powerflow.point[case - 1]["c"]["step"]
                ) and (not powerflow.cpfsolution["pmc"]):
                    powerflow.cpfsolution["pmc"] = True
                    powerflow.pmcidx = deepcopy(case)

    # Condição de correção
    elif stage == "c":
        powerflow.solution["voltage"] += powerflow.statevar[
            (powerflow.nbus) : (2 * powerflow.nbus)
        ]
        powerflow.cpfsolution["step"] += powerflow.statevar[-1]

        if powerflow.cpfsolution["varstep"] == "volt":
            powerflow.cpfsolution["stepsch"] += powerflow.statevar[-1]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )


def storage(
    case,
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
    powerflow.point[case][stage] = {
        **deepcopy(powerflow.solution),
        **deepcopy(powerflow.cpfsolution),
    }

    if "SVCs" in powerflow.control:
        powerflow.point[case][stage]["svc_reactive_generation"] = deepcopy(
            powerflow.solution["svc_reactive_generation"]
        )

    # Armazenamento do índice do barramento com maior variação de magnitude de tensão
    powerflow.point[case]["nodevarvolt"] = deepcopy(powerflow.nodevarvolt)

    # Análise de sensibilidade e armazenamento
    eigensens(
        case,
        powerflow,
        stage=stage,
    )


def eigensens(
    case,
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
    jacob = deepcopy(powerflow.jacob.A)

    if case > 0:
        jacob = jacob[:-1, :-1]

    # # Submatrizes Jacobianas
    pt = deepcopy(jacob[: (2 * powerflow.nbus), :][:, : (2 * powerflow.nbus)])
    pv = deepcopy(
        jacob[: (2 * powerflow.nbus), :][
            :,
            (2 * powerflow.nbus) : (2 * powerflow.nbus + powerflow.totaldevicescontrol),
        ]
    )
    qt = deepcopy(
        jacob[
            (2 * powerflow.nbus) : (2 * powerflow.nbus + powerflow.totaldevicescontrol),
            :,
        ][:, : (2 * powerflow.nbus)]
    )
    qv = deepcopy(
        jacob[
            (2 * powerflow.nbus) : (2 * powerflow.nbus + powerflow.totaldevicescontrol),
            :,
        ][
            :,
            (2 * powerflow.nbus) : (2 * powerflow.nbus + powerflow.totaldevicescontrol),
        ]
    )

    try:
        # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
        rightvalues, rightvector = eig(
            powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask]
        )
        powerflow.PF = zeros(
            [
                powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask].shape[0],
                powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask].shape[1],
            ]
        )

        # Jacobiana reduzida - sensibilidade QV
        powerflow.jacobQV = qv - dot(dot(qt, inv(pt)), pv)
        rightvaluesQV, rightvectorQV = eig(powerflow.jacobQV)
        rightvaluesQV = absolute(rightvaluesQV)
        powerflow.PFQV = zeros([powerflow.jacobQV.shape[0], powerflow.jacobQV.shape[1]])
        for row in range(0, powerflow.jacobQV.shape[0]):
            for col in range(0, powerflow.jacobQV.shape[1]):
                powerflow.PFQV[col, row] = (
                    rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                )

        # Condição
        if stage == None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.point[case]["jacobian"] = powerflow.jacob.A[powerflow.mask, :][
                :, powerflow.mask
            ]

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.point[case]["determinant"] = det(
                powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask]
            )

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            powerflow.point[case]["eigenvalues"] = rightvalues
            powerflow.point[case]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.point[case]["participation_factor"] = powerflow.PF

            # Armazenamento da matriz de sensibilidade QV
            powerflow.point[case]["jacobian-QV"] = powerflow.jacobQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.point[case]["determinant-QV"] = det(powerflow.jacobQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            powerflow.point[case]["eigenvalues-QV"] = rightvaluesQV
            powerflow.point[case]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.point[case]["participationfactor-QV"] = powerflow.PFQV

        elif stage != None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.point[case][stage]["jacobian"] = powerflow.jacob.A

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.point[case][stage]["determinant"] = det(
                powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask]
            )

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            powerflow.point[case][stage]["eigenvalues"] = rightvalues
            powerflow.point[case][stage]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.point[case][stage]["participationfactor"] = powerflow.PF

            # Armazenamento da matriz de sensibilidade QV
            powerflow.point[case][stage]["jacobian-QV"] = powerflow.jacobQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.point[case][stage]["determinant-QV"] = det(powerflow.jacobQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            powerflow.point[case][stage]["eigenvalues-QV"] = rightvaluesQV
            powerflow.point[case][stage]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.point[case][stage]["participationfactor-QV"] = powerflow.PFQV

    # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
    # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
    except:
        # self.active_heuristic = True

        # Reconfiguração do caso
        auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
        case -= 1
        controlpop(
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
        powerflow.cpfsolution = {
            key: deepcopy(powerflow.point[case]["c"][key])
            for key in powerflow.cpfsolution.keys() & cpfkeys
        }
        powerflow.cpfsolution["div"] = auxdiv

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        powerflow.solution["voltage"] = deepcopy(powerflow.point[case]["c"]["voltage"])
        powerflow.solution["theta"] = deepcopy(powerflow.point[case]["c"]["theta"])

        # # Loop
        # pass


def evaluate(
    case,
    powerflow,
):
    """avaliação para determinação do passo do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição Inicial
    if case == 1:
        # Lambda
        varlambda = abs(
            (powerflow.cpfsolution["step"] - 0) / (powerflow.cpfsolution["step"])
        )

        # Voltage
        powerflow.nodevarvolt = argmax(
            abs(powerflow.solution["voltage"] - powerflow.point[0]["voltage"])
        )
        varvolt = abs(
            (
                powerflow.solution["voltage"][powerflow.nodevarvolt]
                - powerflow.point[0]["voltage"][powerflow.nodevarvolt]
            )
            / powerflow.solution["voltage"][powerflow.nodevarvolt]
        )

    # Condição Durante
    elif case != 1:
        # Lambda
        varlambda = abs(
            (
                powerflow.point[case]["c"]["step"]
                - powerflow.point[case - 1]["c"]["step"]
            )
            / powerflow.point[case]["c"]["step"]
        )

        # Voltage
        powerflow.nodevarvolt = argmax(
            abs(
                powerflow.solution["voltage"]
                - powerflow.point[case - 1]["c"]["voltage"]
            )
        )
        varvolt = abs(
            (
                powerflow.point[case]["c"]["voltage"][powerflow.nodevarvolt]
                - powerflow.point[case - 1]["c"]["voltage"][powerflow.nodevarvolt]
            )
            / powerflow.point[case]["c"]["voltage"][powerflow.nodevarvolt]
        )

    # Avaliação
    if (varlambda > varvolt) and (powerflow.cpfsolution["varstep"] == "lambda"):
        powerflow.cpfsolution["varstep"] = "lambda"

    else:
        if powerflow.cpfsolution["pmc"]:
            if (
                (
                    powerflow.cpfsolution["step"]
                    < (powerflow.options["cpfV2L"] * powerflow.cpfsolution["stepmax"])
                )
                and (varlambda > varvolt)
                and (not powerflow.cpfsolution["v2l"])
            ):
                powerflow.cpfsolution["varstep"] = "lambda"
                powerflow.options["LMBD"] = deepcopy(powerflow.point[1]["c"]["step"])
                powerflow.cpfsolution["v2l"] = True
                powerflow.cpfsolution["div"] = 0
                powerflow.v2lidx = deepcopy(case)

            elif not powerflow.cpfsolution["v2l"]:
                powerflow.cpfsolution["varstep"] = "volt"

        elif (
            (not powerflow.cpfsolution["pmc"])
            and (powerflow.cpfsolution["varstep"] == "lambda")
            and (
                (
                    powerflow.options["LMBD"]
                    * ((1 / powerflow.options["FDIV"]) ** powerflow.cpfsolution["div"])
                )
                <= powerflow.options["ICMN"]
            )
        ):
            powerflow.cpfsolution["pmc"] = True
            powerflow.pmcidx = deepcopy(case)
            powerflow.cpfsolution["varstep"] = "volt"
            powerflow.cpfsolution["div"] = 0


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
        and (case == 1)
        and (not powerflow.cpfsolution["pmc"])
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
            self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
            case -= 1
            controlpop(
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
            powerflow.cpfsolution = {
                key: deepcopy(powerflow.point[case][key])
                for key in powerflow.cpfsolution.keys() & cpfkeys
            }
            powerflow.cpfsolution["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(powerflow.point[case]["voltage"])
            powerflow.solution["theta"] = deepcopy(powerflow.point[case]["theta"])

    elif (
        (powerflow.name != "ieee24")
        and (powerflow.name != "ieee118")
        and (powerflow.name != "ieee118-collapse")
        and (case == 2)
        and (not powerflow.cpfsolution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                powerflow.solution["voltage"]
                - powerflow.point[case - 1]["c"]["voltage"]
                <= powerflow.options["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
            case -= 2
            controlpop(powerflow, pop=2)

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
            powerflow.cpfsolution = {
                key: deepcopy(powerflow.point[case][key])
                for key in powerflow.cpfsolution.keys() & cpfkeys
            }
            powerflow.cpfsolution["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(powerflow.point[case]["voltage"])
            powerflow.solution["theta"] = deepcopy(powerflow.point[case]["theta"])

    elif (
        (powerflow.name != "ieee24")
        and (powerflow.name != "ieee118")
        and (powerflow.name != "ieee118-collapse")
        and (case > 2)
        and (not powerflow.cpfsolution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                powerflow.solution["voltage"]
                - powerflow.point[case - 1]["c"]["voltage"]
                <= powerflow.options["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
            case -= 2
            controlpop(powerflow, pop=2)

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
            powerflow.cpfsolution = {
                key: deepcopy(powerflow.point[case]["c"][key])
                for key in powerflow.cpfsolution.keys() & cpfkeys
            }
            powerflow.cpfsolution["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.point[case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(powerflow.point[case]["c"]["theta"])

    if case > 0:
        # Condição de divergência na etapa de previsão por excesso de iterações
        if (
            (powerflow.point[case]["p"]["iter"] > powerflow.options["ACIT"])
            and (not self.active_heuristic)
            and (powerflow.name != "ieee118")
            and (powerflow.name != "ieee118-collapse")
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
            case -= 1
            controlpop(
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
            powerflow.cpfsolution = {
                key: deepcopy(powerflow.point[case]["c"][key])
                for key in powerflow.cpfsolution.keys() & cpfkeys
            }
            powerflow.cpfsolution["div"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.point[case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(powerflow.point[case]["c"]["theta"])

        # Condição de atingimento do PMC para varstep volt pequeno
        if (
            (not powerflow.cpfsolution["pmc"])
            and (powerflow.cpfsolution["varstep"] == "volt")
            and (
                powerflow.options["ICMV"] * (5e-1 ** powerflow.cpfsolution["div"])
                < powerflow.options["ICMN"]
            )
            and (not self.active_heuristic)
        ):
            self.active_heuristic = True

            # Reconfiguração de caso
            case -= 1
            controlpop(
                powerflow,
            )

            # Reconfiguração da variável de passo
            powerflow.cpfsolution["div"] = 0

            # Condição de máximo carregamento atingida
            powerflow.cpfsolution["pmc"] = True
            powerflow.point[case]["c"]["pmc"] = True
            powerflow.pmcidx = deepcopy(case)

        # Condição de valor de tensão da barra slack variar
        if (
            (
                powerflow.solution["voltage"][powerflow.slackidx]
                < (powerflow.dbarraDF.loc[powerflow.slackidx, "tensao"] * 1e-3) - 1e-8
            )
            or (
                powerflow.solution["voltage"][powerflow.slackidx]
                > (powerflow.dbarraDF.loc[powerflow.slackidx, "tensao"] * 1e-3) + 1e-8
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
                self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
                case -= 1
                controlpop(
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
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.point[case]["c"][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[case]["c"]["theta"]
                )

        # Condição de Heurísticas para controle
        if powerflow.controlcount > 0:
            controlheuristics(
                powerflow,
            )

            # Condição de violação de limite máximo de geração de potência reativa
            if (powerflow.controlheur) and (not self.active_heuristic):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.cpfsolution["div"]) + 1
                case -= 1
                controlpop(
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
                powerflow.cpfsolution = {
                    key: deepcopy(powerflow.point[case]["c"][key])
                    for key in powerflow.cpfsolution.keys() & cpfkeys
                }
                powerflow.cpfsolution["div"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.point[case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.point[case]["c"]["theta"]
                )

            # Condição de atingimento de ponto de bifurcação
            if (powerflow.bifurcation) and (not powerflow.cpfsolution["pmc"]):
                powerflow.cpfsolution["pmc"] = True
                powerflow.pmcidx = deepcopy(case)
                powerflow.cpfsolution["varstep"] = "volt"
                powerflow.cpfsolution["div"] = 0
