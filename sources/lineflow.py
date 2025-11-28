# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import cos, sin, zeros


def lineflow(
    anarede,
):
    """cálculo do fluxo de potência nas linhas de transmissão

    Args
        anarede:
    """
    ## Inicialização
    anarede.solution.update(
        {
            "active_flow_F2": zeros(anarede.nlin),
            "reactive_flow_F2": zeros(anarede.nlin),
            "active_flow_2F": zeros(anarede.nlin),
            "reactive_flow_2F": zeros(anarede.nlin),
        }
    )

    for idx, value in anarede.dlinDF.iterrows():
        k = anarede.dbarDF.index[anarede.dbarDF["numero"] == value["de"]][0]
        m = anarede.dbarDF.index[anarede.dbarDF["numero"] == value["para"]][0]
        yline = 1 / ((value["resistencia"] / 100) + 1j * (value["reatancia"] / 100))

        # Verifica presença de transformadores com tap != 1.
        if value["tap"] != 0:
            yline /= value["tap"]

        # Potência ativa k -> m
        anarede.solution["active_flow_F2"][idx] = yline.real * (
            anarede.solution["voltage"][k] ** 2
        ) - anarede.solution["voltage"][k] * anarede.solution["voltage"][m] * (
            yline.real
            * cos(anarede.solution["theta"][k] - anarede.solution["theta"][m])
            + yline.imag
            * sin(anarede.solution["theta"][k] - anarede.solution["theta"][m])
        )

        # Potência reativa k -> m
        anarede.solution["reactive_flow_F2"][idx] = -(
            (value["susceptancia"] / (2 * anarede.cte["BASE"])) + yline.imag
        ) * (anarede.solution["voltage"][k] ** 2) + anarede.solution["voltage"][
            k
        ] * anarede.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(anarede.solution["theta"][k] - anarede.solution["theta"][m])
            - yline.real
            * sin(anarede.solution["theta"][k] - anarede.solution["theta"][m])
        )

        # Potência ativa m -> k
        anarede.solution["active_flow_2F"][idx] = yline.real * (
            anarede.solution["voltage"][m] ** 2
        ) - anarede.solution["voltage"][k] * anarede.solution["voltage"][m] * (
            yline.real
            * cos(anarede.solution["theta"][k] - anarede.solution["theta"][m])
            - yline.imag
            * sin(anarede.solution["theta"][k] - anarede.solution["theta"][m])
        )

        # Potência reativa m -> k
        anarede.solution["reactive_flow_2F"][idx] = -(
            (value["susceptancia"] / (2 * anarede.cte["BASE"])) + yline.imag
        ) * (anarede.solution["voltage"][m] ** 2) + anarede.solution["voltage"][
            k
        ] * anarede.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(anarede.solution["theta"][k] - anarede.solution["theta"][m])
            + yline.real
            * sin(anarede.solution["theta"][k] - anarede.solution["theta"][m])
        )

    # Active Flow
    anarede.solution["active_flow_F2"] *= anarede.cte["BASE"]
    anarede.solution["active_flow_2F"] *= anarede.cte["BASE"]
    anarede.solution["active_flow_loss"] = deepcopy(
        anarede.solution["active_flow_F2"] + anarede.solution["active_flow_2F"]
    )

    # Reactive Flow
    anarede.solution["reactive_flow_F2"] *= anarede.cte["BASE"]
    anarede.solution["reactive_flow_2F"] *= anarede.cte["BASE"]
    anarede.solution["reactive_flow_loss"] = deepcopy(
        anarede.solution["reactive_flow_F2"] + anarede.solution["reactive_flow_2F"]
    )
