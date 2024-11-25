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
        powerflow:
    """

    from os import path, remove
    from pandas import to_numeric

    from anarede import exlf
    from areas import q2024
    from factor import factor, loadf, windf
    from folder import areasfolder, stochasticfolder
    from stochastic import loadn, windn
    from rwstb import rwstb
    from ulog import wulog

    ## Inicialização
    powerflow.nsamples = 1000
    powerflow.exicflag = False
    powerflow.exctflag = False
    areasfolder(
        powerflow,
    )
    q2024(
        powerflow,
    )
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
        ) = loadn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            loadstd=loadstd,
            stateload=powerflow.sao_paulo,
        )
        (
            wpsamples,
            wpmean,
        ) = windn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            geolstd=geolstd,
            stategeneration=powerflow.nordeste,
        )

        # Factor
        powerflow.mdbar, powerflow.mdger = factor(
            name=powerflow.name,
            lpmean=lpmean,
            wpmean=wpmean,
            dbarDF=powerflow.dbarDF.copy(),
            dbar=powerflow.dbar.copy(),
            dger=powerflow.dger.copy(),
            stateload=powerflow.sao_paulo.copy(),
            stategeneration=powerflow.nordeste.copy(),
        )

        # Loop de amostras
        powerflow.ones = 0
        for s in range(0, len(lpsamples)):
            powerflow.mdbar = loadf(
                mdbar=powerflow.mdbar,
                psamples=lpsamples,
                s=s,
            )
            powerflow.mdbar = windf(
                mdbar=powerflow.mdbar,
                wsamples=wpsamples,
                s=s,
            )
            powerflow.ones += 1

            wulog(
                powerflow,
            )

            exlf(file=powerflow.filedir, time=3)

            exlfrel = path.realpath(
                powerflow.filefolder
                + "/"
                + "EXLF"
                + powerflow.namecase.upper()
                + "{}.REL".format(powerflow.ones)
            )
            savfile = path.realpath(
                powerflow.filefolder
                + "/"
                + powerflow.namecase.upper()
                + "{}.SAV".format(powerflow.ones)
            )

            if not path.exists(exlfrel):
                remove(savfile)
            # else:
                # print()
                # with open(powerflow.stochasticsystems + "\\BALANCE.txt", "a") as file:
                #     file.write(
                #         "{};{};{}\n".format(
                #             stddev,
                #             to_numeric(powerflow.mdbar.potencia_ativa, errors="coerce")
                #             .fillna(0)
                #             .sum(),
                #             to_numeric(powerflow.mdbar.potencia_reativa, errors="coerce")
                #             .fillna(0)
                #             .sum(),
                #             to_numeric(powerflow.mdbar.demanda_ativa, errors="coerce")
                #             .fillna(0)
                #             .sum(),
                #             to_numeric(powerflow.mdbar.demanda_reativa, errors="coerce")
                #             .fillna(0)
                #             .sum(),
                #         )
                #     )


def stochsxct(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from os import listdir

    from ulog import usxct

    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "/sistemas/"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
        savextension = ".SAV"  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            usxct(
                powerflow,
                savfile,
            )


def stochsxic(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from os import listdir

    from ulog import usxic

    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "/sistemas/"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
        savextension = ".REL"  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            usxic(
                powerflow,
                savfile,
            )


def stochsxict(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from os import listdir

    from ulog import uspvct

    for stddev in range(1, 11, 1):
        loadstd = stddev
        geolstd = stddev

        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "/sistemas/"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
        savextension = ".REL"  # Change to the extension you need

        # List and filter files by extension
        savfiles = [f for f in listdir(folder_path) if f.endswith(savextension)]

        # Print the filtered files
        for savfile in savfiles:
            uspvct(
                powerflow,
                savfile,
            )
