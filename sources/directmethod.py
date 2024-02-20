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
    radians,
    zeros,
)
from numpy.linalg import LinAlgError, norm
from scipy.sparse import vstack, hstack
from scipy.sparse.linalg import lsqr

from ctrl import controlsol
from increment import increment
from matrices import matrices
from reduction import reduction
from residue import residue
from scheduled import scheduled
from update import updtstt, updtpwr


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
        "lambda": 0.0,
        "potencia_ativa": deepcopy(powerflow.dbarraDF["potencia_ativa"]),
        "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
        "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
        "eigen": 1.0 * (powerflow.mask),
        "sign": -1.0,
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

        # Matrizes
        matrices(
            powerflow,
        )

        # expansao total
        expansion(
            powerflow,
        )

        powerflow.funccani = hstack(
            [
                -powerflow.deltaPQY,
                powerflow.G,
                array([powerflow.H @ powerflow.H - 1]),
            ],
            "csr",
        )

        try:
            # Your sparse matrix computation using spsolve here
            powerflow.statevar = lsqr(
                powerflow.jaccani,
                powerflow.funccani.T.A,
            )[0]
        except LinAlgError:
            raise ValueError(
                "\033[91mERROR: Falha ao inverter a Matriz (singularidade)!\033[0m"
            )

        # Atualização das Variáveis de estado
        updtstt(
            powerflow,
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição de Divergência por iterações
        if powerflow.solution["iter"] > powerflow.options["ACIT"]:
            powerflow.solution[
                "convergence"
            ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

        elif (norm(powerflow.statevar) <= powerflow.options["CTOL"]) and (
            powerflow.solution["iter"] <= powerflow.options["ACIT"]
        ):
            powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"
            break

    updtpwr(
        powerflow,
    )


def expansion(
    powerflow,
):
    """expansão da matriz jacobiana para o método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtf = zeros([2 * powerflow.nbus, 1])

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

    # Reducao Total
    reduction(
        powerflow,
    )

    powerflow.jaccani = hstack(
        [powerflow.jacobian, powerflow.dtf, powerflow.dwf],
        "csr",
    )

    powerflow.jaccani = vstack(
        [
            powerflow.jaccani,
            hstack(
                [powerflow.hessian, powerflow.dtg, powerflow.jacobian.T],
                "csr",
            ),
        ],
        "csr",
    )

    powerflow.jaccani = vstack(
        [
            powerflow.jaccani,
            hstack(
                [powerflow.dxh, array([0]), powerflow.dwh],
                "csr",
            ),
        ],
        "csr",
    )
