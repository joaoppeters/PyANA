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
    anarede,
):
    """variável de estado adicional para o problema de fluxo de potência

    Args
        anarede:
    """
    ## Inicialização
    # Variáveis
    if "qlim_reactive_generation" not in anarede.solution:
        anarede.solution["qlim_reactive_generation"] = zeros([anarede.nbus])
        anarede.maskQ = ones(anarede.nbus, dtype=bool)
        anarede.mask = concatenate((anarede.maskP, anarede.maskQ), axis=0)
        anarede.slackqlim = False


def qlimres(
    anarede,
):
    """cálculo de resíduos das equações de controle adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Vetor de resíduos
    anarede.deltaQLIM = zeros([anarede.nger])

    # Contador
    nger = 0

    # Loop
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Tratamento de limites em barras PV
            if value["tipo"] == 1:
                if (
                    anarede.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_maxima"]
                ) and (
                    anarede.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de magnitude de tensão
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BASE"]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potência reativa gerada máxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.dbarDF.loc[idx, "tipo"] = -1

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potência reativa gerada mínima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_minima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.dbarDF.loc[idx, "tipo"] = -1

            # Tratamento de backoff em barras PQV
            elif value["tipo"] == -1:
                if (
                    (
                        anarede.solution["qlim_reactive_generation"][idx]
                        >= value["potencia_reativa_maxima"]
                    )
                    and (anarede.solution["voltage"][idx] > value["tensao"] * (1e-3))
                ) or (
                    (
                        anarede.solution["qlim_reactive_generation"][idx]
                        <= value["potencia_reativa_minima"]
                    )
                    and (anarede.solution["voltage"][idx] < value["tensao"] * (1e-3))
                ):
                    # Tratamento de backoff de magnitude de tensão
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BASE"]
                    anarede.dbarDF.loc[idx, "tipo"] = 1

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (anarede.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada máxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (anarede.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada mínima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_minima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

            # Tratamento de limites de barra SLACK
            elif (value["tipo"] == 2) and (not anarede.slackqlim):
                if (
                    anarede.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_maxima"]
                ) and (
                    anarede.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de magnitude de tensão
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BASE"]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potência reativa gerada máxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.slackqlim = True

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potência reativa gerada mínima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_minima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.slackqlim = True

            # Tratamento de backoff de barra SLACK
            elif (value["tipo"] == 2) and (anarede.slackqlim):
                if (
                    (
                        anarede.solution["qlim_reactive_generation"][idx]
                        >= value["potencia_reativa_maxima"]
                    )
                    and (anarede.solution["voltage"][idx] > value["tensao"] * (1e-3))
                ) or (
                    (
                        anarede.solution["qlim_reactive_generation"][idx]
                        <= value["potencia_reativa_minima"]
                    )
                    and (anarede.solution["voltage"][idx] < value["tensao"] * (1e-3))
                ):
                    # Tratamento de backoff de magnitude de tensão
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BASE"]
                    anarede.slackqlim = False

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (anarede.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada máxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (anarede.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potência reativa gerada mínima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_minima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    anarede.deltaQLIM /= anarede.cte["BASE"]
    anarede.deltaY = append(anarede.deltaY, anarede.deltaQLIM)


def qlimsubjac(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
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
    anarede.dimpreqlim = deepcopy(anarede.jacobian.shape[0])

    # Submatrizes
    anarede.px = zeros([anarede.nbus, anarede.nger])
    anarede.qx = zeros([anarede.nbus, anarede.nger])
    anarede.yx = zeros([anarede.nger, anarede.nger])
    anarede.yt = zeros([anarede.nger, anarede.nbus])
    anarede.yv = zeros([anarede.nger, anarede.nbus])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # dQg/dx
            anarede.qx[idx, nger] = -1

            anarede.yx[nger, nger] = 1e-10

            # Barras PV
            if (value["tipo"] == 1) or (
                (value["tipo"] == 2) and (not anarede.slackqlim)
            ):
                anarede.yv[nger, idx] = 1

            # Barras PQV
            elif (value["tipo"] == -1) or (
                (value["tipo"] == 2) and (anarede.slackqlim)
            ):
                anarede.yx[nger, nger] = 1

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    # Condição
    if anarede.controldim != 0:
        anarede.extrarow = zeros([anarede.nger, anarede.controldim])
        anarede.extracol = zeros([anarede.controldim, anarede.nger])

        ytv = csc_matrix(
            concatenate(
                (anarede.yt, anarede.yv, anarede.extrarow),
                axis=1,
            )
        )
        pqyx = csc_matrix(
            concatenate(
                (
                    anarede.px,
                    anarede.qx,
                    anarede.extracol,
                    anarede.yx,
                ),
                axis=0,
            )
        )

    elif anarede.controldim == 0:
        ytv = csc_matrix(concatenate((anarede.yt, anarede.yv), axis=1))
        pqyx = csc_matrix(concatenate((anarede.px, anarede.qx, anarede.yx), axis=0))

    anarede.jacobian = vstack([anarede.jacobian, ytv], format="csc")
    anarede.jacobian = hstack([anarede.jacobian, pqyx], format="csc")


def qlimupdt(
    anarede,
):
    """atualização das variáveis de estado adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Contador
    nger = 0

    # Atualização da potência reativa gerada
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            anarede.solution["qlim_reactive_generation"][idx] += (
                anarede.statevar[(anarede.dimpreqlim + nger)] * anarede.cte["BASE"]
            )

            if (value["tipo"] == 1) and (
                (
                    anarede.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                )
                or (
                    anarede.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_minima"]
                )
            ):
                anarede.dbarDF.loc[idx, "tipo"] = -1

            if (value["tipo"] == 2) and (
                (
                    anarede.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                )
                or (
                    anarede.solution["qlim_reactive_generation"][idx]
                    < value["potencia_reativa_minima"]
                )
            ):
                anarede.slackqlim = True

            # Incrementa contador
            nger += 1

    qlimsch(
        anarede,
    )


def qlimsch(
    anarede,
):
    """atualização do valor de potência reativa especificada

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.qsch = zeros([anarede.nbus])

    # Atualização da potência reativa especificada
    anarede.qsch += anarede.solution["qlim_reactive_generation"]
    anarede.qsch -= anarede.dbarDF["demanda_reativa"].to_numpy()
    anarede.qsch /= anarede.cte["BASE"]


def qlimcorr(
    anarede,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.solution["qlim_reactive_generation"] = deepcopy(
        anarede.operationpoint[case]["p"]["qlim_reactive_generation"]
    )


def qlimheur(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    # Condição de geração de potência reativa ser superior ao valor máximo
    if any(
        (
            anarede.solution["qlim_reactive_generation"]
            > anarede.dbarDF["potencia_reativa_maxima"].to_numpy()
        ),
        where=~anarede.mask[(anarede.nbus) : (2 * anarede.nbus)],
    ):
        anarede.controlheur = True

    # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
    if (
        (not anarede.solution["pmc"])
        and (anarede.solution["varstep"] == "lambda")
        and (
            (anarede.cte["LMBD"] * (5e-1 ** anarede.solution["ndiv"]))
            <= anarede.cte["ICMN"]
        )
    ):
        anarede.bifurcation = True
        # Condição de curva completa do fluxo de potência continuado
        if anarede.cte["FULL"]:
            anarede.dbarDF["true_potencia_reativa_minima"] = anarede.dbarDF.loc[
                :, "potencia_reativa_minima"
            ]
            for idx, value in anarede.dbarDF.iterrows():
                if (
                    anarede.solution["qlim_reactive_generation"][idx]
                    > value["potencia_reativa_maxima"]
                ):
                    anarede.dbarDF.loc[idx, "potencia_reativa_minima"] = deepcopy(
                        value["potencia_reativa_maxima"]
                    )


def qlimsubhess(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
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
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    pass
