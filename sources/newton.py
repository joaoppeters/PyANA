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
from numpy.linalg import lstsq, norm

from convergence import convergence
from ctrl import ctrlsol, ctrldelta
from matrices import matrices
from residue import residue
from scheduled import scheduled
from update import updtpwr, updtstt


def newton(
    anarede,
):
    """analise do fluxo de potencia nao-linear em regime permanente de SEP via metodo Newton-Raphson

    Args
        anarede:
    """
    ## Inicializacao
    # Variavel para armazenamento de solucao
    anarede.solution = {
        "system": anarede.name,
        "method": "EXLF",
        "iter": 0,
        "voltage": array(anarede.dbarDF["tensao"] * 1e-3),
        "theta": array(radians(anarede.dbarDF["angulo"])),
        "active": zeros(anarede.nbus),
        "reactive": zeros(anarede.nbus),
        "freq": 1.0,
        "freqiter": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": array([]),
        "busQ": array([]),
        "convY": array([]),
        "busY": array([]),
        "sign": 1.0,
    }

    # Controles
    ctrlsol(
        anarede,
    )

    # Variaveis Especificadas
    scheduled(
        anarede,
    )

    # Residuos
    residue(
        anarede,
    )

    while (
        norm(
            anarede.deltaP[anarede.maskP],
        )
        > anarede.cte["TEPA"]
        or norm(
            anarede.deltaQ[anarede.maskQ],
        )
        > anarede.cte["TEPR"]
        or ctrldelta(
            anarede,
        )
    ):
        # Armazenamento da trajetoria de convergencia
        convergence(
            anarede,
        )

        # Matriz Jacobiana
        matrices(
            anarede,
        )

        # Variaveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualizacao das Variaveis de estado
        updtstt(
            anarede,
        )

        # Atualizacao das potencias
        updtpwr(
            anarede,
        )

        # Atualizacao dos residuos
        residue(
            anarede,
        )

        # Incremento de iteracao
        anarede.solution["iter"] += 1

        # Condicao Divergencia por iteracoes
        if anarede.solution["iter"] > anarede.cte["ACIT"]:
            anarede.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolacao de numero maximo de iteracoes)"
            )
            break

    # Iteracao Adicional
    if anarede.solution["iter"] <= anarede.cte["ACIT"]:
        # Armazenamento da trajetoria de convergencia
        convergence(
            anarede,
        )

        # Matriz Jacobiana
        matrices(
            anarede,
        )

        # Variaveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualizacao das variaveis de estado
        updtstt(
            anarede,
        )

        # Atualizacao das potencias
        updtpwr(
            anarede,
        )

        # Atualizacao dos residuos
        residue(
            anarede,
        )

        # Convergencia
        anarede.solution["convergence"] = "SISTEMA CONVERGENTE"
