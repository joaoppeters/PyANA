# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def usxlf(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """

    from os.path import realpath

    from sav import savmove
    from uwrite import uheader, uarq, udbar, udger, udmfl, udmfl_circ, udmte, utail

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.sxlf
        + "\\EXLF_"
        + powerflow.namecase
        + "{}.PWF".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")
    savfile = "_".join(powerflow.name.split("_")[:-1]) + ".SAV"
    case = powerflow.name.split("_")[-1][1:]

    savmove(
        filename=powerflow.maindir + "\\sistemas\\" + savfile,
        filedir=powerflow.sxlf,
    )

    # Cabecalho
    uheader(
        file,
    )

    # Corpo
    uarq(
        file,
        savfile,
        case,
    )

    if powerflow.codes["DBAR"]:
        udbar(
            powerflow.mdbar,
            file,
        )

    if powerflow.codes["DGER"]:
        udger(
            powerflow.mdger,
            file,
        )

    if powerflow.codes["DMFL"]:
        if "CIRC" in powerflow.dmfl.dmfl.iloc[0]:
            udmfl_circ(
                powerflow.dmfl,
                file,
            )
        else:
            udmfl(
                powerflow.dmfl,
                file,
            )

    if powerflow.codes["DMTE"]:
        udmte(
            powerflow.dmte,
            file,
        )

    # Saida
    utail(
        powerflow,
        file,
    )


def usxic(
    powerflow,
    folder_path,
    savfiles,
):
    """

    Args
        powerflow:
        folder_path:
        file:
    """

    from os.path import realpath

    from anarede import exic
    from rwpwf import wdcte
    from sav import exlf2new
    from uwrite import uheader, uarq, sdinc

    ## Inicialização
    for savfile in savfiles:
        exlf2new(
            exlffolder=folder_path,
            newfolder=powerflow.sxic,
            savfile=savfile,
        )

        filename = savfile.removesuffix(".SAV")

        # Arquivo
        filedir = realpath(powerflow.sxic + "\\EXIC_" + filename + ".PWF")

        # Manipulacao
        file = open(filedir, "w")

        # Cabecalho
        uheader(
            file,
        )

        for inc in range(0, 11, 1):
            if inc <= 5:
                x = round(inc * 0.2, 1)
                y = 1.0
            else:
                x = 1.0
                y = round(1.0 - (inc - 5) * 0.2, 1)

            file.write("( Crescimento de Carga No{}: ({};{})".format(inc + 1, x, y))
            file.write("\n")
            file.write("(")
            file.write("\n")

            # Corpo
            uarq(
                file,
                savfile,
                case=1,
            )

            wdcte(
                powerflow.mdcte,
            )

            sdinc(
                powerflow.dinc,
                file,
                varinc=(x, y),
            )

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("4")
            file.write("\n")
            file.write("EXIC_" + filename + "_{}.REL".format(inc + 1))

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("EXIC BPSI RINT RTOT")

            file.write("\n")
            file.write("( ")
            file.write("\n")

        file.write("FIM")
        file.close()

        exic(
            file=filedir,
            time=240,
        )


def usxct(
    powerflow,
    folder_path,
    savfiles,
):
    """

    Args
        powerflow:
        folder_path:
        file:
    """

    from os.path import realpath

    from anarede import exct
    from sav import exlf2new
    from uwrite import uheader, uarq

    ## Inicialização
    for savfile in savfiles:
        exlf2new(
            exlffolder=folder_path,
            newfolder=powerflow.sxct,
            savfile=savfile,
        )

        filename = savfile.removesuffix(".SAV")

        # Arquivo
        filedir = realpath(powerflow.sxct + "\\EXCT_" + filename + ".PWF")

        # Manipulacao
        file = open(filedir, "w")

        # Cabecalho
        uheader(
            file,
        )

        # Corpo
        uarq(
            file,
            savfile,
            case=1,
        )

        file.write("ULOG")
        file.write("\n")
        file.write("(N")
        file.write("\n")
        file.write("4")
        file.write("\n")
        file.write("EXCT_" + filename + ".REL")

        file.write("\n")
        file.write("( ")
        file.write("\n")

        file.write("EXCT BPSI RINT RTOT")
        file.write("\n")
        file.write("(P Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr")
        file.write("\n")
        file.write(" 1  2  3  4  5  6  7  8  9 10 11 12")

        file.write("\n")
        file.write("( ")
        file.write("\n")

        file.write("FIM")
        file.close()

        exct(
            file=filedir,
            time=35,
        )


def uspvct(
    powerflow,
    folder_path,
    savfiles,
):
    """

    Args
        powerflow:
        file:
    """

    from os.path import realpath

    from anarede import epvct
    from sav import exlf2new
    from uwrite import uheader, uarq, sdinc

    ## Inicialização
    for savfile in savfiles:
        exlf2new(
            exlffolder=folder_path,
            newfolder=powerflow.spvct,
            savfile=savfile,
        )

        filename = savfile.removesuffix(".SAV")

        # Arquivo
        filedir = realpath(powerflow.spvct + "\\PVCT_" + filename + ".PWF")

        # Manipulacao
        file = open(filedir, "w")

        # Cabecalho
        uheader(
            file,
        )

        for inc in range(0, 11, 1):
            if inc <= 5:
                x = round(inc * 0.2, 1)
                y = 1.0
            else:
                x = 1.0
                y = round(1.0 - (inc - 5) * 0.2, 1)

            file.write("( Crescimento de Carga No{}: ({};{})".format(inc + 1, x, y))
            file.write("\n")
            file.write("(")
            file.write("\n")

            # Corpo
            uarq(
                file,
                savfile,
                case=1,
            )

            sdinc(
                powerflow.dinc,
                file,
                varinc=(x, y),
            )

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("4")
            file.write("\n")
            file.write("EXIC" + filename + "_{}.REL".format(inc + 1))

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("EXIC PVCT BPSI RINT RTOT")

            file.write("\n")
            file.write("( ")
            file.write("\n")

        file.write("FIM")
        file.close()

        epvct(
            file=filedir,
            time=300,
        )