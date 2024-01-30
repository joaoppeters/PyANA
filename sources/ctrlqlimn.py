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
    powerflow,
):
    '''variável de estado adicional para o problema de fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variáveis
    if 'qlim_reactive_generation' not in powerflow.solution:
        powerflow.solution['qlim_reactive_generation'] = zeros([powerflow.nbus])
        powerflow.maskQ = ones(powerflow.nbus, dtype=bool)

def qlimnres(
    powerflow,
    case,
):
    '''cálculo de resíduos das equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: caso analisado do fluxo de potência continuado (prev + corr)
    '''

    ## Inicialização
    # Vetor de resíduos
    powerflow.deltaQlim = zeros([powerflow.nger])

    # Contador
    nger = 0

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        if value['tipo'] != 0:
            qlimnsmooth(
                idx,
                powerflow,
                nger,
                case,
            )

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    powerflow.deltaY = append(
        powerflow.deltaY, powerflow.deltaQlim
    )

def qlimnsubjac(
    powerflow,
):
    '''submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    # Dimensão da matriz Jacobiana
    powerflow.dimpreqlim = deepcopy(powerflow.jacob.shape[0])

    # Submatrizes
    powerflow.px = zeros([powerflow.nbus, powerflow.nger])
    powerflow.qx = zeros([powerflow.nbus, powerflow.nger])
    powerflow.yx = zeros([powerflow.nger, powerflow.nger])
    powerflow.yt = zeros([powerflow.nger, powerflow.nbus])
    powerflow.yv = zeros([powerflow.nger, powerflow.nbus])

    # Contador
    nger = 0

    # Submatrizes QX YV YX
    for idx, value in powerflow.dbarraDF.iterrows():
        if value['tipo'] != 0:
            # dQg/dx
            powerflow.qx[idx, nger] = -1

            # Barras PV
            powerflow.yv[nger, idx] = powerflow.diffqlim[idx][0]
            # powerflow.yx[nger, nger] = 1E-10

            # Barras PQV
            if (
                powerflow.solution['qlim_reactive_generation'][idx]
                > value['potencia_reativa_maxima'] - powerflow.options['SIGQ']
            ) or (
                powerflow.solution['qlim_reactive_generation'][idx]
                < value['potencia_reativa_minima'] + powerflow.options['SIGQ']
            ):
                powerflow.yx[nger, nger] = powerflow.diffqlim[idx][1]

            # Incrementa contador
            nger += 1

    ## Montagem Jacobiana
    # Condição
    if powerflow.controldim != 0:
        powerflow.extrarow = zeros(
            [powerflow.nger, powerflow.controldim]
        )
        powerflow.extracol = zeros(
            [powerflow.controldim, powerflow.nger]
        )

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
        ytv = csc_matrix(
            concatenate((powerflow.yt, powerflow.yv), axis=1)
        )
        pqyx = csc_matrix(
            concatenate(
                (powerflow.px, powerflow.qx, powerflow.yx), axis=0
            )
        )

    powerflow.jacob = vstack([powerflow.jacob, ytv], format='csc')
    powerflow.jacob = hstack([powerflow.jacob, pqyx], format='csc')

def qlimnupdt(
    powerflow,
):
    '''atualização das variáveis de estado adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Contador
    nger = 0

    # Atualização da potência reativa gerada
    for idx, value in powerflow.dbarraDF.iterrows():
        if value['tipo'] != 0:
            powerflow.solution['qlim_reactive_generation'][idx] += (
                powerflow.statevar[(powerflow.dimpreqlim + nger)]
                * powerflow.options['BASE']
            )

            # Incrementa contador
            nger += 1

    qlimnsch(
        powerflow,
    )

def qlimnsch(
    powerflow,
):
    '''atualização do valor de potência reativa especificada

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variável
    powerflow.pqsch['potencia_reativa_especificada'] = zeros(
        [powerflow.nbus]
    )

    # Atualização da potência reativa especificada
    powerflow.pqsch['potencia_reativa_especificada'] += powerflow.solution[
        'qlim_reactive_generation'
    ]
    powerflow.pqsch[
        'potencia_reativa_especificada'
    ] -= powerflow.dbarraDF['demanda_reativa'].to_numpy()
    powerflow.pqsch[
        'potencia_reativa_especificada'
    ] /= powerflow.options['BASE']

def qlimncorr(
    powerflow,
    case,
):
    '''atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: etapa do fluxo de potência continuado analisada
    '''

    ## Inicialização
    # Variável
    powerflow.solution['qlim_reactive_generation'] = deepcopy(
        powerflow.point[case]['p']['qlim_reactive_generation']
    )

def qlimnheur(
    powerflow,
):
    '''heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Condição de geração de potência reativa ser superior ao valor máximo - analisa apenas para as barras de geração
    # powerflow.dbarraDF['potencia_reativa_maxima'].to_numpy()
    if any(
        (
            powerflow.solution['qlim_reactive_generation']
            > powerflow.dbarraDF['potencia_reativa_maxima'].to_numpy()
            - powerflow.options['SIGQ']
        ),
        where=~powerflow.mask[
            (powerflow.nbus) : (2 * powerflow.nbus)
        ],
    ):
        powerflow.controlheur = True

    # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
    if (
        (not powerflow.cpfsolution['pmc'])
        and (powerflow.cpfsolution['varstep'] == 'lambda')
        and (
            (
                powerflow.options['LMBD']
                * (5e-1 ** powerflow.cpfsolution['div'])
            )
            <= powerflow.options['ICMN']
        )
    ):
        powerflow.bifurcation = True
        # Condição de curva completa do fluxo de potência continuado
        if powerflow.options['FULL']:
            powerflow.dbarraDF[
                'true_potencia_reativa_minima'
            ] = powerflow.dbarraDF.loc[:, 'potencia_reativa_minima']
            for idx, value in powerflow.dbarraDF.iterrows():
                if (
                    powerflow.solution['qlim_reactive_generation'][idx]
                    > value['potencia_reativa_maxima']
                ) and (value['tipo'] != 0):
                    powerflow.dbarraDF.loc[
                        idx, 'potencia_reativa_minima'
                    ] = deepcopy(value['potencia_reativa_maxima'])

def qlimnpop(
    powerflow,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
            atua diretamente na variável de controle associada à opção de controle QLIMn

    Parâmetros
        powerflow: self do arquivo powerflow.py
        pop: quantidade de ações necessárias
    """

    ## Inicialização
    qlimspop(
        powerflow,
        pop=pop,
    )