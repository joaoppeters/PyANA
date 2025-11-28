# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time

from dpwf import *


def pwf(
    anarede,
    file,
):
    """inicialização

    Args
        anarede:
    """
    ## Inicialização
    t = time.process_time()

    # Variáveis
    anarede.linecount = 0

    # Funções
    keywords(
        anarede,
    )

    # Códigos
    codes(
        anarede,
    )

    # Leitura
    readfile(
        anarede,
        file,
    )

    print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")


def keywords(
    anarede,
):
    """palavras-chave de arquivo .pwf

    Args
        anarede:
    """
    ## Inicialização
    anarede.end_line = "\n"
    anarede.end_archive = "FIM"
    anarede.end_block = ("9999", "99999", "999999")
    anarede.comment = "("


def codes(
    anarede,
):
    """códigos de dados de execução implementados

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.pwfblock = dict(
        {
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
    )


def readfile(
    anarede,
    file,
):
    """leitura do arquivo .pwf

    Args
        anarede:
    """
    ## Inicialização
    f = open(f"{file}", "r", encoding="latin-1")
    anarede.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.pwf`
    while anarede.lines[anarede.linecount].strip() != anarede.end_archive:
        # Dados de Agregadores Genericos
        if (
            anarede.lines[anarede.linecount].strip() == "DAGR"
            or anarede.lines[anarede.linecount].strip() == "DAGR IMPR"
        ):
            anarede.linecount += 1
            anarede.dagr = dict()
            anarede.dagr1 = dict()
            anarede.dagr2 = dict()
            anarede.dagr["dagr"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dagr1["ruler"] = anarede.lines[anarede.linecount][:]
            anarede.dagr2["ruler"] = anarede.lines[anarede.linecount + 2][:]
            dagr(
                anarede,
            )

        # Dados de Alteração do Nível de Carregamento
        elif (
            anarede.lines[anarede.linecount].strip() == "DANC"
            or anarede.lines[anarede.linecount].strip() == "DANC IMPR"
            or anarede.lines[anarede.linecount].strip() == "DANC ACLS"
            or anarede.lines[anarede.linecount].strip() == "DANC ACLS IMPR"
        ):
            anarede.linecount += 1
            anarede.danc = dict()
            anarede.danc["danc"] = anarede.lines[anarede.linecount - 1][:]
            anarede.danc["ruler"] = anarede.lines[anarede.linecount][:]
            if "ACLS" in anarede.lines[anarede.linecount - 1].strip():
                danc_acls(
                    anarede,
                )
            else:
                danc(
                    anarede,
                )

        # Dados de Intercâmbio de Potência Ativa entre Áreas
        elif (
            anarede.lines[anarede.linecount].strip() == "DARE"
            or anarede.lines[anarede.linecount].strip() == "DARE IMPR"
        ):
            anarede.linecount += 1
            anarede.dare = dict()
            anarede.dare["dare"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dare["ruler"] = anarede.lines[anarede.linecount][:]
            dare(
                anarede,
            )

        # Dados de Barra
        elif (
            anarede.lines[anarede.linecount].strip() == "DBAR"
            or anarede.lines[anarede.linecount].strip() == "DBAR IMPR"
        ):
            anarede.linecount += 1
            anarede.dbar = dict()
            anarede.dbar["dbar"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dbar["ruler"] = anarede.lines[anarede.linecount][:]
            dbar(
                anarede,
            )

        # Dados de Bancos de Capacitores e/ou Reatores Individualizados de Barras CA ou de Linhas de Transmissão
        elif (
            anarede.lines[anarede.linecount].strip() == "DBSH"
            or anarede.lines[anarede.linecount].strip() == "DBSH IMPR"
        ):
            anarede.linecount += 1
            anarede.dbsh = dict()
            anarede.dbsh1 = dict()
            anarede.dbsh2 = dict()
            anarede.dbsh["dbsh"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dbsh1["ruler"] = anarede.lines[anarede.linecount][:]
            anarede.dbsh2["ruler"] = anarede.lines[anarede.linecount + 2][:]
            dbsh(
                anarede,
            )

        # Dados de Args da Curva de Carga
        elif (
            anarede.lines[anarede.linecount].strip() == "DCAR"
            or anarede.lines[anarede.linecount].strip() == "DCAR IMPR"
        ):
            anarede.linecount += 1
            anarede.dcar = dict()
            anarede.dcar["dcar"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcar["ruler"] = anarede.lines[anarede.linecount][:]
            dcar(
                anarede,
            )

        # Dados de Barras CC
        elif (
            anarede.lines[anarede.linecount].strip() == "DCBA"
            or anarede.lines[anarede.linecount].strip() == "DCBA IMPR"
        ):
            anarede.linecount += 1
            anarede.dcba = dict()
            anarede.dcba["dcba"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcba["ruler"] = anarede.lines[anarede.linecount][:]
            dcba(
                anarede,
            )

        # Dados de Controle de Conversor CA/CC
        elif (
            anarede.lines[anarede.linecount].strip() == "DCCV"
            or anarede.lines[anarede.linecount].strip() == "DCCV IMPR"
        ):
            anarede.linecount += 1
            anarede.dccv = dict()
            anarede.dccv["dccv"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dccv["ruler"] = anarede.lines[anarede.linecount][:]
            dccv(
                anarede,
            )

        # Dados de Compensadores Estáticos de Potência Reativa
        elif (
            anarede.lines[anarede.linecount].strip() == "DCER"
            or anarede.lines[anarede.linecount].strip() == "DCER IMPR"
        ):
            anarede.linecount += 1
            anarede.dcer = dict()
            anarede.dcer["dcer"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcer["ruler"] = anarede.lines[anarede.linecount][:]
            dcer(
                anarede,
            )

        # Dados de Linha CC
        elif (
            anarede.lines[anarede.linecount].strip() == "DCLI"
            or anarede.lines[anarede.linecount].strip() == "DCLI IMPR"
        ):
            anarede.linecount += 1
            anarede.dcli = dict()
            anarede.dcli["dcli"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcli["ruler"] = anarede.lines[anarede.linecount][:]
            dcli(
                anarede,
            )

        # Dados de Conversor CA/CC
        elif (
            anarede.lines[anarede.linecount].strip() == "DCNV"
            or anarede.lines[anarede.linecount].strip() == "DCNV IMPR"
        ):
            anarede.linecount += 1
            anarede.dcnv = dict()
            anarede.dcnv["dcnv"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcnv["ruler"] = anarede.lines[anarede.linecount][:]
            dcnv(
                anarede,
            )

        # Dados de Compensador Série Controlável
        elif (
            anarede.lines[anarede.linecount].strip() == "DCSC"
            or anarede.lines[anarede.linecount].strip() == "DCSC IMPR"
        ):
            anarede.linecount += 1
            anarede.dcsc = dict()
            anarede.dcsc["dcsc"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcsc["ruler"] = anarede.lines[anarede.linecount][:]
            dcsc(
                anarede,
            )

        # Dados de Constantes
        elif (
            anarede.lines[anarede.linecount].strip() == "DCTE"
            or anarede.lines[anarede.linecount].strip() == "DCTE IMPR"
        ):
            anarede.linecount += 1
            anarede.dcte = dict()
            anarede.dcte["dcte"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dcte["ruler"] = anarede.lines[anarede.linecount][:]
            dcte(
                anarede,
            )

        # Dados de Contingências
        elif (
            anarede.lines[anarede.linecount].strip() == "DCTG"
            or anarede.lines[anarede.linecount].strip() == "DCTG IMPR"
        ):
            anarede.linecount += 1
            anarede.dctg = dict()
            anarede.dctg1 = dict()
            anarede.dctg2 = dict()
            anarede.dctg["dctg"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dctg1["ruler"] = anarede.lines[anarede.linecount][:]
            anarede.dctg2["ruler"] = anarede.lines[anarede.linecount + 2][:]
            dctg(
                anarede,
            )

        # Dados Complementares de Transformadores
        elif (
            anarede.lines[anarede.linecount].strip() == "DCTR"
            or anarede.lines[anarede.linecount].strip() == "DCTR IMPR"
        ):
            anarede.linecount += 1
            anarede.dctr = dict()
            anarede.dctr["dctr"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dctr["ruler"] = anarede.lines[anarede.linecount][:]
            dctr(
                anarede,
            )

        # Dados de Elo CC
        elif (
            anarede.lines[anarede.linecount].strip() == "DELO"
            or anarede.lines[anarede.linecount].strip() == "DELO IMPR"
        ):
            anarede.linecount += 1
            anarede.delo = dict()
            anarede.delo["delo"] = anarede.lines[anarede.linecount - 1][:]
            anarede.delo["ruler"] = anarede.lines[anarede.linecount][:]
            delo(
                anarede,
            )

        # Dados de Grupo de Base de Tensão de Barras CA
        elif (
            anarede.lines[anarede.linecount].strip() == "DGBT"
            or anarede.lines[anarede.linecount].strip() == "DGBT IMPR"
        ):
            anarede.linecount += 1
            anarede.dgbt = dict()
            anarede.dgbt["dgbt"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dgbt["ruler"] = anarede.lines[anarede.linecount][:]
            dgbt(
                anarede,
            )

        # Dados de Geradores
        elif (
            anarede.lines[anarede.linecount].strip() == "DGER"
            or anarede.lines[anarede.linecount].strip() == "DGER IMPR"
        ):
            anarede.linecount += 1
            anarede.dger = dict()
            anarede.dger["dger"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dger["ruler"] = anarede.lines[anarede.linecount][:]
            dger(
                anarede,
            )

        # Dados de Grupos de Limites de Tensão
        elif (
            anarede.lines[anarede.linecount].strip() == "DGLT"
            or anarede.lines[anarede.linecount].strip() == "DGLT IMPR"
        ):
            anarede.linecount += 1
            anarede.dglt = dict()
            anarede.dglt["dglt"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dglt["ruler"] = anarede.lines[anarede.linecount][:]
            dglt(
                anarede,
            )

        # Dados de Incremento do Nível de Carregamento
        elif (
            anarede.lines[anarede.linecount].strip() == "DINC"
            or anarede.lines[anarede.linecount].strip() == "DINC IMPR"
        ):
            anarede.linecount += 1
            anarede.dinc = dict()
            anarede.dinc["dinc"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dinc["ruler"] = anarede.lines[anarede.linecount][:]
            dinc(
                anarede,
            )

        # Dados de Injeções de Potências, Shunts e Fatores de Participação de Geração do Modelo Equivalente
        elif (
            anarede.lines[anarede.linecount].strip() == "DINJ"
            or anarede.lines[anarede.linecount].strip() == "DINJ IMPR"
        ):
            anarede.linecount += 1
            anarede.dinj = dict()
            anarede.dinj["dinj"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dinj["ruler"] = anarede.lines[anarede.linecount][:]
            dinj(
                anarede,
            )

        # Dados de Linha CA
        elif (
            anarede.lines[anarede.linecount].strip() == "DLIN"
            or anarede.lines[anarede.linecount].strip() == "DLIN IMPR"
        ):
            anarede.linecount += 1
            anarede.dlin = dict()
            anarede.dlin["dlin"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dlin["ruler"] = anarede.lines[anarede.linecount][:]
            dlin(
                anarede,
            )

        # Dados de Monitoração para Estabilidade de Tensão em Barra CA
        elif (
            anarede.lines[anarede.linecount].strip() == "DMET"
            or anarede.lines[anarede.linecount].strip() == "DMET IMPR"
        ):
            anarede.linecount += 1
            anarede.dmte = dict()
            anarede.dmte["dmet"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dmte["ruler"] = anarede.lines[anarede.linecount][:]
            dmet(
                anarede,
            )

        # Dados de Monitoração de Fluxo em Circuito CA
        elif (
            anarede.lines[anarede.linecount].strip() == "DMFL"
            or anarede.lines[anarede.linecount].strip() == "DMFL IMPR"
            or anarede.lines[anarede.linecount].strip() == "DMFL CIRC"
            or anarede.lines[anarede.linecount].strip() == "DMFL CIRC IMPR"
        ):
            anarede.linecount += 1
            anarede.dmfl = dict()
            anarede.dmfl["dmfl"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dmfl["ruler"] = anarede.lines[anarede.linecount][:]
            if "CIRC" in anarede.lines[anarede.linecount - 1].strip():
                dmfl_circ(
                    anarede,
                )
            else:
                dmfl(
                    anarede,
                )

        # Dados de Monitoração de Tensão em Barra CA
        # elif (
        #     anarede.lines[anarede.linecount].strip() == "DMTE"
        #     or anarede.lines[anarede.linecount].strip() == "DMTE IMPR"
        # ):
        #     anarede.linecount += 1
        #     anarede.dmte = dict()
        #     anarede.dmte["dmte"] = anarede.lines[anarede.linecount - 1][:]
        #     anarede.dmte["ruler"] = anarede.lines[anarede.linecount][:]
        #     dmte(
        #         anarede,
        #     )

        # Dados de Opções de Controle e Execução Padrão
        elif (
            anarede.lines[anarede.linecount].strip() == "DOPC"
            or anarede.lines[anarede.linecount].strip() == "DOPC IMPR"
        ):
            anarede.linecount += 1
            anarede.dopc = dict()
            anarede.dopc["dopc"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dopc["ruler"] = anarede.lines[anarede.linecount][:]
            dopc(
                anarede,
            )

        # Dados de Dispositivos Shunt de Circuito CA
        elif (
            anarede.lines[anarede.linecount].strip() == "DSHL"
            or anarede.lines[anarede.linecount].strip() == "DSHL IMPR"
        ):
            anarede.linecount += 1
            anarede.dshl = dict()
            anarede.dshl["dshl"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dshl["ruler"] = anarede.lines[anarede.linecount][:]
            dshl(
                anarede,
            )

        # Dados de
        elif (
            anarede.lines[anarede.linecount].strip() == "DTPF"
            or anarede.lines[anarede.linecount].strip() == "DTPF IMPR"
            or anarede.lines[anarede.linecount].strip() == "DTPF CIRC"
            or anarede.lines[anarede.linecount].strip() == "DTPF CIRC IMPR"
        ):
            anarede.linecount += 1
            anarede.dtpf = dict()
            anarede.dtpf["dtpf"] = anarede.lines[anarede.linecount - 1][:]
            anarede.dtpf["ruler"] = anarede.lines[anarede.linecount][:]
            if "CIRC" in anarede.lines[anarede.linecount - 1].strip():
                dtpf_circ(
                    anarede,
                )
            else:
                dtpf(
                    anarede,
                )

        # Título do Sistema/Caso em Estudo
        elif (
            anarede.lines[anarede.linecount].strip() == "TITU"
            or anarede.lines[anarede.linecount].strip() == "TITU IMPR"
        ):
            anarede.linecount += 1
            anarede.titu = dict()
            anarede.titu["titu"] = anarede.lines[anarede.linecount - 1][:]
            anarede.titu["ruler"] = anarede.lines[anarede.linecount][:]
            anarede.pwfblock["TITU"] = True

        anarede.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{anarede.name + '.pwf'}`!\033[0m")

    # Checa alteração do nível de carregamento
    checkdanc(
        anarede,
    )
