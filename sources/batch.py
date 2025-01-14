# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def stochsxlf(
    powerflow,
):
    """batch de execução estocástica

    Args
        powerflow:
    """

    from os import listdir, remove
    from os.path import dirname, exists, isfile, join, realpath

    from anarede import anarede
    from areas import ne224, q2024
    from factor import factor, loadf, windf
    from folder import areasfolder, sxlffolder
    from stochastic import loadn, windn
    from rela import rxlf
    from rwstb import rwstb
    from ulog import usxlf

    ## Inicialização
    powerflow.nsamples = 1000
    areasfolder(
        powerflow,
    )
    if "NE224" in powerflow.name:
        ne224(
            powerflow,
        )
    elif "Q2024" in powerflow.name:
        q2024(
            powerflow,
        )
    for stddev in range(1, 2, 1):
        sxlffolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        (
            lpsamples,
            lpmean,
        ) = loadn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            loadstd=stddev,
            stateload=powerflow.cargas,
            maindir=powerflow.maindir,
        )
        (
            wpsamples,
            wpmean,
        ) = windn(
            name=powerflow.name,
            nsamples=powerflow.nsamples,
            geolstd=stddev,
            stategeneration=powerflow.eolicas,
            maindir=powerflow.maindir,
        )

        # Factor
        powerflow.mdbar, powerflow.mdger = factor(
            name=powerflow.name,
            lpmean=lpmean,
            wpmean=wpmean,
            dbarDF=powerflow.dbarDF.copy(),
            dbar=powerflow.dbar.copy(),
            dger=powerflow.dger.copy(),
            stateload=powerflow.cargas.copy(),
            stategeneration=powerflow.eolicas.copy(),
        )

        # Loop de amostras
        powerflow.ones = 0
        for s in range(0, len(lpsamples)):
            if s == 35:
                print()
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

            usxlf(
                powerflow,
            )

            anarede(file=powerflow.filedir, time=2)

            exlfpwf = realpath(
                powerflow.sxlf
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.PWF".format(powerflow.ones)
            )
            exlfrel = realpath(
                powerflow.sxlf
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.REL".format(powerflow.ones)
            )
            savfile = realpath(
                powerflow.sxlf
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.SAV".format(powerflow.ones)
            )

            if exists(savfile):
                remove(exlfpwf)
            if not exists(exlfrel):
                remove(savfile)

    for stddev in range(1, 11, 1):
        sxlffolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )
        folder = dirname(powerflow.sxlf)
        folder_path = (
            folder
            + "\\EXLF_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(stddev, stddev)
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

    from folder import sxicfolder
    from rela import rxic
    from ulog import usxic

    for stddev in range(10, 11, 1):
        sxicfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlf
            + "\\EXLF_"
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
            if f.startswith("EXLF_")
            and f.endswith(".SAV")
            and isfile(join(folder_path, f))
        ]

        usxic(
            powerflow,
            folder_path,
            savfiles,
        )

    # for stddev in range(1, 11, 1):
    #     folder_path = (
    #         powerflow.maindir
    #         + "\\sistemas\\"
    #         + powerflow.name
    #         + "_loadstd{}_geolstd{}".format(
    #             stddev,
    #             stddev,
    #         )
    #     )

    #     # List and filter files by extension
    #     relfiles = [
    #         f
    #         for f in listdir(folder_path)
    #         if f.startswith("EXIC")
    #         and f.endswith(".REL")
    #         and isfile(join(folder_path, f))
    #     ]

    #     rxic(
    #         powerflow,
    #         relfiles,
    #     )


def stochsxct(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    ## Inicialização
    from os import listdir
    from os.path import isfile, join

    from folder import sxctfolder
    from rela import rxct
    from ulog import usxct

    for stddev in range(4, 5, 1):
        sxctfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlf
            + "\\EXLF_"
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
            folder_path,
            savfiles,
        )

    # for stddev in range(1, 11, 1):
    #     folder_path = (
    #         powerflow.maindir
    #         + "\\sistemas\\"
    #         + powerflow.name
    #         + "_loadstd{}_geolstd{}".format(
    #             stddev,
    #             stddev,
    #         )
    #     )

    #     # List and filter files by extension
    #     relfiles = [
    #         f
    #         for f in listdir(folder_path)
    #         if f.startswith("EXCT")
    #         and f.endswith(".REL")
    #         and isfile(join(folder_path, f))
    #     ]

    #     rxct(
    #         powerflow,
    #         relfiles,
    #     )


def stochspvct(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    ## Inicialização
    from os import listdir
    from os.path import isfile, join

    from folder import spvctfolder
    from rela import rpvct
    from ulog import uspvct

    for stddev in range(1, 4, 1):
        spvctfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlf
            + "\\EXLF_"
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
            folder_path,
            savfiles,
        )

    # for stddev in range(1, 11, 1):
    #     folder_path = (
    #         powerflow.maindir
    #         + "\\sistemas\\"
    #         + powerflow.name
    #         + "_loadstd{}_geolstd{}".format(
    #             stddev,
    #             stddev,
    #         )
    #     )

    #     # List and filter files by extension
    #     relfiles = [
    #         f
    #         for f in listdir(folder_path)
    #         if f.startswith("EPVCT")
    #         and f.endswith(".REL")
    #         and isfile(join(folder_path, f))
    #     ]

    #     rxpvct(
    #         powerflow,
    #         relfiles,
    #     )
