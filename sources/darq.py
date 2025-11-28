# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from path import pathdarq
from dstb import *


def rdarq(
    anatem,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    anatem.dblt = dict()
    anatem.dcdu = dict()
    pathdarq(
        anatem,
    )


def rblt(
    anatem,
    arquivo,
    nome,
):
    """leitura de arquivo .blt associado ao dado de entrada DARQ

    Args
        anatem:
        arquivo:
    """
    ## Inicialização
    anatem.linecount = 0

    f = open(f"{arquivo}", "r", encoding="latin-1")
    anatem.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.stb`
    while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
        if anatem.lines[anatem.linecount].strip()[:4] == "DCST":
            anatem.linecount += 1
            if not hasattr(anatem, "dcst"):
                anatem.dcst = dict()
                anatem.dcst["dcst"] = anatem.lines[anatem.linecount - 1][:]
                anatem.dcst["ruler"] = "(No)   T (  Y1  ) (  Y2  ) (  X1  )\n"
            dcst(
                anatem,
            )

        elif anatem.lines[anatem.linecount].strip()[:4] == "DMDG":
            anatem.linecount += 1
            if not hasattr(anatem, "dmdg"):
                anatem.dmdg = dict()
                anatem.dmdg["dmdg"] = anatem.lines[anatem.linecount - 1][:]
                anatem.dmdg["md01_ruler"] = "(No)   (L'd)(Ra )( H )( D )(MVA)Fr C\n"
                anatem.dmdg["md02_ruler"] = (
                    '(No)   (CS) (Xd )(Xq )(X\'d)     (X"d)(Xl )(T\'d)     (T"d)(T"q)\n'
                )
                anatem.dmdg["md03_ruler"] = (
                    "(No)   (CS) (Xd )(Xq )(X'd)(X'q)(X\"d)(Xl )(T'd)(T'q)(T\"d)(T\"q)\n"
                )

            if anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD01":
                dmdgmd01(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD02":
                dmdgmd02(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD03":
                dmdgmd03(
                    anatem,
                )

        elif anatem.lines[anatem.linecount].strip()[:4] == "DRGV":
            anatem.linecount += 1
            if not hasattr(anatem, "drgv"):
                anatem.drgv = dict()
                anatem.drgv["drgv"] = anatem.lines[anatem.linecount - 1][:]
                anatem.drgv["md01_ruler"] = (
                    "(No)   ( R )(Rp )(At )(Qnl)(Tw )(Tr )(Tf )(Tg )(Lmn)(Lmx)(Dtb)( D )(Pbg)(Pbt)\n"
                )
                anatem.drgv["md02_ruler"] = (
                    "(No)   ( R )( T )(T1 )(T2 )(Lmn)(Lmx)(Dtb)L\n",
                    "(No)   ( R )( T )(T1 )(T2 )(Lmn)(Lmx)(Dtb)T\n",
                )
                anatem.drgv["md03_ruler"] = (
                    "(No)   (Bp )(Bt )(Tv )(T1 )(T2 )(Tw )(Lmn)(Lmx)(Tmx)(Dtb)\n"
                )
                anatem.drgv["md04_ruler"] = (
                    "(No)   (Bp )(Bt )(At )(Qnl)(Tp )(Ty )(Td )(Ts )(Tg )(Tw )(Lmn)(Lmx)\n"
                )
                anatem.drgv["md05_ruler"] = (
                    "(No)   (C1 )(C2 )(C3 )(C8 )(T3 )(T4 )(T5 )(Tc )(Tmx)(Dtb)\n"
                )
                anatem.drgv["md06_ruler"] = (
                    "(No)   (Kr )(Bp )(Bt )(Blp)(At )(Qnl)(Tn )(Tv )(Tr )(Tg )(Tlg)(Td )(Tt )\n"
                )
                anatem.drgv["md07_ruler"] = (
                    "(No)   (K0 )(K5 )(Kp1)(Kp2)(Klp)(Kp )(Bp )(Tv )(Tn )(Ta )(Tf )(Tr )(Ty )\n"
                )

            if anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD01":
                drgvmd01(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD02":
                drgvmd02(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD03":
                drgvmd03(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD04":
                drgvmd04(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD05":
                drgvmd05(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD06":
                drgvmd06(
                    anatem,
                )
            elif anatem.lines[anatem.linecount - 1].strip()[5:9] == "MD07":
                drgvmd07(
                    anatem,
                )

        anatem.linecount += 1

    print(f"\033[32mSucesso na leitura de arquivo `{nome}`!\033[0m")


def rcdu(
    anatem,
    arquivo,
    nome,
):
    """leitura de arquivo .cdu associado ao dado de entrada DARQ

    Args
        anatem:
        arquivo:
    """
    ## Inicialização
    # Variáveis
    anatem.linecount = 0

    f = open(f"{arquivo}", "r", encoding="latin-1")
    anatem.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.stb`
    while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
        if anatem.lines[anatem.linecount].strip()[:4] == "DCDU":
            anatem.linecount += 1
            anatem.dcdu["dctg"] = anatem.lines[anatem.linecount - 1][:]
            anatem.dcdu["ncdu_ruler"] = (
                "(ncdu) ( nome cdu )\n",
                "( nc ) ( nome cdu )\n",
            )
            anatem.dcdu["defpar_ruler"] = "(EFPAR (nome) (     valor      )\n"
            anatem.dcdu["bloco_ruler"] = (
                "(nb)i(tipo)o(stip)s(vent) (vsai) ( p1 )( p2 )( p3 )( p4 ) (vmin) (vmax)\n"
            )
            anatem.dcdu["defval_ruler"] = "(EFVAL (stip) (vdef) ( d1 )o( d2 )\n"
            dcdu(
                anatem,
            )
        anatem.linecount += 1

    print(f"\033[32mSucesso na leitura de arquivo `{nome}`!\033[0m")


def rdat(
    anatem,
    arquivo,
    nome,
):
    """leitura de arquivo .dat associado ao dado de entrada DARQ

    Args
        anatem:
        arquivo:
    """
    ## Inicialização
    anatem.linecount = 0

    f = open(f"{arquivo}", "r", encoding="latin-1")
    anatem.lines = f.readlines()
    f.close()

    # Loop de leitura de linhas do `.stb`
    while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
        if anatem.lines[anatem.linecount].strip()[:4] == "DGER":
            anatem.linecount += 1
            if not hasattr(anatem, "dger"):
                anatem.dger = dict()
                anatem.dger["dger"] = anatem.lines[anatem.linecount - 1][:]
                anatem.dger["ruler"] = (
                    "(tp) ( no) C (tp) ( no) C (tp) ( no) C (tp) ( no)   (A) (B) (C) (D) (VbP) (VdP) (VbQ) (VdQ)\n"
                )
            dger(
                anatem,
            )
        anatem.linecount += 1

    print(f"\033[32mSucesso na leitura de arquivo `{nome}`!\033[0m")


# def rdarq(
#     anatem,
# ):
#     """leitura de arquivos .dat e .blt associados ao dado de entrada DARQ

#     Args
#         anatem:
#     """

#     for idx, value in anatem.darqDF.iterrows():
#         if value["tipo"].split()[0] == "DAT":
#             arquivo, arquivoname = checktem(anatem, value["nome"])
#             if value["nome"].split("-")[1].strip().lower() == "dmaq.dat":
#                 dmaq(
#                     anatem,
#                     arquivo,
#                     arquivoname,
#                 )
#         if value["tipo"].split()[0] == "BLT":
#             arquivo, arquivoname = checktem(
#                 anatem,
#                 value["nome"],
#             )
#             if value["nome"].split("-")[1].strip().lower() == "uheute.blt":
#                 blt(
#                     anatem,
#                     arquivo,
#                     arquivoname,
#                 )
