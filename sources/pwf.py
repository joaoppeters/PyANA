# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from drede import *


def pwf(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    t = time.process_time()

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

    print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")


def keywords(
    powerflow,
):
    """palavras-chave de arquivo .pwf

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.end_archive = "FIM"
    powerflow.end_block = ("9999", "99999", "999999")
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
        "TITU": False,
        "DAGR": False,
        "DANC": False,
        "DARE": False,
        "DBAR": False,
        "DBSH": False,
        "DCER": False,
        "DCTE": False,
        "DGBT": False,
        "DGER": False,
        "DGLT": False,
        "DINC": False,
        "DINJ": False,
        "DLIN": False,
        "DOPC": False,
        "DSHL": False,
    }


def readfile(
    powerflow,
):
    """leitura do arquivo .pwf

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    f = open(f"{powerflow.dirPWF}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.pwf`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Agregadores Genericos
        if powerflow.lines[powerflow.linecount].strip() == "DAGR":
            powerflow.linecount += 1
            powerflow.dagr1 = dict()
            powerflow.dagr2 = dict()
            powerflow.dagr1["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.dagr2["ruler"] = powerflow.lines[powerflow.linecount + 2][:]
            dagr(
                powerflow,
            )

        # Dados de Alteração do Nível de Carregamento
        elif powerflow.lines[powerflow.linecount].strip() == "DANC":
            powerflow.linecount += 1
            powerflow.danc = dict()
            powerflow.danc["ruler"] = powerflow.lines[powerflow.linecount][:]
            danc(
                powerflow,
            )

        # Dados de Intercâmbio de Potência Ativa entre Áreas
        elif powerflow.lines[powerflow.linecount].strip() == "DARE":
            powerflow.linecount += 1
            powerflow.dare = dict()
            powerflow.dare["ruler"] = powerflow.lines[powerflow.linecount][:]
            dare(
                powerflow,
            )

        # Dados de Barra
        elif powerflow.lines[powerflow.linecount].strip() == "DBAR":
            powerflow.linecount += 1
            powerflow.dbar = dict()
            powerflow.dbar["ruler"] = powerflow.lines[powerflow.linecount][:]
            dbar(
                powerflow,
            )

        # Dados de Bancos de Capacitores e/ou Reatores Individualizados de Barras CA ou de Linhas de Transmissão
        elif powerflow.lines[powerflow.linecount].strip() == "DBSH":
            powerflow.linecount += 1
            powerflow.dbsh1 = dict()
            powerflow.dbsh2 = dict()
            powerflow.dbsh1["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.dbsh2["ruler"] = powerflow.lines[powerflow.linecount + 2][:]
            dbsh(
                powerflow,
            )

        # Dados de Compensadores Estáticos de Potência Reativa
        elif powerflow.lines[powerflow.linecount].strip() == "DCER":
            powerflow.linecount += 1
            powerflow.dcer = dict()
            powerflow.dcer["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcer(
                powerflow,
            )

        # Dados de Constantes
        elif powerflow.lines[powerflow.linecount].strip() == "DCTE":
            powerflow.linecount += 1
            powerflow.dcte = dict()
            powerflow.dcte["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcte(
                powerflow,
            )

        # Dados de Grupo de Base de Tensão de Barras CA
        elif powerflow.lines[powerflow.linecount].strip() == "DGBT":
            powerflow.linecount += 1
            powerflow.dgbt = dict()
            powerflow.dgbt["ruler"] = powerflow.lines[powerflow.linecount][:]
            dgbt(
                powerflow,
            )

        # Dados de Geradores
        elif powerflow.lines[powerflow.linecount].strip() == "DGER":
            powerflow.linecount += 1
            powerflow.dger = dict()
            powerflow.dger["ruler"] = powerflow.lines[powerflow.linecount][:]
            dger(
                powerflow,
            )

        # Dados de Grupos de Limites de Tensão
        elif powerflow.lines[powerflow.linecount].strip() == "DGLT":
            powerflow.linecount += 1
            powerflow.dglt = dict()
            powerflow.dglt["ruler"] = powerflow.lines[powerflow.linecount][:]
            dglt(
                powerflow,
            )

        # Dados de Incremento do Nível de Carregamento
        elif powerflow.lines[powerflow.linecount].strip() == "DINC":
            powerflow.linecount += 1
            powerflow.dinc = dict()
            powerflow.dinc["ruler"] = powerflow.lines[powerflow.linecount][:]
            dinc(
                powerflow,
            )

        # Dados de Injeções de Potências, Shunts e Fatores de Participação de Geração do Modelo Equivalente
        elif powerflow.lines[powerflow.linecount].strip() == "DINJ":
            powerflow.linecount += 1
            powerflow.dinj = dict()
            powerflow.dinj["ruler"] = powerflow.lines[powerflow.linecount][:]
            dinj(
                powerflow,
            )

        # Dados de Linha
        elif powerflow.lines[powerflow.linecount].strip() == "DLIN":
            powerflow.linecount += 1
            powerflow.dlin = dict()
            powerflow.dlin["ruler"] = powerflow.lines[powerflow.linecount][:]
            dlin(
                powerflow,
            )

        # Dados de Opções de Controle e Execução Padrão
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DOPC"
            or powerflow.lines[powerflow.linecount].strip() == "DOPC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dopc = dict()
            powerflow.dopc["ruler"] = powerflow.lines[powerflow.linecount][:]
            dopc(
                powerflow,
            )

        # Dados de Dispositivos Shunt de Circuito CA
        elif powerflow.lines[powerflow.linecount].strip() == "DSHL":
            powerflow.linecount += 1
            powerflow.dshl = dict()
            powerflow.dshl["ruler"] = powerflow.lines[powerflow.linecount][:]
            dshl(
                powerflow,
            )

        # Título do Sistema/Caso em Estudo
        elif powerflow.lines[powerflow.linecount].strip() == "TITU":
            powerflow.linecount += 1
            powerflow.titu = powerflow.lines[powerflow.linecount][:]
            powerflow.codes["TITU"] = True

        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{powerflow.anarede}`!\033[0m")

    # Checa alteração do nível de carregamento
    checkdanc(
        powerflow,
    )
