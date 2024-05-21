# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import concatenate, exp, nan, ones, pi
from pandas import DataFrame as DF


def darq(
    powerflow,
):
    """inicialização para leitura de dados de entrada e saida de arquivos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    powerflow.darq["tipo"] = list()
    powerflow.darq["c"] = list()
    powerflow.darq["nome"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.darq["tipo"].append(powerflow.lines[powerflow.linecount][:6])
            powerflow.darq["c"].append(powerflow.lines[powerflow.linecount][7:10])
            powerflow.darq["nome"].append(powerflow.lines[powerflow.linecount][11:])
        powerflow.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    powerflow.darqDF = DF(data=powerflow.darq)
    powerflow.darq = deepcopy(powerflow.darqDF)
    powerflow.darqDF = powerflow.darqDF.replace(r"^\s*$", "0", regex=True)
    powerflow.darqDF = powerflow.darqDF.astype(
        {   
            "tipo": "object",
            "c": "object",
            "nome": "str",
        }
    )
    
    if powerflow.darqDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DARQ`!\033[0m"
        )
    else:
        powerflow.codes["DARQ"] = True


def devt(
    powerflow,
):
    """inicialização para leitura de dados de eventos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.devt["tipo"] = list()
    powerflow.devt["tempo"] = list()
    powerflow.devt["elemento"] = list()
    powerflow.devt["para"] = list()
    powerflow.devt["ncircuito"] = list()
    powerflow.devt["extremidade"] = list()
    powerflow.devt["v-percentual"] = list()
    powerflow.devt["v-absoluto"] = list()
    powerflow.devt["grupo"] = list()
    powerflow.devt["unidades"] = list()
    powerflow.devt["bloco-cdu"] = list()
    powerflow.devt["polaridade"] = list()
    powerflow.devt["resistencia"] = list()
    powerflow.devt["reatancia"] = list()
    powerflow.devt["susceptancia"] = list()
    powerflow.devt["defasagem"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.devt["tipo"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.devt["tempo"].append(powerflow.lines[powerflow.linecount][5:13])
            powerflow.devt["elemento"].append(powerflow.lines[powerflow.linecount][13:19])
            powerflow.devt["para"].append(powerflow.lines[powerflow.linecount][19:24])
            powerflow.devt["ncircuito"].append(powerflow.lines[powerflow.linecount][24:26])
            powerflow.devt["extremidade"].append(powerflow.lines[powerflow.linecount][26:31])
            powerflow.devt["v-percentual"].append(powerflow.lines[powerflow.linecount][32:37])
            powerflow.devt["v-absoluto"].append(powerflow.lines[powerflow.linecount][38:44])
            powerflow.devt["grupo"].append(powerflow.lines[powerflow.linecount][45:47])
            powerflow.devt["unidades"].append(powerflow.lines[powerflow.linecount][48:51])
            powerflow.devt["bloco-cdu"].append(powerflow.lines[powerflow.linecount][60:64])
            powerflow.devt["polaridade"].append(powerflow.lines[powerflow.linecount][64])
            powerflow.devt["resistencia"].append(powerflow.lines[powerflow.linecount][66:72])
            powerflow.devt["reatancia"].append(powerflow.lines[powerflow.linecount][73:79])
            powerflow.devt["susceptancia"].append(powerflow.lines[powerflow.linecount][80:86])
            powerflow.devt["defasagem"].append(powerflow.lines[powerflow.linecount][87:94])
        powerflow.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    powerflow.devtDF = DF(data=powerflow.devt)
    powerflow.devt = deepcopy(powerflow.devtDF)
    powerflow.devtDF = powerflow.devtDF.replace(r"^\s*$", "0", regex=True)
    powerflow.devtDF = powerflow.devtDF.astype(
        {
            "tipo": "object",
            "tempo": "float",
            "elemento": "int",
            "para": "int",
            "ncircuito": "int",
            "extremidade": "int",
            "v-percentual": "float",
            "v-absoluto": "float",
            "grupo": "int",
            "unidades": "int",
            "bloco-cdu": "int",
            "polaridade": "object",
            "resistencia": "float",
            "reatancia": "float",
            "susceptancia": "float",
            "defasagem": "float",
        }
    )
    if powerflow.devtDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DEVT`!\033[0m"
        )
    else:
        powerflow.codes["DEVT"] = True


def dsim(
    powerflow,
):
    """inicialização para leitura de dados de controle de simulação

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dsim["tmax"] = list()
    powerflow.dsim["step"] = list()
    powerflow.dsim["plot"] = list()
    powerflow.dsim["rela"] = list()
    powerflow.dsim["freq"] = list()

    while not powerflow.dsim["tmax"]:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dsim["tmax"].append(powerflow.lines[powerflow.linecount][:8])
            powerflow.dsim["step"].append(powerflow.lines[powerflow.linecount][9:14])
            powerflow.dsim["plot"].append(powerflow.lines[powerflow.linecount][15:20])
            powerflow.dsim["rela"].append(powerflow.lines[powerflow.linecount][21:26])
            powerflow.dsim["freq"].append(powerflow.lines[powerflow.linecount][27:32])
        powerflow.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    powerflow.dsimDF = DF(data=powerflow.dsim)
    powerflow.dsim = deepcopy(powerflow.dsimDF)
    powerflow.dsimDF = powerflow.dsimDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dsimDF = powerflow.dsimDF.astype(
        {
            "tmax": "float",
            "step": "float",
            "plot": "int",
            "rela": "int",
            "freq": "int",
        }
    )
    if powerflow.dsimDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DSIM`!\033[0m"
        )
    else:
        powerflow.codes["DSIM"] = True


def dmaq(
    powerflow,
):
    """inicialização para leitura de dados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    pass
    # powerflow.dmaq

    # while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
    #     if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
    #         pass
    #     else:
    #         pass
    #     powerflow.linecount += 1

    # # DataFrame dos Dados de Agregadores Genericos
    # powerflow.dmaqDF = DF(data=powerflow.dmaq)
    # powerflow.dmaq = deepcopy(powerflow.dmaqDF)
    # powerflow.dmaqDF = powerflow.dmaqDF.replace(r"^\s*$", "0", regex=True)
    # powerflow.dmaqDF = powerflow.dmaqDF.astype(
    #     {
            
    #     }
    # )
    # if powerflow.dmaqDF.empty:
    #     ## ERROR - VERMELHO
    #     raise ValueError(
    #         "\033[91mERROR: Falha na leitura de código de execução `DMAQ`!\033[0m"
    #     )
    # else:
    #     powerflow.codes["DMAQ"] = True


def blt(
    powerflow,
):
    """inicialização para leitura de dados
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
    # powerflow.blt["tipo"] = list()
