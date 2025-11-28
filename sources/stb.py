# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from darq import rdarq
from dstb import *


def stb(
    anatem,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    t = time.process_time()

    # Variáveis
    anatem.linecount = 0

    # Funções
    keywords(
        anatem,
    )

    # Funções
    codes(
        anatem,
    )

    # Leitura
    rstb(
        anatem,
    )

    rdarq(
        anatem,
    )

    print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")


def keywords(
    anatem,
):
    """palavras-chave de arquivo .pwf

    Args
        anarede:
    """
    ## Inicialização
    anatem.end_line = "\n"
    anatem.end_archive = "FIM"
    anatem.end_block = (
        "9999",
        "99999",
        "999999",
    )
    anatem.comment = "("


def codes(
    anatem,
):
    """códigos de dados de execução implementados

    Args
        anatem:
    """
    ## Inicialização
    # Variável
    anatem.stbblock = dict(
        {
            "TITU": False,
            "DARQ": False,
            "DCAR": False,
            "DCTE": False,
            "DEVT": False,
            "DOPC": False,
            "DPLT": False,
            "DSIM": False,
        }
    )


def rstb(
    anatem,
):
    """leitura de arquivo .stb

    Args
        anatem:
    """
    ## Inicialização
    # Variáveis
    f = open(f"{anatem.dirSTB}", "r", encoding="latin-1")
    anatem.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.stb`
    while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
        # Dados de Arquivos de Entrada e Saida
        if anatem.lines[anatem.linecount].strip() == "DARQ":
            anatem.linecount += 1
            anatem.darq = dict()
            anatem.darq["ruler"] = anatem.lines[anatem.linecount][:]
            darq(
                anatem,
            )

        # Dados de Cargas Funcionais Estáticas
        elif (
            anatem.lines[anatem.linecount].strip() == "DCAR"
            or anatem.lines[anatem.linecount].strip() == "DCAR IMPR"
        ):
            anatem.linecount += 1
            anatem.dcar = dict()
            anatem.dcar["dcar"] = anatem.lines[anatem.linecount - 1][:]
            anatem.dcar["ruler"] = anatem.lines[anatem.linecount][:]
            dcar(
                anatem,
            )

        # Dados de Controle de Execução do Programa
        elif (
            anatem.lines[anatem.linecount].strip() == "DCTE"
            or anatem.lines[anatem.linecount].strip() == "DCTE IMPR"
        ):
            anatem.linecount += 1
            anatem.dcte = dict()
            anatem.dcte["dcte"] = anatem.lines[anatem.linecount - 1][:]
            anatem.dcte["ruler"] = anatem.lines[anatem.linecount][:]
            dcte(
                anatem,
            )

        # Dados de Eventos
        elif (
            anatem.lines[anatem.linecount].strip() == "DEVT"
            or anatem.lines[anatem.linecount].strip() == "DEVT IMPR"
        ):
            anatem.linecount += 1
            anatem.devt = dict()
            anatem.devt["ruler"] = anatem.lines[anatem.linecount][:]
            devt(
                anatem,
            )

        # Dados de Opções de Controle e Execução Padrão
        elif (
            anatem.lines[anatem.linecount].strip() == "DOPC"
            or anatem.lines[anatem.linecount].strip() == "DOPC IMPR"
        ):
            anatem.linecount += 1
            anatem.dopc = dict()
            anatem.dopc["dopc"] = anatem.lines[anatem.linecount - 1][:]
            anatem.dopc["ruler"] = anatem.lines[anatem.linecount][:]
            dopc(
                anatem,
            )

        # Dados de Variáveis para Plotagem
        elif (
            anatem.lines[anatem.linecount].strip() == "DPLT"
            or anatem.lines[anatem.linecount].strip() == "DPLT IMPR"
        ):
            anatem.linecount += 1
            anatem.dplt = dict()
            anatem.dplt["dplt"] = anatem.lines[anatem.linecount - 1][:]
            anatem.dplt["ruler"] = anatem.lines[anatem.linecount][:]
            # dplt(
            #     anatem,
            # )

        # Dados de Controle da Simulação
        elif anatem.lines[anatem.linecount].strip() == "DSIM":
            anatem.linecount += 1
            anatem.dsim = dict()
            anatem.dsim["ruler"] = anatem.lines[anatem.linecount][:]
            dsim(
                anatem,
            )

        # Título do Sistema/Caso em Estudo
        elif (
            anatem.lines[anatem.linecount].strip() == "TITU"
            or anatem.lines[anatem.linecount].strip() == "TITU IMPR"
        ):
            anatem.linecount += 1
            anatem.titu = dict()
            anatem.titu["titu"] = anatem.lines[anatem.linecount - 1][:]
            anatem.titu["ruler"] = anatem.lines[anatem.linecount][:]
            anatem.stbblock["TITU"] = True

        anatem.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{anatem.system}`!\033[0m")
