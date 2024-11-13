# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import random


def loadn(
    name,
    dbarDF,
    nsamples,
    loadstd,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        loadstd: desvio padrão da carga em porcento (default=10)
    """

    ## Inicialização
    random.seed(1)

    # ACTIVE DEMAND
    if "2Q2024" in name:
        # IN SP REGION
        sao_paulo = dbarDF.loc[
            dbarDF.area.isin(
                [
                    201,
                    202,
                    203,
                    204,
                    205,
                    206,
                    207,
                    208,
                    209,
                    210,
                    211,
                    212,
                    213,
                    214,
                    215,
                    216,
                    217,
                ]
            )
        ]
        lpmean = sao_paulo.demanda_ativa[sao_paulo.demanda_ativa > 0].sum()
        lpstddev = (loadstd * 1e-2) * lpmean
        lpsamples = random.normal(lpmean, lpstddev, nsamples)
    else:
        lpmean = dbarDF.demanda_ativa[dbarDF.demanda_ativa > 0].sum()
        lpstddev = (loadstd * 1e-2) * lpmean
        lpsamples = random.normal(lpmean, lpstddev, nsamples)

    # Plot the PDF
    from matplotlib import pyplot as plt

    plt.figure(1, figsize=(10, 6))
    plt.hist(lpsamples, bins=250, density=True, alpha=0.6, color="b")
    plt.xlabel("Total Active Power Demand", fontsize=18)
    plt.ylabel("Probability Density", fontsize=18)
    plt.savefig(
        "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\normal_active_demand_{}.pdf".format(
            name
        ),
        dpi=500,
    )

    return lpsamples, lpmean


def windn(
    name,
    dbarDF,
    nsamples,
    geolstd,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        wstd: desvio padrão da geração eólica em porcento (default=10)
    """

    from pandas import concat

    ## Inicialização
    random.seed(2)

    # WIND POWER GENERATION
    if "2Q2024" in name:
        # IN NORTHEAST REGION
        bahia = dbarDF.loc[dbarDF.area.isin([701, 702, 703, 704])]
        bahia_sergipe = dbarDF.loc[dbarDF.area.isin([711, 712, 713, 714, 715, 716])]
        alagoas_pernambuco = dbarDF.loc[dbarDF.area.isin([721, 722, 723, 724])]
        paraiba_rio_grande_norte = dbarDF.loc[dbarDF.area.isin([741, 742, 743, 744])]
        ceara = dbarDF.loc[dbarDF.area.isin([761, 762, 763, 764])]
        piaui = dbarDF.loc[dbarDF.area.isin([771, 772, 773])]
        maranhao = dbarDF.loc[dbarDF.area.isin([222, 861, 862, 863, 864, 865, 866])]
        nordeste = concat(
            [
                bahia,
                bahia_sergipe,
                alagoas_pernambuco,
                paraiba_rio_grande_norte,
                ceara,
                piaui,
                maranhao,
            ],
            axis=0,
            ignore_index=True,
        )

        wpmean = nordeste[nordeste.nome.str.contains("EOL")]["potencia_ativa"].sum()
        wpstddev = (geolstd * 1e-2) * wpmean
        wpsamples = random.normal(wpmean, wpstddev, nsamples)

    else:
        wpmean = dbarDF[dbarDF["nome"].str.contains("EOL")]["potencia_ativa"].sum()
        wpstddev = (geolstd * 1e-2) * wpmean
        wpsamples = random.normal(wpmean, wpstddev, nsamples)

    # Plot the PDF
    from matplotlib import pyplot as plt

    plt.figure(2, figsize=(10, 6))
    plt.hist(wpsamples, bins=250, density=True, alpha=0.6, color="g")
    plt.xlabel("Total Wind Power Generation", fontsize=18)
    plt.ylabel("Probability Density", fontsize=18)
    plt.savefig(
        "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\normal_wind_power{}.pdf".format(
            name
        ),
        dpi=500,
    )

    return wpsamples, wpmean
