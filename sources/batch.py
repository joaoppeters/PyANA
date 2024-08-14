# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import os
import time

from anarede import anarede
from folder import stochasticfolder
from rewrite import rewrite
from stochastic import normalLOAD, normalEOL


def stochbatch(
    powerflow,
):
    """batch de execução estocástica

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.nsamples = 1000
    stochasticfolder(
        powerflow,
        lstd=10,
        geolstd=10,
    )

    (
        psamples,
        pmean,
    ) = normalLOAD(
        dbarDF=powerflow.dbarDF,
        nsamples=powerflow.nsamples,
        lstd=10,
    )
    (
        wsamples,
        wmean,
    ) = normalEOL(
        dbarDF=powerflow.dbarDF,
        nsamples=powerflow.nsamples,
        wstd=10,
    )

    # Load Power Factor
    powerflow.dbar["fator_demanda_ativa"] = powerflow.dbarDF.demanda_ativa / pmean
    powerflow.dbar["fator_potencia"] = (
        powerflow.dbarDF.demanda_reativa / powerflow.dbarDF.demanda_ativa
    )

    # Wind Generation Power Factor
    powerflow.dbar["fator_eol"] = [
        value["potencia_ativa"] / wmean if "EOL" in value["nome"] else 0
        for idx, value in powerflow.dbarDF.iterrows()
    ]

    # Loop de amostras
    powerflow.ones = 0
    for s in range(0, len(psamples)):
        powerfactor(
            powerflow.dbar,
            powerflow.dbarDF,
            psamples,
            s,
        )
        eol(powerflow.dbar,
            powerflow.dbarDF,
            wsamples, 
            s, 
        )
        powerflow.ones += 1

        rewrite(
            powerflow,
        )

        anarede(file=powerflow.filedir,)

        if powerflow.exicflag and not powerflow.exctflag:
            print("Monitoring for file: EXIC_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL")
            while not os.path.exists(powerflow.filedir + "//EXIC_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL"):
                time.sleep(1)
            
            os.system("taskkill /f /im ANAREDE.exe")
        
        elif not powerflow.exicflag and powerflow.exctflag:
            print("Monitoring for file: EXCT_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL")
            while not os.path.exists(powerflow.filedir + "//EXCT_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL"):
                time.sleep(1)
            
            os.system("taskkill /f /im ANAREDE.exe")

        elif powerflow.exicflag and powerflow.exctflag:
            print("Monitoring for file: EXICnEXCT_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL")
            while not os.path.exists(powerflow.filedir + "//EXICnEXCT_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL"):
                time.sleep(1)
            
            os.system("taskkill /f /im ANAREDE.exe")
        
        else:
            print("Monitoring for file: EXLF_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL")
            while not os.path.exists(powerflow.filedir + "//EXLF_" + powerflow.namecase + "c" + str(powerflow.ones) + ".REL"):
                time.sleep(1)
            
            os.system("taskkill /f /im ANAREDE.exe")


def powerfactor(
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


def eol(
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
