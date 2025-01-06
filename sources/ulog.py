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
    if "Q2024" in powerflow.name:
        savfile = "_".join(powerflow.name.split("_")[:-1]) + ".SAV"
        case = powerflow.name.split("_")[-1][1:]
    elif "NE224" in powerflow.name:
        savfile = powerflow.name + '.SAV'
        case=1

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

    from os import remove
    from os.path import exists, realpath

    from anarede import anarede
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

        filename = savfile.removesuffix(".SAV").removeprefix("EXLF_")

        # Arquivo
        filedir = realpath(powerflow.sxic + "\\EXIC_" + filename + ".PWF")

        # Manipulacao
        file = open(filedir, "w")

        # Cabecalho
        uheader(
            file,
        )

        for inc in range(3, 8, 1):
            if inc <= 5:
                x = round(inc * 0.2, 1)
                y = 1.0
            else:
                x = 1.0
                y = round(1.0 - (inc - 5) * 0.2, 1)

            file.write("( Crescimento de Carga No{}: ({};{})".format(inc - 2, x, y))
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
                powerflow.dcte,
                file,
            )

            sdinc(
                powerflow.dinc,
                file,
                varinc=(x, y),
            )

            file.write("( ")
            file.write("\n")

            file.write("EXLF BPSI")

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("2")
            file.write("\n")
            file.write("EXIC_" + filename + ".SAV")

            file.write("\n")
            file.write("(")
            file.write("\n")

            if inc == 0:
                file.write("ARQV INIC IMPR")
                file.write("\n")
                file.write("SIM")

                file.write("\n")
                file.write("(")
                file.write("\n")

                file.write("ARQV GRAV IMPR NOVO")
                file.write("\n")
                file.write("1")
                file.write("\n")
                file.write("(")
                file.write("\n")
            else:
                file.write("ARQV GRAV IMPR")
                file.write("\n")
                file.write("{}".format(inc - 2))
                file.write("\n")
                file.write("(")
                file.write("\n")

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("4")
            file.write("\n")
            file.write("EXIC_" + filename + "_{}.REL".format(inc - 2))

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("EXIC BPSI RINT RTOT")

            file.write("\n")
            file.write("( ")
            file.write("\n")

        file.write("FIM")
        file.close()

        anarede(
            file=filedir,
            time=150,
        )

        savfile = realpath(
            powerflow.sxic
            + "\\EXIC_"
            + filename
            + "SAV"
        )

        if exists(savfile):
            remove(filedir)


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

    from os import remove
    from os.path import exists, realpath

    from anarede import anarede
    from sav import exlf2new
    from uwrite import uheader, uarq, udctg

    ## Inicialização
    for savfile in savfiles:
        exlf2new(
            exlffolder=folder_path,
            newfolder=powerflow.sxct,
            savfile=savfile,
        )

        filename = savfile.removesuffix(".SAV").removeprefix("EXLF_")

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

        udctg(
            powerflow.dctg,
            powerflow.dctg1,
            powerflow.dctg2,
            file,
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

        file.write("EXCT BPSI RTOT")
        file.write("\n")
        file.write("(P Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr")
        file.write("\n")
        file.write(" 1  2  3  4  5  6  7  8  9 10 11 12")

        file.write("\n")
        file.write("( ")
        file.write("\n")

        file.write("FIM")
        file.close()

        anarede(
            file=filedir,
            time=35,
        )

        savfile = realpath(
            powerflow.sxct
            + "\\EXCT_"
            + filename
            + "SAV"
        )

        if exists(savfile):
            remove(filedir)


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

    from os import remove
    from os.path import exists, realpath

    from anarede import anarede
    from sav import exlf2new
    from uwrite import uheader, uarq, sdinc, udctg

    ## Inicialização
    for savfile in savfiles:
        exlf2new(
            exlffolder=folder_path,
            newfolder=powerflow.spvct,
            savfile=savfile,
        )

        filename = savfile.removesuffix(".SAV").removeprefix("EXLF_")

        # Arquivo
        filedir = realpath(powerflow.spvct + "\\PVCT_" + filename + ".PWF")

        # Manipulacao
        file = open(filedir, "w")

        # Cabecalho
        uheader(
            file,
        )

        for inc in range(3, 8, 1):
            if inc <= 5:
                x = round(inc * 0.2, 1)
                y = 1.0
            else:
                x = 1.0
                y = round(1.0 - (inc - 5) * 0.2, 1)

            file.write("( Crescimento de Carga No{}: ({};{})".format(inc - 2, x, y))
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

            udctg(
                powerflow.dctg,
                powerflow.dctg1,
                powerflow.dctg2,
                file,
            )

            file.write("( ")
            file.write("\n")

            file.write("EXLF BPSI")

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("2")
            file.write("\n")
            file.write("PVCT_" + filename + ".SAV")

            file.write("\n")
            file.write("(")
            file.write("\n")

            if inc == 0:
                file.write("ARQV INIC IMPR")
                file.write("\n")
                file.write("SIM")

                file.write("\n")
                file.write("(")
                file.write("\n")

                file.write("ARQV GRAV IMPR NOVO")
                file.write("\n")
                file.write("1")
                file.write("\n")
                file.write("(")
                file.write("\n")
            else:
                file.write("ARQV GRAV IMPR")
                file.write("\n")
                file.write("{}".format(inc - 2))
                file.write("\n")
                file.write("(")
                file.write("\n")

            file.write("ULOG")
            file.write("\n")
            file.write("(N")
            file.write("\n")
            file.write("4")
            file.write("\n")
            file.write("PVCT_" + filename + "_{}.REL".format(inc - 2))

            file.write("\n")
            file.write("( ")
            file.write("\n")

            file.write("EXIC PVCT BPSI RTOT")

            file.write("\n")
            file.write("( ")
            file.write("\n")

        file.write("FIM")
        file.close()

        anarede(
            file=filedir,
            time=300,
        )

        savfile = realpath(
            powerflow.spvct
            + "\\PVCT_"
            + filename
            + "SAV".format(powerflow.ones)
        )

        if exists(savfile):
            remove(filedir)
