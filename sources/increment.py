# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy


def increment(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy())

    ## CANI
    if powerflow.solution["method"] == "CANI":
        # Incremento de carga
        for idxbar, _ in powerflow.dbarraDF.iterrows():
            # Incremento de Carregamento
            powerflow.dbarraDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
                "demanda_ativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])
            powerflow.dbarraDF.at[idxbar, "demanda_reativa"] = powerflow.solution[
                "demanda_reativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])

    # Delta incremento de carga
    deltaincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - preincrement


def incrementx(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy())

    # Incremento de carga
    for idxinc, valueinc in powerflow.dincDF.iterrows():
        # Incremento de carregamento específico por AREA
        if valueinc["tipo_incremento_1"] == "AREA":
            for idxbar, valuebar in powerflow.dbarraDF.iterrows():
                if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                    # Incremento de Carregamento
                    powerflow.dbarraDF.at[
                        idxbar, "demanda_ativa"
                    ] = powerflow.solution["demanda_ativa"][idxbar] * (
                        1 + powerflow.solution["stepsch"]
                    )
                    powerflow.dbarraDF.at[
                        idxbar, "demanda_reativa"
                    ] = powerflow.solution["demanda_reativa"][idxbar] * (
                        1 + powerflow.solution["stepsch"]
                    )

        # Incremento de carregamento específico por BARRA
        elif valueinc["tipo_incremento_1"] == "BARR":
            # Reconfiguração da variável de índice
            idxinc = valueinc["identificacao_incremento_1"] - 1
            powerflow.dbarraDF.at[idxinc, "demanda_ativa"] = powerflow.solution[
                "demanda_ativa"
            ][idxinc] * (1 + powerflow.solution["stepsch"])
            powerflow.dbarraDF.at[idxinc, "demanda_reativa"] = powerflow.solution[
                "demanda_reativa"
            ][idxinc] * (1 + powerflow.solution["stepsch"])

    deltaincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - preincrement

    # Incremento de geração
    if powerflow.codes["DGER"]:
        for _, valueger in powerflow.dgeraDF.iterrows():
            idx = valueger["numero"] - 1
            powerflow.dbarraDF.at[idx, "potencia_ativa"] = powerflow.dbarraDF[
                "potencia_ativa"
            ][idx] + (deltaincrement * valueger["fator_participacao"])

        powerflow.solution["potencia_ativa"] = deepcopy(
            powerflow.dbarraDF["potencia_ativa"]
        )

    # Condição de atingimento do máximo incremento do nível de carregamento delimitado
    if (
        powerflow.solution["stepsch"]
        == powerflow.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
    ):
        powerflow.solution["pmc"] = True