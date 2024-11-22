# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, ones, zeros

from smooth import qlims, qlimssmooth, qlimspop


def qlimssol(
    powerflow,
):
    """variável de estado adicional para o problema de fluxo de potência

    Args
        powerflow:
    """

    ## Inicialização
    # Variáveis
    if "qlim_reactive_generation" not in powerflow.solution:
        powerflow.solution["qlim_reactive_generation"] = zeros([powerflow.nbus])
        powerflow.maskQ = ones(powerflow.nbus, dtype=bool)
        powerflow.mask = concatenate((powerflow.maskP, powerflow.maskQ), axis=0)

        powerflow.Y = dict()
        powerflow.qlimsch = dict()
        powerflow.qlimkeys = dict()
        powerflow.qlimdiff = dict()
        powerflow.qlimvar = dict()
        powerflow.diffyqg = dict()
        powerflow.diffyv = dict()

        if powerflow.method == "EXPC":
            powerflow.diffyqgqg = dict()
            powerflow.diffyvqg = dict()
            powerflow.diffyqgv = dict()
            powerflow.diffyvv = dict()

        # Inicialização sigmoides
        for idx, value in powerflow.dbarDF.iterrows():
            if value["tipo"] != 0:
                qlims(
                    powerflow,
                    idx,
                    value,
                )

        powerflow.mask = concatenate(
            (powerflow.mask, ones(powerflow.nger, dtype=bool)), axis=0
        )


def qlimsres(
    powerflow,
    case,
):
    """cálculo de resíduos das equações de controle adicionais

    Args
        powerflow:
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    # Vetor de resíduos
    powerflow.deltaQLIM = zeros([powerflow.nger])

    # Contador
    nger = 0

    # Loop
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            qlimssmooth(
                idx,
                powerflow,
                nger,
                case,
            )

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaQLIM)


def qlimssubjac(
    powerflow,
):
    """submatrizes da matriz jacobiana

    Args
        powerflow:
    """

    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    # Submatrizes
    px = zeros([powerflow.nbus, powerflow.nger])
    qx = zeros([powerflow.nbus, powerflow.nger])
    yx = zeros([powerflow.nger, powerflow.nger])
    yt = zeros([powerflow.nger, powerflow.nbus])
    yv = zeros([powerflow.nger, powerflow.nbus])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            # dQg/dx
            qx[idx, nger] = -1

            # Barras PV
            yv[nger, idx] = powerflow.qlimdiff[idx][0]

            # # Barras PQV
            # if (
            #     powerflow.solution["qlim_reactive_generation"][idx]
            #     > value["potencia_reativa_maxima"] - powerflow.options["SIGQ"]
            # ) or (
            #     powerflow.solution["qlim_reactive_generation"][idx]
            #     < value["potencia_reativa_minima"] + powerflow.options["SIGQ"]
            # ):
            yx[nger, nger] = powerflow.qlimdiff[idx][1]

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    if powerflow.controldim != 0:
        extrarow = zeros([powerflow.nger, powerflow.controldim])
        extracol = zeros([powerflow.controldim, powerflow.nger])

        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        yt[:, powerflow.maskP],
                        yv[:, powerflow.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        px[powerflow.maskP, :],
                        qx[powerflow.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif powerflow.controldim == 0:
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        yt[:, powerflow.maskP],
                        yv[:, powerflow.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        px[powerflow.maskP, :],
                        qx[powerflow.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def qlimsupdt(
    powerflow,
):
    """atualização das variáveis de estado adicionais

    Args
        powerflow:
    """

    ## Inicialização
    powerflow.dimpreqlim = powerflow.jacobian.shape[0] - powerflow.controldim

    # Contador
    nger = 0

    # Atualização da potência reativa gerada
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            powerflow.solution["qlim_reactive_generation"][idx] += powerflow.solution[
                "sign"
            ] * (
                powerflow.statevar[(powerflow.dimpreqlim + nger)]
                * powerflow.options["BASE"]
            )

            # Incrementa contador
            nger += 1

    qlimssch(
        powerflow,
    )


def qlimssch(
    powerflow,
):
    """atualização do valor de potência reativa especificada

    Args
        powerflow:
    """

    ## Inicialização
    # Variável
    powerflow.qsch = zeros([powerflow.nbus])

    # Atualização da potência reativa especificada
    powerflow.qsch += powerflow.solution["qlim_reactive_generation"]
    powerflow.qsch -= powerflow.dbarDF["demanda_reativa"].to_numpy()
    powerflow.qsch /= powerflow.options["BASE"]


def qlimscorr(
    powerflow,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Args
        powerflow:
        case: etapa do fluxo de potência continuado analisada
    """

    ## Inicialização
    # Variável
    powerflow.solution["qlim_reactive_generation"] = deepcopy(
        powerflow.operationpoint[case]["p"]["qlim_reactive_generation"]
    )


def qlimsheur(
    powerflow,
):
    """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

    Args
        powerflow:
    """

    ## Inicialização
    # Condição de geração de potência reativa ser superior ao valor máximo - analisa apenas para as barras de geração
    # powerflow.dbarDF['potencia_reativa_maxima'].to_numpy()
    if any(
        (
            powerflow.solution["qlim_reactive_generation"]
            > powerflow.dbarDF["potencia_reativa_maxima"].to_numpy()
            - powerflow.options["SIGQ"]
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
                ) and (value["tipo"] != 0):
                    powerflow.dbarDF.loc[idx, "potencia_reativa_minima"] = deepcopy(
                        value["potencia_reativa_maxima"]
                    )


def qlimspop(
    powerflow,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
            atua diretamente na variável de controle associada à opção de controle QLIMs

    Args
        powerflow:
        pop: quantidade de ações necessárias
    """

    ## Inicialização
    qlimspop(
        powerflow,
        pop=pop,
    )


def qlimscpf(
    powerflow,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        powerflow:
    """

    ## Inicialização
    powerflow.solution["qlim_reactive_generation"] = deepcopy(
        powerflow.solution["qlim_reactive_generation"]
    )


def qlimssolcpf(
    powerflow,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        powerflow:
        case: etapa do fluxo de potência continuado analisada
    """

    ## Inicialização
    # Condição
    precase = case - 1
    if case == 1:
        powerflow.solution["qlim_reactive_generation"] = deepcopy(
            powerflow.operationpoint[precase]["qlim_reactive_generation"]
        )

    elif case > 1:
        powerflow.solution["qlim_reactive_generation"] = deepcopy(
            powerflow.operationpoint[precase]["p"]["qlim_reactive_generation"]
        )


def qlimssubhess(
    powerflow,
):
    """submatrizes da matriz hessiana

    Args
        powerflow:
    """

    ## Inicialização
    # hessiana - LEMBRANDO QUE A MATRIZ HESSIANA É CONSTRUÍDA COM A *TRANSPOSTA* DA JACOBIANA
    #
    #   H     M   yt
    #   N     L   yv
    #  px    qx   yx
    #

    # Submatrizes
    px = zeros([powerflow.nger, powerflow.nbus])
    qx = zeros([powerflow.nger, powerflow.nbus])
    yx = zeros([powerflow.nger, powerflow.nger])
    yt = zeros([powerflow.nbus, powerflow.nger])
    yv = zeros([powerflow.nbus, powerflow.nger])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            powerflow.hessian[powerflow.Tval + idx, powerflow.Tval + idx] -= (
                powerflow.qlimdiff[idx][2]
                * powerflow.solution["eigen"][2 * powerflow.nbus + nger]
            )
            yv[idx, nger] = -(
                powerflow.qlimdiff[idx][3]
                * powerflow.solution["eigen"][2 * powerflow.nbus + nger]
            )

            # # Barras PQV
            # if (
            #     powerflow.solution["qlim_reactive_generation"][idx]
            #     > value["potencia_reativa_maxima"] - powerflow.options["SIGQ"]
            # ) or (
            #     powerflow.solution["qlim_reactive_generation"][idx]
            #     < value["potencia_reativa_minima"] + powerflow.options["SIGQ"]
            # ):
            qx[nger, idx] = -(
                powerflow.qlimdiff[idx][4]
                * powerflow.solution["eigen"][2 * powerflow.nbus + nger]
            )
            yx[nger, nger] = -(
                powerflow.qlimdiff[idx][5]
                * powerflow.solution["eigen"][2 * powerflow.nbus + nger]
            )

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    if powerflow.controldim != 0:
        extrarow = zeros([powerflow.nger, powerflow.controldim])
        extracol = zeros([powerflow.controldim, powerflow.nger])
        powerflow.hessian = concatenate(
            (
                powerflow.hessian,
                concatenate(
                    (
                        px[:, powerflow.maskP],
                        qx[:, powerflow.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.hessian = concatenate(
            (
                powerflow.hessian,
                concatenate(
                    (
                        yt[powerflow.maskP, :],
                        yv[powerflow.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif powerflow.controldim == 0:
        powerflow.hessian = concatenate(
            (
                powerflow.hessian,
                concatenate(
                    (
                        px[:, powerflow.maskP],
                        qx[:, powerflow.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.hessian = concatenate(
            (
                powerflow.hessian,
                concatenate(
                    (
                        yt[powerflow.maskP, :],
                        yv[powerflow.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )
