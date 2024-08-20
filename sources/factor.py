# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

 
def loadfactor(
    dbar,
    dbarDF,
    psamples,
    s,
):
    """fator de potência aplicado à estocasticidade das cargas

    Parâmetros
        dbar: DataFrame com as barras
        dbarDF: DataFrame com as barras
        psamples: amostras da demanda ativa
        s: amostra
    """

    ## Inicialização
    for idx, value in dbarDF.iterrows():
        dbar.loc[idx, "demanda_ativa"] = str(
            psamples[s] * dbar.loc[idx, "fator_demanda_ativa"]
        )
        if value["demanda_reativa"] != 0 and value["demanda_ativa"] != 0:
            dbar.loc[idx, "demanda_reativa"] = str(
                psamples[s]
                * dbar.loc[idx, "fator_demanda_ativa"]
                * dbar.loc[idx, "fator_potencia"]
            )


def eolfactor(
    dbar,
    dbarDF,
    wsamples,
    s,
):
    """fator de potência aplicado à estocasticidade da geração eólica	

    Parâmetros
        dbar: DataFrame com as barras
        dbarDF: DataFrame com as barras
        wsamples: amostras da geração eólica
        s: amostra
    """

    ## Inicialização
    for idx, value in dbarDF.iterrows():
        if "EOL" in value["nome"]:
            dbar.loc[idx, "potencia_ativa"] = str(
                round(wsamples[s] * dbar.loc[idx, "fator_eol"], 0)
            )