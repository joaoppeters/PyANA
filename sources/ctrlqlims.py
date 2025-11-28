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

        anarede.Y = dict()
        anarede.qlimsch = dict()
        anarede.qlimkeys = dict()
        anarede.qlimdiff = dict()
        anarede.qlimvar = dict()
        anarede.diffyqg = dict()
        anarede.diffyv = dict()

        if anarede.method == "EXPC":
            anarede.diffyqgqg = dict()
            anarede.diffyvqg = dict()
            anarede.diffyqgv = dict()
            anarede.diffyvv = dict()

        # Inicialização sigmoides
        for idx, value in anarede.dbarDF.iterrows():
            if value["tipo"] != 0:
                qlims(
                    anarede,
                    idx,
                    value,
                )

        anarede.mask = concatenate(
            (anarede.mask, ones(anarede.nger, dtype=bool)), axis=0
        )


def qlimsres(
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
            qlimssmooth(
                idx,
                anarede,
                nger,
                case,
            )

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    anarede.deltaY = append(anarede.deltaY, anarede.deltaQLIM)


def qlimssubjac(
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

    # Submatrizes
    px = zeros([anarede.nbus, anarede.nger])
    qx = zeros([anarede.nbus, anarede.nger])
    yx = zeros([anarede.nger, anarede.nger])
    yt = zeros([anarede.nger, anarede.nbus])
    yv = zeros([anarede.nger, anarede.nbus])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # dQg/dx
            qx[idx, nger] = -1

            # Barras PV
            yv[nger, idx] = anarede.qlimdiff[idx][0]

            # # Barras PQV
            # if (
            #     anarede.solution["qlim_reactive_generation"][idx]
            #     > value["potencia_reativa_maxima"] - anarede.cte["SIGQ"]
            # ) or (
            #     anarede.solution["qlim_reactive_generation"][idx]
            #     < value["potencia_reativa_minima"] + anarede.cte["SIGQ"]
            # ):
            yx[nger, nger] = anarede.qlimdiff[idx][1]

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    if anarede.controldim != 0:
        extrarow = zeros([anarede.nger, anarede.controldim])
        extracol = zeros([anarede.controldim, anarede.nger])

        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        yt[:, anarede.maskP],
                        yv[:, anarede.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        px[anarede.maskP, :],
                        qx[anarede.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif anarede.controldim == 0:
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        yt[:, anarede.maskP],
                        yv[:, anarede.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        px[anarede.maskP, :],
                        qx[anarede.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def qlimsupdt(
    anarede,
):
    """atualização das variáveis de estado adicionais

    Args
        anarede:
    """
    ## Inicialização
    anarede.dimpreqlim = anarede.jacobian.shape[0] - anarede.controldim

    # Contador
    nger = 0

    # Atualização da potência reativa gerada
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            anarede.solution["qlim_reactive_generation"][idx] += anarede.solution[
                "sign"
            ] * (anarede.statevar[(anarede.dimpreqlim + nger)] * anarede.cte["BASE"])

            # Incrementa contador
            nger += 1

    qlimssch(
        anarede,
    )


def qlimssch(
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


def qlimscorr(
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


def qlimsheur(
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


def qlimspop(
    anarede,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
            atua diretamente na variável de controle associada à opção de controle QLIMs

    Args
        anarede:
        pop: quantidade de ações necessárias
    """
    ## Inicialização
    qlimspop(
        anarede,
        pop=pop,
    )


def qlimscpf(
    anarede,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    anarede.solution["qlim_reactive_generation"] = deepcopy(
        anarede.solution["qlim_reactive_generation"]
    )


def qlimssolcpf(
    anarede,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
        case: etapa do fluxo de potência continuado analisada
    """
    ## Inicialização
    # Condição
    precase = case - 1
    if case == 1:
        anarede.solution["qlim_reactive_generation"] = deepcopy(
            anarede.operationpoint[precase]["qlim_reactive_generation"]
        )

    elif case > 1:
        anarede.solution["qlim_reactive_generation"] = deepcopy(
            anarede.operationpoint[precase]["p"]["qlim_reactive_generation"]
        )


def qlimssubhess(
    anarede,
):
    """submatrizes da matriz hessiana

    Args
        anarede:
    """
    ## Inicialização
    # hessiana - LEMBRANDO QUE A MATRIZ HESSIANA É CONSTRUÍDA COM A *TRANSPOSTA* DA JACOBIANA
    #
    #   H     M   yt
    #   N     L   yv
    #  px    qx   yx
    #

    # Submatrizes
    px = zeros([anarede.nger, anarede.nbus])
    qx = zeros([anarede.nger, anarede.nbus])
    yx = zeros([anarede.nger, anarede.nger])
    yt = zeros([anarede.nbus, anarede.nger])
    yv = zeros([anarede.nbus, anarede.nger])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            anarede.hessian[anarede.Tval + idx, anarede.Tval + idx] -= (
                anarede.qlimdiff[idx][2]
                * anarede.solution["eigen"][2 * anarede.nbus + nger]
            )
            yv[idx, nger] = -(
                anarede.qlimdiff[idx][3]
                * anarede.solution["eigen"][2 * anarede.nbus + nger]
            )

            # # Barras PQV
            # if (
            #     anarede.solution["qlim_reactive_generation"][idx]
            #     > value["potencia_reativa_maxima"] - anarede.cte["SIGQ"]
            # ) or (
            #     anarede.solution["qlim_reactive_generation"][idx]
            #     < value["potencia_reativa_minima"] + anarede.cte["SIGQ"]
            # ):
            qx[nger, idx] = -(
                anarede.qlimdiff[idx][4]
                * anarede.solution["eigen"][2 * anarede.nbus + nger]
            )
            yx[nger, nger] = -(
                anarede.qlimdiff[idx][5]
                * anarede.solution["eigen"][2 * anarede.nbus + nger]
            )

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    if anarede.controldim != 0:
        extrarow = zeros([anarede.nger, anarede.controldim])
        extracol = zeros([anarede.controldim, anarede.nger])
        anarede.hessian = concatenate(
            (
                anarede.hessian,
                concatenate(
                    (
                        px[:, anarede.maskP],
                        qx[:, anarede.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.hessian = concatenate(
            (
                anarede.hessian,
                concatenate(
                    (
                        yt[anarede.maskP, :],
                        yv[anarede.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif anarede.controldim == 0:
        anarede.hessian = concatenate(
            (
                anarede.hessian,
                concatenate(
                    (
                        px[:, anarede.maskP],
                        qx[:, anarede.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.hessian = concatenate(
            (
                anarede.hessian,
                concatenate(
                    (
                        yt[anarede.maskP, :],
                        yv[anarede.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )
