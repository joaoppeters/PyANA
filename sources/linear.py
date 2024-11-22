# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import append, array, ones, zeros
from numpy.linalg import solve

from scheduled import scheduled
from update import updtlinear


def linear(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Args
        powerflow:
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.controlcount = 0
    powerflow.solution = {
        "method": "LFDC",
        "system": powerflow.name,
        "iter": 1,
        "voltage": ones(powerflow.nbus),
        "theta": zeros(powerflow.nbus),
        "active": zeros(powerflow.nbus),
        "reactive": zeros(powerflow.nbus),
        "freq": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": zeros([]),
        "busQ": zeros([]),
    }

    # Variáveis Especificadas
    scheduled(
        powerflow,
    )

    # Resíduos
    residue(
        powerflow,
    )

    # Armazenamento da trajetória de convergência
    convergence(
        powerflow,
    )

    # Matriz B
    Ybus = powerflow.Yb.A.imag
    Ybus[powerflow.slackidx, :] = 0
    Ybus[:, powerflow.slackidx] = 0
    Ybus[powerflow.slackidx, powerflow.slackidx] = 1

    # Variáveis de estado
    powerflow.statevar = solve(-Ybus, powerflow.psch)

    # Atualização das Variáveis de estado
    updtlinear(
        powerflow,
    )

    # Convergência
    powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"


def residue(
    powerflow,
):
    """cálculo de resíduos das equações diferenciáveis"""

    ## Inicialização
    # Vetores de resíduo
    powerflow.deltaP = zeros(powerflow.nbus)
    powerflow.deltaQ = zeros(powerflow.nbus)


def convergence(
    powerflow,
):
    """armazenamento da trajetória de convergência do processo de solução do fluxo de potência

    Args
        powerflow:
    """

    ## Inicialização
    # Trajetória de convergência da frequência
    powerflow.solution["freq"] = append(powerflow.solution["freq"], 0.0)

    # Trajetória de convergência da potência ativa
    powerflow.solution["convP"] = append(powerflow.solution["convP"], 0.0)
    powerflow.solution["busP"] = append(powerflow.solution["busP"], 0)

    # Trajetória de convergência da potência reativa
    powerflow.solution["convQ"] = append(powerflow.solution["convQ"], 0.0)
    powerflow.solution["busQ"] = append(powerflow.solution["busQ"], 0)
