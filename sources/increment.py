# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from rwpwf import rwpwf


def increment(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Args
        powerflow:
    """
    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarDF["demanda_ativa"].to_numpy())

    ## Point of Collapse Method (Canizares, 1992)
    if powerflow.solution["method"] == "EXPC":
        # Incremento de carga
        for idxbar, _ in powerflow.dbarDF.iterrows():
            # Incremento de Carregamento
            powerflow.dbarDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
                "demanda_ativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])
            powerflow.dbarDF.at[idxbar, "demanda_reativa"] = powerflow.solution[
                "demanda_reativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])

    # Prediction-Correction Method (Ajjarapu & Christy, 1992)
    elif powerflow.solution["method"] == "EXIC":
        for idxinc, valueinc in powerflow.dincDF.iterrows():
            # Incremento de carregamento específico por AREA
            if valueinc["tipo_incremento_1"] == "AREA":
                for idxbar, valuebar in powerflow.dbarDF.iterrows():
                    if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                        # Incremento de Carregamento
                        powerflow.dbarDF.at[idxbar, "demanda_ativa"] = (
                            powerflow.solution["demanda_ativa"][idxbar]
                            * (1 + powerflow.solution["stepsch"])
                        )
                        powerflow.dbarDF.at[idxbar, "demanda_reativa"] = (
                            powerflow.solution["demanda_reativa"][idxbar]
                            * (1 + powerflow.solution["stepsch"])
                        )

            # Incremento de carregamento específico por BARRA
            elif valueinc["tipo_incremento_1"] == "BARR":
                # Reconfiguração da variável de índice
                idxinc = valueinc["identificacao_incremento_1"] - 1
                powerflow.dbarDF.at[idxinc, "demanda_ativa"] = powerflow.solution[
                    "demanda_ativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])
                powerflow.dbarDF.at[idxinc, "demanda_reativa"] = powerflow.solution[
                    "demanda_reativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])

        deltaincrement = (
            sum(powerflow.dbarDF["demanda_ativa"].to_numpy()) - preincrement
        )

        # Incremento de geração
        if powerflow.codes["DGER"]:
            for _, valueger in powerflow.dgerDF.iterrows():
                idx = valueger["numero"] - 1
                powerflow.dbarDF.at[idx, "potencia_ativa"] = powerflow.dbarDF[
                    "potencia_ativa"
                ][idx] + (deltaincrement * valueger["fator_participacao"])

            powerflow.solution["potencia_ativa"] = deepcopy(
                powerflow.dbarDF["potencia_ativa"]
            )

        # Condição de atingimento do máximo incremento do nível de carregamento delimitado
        if (
            powerflow.solution["stepsch"]
            == powerflow.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
        ):
            powerflow.solution["pmc"] = True
