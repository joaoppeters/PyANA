# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import abs, append, argmax
from numpy.linalg import norm


def convergence(
    powerflow,
):
    """armazenamento da trajetória de convergência do processo de solução do fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Trajetória de convergência da frequência
    powerflow.solution["freqiter"] = append(
        powerflow.solution["freqiter"],
        powerflow.solution["freq"] * powerflow.options["FBASE"],
    )

    # Trajetória de convergência da potência ativa
    powerflow.solution["convP"] = append(
        powerflow.solution["convP"], norm(powerflow.deltaP[powerflow.maskP])
    )
    powerflow.solution["busP"] = append(
        powerflow.solution["busP"], argmax(abs(powerflow.deltaP[powerflow.maskP]))
    )

    # Trajetória de convergência da potência reativa
    powerflow.solution["convQ"] = append(
        powerflow.solution["convQ"], norm(powerflow.deltaQ[powerflow.maskQ])
    )
    powerflow.solution["busQ"] = append(
        powerflow.solution["busQ"], argmax(abs(powerflow.deltaQ[powerflow.maskQ]))
    )

    # Trajetória de convergência referente a cada equação de controle adicional
    if powerflow.deltaY.size != 0:
        powerflow.solution["convY"] = append(
            powerflow.solution["convY"], norm(powerflow.deltaY)
        )
        powerflow.solution["busY"] = append(
            powerflow.solution["busY"], argmax(abs(powerflow.deltaY))
        )
    else:
        powerflow.solution["convY"] = append(powerflow.solution["convY"], 0.0)
        powerflow.solution["busY"] = append(powerflow.solution["busY"], 0.0)
