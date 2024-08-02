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
    (
        psamples,
        pmean,
        wsamples,
        wmean,
    ) = stocharou(
        powerflow,
    )
    qsamples = zeros(psamples.shape[0])

    powerflow.dbar["fator_demanda_ativa"] = powerflow.dbarDF.demanda_ativa / pmean
    powerflow.dbar["fator_potencia"] = (
        powerflow.dbarDF.demanda_reativa / powerflow.dbarDF.demanda_ativa
    )
    powerflow.dbar["fator_eol"] = [
        value["potencia_ativa"] / wmean if "EOL" in value["nome"] else 0
        for idx, value in powerflow.dbarDF.iterrows()
    ]

    powerflow.tenths = 1
    powerflow.ones = 0

    for s in range(0, len(psamples)):
        powerfactor(
            powerflow,
            psamples,
            s,
        )
        eol(powerflow, wsamples, s, wmean)
        powerflow.ones += 1

        rewrite(
            powerflow,
        )

        filepath = (
            powerflow.maindir + "/sistemas"
        )  # C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas"
        anarede(filepath=filepath, filenamecase=powerflow.namecase)
        if powerflow.ones == 10:
            powerflow.tenths += 1
            powerflow.ones = 0


def powerfactor(
    powerflow,
    psamples,
    s,
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

    # qsamples[s] = sum(powerflow.dbar.demanda_reativa.astype(float))


def eol(
    powerflow,
    wsamples,
    s,
    wmean,
):

    for idx, value in powerflow.dbarDF.iterrows():
        if "EOL" in value["nome"]:
            powerflow.dbar.loc[idx, "potencia_ativa"] = str(
                round(wsamples[s] * powerflow.dbar.loc[idx, "fator_eol"], 0)
            )
