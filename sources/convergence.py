# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import abs, append, argmax
from numpy.linalg import norm


def convergence(
    anarede,
):
    """armazenamento da trajetoria de convergencia do processo de solucao do fluxo de potencia

    Args
        anarede:
    """
    # Trajetória de convergência da frequência
    anarede.solution["freqiter"] = append(
        anarede.solution["freqiter"],
        anarede.solution["freq"] * anarede.cte["FBSE"],
    )

    # Trajetoria de convergencia da potencia ativa
    anarede.solution["convP"] = append(
        anarede.solution["convP"], norm(anarede.deltaP[anarede.maskP])
    )
    anarede.solution["busP"] = append(
        anarede.solution["busP"], argmax(abs(anarede.deltaP[anarede.maskP]))
    )

    # Trajetoria de convergencia da potencia reativa
    anarede.solution["convQ"] = append(
        anarede.solution["convQ"], norm(anarede.deltaQ[anarede.maskQ])
    )
    try:
        anarede.solution["busQ"] = append(
            anarede.solution["busQ"], argmax(abs(anarede.deltaQ[anarede.maskQ]))
        )
    except:
        anarede.solution["busQ"] = append(anarede.solution["busQ"], [0.0])

    # Trajetoria de convergencia referente a cada equacao de controle adicional
    if anarede.deltaY.size != 0:
        anarede.solution["convY"] = append(
            anarede.solution["convY"], norm(anarede.deltaY)
        )
        anarede.solution["busY"] = append(
            anarede.solution["busY"], argmax(abs(anarede.deltaY))
        )
    else:
        anarede.solution["convY"] = append(anarede.solution["convY"], 0.0)
        anarede.solution["busY"] = append(anarede.solution["busY"], 0.0)
