# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import array, concatenate, vstack, zeros
from numpy.linalg import LinAlgError, lstsq, norm

from ctrl import controlsol
from increment import increment
from matrices import matrices
from residue import residue
from scheduled import scheduled
from update import updtstt, updtpwr


def poc(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution.update(
        {
            "method": "tPoC",
            "iter": 0,
            "freq": 1.0,
            "lambda": 0.0,
            "potencia_ativa": deepcopy(powerflow.solution["active"]),
            "potencia_reativa": deepcopy(powerflow.solution["reactive"]),
            "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
            "eigen": 1.0 * (powerflow.mask),
            "sign": -1.0,
        }
    )

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

        powerflow.funccani = concatenate(
            (
                -powerflow.deltaPQY.reshape((sum(powerflow.mask), 1)),
                powerflow.G,
                array([[powerflow.H @ powerflow.H - 1]]),
            ),
            axis=0,
        )

        try:
            # Your sparse matrix computation using spsolve here
            powerflow.statevar, residuals, rank, singular = lstsq(
                powerflow.jaccani,
                powerflow.funccani,
                rcond=None,
            )
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

        print(norm(powerflow.statevar), powerflow.solution["lambda"])

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
    powerflow.dtf = vstack(
        (powerflow.solution["demanda_ativa"], powerflow.solution["demanda_reativa"])
    )
    powerflow.dtf = (
        powerflow.dtf.reshape((2 * powerflow.nbus, 1)) / powerflow.options["BASE"]
    )
    powerflow.dtf = concatenate(
        (powerflow.dtf, zeros((powerflow.controldim, 1))), axis=0
    )

    # Reducao Total
    powerflow.dtf = powerflow.dtf[powerflow.mask]
    powerflow.dwf = zeros((powerflow.mask.shape[0], powerflow.mask.shape[0]))[
        powerflow.mask, :
    ][:, powerflow.mask]

    powerflow.dtg = zeros(powerflow.dtf.shape)

    powerflow.dxh = zeros((1, powerflow.mask.shape[0]))[0, powerflow.mask]
    powerflow.dwh = 2 * powerflow.solution["eigen"][powerflow.mask]

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
