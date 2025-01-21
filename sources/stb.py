# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from dstb import *


def stb(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    t = time.process_time()

    # Variáveis
    powerflow.linecount = 0

    # Funções
    codes(
        powerflow,
    )

    # Leitura
    rstb(
        powerflow,
    )

    if powerflow.sim == "EXSI":
        rdarq(
            powerflow,
        )

    print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")


def codes(
    powerflow,
):
    """códigos de dados de execução implementados

    Args
        powerflow:
    """
    ## Inicialização
    # Variável
    powerflow.codes.update(
        {
            "DARQ": False,
            "DEVT": False,
            "DMAQ": False,
            "DMDG MD01": False,
            "DSIM": False,
        }
    )


def rstb(
    powerflow,
):
    """leitura de arquivo .stb

    Args
        powerflow:
    """
    ## Inicialização
    # Variáveis
    f = open(f"{powerflow.dirSTB}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.stb`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Arquivos de Entrada e Saida
        if powerflow.lines[powerflow.linecount].strip() == "DARQ":
            powerflow.linecount += 1
            powerflow.darq = dict()
            powerflow.darq["ruler"] = powerflow.lines[powerflow.linecount][:]
            darq(
                powerflow,
            )

        # Dados de Eventos
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DEVT"
            or powerflow.lines[powerflow.linecount].strip() == "DEVT IMPR"
        ):
            powerflow.linecount += 1
            powerflow.devt = dict()
            powerflow.devt["ruler"] = powerflow.lines[powerflow.linecount][:]
            devt(
                powerflow,
            )

        # Dados de Controle da Simulação
        elif powerflow.lines[powerflow.linecount].strip() == "DSIM":
            powerflow.linecount += 1
            powerflow.dsim = dict()
            powerflow.dsim["ruler"] = powerflow.lines[powerflow.linecount][:]
            dsim(
                powerflow,
            )

        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{powerflow.anatem}`!\033[0m")


def rdarq(
    powerflow,
):
    """leitura de arquivos .dat e .blt associados ao dado de entrada DARQ

    Args
        powerflow:
    """

    for idx, value in powerflow.darqDF.iterrows():
        if value["tipo"].split()[0] == "DAT":
            arquivo, arquivoname = checktem(powerflow, value["nome"])
            if value["nome"].split("-")[1].strip().lower() == "dmaq.dat":
                dmaq(
                    powerflow,
                    arquivo,
                    arquivoname,
                )
        if value["tipo"].split()[0] == "BLT":
            arquivo, arquivoname = checktem(
                powerflow,
                value["nome"],
            )
            if value["nome"].split("-")[1].strip().lower() == "uheute.blt":
                blt(
                    powerflow,
                    arquivo,
                    arquivoname,
                )
