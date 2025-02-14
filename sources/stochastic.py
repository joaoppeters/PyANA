# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def sxlf(
    powerflow,
):
    """batch de execução estocástica

    Args
        powerflow:
    """

    from os import remove
    from os.path import exists, realpath

    from anarede import anarede
    from factor import load_participation, loadf, windf
    from folder import sxlffolder
    from normal import loadn, windn
    from ulog import usxlf

    ## Inicialização
    powerflow.nsamples = 200
    for stddev in range(1, 2, 1):
        loadstd = 9
        geolstd = 15
        sxlffolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

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
            lmean=lmean,
            wmean=wmean,
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

            usxlf(
                powerflow,
            )

            anarede(file=powerflow.filedir, time=2)

            exlfpwf = realpath(
                powerflow.sxlffolder
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.PWF".format(powerflow.ones)
            )
            exlfrel = realpath(
                powerflow.sxlffolder
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.REL".format(powerflow.ones)
            )
            savfile = realpath(
                powerflow.sxlffolder
                + "\\EXLF_"
                + powerflow.namecase.upper()
                + "{}.SAV".format(powerflow.ones)
            )

            if exists(savfile):
                remove(exlfpwf)
            if not exists(exlfrel):
                remove(savfile)


def sxic(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    from areas import ne224, q2024
    from folder import areasfolder, sxicfolder
    from ulog import usxic

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

    for stddev in range(10, 11, 1):
        sxicfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlffolder
            + "\\EXLF_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                stddev,
                stddev,
            )
        )

        savfiles = list()
        with open(
            folder_path
            + "\\EXLF_"
            + powerflow.name
            + "_loadstd{}_geolstd{}.txt".format(
                stddev,
                stddev,
            ),
            "r",
        ) as file:
            for line_number, line in enumerate(file, start=1):
                # Split the line by semicolon
                columns = line.strip().split(";")
                try:
                    # Extract the value in the fourth column (index 3)
                    fourth_column_value = float(columns[3])
                    # Check if the value meets the condition
                    if fourth_column_value >= powerflow.carga_total:
                        savfiles.append(
                            "EXLF_"
                            + powerflow.name
                            + "jpmod"
                            + str(columns[0])
                            + ".SAV"
                        )
                except (IndexError, ValueError):
                    print(f"Line {line_number}: Invalid format or non-numeric value.")

        usxic(
            powerflow,
            folder_path,
            savfiles,
        )


def sxct(
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
    from ulog import usxct

    for stddev in range(1, 11, 1):
        sxctfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlffolder
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

        usxct(
            powerflow,
            folder_path,
            savfiles,
        )


def spvct(
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
    from ulog import uspvct

    for stddev in range(1, 4, 1):
        spvctfolder(
            powerflow,
            loadstd=stddev,
            geolstd=stddev,
        )

        folder_path = (
            powerflow.sxlffolder
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
