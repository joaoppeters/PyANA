# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy.linalg import inv


def apcb(
    powerflow,
    event,
    Yblc,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    busidx = powerflow.devtDF.iloc[event].elemento - 1
    Yblc[powerflow.nger + busidx, :] = 0
    Yblc[:, powerflow.nger + busidx] = 0
    Yblc[powerflow.nger + busidx, powerflow.nger + busidx] = 1

    Ya = Yblc[: (powerflow.nger), :][:, : (powerflow.nger)]
    Yb = Yblc[: (powerflow.nger), :][:, (powerflow.nger) :]
    Ybl = Yblc[(powerflow.nger) :, :][:, (powerflow.nger) :]

    return Ya - Yb @ inv(Ybl) @ Yb.T


def rmcb(
    powerflow,
    Yblc,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    Ya = Yblc[: (powerflow.nger), :][:, : (powerflow.nger)]
    Yb = Yblc[: (powerflow.nger), :][:, (powerflow.nger) :]
    Ybl = Yblc[(powerflow.nger) :, :][:, (powerflow.nger) :]

    return Ya - Yb @ inv(Ybl) @ Yb.T


def rmgr(
    powerflow,
    event,
    Yblc,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def abci(
    powerflow,
    event,
    Yblc,
):
    """
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    
    ## Inicialização
    pass
