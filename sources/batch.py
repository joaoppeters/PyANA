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

    from os import listdir, remove
    from os.path import exists, isfile, join, realpath

    from anarede import exlf
    from areas import q2024
    from factor import factor, loadf, windf
    from folder import areasfolder, stochasticfolder
    from stochastic import loadn, windn
    from rela import rxlf
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

            exlfrel = realpath(
                powerflow.filefolder
                + "\\"
                + "EXLF"
                + powerflow.namecase.upper()
                + "{}.REL".format(powerflow.ones)
            )
            savfile = realpath(
                powerflow.filefolder
                + "\\"
                + powerflow.namecase.upper()
                + "{}.SAV".format(powerflow.ones)
            )

            if not exists(exlfrel):
                remove(savfile)

    for stddev in range(1, 11, 1):
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                stddev,
                stddev,
            )
        )

        with open(folder_path + "\\BALANCE.txt", "w") as balancefile:
            balancefile.write("CASO;pATIVA;pREATIVA;dATIVA;dREATIVA\n")

        # List and filter files by extension
        relfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith("EXLF")
            and f.endswith(".REL")
            and isfile(join(folder_path, f))
        ]

        rxlf(
            powerflow,
            folder=folder_path,
            relfiles=relfiles,
            balancefile=balancefile,
        )

        # Open and read the file
        with open(folder_path + "\\BALANCE.txt", "r") as f:
            lines = f.readlines()

        # Separate the header and data
        header = lines[0]
        data = lines[1:]

        # Sort the data lines based on the first column (split by `;`)
        sorted_data = sorted(data, key=lambda x: int(x.split(";")[0]))

        # Combine the header and sorted data
        sorted_lines = [header] + sorted_data

        # Write the sorted lines to a new file
        with open(folder_path + "\\BALANCE.txt", "w") as f:
            f.writelines(sorted_lines)


def stochsxic(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from os import listdir
    from os.path import isfile, join

    from rela import rxic
    from ulog import usxic

    for stddev in range(1, 11, 1):
        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                stddev,
                stddev,
            )
        )
        # List and filter files by extension
        savfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith(powerflow.name + "JP")
            and f.endswith(".SAV")
            and isfile(join(folder_path, f))
        ]
        usxic(
            powerflow,
            savfiles,
        )

    for stddev in range(1, 11, 1):
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}geolstd{}".format(
                stddev,
                stddev,
            )
        )

        # List and filter files by extension
        relfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith("EXIC")
            and f.endswith(".REL")
            and isfile(join(folder_path, f))
        ]

        rxic(
            powerflow,
            relfiles,
        )


def stochsxct(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from os import listdir
    from os.path import isfile, join

    from rela import rxct
    from ulog import usxct

    for stddev in range(1, 11, 1):
        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                stddev,
                stddev,
            )
        )
        # List and filter files by extension
        savfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith(powerflow.name + "JP")
            and f.endswith(".SAV")
            and isfile(join(folder_path, f))
        ]

        usxct(
            powerflow,
            savfiles,
        )

    for stddev in range(1, 11, 1):
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}geolstd{}".format(
                stddev,
                stddev,
            )
        )

        # List and filter files by extension
        relfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith("EXCT")
            and f.endswith(".REL")
            and isfile(join(folder_path, f))
        ]

        rxct(
            powerflow,
            relfiles,
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
    from os.path import isfile, join

    from rela import rpvct
    from ulog import uspvct

    for stddev in range(1, 11, 1):
        # Specify the folder path and file extension
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                stddev,
                stddev,
            )
        )
        # List and filter files by extension
        savfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith(powerflow.name + "JP")
            and f.endswith(".SAV")
            and isfile(join(folder_path, f))
        ]

        uspvct(
            powerflow,
            savfiles,
        )

    for stddev in range(1, 11, 1):
        folder_path = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}geolstd{}".format(
                stddev,
                stddev,
            )
        )

        # List and filter files by extension
        relfiles = [
            f
            for f in listdir(folder_path)
            if f.startswith("EPVCT")
            and f.endswith(".REL")
            and isfile(join(folder_path, f))
        ]

        rpvct(
            powerflow,
            relfiles,
        )
