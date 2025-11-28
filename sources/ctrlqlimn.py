# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, ones, zeros
from scipy.sparse import csc_matrix, hstack, vstack

from smooth import qlimnsmooth, qlimspop


def qlimnsol(
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


def qlimnres(
    anarede,
    case,
):
    """cálculo de resíduos das equações de controle adicionais

    Args
        anarede:
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    # Vetor de resíduos
    anarede.deltaQLIM = zeros([anarede.nger])

    # Contador
    nger = 0

    # Loop
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            qlimnsmooth(
                idx,
                anarede,
                nger,
                case,
            )

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    anarede.deltaY = append(anarede.deltaY, anarede.deltaQLIM)


def qlimnsubjac(
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

            # Barras PV
            anarede.yv[nger, idx] = anarede.qlimdiff[idx][0]
            # anarede.yx[nger, nger] = 1E-10

            # Barras PQV
            if (
                anarede.solution["qlim_reactive_generation"][idx]
                > value["potencia_reativa_maxima"] - anarede.cte["SIGQ"]
            ) or (
                anarede.solution["qlim_reactive_generation"][idx]
                < value["potencia_reativa_minima"] + anarede.cte["SIGQ"]
            ):
                anarede.yx[nger, nger] = anarede.qlimdiff[idx][1]

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


def qlimnupdt(
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

            # Incrementa contador
            nger += 1

    qlimnsch(
        anarede,
    )


def qlimnsch(
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


def qlimncorr(
    anarede,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
        case: etapa do fluxo de potência continuado analisada
    """
    ## Inicialização
    # Variável
    anarede.solution["qlim_reactive_generation"] = deepcopy(
        anarede.operationpoint[case]["p"]["qlim_reactive_generation"]
    )


def qlimnheur(
    anarede,
):
    """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Condição de geração de potência reativa ser superior ao valor máximo - analisa apenas para as barras de geração
    # anarede.dbarDF['potencia_reativa_maxima'].to_numpy()
    if any(
        (
            anarede.solution["qlim_reactive_generation"]
            > anarede.dbarDF["potencia_reativa_maxima"].to_numpy() - anarede.cte["SIGQ"]
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
                ) and (value["tipo"] != 0):
                    anarede.dbarDF.loc[idx, "potencia_reativa_minima"] = deepcopy(
                        value["potencia_reativa_maxima"]
                    )


def qlimnpop(
    anarede,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
            atua diretamente na variável de controle associada à opção de controle QLIMn

    Args
        anarede:
        pop: quantidade de ações necessárias
    """
    ## Inicialização
    qlimspop(
        anarede,
        pop=pop,
    )


def qlimnsubhess(
    anarede,
):
    """submatrizes da matriz hessiana

    Args
        anarede:
    """
    ## Inicialização
    #
    # hessiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    pass


def qlimnsubjacsym(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização

    pass
