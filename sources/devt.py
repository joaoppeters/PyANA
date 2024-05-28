# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy.linalg import inv


def apcb(
    powerflow,
    idx,
    Yblc,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    busidx = powerflow.devtDF.iloc[idx].elemento - 1
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
    idx,
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
    idx,
    Yblc,
):
    """
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    
    ## Inicialização
    de = powerflow.devtDF.iloc[idx].elemento - 1
    para = powerflow.devtDF.iloc[idx].para - 1

    Ya = Yblc[: (powerflow.nger), :][:, : (powerflow.nger)]
    Yb = Yblc[: (powerflow.nger), :][:, (powerflow.nger) :]
    Ybl = Yblc[(powerflow.nger) :, :][:, (powerflow.nger) :]

    y = Ybl[de, para]

    Ybl[de, de] += y
    Ybl[de, para] -= y
    Ybl[para, de] -= y
    Ybl[para, para] += y

    return Ya - Yb @ inv(Ybl) @ Yb.T
