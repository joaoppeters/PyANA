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
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.solution["eventname"] += str(powerflow.devtDF.iloc[idx].elemento)
    busidx = powerflow.devtDF.iloc[idx].elemento - 1
    powerflow.Yblc[powerflow.nger + busidx, :] = 0
    powerflow.Yblc[:, powerflow.nger + busidx] = 0
    powerflow.Yblc[powerflow.nger + busidx, powerflow.nger + busidx] = 1


def rmgr(
    powerflow,
    idx,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
    powerflow.solution["eventname"] += str(powerflow.devtDF.iloc[idx].elemento)


def abci(
    powerflow,
    idx,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.solution["eventname"] += str(powerflow.devtDF.iloc[idx].elemento)
    de = powerflow.devtDF.iloc[idx].elemento - 1
    para = powerflow.devtDF.iloc[idx].para - 1

    powerflow.Yblc[de, de] += powerflow.Yblc[powerflow.nger + de, powerflow.nger + para]
    powerflow.Yblc[de, para] -= powerflow.Yblc[
        powerflow.nger + de, powerflow.nger + para
    ]
    powerflow.Yblc[para, de] -= powerflow.Yblc[
        powerflow.nger + de, powerflow.nger + para
    ]
    powerflow.Yblc[para, para] += powerflow.Yblc[
        powerflow.nger + de, powerflow.nger + para
    ]
