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
    sqrt,
    sum,
    zeros,
)
from numpy.linalg import solve

from calc import pcalc, qcalc
from ctrl import controlupdt, controlres, controlsol, controlsch
from hessian import hessian
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
    powerflow.hessvar = dict()
    powerflow.solution = {
        "system": powerflow.name,
        "iter": 0,
        "voltage": array(powerflow.dbarraDF["tensao"] * 1e-3),
        "theta": array(radians(powerflow.dbarraDF["angulo"])),
        "active": zeros(powerflow.nbus),
        "reactive": zeros(powerflow.nbus),
        "freq": 1.0,
        "lambda": 0.0,
        "potencia_ativa": deepcopy(powerflow.dbarraDF["potencia_ativa"]),
        "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
        "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
        "eigen": 1.0 * (powerflow.mask),
    }

    # Controles
    controlsol(
        powerflow,
    )

    while True:
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

        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Vetor Jacobiana-Lambda    
        powerflow.G = powerflow.jacob.A.T @ powerflow.solution["eigen"]
        powerflow.G = powerflow.G.reshape((powerflow.G.shape[0], 1))

        # Matriz Hessiana
        hessian(
            powerflow,
        )

        # expansao total
        expansion(
            powerflow,
        )
        
        powerflow.canistate = concatenate(
        (
            powerflow.solution["theta"],
            powerflow.solution["voltage"],
            array([powerflow.solution["lambda"]]),
            powerflow.solution["eigen"],
        ),
        axis=0,
    )

        powerflow.funccani = concatenate(
            (
                -powerflow.deltaPQY,
                powerflow.G.reshape(powerflow.G.shape[0],),
                array([sum(powerflow.H.T * powerflow.H) - 1]),
            ),
            axis=0,
        ).astype(float)

        # Variáveis de estado
        powerflow.statevar = solve(powerflow.jaccani, powerflow.funccani)

        # Atualização das Variáveis de estado
        update_statevar(
            powerflow,
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        norm = sqrt(sum(powerflow.statevar ** 2))
        print(norm)

        # Condição de Divergência por iterações
        if  (norm > powerflow.options["CTOL"]) and (powerflow.solution["iter"] > powerflow.options["ACIT"]):
            powerflow.solution[
                "convergence"
            ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

        elif (norm <= powerflow.options["CTOL"]) and (
            powerflow.solution["iter"] <= powerflow.options["ACIT"]
        ):
            powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"
            break


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
    for idxbar, _ in powerflow.dbarraDF.iterrows():
        # Incremento de Carregamento
        powerflow.dbarraDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
            "demanda_ativa"
        ][idxbar] * (1 + powerflow.solution["lambda"])
        powerflow.dbarraDF.at[idxbar, "demanda_reativa"] = powerflow.solution[
            "demanda_reativa"
        ][idxbar] * (1 + powerflow.solution["lambda"])

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
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    thetavalues = sum(powerflow.maskP)
    voltagevalues = sum(powerflow.maskQ)

    # configuração reduzida
    powerflow.solution["theta"][powerflow.maskP] -= powerflow.statevar[0:(thetavalues)]
    powerflow.solution["voltage"][powerflow.maskQ] -= powerflow.statevar[
        (thetavalues) : (thetavalues + voltagevalues)
    ]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    powerflow.solution["lambda"] -= powerflow.statevar[
        (thetavalues + voltagevalues + powerflow.controldim)
    ]
    powerflow.solution["eigen"][powerflow.mask] -= powerflow.statevar[
        (thetavalues + voltagevalues + powerflow.controldim + 1) :
    ]


def expansion(
    powerflow,
):
    """expansão da matriz jacobiana para o método continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtf = zeros([powerflow.jacob.A.shape[0], 1])

    # Demanda
    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 2:
            powerflow.dtf[idx, 0] = (
                powerflow.solution["demanda_ativa"][idx]
                - powerflow.solution["potencia_ativa"][idx]
            )
            if value["tipo"] == 0:
                powerflow.dtf[(idx + powerflow.nbus), 0] = powerflow.solution[
                    "demanda_reativa"
                ][idx]

    powerflow.dtf /= powerflow.options["BASE"]

    # reducao total
    reduction(
        powerflow,
    )

    powerflow.jaccani = concatenate(
        (powerflow.jacobian, powerflow.dtf, powerflow.dwf),
        axis=1,
    )

    powerflow.jaccani = concatenate(
        (
            powerflow.jaccani,
            concatenate(
                (powerflow.hessian, powerflow.dtg, powerflow.jacobian.T),
                axis=1,
            ),
        ),
        axis=0,
    )

    powerflow.jaccani = concatenate(
        (
            powerflow.jaccani,
            concatenate(
                (powerflow.dxh, array([0]), powerflow.dwh),
                axis=0,
            ).reshape((1, powerflow.jaccani.shape[1])),
        ),
        axis=0,
    )


def reduction(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.deltaPQY = powerflow.deltaPQY[powerflow.mask]
    powerflow.G = powerflow.G[powerflow.mask]
    powerflow.H = powerflow.solution["eigen"][powerflow.mask]

    powerflow.jacobian = powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask]
    powerflow.dtf = powerflow.dtf[powerflow.mask]
    powerflow.dwf = zeros((powerflow.mask.shape[0], powerflow.mask.shape[0]))[
        powerflow.mask, :
    ][:, powerflow.mask]

    powerflow.hessian = powerflow.hessian[powerflow.mask, :][:, powerflow.mask]
    powerflow.dtg = zeros((powerflow.mask.shape[0], 1))[powerflow.mask]

    powerflow.dxh = zeros((1, powerflow.mask.shape[0]))[0, powerflow.mask]
    powerflow.dwh = 2 * ones((1, powerflow.mask.shape[0]))[0, powerflow.mask]
