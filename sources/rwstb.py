# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import realpath
from datetime import datetime as dt


def rwstb(
    powerflow,
):
    """inicializacao

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicializacao
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder + "/" + powerflow.namecase + "{}.stb".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")

    # Cabecalho
    wheader(
        file,
    )

    if powerflow.codes["DARQ"]:
        wdarq(
            powerflow,
            file,
        )

    if powerflow.codes["DEVT"]:
        wdevt(
            powerflow,
            file,
        )

    if powerflow.codes["DMAQ"]:
        wdmaq(
            powerflow,
            file,
        )

    if powerflow.codes["DMDG MD01"]:
        wdmdg_md01(
            powerflow,
            file,
        )

    if powerflow.codes["DSIM"]:
        wdsim(
            powerflow,
            file,
        )

    wtail(
        powerflow,
        file,
    )

    file.close()


def wheader(
    file,
):
    """

    Args
        file: arquivo de saída
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
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.titu["titu"]))
    file.write(format(powerflow.titu["ruler"]))


def wdevt(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    agr = 0
    file.write(format(powerflow.dagr.dagr.iloc[0]))
    for idx, value in powerflow.dagr1.iterrows():
        file.write(value.ruler)
        file.write(f"{value['numero']:>3} {value['descricao']:>36}")
        file.write("\n")
        file.write(powerflow.dagr2.ruler.iloc[0])
        for idx in range(0, value["ndagr2"]):
            file.write(
                f"{powerflow.dagr2.numero.iloc[idx + agr]:>3} {powerflow.dagr2.operacao.iloc[idx + agr]:1} {powerflow.dagr2.descricao.iloc[idx + agr]:>36}"
            )
            file.write("\n")
        agr += value["ndagr2"]
        file.write("FAGR")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmaq(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.danc.danc.iloc[0]))
    file.write(format(powerflow.danc.ruler.iloc[0]))
    if "ACLS" in powerflow.danc.danc:
        pass
    else:
        for idx, value in powerflow.danc.iterrows():
            file.write(
                f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6}"
            )
            file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmdg_md01(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.danc.danc.iloc[0]))
    file.write(format(powerflow.danc.ruler.iloc[0]))
    for idx, value in powerflow.danc.iterrows():
        file.write(
            f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6} {value['ACLS']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdsim(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dare.dare.iloc[0]))
    file.write(format(powerflow.dare.ruler.iloc[0]))
    for idx, value in powerflow.dare.iterrows():
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
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write("(")
    file.write("\n")

    file.write("EXSI DLCC DLCA OTMX ANWT ESTC ESTS")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")
