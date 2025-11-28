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
from ctrl import controlsol, controldelta
from matrices import matrices
from residue import residue
from scheduled import scheduled
from update import updtpwr, updtstt


def newton(
    anarede,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Args
        anarede:
    """
    ## Inicialização
    # Variável para armazenamento de solução
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
    controlsol(
        anarede,
    )

    # Variáveis Especificadas
    scheduled(
        anarede,
    )

    # Resíduos
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
        or controldelta(
            anarede,
        )
    ):
        # Armazenamento da trajetória de convergência
        convergence(
            anarede,
        )

        # Matriz Jacobiana
        matrices(
            anarede,
        )

        # Variáveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            anarede,
        )

        # Atualização das potências
        updtpwr(
            anarede,
        )

        # Atualização dos resíduos
        residue(
            anarede,
        )

        # Incremento de iteração
        anarede.solution["iter"] += 1

        # Condição Divergência por iterações
        if anarede.solution["iter"] > anarede.cte["ACIT"]:
            anarede.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

    # Iteração Adicional
    if anarede.solution["iter"] <= anarede.cte["ACIT"]:
        # Armazenamento da trajetória de convergência
        convergence(
            anarede,
        )

        # Matriz Jacobiana
        matrices(
            anarede,
        )

        # Variáveis de estado
        anarede.statevar, residuals, rank, singular = lstsq(
            anarede.jacobian,
            anarede.deltaPQY,
            rcond=None,
        )

        # Atualização das variáveis de estado
        updtstt(
            anarede,
        )

        # Atualização das potências
        updtpwr(
            anarede,
        )

        # Atualização dos resíduos
        residue(
            anarede,
        )

        # Convergência
        anarede.solution["convergence"] = "SISTEMA CONVERGENTE"
