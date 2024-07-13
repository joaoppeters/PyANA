# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import concatenate, exp, nan, ones, pi
from pandas import DataFrame as DF


def dagr(
    powerflow,
):
    """inicialização para leitura de dados de agregadores genéricos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    powerflow.dagr1["numero"] = list()
    powerflow.dagr1["descricao"] = list()
    powerflow.dagr1["ndagr2"] = list()
    powerflow.dagr2["numero"] = list()
    powerflow.dagr2["operacao"] = list()
    powerflow.dagr2["descricao"] = list()
    idx = 0

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        elif powerflow.lines[powerflow.linecount - 1][:] == powerflow.dagr1["ruler"]:
            powerflow.dagr1["numero"].append(powerflow.lines[powerflow.linecount][:3])
            powerflow.dagr1["descricao"].append(
                powerflow.lines[powerflow.linecount][4:40]
            )
        elif powerflow.lines[powerflow.linecount - 1][:] == powerflow.dagr2["ruler"]:
            powerflow.dagr1["ndagr2"].append(0)
            while powerflow.lines[powerflow.linecount].strip() != "FAGR":
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dagr2["numero"].append(
                        powerflow.lines[powerflow.linecount][:3]
                    )
                    powerflow.dagr2["operacao"].append(
                        powerflow.lines[powerflow.linecount][4]
                    )
                    powerflow.dagr2["descricao"].append(
                        powerflow.lines[powerflow.linecount][6:42]
                    )
                powerflow.dagr1["ndagr2"][idx] += 1
                powerflow.linecount += 1
            idx += 1
        powerflow.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    powerflow.dagr1DF = DF(data=powerflow.dagr1)
    powerflow.dagr1 = deepcopy(powerflow.dagr1DF)
    powerflow.dagr1DF = powerflow.dagr1DF.replace(r"^\s*$", "0", regex=True)
    powerflow.dagr1DF = powerflow.dagr1DF.astype(
        {
            "numero": "int",
            "descricao": "str",
        }
    )

    powerflow.dagr2DF = DF(data=powerflow.dagr2)
    powerflow.dagr2 = deepcopy(powerflow.dagr2DF)
    powerflow.dagr2DF = powerflow.dagr2DF.replace(r"^\s*$", "0", regex=True)
    powerflow.dagr2DF = powerflow.dagr2DF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "descricao": "str",
        }
    )
    if powerflow.dagr1DF.empty or powerflow.dagr2DF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DAGR`!\033[0m"
        )
    else:
        powerflow.codes["DAGR"] = True


def danc(
    powerflow,
):
    """inicialização para leitura de dados de alteração do nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.danc["area"] = list()
    powerflow.danc["fator_carga_ativa"] = list()
    powerflow.danc["fator_carga_reativa"] = list()
    powerflow.danc["fator_shunt_barra"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.danc["area"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.danc["fator_carga_ativa"].append(
                powerflow.lines[powerflow.linecount][5:12]
            )
            powerflow.danc["fator_carga_reativa"].append(
                powerflow.lines[powerflow.linecount][12:19]
            )
            powerflow.danc["fator_shunt_barra"].append(
                powerflow.lines[powerflow.linecount][19:24]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    powerflow.dancDF = DF(data=powerflow.danc)
    powerflow.danc = deepcopy(powerflow.dancDF)
    powerflow.dancDF = powerflow.dancDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dancDF = powerflow.dancDF.astype(
        {
            "area": "int",
            "fator_carga_ativa": "float",
            "fator_carga_reativa": "float",
            "fator_shunt_barra": "float",
        }
    )
    if powerflow.dancDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m"
        )
    else:
        powerflow.codes["DANC"] = True


def danc_acls(
    powerflow,
):
    """inicialização para leitura de dados de alteração do nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.danc["tipo_elemento_1"] = list()
    powerflow.danc["identificacao_elemento_1"] = list()
    powerflow.danc["condicao_elemento_1"] = list()
    powerflow.danc["tipo_elemento_2"] = list()
    powerflow.danc["identificacao_elemento_2"] = list()
    powerflow.danc["condicao_elemento_2"] = list()
    powerflow.danc["tipo_elemento_3"] = list()
    powerflow.danc["identificacao_elemento_3"] = list()
    powerflow.danc["condicao_elemento_3"] = list()
    powerflow.danc["tipo_elemento_4"] = list()
    powerflow.danc["identificacao_elemento_4"] = list()
    powerflow.danc["fator_carga_ativa"] = list()
    powerflow.danc["fator_carga_reativa"] = list()
    powerflow.danc["fator_shunt_barra"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.danc["tipo_incremento_1"].append(
                powerflow.lines[powerflow.linecount][:4]
            )
            powerflow.danc["identificacao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][5:10]
            )
            powerflow.danc["condicao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][11]
            )
            powerflow.danc["tipo_incremento_2"].append(
                powerflow.lines[powerflow.linecount][13:17]
            )
            powerflow.danc["identificacao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][18:23]
            )
            powerflow.danc["condicao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][24]
            )
            powerflow.danc["tipo_incremento_3"].append(
                powerflow.lines[powerflow.linecount][26:30]
            )
            powerflow.danc["identificacao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][31:36]
            )
            powerflow.danc["condicao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][37]
            )
            powerflow.danc["tipo_incremento_4"].append(
                powerflow.lines[powerflow.linecount][39:43]
            )
            powerflow.danc["identificacao_incremento_4"].append(
                powerflow.lines[powerflow.linecount][44:49]
            )
            powerflow.danc["fator_carga_ativa"].append(
                powerflow.lines[powerflow.linecount][50:56]
            )
            powerflow.danc["fator_carga_reativa"].append(
                powerflow.lines[powerflow.linecount][57:63]
            )
            powerflow.danc["fator_shunt_barra"].append(
                powerflow.lines[powerflow.linecount][64:70]
            )
        powerflow.linecount += 1

    # DataFrame dos dados de Alteração do Nível de Carregamento
    powerflow.dancDF = DF(data=powerflow.danc)
    powerflow.dancDF = deepcopy(powerflow.dancDF)
    powerflow.dancDF = powerflow.dancDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dancDF = powerflow.dancDF.astype(
        {
            "tipo_incremento_1": "int",
            "identificacao_incremento_1": "int",
            "condicao_incremento_1": "object",
            "tipo_incremento_2": "int",
            "identificacao_incremento_2": "int",
            "condicao_incremento_2": "object",
            "tipo_incremento_3": "int",
            "identificacao_incremento_3": "int",
            "condicao_incremento_3": "object",
            "tipo_incremento_4": "int",
            "identificacao_incremento_4": "int",
            "fator_carga_ativa": "float",
            "fator_carga_reativa": "float",
            "fator_shunt_barra": "float",
        }
    )
    if powerflow.dancDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m"
        )
    else:
        powerflow.codes["DANC"] = True


def checkdanc(
    powerflow,
):
    """checa alteração no nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    if powerflow.codes["DANC"]:
        for area in powerflow.dancDF["area"].values:
            for idx, value in powerflow.dbarDF.iterrows():
                if value["area"] == area:
                    powerflow.dbarDF.loc[idx, "demanda_ativa"] *= (
                        1
                        + powerflow.dancDF["fator_carga_ativa"][0]
                        / powerflow.options["BASE"]
                    )
                    powerflow.dbarDF.loc[idx, "demanda_reativa"] *= (
                        1
                        + powerflow.dancDF["fator_carga_reativa"][0]
                        / powerflow.options["BASE"]
                    )
                    powerflow.dbarDF.loc[idx, "shunt_barra"] *= (
                        1
                        + powerflow.dancDF["fator_shunt_barra"][0]
                        / powerflow.options["BASE"]
                    )


def dare(
    powerflow,
):
    """inicialização para leitura de dados de intercâmbio de potência ativa entre áreas

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dare["numero"] = list()
    powerflow.dare["intercambio_liquido"] = list()
    powerflow.dare["nome"] = list()
    powerflow.dare["intercambio_minimo"] = list()
    powerflow.dare["intercambio_maximo"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dare["numero"].append(powerflow.lines[powerflow.linecount][:3])
            powerflow.dare["intercambio_liquido"].append(
                powerflow.lines[powerflow.linecount][7:13]
            )
            powerflow.dare["nome"].append(powerflow.lines[powerflow.linecount][18:54])
            powerflow.dare["intercambio_minimo"].append(
                powerflow.lines[powerflow.linecount][55:61]
            )
            powerflow.dare["intercambio_maximo"].append(
                powerflow.lines[powerflow.linecount][62:68]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    powerflow.dareDF = DF(data=powerflow.dare)
    powerflow.dare = deepcopy(powerflow.dareDF)
    powerflow.dareDF = powerflow.dareDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dareDF = powerflow.dareDF.astype(
        {
            "numero": "int",
            "intercambio_liquido": "float",
            "nome": "str",
            "intercambio_minimo": "float",
            "intercambio_maximo": "float",
        }
    )
    if powerflow.dareDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DARE`!\033[0m"
        )
    else:
        powerflow.codes["DARE"] = True

        # Numero de Areas
        powerflow.narea = powerflow.dareDF.shape[0]
        powerflow.areas = sorted(powerflow.dareDF["numero"].unique())


def dbar(
    powerflow,
):
    """inicialização para leitura de dados de barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dbar["numero"] = list()
    powerflow.dbar["operacao"] = list()
    powerflow.dbar["estado"] = list()
    powerflow.dbar["tipo"] = list()
    powerflow.dbar["grupo_base_tensao"] = list()
    powerflow.dbar["nome"] = list()
    powerflow.dbar["grupo_limite_tensao"] = list()
    powerflow.dbar["tensao"] = list()
    powerflow.dbar["angulo"] = list()
    powerflow.dbar["potencia_ativa"] = list()
    powerflow.dbar["potencia_reativa"] = list()
    powerflow.dbar["potencia_reativa_minima"] = list()
    powerflow.dbar["potencia_reativa_maxima"] = list()
    powerflow.dbar["barra_controlada"] = list()
    powerflow.dbar["demanda_ativa"] = list()
    powerflow.dbar["demanda_reativa"] = list()
    powerflow.dbar["shunt_barra"] = list()
    powerflow.dbar["area"] = list()
    powerflow.dbar["tensao_base"] = list()
    powerflow.dbar["modo"] = list()
    powerflow.dbar["agreg1"] = list()
    powerflow.dbar["agreg2"] = list()
    powerflow.dbar["agreg3"] = list()
    powerflow.dbar["agreg4"] = list()
    powerflow.dbar["agreg5"] = list()
    powerflow.dbar["agreg6"] = list()
    powerflow.dbar["agreg7"] = list()
    powerflow.dbar["agreg8"] = list()
    powerflow.dbar["agreg9"] = list()
    powerflow.dbar["agreg10"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dbar["numero"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dbar["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.dbar["estado"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dbar["tipo"].append(powerflow.lines[powerflow.linecount][7])
            powerflow.dbar["grupo_base_tensao"].append(
                powerflow.lines[powerflow.linecount][8:10]
            )
            powerflow.dbar["nome"].append(
                powerflow.lines[powerflow.linecount][10:22].split(" ")[0]
            )
            powerflow.dbar["grupo_limite_tensao"].append(
                powerflow.lines[powerflow.linecount][22:24]
            )
            powerflow.dbar["tensao"].append(powerflow.lines[powerflow.linecount][24:28])
            powerflow.dbar["angulo"].append(powerflow.lines[powerflow.linecount][28:32])
            powerflow.dbar["potencia_ativa"].append(
                powerflow.lines[powerflow.linecount][32:37]
            )
            powerflow.dbar["potencia_reativa"].append(
                powerflow.lines[powerflow.linecount][37:42]
            )
            powerflow.dbar["potencia_reativa_minima"].append(
                powerflow.lines[powerflow.linecount][42:47]
            )
            powerflow.dbar["potencia_reativa_maxima"].append(
                powerflow.lines[powerflow.linecount][47:52]
            )
            powerflow.dbar["barra_controlada"].append(
                powerflow.lines[powerflow.linecount][52:58]
            )
            powerflow.dbar["demanda_ativa"].append(
                powerflow.lines[powerflow.linecount][58:63]
            )
            powerflow.dbar["demanda_reativa"].append(
                powerflow.lines[powerflow.linecount][63:68]
            )
            powerflow.dbar["shunt_barra"].append(
                powerflow.lines[powerflow.linecount][68:73]
            )
            powerflow.dbar["area"].append(powerflow.lines[powerflow.linecount][73:76])
            powerflow.dbar["tensao_base"].append(
                powerflow.lines[powerflow.linecount][76:80]
            )
            powerflow.dbar["modo"].append(powerflow.lines[powerflow.linecount][80])
            powerflow.dbar["agreg1"].append(powerflow.lines[powerflow.linecount][81:84])
            powerflow.dbar["agreg2"].append(powerflow.lines[powerflow.linecount][84:87])
            powerflow.dbar["agreg3"].append(powerflow.lines[powerflow.linecount][87:90])
            powerflow.dbar["agreg4"].append(powerflow.lines[powerflow.linecount][90:93])
            powerflow.dbar["agreg5"].append(powerflow.lines[powerflow.linecount][93:96])
            powerflow.dbar["agreg6"].append(powerflow.lines[powerflow.linecount][96:99])
            powerflow.dbar["agreg7"].append(
                powerflow.lines[powerflow.linecount][99:102]
            )
            powerflow.dbar["agreg8"].append(
                powerflow.lines[powerflow.linecount][102:105]
            )
            powerflow.dbar["agreg9"].append(
                powerflow.lines[powerflow.linecount][105:108]
            )
            powerflow.dbar["agreg10"].append(
                powerflow.lines[powerflow.linecount][108:111]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Barra
    powerflow.dbarDF = DF(data=powerflow.dbar)
    powerflow.dbar = deepcopy(powerflow.dbarDF)
    powerflow.dbarDF = powerflow.dbarDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dbarDF = powerflow.dbarDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "estado": "object",
            "tipo": "int",
            "grupo_base_tensao": "object",
            "nome": "str",
            "grupo_limite_tensao": "object",
            "tensao": "float",
            "angulo": "float",
            "potencia_ativa": "float",
            "potencia_reativa": "float",
            "potencia_reativa_minima": "float",
            "potencia_reativa_maxima": "float",
            "barra_controlada": "int",
            "demanda_ativa": "float",
            "demanda_reativa": "float",
            "shunt_barra": "float",
            "area": "int",
            "tensao_base": "float",
            "modo": "int",
            "agreg1": "object",
            "agreg2": "object",
            "agreg3": "object",
            "agreg4": "object",
            "agreg5": "object",
            "agreg6": "object",
            "agreg7": "object",
            "agreg8": "object",
            "agreg9": "object",
            "agreg10": "object",
        }
    )
    if powerflow.dbarDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DBAR`!\033[0m"
        )
    else:
        powerflow.codes["DBAR"] = True

        # Número de barras do sistema
        powerflow.nbus = len(powerflow.dbarDF.tipo.values)

        # Barras geradoras: número & máscara
        powerflow.npv = 0
        powerflow.maskP = ones(powerflow.nbus, dtype=bool)
        powerflow.maskLp = ones(powerflow.nbus, dtype=bool)
        powerflow.maskQ = ones(powerflow.nbus, dtype=bool)
        powerflow.maskLq = ones(powerflow.nbus, dtype=bool)
        for idx, value in powerflow.dbarDF.iterrows():
            powerflow.dbarDF.at[idx, "grupo_base_tensao"] = value['grupo_base_tensao'].strip()
            powerflow.dbarDF.at[idx, "grupo_limite_tensao"] = value['grupo_limite_tensao'].strip()
            if (value["tipo"] == 2) or (value["tipo"] == 1):
                powerflow.npv += 1
                powerflow.maskQ[idx] = False

                if value["tipo"] == 2:
                    powerflow.maskP[idx] = False
                    powerflow.slackidx = idx
                    powerflow.refgen = powerflow.npv - 1

                elif value["tipo"] == 1:
                    powerflow.dbarDF.at[idx, "angulo"] = 0.0

                if value["potencia_reativa"] > value["potencia_reativa_maxima"]:
                    powerflow.dbarDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_maxima"
                    ]

                elif value["potencia_reativa"] < value["potencia_reativa_minima"]:
                    powerflow.dbarDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_minima"
                    ]

            elif value["tipo"] == 0:
                powerflow.dbarDF.at[idx, "angulo"] = 0.0

            if value["demanda_ativa"] == 0.0:
                powerflow.maskLp[idx] = False

            if value["demanda_reativa"] == 0.0:
                powerflow.maskLq[idx] = False

            if value["grupo_base_tensao"] == "0":
                powerflow.dbarDF.at[idx, "grupo_base_tensao"] = " 0"

        powerflow.mask = concatenate((powerflow.maskP, powerflow.maskQ), axis=0)

        # Número de barras PV
        powerflow.nger = powerflow.npv

        # Número de barras PQ
        powerflow.npq = powerflow.nbus - powerflow.npv

        # Tensao Base
        powerflow.dbarDF.loc[
            powerflow.dbarDF["tensao_base"] == 0.0, "tensao_base"
        ] = 1000.0

        powerflow.dbarDF = powerflow.dbarDF.reset_index()


def dbsh(
    powerflow,
):
    """inicialização para leitura de dados de bancos de capacitores e/ou reatores individualizados de barras CA ou de linhas de transmissão

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dbsh1["from"] = list()
    powerflow.dbsh1["operacao"] = list()
    powerflow.dbsh1["to"] = list()
    powerflow.dbsh1["circuito"] = list()
    powerflow.dbsh1["modo_controle"] = list()
    powerflow.dbsh1["tensao_minima"] = list()
    powerflow.dbsh1["tensao_maxima"] = list()
    powerflow.dbsh1["barra_controlada"] = list()
    powerflow.dbsh1["injecao_reativa_inicial"] = list()
    powerflow.dbsh1["tipo_controle"] = list()
    powerflow.dbsh1["apagar"] = list()
    powerflow.dbsh1["extremidade"] = list()
    powerflow.dbsh1["ndbsh2"] = list()
    powerflow.dbsh2["grupo_banco"] = list()
    powerflow.dbsh2["operacao"] = list()
    powerflow.dbsh2["estado"] = list()
    powerflow.dbsh2["unidades"] = list()
    powerflow.dbsh2["unidades_operacao"] = list()
    powerflow.dbsh2["capacitor_reator"] = list()
    powerflow.dbsh2["manobravel"] = list()
    idx = 0

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        elif powerflow.lines[powerflow.linecount - 1][:] == powerflow.dbsh1["ruler"]:
            powerflow.dbsh1["from"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dbsh1["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dbsh1["to"].append(powerflow.lines[powerflow.linecount][8:13])
            powerflow.dbsh1["circuito"].append(
                powerflow.lines[powerflow.linecount][14:16]
            )
            powerflow.dbsh1["modo_controle"].append(
                powerflow.lines[powerflow.linecount][17]
            )
            powerflow.dbsh1["tensao_minima"].append(
                powerflow.lines[powerflow.linecount][19:23]
            )
            powerflow.dbsh1["tensao_maxima"].append(
                powerflow.lines[powerflow.linecount][24:28]
            )
            powerflow.dbsh1["barra_controlada"].append(
                powerflow.lines[powerflow.linecount][29:34]
            )
            powerflow.dbsh1["injecao_reativa_inicial"].append(
                powerflow.lines[powerflow.linecount][35:41]
            )
            powerflow.dbsh1["tipo_controle"].append(
                powerflow.lines[powerflow.linecount][42]
            )
            powerflow.dbsh1["apagar"].append(powerflow.lines[powerflow.linecount][44])
            powerflow.dbsh1["extremidade"].append(
                powerflow.lines[powerflow.linecount][46:51]
            )

        elif powerflow.lines[powerflow.linecount - 1][:] == powerflow.dbsh2["ruler"]:
            powerflow.dbsh1["ndbsh2"].append(0)
            while powerflow.lines[powerflow.linecount].strip() != "FBAN":
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dbsh2["grupo_banco"].append(
                        powerflow.lines[powerflow.linecount][:2]
                    )
                    powerflow.dbsh2["operacao"].append(
                        powerflow.lines[powerflow.linecount][4]
                    )
                    powerflow.dbsh2["estado"].append(
                        powerflow.lines[powerflow.linecount][6]
                    )
                    powerflow.dbsh2["unidades"].append(
                        powerflow.lines[powerflow.linecount][8:11]
                    )
                    powerflow.dbsh2["unidades_operacao"].append(
                        powerflow.lines[powerflow.linecount][12:15]
                    )
                    powerflow.dbsh2["capacitor_reator"].append(
                        powerflow.lines[powerflow.linecount][16:22]
                    )
                    powerflow.dbsh2["manobravel"].append(
                        powerflow.lines[powerflow.linecount][23]
                    )
                powerflow.dbsh1["ndbsh2"][idx] += 1
                powerflow.linecount += 1
            idx += 1
        powerflow.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    powerflow.dbsh1DF = DF(data=powerflow.dbsh1)
    powerflow.dbsh1 = deepcopy(powerflow.dbsh1DF)
    powerflow.dbsh1DF = powerflow.dbsh1DF.replace(r"^\s*$", "0", regex=True)
    powerflow.dbsh1DF = powerflow.dbsh1DF.astype(
        {
            "from": "int",
            "operacao": "object",
            "to": "int",
            "circuito": "int",
            "modo_controle": "object",
            "tensao_minima": "int",
            "tensao_maxima": "int",
            "barra_controlada": "int",
            "injecao_reativa_inicial": "float",
            "tipo_controle": "object",
            "apagar": "object",
            "extremidade": "int",
        }
    )

    powerflow.dbsh2DF = DF(data=powerflow.dbsh2)
    powerflow.dbsh2 = deepcopy(powerflow.dbsh2DF)
    powerflow.dbsh2DF = powerflow.dbsh2DF.replace(r"^\s*$", "0", regex=True)
    powerflow.dbsh2DF = powerflow.dbsh2DF.astype(
        {
            "grupo_banco": "int",
            "operacao": "object",
            "estado": "object",
            "unidades": "int",
            "unidades_operacao": "int",
            "capacitor_reator": "float",
            "manobravel": "object",
        }
    )
    if powerflow.dbsh1DF.empty or powerflow.dbsh2DF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DBSH`!\033[0m"
        )
    else:
        powerflow.codes["DBSH"] = True

        for idx, value in powerflow.dbsh1DF.iterrows():
            if value["circuito"] == 0:
                powerflow.dbsh1DF.at[idx, "circuito"] = 1
            if value["apagar"] == "0":
                powerflow.dbsh1DF.at[idx, "apagar"] = " "


def dcar(
    powerflow,
):
    """inicialização para leitura de parâmetros A, B, C e D que estabelecem a curva de variação de carga em relação a magnitude de tensão nas barras

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcar["tipo_elemento_1"] = list()
    powerflow.dcar["identificacao_elemento_1"] = list()
    powerflow.dcar["condicao_elemento_1"] = list()
    powerflow.dcar["tipo_elemento_2"] = list()
    powerflow.dcar["identificacao_elemento_2"] = list()
    powerflow.dcar["condicao_elemento_2"] = list()
    powerflow.dcar["tipo_elemento_3"] = list()
    powerflow.dcar["identificacao_elemento_3"] = list()
    powerflow.dcar["condicao_elemento_3"] = list()
    powerflow.dcar["tipo_elemento_4"] = list()
    powerflow.dcar["identificacao_elemento_4"] = list()
    powerflow.dcar["operacao"] = list()
    powerflow.dcar["parametro_A"] = list()
    powerflow.dcar["parametro_B"] = list()
    powerflow.dcar["parametro_C"] = list()
    powerflow.dcar["parametro_D"] = list()
    powerflow.dcar["tensao_limite"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcar["tipo_incremento_1"].append(
                powerflow.lines[powerflow.linecount][:4]
            )
            powerflow.dcar["identificacao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][5:10]
            )
            powerflow.dcar["condicao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][11]
            )
            powerflow.dcar["tipo_incremento_2"].append(
                powerflow.lines[powerflow.linecount][13:17]
            )
            powerflow.dcar["identificacao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][18:23]
            )
            powerflow.dcar["condicao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][24]
            )
            powerflow.dcar["tipo_incremento_3"].append(
                powerflow.lines[powerflow.linecount][26:30]
            )
            powerflow.dcar["identificacao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][31:36]
            )
            powerflow.dcar["condicao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][37]
            )
            powerflow.dcar["tipo_incremento_4"].append(
                powerflow.lines[powerflow.linecount][39:43]
            )
            powerflow.dcar["identificacao_incremento_4"].append(
                powerflow.lines[powerflow.linecount][44:49]
            )
            powerflow.dcar["operacao"].append(powerflow.lines[powerflow.linecount][50])
            powerflow.dcar["parametro_A"].append(
                powerflow.lines[powerflow.linecount][52:55]
            )
            powerflow.dcar["parametro_B"].append(
                powerflow.lines[powerflow.linecount][56:59]
            )
            powerflow.dcar["parametro_C"].append(
                powerflow.lines[powerflow.linecount][60:63]
            )
            powerflow.dcar["parametro_D"].append(
                powerflow.lines[powerflow.linecount][64:67]
            )
            powerflow.dcar["tensao_limite"].append(
                powerflow.options["VFLD"]
                if powerflow.lines[powerflow.linecount][68:72] == 4 * " "
                else powerflow.lines[powerflow.linecount][68:72]
            )
        powerflow.linecount += 1

    # DataFrame dos dados de Incremento do Nível de Carregamento
    powerflow.dcarDF = DF(data=powerflow.dcar)
    powerflow.dcarDF = deepcopy(powerflow.dcarDF)
    powerflow.dcarDF = powerflow.dcarDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcarDF = powerflow.dcarDF.astype(
        {
            "tipo_incremento_1": "object",
            "identificacao_incremento_1": "int",
            "condicao_incremento_1": "object",
            "tipo_incremento_2": "object",
            "identificacao_incremento_2": "int",
            "condicao_incremento_2": "object",
            "tipo_incremento_3": "object",
            "identificacao_incremento_3": "int",
            "condicao_incremento_3": "object",
            "tipo_incremento_4": "object",
            "identificacao_incremento_4": "int",
            "operacao": "object",
            "parametro_A": "int",
            "parametro_B": "int",
            "parametro_C": "int",
            "parametro_D": "int",
            "tensao_limite": "float",
        }
    )
    if powerflow.dcarDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCAR`!\033[0m"
        )
    else:
        powerflow.codes["DCAR"] = True


def dcba(
    powerflow,
):
    """inicialização para leitura de dados de barra CC

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcba["numero"] = list()
    powerflow.dcba["operacao"] = list()
    powerflow.dcba["tipo"] = list()
    powerflow.dcba["polaridade"] = list()
    powerflow.dcba["nome"] = list()
    powerflow.dcba["grupo_limite_tensao"] = list()
    powerflow.dcba["tensao"] = list()
    powerflow.dcba["eletrodo_terra"] = list()
    powerflow.dcba["numero_elo_cc"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcba["numero"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dcba["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.dcba["tipo"].append(powerflow.lines[powerflow.linecount][7])
            powerflow.dcba["polaridade"].append(powerflow.lines[powerflow.linecount][8])
            powerflow.dcba["nome"].append(powerflow.lines[powerflow.linecount][9:21])
            powerflow.dcba["grupo_limite_tensao"].append(
                powerflow.lines[powerflow.linecount][21:23]
            )
            powerflow.dcba["tensao"].append(powerflow.lines[powerflow.linecount][23:28])
            powerflow.dcba["eletrodo_terra"].append(
                powerflow.lines[powerflow.linecount][66:71]
            )
            powerflow.dcba["numero_elo_cc"].append(
                powerflow.lines[powerflow.linecount][71:75]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Barra CC
    powerflow.dcbaDF = DF(data=powerflow.dcba)
    powerflow.dcba = deepcopy(powerflow.dcbaDF)
    powerflow.dcbaDF = powerflow.dcbaDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcbaDF = powerflow.dcbaDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "tipo": "int",
            "polaridade": "object",
            "nome": "str",
            "grupo_limite_tensao": "object",
            "tensao": "float",
            "eletrodo_terra": "object",
            "numero_elo_cc": "int",
        }
    )
    if powerflow.dcbaDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCBA`!\033[0m"
        )
    else:
        powerflow.codes["DCBA"] = True


def dccv(
    powerflow,
):
    """inicialização para leitura de dados de controle de conversores CA/CC

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dccv["numero"] = list()
    powerflow.dccv["operacao"] = list()
    powerflow.dccv["folga"] = list()
    powerflow.dccv["modo_controle_inversor"] = list()
    powerflow.dccv["tipo_controle_conversor"] = list()
    powerflow.dccv["valor_especificado"] = list()
    powerflow.dccv["margem_corrente"] = list()
    powerflow.dccv["maxima_sobrecorrente"] = list()
    powerflow.dccv["angulo_conversor"] = list()
    powerflow.dccv["angulo_conversor_minimo"] = list()
    powerflow.dccv["angulo_conversor_maximo"] = list()
    powerflow.dccv["tap_transformador_minimo"] = list()
    powerflow.dccv["tap_transformador_maximo"] = list()
    powerflow.dccv["tap_transformador_numero"] = list()
    powerflow.dccv["tensao_cc_minima"] = list()
    powerflow.dccv["tap_high"] = list()
    powerflow.dccv["tap_reduzido"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dccv["numero"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dccv["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.dccv["folga"].append(powerflow.lines[powerflow.linecount][7])
            powerflow.dccv["modo_controle_inversor"].append(
                powerflow.lines[powerflow.linecount][8]
            )
            powerflow.dccv["tipo_controle_conversor"].append(
                powerflow.lines[powerflow.linecount][9]
            )
            powerflow.dccv["valor_especificado"].append(
                powerflow.lines[powerflow.linecount][11:16]
            )
            powerflow.dccv["margem_corrente"].append(
                powerflow.lines[powerflow.linecount][17:22]
            )
            powerflow.dccv["maxima_sobrecorrente"].append(
                powerflow.lines[powerflow.linecount][23:28]
            )
            powerflow.dccv["angulo_conversor"].append(
                powerflow.lines[powerflow.linecount][29:34]
            )
            powerflow.dccv["angulo_conversor_minimo"].append(
                powerflow.lines[powerflow.linecount][35:40]
            )
            powerflow.dccv["angulo_conversor_maximo"].append(
                powerflow.lines[powerflow.linecount][41:46]
            )
            powerflow.dccv["tap_transformador_minimo"].append(
                powerflow.lines[powerflow.linecount][47:52]
            )
            powerflow.dccv["tap_transformador_maximo"].append(
                powerflow.lines[powerflow.linecount][53:58]
            )
            powerflow.dccv["tap_transformador_numero"].append(
                powerflow.lines[powerflow.linecount][59:61]
            )
            powerflow.dccv["tensao_cc_minima"].append(
                powerflow.lines[powerflow.linecount][62:66]
            )
            powerflow.dccv["tap_high"].append(
                powerflow.lines[powerflow.linecount][67:72]
            )
            powerflow.dccv["tap_reduzido"].append(
                powerflow.lines[powerflow.linecount][73:78]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Controle de Conversores de Tensão CC
    powerflow.dccvDF = DF(data=powerflow.dccv)
    powerflow.dccv = deepcopy(powerflow.dccvDF)
    powerflow.dccvDF = powerflow.dccvDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dccvDF = powerflow.dccvDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "folga": "object",
            "modo_controle_inversor": "object",
            "tipo_controle_conversor": "object",
            "valor_especificado": "float",
            "margem_corrente": "float",
            "maxima_sobrecorrente": "float",
            "angulo_conversor": "float",
            "angulo_conversor_minimo": "float",
            "angulo_conversor_maximo": "float",
            "tap_transformador_minimo": "float",
            "tap_transformador_maximo": "float",
            "tap_transformador_numero": "int",
            "tensao_cc_minima": "float",
            "tap_high": "object",
            "tap_reduzido": "object",
        }
    )

    if powerflow.dccvDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCCV`!\033[0m"
        )
    else:
        powerflow.codes["DCCV"] = True


def dcer(
    powerflow,
):
    """inicialização para leitura de dados de compensadores estáticos de potência reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcer["barra"] = list()
    powerflow.dcer["operacao"] = list()
    powerflow.dcer["grupo_base"] = list()
    powerflow.dcer["unidades"] = list()
    powerflow.dcer["barra_controlada"] = list()
    powerflow.dcer["droop"] = list()
    powerflow.dcer["potencia_reativa"] = list()
    powerflow.dcer["potencia_reativa_minima"] = list()
    powerflow.dcer["potencia_reativa_maxima"] = list()
    powerflow.dcer["controle"] = list()
    powerflow.dcer["estado"] = list()
    powerflow.dcer["modo_correcao_limites"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcer["barra"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dcer["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dcer["grupo_base"].append(
                powerflow.lines[powerflow.linecount][8:10]
            )
            powerflow.dcer["unidades"].append(
                powerflow.lines[powerflow.linecount][11:13]
            )
            powerflow.dcer["barra_controlada"].append(
                powerflow.lines[powerflow.linecount][14:19]
            )
            powerflow.dcer["droop"].append(powerflow.lines[powerflow.linecount][20:26])
            powerflow.dcer["potencia_reativa"].append(
                powerflow.lines[powerflow.linecount][27:32]
            )
            powerflow.dcer["potencia_reativa_minima"].append(
                powerflow.lines[powerflow.linecount][32:37]
            )
            powerflow.dcer["potencia_reativa_maxima"].append(
                powerflow.lines[powerflow.linecount][37:42]
            )
            powerflow.dcer["controle"].append(powerflow.lines[powerflow.linecount][43])
            powerflow.dcer["estado"].append(powerflow.lines[powerflow.linecount][45])
            powerflow.dcer["modo_correcao_limites"].append(
                powerflow.lines[powerflow.linecount][47]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados dos Compensadores Estáticos de Potência Reativa
    powerflow.dcerDF = DF(data=powerflow.dcer)
    powerflow.dcer = deepcopy(powerflow.dcerDF)
    powerflow.dcerDF = powerflow.dcerDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcerDF = powerflow.dcerDF.astype(
        {
            "barra": "int",
            "operacao": "object",
            "grupo_base": "object",
            "unidades": "int",
            "barra_controlada": "int",
            "droop": "float",
            "potencia_reativa": "float",
            "potencia_reativa_minima": "float",
            "potencia_reativa_maxima": "float",
            "controle": "object",
            "estado": "object",
        }
    )
    if powerflow.dcerDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código e execução `DCER`!\033[0m"
        )
    else:
        powerflow.codes["DCER"] = True

        # Número de Compensadores Estáticos de Potência Reativa
        powerflow.ncer = 0
        for idx, value in powerflow.dcerDF.iterrows():
            if value["estado"] == "D":
                powerflow.dcerDF = powerflow.dcerDF.drop(
                    labels=idx,
                    axis=0,
                )

            elif ((value["estado"] == "0") or (value["estado"] == "L")) and (
                (value["controle"] == "0")
                or (value["controle"] == "P")
                or (value["controle"] == "I")
            ):
                powerflow.ncer += 1
                powerflow.dcerDF.at[idx, "droop"] = -value["droop"] / (
                    1e2 * value["unidades"]
                )

                if value["barra_controlada"] == 0:
                    powerflow.dcerDF.at[idx, "barra_controlada"] = value["barra"]

                if value["potencia_reativa"] > value["potencia_reativa_maxima"]:
                    powerflow.dcerDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_maxima"
                    ]

                elif value["potencia_reativa"] < value["potencia_reativa_minima"]:
                    powerflow.dcerDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_minima"
                    ]

                if value["controle"] == "0":
                    powerflow.dcerDF.at[idx, "controle"] = "P"

            elif ((value["estado"] == "0") or (value["estado"] == "L")) and (
                value["controle"] == "A"
            ):
                powerflow.ncer += 1
                powerflow.dcerDF.at[idx, "droop"] = -value["droop"] / (
                    1e2 * value["unidades"]
                )

                if value["barra_controlada"] == 0:
                    powerflow.dcerDF.at[idx, "barra_controlada"] = value["barra"]


def dcli(
    powerflow,
):
    """inicialização para leitura de dados de linhas de transmissão CC

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcli["de"] = list()
    powerflow.dcli["operacao"] = list()
    powerflow.dcli["para"] = list()
    powerflow.dcli["circuito"] = list()
    powerflow.dcli["proprietario"] = list()
    powerflow.dcli["resistencia"] = list()
    powerflow.dcli["indutancia"] = list()
    powerflow.dcli["capacidade"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcli["de"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dcli["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.dcli["para"].append(powerflow.lines[powerflow.linecount][8:12])
            powerflow.dcli["circuito"].append(
                powerflow.lines[powerflow.linecount][12:14]
            )
            powerflow.dcli["proprietario"].append(
                powerflow.lines[powerflow.linecount][15]
            )
            powerflow.dcli["resistencia"].append(
                powerflow.lines[powerflow.linecount][17:23]
            )
            powerflow.dcli["indutancia"].append(
                powerflow.lines[powerflow.linecount][23:29]
            )
            powerflow.dcli["capacidade"].append(
                powerflow.lines[powerflow.linecount][60:64]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Linhas de Transmissão CC
    powerflow.dcliDF = DF(data=powerflow.dcli)
    powerflow.dcli = deepcopy(powerflow.dcliDF)
    powerflow.dcliDF = powerflow.dcliDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcliDF = powerflow.dcliDF.astype(
        {
            "de": "int",
            "operacao": "object",
            "para": "int",
            "circuito": "int",
            "proprietario": "object",
            "resistencia": "float",
            "indutancia": "float",
            "capacidade": "float",
        }
    )

    if powerflow.dcliDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCLI`!\033[0m"
        )
    else:
        powerflow.codes["DCLI"] = True


def dcnv(
    powerflow,
):
    """inicialização para leitura de dados de conversores CA/CC

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcnv["numero"] = list()
    powerflow.dcnv["operacao"] = list()
    powerflow.dcnv["barra_CA"] = list()
    powerflow.dcnv["barra_CC"] = list()
    powerflow.dcnv["barra_neutra"] = list()
    powerflow.dcnv["modo_operacao"] = list()
    powerflow.dcnv["pontes"] = list()
    powerflow.dcnv["corrente"] = list()
    powerflow.dcnv["reatancia_comutacao"] = list()
    powerflow.dcnv["tensao_secundario"] = list()
    powerflow.dcnv["potencia_transformador"] = list()
    powerflow.dcnv["resistencia_reator"] = list()
    powerflow.dcnv["indutancia_reator"] = list()
    powerflow.dcnv["capacitancia"] = list()
    powerflow.dcnv["frequencia"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcnv["numero"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dcnv["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.dcnv["barra_CA"].append(
                powerflow.lines[powerflow.linecount][7:12]
            )
            powerflow.dcnv["barra_CC"].append(
                powerflow.lines[powerflow.linecount][13:17]
            )
            powerflow.dcnv["barra_neutra"].append(
                powerflow.lines[powerflow.linecount][18:22]
            )
            powerflow.dcnv["modo_operacao"].append(
                powerflow.lines[powerflow.linecount][23]
            )
            powerflow.dcnv["pontes"].append(powerflow.lines[powerflow.linecount][25])
            powerflow.dcnv["corrente"].append(
                powerflow.lines[powerflow.linecount][27:32]
            )
            powerflow.dcnv["reatancia_comutacao"].append(
                powerflow.lines[powerflow.linecount][33:38]
            )
            powerflow.dcnv["tensao_secundario"].append(
                powerflow.lines[powerflow.linecount][39:44]
            )
            powerflow.dcnv["potencia_transformador"].append(
                powerflow.lines[powerflow.linecount][45:50]
            )
            powerflow.dcnv["resistencia_reator"].append(
                powerflow.lines[powerflow.linecount][51:56]
            )
            powerflow.dcnv["indutancia_reator"].append(
                powerflow.lines[powerflow.linecount][57:62]
            )
            powerflow.dcnv["capacitancia"].append(
                powerflow.lines[powerflow.linecount][63:68]
            )
            powerflow.dcnv["frequencia"].append(
                powerflow.lines[powerflow.linecount][69:71]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Conversores CA/CC
    powerflow.dcnvDF = DF(data=powerflow.dcnv)
    powerflow.dcnv = deepcopy(powerflow.dcnvDF)
    powerflow.dcnvDF = powerflow.dcnvDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcnvDF = powerflow.dcnvDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "barra_CA": "int",
            "barra_CC": "int",
            "barra_neutra": "int",
            "modo_operacao": "object",
            "pontes": "int",
            "corrente": "float",
            "reatancia_comutacao": "float",
            "tensao_secundario": "float",
            "potencia_transformador": "float",
            "resistencia_reator": "float",
            "indutancia_reator": "float",
            "capacitancia": "float",
            "frequencia": "float",
        }
    )

    if powerflow.dcnvDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCNV`!\033[0m"
        )
    else:
        powerflow.codes["DCNV"] = True


def dcsc(
    powerflow,
):
    """inicialização para leitura de dados de compensador série controlável

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcsc["de"] = list()
    powerflow.dcsc["operacao"] = list()
    powerflow.dcsc["para"] = list()
    powerflow.dcsc["circuito"] = list()
    powerflow.dcsc["estado"] = list()
    powerflow.dcsc["proprietario"] = list()
    powerflow.dcsc["bypass"] = list()
    powerflow.dcsc["reatancia_minima"] = list()
    powerflow.dcsc["reatancia_maxima"] = list()
    powerflow.dcsc["reatancia_inicial"] = list()
    powerflow.dcsc["modo_controle"] = list()
    powerflow.dcsc["especificado"] = list()
    powerflow.dcsc["extremidade"] = list()
    powerflow.dcsc["estagios"] = list()
    powerflow.dcsc["capacidade_normal"] = list()
    powerflow.dcsc["capacidade_emergencia"] = list()
    powerflow.dcsc["capacidade"] = list()
    powerflow.dcsc["agreg1"] = list()
    powerflow.dcsc["agreg2"] = list()
    powerflow.dcsc["agreg3"] = list()
    powerflow.dcsc["agreg4"] = list()
    powerflow.dcsc["agreg5"] = list()
    powerflow.dcsc["agreg6"] = list()
    powerflow.dcsc["agreg7"] = list()
    powerflow.dcsc["agreg8"] = list()
    powerflow.dcsc["agreg9"] = list()
    powerflow.dcsc["agreg10"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcsc["de"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dcsc["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dcsc["para"].append(powerflow.lines[powerflow.linecount][9:14])
            powerflow.dcsc["circuito"].append(
                powerflow.lines[powerflow.linecount][14:16]
            )
            powerflow.dcsc["estado"].append(powerflow.lines[powerflow.linecount][16])
            powerflow.dcsc["proprietario"].append(
                powerflow.lines[powerflow.linecount][17]
            )
            powerflow.dcsc["bypass"].append(powerflow.lines[powerflow.linecount][18])
            powerflow.dcsc["reatancia_minima"].append(
                powerflow.lines[powerflow.linecount][25:31]
            )
            powerflow.dcsc["reatancia_maxima"].append(
                powerflow.lines[powerflow.linecount][31:37]
            )
            powerflow.dcsc["reatancia_inicial"].append(
                powerflow.lines[powerflow.linecount][37:43]
            )
            powerflow.dcsc["modo_controle"].append(
                powerflow.lines[powerflow.linecount][43]
            )
            powerflow.dcsc["especificado"].append(
                powerflow.lines[powerflow.linecount][45:51]
            )
            powerflow.dcsc["extremidade"].append(
                powerflow.lines[powerflow.linecount][52:57]
            )
            powerflow.dcsc["estagios"].append(
                powerflow.lines[powerflow.linecount][57:60]
            )
            powerflow.dcsc["capacidade_normal"].append(
                powerflow.lines[powerflow.linecount][60:64]
            )
            powerflow.dcsc["capacidade_emergencia"].append(
                powerflow.lines[powerflow.linecount][64:68]
            )
            powerflow.dcsc["capacidade"].append(
                powerflow.lines[powerflow.linecount][68:72]
            )
            powerflow.dcsc["agreg1"].append(powerflow.lines[powerflow.linecount][72:75])
            powerflow.dcsc["agreg2"].append(powerflow.lines[powerflow.linecount][75:78])
            powerflow.dcsc["agreg3"].append(powerflow.lines[powerflow.linecount][78:81])
            powerflow.dcsc["agreg4"].append(powerflow.lines[powerflow.linecount][81:84])
            powerflow.dcsc["agreg5"].append(powerflow.lines[powerflow.linecount][84:87])
            powerflow.dcsc["agreg6"].append(powerflow.lines[powerflow.linecount][87:90])
            powerflow.dcsc["agreg7"].append(powerflow.lines[powerflow.linecount][90:93])
            powerflow.dcsc["agreg8"].append(powerflow.lines[powerflow.linecount][93:96])
            powerflow.dcsc["agreg9"].append(powerflow.lines[powerflow.linecount][96:99])
            powerflow.dcsc["agreg10"].append(
                powerflow.lines[powerflow.linecount][99:102]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Compensador Série Controlável
    powerflow.dcscDF = DF(data=powerflow.dcsc)
    powerflow.dcsc = deepcopy(powerflow.dcscDF)
    powerflow.dcscDF = powerflow.dcscDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcscDF = powerflow.dcscDF.astype(
        {
            "de": "int",
            "operacao": "object",
            "para": "int",
            "circuito": "int",
            "estado": "object",
            "proprietario": "object",
            "bypass": "object",
            "reatancia_minima": "float",
            "reatancia_maxima": "float",
            "reatancia_inicial": "float",
            "modo_controle": "object",
            "especificado": "object",
            "extremidade": "object",
            "estagios": "int",
            "capacidade_normal": "float",
            "capacidade_emergencia": "float",
            "capacidade": "float",
            "agreg1": "int",
            "agreg2": "int",
            "agreg3": "int",
            "agreg4": "int",
            "agreg5": "int",
            "agreg6": "int",
            "agreg7": "int",
            "agreg8": "int",
            "agreg9": "int",
            "agreg10": "int",
        }
    )

    if powerflow.dcscDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCSC`!\033[0m"
        )
    else:
        powerflow.codes["DCSC"] = True


def dcte(
    powerflow,
):
    """inicialização para leitura de dados de constantes

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dcte["constante"] = list()
    powerflow.dcte["valor_constante"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dcte["constante"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][5:11]
            )
            powerflow.dcte["constante"].append(
                powerflow.lines[powerflow.linecount][12:16]
            )
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][17:23]
            )
            powerflow.dcte["constante"].append(
                powerflow.lines[powerflow.linecount][24:28]
            )
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][29:35]
            )
            powerflow.dcte["constante"].append(
                powerflow.lines[powerflow.linecount][36:40]
            )
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][41:47]
            )
            powerflow.dcte["constante"].append(
                powerflow.lines[powerflow.linecount][48:52]
            )
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][53:59]
            )
            powerflow.dcte["constante"].append(
                powerflow.lines[powerflow.linecount][60:64]
            )
            powerflow.dcte["valor_constante"].append(
                powerflow.lines[powerflow.linecount][65:71]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Constantes
    powerflow.dcteDF = DF(data=powerflow.dcte)
    powerflow.dcte = deepcopy(powerflow.dcteDF)
    powerflow.dcteDF = powerflow.dcteDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dcteDF = powerflow.dcteDF.astype(
        {
            "constante": "object",
            "valor_constante": "float",
        }
    )
    if powerflow.dcteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTE`!\033[0m"
        )
    else:
        powerflow.codes["DCTE"] = True

        powerflow.dcteDF["constante"] = powerflow.dcteDF["constante"].replace("0", nan)
        powerflow.dcteDF = powerflow.dcteDF.dropna(axis=0, subset=["constante"])
        powerflow.dcteDF = powerflow.dcteDF.drop_duplicates(
            subset=["constante"], keep="last"
        ).reset_index(drop=True)


def dctg(
    powerflow,
):
    """inicialização para leitura de lista de casos de contingência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def dctr(
    powerflow,
):
    """inicialização para leitura de dados complementares de transformadores

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dctr["de"] = list()
    powerflow.dctr["operacao"] = list()
    powerflow.dctr["para"] = list()
    powerflow.dctr["circuito"] = list()
    powerflow.dctr["tensao_minima"] = list()
    powerflow.dctr["tensao_maxima"] = list()
    powerflow.dctr["tipo_controle_1"] = list()
    powerflow.dctr["modo_controle"] = list()
    powerflow.dctr["fase_minima"] = list()
    powerflow.dctr["fase_maxima"] = list()
    powerflow.dctr["tipo_controle_2"] = list()
    powerflow.dctr["valor_especificado"] = list()
    powerflow.dctr["extremidade"] = list()
    powerflow.dctr["taps"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dctr["de"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dctr["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dctr["para"].append(powerflow.lines[powerflow.linecount][8:13])
            powerflow.dctr["circuito"].append(
                powerflow.lines[powerflow.linecount][14:16]
            )
            powerflow.dctr["tensao_minima"].append(
                powerflow.lines[powerflow.linecount][17:21]
            )
            powerflow.dctr["tensao_maxima"].append(
                powerflow.lines[powerflow.linecount][22:26]
            )
            powerflow.dctr["tipo_controle_1"].append(
                powerflow.lines[powerflow.linecount][27]
            )
            powerflow.dctr["modo_controle"].append(
                powerflow.lines[powerflow.linecount][29]
            )
            powerflow.dctr["fase_minima"].append(
                powerflow.lines[powerflow.linecount][31:37]
            )
            powerflow.dctr["fase_maxima"].append(
                powerflow.lines[powerflow.linecount][38:44]
            )
            powerflow.dctr["tipo_controle_2"].append(
                powerflow.lines[powerflow.linecount][45]
            )
            powerflow.dctr["valor_especificado"].append(
                powerflow.lines[powerflow.linecount][47:53]
            )
            powerflow.dctr["extremidade"].append(
                powerflow.lines[powerflow.linecount][54:59]
            )
            powerflow.dctr["taps"].append(powerflow.lines[powerflow.linecount][60:62])
        powerflow.linecount += 1

    # DataFrame dos Dados Complementares de Transformadores
    powerflow.dctrDF = DF(data=powerflow.dctr)
    powerflow.dctr = deepcopy(powerflow.dctrDF)
    powerflow.dctrDF = powerflow.dctrDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dctrDF = powerflow.dctrDF.astype(
        {
            "de": "int",
            "operacao": "object",
            "para": "int",
            "circuito": "int",
            "tensao_minima": "float",
            "tensao_maxima": "float",
            "tipo_controle_1": "object",
            "modo_controle": "object",
            "fase_minima": "float",
            "fase_maxima": "float",
            "tipo_controle_2": "object",
            "valor_especificado": "float",
            "extremidade": "object",
            "taps": "int",
        }
    )

    if powerflow.dctrDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTR`!\033[0m"
        )
    else:
        powerflow.codes["DCTR"] = True


def delo(
    powerflow,
):
    """inicialização para leitura de dados de elo CC

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.delo["numero"] = list()
    powerflow.delo["operacao"] = list()
    powerflow.delo["tensao"] = list()
    powerflow.delo["base"] = list()
    powerflow.delo["nome"] = list()
    powerflow.delo["modo_high"] = list()
    powerflow.delo["estado"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.delo["numero"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.delo["operacao"].append(powerflow.lines[powerflow.linecount][5])
            powerflow.delo["tensao"].append(powerflow.lines[powerflow.linecount][7:12])
            powerflow.delo["base"].append(powerflow.lines[powerflow.linecount][13:18])
            powerflow.delo["nome"].append(powerflow.lines[powerflow.linecount][19:39])
            powerflow.delo["modo_high"].append(powerflow.lines[powerflow.linecount][40])
            powerflow.delo["estado"].append(powerflow.lines[powerflow.linecount][42])
        powerflow.linecount += 1

    # DataFrame dos Dados de Elo CC
    powerflow.deloDF = DF(data=powerflow.delo)
    powerflow.delo = deepcopy(powerflow.deloDF)
    powerflow.deloDF = powerflow.deloDF.replace(r"^\s*$", "0", regex=True)
    powerflow.deloDF = powerflow.deloDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "tensao": "float",
            "base": "float",
            "nome": "object",
            "modo_high": "object",
            "estado": "object",
        }
    )

    if powerflow.deloDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DELO`!\033[0m"
        )
    else:
        powerflow.codes["DELO"] = True


def dgbt(
    powerflow,
):
    """inicialização para leitura de dados de grupos de base de tensão de barras CA

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dgbt["grupo"] = list()
    powerflow.dgbt["tensao"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dgbt["grupo"].append(powerflow.lines[powerflow.linecount][:2])
            powerflow.dgbt["tensao"].append(powerflow.lines[powerflow.linecount][3:8])
        powerflow.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    powerflow.dgbtDF = DF(data=powerflow.dgbt)
    powerflow.dgbt = deepcopy(powerflow.dgbtDF)
    powerflow.dgbtDF = powerflow.dgbtDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dgbtDF = powerflow.dgbtDF.astype(
        {
            "grupo": "object",
            "tensao": "float",
        }
    )
    if powerflow.dgbtDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGBT`!\033[0m"
        )
    else:
        powerflow.codes["DGBT"] = True

        for idx, value in powerflow.dgbtDF.iterrows():
            powerflow.dgbtDF.at[idx, "grupo"] = value['grupo'].strip()
            if value["tensao"] == 0.0:
                powerflow.dgbtDF.at[idx, "tensao"] = 1.0


def dger(
    powerflow,
):
    """inicialização para leitura de dados de geradores

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dger["numero"] = list()
    powerflow.dger["operacao"] = list()
    powerflow.dger["potencia_ativa_minima"] = list()
    powerflow.dger["potencia_ativa_maxima"] = list()
    powerflow.dger["fator_participacao"] = list()
    powerflow.dger["fator_participacao_controle_remoto"] = list()
    powerflow.dger["fator_potencia_nominal"] = list()
    powerflow.dger["fator_servico_armadura"] = list()
    powerflow.dger["fator_servico_rotor"] = list()
    powerflow.dger["angulo_maximo_carga"] = list()
    powerflow.dger["reatancia_maquina"] = list()
    powerflow.dger["potencia_aparente_nominal"] = list()
    powerflow.dger["estatismo"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dger["numero"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dger["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dger["potencia_ativa_minima"].append(
                powerflow.lines[powerflow.linecount][8:14]
            )
            powerflow.dger["potencia_ativa_maxima"].append(
                powerflow.lines[powerflow.linecount][15:21]
            )
            powerflow.dger["fator_participacao"].append(
                powerflow.lines[powerflow.linecount][22:27]
            )
            powerflow.dger["fator_participacao_controle_remoto"].append(
                powerflow.lines[powerflow.linecount][28:33]
            )
            powerflow.dger["fator_potencia_nominal"].append(
                powerflow.lines[powerflow.linecount][34:39]
            )
            powerflow.dger["fator_servico_armadura"].append(
                powerflow.lines[powerflow.linecount][40:44]
            )
            powerflow.dger["fator_servico_rotor"].append(
                powerflow.lines[powerflow.linecount][45:49]
            )
            powerflow.dger["angulo_maximo_carga"].append(
                powerflow.lines[powerflow.linecount][50:54]
            )
            powerflow.dger["reatancia_maquina"].append(
                powerflow.lines[powerflow.linecount][55:60]
            )
            powerflow.dger["potencia_aparente_nominal"].append(
                powerflow.lines[powerflow.linecount][61:66]
            )
            powerflow.dger["estatismo"].append(
                powerflow.lines[powerflow.linecount][66:72]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Geradores
    powerflow.dgerDF = DF(data=powerflow.dger)
    powerflow.dger = deepcopy(powerflow.dgerDF)
    powerflow.dgerDF = powerflow.dgerDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dgerDF = powerflow.dgerDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "potencia_ativa_minima": "float",
            "potencia_ativa_maxima": "float",
            "fator_participacao": "float",
            "fator_participacao_controle_remoto": "float",
            "fator_potencia_nominal": "float",
            "fator_servico_armadura": "float",
            "fator_servico_rotor": "float",
            "angulo_maximo_carga": "float",
            "reatancia_maquina": "float",
            "potencia_aparente_nominal": "float",
            "estatismo": "float",
        }
    )
    if powerflow.dgerDF.empty:  # or (powerflow.dgerDF.shape[0] != powerflow.nger):
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGER`!\033[0m"
        )
    else:
        powerflow.codes["DGER"] = True

        powerflow.dgerDF["fator_participacao"] = powerflow.dgerDF[
            "fator_participacao"
        ].apply(lambda x: x * 1e-2)

        powerflow.nger = powerflow.dgerDF.shape[0]


def dglt(
    powerflow,
):
    """inicialização para leitura de dados de grupos de limites de tensão

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dglt["grupo"] = list()
    powerflow.dglt["limite_minimo"] = list()
    powerflow.dglt["limite_maximo"] = list()
    powerflow.dglt["limite_minimo_E"] = list()
    powerflow.dglt["limite_maximo_E"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dglt["grupo"].append(powerflow.lines[powerflow.linecount][:2])
            powerflow.dglt["limite_minimo"].append(
                powerflow.lines[powerflow.linecount][3:8]
            )
            powerflow.dglt["limite_maximo"].append(
                powerflow.lines[powerflow.linecount][9:14]
            )
            powerflow.dglt["limite_minimo_E"].append(
                powerflow.lines[powerflow.linecount][15:20]
            )
            powerflow.dglt["limite_maximo_E"].append(
                powerflow.lines[powerflow.linecount][21:26]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    powerflow.dgltDF = DF(data=powerflow.dglt)
    powerflow.dglt = deepcopy(powerflow.dgltDF)
    powerflow.dgltDF = powerflow.dgltDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dgltDF = powerflow.dgltDF.astype(
        {
            "grupo": "object",
            "limite_minimo": "float",
            "limite_maximo": "float",
            "limite_minimo_E": "float",
            "limite_maximo_E": "float",
        }
    )
    if powerflow.dgltDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGLT`!\033[0m"
        )
    else:
        powerflow.codes["DGLT"] = True

        for idx, value in powerflow.dgltDF.iterrows():
            powerflow.dgltDF.at[idx, "grupo"] = value['grupo'].strip()
            if value["limite_minimo"] == 0.0:
                powerflow.dgltDF.at[idx, "limite_minimo"] = 0.8

            if value["limite_maximo"] == 0.0:
                powerflow.dgltDF.at[idx, "limite_maximo"] = 1.2

            if value["limite_minimo_E"] == 0.0:
                powerflow.dgltDF.at[idx, "limite_minimo_E"] = value["limite_minimo"]
            elif value["limite_maximo_E"] == 0.0:
                powerflow.dgltDF.at[idx, "limite_maximo_E"] = value["limite_maximo"]


def dinc(
    powerflow,
):
    """inicialização para leitura de dados de incremento do nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dinc["tipo_incremento_1"] = list()
    powerflow.dinc["identificacao_incremento_1"] = list()
    powerflow.dinc["condicao_incremento_1"] = list()
    powerflow.dinc["tipo_incremento_2"] = list()
    powerflow.dinc["identificacao_incremento_2"] = list()
    powerflow.dinc["condicao_incremento_2"] = list()
    powerflow.dinc["tipo_incremento_3"] = list()
    powerflow.dinc["identificacao_incremento_3"] = list()
    powerflow.dinc["condicao_incremento_3"] = list()
    powerflow.dinc["tipo_incremento_4"] = list()
    powerflow.dinc["identificacao_incremento_4"] = list()
    powerflow.dinc["condicao_incremento_4"] = list()
    powerflow.dinc["passo_incremento_potencia_ativa"] = list()
    powerflow.dinc["passo_incremento_potencia_reativa"] = list()
    powerflow.dinc["maximo_incremento_potencia_ativa"] = list()
    powerflow.dinc["maximo_incremento_potencia_reativa"] = list()
    powerflow.dinc["tratamento_incremento_potencia_ativa"] = list()
    powerflow.dinc["tratamento_incremento_potencia_reativa"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dinc["tipo_incremento_1"].append(
                powerflow.lines[powerflow.linecount][:4]
            )
            powerflow.dinc["identificacao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][5:10]
            )
            powerflow.dinc["condicao_incremento_1"].append(
                powerflow.lines[powerflow.linecount][11]
            )
            powerflow.dinc["tipo_incremento_2"].append(
                powerflow.lines[powerflow.linecount][13:17]
            )
            powerflow.dinc["identificacao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][18:23]
            )
            powerflow.dinc["condicao_incremento_2"].append(
                powerflow.lines[powerflow.linecount][24]
            )
            powerflow.dinc["tipo_incremento_3"].append(
                powerflow.lines[powerflow.linecount][26:30]
            )
            powerflow.dinc["identificacao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][31:36]
            )
            powerflow.dinc["condicao_incremento_3"].append(
                powerflow.lines[powerflow.linecount][37]
            )
            powerflow.dinc["tipo_incremento_4"].append(
                powerflow.lines[powerflow.linecount][39:43]
            )
            powerflow.dinc["identificacao_incremento_4"].append(
                powerflow.lines[powerflow.linecount][44:49]
            )
            powerflow.dinc["condicao_incremento_4"].append(
                powerflow.lines[powerflow.linecount][50]
            )
            powerflow.dinc["passo_incremento_potencia_ativa"].append(
                powerflow.lines[powerflow.linecount][52:57]
            )
            powerflow.dinc["passo_incremento_potencia_reativa"].append(
                powerflow.lines[powerflow.linecount][58:63]
            )
            powerflow.dinc["maximo_incremento_potencia_ativa"].append(
                powerflow.lines[powerflow.linecount][64:69]
            )
            powerflow.dinc["maximo_incremento_potencia_reativa"].append(
                powerflow.lines[powerflow.linecount][70:75]
            )
            powerflow.dinc["tratamento_incremento_potencia_ativa"].append(
                False if powerflow.lines[powerflow.linecount][64:69] != "" else True
            )
            powerflow.dinc["tratamento_incremento_potencia_reativa"].append(
                False if powerflow.lines[powerflow.linecount][70:75] != "" else True
            )
        powerflow.linecount += 1

    # DataFrame dos dados de Incremento do Nível de Carregamento
    powerflow.dincDF = DF(data=powerflow.dinc)
    powerflow.dincDF = deepcopy(powerflow.dincDF)
    powerflow.dincDF = powerflow.dincDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dincDF = powerflow.dincDF.astype(
        {
            "tipo_incremento_1": "object",
            "identificacao_incremento_1": "int",
            "condicao_incremento_1": "object",
            "tipo_incremento_2": "object",
            "identificacao_incremento_2": "int",
            "condicao_incremento_2": "object",
            "tipo_incremento_3": "object",
            "identificacao_incremento_3": "int",
            "condicao_incremento_3": "object",
            "tipo_incremento_4": "object",
            "identificacao_incremento_4": "int",
            "condicao_incremento_4": "object",
            "passo_incremento_potencia_ativa": "float",
            "passo_incremento_potencia_reativa": "float",
            "maximo_incremento_potencia_ativa": "float",
            "maximo_incremento_potencia_reativa": "float",
            "tratamento_incremento_potencia_ativa": "bool",
            "tratamento_incremento_potencia_reativa": "bool",
        }
    )
    if powerflow.dincDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DINC`!\033[0m"
        )
    else:
        powerflow.codes["DINC"] = True

        for idx, value in powerflow.dincDF.iterrows():
            powerflow.dincDF.at[idx, "passo_incremento_potencia_ativa"] *= 1e-2
            if value["tratamento_incremento_potencia_ativa"]:
                powerflow.dincDF.at[idx, "maximo_incremento_potencia_ativa"] = 99.99
            else:
                powerflow.dincDF.at[idx, "maximo_incremento_potencia_ativa"] *= 1e-2

            powerflow.dincDF.at[idx, "passo_incremento_potencia_reativa"] *= 1e-2
            if value["tratamento_incremento_potencia_reativa"]:
                powerflow.dincDF.at[idx, "maximo_incremento_potencia_reativa"] = 99.99
            else:
                powerflow.dincDF.at[idx, "maximo_incremento_potencia_reativa"] *= 1e-2


def dinj(
    powerflow,
):
    """inicialização para leitura de dados de injeções de potências, shunts e fatores de participação de geração do modelo equivalente

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dinj["numero"] = list()
    powerflow.dinj["operacao"] = list()
    powerflow.dinj["injecao_ativa_eq"] = list()
    powerflow.dinj["injecao_reativa_eq"] = list()
    powerflow.dinj["shunt_eq"] = list()
    powerflow.dinj["fator_participacao_eq"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dinj["numero"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dinj["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dinj["injecao_ativa_eq"].append(
                powerflow.lines[powerflow.linecount][8:15]
            )
            powerflow.dinj["injecao_reativa_eq"].append(
                powerflow.lines[powerflow.linecount][15:22]
            )
            powerflow.dinj["shunt_eq"].append(
                powerflow.lines[powerflow.linecount][22:29]
            )
            powerflow.dinj["fator_participacao_eq"].append(
                powerflow.lines[powerflow.linecount][29:36]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Injeção de Potências, Shunts e Fatores de Participação de Geração do Modelo Equivalente
    powerflow.dinjDF = DF(data=powerflow.dinj)
    powerflow.dinj = deepcopy(powerflow.dinjDF)
    powerflow.dinjDF = powerflow.dinjDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dinjDF = powerflow.dinjDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "injecao_ativa_eq": "float",
            "injecao_reativa_eq": "float",
            "shunt_eq": "float",
            "fator_participacao_eq": "float",
        }
    )
    if powerflow.dinjDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DINJ`!\033[0m"
        )
    else:
        powerflow.codes["DINJ"] = True
        # precision = lambda x: tuple(len(p) for p in str(x).split("."))

        # for idx, value in powerflow.dinjDF.iterrows():
        #     precision(powerflow.dinj.injecao_ativa_eq[idx])
        #     precision(powerflow.dinj.injecao_reativa_eq[idx])
        #     precision(powerflow.dinj.shunt_eq[idx])
        #     powerflow.dbarDF.loc[
        #         powerflow.dbarDF["numero"] == value["numero"], "demanda_ativa"
        #     ] += -value["injecao_ativa_eq"]

        #     powerflow.dbarDF.loc[
        #         powerflow.dbarDF["numero"] == value["numero"], "demanda_reativa"
        #     ] += (-value["injecao_reativa_eq"] + value["shunt_eq"])

        #     # powerflow.dbarDF.loc[
        #     #     powerflow.dbarDF["numero"] == value["numero"], "shunt_barra"
        #     # ] += round(value["shunt_eq"])

        #     if powerflow.codes["DGER"]:
        #         powerflow.dgerDF.loc[
        #             powerflow.dbarDF["numero"] == value["numero"],
        #             "fator_participacao",
        #         ] += value["fator_participacao_eq"]

        # powerflow.dbar.demanda_ativa = powerflow.dbarDF.demanda_ativa.values
        # powerflow.dbar.demanda_reativa = powerflow.dbarDF.demanda_reativa.values
        # powerflow.dbar.shunt_barra = powerflow.dbarDF.shunt_barra.values


def dlin(
    powerflow,
):
    """inicialização para leitura de dados de linha de transmissão CA

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dlin["de"] = list()
    powerflow.dlin["abertura_de"] = list()
    powerflow.dlin["operacao"] = list()
    powerflow.dlin["abertura_para"] = list()
    powerflow.dlin["para"] = list()
    powerflow.dlin["circuito"] = list()
    powerflow.dlin["estado"] = list()
    powerflow.dlin["proprietario"] = list()
    powerflow.dlin["manobravel"] = list()
    powerflow.dlin["resistencia"] = list()
    powerflow.dlin["reatancia"] = list()
    powerflow.dlin["susceptancia"] = list()
    powerflow.dlin["tap"] = list()
    powerflow.dlin["tap_minimo"] = list()
    powerflow.dlin["tap_maximo"] = list()
    powerflow.dlin["tap_defasagem"] = list()
    powerflow.dlin["barra_controlada"] = list()
    powerflow.dlin["capacidade_normal"] = list()
    powerflow.dlin["capacidade_emergencial"] = list()
    powerflow.dlin["numero_taps"] = list()
    powerflow.dlin["capacidade_equipamento"] = list()
    powerflow.dlin["agreg1"] = list()
    powerflow.dlin["agreg2"] = list()
    powerflow.dlin["agreg3"] = list()
    powerflow.dlin["agreg4"] = list()
    powerflow.dlin["agreg5"] = list()
    powerflow.dlin["agreg6"] = list()
    powerflow.dlin["agreg7"] = list()
    powerflow.dlin["agreg8"] = list()
    powerflow.dlin["agreg9"] = list()
    powerflow.dlin["agreg10"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dlin["de"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dlin["abertura_de"].append(
                powerflow.lines[powerflow.linecount][5]
            )
            powerflow.dlin["operacao"].append(powerflow.lines[powerflow.linecount][7])
            powerflow.dlin["abertura_para"].append(
                powerflow.lines[powerflow.linecount][9]
            )
            powerflow.dlin["para"].append(powerflow.lines[powerflow.linecount][10:15])
            powerflow.dlin["circuito"].append(
                powerflow.lines[powerflow.linecount][15:17]
            )
            powerflow.dlin["estado"].append(powerflow.lines[powerflow.linecount][17])
            powerflow.dlin["proprietario"].append(
                powerflow.lines[powerflow.linecount][18]
            )
            powerflow.dlin["manobravel"].append(
                powerflow.lines[powerflow.linecount][19]
            )
            powerflow.dlin["resistencia"].append(
                powerflow.lines[powerflow.linecount][20:26]
            )
            powerflow.dlin["reatancia"].append(
                powerflow.lines[powerflow.linecount][26:32]
            )
            powerflow.dlin["susceptancia"].append(
                powerflow.lines[powerflow.linecount][32:38]
            )
            powerflow.dlin["tap"].append(powerflow.lines[powerflow.linecount][38:43])
            powerflow.dlin["tap_minimo"].append(
                powerflow.lines[powerflow.linecount][43:48]
            )
            powerflow.dlin["tap_maximo"].append(
                powerflow.lines[powerflow.linecount][48:53]
            )
            powerflow.dlin["tap_defasagem"].append(
                powerflow.lines[powerflow.linecount][53:58]
            )
            powerflow.dlin["barra_controlada"].append(
                powerflow.lines[powerflow.linecount][58:64]
            )
            powerflow.dlin["capacidade_normal"].append(
                powerflow.lines[powerflow.linecount][64:68]
            )
            powerflow.dlin["capacidade_emergencial"].append(
                powerflow.lines[powerflow.linecount][68:72]
            )
            powerflow.dlin["numero_taps"].append(
                powerflow.lines[powerflow.linecount][72:74]
            )
            powerflow.dlin["capacidade_equipamento"].append(
                powerflow.lines[powerflow.linecount][74:78]
            )
            powerflow.dlin["agreg1"].append(powerflow.lines[powerflow.linecount][78:81])
            powerflow.dlin["agreg2"].append(powerflow.lines[powerflow.linecount][81:84])
            powerflow.dlin["agreg3"].append(powerflow.lines[powerflow.linecount][84:87])
            powerflow.dlin["agreg4"].append(powerflow.lines[powerflow.linecount][87:90])
            powerflow.dlin["agreg5"].append(powerflow.lines[powerflow.linecount][90:93])
            powerflow.dlin["agreg6"].append(powerflow.lines[powerflow.linecount][93:96])
            powerflow.dlin["agreg7"].append(powerflow.lines[powerflow.linecount][96:99])
            powerflow.dlin["agreg8"].append(
                powerflow.lines[powerflow.linecount][99:102]
            )
            powerflow.dlin["agreg9"].append(
                powerflow.lines[powerflow.linecount][102:105]
            )
            powerflow.dlin["agreg10"].append(
                powerflow.lines[powerflow.linecount][105:108]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Linha
    powerflow.dlinDF = DF(data=powerflow.dlin)
    powerflow.dlin = deepcopy(powerflow.dlinDF)
    powerflow.dlinDF = powerflow.dlinDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dlinDF = powerflow.dlinDF.astype(
        {
            "de": "int",
            "abertura_de": "object",
            "operacao": "object",
            "abertura_para": "object",
            "para": "int",
            "circuito": "object",
            "estado": "object",
            "proprietario": "object",
            "manobravel": "object",
            "resistencia": "float",
            "reatancia": "float",
            "susceptancia": "float",
            "tap": "float",
            "tap_minimo": "float",
            "tap_maximo": "float",
            "tap_defasagem": "float",
            "barra_controlada": "int",
            "capacidade_normal": "float",
            "capacidade_emergencial": "float",
            "numero_taps": "int",
            "capacidade_equipamento": "float",
            "agreg1": "object",
            "agreg2": "object",
            "agreg3": "object",
            "agreg4": "object",
            "agreg5": "object",
            "agreg6": "object",
            "agreg7": "object",
            "agreg8": "object",
            "agreg9": "object",
            "agreg10": "object",
        }
    )
    if powerflow.dlinDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DLIN`!\033[0m"
        )
    else:
        powerflow.codes["DLIN"] = True

        powerflow.dlinDF["resistencia"] *= 1e-2
        powerflow.dlinDF["reatancia"] *= 1e-2
        powerflow.dlinDF["susceptancia"] /= (
            2
            * powerflow.dcteDF.loc[
                powerflow.dcteDF.constante == "BASE"
            ].valor_constante[0]
        )

        powerflow.dlinDF["estado"] = (powerflow.dlinDF["estado"] == "0") | (
            powerflow.dlinDF["estado"] == "L"
        )
        powerflow.dlinDF["transf"] = (
            powerflow.dlinDF["tap"] != 0.0
        ) & powerflow.dlinDF["estado"]

        powerflow.dlinDF["tap"] = powerflow.dlinDF["tap"].tolist() + 1 * (
            ~powerflow.dlinDF["transf"].values
        )
        powerflow.dlinDF["tapp"] = deepcopy(powerflow.dlinDF["tap"])
        powerflow.dlinDF["tap"] = powerflow.dlinDF["tap"] * exp(
            1j * pi / 180 * powerflow.dlinDF["tap_defasagem"]
        )  ## add phase shifters

        # Número de barras do sistema
        powerflow.nlin = len(powerflow.dlinDF.de.values)

        powerflow.dlinDF["de-idx"] = powerflow.dlinDF["de"].map(
            powerflow.dbarDF.set_index("numero")["index"]
        )
        powerflow.dlinDF["para-idx"] = powerflow.dlinDF["para"].map(
            powerflow.dbarDF.set_index("numero")["index"]
        )


def dopc(
    powerflow,
):
    """inicialização para leitura de dados de código de opções de controle e execução padrão

    Parâmetros
        powerflow:
    """
    ## Inicialização
    powerflow.dopc["opcao"] = list()
    powerflow.dopc["padrao"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            try:
                powerflow.dopc["opcao"].append(powerflow.lines[powerflow.linecount][:4])
                powerflow.dopc["padrao"].append(powerflow.lines[powerflow.linecount][5])
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][7:11]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][12]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][14:18]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][19]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][21:25]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][26]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][28:32]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][33]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][35:39]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][40]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][42:46]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][47]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][49:53]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][54]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][56:60]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][61]
                )
                powerflow.dopc["opcao"].append(
                    powerflow.lines[powerflow.linecount][63:67]
                )
                powerflow.dopc["padrao"].append(
                    powerflow.lines[powerflow.linecount][68]
                )
            except:
                powerflow.dopc["opcao"] = powerflow.dopc["opcao"][:-1]
                break
        powerflow.linecount += 1

    # DataFrame dos Dados de Constantes
    powerflow.dopcDF = DF(data=powerflow.dopc)
    powerflow.dopc = deepcopy(powerflow.dopcDF)
    powerflow.dopcDF = powerflow.dopcDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dopcDF = powerflow.dopcDF.astype(
        {
            "opcao": "object",
            "padrao": "object",
        }
    )
    if powerflow.dopcDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DOPC`!\033[0m"
        )
    else:
        powerflow.codes["DOPC"] = True

        powerflow.dopcDF["opcao"] = powerflow.dopcDF["opcao"].replace("0", nan)
        powerflow.dopcDF = powerflow.dopcDF.dropna(axis=0, subset=["opcao"])
        powerflow.dopcDF = powerflow.dopcDF.drop_duplicates(
            subset=["opcao"], keep="last"
        ).reset_index(drop=True)


def dshl(
    powerflow,
):
    """inicialização para leitura de dados de dispositivos shunt de circuito CA

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    powerflow.dshl["from"] = list()
    powerflow.dshl["operacao"] = list()
    powerflow.dshl["to"] = list()
    powerflow.dshl["circuito"] = list()
    powerflow.dshl["shunt_from"] = list()
    powerflow.dshl["shunt_to"] = list()
    powerflow.dshl["estado_shunt_from"] = list()
    powerflow.dshl["estado_shunt_to"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dshl["from"].append(powerflow.lines[powerflow.linecount][:5])
            powerflow.dshl["operacao"].append(powerflow.lines[powerflow.linecount][6])
            powerflow.dshl["to"].append(powerflow.lines[powerflow.linecount][9:14])
            powerflow.dshl["circuito"].append(
                powerflow.lines[powerflow.linecount][14:16]
            )
            powerflow.dshl["shunt_from"].append(
                powerflow.lines[powerflow.linecount][17:23]
            )
            powerflow.dshl["shunt_to"].append(
                powerflow.lines[powerflow.linecount][23:29]
            )
            powerflow.dshl["estado_shunt_from"].append(
                powerflow.lines[powerflow.linecount][30:32]
            )
            powerflow.dshl["estado_shunt_to"].append(
                powerflow.lines[powerflow.linecount][33:35]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Constantes
    powerflow.dshlDF = DF(data=powerflow.dshl)
    powerflow.dshl = deepcopy(powerflow.dshlDF)
    powerflow.dshlDF = powerflow.dshlDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dshlDF = powerflow.dshlDF.astype(
        {
            "from": "int",
            "operacao": "object",
            "to": "int",
            "circuito": "object",
            "shunt_from": "float",
            "shunt_to": "float",
            "estado_shunt_from": "object",
            "estado_shunt_to": "object",
        }
    )
    if powerflow.dshlDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DSHL`!\033[0m"
        )
    else:
        powerflow.codes["DSHL"] = True


def dtpf(
    powerflow,
):
    """inicialização para leitura de dados de fixação na aplicação do controle de tensão por variação automática de tap

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtpf["tipo_elemento_1"] = list()
    powerflow.dtpf["identificacao_elemento_1"] = list()
    powerflow.dtpf["condicao_elemento_1"] = list()
    powerflow.dtpf["tipo_elemento_2"] = list()
    powerflow.dtpf["identificacao_elemento_2"] = list()
    powerflow.dtpf["condicao_elemento_2"] = list()
    powerflow.dtpf["tipo_elemento_3"] = list()
    powerflow.dtpf["identificacao_elemento_3"] = list()
    powerflow.dtpf["condicao_elemento_3"] = list()
    powerflow.dtpf["tipo_elemento_4"] = list()
    powerflow.dtpf["identificacao_elemento_4"] = list()
    powerflow.dtpf["operacao"] = list()
    powerflow.dtpf["interligacao"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dtpf["tipo_elemento_1"].append(
                powerflow.lines[powerflow.linecount][:4]
            )
            powerflow.dtpf["identificacao_elemento_1"].append(
                powerflow.lines[powerflow.linecount][5:10]
            )
            powerflow.dtpf["condicao_elemento_1"].append(
                powerflow.lines[powerflow.linecount][11]
            )
            powerflow.dtpf["tipo_elemento_2"].append(
                powerflow.lines[powerflow.linecount][13:17]
            )
            powerflow.dtpf["identificacao_elemento_2"].append(
                powerflow.lines[powerflow.linecount][18:23]
            )
            powerflow.dtpf["condicao_elemento_2"].append(
                powerflow.lines[powerflow.linecount][24]
            )
            powerflow.dtpf["tipo_elemento_3"].append(
                powerflow.lines[powerflow.linecount][26:30]
            )
            powerflow.dtpf["identificacao_elemento_3"].append(
                powerflow.lines[powerflow.linecount][31:36]
            )
            powerflow.dtpf["condicao_elemento_3"].append(
                powerflow.lines[powerflow.linecount][37]
            )
            powerflow.dtpf["tipo_elemento_4"].append(
                powerflow.lines[powerflow.linecount][39:43]
            )
            powerflow.dtpf["identificacao_elemento_4"].append(
                powerflow.lines[powerflow.linecount][44:49]
            )
            powerflow.dtpf["operacao"].append(powerflow.lines[powerflow.linecount][50])
            powerflow.dtpf["interligacao"].append(
                powerflow.lines[powerflow.linecount][52]
            )
        powerflow.linecount += 1

    # DataFrame dos dados de Fixação na Aplicação do Controle de Tensão por Variação Automática de Tap
    powerflow.dtpfDF = DF(data=powerflow.dtpf)
    powerflow.dtpf = deepcopy(powerflow.dtpfDF)
    powerflow.dtpfDF = powerflow.dtpfDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dtpfDF = powerflow.dtpfDF.astype(
        {
            "tipo_elemento_1": "object",
            "identificacao_elemento_1": "int",
            "condicao_elemento_1": "object",
            "tipo_elemento_2": "object",
            "identificacao_elemento_2": "int",
            "condicao_elemento_2": "object",
            "tipo_elemento_3": "object",
            "identificacao_elemento_3": "int",
            "condicao_elemento_3": "object",
            "tipo_elemento_4": "object",
            "identificacao_elemento_4": "int",
            "operacao": "object",
            "interligacao": "float",
        }
    )
    if powerflow.dtpfDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DTPF`!\033[0m"
        )
    else:
        powerflow.codes["DTPF"] = True


def dtpf_circ(
    powerflow,
):
    """inicialização para leitura de dados de fixação na aplicação do controle de tensão por variação automática de tap

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtpf["de"] = list()
    powerflow.dtpf["para"] = list()
    powerflow.dtpf["circuito"] = list()
    powerflow.dtpf["operacao"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            try:
                powerflow.dtpf["de"].append(powerflow.lines[powerflow.linecount][:5])
                powerflow.dtpf["para"].append(
                    powerflow.lines[powerflow.linecount][6:11]
                )
                powerflow.dtpf["circuito"].append(
                    powerflow.lines[powerflow.linecount][12:14]
                )
                powerflow.dtpf["operacao"].append(
                    powerflow.lines[powerflow.linecount][75]
                )
                powerflow.dtpf["de"].append(powerflow.lines[powerflow.linecount][15:20])
                powerflow.dtpf["para"].append(
                    powerflow.lines[powerflow.linecount][21:26]
                )
                powerflow.dtpf["circuito"].append(
                    powerflow.lines[powerflow.linecount][27:29]
                )
                powerflow.dtpf["operacao"].append(
                    powerflow.lines[powerflow.linecount][75]
                )
                powerflow.dtpf["de"].append(powerflow.lines[powerflow.linecount][30:35])
                powerflow.dtpf["para"].append(
                    powerflow.lines[powerflow.linecount][36:41]
                )
                powerflow.dtpf["circuito"].append(
                    powerflow.lines[powerflow.linecount][42:44]
                )
                powerflow.dtpf["operacao"].append(
                    powerflow.lines[powerflow.linecount][75]
                )
                powerflow.dtpf["de"].append(powerflow.lines[powerflow.linecount][45:50])
                powerflow.dtpf["para"].append(
                    powerflow.lines[powerflow.linecount][51:56]
                )
                powerflow.dtpf["circuito"].append(
                    powerflow.lines[powerflow.linecount][57:59]
                )
                powerflow.dtpf["operacao"].append(
                    powerflow.lines[powerflow.linecount][75]
                )
                powerflow.dtpf["de"].append(powerflow.lines[powerflow.linecount][60:65])
                powerflow.dtpf["para"].append(
                    powerflow.lines[powerflow.linecount][66:71]
                )
                powerflow.dtpf["circuito"].append(
                    powerflow.lines[powerflow.linecount][72:74]
                )
                powerflow.dtpf["operacao"].append(
                    powerflow.lines[powerflow.linecount][75]
                )
            except:
                powerflow.dtpf["de"] = powerflow.dtpf["de"][:-1]
                break
        powerflow.linecount += 1

    # DataFrame dos dados de Fixação na Aplicação do Controle de Tensão por Variação Automática de Tap
    powerflow.dtpfDF = DF(data=powerflow.dtpf)
    powerflow.dtpf = deepcopy(powerflow.dtpfDF)
    powerflow.dtpfDF = powerflow.dtpfDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dtpfDF = powerflow.dtpfDF.astype(
        {
            "de": "int",
            "para": "int",
            "circuito": "object",
            "operacao": "object",
        }
    )
    if powerflow.dtpfDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DTPF`!\033[0m"
        )
    else:
        powerflow.codes["DTPF"] = True
