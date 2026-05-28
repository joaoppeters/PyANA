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
    """analise do fluxo de potencia nao-linear em regime permanente de SEP via metodo Newton-Raphson

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
    # Variavel para armazenamento de solucao
=======
    # Variável para armazenamento de solução
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.ctrlcount = 0
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

    # Variaveis Especificadas
    scheduled(
        anarede,
    )

    # Residuos
    residue(
        anarede,
    )

    # Armazenamento da trajetoria de convergencia
    convergence(
        anarede,
    )

    # Matriz B
    Ybus = anarede.Yb.A.imag
    Ybus[anarede.slackidx, :] = 0
    Ybus[:, anarede.slackidx] = 0
    Ybus[anarede.slackidx, anarede.slackidx] = 1

    # Variaveis de estado
    anarede.statevar = solve(-Ybus, anarede.psch)

    # Atualizacao das Variaveis de estado
    updtlinear(
        anarede,
    )

    # Convergencia
    anarede.solution["convergence"] = "SISTEMA CONVERGENTE"


def residue(
    anarede,
):
    """calculo de residuos das equacoes diferenciaveis"""

<<<<<<< HEAD
    ## Inicializacao
    # Vetores de residuo
=======
    # Vetores de resíduo
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.deltaP = zeros(anarede.nbus)
    anarede.deltaQ = zeros(anarede.nbus)


def convergence(
    anarede,
):
    """armazenamento da trajetoria de convergencia do processo de solucao do fluxo de potencia

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
    # Trajetoria de convergencia da frequencia
=======
    # Trajetória de convergência da frequência
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.solution["freq"] = append(anarede.solution["freq"], 0.0)

    # Trajetoria de convergencia da potencia ativa
    anarede.solution["convP"] = append(anarede.solution["convP"], 0.0)
    anarede.solution["busP"] = append(anarede.solution["busP"], 0)

    # Trajetoria de convergencia da potencia reativa
    anarede.solution["convQ"] = append(anarede.solution["convQ"], 0.0)
    anarede.solution["busQ"] = append(anarede.solution["busQ"], 0)
