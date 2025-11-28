# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def apcb(
    anatem,
    idx,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    anatem.solution["eventname"] += str(anatem.devtDF.iloc[idx].elemento)
    busidx = anatem.devtDF.iloc[idx].elemento - 1
    anatem.Yblc[anatem.nger + busidx, :] = 0
    anatem.Yblc[:, anatem.nger + busidx] = 0
    anatem.Yblc[anatem.nger + busidx, anatem.nger + busidx] = 1


def rmgr(
    anatem,
    idx,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    pass
    anatem.solution["eventname"] += str(anatem.devtDF.iloc[idx].elemento)


def abci(
    anatem,
    idx,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    anatem.solution["eventname"] += str(anatem.devtDF.iloc[idx].elemento)
    de = anatem.devtDF.iloc[idx].elemento - 1
    para = anatem.devtDF.iloc[idx].para - 1

    anatem.Yblc[de, de] += anatem.Yblc[anatem.nger + de, anatem.nger + para]
    anatem.Yblc[de, para] -= anatem.Yblc[anatem.nger + de, anatem.nger + para]
    anatem.Yblc[para, de] -= anatem.Yblc[anatem.nger + de, anatem.nger + para]
    anatem.Yblc[para, para] += anatem.Yblc[anatem.nger + de, anatem.nger + para]
