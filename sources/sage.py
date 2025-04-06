# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def sage(
    powerflow,
):
    """análise de fluxo de potência estocástica via SAGE (Stochastic Analysis of Generation and Demand)
    Args
        powerflow:
    """

    from os import listdir
    from os.path import dirname, isfile, join

    from areas import q2024, ne224
    from factor import generator_participation, load_participation, loadf, windf
    from folder import sagefolder
    from normal import loadn, windn
    from pwf import pwf
    from rwpwf import rwpwf

    pwffiles = [
        f
        for f in listdir(powerflow.maindir + "\\sistemas\\")
        if f.startswith(powerflow.name + "_CTG")
        and f.endswith(".PWF")
        and isfile(join(powerflow.maindir + "\\sistemas\\", f))
    ]

    powerflow.nsamples = 1000
    stddev = 15

    for pwffile in pwffiles:
        pwf(powerflow, dirname(powerflow.dirPWF) + "\\" + pwffile)
        sagefolder(
            powerflow,
            pwffile,
        )

        if "NE224" in powerflow.name:
            ne224(
                powerflow,
            )
        elif "Q2024" in powerflow.name:
            q2024(
                powerflow,
            )

        powerflow.mdger = generator_participation(
            name=powerflow.name,
            dbarDF=powerflow.dbarDF.copy(),
            dger=powerflow.dger.copy(),
        )

        powerflow.namecase = powerflow.name + "jpmod"

        (
            sload,
            lmean,
        ) = loadn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            loadstd=stddev,
            stateload=powerflow.cargas,
            maindir=powerflow.maindir,
        )
        (
            swind,
            wmean,
        ) = windn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            geolstd=stddev,
            stategeneration=powerflow.eolicas,
            maindir=powerflow.maindir,
        )

        # Factor
        powerflow.mdbar = load_participation(
            name=powerflow.name,
            lpmean=lmean,
            wpmean=wmean,
            dbar=powerflow.dbarDF.copy(),
            stateload=powerflow.cargas.copy(),
            stategeneration=powerflow.eolicas.copy(),
        )

        # Loop de amostras
        powerflow.ones = 0
        for s in range(0, len(sload)):
            powerflow.mdbar = loadf(
                mdbar=powerflow.mdbar,
                psamples=sload,
                s=s,
            )
            powerflow.mdbar = windf(
                mdbar=powerflow.mdbar,
                wsamples=swind,
                s=s,
            )
            powerflow.ones += 1

            rwpwf(
                powerflow,
                powerflow.sagefolder,
            )

        print()
