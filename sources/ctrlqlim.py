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
    """variavel de estado adicional para o problema de fluxo de potencia

    Args
        anarede:
    """
    # Variáveis
    if "qlim_reactive_generation" not in anarede.solution:
        anarede.solution["qlim_reactive_generation"] = zeros([anarede.nbus])
        anarede.maskQ = ones(anarede.nbus, dtype=bool)
        anarede.mask = concatenate((anarede.maskP, anarede.maskQ), axis=0)
        anarede.slackqlim = False


def qlimres(
    anarede,
):
    """calculo de residuos das equacoes de controle adicionais

    Args
        anarede:
    """
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
                    # Tratamento de limite de magnitude de tensao
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BMVA"]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potencia reativa gerada maxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.dbarDF.loc[idx, "tipo"] = -1

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potencia reativa gerada minima
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
                    # Tratamento de backoff de magnitude de tensao
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BMVA"]
                    anarede.dbarDF.loc[idx, "tipo"] = 1

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (anarede.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potencia reativa gerada maxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (anarede.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potencia reativa gerada minima
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
                    # Tratamento de limite de magnitude de tensao
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BMVA"]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ):
                    # Tratamento de limite de potencia reativa gerada maxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]
                    anarede.slackqlim = True

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ):
                    # Tratamento de limite de potencia reativa gerada minima
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
                    # Tratamento de backoff de magnitude de tensao
                    anarede.deltaQLIM[nger] += value["tensao"] * (1e-3)
                    anarede.deltaQLIM[nger] -= anarede.solution["voltage"][idx]
                    anarede.deltaQLIM[nger] *= anarede.cte["BMVA"]
                    anarede.slackqlim = False

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    >= value["potencia_reativa_maxima"]
                ) and (anarede.solution["voltage"][idx] <= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potencia reativa gerada maxima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_maxima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

                elif (
                    anarede.solution["qlim_reactive_generation"][idx]
                    <= value["potencia_reativa_minima"]
                ) and (anarede.solution["voltage"][idx] >= value["tensao"] * (1e-3)):
                    # Tratamento de limite de potencia reativa gerada minima
                    anarede.deltaQLIM[nger] += value["potencia_reativa_minima"]
                    anarede.deltaQLIM[nger] -= anarede.solution[
                        "qlim_reactive_generation"
                    ][idx]

            # Incrementa contador
            nger += 1

    # Residuo de equacao de controle
    anarede.deltaQLIM /= anarede.cte["BMVA"]
    anarede.deltaY = append(anarede.deltaY, anarede.deltaQLIM)


def qlimsubjac(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
    """
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    # Dimensao da matriz Jacobiana
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
    # Condicao
    if anarede.ctrldim != 0:
        anarede.extrarow = zeros([anarede.nger, anarede.ctrldim])
        anarede.extracol = zeros([anarede.ctrldim, anarede.nger])

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

    elif anarede.ctrldim == 0:
        ytv = csc_matrix(concatenate((anarede.yt, anarede.yv), axis=1))
        pqyx = csc_matrix(concatenate((anarede.px, anarede.qx, anarede.yx), axis=0))

    anarede.jacobian = vstack([anarede.jacobian, ytv], format="csc")
    anarede.jacobian = hstack([anarede.jacobian, pqyx], format="csc")


def qlimupdt(
    anarede,
):
    """atualizacao das variaveis de estado adicionais

    Args
        anarede:
    """
    # Contador
    nger = 0

    # Atualizacao da potencia reativa gerada
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            anarede.solution["qlim_reactive_generation"][idx] += (
                anarede.statevar[(anarede.dimpreqlim + nger)] * anarede.cte["BMVA"]
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
    """atualizacao do valor de potencia reativa especificada

    Args
        anarede:
    """
    # Variável
    anarede.qsch = zeros([anarede.nbus])

    # Atualizacao da potencia reativa especificada
    anarede.qsch += anarede.solution["qlim_reactive_generation"]
    anarede.qsch -= anarede.dbarDF["demanda_reativa"].to_numpy()
    anarede.qsch /= anarede.cte["BMVA"]


def qlimcorr(
    anarede,
    case,
):
    """atualizacao dos valores de potencia reativa gerada para a etapa de correcao do fluxo de potencia continuado

    Args
        anarede:
    """
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
    # Condição de geração de potência reativa ser superior ao valor máximo
    if any(
        (
            anarede.solution["qlim_reactive_generation"]
            > anarede.dbarDF["potencia_reativa_maxima"].to_numpy()
        ),
        where=~anarede.mask[(anarede.nbus) : (2 * anarede.nbus)],
    ):
        anarede.ctrlheur = True

    # Condicao de atingimento do ponto de maximo carregamento ou bifurcacao LIB
    if (
        (not anarede.solution["pmc"])
        and (anarede.solution["varstep"] == "lambda")
        and (
            (anarede.cte["LMBD"] * (5e-1 ** anarede.solution["ndiv"]))
            <= anarede.cte["ICMN"]
        )
    ):
        anarede.bifurcation = True
        # Condicao de curva completa do fluxo de potencia continuado
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
    pass
