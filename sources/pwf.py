# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from dpwf import *


def pwf(
    powerflow,
):
    """inicialização

    Args
        powerflow:
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

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.end_line = "\n"
    powerflow.end_archive = "FIM"
    powerflow.end_block = ("9999", "99999", "999999")
    powerflow.comment = "("


def codes(
    powerflow,
):
    """códigos de dados de execução implementados

    Args
        powerflow:
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
        "DCAR": False,
        "DCBA": False,
        "DCCV": False,
        "DCER": False,
        "DCLI": False,
        "DCNV": False,
        "DCSC": False,
        "DCTE": False,
        "DCTG": False,
        "DCTR": False,
        "DELO": False,
        "DGBT": False,
        "DGER": False,
        "DGLT": False,
        "DINC": False,
        "DINJ": False,
        "DLIN": False,
        "DMET": False,
        "DMFL": False,
        "DMTE": False,
        "DOPC": False,
        "DSHL": False,
        "DTPF": False,
    }


def readfile(
    powerflow,
):
    """leitura do arquivo .pwf

    Args
        powerflow:
    """
    ## Inicialização
    f = open(f"{powerflow.dirPWF}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.pwf`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Agregadores Genericos
        if (
            powerflow.lines[powerflow.linecount].strip() == "DAGR"
            or powerflow.lines[powerflow.linecount].strip() == "DAGR IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dagr = dict()
            powerflow.dagr1 = dict()
            powerflow.dagr2 = dict()
            powerflow.dagr["dagr"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dagr1["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.dagr2["ruler"] = powerflow.lines[powerflow.linecount + 2][:]
            dagr(
                powerflow,
            )

        # Dados de Alteração do Nível de Carregamento
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DANC"
            or powerflow.lines[powerflow.linecount].strip() == "DANC IMPR"
            or powerflow.lines[powerflow.linecount].strip() == "DANC ACLS"
            or powerflow.lines[powerflow.linecount].strip() == "DANC ACLS IMPR"
        ):
            powerflow.linecount += 1
            powerflow.danc = dict()
            powerflow.danc["danc"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.danc["ruler"] = powerflow.lines[powerflow.linecount][:]
            if "ACLS" in powerflow.lines[powerflow.linecount - 1].strip():
                danc_acls(
                    powerflow,
                )
            else:
                danc(
                    powerflow,
                )

        # Dados de Intercâmbio de Potência Ativa entre Áreas
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DARE"
            or powerflow.lines[powerflow.linecount].strip() == "DARE IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dare = dict()
            powerflow.dare["dare"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dare["ruler"] = powerflow.lines[powerflow.linecount][:]
            dare(
                powerflow,
            )

        # Dados de Barra
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DBAR"
            or powerflow.lines[powerflow.linecount].strip() == "DBAR IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dbar = dict()
            powerflow.dbar["dbar"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dbar["ruler"] = powerflow.lines[powerflow.linecount][:]
            dbar(
                powerflow,
            )

        # Dados de Bancos de Capacitores e/ou Reatores Individualizados de Barras CA ou de Linhas de Transmissão
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DBSH"
            or powerflow.lines[powerflow.linecount].strip() == "DBSH IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dbsh = dict()
            powerflow.dbsh1 = dict()
            powerflow.dbsh2 = dict()
            powerflow.dbsh["dbsh"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dbsh1["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.dbsh2["ruler"] = powerflow.lines[powerflow.linecount + 2][:]
            dbsh(
                powerflow,
            )

        # Dados de Args da Curva de Carga
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCAR"
            or powerflow.lines[powerflow.linecount].strip() == "DCAR IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcar = dict()
            powerflow.dcar["dcar"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcar["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcar(
                powerflow,
            )

        # Dados de Barras CC
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCBA"
            or powerflow.lines[powerflow.linecount].strip() == "DCBA IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcba = dict()
            powerflow.dcba["dcba"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcba["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcba(
                powerflow,
            )

        # Dados de Controle de Conversor CA/CC
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCCV"
            or powerflow.lines[powerflow.linecount].strip() == "DCCV IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dccv = dict()
            powerflow.dccv["dccv"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dccv["ruler"] = powerflow.lines[powerflow.linecount][:]
            dccv(
                powerflow,
            )

        # Dados de Compensadores Estáticos de Potência Reativa
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCER"
            or powerflow.lines[powerflow.linecount].strip() == "DCER IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcer = dict()
            powerflow.dcer["dcer"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcer["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcer(
                powerflow,
            )

        # Dados de Linha CC
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCLI"
            or powerflow.lines[powerflow.linecount].strip() == "DCLI IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcli = dict()
            powerflow.dcli["dcli"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcli["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcli(
                powerflow,
            )

        # Dados de Conversor CA/CC
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCNV"
            or powerflow.lines[powerflow.linecount].strip() == "DCNV IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcnv = dict()
            powerflow.dcnv["dcnv"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcnv["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcnv(
                powerflow,
            )

        # Dados de Compensador Série Controlável
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCSC"
            or powerflow.lines[powerflow.linecount].strip() == "DCSC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcsc = dict()
            powerflow.dcsc["dcsc"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcsc["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcsc(
                powerflow,
            )

        # Dados de Constantes
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCTE"
            or powerflow.lines[powerflow.linecount].strip() == "DCTE IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dcte = dict()
            powerflow.dcte["dcte"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dcte["ruler"] = powerflow.lines[powerflow.linecount][:]
            dcte(
                powerflow,
            )

        # Dados de Contingências
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCTG"
            or powerflow.lines[powerflow.linecount].strip() == "DCTG IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dctg = dict()
            powerflow.dctg1 = dict()
            powerflow.dctg2 = dict()
            powerflow.dctg["dctg"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dctg1["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.dctg2["ruler"] = powerflow.lines[powerflow.linecount + 2][:]
            dctg(
                powerflow,
            )

        # Dados Complementares de Transformadores
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DCTR"
            or powerflow.lines[powerflow.linecount].strip() == "DCTR IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dctr = dict()
            powerflow.dctr["dctr"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dctr["ruler"] = powerflow.lines[powerflow.linecount][:]
            dctr(
                powerflow,
            )

        # Dados de Elo CC
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DELO"
            or powerflow.lines[powerflow.linecount].strip() == "DELO IMPR"
        ):
            powerflow.linecount += 1
            powerflow.delo = dict()
            powerflow.delo["delo"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.delo["ruler"] = powerflow.lines[powerflow.linecount][:]
            delo(
                powerflow,
            )

        # Dados de Grupo de Base de Tensão de Barras CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DGBT"
            or powerflow.lines[powerflow.linecount].strip() == "DGBT IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dgbt = dict()
            powerflow.dgbt["dgbt"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dgbt["ruler"] = powerflow.lines[powerflow.linecount][:]
            dgbt(
                powerflow,
            )

        # Dados de Geradores
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DGER"
            or powerflow.lines[powerflow.linecount].strip() == "DGER IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dger = dict()
            powerflow.dger["dger"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dger["ruler"] = powerflow.lines[powerflow.linecount][:]
            dger(
                powerflow,
            )

        # Dados de Grupos de Limites de Tensão
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DGLT"
            or powerflow.lines[powerflow.linecount].strip() == "DGLT IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dglt = dict()
            powerflow.dglt["dglt"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dglt["ruler"] = powerflow.lines[powerflow.linecount][:]
            dglt(
                powerflow,
            )

        # Dados de Incremento do Nível de Carregamento
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DINC"
            or powerflow.lines[powerflow.linecount].strip() == "DINC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dinc = dict()
            powerflow.dinc["dinc"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dinc["ruler"] = powerflow.lines[powerflow.linecount][:]
            dinc(
                powerflow,
            )

        # Dados de Injeções de Potências, Shunts e Fatores de Participação de Geração do Modelo Equivalente
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DINJ"
            or powerflow.lines[powerflow.linecount].strip() == "DINJ IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dinj = dict()
            powerflow.dinj["dinj"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dinj["ruler"] = powerflow.lines[powerflow.linecount][:]
            dinj(
                powerflow,
            )

        # Dados de Linha CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DLIN"
            or powerflow.lines[powerflow.linecount].strip() == "DLIN IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dlin = dict()
            powerflow.dlin["dlin"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dlin["ruler"] = powerflow.lines[powerflow.linecount][:]
            dlin(
                powerflow,
            )

        # Dados de Monitoração para Estabilidade de Tensão em Barra CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DMET"
            or powerflow.lines[powerflow.linecount].strip() == "DMET IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dmet = dict()
            powerflow.dmet["dmet"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dmet["ruler"] = powerflow.lines[powerflow.linecount][:]
            dmet(
                powerflow,
            )

        # Dados de Monitoração de Fluxo em Circuito CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DMFL"
            or powerflow.lines[powerflow.linecount].strip() == "DMFL IMPR"
            or powerflow.lines[powerflow.linecount].strip() == "DMFL CIRC"
            or powerflow.lines[powerflow.linecount].strip() == "DMFL CIRC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dmfl = dict()
            powerflow.dmfl["dmfl"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dmfl["ruler"] = powerflow.lines[powerflow.linecount][:]
            if "CIRC" in powerflow.lines[powerflow.linecount - 1].strip():
                dmfl_circ(
                    powerflow,
                )
            else:
                dmfl(
                    powerflow,
                )

        # Dados de Monitoração de Tensão em Barra CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DMTE"
            or powerflow.lines[powerflow.linecount].strip() == "DMTE IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dmte = dict()
            powerflow.dmte["dmte"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dmte["ruler"] = powerflow.lines[powerflow.linecount][:]
            dmte(
                powerflow,
            )

        # Dados de Opções de Controle e Execução Padrão
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DOPC"
            or powerflow.lines[powerflow.linecount].strip() == "DOPC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dopc = dict()
            powerflow.dopc["dopc"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dopc["ruler"] = powerflow.lines[powerflow.linecount][:]
            dopc(
                powerflow,
            )

        # Dados de Dispositivos Shunt de Circuito CA
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DSHL"
            or powerflow.lines[powerflow.linecount].strip() == "DSHL IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dshl = dict()
            powerflow.dshl["dshl"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dshl["ruler"] = powerflow.lines[powerflow.linecount][:]
            dshl(
                powerflow,
            )

        # Dados de
        elif (
            powerflow.lines[powerflow.linecount].strip() == "DTPF"
            or powerflow.lines[powerflow.linecount].strip() == "DTPF IMPR"
            or powerflow.lines[powerflow.linecount].strip() == "DTPF CIRC"
            or powerflow.lines[powerflow.linecount].strip() == "DTPF CIRC IMPR"
        ):
            powerflow.linecount += 1
            powerflow.dtpf = dict()
            powerflow.dtpf["dtpf"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.dtpf["ruler"] = powerflow.lines[powerflow.linecount][:]
            if "CIRC" in powerflow.lines[powerflow.linecount - 1].strip():
                dtpf_circ(
                    powerflow,
                )
            else:
                dtpf(
                    powerflow,
                )

        # Título do Sistema/Caso em Estudo
        elif (
            powerflow.lines[powerflow.linecount].strip() == "TITU"
            or powerflow.lines[powerflow.linecount].strip() == "TITU IMPR"
        ):
            powerflow.linecount += 1
            powerflow.titu = dict()
            powerflow.titu["titu"] = powerflow.lines[powerflow.linecount - 1][:]
            powerflow.titu["ruler"] = powerflow.lines[powerflow.linecount][:]
            powerflow.codes["TITU"] = True

        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{powerflow.anarede}`!\033[0m")

    # Checa alteração do nível de carregamento
    checkdanc(
        powerflow,
    )
