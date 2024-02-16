# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros

def reduction(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtf = powerflow.dtf[powerflow.mask]
    powerflow.dwf = zeros((powerflow.mask.shape[0], powerflow.mask.shape[0]))[
        powerflow.mask, :
    ][:, powerflow.mask]

    powerflow.dtg = zeros((powerflow.mask.shape[0], 1))[powerflow.mask]

    powerflow.dxh = zeros((1, powerflow.mask.shape[0]))[0, powerflow.mask]
    powerflow.dwh = 2 * powerflow.solution["eigen"][powerflow.mask]