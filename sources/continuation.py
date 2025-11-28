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
    anarede,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Args
        anarede:
    """
    ## Inicialização
    # Variável para armazenamento das variáveis de solução do fluxo de potência continuado
    anarede.solution.update(
        {
            "method": "EXIC",
            "demanda_ativa": deepcopy(anarede.dbarDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(anarede.dbarDF["demanda_reativa"]),
            "potencia_ativa": deepcopy(anarede.dbarDF["potencia_ativa"]),
            "potencia_reativa": deepcopy(anarede.dbarDF["potencia_reativa"]),
            "pmc": False,
            "v2l": False,
            "ndiv": 0,
            "beta": deepcopy(anarede.cte["cpfBeta"]),
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
    anarede.operationpoint = dict()

    # Variável para armazenamento de solução por casos do continuado (previsão e correção)
    case = 0

    # Armazenamento da solução inicial
    anarede.operationpoint[case] = {
        **deepcopy(anarede.solution),
    }

    # # Armazenamento de determinante e autovalores
    # eigensens(
    #     anarede,
    #     case,
    # )

    # Reconfiguração da Máscara - Elimina expansão da matriz Jacobiana
    anarede.mask = append(anarede.mask, False)

    # Barra com maior variação de magnitude de tensão - CASO BASE
    anarede.nodevarvolt = argmax(
        norm(anarede.solution["voltage"] - anarede.dbarDF["tensao"] * 1e-3)
    )

    # Loop de Previsão - Correção
    exicloop(
        anarede,
        case,
    )

    del anarede.operationpoint[len(anarede.operationpoint) - 1]

    # Geração e armazenamento de gráficos de perfil de tensão e autovalores
    loading(
        anarede,
    )

    # Smooth exicstorage
    if "QLIMs" in anarede.control:
        for _, v in anarede.qlimkeys.items():
            v.popitem()
        from smooth import qlimstorage

        qlimstorage(
            anarede,
        )
    if "SVCs" in anarede.control:
        for _, v in anarede.svckeys.items():
            v.popitem()
        from smooth import svcstorage

        svcstorage(
            anarede,
        )


def exicloop(
    anarede,
    case,
):
    """loop do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Condição de parada do fluxo de potência continuado -> Estável & Instável
    while (
        anarede.cte["LMBD"]
        * ((1 / anarede.cte["FDIV"]) ** anarede.solution["ndiv"])
        * 1e2
        >= anarede.cte["ICMN"]
        and anarede.solution["ndiv"] <= anarede.cte["DMAX"]
        and case <= anarede.cte["ICIT"]
    ):

        # Incremento de Caso
        case += 1

        # Variável de armazenamento
        anarede.operationpoint[case] = dict()

        # Previsão
        prediction(
            anarede,
            case,
        )

        # Correção
        case = correction(
            anarede,
            case,
        )

        if (
            anarede.solution["cvgprint"]
            and anarede.solution["convergence"] == "SISTEMA CONVERGENTE"
        ):
            exiccvgprint(
                anarede,
                case,
            )

        # Break Curva de Carregamento - Parte Estável
        if (not anarede.cte["FULL"]) and (anarede.solution["pmc"]):
            break


def prediction(
    anarede,
    case,
):
    """etapa de previsão do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    anarede.solution["iter"] = 0

    # Incremento do Nível de Carregamento e Geração
    increment(
        anarede,
    )

    # Variáveis Especificadas
    scheduled(
        anarede,
    )

    # Resíduos
    residue(
        anarede,
        case,
        stage="p",
    )

    # Atualização da Matriz Jacobiana
    matrices(
        anarede,
    )

    # Expansão Jacobiana
    exicjacobian(
        anarede,
    )

    # Variáveis de estado
    anarede.statevar, residuals, rank, singular = lstsq(
        anarede.jacobian,
        anarede.deltaPQY,
        rcond=None,
    )

    # Atualização das Variáveis de estado
    updtstt(
        anarede,
        case,
        stage="p",
    )

    updtpwr(
        anarede,
    )

    # Armazenamento de Solução
    exicstorage(
        anarede,
        case,
        stage="p",
    )


def correction(
    anarede,
    case,
):
    """etapa de correção do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Variável para armazenamento de solução
    anarede.solution.update(
        {
            "iter": 0,
            "voltage": deepcopy(anarede.operationpoint[case]["p"]["voltage"]),
            "theta": deepcopy(anarede.operationpoint[case]["p"]["theta"]),
            "active": deepcopy(anarede.operationpoint[case]["p"]["active"]),
            "reactive": deepcopy(anarede.operationpoint[case]["p"]["reactive"]),
            "freq": deepcopy(anarede.operationpoint[case]["p"]["freq"]),
            "freqiter": array([]),
            "convP": array([]),
            "busP": array([]),
            "convQ": array([]),
            "busQ": array([]),
            "convY": array([]),
            "busY": array([]),
            "active_flow_F2": zeros(anarede.nlin),
            "reactive_flow_F2": zeros(anarede.nlin),
            "active_flow_2F": zeros(anarede.nlin),
            "reactive_flow_2F": zeros(anarede.nlin),
        }
    )

    # Adição de variáveis de controle na variável de armazenamento de solução
    controlcorrsol(
        anarede,
        case,
    )

    # Incremento do Nível de Carregamento e Geração
    increment(
        anarede,
    )

    # Variáveis Especificadas
    scheduled(
        anarede,
    )

    # Resíduos
    residue(
        anarede,
        case,
        stage="c",
    )

    while (
        norm(
            anarede.deltaP[anarede.maskP],
        )
        > anarede.cte["TEPA"]
        or norm(
            anarede.deltaQ[anarede.maskQ],
        )
        > anarede.cte["TEPR"]
        or controldelta(
            anarede,
        )
    ):
        # Armazenamento da trajetória de convergência
        convergence(
            anarede,
        )

        # Atualização da Matriz Jacobiana
        matrices(
            anarede,
        )

        # Expansão Jacobiana
        exicjacobian(
            anarede,
        )

        # Variáveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            anarede,
            case,
            stage="c",
        )

        updtpwr(
            anarede,
        )

        # Condição de variável de passo
        if anarede.solution["varstep"] == "volt":
            # Incremento do Nível de Carregamento e Geração
            increment(
                anarede,
            )

            # Variáveis Especificadas
            scheduled(
                anarede,
            )

        # Atualização dos resíduos
        residue(
            anarede,
            case,
            stage="c",
        )

        # Incremento de iteração
        anarede.solution["iter"] += 1

        # Condição de Divergência por iterações
        if anarede.solution["iter"] > anarede.cte["ACIT"]:
            anarede.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

    ## Condição
    # Iteração Adicional em Caso de Convergência
    if anarede.solution["iter"] < anarede.cte["ACIT"]:
        # Armazenamento da trajetória de convergência
        convergence(
            anarede,
        )

        # Atualização da Matriz Jacobiana
        matrices(
            anarede,
        )

        # Expansão Jacobiana
        exicjacobian(
            anarede,
        )

        # Variáveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            anarede,
            case,
            stage="c",
        )

        updtpwr(
            anarede,
        )

        # Atualização dos resíduos
        residue(
            anarede,
            case,
            stage="c",
        )

        # Armazenamento de Solução
        exicstorage(
            anarede,
            case,
            stage="c",
        )

        # Convergência
        anarede.solution["convergence"] = "SISTEMA CONVERGENTE"

        # Avaliação
        exicevaluate(
            anarede,
            case,
        )

    # Reconfiguração dos Dados de Solução em Caso de Divergência
    elif ((anarede.solution["iter"] >= anarede.cte["ACIT"])) and (case == 1):
        # self.active_heuristic = True
        anarede.solution["convergence"] = "SISTEMA DIVERGENTE"

        # Reconfiguração do caso
        case -= 1
        controlpop(
            anarede,
        )

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        anarede.solution["voltage"] = deepcopy(
            anarede.operationpoint[case]["c"]["voltage"]
        )
        anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["c"]["theta"])

        # Reconfiguração da variável de passo
        anarede.solution["ndiv"] += 1

        # Reconfiguração do valor da variável de passo
        anarede.solution["step"] = deepcopy(anarede.operationpoint[case]["c"]["step"])
        anarede.solution["stepsch"] = deepcopy(
            anarede.operationpoint[case]["c"]["stepsch"]
        )
        anarede.solution["vsch"] = deepcopy(anarede.operationpoint[case]["c"]["vsch"])

    # Reconfiguração dos Dados de Solução em Caso de Divergência
    elif ((anarede.solution["iter"] >= anarede.cte["ACIT"])) and (case > 1):
        # self.active_heuristic = True
        anarede.solution["convergence"] = "SISTEMA DIVERGENTE"

        # Reconfiguração do caso
        case -= 1
        controlpop(
            anarede,
        )

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        anarede.solution["voltage"] = deepcopy(
            anarede.operationpoint[case]["c"]["voltage"]
        )
        anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["c"]["theta"])

        # Reconfiguração da variável de passo
        anarede.solution["ndiv"] += 1

        # Reconfiguração do valor da variável de passo
        anarede.solution["step"] = deepcopy(anarede.operationpoint[case]["c"]["step"])
        anarede.solution["stepsch"] = deepcopy(
            anarede.operationpoint[case]["c"]["stepsch"]
        )
        anarede.solution["vsch"] = deepcopy(anarede.operationpoint[case]["c"]["vsch"])
    return case


def exicresidue(
    anarede,
    case,
    stage: str = None,
):
    """cálculo de resíduos das equações diferenciáveis

    Args
        anarede:
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """
    ## Inicialização
    residue(
        anarede,
        case,
    )

    # Resíduo de Fluxo de Potência Continuado
    # Condição de previsão
    if stage == "p":
        anarede.deltaPQY = zeros(anarede.deltaPQY.shape[0] + 1)
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            if not anarede.solution["pmc"]:
                anarede.deltaPQY[-1] = anarede.cte["LMBD"] * (
                    5e-1 ** anarede.solution["ndiv"]
                )

            elif anarede.solution["pmc"]:
                anarede.deltaPQY[-1] = (
                    -1 * anarede.cte["LMBD"] * (5e-1 ** anarede.solution["ndiv"])
                )

        elif anarede.solution["varstep"] == "volt":
            anarede.deltaPQY[-1] = (
                -1 * anarede.cte["ICMV"] * (5e-1 ** anarede.solution["ndiv"])
            )

    # Condição de correção
    elif stage == "c":
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            anarede.deltaY = array(
                [anarede.solution["stepsch"] - anarede.solution["step"]]
            )

        elif anarede.solution["varstep"] == "volt":
            anarede.deltaY = array(
                [
                    anarede.solution["vsch"]
                    - anarede.solution["voltage"][anarede.nodevarvolt]
                ]
            )

        anarede.deltaPQY = concatenate((anarede.deltaPQY, anarede.deltaY), axis=0)


def exicjacobian(
    anarede,
):
    """expansão da matriz jacobiana para o método continuado

    Args
        anarede:
    """
    ## Inicialização
    # Arrays adicionais
    rowarray = zeros([1, anarede.jacobian.shape[0]])

    # Condição de variável de passo
    if anarede.solution["varstep"] == "lambda":
        stepvar = 1

    elif anarede.solution["varstep"] == "volt":
        rowarray[0, (anarede.nbus + anarede.nodevarvolt)] = 1

    # Demanda
    colarray = concatenate(
        (
            anarede.solution["demanda_ativa"] - anarede.solution["potencia_ativa"],
            anarede.solution["demanda_reativa"],
            zeros(anarede.controldim + 1),
        ),
        axis=0,
    )
    colarray = (colarray[anarede.mask] / anarede.cte["BASE"]).reshape(
        (sum(anarede.mask), 1)
    )

    # Expansão Jacobiana Continuada
    anarede.jacobian = concatenate(
        (anarede.jacobian, colarray),
        axis=1,
    )
    anarede.jacobian = concatenate(
        (anarede.jacobian, concatenate((rowarray, array([[stepvar]])), axis=1)),
        axis=0,
    )


def update_statevar(
    anarede,
    case,
    stage: str = None,
):
    """atualização das variáveis de estado

    Args
        anarede:
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """
    ## Inicialização
    anarede.solution["theta"][anarede.maskP] += (
        anarede.solution["sign"] * anarede.statevar[0 : (anarede.Tval)]
    )
    # Condição de previsão
    if stage == "p":
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            anarede.solution["voltage"][anarede.maskQ] += (
                anarede.solution["sign"]
                * anarede.statevar[(anarede.Tval) : (anarede.Tval + anarede.Vval)]
            )
            anarede.solution["stepsch"] += anarede.statevar[-1]

        elif anarede.solution["varstep"] == "volt":
            anarede.solution["step"] += anarede.statevar[-1]
            anarede.solution["stepsch"] += anarede.statevar[-1]
            anarede.solution["vsch"] = (
                anarede.solution["voltage"][anarede.nodevarvolt]
                + anarede.statevar[(anarede.nbus + anarede.nodevarvolt)]
            )

        # Verificação do Ponto de Máximo Carregamento
        if case > 0:
            if case == 1:
                anarede.solution["stepmax"] = deepcopy(anarede.solution["stepsch"])

            elif case != 1:
                if (
                    anarede.solution["stepsch"]
                    > anarede.operationpoint[case - 1]["c"]["step"]
                ) and (not anarede.solution["pmc"]):
                    anarede.solution["stepmax"] = deepcopy(anarede.solution["stepsch"])

                elif (
                    anarede.solution["stepsch"]
                    < anarede.operationpoint[case - 1]["c"]["step"]
                ) and (not anarede.solution["pmc"]):
                    anarede.solution["pmc"] = True
                    anarede.pmcidx = deepcopy(case)

    # Condição de correção
    elif stage == "c":
        anarede.solution["voltage"][anarede.maskQ] += (
            anarede.solution["sign"]
            * anarede.statevar[(anarede.Tval) : (anarede.Tval + anarede.Vval)]
        )
        anarede.solution["step"] += anarede.statevar[-1]

        if anarede.solution["varstep"] == "volt":
            anarede.solution["stepsch"] += anarede.statevar[-1]

    # Atualização das variáveis de estado adicionais para controles ativos
    if anarede.controlcount > 0:
        controlupdt(
            anarede,
        )

    updtpwr(
        anarede,
    )


def exicstorage(
    anarede,
    case,
    stage: str = None,
):
    """armazenamento dos resultados de fluxo de potência continuado

    Args
        anarede:
        stage: string de identificação da etapa do fluxo de potência continuado (previsão/correção)
    """
    ## Inicialização
    # Armazenamento das variáveis de solução do fluxo de potência
    anarede.operationpoint[case][stage] = {
        **deepcopy(anarede.solution),
    }

    # Armazenamento do índice do barramento com maior variação de magnitude de tensão
    anarede.operationpoint[case]["nodevarvolt"] = deepcopy(anarede.nodevarvolt)

    # # Análise de sensibilidade e armazenamento
    # eigensens(
    #     anarede,
    #     case,
    #     stage=stage,
    # )


def exicevaluate(
    anarede,
    case,
):
    """avaliação para determinação do passo do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Condição Inicial
    if case == 1:
        # Lambda
        varlambda = abs((anarede.solution["step"] - 0) / (anarede.solution["step"]))

        # Voltage
        anarede.nodevarvolt = argmax(
            abs(anarede.solution["voltage"] - anarede.operationpoint[0]["voltage"])
        )
        varvolt = abs(
            (
                anarede.solution["voltage"][anarede.nodevarvolt]
                - anarede.operationpoint[0]["voltage"][anarede.nodevarvolt]
            )
            / anarede.solution["voltage"][anarede.nodevarvolt]
        )

    # Condição Durante
    elif case != 1:
        # Lambda
        varlambda = abs(
            (
                anarede.operationpoint[case]["c"]["step"]
                - anarede.operationpoint[case - 1]["c"]["step"]
            )
            / anarede.operationpoint[case]["c"]["step"]
        )

        # Voltage
        anarede.nodevarvolt = argmax(
            abs(
                anarede.solution["voltage"]
                - anarede.operationpoint[case - 1]["c"]["voltage"]
            )
        )
        varvolt = abs(
            (
                anarede.operationpoint[case]["c"]["voltage"][anarede.nodevarvolt]
                - anarede.operationpoint[case - 1]["c"]["voltage"][anarede.nodevarvolt]
            )
            / anarede.operationpoint[case]["c"]["voltage"][anarede.nodevarvolt]
        )

    # Avaliação
    if (varlambda > varvolt) and (anarede.solution["varstep"] == "lambda"):
        anarede.solution["varstep"] = "lambda"

    else:
        if anarede.solution["pmc"]:
            if (
                (
                    anarede.solution["step"]
                    < (anarede.cte["cpfV2L"] * anarede.solution["stepmax"])
                )
                and (varlambda > varvolt)
                and (not anarede.solution["v2l"])
            ):
                anarede.solution["varstep"] = "lambda"
                anarede.cte["LMBD"] = deepcopy(anarede.operationpoint[1]["c"]["step"])
                anarede.solution["v2l"] = True
                anarede.solution["ndiv"] = 0
                anarede.v2lidx = deepcopy(case)

            elif not anarede.solution["v2l"]:
                anarede.solution["varstep"] = "volt"

        elif (
            (not anarede.solution["pmc"])
            and (anarede.solution["varstep"] == "lambda")
            and (
                (
                    anarede.cte["LMBD"]
                    * ((1 / anarede.cte["FDIV"]) ** anarede.solution["ndiv"])
                )
                <= anarede.cte["ICMN"]
            )
        ):
            anarede.solution["pmc"] = True
            anarede.pmcidx = deepcopy(case)
            anarede.solution["varstep"] = "volt"
            anarede.solution["ndiv"] = 0


def exicheuristics(
    self,
    anarede,
):
    """heurísticas para determinação do funcionamento do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    ## Afundamento de tensão não desejado (em i+1) e retorno ao valor esperado (em i+2) -> correção: voltar duas casas
    # Condição de caso para sistema != ieee24 (pq nesse sistema há aumento de magnitude de tensão na barra 17 PQ)
    if (
        (anarede.name != "ieee24")
        and (anarede.name != "ieee118")
        and (anarede.name != "ieee118-collapse")
        and (case == 1)
        and (not anarede.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                anarede.solution["voltage"] - anarede.operationpoint[0]["voltage"]
                <= anarede.cte["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
            case -= 1
            controlpop(
                anarede,
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
            anarede.solution = {
                key: deepcopy(anarede.operationpoint[case][key])
                for key in anarede.solution.keys() & cpfkeys
            }
            anarede.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            anarede.solution["voltage"] = deepcopy(
                anarede.operationpoint[case]["voltage"]
            )
            anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["theta"])

    elif (
        (anarede.name != "ieee24")
        and (anarede.name != "ieee118")
        and (anarede.name != "ieee118-collapse")
        and (case == 2)
        and (not anarede.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                anarede.solution["voltage"]
                - anarede.operationpoint[case - 1]["c"]["voltage"]
                <= anarede.cte["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
            case -= 2
            controlpop(anarede, pop=2)

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
            anarede.solution = {
                key: deepcopy(anarede.operationpoint[case][key])
                for key in anarede.solution.keys() & cpfkeys
            }
            anarede.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            anarede.solution["voltage"] = deepcopy(
                anarede.operationpoint[case]["voltage"]
            )
            anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["theta"])

    elif (
        (anarede.name != "ieee24")
        and (anarede.name != "ieee118")
        and (anarede.name != "ieee118-collapse")
        and (case > 2)
        and (not anarede.solution["pmc"])
        and (not self.active_heuristic)
    ):
        if not all(
            (
                anarede.solution["voltage"]
                - anarede.operationpoint[case - 1]["c"]["voltage"]
                <= anarede.cte["VVAR"]
            )
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
            case -= 2
            controlpop(anarede, pop=2)

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
            anarede.solution = {
                key: deepcopy(anarede.operationpoint[case]["c"][key])
                for key in anarede.solution.keys() & cpfkeys
            }
            anarede.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            anarede.solution["voltage"] = deepcopy(
                anarede.operationpoint[case]["c"]["voltage"]
            )
            anarede.solution["theta"] = deepcopy(
                anarede.operationpoint[case]["c"]["theta"]
            )

    if case > 0:
        # Condição de divergência na etapa de previsão por excesso de iterações
        if (
            (anarede.operationpoint[case]["p"]["iter"] > anarede.cte["ACIT"])
            and (not self.active_heuristic)
            and (anarede.name != "ieee118")
            and (anarede.name != "ieee118-collapse")
        ):
            self.active_heuristic = True

            # Reconfiguração do caso
            self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
            case -= 1
            controlpop(
                anarede,
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
            anarede.solution = {
                key: deepcopy(anarede.operationpoint[case]["c"][key])
                for key in anarede.solution.keys() & cpfkeys
            }
            anarede.solution["ndiv"] = self.auxdiv

            # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
            anarede.solution["voltage"] = deepcopy(
                anarede.operationpoint[case]["c"]["voltage"]
            )
            anarede.solution["theta"] = deepcopy(
                anarede.operationpoint[case]["c"]["theta"]
            )

        # Condição de atingimento do PMC para varstep volt pequeno
        if (
            (not anarede.solution["pmc"])
            and (anarede.solution["varstep"] == "volt")
            and (
                anarede.cte["ICMV"] * (5e-1 ** anarede.solution["ndiv"])
                < anarede.cte["ICMN"]
            )
            and (not self.active_heuristic)
        ):
            self.active_heuristic = True

            # Reconfiguração de caso
            case -= 1
            controlpop(
                anarede,
            )

            # Reconfiguração da variável de passo
            anarede.solution["ndiv"] = 0

            # Condição de máximo carregamento atingida
            anarede.solution["pmc"] = True
            anarede.operationpoint[case]["c"]["pmc"] = True
            anarede.pmcidx = deepcopy(case)

        # Condição de valor de tensão da barra slack variar
        if (
            (
                anarede.solution["voltage"][anarede.slackidx]
                < (anarede.dbarDF.loc[anarede.slackidx, "tensao"] * 1e-3) - 1e-8
            )
            or (
                anarede.solution["voltage"][anarede.slackidx]
                > (anarede.dbarDF.loc[anarede.slackidx, "tensao"] * 1e-3) + 1e-8
            )
        ) and (not self.active_heuristic):

            # variação de tensão da barra slack
            if (anarede.name == "ieee118") and (
                sum(anarede.dbarDF.demanda_ativa.to_numpy()) > 5400
            ):
                pass

            else:
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
                case -= 1
                controlpop(
                    anarede,
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
                anarede.solution = {
                    key: deepcopy(anarede.operationpoint[case]["c"][key])
                    for key in anarede.solution.keys() & cpfkeys
                }
                anarede.solution["ndiv"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                anarede.solution["voltage"] = deepcopy(
                    anarede.operationpoint[case]["c"]["voltage"]
                )
                anarede.solution["theta"] = deepcopy(
                    anarede.operationpoint[case]["c"]["theta"]
                )

        # Condição de Heurísticas para controle
        if anarede.controlcount > 0:
            controlheuristics(
                anarede,
            )

            # Condição de violação de limite máximo de geração de potência reativa
            if (anarede.controlheur) and (not self.active_heuristic):
                self.active_heuristic = True

                # Reconfiguração do caso
                self.auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
                case -= 1
                controlpop(
                    anarede,
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
                anarede.solution = {
                    key: deepcopy(anarede.operationpoint[case]["c"][key])
                    for key in anarede.solution.keys() & cpfkeys
                }
                anarede.solution["ndiv"] = self.auxdiv

                # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
                anarede.solution["voltage"] = deepcopy(
                    anarede.operationpoint[case]["c"]["voltage"]
                )
                anarede.solution["theta"] = deepcopy(
                    anarede.operationpoint[case]["c"]["theta"]
                )

            # Condição de atingimento de ponto de bifurcação
            if (anarede.bifurcation) and (not anarede.solution["pmc"]):
                anarede.solution["pmc"] = True
                anarede.pmcidx = deepcopy(case)
                anarede.solution["varstep"] = "volt"
                anarede.solution["ndiv"] = 0


def exiccvgprint(
    anarede,
    case,
):
    """impressão de convergência do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Impressão de convergência
    # print(
    #     f"Convergência: {anarede.solution['convergence']} - Caso: {len(anarede.operationpoint)} - Iteração: {anarede.solution['iter']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão: {norm(anarede.solution['voltage'] - anarede.operationpoint[0]['voltage'])}"
    # )
    # print(
    #     f"Variação de Defasagem Angular: {norm(anarede.solution['theta'] - anarede.operationpoint[0]['theta'])}"
    # )
    # print(
    #     f"Variação de Potência Ativa: {norm(anarede.solution['active'] - anarede.operationpoint[0]['active'])}"
    # )
    # print(
    #     f"Variação de Potência Reativa: {norm(anarede.solution['reactive'] - anarede.operationpoint[0]['reactive'])}"
    # )
    # print(
    #     f"Variação de Frequência: {norm(anarede.solution['freq'] - anarede.operationpoint[0]['freq'])}"
    # )
    # print(
    #     f"Variação de Passo: {anarede.solution['step'] - anarede.operationpoint[0]['step']}"
    # )
    # print(
    #     f"Variação de Passo Programado: {anarede.solution['stepsch'] - anarede.operationpoint[0]['stepsch']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão Programada: {anarede.solution['vsch'] - anarede.operationpoint[0]['vsch']}"
    # )
    # print(
    #     f"Variação de Lambda: {anarede.solution['step'] - anarede.operationpoint[0]['step']}"
    # )
    # print(
    #     f"Variação de Lambda Programado: {anarede.solution['stepsch'] - anarede.operationpoint[0]['stepsch']}"
    # )
    # print(
    #     f"Variação de Magnitude de Tensão Programada: {anarede.solution['vsch'] - anarede.operationpoint[0]['vsch']}"
    # )
    # print(
    #     f"Variação de Passo Máximo: {anarede.solution['stepmax'] - anarede.operationpoint[0]['stepmax']}"
    # )

    if (anarede.solution["convergence"] == "SISTEMA CONVERGENTE") and (case > 0):
        print("Aumento Sistema (%): ", anarede.solution["step"] * 1e2)
        if anarede.solution["varstep"] == "volt":
            print(
                "Passo (%): ",
                anarede.operationpoint[case]["c"]["varstep"],
                "  ",
                anarede.cte["ICMV"]
                * ((1 / anarede.cte["FDIV"]) ** anarede.solution["ndiv"])
                * 1e2,
            )
        else:
            print(
                "Passo (%): ",
                anarede.operationpoint[case]["c"]["varstep"],
                "  ",
                anarede.cte["LMBD"]
                * ((1 / anarede.cte["FDIV"]) ** anarede.solution["ndiv"])
                * 1e2,
            )
        print("\n")

    if (
        anarede.cte["LMBD"]
        * ((1 / anarede.cte["FDIV"]) ** anarede.solution["ndiv"])
        * 1e2
        < 2e-07
    ):
        print()
