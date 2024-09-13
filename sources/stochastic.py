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

    # Plot the PDF
    from matplotlib import pyplot as plt
    plt.figure(1, figsize=(10, 6))
    plt.hist(lpsamples, bins=250, density=True, alpha=0.6, color="b")
    plt.xlabel('Total Active Power Demand', fontsize=18)
    plt.ylabel('Probability Density', fontsize=18)
    plt.savefig("C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\normal_active_demand.pdf", dpi=500)

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
    random.seed(2)

    # WIND POWER GENERATION
    wpmean = dbarDF[dbarDF["nome"].str.contains("EOL")][
        "potencia_ativa"
    ].sum()
    wpstddev = (geolstd * 1e-2) * wpmean
    wpsamples = random.normal(wpmean, wpstddev, nsamples)

    # Plot the PDF
    from matplotlib import pyplot as plt
    plt.figure(2, figsize=(10, 6))
    plt.hist(wpsamples, bins=250, density=True, alpha=0.6, color="g")
    plt.xlabel('Total Wind Power Generation', fontsize=18)
    plt.ylabel('Probability Density', fontsize=18)
    plt.savefig("C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\normal_eolic_power.pdf", dpi=500)

    return wpsamples, wpmean
