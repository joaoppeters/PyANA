# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, ones, zeros
from scipy.sparse import csc_matrix, hstack, vstack


def qlimsol(
    powerflow,
):
    """variável de estado adicional para o problema de fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    if "qlim_reactive_generation" not in powerflow.solution:
        powerflow.solution["qlim_reactive_generation"] = zeros([powerflow.nbus])
        powerflow.maskQ = ones(powerflow.nbus, dtype=bool)
        powerflow.mask = concatenate((powerflow.maskP, powerflow.maskQ), axis=0)
        powerflow.slackqlim = False


def qlimres(
    powerflow,
):
    """cálculo de resíduos das equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetor de resíduos
    powerflow.deltaQlim = zeros([powerflow.nger])

    # Contador
    nger = 0

    # Loop
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Tratamento de limites em barras PV
            if value["tipo"] == 1:
                if (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_maxima"]
                ) and (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de magnitude de tensão
                    powerflow.deltaQlim[nger] += value["tensao"] * (1e-3)
                    powerflow.deltaQlim[nger] -= powerflow.solution["voltage"][idx]
                    powerflow.deltaQlim[nger] *= powerflow.options["BASE"]

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potência reativa gerada máxima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_maxima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    powerflow.dbarDF.loc[idx, "tipo"] = -1

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potência reativa gerada mínima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_minima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    powerflow.dbarDF.loc[idx, "tipo"] = -1

            # Tratamento de backoff em barras PQV
            elif value["tipo"] == -1:
                if (
                    (
                        powerflow.solution["qlim_reactive_generation"][idx]
                        >= value["potencia_reativa_maxima"]
                    )
                    and (powerflow.solution["voltage"][idx] > value["tensao"] * (1e-3))
                ) or (
                    (
                        powerflow.solution["qlim_reactive_generation"][idx]
                        <= value["potencia_reativa_minima"]
                    )
                    and (powerflow.solution["voltage"][idx] < value["tensao"] * (1e-3))
                ):
                    # Tratamento de backoff de magnitude de tensão
                    powerflow.deltaQlim[nger] += value["tensao"] * (1e-3)
                    powerflow.deltaQlim[nger] -= powerflow.solution["voltage"][idx]
                    powerflow.deltaQlim[nger] *= powerflow.options["BASE"]
                    powerflow.dbarDF.loc[idx, "tipo"] = 1

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (powerflow.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada máxima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_maxima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (powerflow.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada mínima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_minima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]

            # Tratamento de limites de barra SLACK
            elif (value["tipo"] == 2) and (not powerflow.slackqlim):
                if (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_maxima"]
                ) and (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de magnitude de tensão
                    powerflow.deltaQlim[nger] += value["tensao"] * (1e-3)
                    powerflow.deltaQlim[nger] -= powerflow.solution["voltage"][idx]
                    powerflow.deltaQlim[nger] *= powerflow.options["BASE"]

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potência reativa gerada máxima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_maxima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    powerflow.slackqlim = True

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potência reativa gerada mínima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_minima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    powerflow.slackqlim = True

            # Tratamento de backoff de barra SLACK
            elif (value["tipo"] == 2) and (powerflow.slackqlim):
                if (
                    (
                        powerflow.solution["qlim_reactive_generation"][idx]
                        >= value["potencia_reativa_maxima"]
                    )
                    and (powerflow.solution["voltage"][idx] > value["tensao"] * (1e-3))
                ) or (
                    (
                        powerflow.solution["qlim_reactive_generation"][idx]
                        <= value["potencia_reativa_minima"]
                    )
                    and (powerflow.solution["voltage"][idx] < value["tensao"] * (1e-3))
                ):
                    # Tratamento de backoff de magnitude de tensão
                    powerflow.deltaQlim[nger] += value["tensao"] * (1e-3)
                    powerflow.deltaQlim[nger] -= powerflow.solution["voltage"][idx]
                    powerflow.deltaQlim[nger] *= powerflow.options["BASE"]
                    powerflow.slackqlim = False

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (powerflow.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada máxima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_maxima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (powerflow.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada mínima
                    powerflow.deltaQlim[nger] += value["potencia_reativa_minima"]
                    powerflow.deltaQlim[nger] -= powerflow.solution[
                        "qlim_reactive_generation"
                    ][idx]

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    powerflow.deltaQlim /= powerflow.options["BASE"]
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaQlim)


def qlimsubjac(
    powerflow,
):
    """submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    # Dimensão da matriz Jacobiana
    powerflow.dimpreqlim = deepcopy(powerflow.jacobian.shape[0])

    # Submatrizes
    powerflow.px = zeros([powerflow.nbus, powerflow.nger])
    powerflow.qx = zeros([powerflow.nbus, powerflow.nger])
    powerflow.yx = zeros([powerflow.nger, powerflow.nger])
    powerflow.yt = zeros([powerflow.nger, powerflow.nbus])
    powerflow.yv = zeros([powerflow.nger, powerflow.nbus])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            # dQg/dx
            powerflow.qx[idx, nger] = -1

            powerflow.yx[nger, nger] = 1e-10

            # Barras PV
            if (value["tipo"] == 1) or (
                (value["tipo"] == 2) and (not powerflow.slackqlim)
            ):
                powerflow.yv[nger, idx] = 1

            # Barras PQV
            elif (value["tipo"] == -1) or (
                (value["tipo"] == 2) and (powerflow.slackqlim)
            ):
                powerflow.yx[nger, nger] = 1

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    # Condição
    if powerflow.controldim != 0:
        powerflow.extrarow = zeros([powerflow.nger, powerflow.controldim])
        powerflow.extracol = zeros([powerflow.controldim, powerflow.nger])

        ytv = csc_matrix(
            concatenate(
                (powerflow.yt, powerflow.yv, powerflow.extrarow),
                axis=1,
            )
        )
        pqyx = csc_matrix(
            concatenate(
                (
                    powerflow.px,
                    powerflow.qx,
                    powerflow.extracol,
                    powerflow.yx,
                ),
                axis=0,
            )
        )

    elif powerflow.controldim == 0:
        ytv = csc_matrix(concatenate((powerflow.yt, powerflow.yv), axis=1))
        pqyx = csc_matrix(
            concatenate((powerflow.px, powerflow.qx, powerflow.yx), axis=0)
        )

    powerflow.jacobian = vstack([powerflow.jacobian, ytv], format="csc")
    powerflow.jacobian = hstack([powerflow.jacobian, pqyx], format="csc")


def qlimupdt(
    powerflow,
):
    """atualização das variáveis de estado adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Contador
    nger = 0

    # Atualização da potência reativa gerada
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            powerflow.solution["qlim_reactive_generation"][idx] += (
                powerflow.statevar[(powerflow.dimpreqlim + nger)]
                * powerflow.options["BASE"]
            )

            if (value["tipo"] == 1) and (
                (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                )
                or (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_minima"]
                )
            ):
                powerflow.dbarDF.loc[idx, "tipo"] = -1

            if (value["tipo"] == 2) and (
                (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                )
                or (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_minima"]
                )
            ):
                powerflow.slackqlim = True

            # Incrementa contador
            nger += 1

    qlimsch(
        powerflow,
    )


def qlimsch(
    powerflow,
):
    """atualização do valor de potência reativa especificada

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.qsch = zeros([powerflow.nbus])

    # Atualização da potência reativa especificada
    powerflow.qsch += powerflow.solution["qlim_reactive_generation"]
    powerflow.qsch -= powerflow.dbarDF["demanda_reativa"].to_numpy()
    powerflow.qsch /= powerflow.options["BASE"]


def qlimcorr(
    powerflow,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.solution["qlim_reactive_generation"] = deepcopy(
        powerflow.operationpoint[case]["p"]["qlim_reactive_generation"]
    )


def qlimheur(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição de geração de potência reativa ser superior ao valor máximo
    if any(
        (
            powerflow.solution["qlim_reactive_generation"]
            > powerflow.dbarDF["potencia_reativa_maxima"].to_numpy()
        ),
        where=~powerflow.mask[(powerflow.nbus) : (2 * powerflow.nbus)],
    ):
        powerflow.controlheur = True

    # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
    if (
        (not powerflow.solution["pmc"])
        and (powerflow.solution["varstep"] == "lambda")
        and (
            (powerflow.options["LMBD"] * (5e-1 ** powerflow.solution["ndiv"]))
            <= powerflow.options["ICMN"]
        )
    ):
        powerflow.bifurcation = True
        # Condição de curva completa do fluxo de potência continuado
        if powerflow.options["FULL"]:
            powerflow.dbarDF["true_potencia_reativa_minima"] = powerflow.dbarDF.loc[
                :, "potencia_reativa_minima"
            ]
            for idx, value in powerflow.dbarDF.iterrows():
                if (
                    powerflow.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                ):
                    powerflow.dbarDF.loc[idx, "potencia_reativa_minima"] = deepcopy(
                        value["potencia_reativa_maxima"]
                    )


def qlimsubhess(
    powerflow,
):
    """submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    pass


def qlimsubjacsym(
    powerflow,
):
    """

    Parametros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicializacao
    pass
