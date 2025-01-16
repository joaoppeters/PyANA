# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import random


def loadn(
    name,
    nsamples,
    loadstd,
    stateload,
    maindir,
):
    """

    Args
        powerflow:
        loadstd:
    """
    ## Inicialização
    random.seed(1)

    ## ACTIVE DEMAND
    # IN SP REGION if "2Q2024" in name
    lpmean = stateload.demanda_ativa[stateload.demanda_ativa > 0].sum()
    lpstddev = (loadstd * 1e-2) * lpmean
    lpsamples = random.normal(lpmean, lpstddev, nsamples)

    # Plot the PDF
    from matplotlib import pyplot as plt

    plt.figure(1, figsize=(10, 6))
    plt.hist(lpsamples, bins=250, density=True, alpha=0.6, color="b")
    plt.xlabel("Total Active Power Demand", fontsize=18)
    plt.ylabel("Probability Density", fontsize=18)
    plt.savefig(
        maindir + "\\sistemas\\normal_active_demand_{}.pdf".format(name),
        dpi=500,
    )

    return lpsamples, lpmean


def windn(
    name,
    nsamples,
    geolstd,
    stategeneration,
    maindir,
):
    """

    Args
        powerflow:
        wstd:
    """
    ## Inicialização
    random.seed(2)

    ## WIND POWER GENERATION
    # IN NORTHEAST REGION if "2Q2024" in name
    wpmean = stategeneration[stategeneration.potencia_ativa > 0].potencia_ativa.sum()
    wpstddev = (geolstd * 1e-2) * wpmean
    wpsamples = random.normal(wpmean, wpstddev, nsamples)

    # Plot the PDF
    from matplotlib import pyplot as plt

    plt.figure(2, figsize=(10, 6))
    plt.hist(wpsamples, bins=250, density=True, alpha=0.6, color="g")
    plt.xlabel("Total Wind Power Generation", fontsize=18)
    plt.ylabel("Probability Density", fontsize=18)
    plt.savefig(
        maindir + "\\sistemas\\normal_wind_power{}.pdf".format(name),
        dpi=500,
    )

    return wpsamples, wpmean
