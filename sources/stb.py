# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from dtem import *
from pwf import keywords

def stb(
    powerflow,
):
    """
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
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
    readfile(
        powerflow,
    )

    readfile2(
        powerflow,
    )

    print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")


def codes(
    powerflow,
):
    """códigos de dados de execução implementados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.codes.update(
        {
            "TITU": False,
            "DARQ": False,
            "DEVT": False,
            "DMAQ": False,
            "DSIM": False,
        }
    )


def readfile(
    powerflow,
):
    """leitura de arquivo .stb

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    f = open(f"{powerflow.dirSTB}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.pwf`
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
        elif powerflow.lines[powerflow.linecount].strip() == "DEVT" or powerflow.lines[powerflow.linecount].strip() == "DEVT IMPR":
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


def readfile2(
    powerflow,
):
    """
    
    Parâmetros
        powerflow.py: self do arquivo powerflow
    """

    for idx, value in powerflow.darqDF.iterrows():
        print(value["tipo"])
        if value["tipo"].split()[0] == "DAT":
            checkfile(
                powerflow,
                value["nome"]
            )
            if value["nome"].split("-")[1] == "DMAQ.dat\n":
                dmaq(
                    powerflow,
                )
        if value["tipo"].split()[0] == "BLT":
            checkfile(
                powerflow,
                value["nome"],
            )
            if value["nome"].split("-")[1] == "UHEUTE.blt\n":
                blt(
                    powerflow,
                )


def checkfile(
    powerflow,
    arquivo,
):
    """
    
    Parametros
        powerflow.py: self do arquivo powerflow
    """

    ## Inicialização
    pass