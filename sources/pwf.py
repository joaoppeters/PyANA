# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from dcode import *

def pwf(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    powerflow.linecount = 0

    # Funções
    keywords(
        powerflow,
    )

    # Códigos
    codes(
        powerflow,
    )

    # Leitura
    readfile(
        powerflow,
    )


def keywords(
    powerflow,
):
    """palavras-chave de arquivo .pwf

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.end_archive = "FIM"
    powerflow.end_block = ("9999", "99999")
    powerflow.comment = "("


def codes(
    powerflow,
):
    """códigos de dados de execução implementados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.codes = {
        "DANC": False,
        "DARE": False,
        "DBAR": False,
        "DCER": False,
        "DCTE": False,
        "DGBT": False,
        "DGER": False,
        "DGLT": False,
        "DINC": False,
        "DLIN": False,
    }


def readfile(
    powerflow,
):
    """leitura do arquivo .pwf

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    f = open(f"{powerflow.dirSEP}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()
    powerflow.pwf2py = {}

    # Loop de leitura de linhas do `.pwf`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Alteração do Nível de Carregamento
        if powerflow.lines[powerflow.linecount].strip() == "DANC":
            powerflow.linecount += 1
            danc(
                powerflow,
            )

        # Dados de Intercâmbio de Potência Ativa entre Áreas
        elif powerflow.lines[powerflow.linecount].strip() == "DARE":
            powerflow.linecount += 1
            dare(
                powerflow,
            )

        # Dados de Barra
        elif powerflow.lines[powerflow.linecount].strip() == "DBAR":
            powerflow.linecount += 1
            dbar(
                powerflow,
            )

        # Dados de Compensadores Estáticos de Potência Reativa
        elif powerflow.lines[powerflow.linecount].strip() == "DCER":
            powerflow.linecount += 1
            dcer(
                powerflow,
            )

        # Dados de Constantes
        elif powerflow.lines[powerflow.linecount].strip() == "DCTE":
            powerflow.linecount += 1
            dcte(
                powerflow,
            )

        # Dados de Grupo de Base de Tensão de Barras CA
        elif powerflow.lines[powerflow.linecount].strip() == "DGBT":
            powerflow.linecount += 1
            dgbt(
                powerflow,
            )

        # Dados de Geradores
        elif powerflow.lines[powerflow.linecount].strip() == "DGER":
            powerflow.linecount += 1
            dger(
                powerflow,
            )

        # Dados de Grupos de Limites de Tensão
        elif powerflow.lines[powerflow.linecount].strip() == "DGLT":
            powerflow.linecount += 1
            dglt(
                powerflow,
            )

        # Dados de Incremento do Nível de Carregamento
        elif powerflow.lines[powerflow.linecount].strip() == "DINC":
            powerflow.linecount += 1
            dinc(
                powerflow,
            )

        # Dados de Linha
        elif powerflow.lines[powerflow.linecount].strip() == "DLIN":
            powerflow.linecount += 1
            dlin(
                powerflow,
            )

        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{powerflow.system}`!\033[0m")
