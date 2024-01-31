# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    array,
    concatenate,
    ones,
    radians,
    sum,
    zeros,
)
from numpy.linalg import inv, norm, solve

from calc import pcalc, qcalc
from ctrl import controlupdt, controlres, controlsol, controlsch
from hessian import *
from jacobian import jacobi


def cani(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution = {
        "system": powerflow.name,
        "iter": 0,
        "voltage": array(powerflow.dbarraDF["tensao"] * 1e-3),
        "theta": array(radians(powerflow.dbarraDF["angulo"])),
        "active": zeros(powerflow.nbus),
        "reactive": zeros(powerflow.nbus),
        "freq": 1.0,
        "freqiter": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": array([]),
        "busQ": array([]),
        "convY": array([]),
        "busY": array([]),
        "step": 0.0,
        "stepsch": 0.0,
        "potencia_ativa": deepcopy(powerflow.dbarraDF["potencia_ativa"]),
        "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
        "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
        "eigen": ones(2*powerflow.nbus),
    }

    # Controles
    controlsol(
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
        powerflow,
    )

    powerflow.canistate = concatenate((powerflow.solution['theta'], powerflow.solution['voltage'], array([powerflow.solution['stepsch']]), powerflow.solution['eigen']), axis=0)
    keys = hessian_init2(powerflow,)
    var = dict(zip(keys, powerflow.canistate))

    while (norm(powerflow.canistate) > powerflow.options["CTOL"]):
        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Matriz Hessiana
        hessian2(
            powerflow,
            var,
            keys,
        )

        # expansao total
        expansion(
            powerflow,
        )

        powerflow.canifunctions = concatenate((powerflow.deltaPQY, powerflow.dxfw, array([sum(powerflow.solution['eigen'].T*powerflow.solution['eigen']) - 1])), axis=0).astype(float)

        # Variáveis de estado
        powerflow.statevar = solve(
            powerflow.jaccani, powerflow.canifunctions
        )

        # Atualização das Variáveis de estado
        var = update_statevar(
            powerflow,
            keys,
        )

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
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição de Divergência por iterações
        if (powerflow.solution["iter"] > powerflow.options["ACIT"]):
            powerflow.solution["convergence"] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

    print()


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
    for idxbar,_ in powerflow.dbarraDF.iterrows():
        # Incremento de Carregamento
        powerflow.dbarraDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
            "demanda_ativa"
        ][idxbar] * (1 + powerflow.solution["stepsch"])
        powerflow.dbarraDF.at[
            idxbar, "demanda_reativa"
        ] = powerflow.solution["demanda_reativa"][idxbar] * (
            1 + powerflow.solution["stepsch"]
        )

    deltaincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - preincrement

    # Incremento de geração
    if powerflow.codes["DGER"]:
        for _, valueger in powerflow.dgeraDF.iterrows():
            idx = valueger["numero"] - 1
            powerflow.dbarraDF.at[idx, "potencia_ativa"] = powerflow.dbarraDF[
                "potencia_ativa"
            ][idx] + (deltaincrement * valueger["fator_participacao"])

        powerflow.solution["potencia_ativa"] = deepcopy(
            powerflow.dbarraDF["potencia_ativa"]
        )


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
        powerflow.pqsch["potencia_ativa_especificada"][idx] += value["potencia_ativa"]
        powerflow.pqsch["potencia_ativa_especificada"][idx] -= value["demanda_ativa"]

        # Potência reativa especificada
        powerflow.pqsch["potencia_reativa_especificada"][idx] += value[
            "potencia_reativa"
        ]
        powerflow.pqsch["potencia_reativa_especificada"][idx] -= value[
            "demanda_reativa"
        ]

    # Tratamento
    powerflow.pqsch["potencia_ativa_especificada"] /= powerflow.options["BASE"]
    powerflow.pqsch["potencia_reativa_especificada"] /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0:
        controlsch(
            powerflow,
        )


def residue(
    powerflow,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    powerflow.deltaP = zeros(powerflow.nbus)
    powerflow.deltaQ = zeros(powerflow.nbus)

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Tipo PV ou PQ - Resíduo Potência Ativa
        if value["tipo"] != 2:
            powerflow.deltaP[idx] += powerflow.pqsch["potencia_ativa_especificada"][idx]
            powerflow.deltaP[idx] -= pcalc(
                powerflow,
                idx,
            )

        # Tipo PQ - Resíduo Potência Reativa
        if (
            ("QLIM" in powerflow.control)
            or ("QLIMs" in powerflow.control)
            or ("QLIMn" in powerflow.control)
            or (value["tipo"] == 0)
        ):
            powerflow.deltaQ[idx] += powerflow.pqsch["potencia_reativa_especificada"][
                idx
            ]
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
        )
        concatresidue(
            powerflow,
        )
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)
    else:
        powerflow.deltaY = array([0])


def concatresidue(
    powerflow,
):
    """concatenação de resíduos de potências ativa e reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)


def update_statevar(
    powerflow,
    keys,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.solution["theta"] += powerflow.statevar[0 : (powerflow.nbus)]
    powerflow.solution["voltage"] += powerflow.statevar[
        (powerflow.nbus) : (2 * powerflow.nbus)
    ]
    powerflow.solution["stepsch"] += powerflow.statevar[(2 * powerflow.nbus)]
    powerflow.solution["eigen"] += powerflow.statevar[(2 * powerflow.nbus)+1 : (6 * powerflow.nbus)+1]
    
    powerflow.canistate = concatenate((powerflow.solution['theta'], powerflow.solution['voltage'], array([powerflow.solution['stepsch']]), powerflow.solution['eigen']), axis=0)
    
    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    return dict(zip(keys, powerflow.canistate))


def expansion(
    powerflow,
):
    """expansão da matriz jacobiana para o método continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.jacobA = deepcopy(powerflow.jacob.A)
    # Arrays adicionais
    colarray = zeros([2*powerflow.nbus, 1])
    
    # Demanda
    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 2:
            colarray[idx, 0] = (
                powerflow.solution["demanda_ativa"][idx]
                - powerflow.solution["potencia_ativa"][idx]
            )
            if value["tipo"] == 0:
                colarray[(idx + powerflow.nbus), 0] = powerflow.solution[
                    "demanda_reativa"
                ][idx]

        if (powerflow.maskP[idx] == False):
            powerflow.jacobA[idx, :] = 0
            powerflow.jacobA[:, idx] = 0
            powerflow.jacobA[idx, idx] = 1
            powerflow.hessian[idx, :] = 0
            powerflow.hessian[:, idx] = 0
            powerflow.hessian[idx, idx] = 1
        
        if (powerflow.maskQ[idx] == False) and (('QLIM' not in powerflow.control) or ('QLIMs' not in powerflow.control)):
            powerflow.jacobA[idx+powerflow.nbus, :] = 0
            powerflow.jacobA[:, idx+powerflow.nbus] = 0
            powerflow.jacobA[idx+powerflow.nbus, idx+powerflow.nbus] = 1
            powerflow.hessian[idx+powerflow.nbus, :] = 0
            powerflow.hessian[:, idx+powerflow.nbus] = 0
            powerflow.hessian[idx+powerflow.nbus, idx+powerflow.nbus] = 1

    colarray /= powerflow.options["BASE"]
    
    powerflow.jaccani = concatenate(
        (powerflow.jacobA, colarray, zeros((2*powerflow.nbus, 2*powerflow.nbus))), axis=1,
    )

    powerflow.jaccani = concatenate(
        (powerflow.jaccani, concatenate(
            (powerflow.hessian, zeros((2*powerflow.nbus, 1)), powerflow.jacobA), axis=1,
        )), axis=0,
    )

    powerflow.jaccani = concatenate(
        (powerflow.jaccani, concatenate(
            (zeros((1, 2*powerflow.nbus)), zeros((1, 1)), 2*ones((1, 2*powerflow.nbus))), axis=1,
        )), axis=0,
    )