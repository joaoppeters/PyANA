# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import matplotlib.pyplot as plt
from numpy import arctan, tan, zeros

from anarede import anarede
from rewrite import rewrite
from stochastic import stocharou


def batch(
    powerflow,
):
    """batch de execução

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pdf, psamples, wsamples, = stocharou(
        powerflow,
    )
    qsamples = zeros(psamples.shape[0])

    powerflow.dbar["fator_demanda_ativa"] = (
        powerflow.dbarDF.demanda_ativa / powerflow.dbarDF.demanda_ativa.sum()
    )
    powerflow.dbar["fator_potencia"] = (
        powerflow.dbarDF.demanda_reativa / powerflow.dbarDF.demanda_ativa
    )
    powerflow.tenths = 1
    powerflow.ones = 0

    for s in range(0, psamples.shape[0]):
        for idx, value in powerflow.dbarDF.iterrows():
            if value["demanda_reativa"] != 0 and value["demanda_ativa"] != 0:
                qsamples[s] += psamples[s] * powerflow.dbar.loc[idx, "fator_demanda_ativa"] * powerflow.dbar.loc[idx, "fator_potencia"]

    # for s in range(0, len(psamples)):
    #     powerfactor(
    #         powerflow,
    #         psamples,
    #         s,
    #         qsamples,
    #     )
    #     powerflow.ones += 1

        # rewrite(
        #     powerflow,
        # )

        # filepath = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas"
        # anarede(filepath=filepath, filenamecase=powerflow.namecase)
        # if powerflow.ones == 10:
        #     powerflow.tenths += 1
        #     powerflow.ones = 0

    plt.hist(psamples, bins=100, density=True, alpha=0.6, color="g", label="Active Demand")
    plt.hist(qsamples, bins=100, density=True, alpha=0.6, color="b", label="Reactive Demand")
    plt.hist(wsamples, bins=100, density=True, alpha=0.6, color="r", label="Wind Generation")
    plt.xlabel("Density", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.legend()
    plt.show()


def powerfactor(
    powerflow,
    psamples,
    s,
    qsamples,
):    


    for idx, value in powerflow.dbarDF.iterrows():
        powerflow.dbar.loc[idx, "demanda_ativa"] = str(
            psamples[s] * powerflow.dbar.loc[idx, "fator_demanda_ativa"]
        )
        if value["demanda_reativa"] != 0 and value["demanda_ativa"] != 0:
            powerflow.dbar.loc[idx, "demanda_reativa"] = str(
                psamples[s]
                * powerflow.dbar.loc[idx, "fator_demanda_ativa"]
                * powerflow.dbar.loc[idx, "fator_potencia"]
            )
            # qsamples[s] += psamples[s] * powerflow.dbar.loc[idx, "fator_demanda_ativa"] * powerflow.dbar.loc[idx, "fator_potencia"]
            
    qsamples[s] = sum(powerflow.dbar.demanda_reativa.astype(float))