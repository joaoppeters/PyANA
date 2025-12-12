# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os import mkdir
from os.path import exists, realpath
from datetime import datetime as dt
from wdyn import wdsm


def worg(
    anarede,
    anatem,
    organon,
):
    """Inicialização

    Args
        anatem:
    """
    ## Inicialização
    # Arquivo
    organon.filedir = realpath(
        anarede.maindir + "\\sistemas\\" + anarede.name + ".dyn",
    )

    # Manipulacao
    organon.file = open(organon.filedir, "w")

    wdsm(
        anarede=anarede,
        anatem=anatem,
        organon=organon,
    )

    organon.file.close()
    cdufiles = list()
    cdufolder = realpath(anarede.maindir + "\\sistemas\\cdu2udc\\")
    if not exists(cdufolder):
        mkdir(cdufolder)

    for key in anatem.dcdu.keys():
        if key not in ['dctg', 'ncdu_ruler', 'defpar_ruler', 'bloco_ruler', 'defval_ruler']:
            nome = "CDU_" + anatem.dcdu[key]['nome'].strip() + "_" + key
            anatem.file = realpath(cdufolder + "\\" + nome + ".cdu")
            anatem.file = open(anatem.file, "w", encoding="latin-1")
            anatem.file.write("DCDU\n")
            anatem.file.write("(ncdu) ( nome cdu )\n")
            anatem.file.write(f"{key:>6} {anatem.dcdu[key]['nome']:<12}\n")
            anatem.file.write("(\n")
            anatem.file.write("(EFPAR (nome) (     valor      )\n")
            for i in range(len(anatem.dcdu[key]['defpar'])):
                anatem.file.write(
                    f"{anatem.dcdu[key]['defpar'][i]:>6} {anatem.dcdu[key]['defpar_nome'][i]:>6} {anatem.dcdu[key]['defpar_valor'][i]:>18}\n",
                )
            anatem.file.write("(\n")
            anatem.file.write("(nb)i(tipo)o(stip)s(vent) (vsai) ( p1 )( p2 )( p3 )( p4 ) (vmin) (vmax)\n")
            for i in range(len(anatem.dcdu[key]['bloco_numero'])):
                anatem.file.write(
                    f"{anatem.dcdu[key]['bloco_numero'][i]:>4}{anatem.dcdu[key]['bloco_inicializacao'][i]:1}{anatem.dcdu[key]['bloco_tipo'][i]:>6}{anatem.dcdu[key]['bloco_omitir'][i]:1}{anatem.dcdu[key]['bloco_subtipo'][i]:>6}{anatem.dcdu[key]['bloco_sinal'][i]:1}{anatem.dcdu[key]['bloco_entrada'][i]:>6} {anatem.dcdu[key]['bloco_saida'][i]:>6} {anatem.dcdu[key]['bloco_parametro1'][i]:>6}{anatem.dcdu[key]['bloco_parametro2'][i]:>6}{anatem.dcdu[key]['bloco_parametro3'][i]:>6}{anatem.dcdu[key]['bloco_parametro4'][i]:>6} {anatem.dcdu[key]['bloco_limite_minimo'][i]:>6} {anatem.dcdu[key]['bloco_limite_maximo'][i]:>6}\n",
                )
            anatem.file.write("(\n")
            anatem.file.write("(EFVAL (stip) (vdef) ( d1 )o( d2 )\n")
            for i in range(len(anatem.dcdu[key]['defval'])):
                anatem.file.write(
                    f"{anatem.dcdu[key]['defval'][i]:>6} {anatem.dcdu[key]['defval_subtipo'][i]:>6} {anatem.dcdu[key]['defval_variavel'][i]:>6} {anatem.dcdu[key]['defval_parametro_d1'][i]:>6}{anatem.dcdu[key]['defval_exclusao'][i]:1}{anatem.dcdu[key]['defval_parametro_d2'][i]:>6}\n",
                )
            anatem.file.write("(\n")
            anatem.file.write("FIMCDU\n")
            anatem.file.write("999999")
            anatem.file.close()
            cdufiles.append(nome)
    
    organon.file = realpath(cdufolder + "\\cdu2udc.spt")
    organon.file = open(organon.file, "w")
    organon.file.write(f"CHDIR {cdufolder}\n")
    for cdu in cdufiles:
        organon.file.write(f"CDU2UDC {cdu}.cdu {cdu}.udc\n")
    organon.file.close()
    pass