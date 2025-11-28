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
    anarede,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Args
        anarede:
    """
    ## Inicialização
    # Variável para armazenamento de solução
    anarede.controlcount = 0
    anarede.solution = {
        "method": "LFDC",
        "system": anarede.name,
        "iter": 1,
        "voltage": ones(anarede.nbus),
        "theta": zeros(anarede.nbus),
        "active": zeros(anarede.nbus),
        "reactive": zeros(anarede.nbus),
        "freq": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": zeros([]),
        "busQ": zeros([]),
    }

    # Variáveis Especificadas
    scheduled(
        anarede,
    )

    # Resíduos
    residue(
        anarede,
    )

    # Armazenamento da trajetória de convergência
    convergence(
        anarede,
    )

    # Matriz B
    Ybus = anarede.Yb.A.imag
    Ybus[anarede.slackidx, :] = 0
    Ybus[:, anarede.slackidx] = 0
    Ybus[anarede.slackidx, anarede.slackidx] = 1

    # Variáveis de estado
    anarede.statevar = solve(-Ybus, anarede.psch)

    # Atualização das Variáveis de estado
    updtlinear(
        anarede,
    )

    # Convergência
    anarede.solution["convergence"] = "SISTEMA CONVERGENTE"


def residue(
    anarede,
):
    """cálculo de resíduos das equações diferenciáveis"""

    ## Inicialização
    # Vetores de resíduo
    anarede.deltaP = zeros(anarede.nbus)
    anarede.deltaQ = zeros(anarede.nbus)


def convergence(
    anarede,
):
    """armazenamento da trajetória de convergência do processo de solução do fluxo de potência

    Args
        anarede:
    """
    ## Inicialização
    # Trajetória de convergência da frequência
    anarede.solution["freq"] = append(anarede.solution["freq"], 0.0)

    # Trajetória de convergência da potência ativa
    anarede.solution["convP"] = append(anarede.solution["convP"], 0.0)
    anarede.solution["busP"] = append(anarede.solution["busP"], 0)

    # Trajetória de convergência da potência reativa
    anarede.solution["convQ"] = append(anarede.solution["convQ"], 0.0)
    anarede.solution["busQ"] = append(anarede.solution["busQ"], 0)
