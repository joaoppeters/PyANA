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
        "method": "NEWTON",
        "iter": 0,
        "voltage": array(powerflow.dbarDF["tensao"] * 1e-3),
        "theta": array(radians(powerflow.dbarDF["angulo"])),
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
        "sign": 1.0,
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
        norm(
            powerflow.deltaP[powerflow.maskP],
        )
        > powerflow.options["TEPA"]
        or norm(
            powerflow.deltaQ[powerflow.maskQ],
        )
        > powerflow.options["TEPR"]
        or controldelta(
            powerflow,
        )
    ):
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Matriz Jacobiana
        matrices(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar, residuals, rank, singular = lstsq(
            powerflow.jacobian,
            powerflow.deltaPQY,
            rcond=None,
        )

        # Atualização das Variáveis de estado
        updtstt(
            powerflow,
        )

        # Atualização das potências
        updtpwr(
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
        matrices(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar, residuals, rank, singular = lstsq(
            powerflow.jacobian,
            powerflow.deltaPQY,
            rcond=None,
        )

        # Atualização das variáveis de estado
        updtstt(
            powerflow,
        )

        # Atualização das potências
        updtpwr(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"
