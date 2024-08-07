# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import (
    exp,
    linspace,
    pi,
    sqrt,
    random,
)
from folder import stochasticfolder


def stocharou(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)
    nsamples = 5000

    stochasticfolder(
        powerflow,
        lstd=10,
        geolstd=10,
    )

    powerflow.filefolder = powerflow.stochasticsystems

    # ACTIVE DEMAND
    pmean = powerflow.dbarDF.demanda_ativa[powerflow.dbarDF.demanda_ativa > 0].sum()
    pstddev = 0.1 * pmean
    # x = linspace(pmean - 5 * pstddev, pmean + 5 * pstddev, nsamples)
    # pdf = (1 / (pstddev * sqrt(2 * pi))) * exp(-0.5 * ((x - pmean) / pstddev) ** 2)
    psamples = random.normal(pmean, pstddev, nsamples)

    # WIND POWER GENERATION
    wmean = powerflow.dbarDF[powerflow.dbarDF["nome"].str.contains("EOL")][
        "potencia_ativa"
    ].mean()
    wstddev = 0.1 * wmean
    # x = linspace(pmean - 5 * wstddev, pmean + 5 * wstddev, nsamples)
    wsamples = random.normal(wmean, wstddev, nsamples)

    return psamples, pmean, wsamples, wmean
