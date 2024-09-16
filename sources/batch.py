# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import os
import time

from anarede import anarede
from factor import loadfactor, eolfactor
from folder import stochasticfolder
from rwpwf import rwpwf
from rwstb import rwstb
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
    powerflow.exicflag = False
    powerflow.exctflag = False
    for stddev in range(5, 6, 1):
        loadstd = stddev
        geolstd = stddev

        stochasticfolder(
            powerflow,
            loadstd=loadstd,
            geolstd=geolstd,
        )

        (
            lpsamples,
            lpmean,
        ) = normalLOAD(
            dbarDF=powerflow.dbarDF,
            nsamples=powerflow.nsamples,
            loadstd=loadstd,
        )
        (
            wpsamples,
            wpmean,
        ) = normalEOL(
            dbarDF=powerflow.dbarDF,
            nsamples=powerflow.nsamples,
            geolstd=geolstd,
        )

        # Load Power Factor
        powerflow.dbar["fator_demanda_ativa"] = powerflow.dbarDF.demanda_ativa / lpmean
        powerflow.dbar["fator_potencia"] = (
            powerflow.dbarDF.demanda_reativa / powerflow.dbarDF.demanda_ativa
        )

        # Wind Generation Power Factor
        powerflow.dbar["fator_eol"] = [
            value["potencia_ativa"] / wpmean if "EOL" in value["nome"] else 0
            for idx, value in powerflow.dbarDF.iterrows()
        ]

        # Loop de amostras
        powerflow.ones = 0
        for s in range(0, len(lpsamples)):
            loadfactor(
                powerflow.dbar,
                powerflow.dbarDF,
                lpsamples,
                s,
            )
            eolfactor(powerflow.dbar,
                powerflow.dbarDF,
                wpsamples, 
                s, 
            )
            powerflow.ones += 1

            rwpwf(
                powerflow,
            )

            anarede(file=powerflow.filedir,)
            time.sleep(3)
            os.system("taskkill /f /im ANAREDE.exe")

            exlfrel = os.path.realpath(powerflow.filefolder + "/" + "EXLF" + powerflow.namecase.upper() + "{}.REL".format(powerflow.ones))
            savfile = os.path.realpath(powerflow.filefolder + "/" + powerflow.namecase.upper() + "{}.SAV".format(powerflow.ones))

            if os.path.exists(exlfrel):
                rwstb(
                    powerflow,
                )
            else:
                os.remove(savfile)
