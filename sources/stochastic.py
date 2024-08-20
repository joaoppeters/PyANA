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
    loadstd,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
        loadstd: desvio padrão da carga em porcento (default=10)
    """

    ## Inicialização
    random.seed(1)

    # ACTIVE DEMAND
    lpmean = dbarDF.demanda_ativa[dbarDF.demanda_ativa > 0].sum()
    lpstddev = (loadstd * 1e-2) * lpmean
    lpsamples = random.normal(lpmean, lpstddev, nsamples)

    return lpsamples, lpmean


def normalEOL(
    dbarDF,
    nsamples,
    geolstd,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
        wstd: desvio padrão da geração eólica em porcento (default=10)
    """

    ## Inicialização
    random.seed(1)

    # WIND POWER GENERATION
    wpmean = dbarDF[dbarDF["nome"].str.contains("EOL")][
        "potencia_ativa"
    ].sum()
    wpstddev = (geolstd * 1e-2) * wpmean
    wpsamples = random.normal(wpmean, wpstddev, nsamples)

    return wpsamples, wpmean
