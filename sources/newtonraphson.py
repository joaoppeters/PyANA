# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import (
    array,
    radians,
    zeros,
)
from numpy.linalg import norm
from scipy.sparse.linalg import spsolve

from convergence import convergence
from ctrl import controlsol, controldelta
from jacobian import jacobi
from lineflow import lineflow
from residue import residue
from scheduled import scheduled
from statevar import update


def newton(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

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
        "active_flow_F2": zeros(powerflow.nlin),
        "reactive_flow_F2": zeros(powerflow.nlin),
        "active_flow_2F": zeros(powerflow.nlin),
        "reactive_flow_2F": zeros(powerflow.nlin),
    }

    # Controles
    controlsol(
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

    while (
        norm(powerflow.deltaP) > powerflow.options["TEPA"]
        or norm(powerflow.deltaQ) > powerflow.options["TEPR"]
        or controldelta(powerflow,)
    ):

        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição Divergência por iterações
        if powerflow.solution["iter"] > powerflow.options["ACIT"]:
            powerflow.solution[
                "convergence"
            ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

    # Iteração Adicional
    if powerflow.solution["iter"] <= powerflow.options["ACIT"]:
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
        )

        # Fluxo em linhas de transmissão
        lineflow(
            powerflow,
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"