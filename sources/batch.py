# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def stochsxsc(
    powerflow,
):
    """batch de execução estocástica

    Args
        powerflow: self do arquivo powerflow.py
    """

    from os import path, remove

    from anarede import exlf
    from factor import loadfactor, eolfactor
    from folder import stochasticfolder
    from stochastic import normalLOAD, normalEOL
    from rwstb import rwstb
    from ulog import wulog

    ## Inicialização
    powerflow.nsamples = 1000
    powerflow.exicflag = False
    powerflow.exctflag = False
    for stddev in range(1, 11, 1):
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

            # rwpwf(
            #     powerflow,
            # )

            wulog(
                powerflow,
            )

            exlf(file=powerflow.filedir, time=3)

            exlfrel = path.realpath(powerflow.filefolder + "/" + "EXLF" + powerflow.namecase.upper() + "{}.REL".format(powerflow.ones))
            savfile = path.realpath(powerflow.filefolder + "/" + powerflow.namecase.upper() + "{}.SAV".format(powerflow.ones))

            if not path.exists(exlfrel):
                remove(savfile)
            # else:
            #     rwstb(powerflow,)


def stochsxct(
    powerflow,
):
    """
    
    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    from os import listdir

    from ulog import usxct

    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = powerflow.maindir + "/sistemas/" + powerflow.name + "_loadstd{}_geolstd{}".format(loadstd, geolstd,)
        savextension = '.SAV'  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            usxct(powerflow, savfile,)


def stochsxic(
    powerflow,
):
    """
    
    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    from os import listdir
    
    from ulog import usxic
    
    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = powerflow.maindir + "/sistemas/" + powerflow.name + "_loadstd{}_geolstd{}".format(loadstd, geolstd,)
        savextension = '.REL'  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            usxic(powerflow, savfile,)


def stochsxict(
    powerflow,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    from os import listdir

    from ulog import uspvct

    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = powerflow.maindir + "/sistemas/" + powerflow.name + "_loadstd{}_geolstd{}".format(loadstd, geolstd,)
        savextension = '.REL'  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            uspvct(powerflow, savfile,)
