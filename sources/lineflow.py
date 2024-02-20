# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import cos, sin, zeros


def lineflow(
    powerflow,
):
    """cálculo do fluxo de potência nas linhas de transmissão

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    powerflow.solution.update(
        {
            "active_flow_F2": zeros(powerflow.nlin),
            "reactive_flow_F2": zeros(powerflow.nlin),
            "active_flow_2F": zeros(powerflow.nlin),
            "reactive_flow_2F": zeros(powerflow.nlin),
        }
    )

    for idx, value in powerflow.dlinhaDF.iterrows():
        k = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["de"]][0]
        m = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["para"]][0]
        yline = 1 / ((value["resistencia"] / 100) + 1j * (value["reatancia"] / 100))

        # Verifica presença de transformadores com tap != 1.
        if value["tap"] != 0:
            yline /= value["tap"]

        # Potência ativa k -> m
        powerflow.solution["active_flow_F2"][idx] = yline.real * (
            powerflow.solution["voltage"][k] ** 2
        ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
            yline.real
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            + yline.imag
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência reativa k -> m
        powerflow.solution["reactive_flow_F2"][idx] = -(
            (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
        ) * (powerflow.solution["voltage"][k] ** 2) + powerflow.solution["voltage"][
            k
        ] * powerflow.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            - yline.real
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência ativa m -> k
        powerflow.solution["active_flow_2F"][idx] = yline.real * (
            powerflow.solution["voltage"][m] ** 2
        ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
            yline.real
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            - yline.imag
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência reativa m -> k
        powerflow.solution["reactive_flow_2F"][idx] = -(
            (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
        ) * (powerflow.solution["voltage"][m] ** 2) + powerflow.solution["voltage"][
            k
        ] * powerflow.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            + yline.real
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

    # Active Flow
    powerflow.solution["active_flow_F2"] *= powerflow.options["BASE"]
    powerflow.solution["active_flow_2F"] *= powerflow.options["BASE"]
    powerflow.solution["active_flow_loss"] = deepcopy(
        powerflow.solution["active_flow_F2"] + powerflow.solution["active_flow_2F"]
    )

    # Reactive Flow
    powerflow.solution["reactive_flow_F2"] *= powerflow.options["BASE"]
    powerflow.solution["reactive_flow_2F"] *= powerflow.options["BASE"]
    powerflow.solution["reactive_flow_loss"] = deepcopy(
        powerflow.solution["reactive_flow_F2"] + powerflow.solution["reactive_flow_2F"]
    )
