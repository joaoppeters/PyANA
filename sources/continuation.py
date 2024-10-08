# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    abs,
    all,
    append,
    argmax,
    array,
    concatenate,
    sum,
    zeros,
)
from numpy.linalg import lstsq, norm

from convergence import convergence
from ctrl import (
    controlcorrsol,
    controlupdt,
    controlpop,
    controldelta,
    controlheuristics,
)
from eigen import eigensens
from increment import increment
from loading import loading
from matrices import matrices
from residue import residue
from scheduled import scheduled
from update import updtstt, updtpwr


def prediction_correction(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
    powerflow.solution.update(
        {
            "method": "EXIC",
            "demanda_ativa": deepcopy(powerflow.dbarDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(powerflow.dbarDF["demanda_reativa"]),
            "potencia_ativa": deepcopy(powerflow.dbarDF["potencia_ativa"]),
            "potencia_reativa": deepcopy(powerflow.dbarDF["potencia_reativa"]),
            "pmc": False,
            "v2l": False,
            "ndiv": 0,
            "beta": deepcopy(powerflow.options["cpfBeta"]),
            "step": 0.0,
            "stepsch": 0.0,
            "vsch": 0.0,
            "stepmax": 0.0,
            "varstep": "lambda",
            "eigencalculation": False,
            "cvgprint": True,
        }
    )

    # Variável para armazenamento da solução do fluxo de potência continuado
    powerflow.operationpoint = dict()

    # Variável para armazenamento de solução por casos do continuado (previsão e correção)
    case = 0

    # Armazenamento da solução inicial
    powerflow.operationpoint[case] = {
        **deepcopy(powerflow.solution),
    }

    # # Armazenamento de determinante e autovalores
    # eigensens(
    #     powerflow,
    #     case,
    # )

    # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
    powerflow.mask = append(powerflow.mask, False)

    # Barra com maior variação de magnitude de tensão - CASO BASE
    powerflow.nodevarvolt = argmax(
        norm(powerflow.solution["voltage"] - powerflow.dbarDF["tensao"] * 1e-3)
    )

    # Loop de Previsão - Correção
    exicloop(
        powerflow,
        case,
    )

    del powerflow.operationpoint[len(powerflow.operationpoint) - 1]

    # Geração e armazenamento de gráficos de perfil de tensão e autovalores
    loading(
        powerflow,
    )

    # Smooth exicstorage
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


def exicloop(
    powerflow,
    case,
):
    """loop do fluxo de potência continuado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição de parada do fluxo de potência continuado -> Estável & Instável
    while (
        powerflow.options["LMBD"]
        * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["ndiv"])
        * 1e2
        >= powerflow.options["ICMN"]
        and powerflow.solution["ndiv"] <= powerflow.options["DMAX"]
        and case <= powerflow.options["ICIT"]
    ):

        # Incremento de Caso
        case += 1

        # Variável de armazenamento
        powerflow.operationpoint[case] = dict()

        # Previsão
        prediction(
            powerflow,
            case,
        )

        # Correção
        case = correction(
            powerflow,
            case,
        )

        if (
            powerflow.solution["cvgprint"]
            and powerflow.solution["convergence"] == "SISTEMA CONVERGENTE"
        ):
            exiccvgprint(
                powerflow,
                case,
            )

        # Break Curva de Carregamento - Parte Estável
        if (not powerflow.options["FULL"]) and (powerflow.solution["pmc"]):
            break


def prediction(
    powerflow,
    case,
):
    """etapa de previsão do fluxo de potência continuado

    Args
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
        powerflow,
        case,
        stage="p",
    )

    # Atualização da Matriz Jacobiana
    matrices(
        powerflow,
    )

    # Expansão Jacobiana
    exicjacobian(
        powerflow,
    )

    # Variáveis de estado
    powerflow.statevar, residuals, rank, singular = lstsq(
        powerflow.jacobian,
        powerflow.deltaPQY,
        rcond=None,
    )

    # Atualização das Variáveis de estado
    updtstt(
        powerflow,
        case,
        stage="p",
    )

    updtpwr(
        powerflow,
    )

    # Armazenamento de Solução
    exicstorage(
        powerflow,
        case,
        stage="p",
    )


def correction(
    powerflow,
    case,
):
    """etapa de correção do fluxo de potência continuado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution.update(
        {
            "iter": 0,
            "voltage": deepcopy(powerflow.operationpoint[case]["p"]["voltage"]),
            "theta": deepcopy(powerflow.operationpoint[case]["p"]["theta"]),
            "active": deepcopy(powerflow.operationpoint[case]["p"]["active"]),
            "reactive": deepcopy(powerflow.operationpoint[case]["p"]["reactive"]),
            "freq": deepcopy(powerflow.operationpoint[case]["p"]["freq"]),
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
    )

    # Adição de variáveis de controle na variável de armazenamento de solução
    controlcorrsol(
        powerflow,
        case,
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
        powerflow,
        case,
        stage="c",
    )

    while (
        norm(
            powerflow.deltaP[powerflow.maskP],
        )
        > powerflow.options["TEPA"]
        or norm(
            powerflow.deltaQ[powerflow.maskQ],
        )
        > powerflow.options["TEPR"]
        or controldelta(
            powerflow,
        )
    ):
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Atualização da Matriz Jacobiana
        matrices(
            powerflow,
        )

        # Expansão Jacobiana
        exicjacobian(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar, residuals, rank, singular = lstsq(
            powerflow.jacobian,
            powerflow.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            powerflow,
            case,
            stage="c",
        )

        updtpwr(
            powerflow,
        )

        # Condição de variável de passo
        if powerflow.solution["varstep"] == "volt":
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
            powerflow,
            case,
            stage="c",
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição de Divergência por iterações
        if powerflow.solution["iter"] > powerflow.options["ACIT"]:
            powerflow.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

    ## Condição
    # Iteração Adicional em Caso de Convergência
    if powerflow.solution["iter"] < powerflow.options["ACIT"]:
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Atualização da Matriz Jacobiana
        matrices(
            powerflow,
        )

        # Expansão Jacobiana
        exicjacobian(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar, residuals, rank, singular = lstsq(
            powerflow.jacobian,
            powerflow.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            powerflow,
            case,
            stage="c",
        )

        updtpwr(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
            case,
            stage="c",
        )

        # Armazenamento de Solução
        exicstorage(
            powerflow,
            case,
            stage="c",
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"

        # Avaliação
        exicevaluate(
            powerflow,
            case,
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
        powerflow.solution["voltage"] = deepcopy(
            powerflow.operationpoint[case]["c"]["voltage"]
        )
        powerflow.solution["theta"] = deepcopy(
            powerflow.operationpoint[case]["c"]["theta"]
        )

        # Reconfiguração da variável de passo
        powerflow.solution["ndiv"] += 1

        # Reconfiguração do valor da variável de passo
        powerflow.solution["step"] = deepcopy(
            powerflow.operationpoint[case]["c"]["step"]
        )
        powerflow.solution["stepsch"] = deepcopy(
            powerflow.operationpoint[case]["c"]["stepsch"]
        )
        powerflow.solution["vsch"] = deepcopy(
            powerflow.operationpoint[case]["c"]["vsch"]
        )

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
        powerflow.solution["voltage"] = deepcopy(
            powerflow.operationpoint[case]["c"]["voltage"]
        )
        powerflow.solution["theta"] = deepcopy(
            powerflow.operationpoint[case]["c"]["theta"]
        )

        # Reconfiguração da variável de passo
        powerflow.solution["ndiv"] += 1

        # Reconfiguração do valor da variável de passo
        powerflow.solution["step"] = deepcopy(
            powerflow.operationpoint[case]["c"]["step"]
        )
        powerflow.solution["stepsch"] = deepcopy(
            powerflow.operationpoint[case]["c"]["stepsch"]
        )
        powerflow.solution["vsch"] = deepcopy(
            powerflow.operationpoint[case]["c"]["vsch"]
        )
    return case


def exicresidue(
    powerflow,
    case,
    stage: str = None,
):
    """cálculo de resíduos das equações diferenciáveis

    Args
        powerflow: self do arquivo powerflow.py
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """

    ## Inicialização
    residue(
        powerflow,
        case,
    )

    # Resíduo de Fluxo de Potência Continuado
    # Condição de previsão
    if stage == "p":
        powerflow.deltaPQY = zeros(powerflow.deltaPQY.shape[0] + 1)
        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            if not powerflow.solution["pmc"]:
                powerflow.deltaPQY[-1] = powerflow.options["LMBD"] * (
                    5e-1 ** powerflow.solution["ndiv"]
                )

            elif powerflow.solution["pmc"]:
                powerflow.deltaPQY[-1] = (
                    -1
                    * powerflow.options["LMBD"]
                    * (5e-1 ** powerflow.solution["ndiv"])
                )

        elif powerflow.solution["varstep"] == "volt":
            powerflow.deltaPQY[-1] = (
                -1 * powerflow.options["ICMV"] * (5e-1 ** powerflow.solution["ndiv"])
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
                    - powerflow.solution["voltage"][powerflow.nodevarvolt]
                ]
            )

        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)


def exicjacobian(
    powerflow,
):
    """expansão da matriz jacobiana para o método continuado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Arrays adicionais
    rowarray = zeros([1, powerflow.jacobian.shape[0]])

    # Condição de variável de passo
    if powerflow.solution["varstep"] == "lambda":
        stepvar = 1

    elif powerflow.solution["varstep"] == "volt":
        rowarray[0, (powerflow.nbus + powerflow.nodevarvolt)] = 1

    # Demanda
    colarray = concatenate(
        (
            powerflow.solution["demanda_ativa"] - powerflow.solution["potencia_ativa"],
            powerflow.solution["demanda_reativa"],
            zeros(powerflow.controldim + 1),
        ),
        axis=0,
    )
    colarray = (colarray[powerflow.mask] / powerflow.options["BASE"]).reshape(
        (sum(powerflow.mask), 1)
    )

    # Expansão Jacobiana Continuada
    powerflow.jacobian = concatenate(
        (powerflow.jacobian, colarray),
        axis=1,
    )
    powerflow.jacobian = concatenate(
        (powerflow.jacobian, concatenate((rowarray, array([[stepvar]])), axis=1)),
        axis=0,
    )


def update_statevar(
    powerflow,
    case,
    stage: str = None,
):
    """atualização das variáveis de estado

    Args
        powerflow: self do arquivo powerflow.py
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """

    ## Inicialização
    powerflow.solution["theta"][powerflow.maskP] += (
        powerflow.solution["sign"] * powerflow.statevar[0 : (powerflow.Tval)]
    )
    # Condição de previsão
    if stage == "p":
        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            powerflow.solution["voltage"][powerflow.maskQ] += (
                powerflow.solution["sign"]
                * powerflow.statevar[
                    (powerflow.Tval) : (powerflow.Tval + powerflow.Vval)
                ]
            )
            powerflow.solution["stepsch"] += powerflow.statevar[-1]

        elif powerflow.solution["varstep"] == "volt":
            powerflow.solution["step"] += powerflow.statevar[-1]
            powerflow.solution["stepsch"] += powerflow.statevar[-1]
            powerflow.solution["vsch"] = (
                powerflow.solution["voltage"][powerflow.nodevarvolt]
                + powerflow.statevar[(powerflow.nbus + powerflow.nodevarvolt)]
            )

        # Verificação do Ponto de Máximo Carregamento
        if case > 0:
            if case == 1:
                powerflow.solution["stepmax"] = deepcopy(powerflow.solution["stepsch"])

            elif case != 1:
                if (
                    powerflow.solution["stepsch"]
                    > powerflow.operationpoint[case - 1]["c"]["step"]
                ) and (not powerflow.solution["pmc"]):
                    powerflow.solution["stepmax"] = deepcopy(
                        powerflow.solution["stepsch"]
                    )

                elif (
                    powerflow.solution["stepsch"]
                    < powerflow.operationpoint[case - 1]["c"]["step"]
                ) and (not powerflow.solution["pmc"]):
                    powerflow.solution["pmc"] = True
                    powerflow.pmcidx = deepcopy(case)

    # Condição de correção
    elif stage == "c":
        powerflow.solution["voltage"][powerflow.maskQ] += (
            powerflow.solution["sign"]
            * powerflow.statevar[(powerflow.Tval) : (powerflow.Tval + powerflow.Vval)]
        )
        powerflow.solution["step"] += powerflow.statevar[-1]

        if powerflow.solution["varstep"] == "volt":
            powerflow.solution["stepsch"] += powerflow.statevar[-1]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    updtpwr(
        powerflow,
    )


def exicstorage(
    powerflow,
    case,
    stage: str = None,
):
    """armazenamento dos resultados de fluxo de potência continuado

    Args
        powerflow: self do arquivo powerflow.py
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """

    ## Inicialização
    # Armazenamento das variáveis de solução do fluxo de potência
    powerflow.operationpoint[case][stage] = {
        **deepcopy(powerflow.solution),
    }

    # Armazenamento do índice do barramento com maior variação de magnitude de tensão
    powerflow.operationpoint[case]["nodevarvolt"] = deepcopy(powerflow.nodevarvolt)

    # # Análise de sensibilidade e armazenamento
    # eigensens(
    #     powerflow,
    #     case,
    #     stage=stage,
    # )


def exicevaluate(
    powerflow,
    case,
):
    """avaliação para determinação do passo do fluxo de potência continuado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição Inicial
    if case == 1:
        # Lambda
        varlambda = abs((powerflow.solution["step"] - 0) / (powerflow.solution["step"]))

        # Voltage
        powerflow.nodevarvolt = argmax(
            abs(powerflow.solution["voltage"] - powerflow.operationpoint[0]["voltage"])
        )
        varvolt = abs(
            (
                powerflow.solution["voltage"][powerflow.nodevarvolt]
                - powerflow.operationpoint[0]["voltage"][powerflow.nodevarvolt]
            )
            / powerflow.solution["voltage"][powerflow.nodevarvolt]
        )

    # Condição Durante
    elif case != 1:
        # Lambda
        varlambda = abs(
            (
                powerflow.operationpoint[case]["c"]["step"]
                - powerflow.operationpoint[case - 1]["c"]["step"]
            )
            / powerflow.operationpoint[case]["c"]["step"]
        )

        # Voltage
        powerflow.nodevarvolt = argmax(
            abs(
                powerflow.solution["voltage"]
                - powerflow.operationpoint[case - 1]["c"]["voltage"]
            )
        )
        varvolt = abs(
            (
                powerflow.operationpoint[case]["c"]["voltage"][powerflow.nodevarvolt]
                - powerflow.operationpoint[case - 1]["c"]["voltage"][
                    powerflow.nodevarvolt
                ]
            )
            / powerflow.operationpoint[case]["c"]["voltage"][powerflow.nodevarvolt]
        )

    # Avaliação
    if (varlambda > varvolt) and (powerflow.solution["varstep"] == "lambda"):
        powerflow.solution["varstep"] = "lambda"

    else:
        if powerflow.solution["pmc"]:
            if (
                (
                    powerflow.solution["step"]
                    < (powerflow.options["cpfV2L"] * powerflow.solution["stepmax"])
                )
                and (varlambda > varvolt)
                and (not powerflow.solution["v2l"])
            ):
                powerflow.solution["varstep"] = "lambda"
                powerflow.options["LMBD"] = deepcopy(
                    powerflow.operationpoint[1]["c"]["step"]
                )
                powerflow.solution["v2l"] = True
                powerflow.solution["ndiv"] = 0
                powerflow.v2lidx = deepcopy(case)

            elif not powerflow.solution["v2l"]:
                powerflow.solution["varstep"] = "volt"

        elif (
            (not powerflow.solution["pmc"])
            and (powerflow.solution["varstep"] == "lambda")
            and (
                (
                    powerflow.options["LMBD"]
                    * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["ndiv"])
                )
                <= powerflow.options["ICMN"]
            )
        ):
            powerflow.solution["pmc"] = True
            powerflow.pmcidx = deepcopy(case)
            powerflow.solution["varstep"] = "volt"
            powerflow.solution["ndiv"] = 0


def exicheuristics(
    self,
    powerflow,
):
    """heurísticas para determinação do funcionamento do fluxo de potência continuado

    Args
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
        and (not powerflow.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                powerflow.solution["voltage"] - powerflow.operationpoint[0]["voltage"]
                <= powerflow.options["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
            case -= 1
            controlpop(
                powerflow,
            )

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                "system",
                "pmc",
                "v2l",
                "ndiv",
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
                key: deepcopy(powerflow.operationpoint[case][key])
                for key in powerflow.solution.keys() & cpfkeys
            }
            powerflow.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.operationpoint[case]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.operationpoint[case]["theta"]
            )

    elif (
        (powerflow.name != "ieee24")
        and (powerflow.name != "ieee118")
        and (powerflow.name != "ieee118-collapse")
        and (case == 2)
        and (not powerflow.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                powerflow.solution["voltage"]
                - powerflow.operationpoint[case - 1]["c"]["voltage"]
                <= powerflow.options["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
            case -= 2
            controlpop(powerflow, pop=2)

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                "system",
                "pmc",
                "v2l",
                "ndiv",
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
                key: deepcopy(powerflow.operationpoint[case][key])
                for key in powerflow.solution.keys() & cpfkeys
            }
            powerflow.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.operationpoint[case]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.operationpoint[case]["theta"]
            )

    elif (
        (powerflow.name != "ieee24")
        and (powerflow.name != "ieee118")
        and (powerflow.name != "ieee118-collapse")
        and (case > 2)
        and (not powerflow.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                powerflow.solution["voltage"]
                - powerflow.operationpoint[case - 1]["c"]["voltage"]
                <= powerflow.options["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
            case -= 2
            controlpop(powerflow, pop=2)

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                "system",
                "pmc",
                "v2l",
                "ndiv",
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
                key: deepcopy(powerflow.operationpoint[case]["c"][key])
                for key in powerflow.solution.keys() & cpfkeys
            }
            powerflow.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.operationpoint[case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.operationpoint[case]["c"]["theta"]
            )

    if case > 0:
        # Condição de divergência na etapa de previsão por excesso de iterações
        if (
            (powerflow.operationpoint[case]["p"]["iter"] > powerflow.options["ACIT"])
            and (not self.active_heuristic)
            and (powerflow.name != "ieee118")
            and (powerflow.name != "ieee118-collapse")
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
            case -= 1
            controlpop(
                powerflow,
            )

            # Reconfiguração das variáveis de passo
            cpfkeys = {
                "system",
                "pmc",
                "v2l",
                "ndiv",
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
                key: deepcopy(powerflow.operationpoint[case]["c"][key])
                for key in powerflow.solution.keys() & cpfkeys
            }
            powerflow.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            powerflow.solution["voltage"] = deepcopy(
                powerflow.operationpoint[case]["c"]["voltage"]
            )
            powerflow.solution["theta"] = deepcopy(
                powerflow.operationpoint[case]["c"]["theta"]
            )

        # Condição de atingimento do PMC para varstep volt pequeno
        if (
            (not powerflow.solution["pmc"])
            and (powerflow.solution["varstep"] == "volt")
            and (
                powerflow.options["ICMV"] * (5e-1 ** powerflow.solution["ndiv"])
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
            powerflow.solution["ndiv"] = 0

            # Condição de máximo carregamento atingida
            powerflow.solution["pmc"] = True
            powerflow.operationpoint[case]["c"]["pmc"] = True
            powerflow.pmcidx = deepcopy(case)

        # Condição de valor de tensão da barra slack variar
        if (
            (
                powerflow.solution["voltage"][powerflow.slackidx]
                < (powerflow.dbarDF.loc[powerflow.slackidx, "tensao"] * 1e-3) - 1e-8
            )
            or (
                powerflow.solution["voltage"][powerflow.slackidx]
                > (powerflow.dbarDF.loc[powerflow.slackidx, "tensao"] * 1e-3) + 1e-8
            )
        ) and (not self.active_heuristic):

            # variação de tensão da barra slack
            if (powerflow.name == "ieee118") and (
                sum(powerflow.dbarDF.demanda_ativa.to_numpy()) > 5400
            ):
                pass

            else:
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
                case -= 1
                controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "ndiv",
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
                    key: deepcopy(powerflow.operationpoint[case]["c"][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["ndiv"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.operationpoint[case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.operationpoint[case]["c"]["theta"]
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
                self.auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
                case -= 1
                controlpop(
                    powerflow,
                )

                # Reconfiguração das variáveis de passo
                cpfkeys = {
                    "system",
                    "pmc",
                    "v2l",
                    "ndiv",
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
                    key: deepcopy(powerflow.operationpoint[case]["c"][key])
                    for key in powerflow.solution.keys() & cpfkeys
                }
                powerflow.solution["ndiv"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                powerflow.solution["voltage"] = deepcopy(
                    powerflow.operationpoint[case]["c"]["voltage"]
                )
                powerflow.solution["theta"] = deepcopy(
                    powerflow.operationpoint[case]["c"]["theta"]
                )

            # Condição de atingimento de ponto de bifurcação
            if (powerflow.bifurcation) and (not powerflow.solution["pmc"]):
                powerflow.solution["pmc"] = True
                powerflow.pmcidx = deepcopy(case)
                powerflow.solution["varstep"] = "volt"
                powerflow.solution["ndiv"] = 0


def exiccvgprint(
    powerflow,
    case,
):
    """impressão de convergência do fluxo de potência continuado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Impressão de convergência
    # print(
    #     f"Convergência: {powerflow.solution['convergence']} - Caso: {len(powerflow.operationpoint)} - Iteração: {powerflow.solution['iter']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão: {norm(powerflow.solution['voltage'] - powerflow.operationpoint[0]['voltage'])}"
    # )
    # print(
    #     f"Variação de Defasagem Angular: {norm(powerflow.solution['theta'] - powerflow.operationpoint[0]['theta'])}"
    # )
    # print(
    #     f"Variação de Potência Ativa: {norm(powerflow.solution['active'] - powerflow.operationpoint[0]['active'])}"
    # )
    # print(
    #     f"Variação de Potência Reativa: {norm(powerflow.solution['reactive'] - powerflow.operationpoint[0]['reactive'])}"
    # )
    # print(
    #     f"Variação de Frequência: {norm(powerflow.solution['freq'] - powerflow.operationpoint[0]['freq'])}"
    # )
    # print(
    #     f"Variação de Passo: {powerflow.solution['step'] - powerflow.operationpoint[0]['step']}"
    # )
    # print(
    #     f"Variação de Passo Programado: {powerflow.solution['stepsch'] - powerflow.operationpoint[0]['stepsch']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão Programada: {powerflow.solution['vsch'] - powerflow.operationpoint[0]['vsch']}"
    # )
    # print(
    #     f"Variação de Lambda: {powerflow.solution['step'] - powerflow.operationpoint[0]['step']}"
    # )
    # print(
    #     f"Variação de Lambda Programado: {powerflow.solution['stepsch'] - powerflow.operationpoint[0]['stepsch']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão Programada: {powerflow.solution['vsch'] - powerflow.operationpoint[0]['vsch']}"
    # )
    # print(
    #     f"Variação de Passo Máximo: {powerflow.solution['stepmax'] - powerflow.operationpoint[0]['stepmax']}"
    # )

    if (powerflow.solution["convergence"] == "SISTEMA CONVERGENTE") and (case > 0):
        print("Aumento Sistema (%): ", powerflow.solution["step"] * 1e2)
        if powerflow.solution["varstep"] == "volt":
            print(
                "Passo (%): ",
                powerflow.operationpoint[case]["c"]["varstep"],
                "  ",
                powerflow.options["ICMV"]
                * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["ndiv"])
                * 1e2,
            )
        else:
            print(
                "Passo (%): ",
                powerflow.operationpoint[case]["c"]["varstep"],
                "  ",
                powerflow.options["LMBD"]
                * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["ndiv"])
                * 1e2,
            )
        print("\n")

    if (
        powerflow.options["LMBD"]
        * ((1 / powerflow.options["FDIV"]) ** powerflow.solution["ndiv"])
        * 1e2
        < 2e-07
    ):
        print()
