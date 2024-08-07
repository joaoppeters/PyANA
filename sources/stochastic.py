# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import random


def normalLOAD(
    dbarDF,
    nsamples,
    lstd=10,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
        lstd: desvio padrão da carga em porcento (default=10)
    """

    ## Inicialização
    random.seed(1)

    # ACTIVE DEMAND
    pmean = dbarDF.demanda_ativa[dbarDF.demanda_ativa > 0].sum()
    pstddev = (lstd * 1e-2) * pmean
    psamples = random.normal(pmean, pstddev, nsamples)

    return psamples, pmean


def normalEOL(
    dbarDF,
    nsamples,
    wstd=10,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
        wstd: desvio padrão da geração eólica em porcento (default=10)
    """

    ## Inicialização
    random.seed(1)

    # WIND POWER GENERATION
    wmean = dbarDF[dbarDF["nome"].str.contains("EOL")][
        "potencia_ativa"
    ].sum()
    wstddev = (wstd * 1e-2) * wmean
    wsamples = random.normal(wmean, wstddev, nsamples)

    return wsamples, wmean
