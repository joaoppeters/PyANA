# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import realpath
from datetime import datetime as dt


def rwstb(
    anatem,
):
    """Inicialização

    Args
        anatem:
    """
    ## Inicialização
    # Arquivo
    anatem.filedir = realpath(
        anatem.sxlffolder + "\\" + anatem.namecase + "{}.stb".format(anatem.ones)
    )

    # Manipulacao
    file = open(anatem.filedir, "w")

    # Cabecalho
    wheader(
        file,
    )

    if anatem.stbblock["DARQ"]:
        wdarq(
            anatem,
            file,
        )

    if anatem.stbblock["DEVT"]:
        wdevt(
            anatem,
            file,
        )

    if anatem.stbblock["DMAQ"]:
        wdmaq(
            anatem,
            file,
        )

    if anatem.stbblock["DMDG MD01"]:
        wdmdg_md01(
            anatem,
            file,
        )

    if anatem.stbblock["DSIM"]:
        wdsim(
            anatem,
            file,
        )

    wtail(
        anatem,
        file,
    )

    file.close()


def wheader(
    file,
):
    """

    Args
        file:
    """
    ## Inicialização
    file.write("(")
    file.write("\n")
    file.write("( Modificacao Automatica de Dados .PWF")
    file.write("\n")
    file.write("( Joao Pedro Peters Barbosa - jpeters@usp.br")
    file.write("\n")
    file.write(
        "( Data e Hora da Gravacao: {} {}, {}  -  {}:{}:{}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
            dt.now().strftime("%H"),
            dt.now().strftime("%M"),
            dt.now().strftime("%S"),
        )
    )
    file.write("\n")
    file.write("( ")
    file.write("\n")


def wdarq(
    anatem,
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    file.write(format(anatem.titu["titu"]))
    file.write(format(anatem.titu["ruler"]))


def wdevt(
    anatem,
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    agr = 0
    file.write(format(anatem.dagr.dagr.iloc[0]))
    for idx, value in anatem.dagr1.iterrows():
        file.write(value.ruler)
        file.write(f"{value['numero']:>3} {value['descricao']:>36}")
        file.write("\n")
        file.write(anatem.dagr2.ruler.iloc[0])
        for idx in range(0, value["ndagr2"]):
            file.write(
                f"{anatem.dagr2.numero.iloc[idx + agr]:>3} {anatem.dagr2.operacao.iloc[idx + agr]:1} {anatem.dagr2.descricao.iloc[idx + agr]:>36}"
            )
            file.write("\n")
        agr += value["ndagr2"]
        file.write("FAGR")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmaq(
    anatem,
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    file.write(format(anatem.danc.danc.iloc[0]))
    file.write(format(anatem.danc.ruler.iloc[0]))
    if "ACLS" in anatem.danc.danc:
        pass
    else:
        for idx, value in anatem.danc.iterrows():
            file.write(
                f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6}"
            )
            file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmdg_md01(
    anatem,
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    file.write(format(anatem.danc.danc.iloc[0]))
    file.write(format(anatem.danc.ruler.iloc[0]))
    for idx, value in anatem.danc.iterrows():
        file.write(
            f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6} {value['ACLS']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdsim(
    anatem,
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    file.write(format(anatem.dare.dare.iloc[0]))
    file.write(format(anatem.dare.ruler.iloc[0]))
    for idx, value in anatem.dare.iterrows():
        file.write(
            f"{value['numero']:3}    {value['intercambio_liquido']:>6}     {value['nome']:^35} {value['intercambio_minimo']:>6} {value['intercambio_maximo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wtail(
    file,
):
    """

    Args
        anatem:
        file:
    """
    ## Inicialização
    file.write("(")
    file.write("\n")

    file.write("EXSI DLCC DLCA OTMX ANWT ESTC ESTS")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")
