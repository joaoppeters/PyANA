# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from rwpwf import rwpwf


def increment(
    anarede,
):
    """realiza incremento no nivel de carregamento (e geracao)

    Args
        anarede:
    """
    # Variável
    preincrement = sum(anarede.dbarDF["demanda_ativa"].to_numpy())

    ## Point of Collapse Method (Canizares, 1992)
    if anarede.solution["method"] == "EXPC":
        # Incremento de carga
        for idxbar, _ in anarede.dbarDF.iterrows():
            # Incremento de Carregamento
            anarede.dbarDF.at[idxbar, "demanda_ativa"] = anarede.solution[
                "demanda_ativa"
            ][idxbar] * (1 + anarede.solution["lambda"])
            anarede.dbarDF.at[idxbar, "demanda_reativa"] = anarede.solution[
                "demanda_reativa"
            ][idxbar] * (1 + anarede.solution["lambda"])

    # Prediction-Correction Method (Ajjarapu & Christy, 1992)
    elif anarede.solution["method"] == "EXIC":
        for idxinc, valueinc in anarede.dincDF.iterrows():
            # Incremento de carregamento especifico por AREA
            if valueinc["tipo_incremento_1"] == "AREA":
                for idxbar, valuebar in anarede.dbarDF.iterrows():
                    if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                        # Incremento de Carregamento
                        anarede.dbarDF.at[idxbar, "demanda_ativa"] = anarede.solution[
                            "demanda_ativa"
                        ][idxbar] * (1 + anarede.solution["stepsch"])
                        anarede.dbarDF.at[idxbar, "demanda_reativa"] = anarede.solution[
                            "demanda_reativa"
                        ][idxbar] * (1 + anarede.solution["stepsch"])

            # Incremento de carregamento especifico por BARRA
            elif valueinc["tipo_incremento_1"] == "BARR":
                # Reconfiguracao da variavel de indice
                idxinc = valueinc["identificacao_incremento_1"] - 1
                anarede.dbarDF.at[idxinc, "demanda_ativa"] = anarede.solution[
                    "demanda_ativa"
                ][idxinc] * (1 + anarede.solution["stepsch"])
                anarede.dbarDF.at[idxinc, "demanda_reativa"] = anarede.solution[
                    "demanda_reativa"
                ][idxinc] * (1 + anarede.solution["stepsch"])

        deltaincrement = sum(anarede.dbarDF["demanda_ativa"].to_numpy()) - preincrement

        # Incremento de geracao
        if anarede.pwfblock["DGER"]:
            for _, valueger in anarede.dgerDF.iterrows():
                idx = valueger["numero"] - 1
                anarede.dbarDF.at[idx, "potencia_ativa"] = anarede.dbarDF[
                    "potencia_ativa"
                ][idx] + (deltaincrement * valueger["fator_participacao"])

            anarede.solution["potencia_ativa"] = deepcopy(
                anarede.dbarDF["potencia_ativa"]
            )

        # Condicao de atingimento do maximo incremento do nivel de carregamento delimitado
        if (
            anarede.solution["stepsch"]
            == anarede.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
        ):
            anarede.solution["pmc"] = True
