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
    anarede,
):
    """inicialização para leitura de dados de agregadores genéricos

    Args
        anarede:
    """
    ## Inicialização
    anarede.dagr1["numero"] = list()
    anarede.dagr1["descricao"] = list()
    anarede.dagr1["ndagr2"] = list()
    anarede.dagr2["numero"] = list()
    anarede.dagr2["operacao"] = list()
    anarede.dagr2["descricao"] = list()
    idx = 0

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        elif anarede.lines[anarede.linecount - 1][:] == anarede.dagr1["ruler"]:
            anarede.dagr1["numero"].append(anarede.lines[anarede.linecount][:3])
            anarede.dagr1["descricao"].append(anarede.lines[anarede.linecount][4:40])
        elif anarede.lines[anarede.linecount - 1][:] == anarede.dagr2["ruler"]:
            anarede.dagr1["ndagr2"].append(0)
            while anarede.lines[anarede.linecount].strip() != "FAGR":
                if anarede.lines[anarede.linecount][0] == anarede.comment:
                    pass
                else:
                    anarede.dagr2["numero"].append(anarede.lines[anarede.linecount][:3])
                    anarede.dagr2["operacao"].append(
                        anarede.lines[anarede.linecount][4]
                    )
                    anarede.dagr2["descricao"].append(
                        anarede.lines[anarede.linecount][6:42]
                    )
                anarede.dagr1["ndagr2"][idx] += 1
                anarede.linecount += 1
            idx += 1
        anarede.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    anarede.dagr1DF = DF(data=anarede.dagr1)
    anarede.dagr1 = deepcopy(anarede.dagr1DF)
    anarede.dagr1DF = anarede.dagr1DF.replace(r"^\s*$", "0", regex=True)
    anarede.dagr1DF = anarede.dagr1DF.astype(
        {
            "numero": "int",
            "descricao": "str",
        }
    )

    anarede.dagr2DF = DF(data=anarede.dagr2)
    anarede.dagr2 = deepcopy(anarede.dagr2DF)
    anarede.dagr2DF = anarede.dagr2DF.replace(r"^\s*$", "0", regex=True)
    anarede.dagr2DF = anarede.dagr2DF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "descricao": "str",
        }
    )
    if anarede.dagr1DF.empty or anarede.dagr2DF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DAGR`!\033[0m"
        )
    else:
        anarede.pwfblock["DAGR"] = True


def danc(
    anarede,
):
    """inicialização para leitura de dados de alteração do nível de carregamento

    Args
        anarede:
    """
    ## Inicialização
    anarede.danc["area"] = list()
    anarede.danc["fator_carga_ativa"] = list()
    anarede.danc["fator_carga_reativa"] = list()
    anarede.danc["fator_shunt_barra"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.danc["area"].append(anarede.lines[anarede.linecount][:5])
            anarede.danc["fator_carga_ativa"].append(
                anarede.lines[anarede.linecount][5:12]
            )
            anarede.danc["fator_carga_reativa"].append(
                anarede.lines[anarede.linecount][12:19]
            )
            anarede.danc["fator_shunt_barra"].append(
                anarede.lines[anarede.linecount][19:24]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    anarede.dancDF = DF(data=anarede.danc)
    anarede.danc = deepcopy(anarede.dancDF)
    anarede.dancDF = anarede.dancDF.replace(r"^\s*$", "0", regex=True)
    anarede.dancDF = anarede.dancDF.astype(
        {
            "area": "int",
            "fator_carga_ativa": "float",
            "fator_carga_reativa": "float",
            "fator_shunt_barra": "float",
        }
    )
    if anarede.dancDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m"
        )
    else:
        anarede.pwfblock["DANC"] = True


def danc_acls(
    anarede,
):
    """inicialização para leitura de dados de alteração do nível de carregamento

    Args
        anarede:
    """
    ## Inicialização
    anarede.danc["tipo_elemento_1"] = list()
    anarede.danc["identificacao_elemento_1"] = list()
    anarede.danc["condicao_elemento_1"] = list()
    anarede.danc["tipo_elemento_2"] = list()
    anarede.danc["identificacao_elemento_2"] = list()
    anarede.danc["condicao_elemento_2"] = list()
    anarede.danc["tipo_elemento_3"] = list()
    anarede.danc["identificacao_elemento_3"] = list()
    anarede.danc["condicao_elemento_3"] = list()
    anarede.danc["tipo_elemento_4"] = list()
    anarede.danc["identificacao_elemento_4"] = list()
    anarede.danc["fator_carga_ativa"] = list()
    anarede.danc["fator_carga_reativa"] = list()
    anarede.danc["fator_shunt_barra"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.danc["tipo_incremento_1"].append(
                anarede.lines[anarede.linecount][:4]
            )
            anarede.danc["identificacao_incremento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.danc["condicao_incremento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.danc["tipo_incremento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.danc["identificacao_incremento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.danc["condicao_incremento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.danc["tipo_incremento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.danc["identificacao_incremento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.danc["condicao_incremento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.danc["tipo_incremento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.danc["identificacao_incremento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.danc["fator_carga_ativa"].append(
                anarede.lines[anarede.linecount][50:56]
            )
            anarede.danc["fator_carga_reativa"].append(
                anarede.lines[anarede.linecount][57:63]
            )
            anarede.danc["fator_shunt_barra"].append(
                anarede.lines[anarede.linecount][64:70]
            )
        anarede.linecount += 1

    # DataFrame dos dados de Alteração do Nível de Carregamento
    anarede.dancDF = DF(data=anarede.danc)
    anarede.dancDF = deepcopy(anarede.dancDF)
    anarede.dancDF = anarede.dancDF.replace(r"^\s*$", "0", regex=True)
    anarede.dancDF = anarede.dancDF.astype(
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
    if anarede.dancDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m"
        )
    else:
        anarede.pwfblock["DANC"] = True


def checkdanc(
    anarede,
):
    """checa alteração no nível de carregamento

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    if anarede.pwfblock["DANC"]:
        for area in anarede.dancDF["area"].values:
            for idx, value in anarede.dbarDF.iterrows():
                if value["area"] == area:
                    anarede.dbarDF.loc[idx, "demanda_ativa"] *= (
                        1 + anarede.dancDF["fator_carga_ativa"][0] / anarede.cte["BASE"]
                    )
                    anarede.dbarDF.loc[idx, "demanda_reativa"] *= (
                        1
                        + anarede.dancDF["fator_carga_reativa"][0] / anarede.cte["BASE"]
                    )
                    anarede.dbarDF.loc[idx, "shunt_barra"] *= (
                        1 + anarede.dancDF["fator_shunt_barra"][0] / anarede.cte["BASE"]
                    )


def dare(
    anarede,
):
    """inicialização para leitura de dados de intercâmbio de potência ativa entre áreas

    Args
        anarede:
    """
    ## Inicialização
    anarede.dare["numero"] = list()
    anarede.dare["intercambio_liquido"] = list()
    anarede.dare["nome"] = list()
    anarede.dare["intercambio_minimo"] = list()
    anarede.dare["intercambio_maximo"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dare["numero"].append(anarede.lines[anarede.linecount][:3])
            anarede.dare["intercambio_liquido"].append(
                anarede.lines[anarede.linecount][7:13]
            )
            anarede.dare["nome"].append(anarede.lines[anarede.linecount][18:54])
            anarede.dare["intercambio_minimo"].append(
                anarede.lines[anarede.linecount][55:61]
            )
            anarede.dare["intercambio_maximo"].append(
                anarede.lines[anarede.linecount][62:68]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    anarede.dareDF = DF(data=anarede.dare)
    anarede.dare = deepcopy(anarede.dareDF)
    anarede.dareDF = anarede.dareDF.replace(r"^\s*$", "0", regex=True)
    anarede.dareDF = anarede.dareDF.astype(
        {
            "numero": "int",
            "intercambio_liquido": "float",
            "nome": "str",
            "intercambio_minimo": "float",
            "intercambio_maximo": "float",
        }
    )
    if anarede.dareDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DARE`!\033[0m"
        )
    else:
        anarede.pwfblock["DARE"] = True

        # Numero de Areas
        anarede.narea = anarede.dareDF.shape[0]
        anarede.areas = sorted(anarede.dareDF["numero"].unique())


def dbar(
    anarede,
):
    """inicialização para leitura de dados de barra

    Args
        anarede:
    """
    ## Inicialização
    anarede.dbar["numero"] = list()
    anarede.dbar["operacao"] = list()
    anarede.dbar["estado"] = list()
    anarede.dbar["tipo"] = list()
    anarede.dbar["grupo_base_tensao"] = list()
    anarede.dbar["nome"] = list()
    anarede.dbar["grupo_limite_tensao"] = list()
    anarede.dbar["tensao"] = list()
    anarede.dbar["angulo"] = list()
    anarede.dbar["potencia_ativa"] = list()
    anarede.dbar["potencia_reativa"] = list()
    anarede.dbar["potencia_reativa_minima"] = list()
    anarede.dbar["potencia_reativa_maxima"] = list()
    anarede.dbar["barra_controlada"] = list()
    anarede.dbar["demanda_ativa"] = list()
    anarede.dbar["demanda_reativa"] = list()
    anarede.dbar["shunt_barra"] = list()
    anarede.dbar["area"] = list()
    anarede.dbar["tensao_base"] = list()
    anarede.dbar["modo"] = list()
    anarede.dbar["agreg1"] = list()
    anarede.dbar["agreg2"] = list()
    anarede.dbar["agreg3"] = list()
    anarede.dbar["agreg4"] = list()
    anarede.dbar["agreg5"] = list()
    anarede.dbar["agreg6"] = list()
    anarede.dbar["agreg7"] = list()
    anarede.dbar["agreg8"] = list()
    anarede.dbar["agreg9"] = list()
    anarede.dbar["agreg10"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dbar["numero"].append(anarede.lines[anarede.linecount][:5])
            anarede.dbar["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dbar["estado"].append(anarede.lines[anarede.linecount][6])
            anarede.dbar["tipo"].append(anarede.lines[anarede.linecount][7])
            anarede.dbar["grupo_base_tensao"].append(
                anarede.lines[anarede.linecount][8:10]
            )
            anarede.dbar["nome"].append(
                anarede.lines[anarede.linecount][10:22].split(" ")[0]
            )
            anarede.dbar["grupo_limite_tensao"].append(
                anarede.lines[anarede.linecount][22:24]
            )
            anarede.dbar["tensao"].append(anarede.lines[anarede.linecount][24:28])
            anarede.dbar["angulo"].append(anarede.lines[anarede.linecount][28:32])
            anarede.dbar["potencia_ativa"].append(
                anarede.lines[anarede.linecount][32:37]
            )
            anarede.dbar["potencia_reativa"].append(
                anarede.lines[anarede.linecount][37:42]
            )
            anarede.dbar["potencia_reativa_minima"].append(
                anarede.lines[anarede.linecount][42:47]
            )
            anarede.dbar["potencia_reativa_maxima"].append(
                anarede.lines[anarede.linecount][47:52]
            )
            anarede.dbar["barra_controlada"].append(
                anarede.lines[anarede.linecount][52:58]
            )
            anarede.dbar["demanda_ativa"].append(
                anarede.lines[anarede.linecount][58:63]
            )
            anarede.dbar["demanda_reativa"].append(
                anarede.lines[anarede.linecount][63:68]
            )
            anarede.dbar["shunt_barra"].append(anarede.lines[anarede.linecount][68:73])
            anarede.dbar["area"].append(anarede.lines[anarede.linecount][73:76])
            anarede.dbar["tensao_base"].append(anarede.lines[anarede.linecount][76:80])
            anarede.dbar["modo"].append(anarede.lines[anarede.linecount][80])
            anarede.dbar["agreg1"].append(anarede.lines[anarede.linecount][81:84])
            anarede.dbar["agreg2"].append(anarede.lines[anarede.linecount][84:87])
            anarede.dbar["agreg3"].append(anarede.lines[anarede.linecount][87:90])
            anarede.dbar["agreg4"].append(anarede.lines[anarede.linecount][90:93])
            anarede.dbar["agreg5"].append(anarede.lines[anarede.linecount][93:96])
            anarede.dbar["agreg6"].append(anarede.lines[anarede.linecount][96:99])
            anarede.dbar["agreg7"].append(anarede.lines[anarede.linecount][99:102])
            anarede.dbar["agreg8"].append(anarede.lines[anarede.linecount][102:105])
            anarede.dbar["agreg9"].append(anarede.lines[anarede.linecount][105:108])
            anarede.dbar["agreg10"].append(anarede.lines[anarede.linecount][108:111])
        anarede.linecount += 1

    # DataFrame dos Dados de Barra
    anarede.dbarDF = DF(data=anarede.dbar)
    anarede.dbar = deepcopy(anarede.dbarDF)
    anarede.dbarDF = anarede.dbarDF.replace(r"^\s*$", "0", regex=True)
    anarede.dbarDF = anarede.dbarDF.astype(
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
    if anarede.dbarDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DBAR`!\033[0m"
        )
    else:
        anarede.pwfblock["DBAR"] = True

        # Número de barras do sistema
        anarede.nbus = len(anarede.dbarDF.tipo.values)

        # Barras geradoras: número & máscara
        anarede.npv = 0
        anarede.maskP = ones(anarede.nbus, dtype=bool)
        anarede.maskLp = ones(anarede.nbus, dtype=bool)
        anarede.maskQ = ones(anarede.nbus, dtype=bool)
        anarede.maskLq = ones(anarede.nbus, dtype=bool)
        for idx, value in anarede.dbarDF.iterrows():
            anarede.dbarDF.at[idx, "grupo_base_tensao"] = value[
                "grupo_base_tensao"
            ].strip()
            anarede.dbarDF.at[idx, "grupo_limite_tensao"] = value[
                "grupo_limite_tensao"
            ].strip()
            if (value["tipo"] == 2) or (value["tipo"] == 1):
                anarede.npv += 1
                anarede.maskQ[idx] = False

                if value["tipo"] == 2:
                    anarede.maskP[idx] = False
                    anarede.slackidx = idx
                    anarede.refgen = anarede.npv - 1

                if value["potencia_reativa"] > value["potencia_reativa_maxima"]:
                    anarede.dbarDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_maxima"
                    ]

                elif value["potencia_reativa"] < value["potencia_reativa_minima"]:
                    anarede.dbarDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_minima"
                    ]

            if value["demanda_ativa"] == 0.0:
                anarede.maskLp[idx] = False

            if value["demanda_reativa"] == 0.0:
                anarede.maskLq[idx] = False

            if value["grupo_base_tensao"] == "0":
                anarede.dbarDF.at[idx, "grupo_base_tensao"] = " 0"

        anarede.mask = concatenate((anarede.maskP, anarede.maskQ), axis=0)

        # Número de barras PV
        anarede.nger = anarede.npv

        # Número de barras PQ
        anarede.npq = anarede.nbus - anarede.npv

        # Tensao Base
        anarede.dbarDF.loc[anarede.dbarDF["tensao_base"] == 0.0, "tensao_base"] = 1000.0

        anarede.dbarDF = anarede.dbarDF.reset_index()


def dbsh(
    anarede,
):
    """inicialização para leitura de dados de bancos de capacitores e/ou reatores individualizados de barras CA ou de linhas de transmissão

    Args
        anarede:
    """
    ## Inicialização
    anarede.dbsh1["from"] = list()
    anarede.dbsh1["operacao"] = list()
    anarede.dbsh1["to"] = list()
    anarede.dbsh1["circuito"] = list()
    anarede.dbsh1["modo_controle"] = list()
    anarede.dbsh1["tensao_minima"] = list()
    anarede.dbsh1["tensao_maxima"] = list()
    anarede.dbsh1["barra_controlada"] = list()
    anarede.dbsh1["injecao_reativa_inicial"] = list()
    anarede.dbsh1["tipo_controle"] = list()
    anarede.dbsh1["apagar"] = list()
    anarede.dbsh1["extremidade"] = list()
    anarede.dbsh1["ndbsh2"] = list()
    anarede.dbsh2["grupo_banco"] = list()
    anarede.dbsh2["operacao"] = list()
    anarede.dbsh2["estado"] = list()
    anarede.dbsh2["unidades"] = list()
    anarede.dbsh2["unidades_operacao"] = list()
    anarede.dbsh2["capacitor_reator"] = list()
    anarede.dbsh2["manobravel"] = list()
    idx = 0

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        elif anarede.lines[anarede.linecount - 1][:] == anarede.dbsh1["ruler"]:
            anarede.dbsh1["from"].append(anarede.lines[anarede.linecount][:5])
            anarede.dbsh1["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dbsh1["to"].append(anarede.lines[anarede.linecount][8:13])
            anarede.dbsh1["circuito"].append(anarede.lines[anarede.linecount][14:16])
            anarede.dbsh1["modo_controle"].append(anarede.lines[anarede.linecount][17])
            anarede.dbsh1["tensao_minima"].append(
                anarede.lines[anarede.linecount][19:23]
            )
            anarede.dbsh1["tensao_maxima"].append(
                anarede.lines[anarede.linecount][24:28]
            )
            anarede.dbsh1["barra_controlada"].append(
                anarede.lines[anarede.linecount][29:34]
            )
            anarede.dbsh1["injecao_reativa_inicial"].append(
                anarede.lines[anarede.linecount][35:41]
            )
            anarede.dbsh1["tipo_controle"].append(anarede.lines[anarede.linecount][42])
            anarede.dbsh1["apagar"].append(anarede.lines[anarede.linecount][44])
            anarede.dbsh1["extremidade"].append(anarede.lines[anarede.linecount][46:51])

        elif anarede.lines[anarede.linecount - 1][:] == anarede.dbsh2["ruler"]:
            anarede.dbsh1["ndbsh2"].append(0)
            while anarede.lines[anarede.linecount].strip() != "FBAN":
                if anarede.lines[anarede.linecount][0] == anarede.comment:
                    pass
                else:
                    anarede.dbsh2["grupo_banco"].append(
                        anarede.lines[anarede.linecount][:2]
                    )
                    anarede.dbsh2["operacao"].append(
                        anarede.lines[anarede.linecount][4]
                    )
                    anarede.dbsh2["estado"].append(anarede.lines[anarede.linecount][6])
                    anarede.dbsh2["unidades"].append(
                        anarede.lines[anarede.linecount][8:11]
                    )
                    anarede.dbsh2["unidades_operacao"].append(
                        anarede.lines[anarede.linecount][12:15]
                    )
                    anarede.dbsh2["capacitor_reator"].append(
                        anarede.lines[anarede.linecount][16:22]
                    )
                    try:
                        anarede.dbsh2["manobravel"].append(
                            anarede.lines[anarede.linecount][23]
                        )
                    except:
                        anarede.dbsh2["manobravel"].append(" ")
                anarede.dbsh1["ndbsh2"][idx] += 1
                anarede.linecount += 1
            idx += 1
        anarede.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    anarede.dbsh1DF = DF(data=anarede.dbsh1)
    anarede.dbsh1 = deepcopy(anarede.dbsh1DF)
    anarede.dbsh1DF = anarede.dbsh1DF.replace(r"^\s*$", "0", regex=True)
    anarede.dbsh1DF = anarede.dbsh1DF.astype(
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

    anarede.dbsh2DF = DF(data=anarede.dbsh2)
    anarede.dbsh2 = deepcopy(anarede.dbsh2DF)
    anarede.dbsh2DF = anarede.dbsh2DF.replace(r"^\s*$", "0", regex=True)
    anarede.dbsh2DF = anarede.dbsh2DF.astype(
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
    if anarede.dbsh1DF.empty or anarede.dbsh2DF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DBSH`!\033[0m"
        )
    else:
        anarede.pwfblock["DBSH"] = True

        for idx, value in anarede.dbsh1DF.iterrows():
            if value["circuito"] == 0:
                anarede.dbsh1DF.at[idx, "circuito"] = 1
            if value["apagar"] == "0":
                anarede.dbsh1DF.at[idx, "apagar"] = " "


def dcar(
    anarede,
):
    """inicialização para leitura de Args A, B, C e D que estabelecem a curva de variação de carga em relação a magnitude de tensão nas barras

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcar["tipo_elemento_1"] = list()
    anarede.dcar["identificacao_elemento_1"] = list()
    anarede.dcar["condicao_elemento_1"] = list()
    anarede.dcar["tipo_elemento_2"] = list()
    anarede.dcar["identificacao_elemento_2"] = list()
    anarede.dcar["condicao_elemento_2"] = list()
    anarede.dcar["tipo_elemento_3"] = list()
    anarede.dcar["identificacao_elemento_3"] = list()
    anarede.dcar["condicao_elemento_3"] = list()
    anarede.dcar["tipo_elemento_4"] = list()
    anarede.dcar["identificacao_elemento_4"] = list()
    anarede.dcar["operacao"] = list()
    anarede.dcar["parametro_A"] = list()
    anarede.dcar["parametro_B"] = list()
    anarede.dcar["parametro_C"] = list()
    anarede.dcar["parametro_D"] = list()
    anarede.dcar["tensao_limite"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcar["tipo_elemento_1"].append(anarede.lines[anarede.linecount][:4])
            anarede.dcar["identificacao_elemento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dcar["condicao_elemento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dcar["tipo_elemento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dcar["identificacao_elemento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dcar["condicao_elemento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dcar["tipo_elemento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dcar["identificacao_elemento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dcar["condicao_elemento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dcar["tipo_elemento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dcar["identificacao_elemento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dcar["operacao"].append(anarede.lines[anarede.linecount][50])
            anarede.dcar["parametro_A"].append(anarede.lines[anarede.linecount][52:55])
            anarede.dcar["parametro_B"].append(anarede.lines[anarede.linecount][56:59])
            anarede.dcar["parametro_C"].append(anarede.lines[anarede.linecount][60:63])
            anarede.dcar["parametro_D"].append(anarede.lines[anarede.linecount][64:67])
            anarede.dcar["tensao_limite"].append(
                anarede.cte["VFLD"]
                if anarede.lines[anarede.linecount][68:72] == 4 * " "
                else anarede.lines[anarede.linecount][68:72]
            )
        anarede.linecount += 1

    # DataFrame dos dados de Variação do Tipo de Carga
    anarede.dcarDF = DF(data=anarede.dcar)
    anarede.dcarDF = deepcopy(anarede.dcarDF)
    anarede.dcarDF = anarede.dcarDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcarDF = anarede.dcarDF.astype(
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
            "parametro_A": "int",
            "parametro_B": "int",
            "parametro_C": "int",
            "parametro_D": "int",
            "tensao_limite": "float",
        }
    )
    if anarede.dcarDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCAR`!\033[0m"
        )
    else:
        anarede.pwfblock["DCAR"] = True


def dcba(
    anarede,
):
    """inicialização para leitura de dados de barra CC

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcba["numero"] = list()
    anarede.dcba["operacao"] = list()
    anarede.dcba["tipo"] = list()
    anarede.dcba["polaridade"] = list()
    anarede.dcba["nome"] = list()
    anarede.dcba["grupo_limite_tensao"] = list()
    anarede.dcba["tensao"] = list()
    anarede.dcba["eletrodo_terra"] = list()
    anarede.dcba["numero_elo_cc"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcba["numero"].append(anarede.lines[anarede.linecount][:4])
            anarede.dcba["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dcba["tipo"].append(anarede.lines[anarede.linecount][7])
            anarede.dcba["polaridade"].append(anarede.lines[anarede.linecount][8])
            anarede.dcba["nome"].append(anarede.lines[anarede.linecount][9:21])
            anarede.dcba["grupo_limite_tensao"].append(
                anarede.lines[anarede.linecount][21:23]
            )
            anarede.dcba["tensao"].append(anarede.lines[anarede.linecount][23:28])
            anarede.dcba["eletrodo_terra"].append(
                anarede.lines[anarede.linecount][66:71]
            )
            anarede.dcba["numero_elo_cc"].append(
                anarede.lines[anarede.linecount][71:75]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Barra CC
    anarede.dcbaDF = DF(data=anarede.dcba)
    anarede.dcba = deepcopy(anarede.dcbaDF)
    anarede.dcbaDF = anarede.dcbaDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcbaDF = anarede.dcbaDF.astype(
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
    if anarede.dcbaDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCBA`!\033[0m"
        )
    else:
        anarede.pwfblock["DCBA"] = True


def dccv(
    anarede,
):
    """inicialização para leitura de dados de controle de conversores CA/CC

    Args
        anarede:
    """
    ## Inicialização
    anarede.dccv["numero"] = list()
    anarede.dccv["operacao"] = list()
    anarede.dccv["folga"] = list()
    anarede.dccv["modo_controle_inversor"] = list()
    anarede.dccv["tipo_controle_conversor"] = list()
    anarede.dccv["valor_especificado"] = list()
    anarede.dccv["margem_corrente"] = list()
    anarede.dccv["maxima_sobrecorrente"] = list()
    anarede.dccv["angulo_conversor"] = list()
    anarede.dccv["angulo_conversor_minimo"] = list()
    anarede.dccv["angulo_conversor_maximo"] = list()
    anarede.dccv["tap_transformador_minimo"] = list()
    anarede.dccv["tap_transformador_maximo"] = list()
    anarede.dccv["tap_transformador_numero"] = list()
    anarede.dccv["tensao_cc_minima"] = list()
    anarede.dccv["tap_high"] = list()
    anarede.dccv["tap_reduzido"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dccv["numero"].append(anarede.lines[anarede.linecount][:4])
            anarede.dccv["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dccv["folga"].append(anarede.lines[anarede.linecount][7])
            anarede.dccv["modo_controle_inversor"].append(
                anarede.lines[anarede.linecount][8]
            )
            anarede.dccv["tipo_controle_conversor"].append(
                anarede.lines[anarede.linecount][9]
            )
            anarede.dccv["valor_especificado"].append(
                anarede.lines[anarede.linecount][11:16]
            )
            anarede.dccv["margem_corrente"].append(
                anarede.lines[anarede.linecount][17:22]
            )
            anarede.dccv["maxima_sobrecorrente"].append(
                anarede.lines[anarede.linecount][23:28]
            )
            anarede.dccv["angulo_conversor"].append(
                anarede.lines[anarede.linecount][29:34]
            )
            anarede.dccv["angulo_conversor_minimo"].append(
                anarede.lines[anarede.linecount][35:40]
            )
            anarede.dccv["angulo_conversor_maximo"].append(
                anarede.lines[anarede.linecount][41:46]
            )
            anarede.dccv["tap_transformador_minimo"].append(
                anarede.lines[anarede.linecount][47:52]
            )
            anarede.dccv["tap_transformador_maximo"].append(
                anarede.lines[anarede.linecount][53:58]
            )
            anarede.dccv["tap_transformador_numero"].append(
                anarede.lines[anarede.linecount][59:61]
            )
            anarede.dccv["tensao_cc_minima"].append(
                anarede.lines[anarede.linecount][62:66]
            )
            anarede.dccv["tap_high"].append(anarede.lines[anarede.linecount][67:72])
            anarede.dccv["tap_reduzido"].append(anarede.lines[anarede.linecount][73:78])
        anarede.linecount += 1

    # DataFrame dos Dados de Controle de Conversores de Tensão CC
    anarede.dccvDF = DF(data=anarede.dccv)
    anarede.dccv = deepcopy(anarede.dccvDF)
    anarede.dccvDF = anarede.dccvDF.replace(r"^\s*$", "0", regex=True)
    anarede.dccvDF = anarede.dccvDF.astype(
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

    if anarede.dccvDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCCV`!\033[0m"
        )
    else:
        anarede.pwfblock["DCCV"] = True


def dcer(
    anarede,
):
    """inicialização para leitura de dados de compensadores estáticos de potência reativa

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcer["barra"] = list()
    anarede.dcer["operacao"] = list()
    anarede.dcer["grupo_base"] = list()
    anarede.dcer["unidades"] = list()
    anarede.dcer["barra_controlada"] = list()
    anarede.dcer["droop"] = list()
    anarede.dcer["potencia_reativa"] = list()
    anarede.dcer["potencia_reativa_minima"] = list()
    anarede.dcer["potencia_reativa_maxima"] = list()
    anarede.dcer["controle"] = list()
    anarede.dcer["estado"] = list()
    anarede.dcer["modo_correcao_limites"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcer["barra"].append(anarede.lines[anarede.linecount][:5])
            anarede.dcer["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dcer["grupo_base"].append(anarede.lines[anarede.linecount][8:10])
            anarede.dcer["unidades"].append(anarede.lines[anarede.linecount][11:13])
            anarede.dcer["barra_controlada"].append(
                anarede.lines[anarede.linecount][14:19]
            )
            anarede.dcer["droop"].append(anarede.lines[anarede.linecount][20:26])
            anarede.dcer["potencia_reativa"].append(
                anarede.lines[anarede.linecount][27:32]
            )
            anarede.dcer["potencia_reativa_minima"].append(
                anarede.lines[anarede.linecount][32:37]
            )
            anarede.dcer["potencia_reativa_maxima"].append(
                anarede.lines[anarede.linecount][37:42]
            )
            anarede.dcer["controle"].append(anarede.lines[anarede.linecount][43])
            anarede.dcer["estado"].append(anarede.lines[anarede.linecount][45])
            anarede.dcer["modo_correcao_limites"].append(
                anarede.lines[anarede.linecount][47]
            )
        anarede.linecount += 1

    # DataFrame dos Dados dos Compensadores Estáticos de Potência Reativa
    anarede.dcerDF = DF(data=anarede.dcer)
    anarede.dcer = deepcopy(anarede.dcerDF)
    anarede.dcerDF = anarede.dcerDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcerDF = anarede.dcerDF.astype(
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
    if anarede.dcerDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código e execução `DCER`!\033[0m"
        )
    else:
        anarede.pwfblock["DCER"] = True

        # Número de Compensadores Estáticos de Potência Reativa
        anarede.ncer = 0
        for idx, value in anarede.dcerDF.iterrows():
            if value["estado"] == "D":
                anarede.dcerDF = anarede.dcerDF.drop(
                    labels=idx,
                    axis=0,
                )

            elif ((value["estado"] == "0") or (value["estado"] == "L")) and (
                (value["controle"] == "0")
                or (value["controle"] == "P")
                or (value["controle"] == "I")
            ):
                anarede.ncer += 1
                anarede.dcerDF.at[idx, "droop"] = -value["droop"] / (
                    1e2 * value["unidades"]
                )

                if value["barra_controlada"] == 0:
                    anarede.dcerDF.at[idx, "barra_controlada"] = value["barra"]

                if value["potencia_reativa"] > value["potencia_reativa_maxima"]:
                    anarede.dcerDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_maxima"
                    ]

                elif value["potencia_reativa"] < value["potencia_reativa_minima"]:
                    anarede.dcerDF.at[idx, "potencia_reativa"] = value[
                        "potencia_reativa_minima"
                    ]

                if value["controle"] == "0":
                    anarede.dcerDF.at[idx, "controle"] = "P"

            elif ((value["estado"] == "0") or (value["estado"] == "L")) and (
                value["controle"] == "A"
            ):
                anarede.ncer += 1
                anarede.dcerDF.at[idx, "droop"] = -value["droop"] / (
                    1e2 * value["unidades"]
                )

                if value["barra_controlada"] == 0:
                    anarede.dcerDF.at[idx, "barra_controlada"] = value["barra"]


def dcli(
    anarede,
):
    """inicialização para leitura de dados de linhas de transmissão CC

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcli["de"] = list()
    anarede.dcli["operacao"] = list()
    anarede.dcli["para"] = list()
    anarede.dcli["circuito"] = list()
    anarede.dcli["proprietario"] = list()
    anarede.dcli["resistencia"] = list()
    anarede.dcli["indutancia"] = list()
    anarede.dcli["capacidade"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcli["de"].append(anarede.lines[anarede.linecount][:4])
            anarede.dcli["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dcli["para"].append(anarede.lines[anarede.linecount][8:12])
            anarede.dcli["circuito"].append(anarede.lines[anarede.linecount][12:14])
            anarede.dcli["proprietario"].append(anarede.lines[anarede.linecount][15])
            anarede.dcli["resistencia"].append(anarede.lines[anarede.linecount][17:23])
            anarede.dcli["indutancia"].append(anarede.lines[anarede.linecount][23:29])
            anarede.dcli["capacidade"].append(anarede.lines[anarede.linecount][60:64])
        anarede.linecount += 1

    # DataFrame dos Dados de Linhas de Transmissão CC
    anarede.dcliDF = DF(data=anarede.dcli)
    anarede.dcli = deepcopy(anarede.dcliDF)
    anarede.dcliDF = anarede.dcliDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcliDF = anarede.dcliDF.astype(
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

    if anarede.dcliDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCLI`!\033[0m"
        )
    else:
        anarede.pwfblock["DCLI"] = True


def dcnv(
    anarede,
):
    """inicialização para leitura de dados de conversores CA/CC

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcnv["numero"] = list()
    anarede.dcnv["operacao"] = list()
    anarede.dcnv["barra_CA"] = list()
    anarede.dcnv["barra_CC"] = list()
    anarede.dcnv["barra_neutra"] = list()
    anarede.dcnv["modo_operacao"] = list()
    anarede.dcnv["pontes"] = list()
    anarede.dcnv["corrente"] = list()
    anarede.dcnv["reatancia_comutacao"] = list()
    anarede.dcnv["tensao_secundario"] = list()
    anarede.dcnv["potencia_transformador"] = list()
    anarede.dcnv["resistencia_reator"] = list()
    anarede.dcnv["indutancia_reator"] = list()
    anarede.dcnv["capacitancia"] = list()
    anarede.dcnv["frequencia"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcnv["numero"].append(anarede.lines[anarede.linecount][:4])
            anarede.dcnv["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dcnv["barra_CA"].append(anarede.lines[anarede.linecount][7:12])
            anarede.dcnv["barra_CC"].append(anarede.lines[anarede.linecount][13:17])
            anarede.dcnv["barra_neutra"].append(anarede.lines[anarede.linecount][18:22])
            anarede.dcnv["modo_operacao"].append(anarede.lines[anarede.linecount][23])
            anarede.dcnv["pontes"].append(anarede.lines[anarede.linecount][25])
            anarede.dcnv["corrente"].append(anarede.lines[anarede.linecount][27:32])
            anarede.dcnv["reatancia_comutacao"].append(
                anarede.lines[anarede.linecount][33:38]
            )
            anarede.dcnv["tensao_secundario"].append(
                anarede.lines[anarede.linecount][39:44]
            )
            anarede.dcnv["potencia_transformador"].append(
                anarede.lines[anarede.linecount][45:50]
            )
            anarede.dcnv["resistencia_reator"].append(
                anarede.lines[anarede.linecount][51:56]
            )
            anarede.dcnv["indutancia_reator"].append(
                anarede.lines[anarede.linecount][57:62]
            )
            anarede.dcnv["capacitancia"].append(anarede.lines[anarede.linecount][63:68])
            anarede.dcnv["frequencia"].append(anarede.lines[anarede.linecount][69:71])
        anarede.linecount += 1

    # DataFrame dos Dados de Conversores CA/CC
    anarede.dcnvDF = DF(data=anarede.dcnv)
    anarede.dcnv = deepcopy(anarede.dcnvDF)
    anarede.dcnvDF = anarede.dcnvDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcnvDF = anarede.dcnvDF.astype(
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

    if anarede.dcnvDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCNV`!\033[0m"
        )
    else:
        anarede.pwfblock["DCNV"] = True


def dcsc(
    anarede,
):
    """inicialização para leitura de dados de compensador série controlável

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcsc["de"] = list()
    anarede.dcsc["operacao"] = list()
    anarede.dcsc["para"] = list()
    anarede.dcsc["circuito"] = list()
    anarede.dcsc["estado"] = list()
    anarede.dcsc["proprietario"] = list()
    anarede.dcsc["bypass"] = list()
    anarede.dcsc["reatancia_minima"] = list()
    anarede.dcsc["reatancia_maxima"] = list()
    anarede.dcsc["reatancia_inicial"] = list()
    anarede.dcsc["modo_controle"] = list()
    anarede.dcsc["especificado"] = list()
    anarede.dcsc["extremidade"] = list()
    anarede.dcsc["estagios"] = list()
    anarede.dcsc["capacidade_normal"] = list()
    anarede.dcsc["capacidade_emergencia"] = list()
    anarede.dcsc["capacidade"] = list()
    anarede.dcsc["agreg1"] = list()
    anarede.dcsc["agreg2"] = list()
    anarede.dcsc["agreg3"] = list()
    anarede.dcsc["agreg4"] = list()
    anarede.dcsc["agreg5"] = list()
    anarede.dcsc["agreg6"] = list()
    anarede.dcsc["agreg7"] = list()
    anarede.dcsc["agreg8"] = list()
    anarede.dcsc["agreg9"] = list()
    anarede.dcsc["agreg10"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcsc["de"].append(anarede.lines[anarede.linecount][:5])
            anarede.dcsc["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dcsc["para"].append(anarede.lines[anarede.linecount][9:14])
            anarede.dcsc["circuito"].append(anarede.lines[anarede.linecount][14:16])
            anarede.dcsc["estado"].append(anarede.lines[anarede.linecount][16])
            anarede.dcsc["proprietario"].append(anarede.lines[anarede.linecount][17])
            anarede.dcsc["bypass"].append(anarede.lines[anarede.linecount][18])
            anarede.dcsc["reatancia_minima"].append(
                anarede.lines[anarede.linecount][25:31]
            )
            anarede.dcsc["reatancia_maxima"].append(
                anarede.lines[anarede.linecount][31:37]
            )
            anarede.dcsc["reatancia_inicial"].append(
                anarede.lines[anarede.linecount][37:43]
            )
            anarede.dcsc["modo_controle"].append(anarede.lines[anarede.linecount][43])
            anarede.dcsc["especificado"].append(anarede.lines[anarede.linecount][45:51])
            anarede.dcsc["extremidade"].append(anarede.lines[anarede.linecount][52:57])
            anarede.dcsc["estagios"].append(anarede.lines[anarede.linecount][57:60])
            anarede.dcsc["capacidade_normal"].append(
                anarede.lines[anarede.linecount][60:64]
            )
            anarede.dcsc["capacidade_emergencia"].append(
                anarede.lines[anarede.linecount][64:68]
            )
            anarede.dcsc["capacidade"].append(anarede.lines[anarede.linecount][68:72])
            anarede.dcsc["agreg1"].append(anarede.lines[anarede.linecount][72:75])
            anarede.dcsc["agreg2"].append(anarede.lines[anarede.linecount][75:78])
            anarede.dcsc["agreg3"].append(anarede.lines[anarede.linecount][78:81])
            anarede.dcsc["agreg4"].append(anarede.lines[anarede.linecount][81:84])
            anarede.dcsc["agreg5"].append(anarede.lines[anarede.linecount][84:87])
            anarede.dcsc["agreg6"].append(anarede.lines[anarede.linecount][87:90])
            anarede.dcsc["agreg7"].append(anarede.lines[anarede.linecount][90:93])
            anarede.dcsc["agreg8"].append(anarede.lines[anarede.linecount][93:96])
            anarede.dcsc["agreg9"].append(anarede.lines[anarede.linecount][96:99])
            anarede.dcsc["agreg10"].append(anarede.lines[anarede.linecount][99:102])
        anarede.linecount += 1

    # DataFrame dos Dados de Compensador Série Controlável
    anarede.dcscDF = DF(data=anarede.dcsc)
    anarede.dcsc = deepcopy(anarede.dcscDF)
    anarede.dcscDF = anarede.dcscDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcscDF = anarede.dcscDF.astype(
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

    if anarede.dcscDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCSC`!\033[0m"
        )
    else:
        anarede.pwfblock["DCSC"] = True


def dcte(
    anarede,
):
    """inicialização para leitura de dados de constantes

    Args
        anarede:
    """
    ## Inicialização
    anarede.dcte["constante"] = list()
    anarede.dcte["valor_constante"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][:4])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][5:11]
            )
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][12:16])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][17:23]
            )
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][24:28])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][29:35]
            )
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][36:40])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][41:47]
            )
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][48:52])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][53:59]
            )
            anarede.dcte["constante"].append(anarede.lines[anarede.linecount][60:64])
            anarede.dcte["valor_constante"].append(
                anarede.lines[anarede.linecount][65:71]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Constantes
    anarede.dcteDF = DF(data=anarede.dcte)
    anarede.dcte = deepcopy(anarede.dcteDF)
    anarede.dcteDF = anarede.dcteDF.replace(r"^\s*$", "0", regex=True)
    anarede.dcteDF = anarede.dcteDF.astype(
        {
            "constante": "object",
            "valor_constante": "float",
        }
    )
    if anarede.dcteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTE`!\033[0m"
        )
    else:
        anarede.pwfblock["DCTE"] = True

        anarede.dcteDF["constante"] = anarede.dcteDF["constante"].replace("0", nan)
        anarede.dcteDF = anarede.dcteDF.dropna(axis=0, subset=["constante"])
        anarede.dcteDF = anarede.dcteDF.drop_duplicates(
            subset=["constante"], keep="last"
        ).reset_index(drop=True)


def dctg(
    anarede,
):
    """inicialização para leitura de lista de casos de contingência

    Args
        anarede:
    """
    ## Inicialização
    anarede.dctg1["identificacao"] = list()
    anarede.dctg1["operacao"] = list()
    anarede.dctg1["prioridade"] = list()
    anarede.dctg1["nome"] = list()
    anarede.dctg1["ndctg2"] = list()
    anarede.dctg2["tipo"] = list()
    anarede.dctg2["de"] = list()
    anarede.dctg2["para"] = list()
    anarede.dctg2["circuito"] = list()
    anarede.dctg2["extremidade"] = list()
    anarede.dctg2["variacao_geracao_ativa"] = list()
    anarede.dctg2["variacao_geracao_ativa_minima"] = list()
    anarede.dctg2["variacao_geracao_ativa_maxima"] = list()
    anarede.dctg2["variacao_geracao_reativa"] = list()
    anarede.dctg2["variacao_geracao_reativa_minima"] = list()
    anarede.dctg2["variacao_geracao_reativa_maxima"] = list()
    anarede.dctg2["variacao_fator_participacao"] = list()
    anarede.dctg2["grupo"] = list()
    anarede.dctg2["unidades"] = list()
    idx = 0

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        elif anarede.lines[anarede.linecount - 1][:] == anarede.dctg1["ruler"]:
            anarede.dctg1["identificacao"].append(anarede.lines[anarede.linecount][:4])
            anarede.dctg1["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.dctg1["prioridade"].append(anarede.lines[anarede.linecount][7:9])
            anarede.dctg1["nome"].append(anarede.lines[anarede.linecount][10:56])

        elif anarede.lines[anarede.linecount - 1][:] == anarede.dctg2["ruler"]:
            anarede.dctg1["ndctg2"].append(0)
            while anarede.lines[anarede.linecount].strip() != "FCAS":
                if anarede.lines[anarede.linecount][0] == anarede.comment:
                    pass
                else:
                    anarede.dctg2["tipo"].append(anarede.lines[anarede.linecount][:4])
                    anarede.dctg2["de"].append(anarede.lines[anarede.linecount][5:10])
                    anarede.dctg2["para"].append(
                        anarede.lines[anarede.linecount][11:16]
                    )
                    anarede.dctg2["circuito"].append(
                        anarede.lines[anarede.linecount][17:19]
                    )
                    anarede.dctg2["extremidade"].append(
                        anarede.lines[anarede.linecount][20:25]
                    )
                    anarede.dctg2["variacao_geracao_ativa"].append(
                        anarede.lines[anarede.linecount][26:31]
                    )
                    anarede.dctg2["variacao_geracao_ativa_minima"].append(
                        anarede.lines[anarede.linecount][32:37]
                    )
                    anarede.dctg2["variacao_geracao_ativa_maxima"].append(
                        anarede.lines[anarede.linecount][38:43]
                    )
                    anarede.dctg2["variacao_geracao_reativa"].append(
                        anarede.lines[anarede.linecount][44:49]
                    )
                    anarede.dctg2["variacao_geracao_reativa_minima"].append(
                        anarede.lines[anarede.linecount][50:55]
                    )
                    anarede.dctg2["variacao_geracao_reativa_maxima"].append(
                        anarede.lines[anarede.linecount][56:61]
                    )
                    anarede.dctg2["variacao_fator_participacao"].append(
                        anarede.lines[anarede.linecount][62:67]
                    )
                    anarede.dctg2["grupo"].append(
                        anarede.lines[anarede.linecount][68:70]
                    )
                    anarede.dctg2["unidades"].append(
                        anarede.lines[anarede.linecount][71:74]
                    )
                anarede.dctg1["ndctg2"][idx] += 1
                anarede.linecount += 1
            idx += 1
        anarede.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    anarede.dctg1DF = DF(data=anarede.dctg1)
    anarede.dctg1 = deepcopy(anarede.dctg1DF)
    anarede.dctg1DF = anarede.dctg1DF.replace(r"^\s*$", "0", regex=True)
    anarede.dctg1DF = anarede.dctg1DF.astype(
        {
            "identificacao": "int",
            "operacao": "object",
            "prioridade": "int",
            "nome": "object",
        }
    )

    anarede.dctg2DF = DF(data=anarede.dctg2)
    anarede.dctg2 = deepcopy(anarede.dctg2DF)
    anarede.dctg2DF = anarede.dctg2DF.replace(r"^\s*$", "0", regex=True)
    anarede.dctg2DF = anarede.dctg2DF.astype(
        {
            "tipo": "object",
            "de": "int",
            "para": "int",
            "circuito": "int",
            "extremidade": "object",
            "variacao_geracao_ativa": "float",
            "variacao_geracao_ativa_minima": "float",
            "variacao_geracao_ativa_maxima": "float",
            "variacao_geracao_reativa": "float",
            "variacao_geracao_reativa_minima": "float",
            "variacao_geracao_reativa_maxima": "float",
            "variacao_fator_participacao": "float",
        }
    )
    if anarede.dctg1DF.empty or anarede.dctg2DF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTG`!\033[0m"
        )
    else:
        anarede.pwfblock["DCTG"] = True


def dctr(
    anarede,
):
    """inicialização para leitura de dados complementares de transformadores

    Args
        anarede:
    """
    ## Inicialização
    anarede.dctr["de"] = list()
    anarede.dctr["operacao"] = list()
    anarede.dctr["para"] = list()
    anarede.dctr["circuito"] = list()
    anarede.dctr["tensao_minima"] = list()
    anarede.dctr["tensao_maxima"] = list()
    anarede.dctr["tipo_controle_1"] = list()
    anarede.dctr["modo_controle"] = list()
    anarede.dctr["fase_minima"] = list()
    anarede.dctr["fase_maxima"] = list()
    anarede.dctr["tipo_controle_2"] = list()
    anarede.dctr["valor_especificado"] = list()
    anarede.dctr["extremidade"] = list()
    anarede.dctr["taps"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dctr["de"].append(anarede.lines[anarede.linecount][:5])
            anarede.dctr["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dctr["para"].append(anarede.lines[anarede.linecount][8:13])
            anarede.dctr["circuito"].append(anarede.lines[anarede.linecount][14:16])
            anarede.dctr["tensao_minima"].append(
                anarede.lines[anarede.linecount][17:21]
            )
            anarede.dctr["tensao_maxima"].append(
                anarede.lines[anarede.linecount][22:26]
            )
            anarede.dctr["tipo_controle_1"].append(anarede.lines[anarede.linecount][27])
            anarede.dctr["modo_controle"].append(anarede.lines[anarede.linecount][29])
            anarede.dctr["fase_minima"].append(anarede.lines[anarede.linecount][31:37])
            anarede.dctr["fase_maxima"].append(anarede.lines[anarede.linecount][38:44])
            anarede.dctr["tipo_controle_2"].append(anarede.lines[anarede.linecount][45])
            anarede.dctr["valor_especificado"].append(
                anarede.lines[anarede.linecount][47:53]
            )
            anarede.dctr["extremidade"].append(anarede.lines[anarede.linecount][54:59])
            anarede.dctr["taps"].append(anarede.lines[anarede.linecount][60:62])
        anarede.linecount += 1

    # DataFrame dos Dados Complementares de Transformadores
    anarede.dctrDF = DF(data=anarede.dctr)
    anarede.dctr = deepcopy(anarede.dctrDF)
    anarede.dctrDF = anarede.dctrDF.replace(r"^\s*$", "0", regex=True)
    anarede.dctrDF = anarede.dctrDF.astype(
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

    if anarede.dctrDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTR`!\033[0m"
        )
    else:
        anarede.pwfblock["DCTR"] = True


def delo(
    anarede,
):
    """inicialização para leitura de dados de elo CC

    Args
        anarede:
    """
    ## Inicialização
    anarede.delo["numero"] = list()
    anarede.delo["operacao"] = list()
    anarede.delo["tensao"] = list()
    anarede.delo["base"] = list()
    anarede.delo["nome"] = list()
    anarede.delo["modo_high"] = list()
    anarede.delo["estado"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.delo["numero"].append(anarede.lines[anarede.linecount][:4])
            anarede.delo["operacao"].append(anarede.lines[anarede.linecount][5])
            anarede.delo["tensao"].append(anarede.lines[anarede.linecount][7:12])
            anarede.delo["base"].append(anarede.lines[anarede.linecount][13:18])
            anarede.delo["nome"].append(anarede.lines[anarede.linecount][19:39])
            anarede.delo["modo_high"].append(anarede.lines[anarede.linecount][40])
            anarede.delo["estado"].append(anarede.lines[anarede.linecount][42])
        anarede.linecount += 1

    # DataFrame dos Dados de Elo CC
    anarede.deloDF = DF(data=anarede.delo)
    anarede.delo = deepcopy(anarede.deloDF)
    anarede.deloDF = anarede.deloDF.replace(r"^\s*$", "0", regex=True)
    anarede.deloDF = anarede.deloDF.astype(
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

    if anarede.deloDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DELO`!\033[0m"
        )
    else:
        anarede.pwfblock["DELO"] = True


def dgbt(
    anarede,
):
    """inicialização para leitura de dados de grupos de base de tensão de barras CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dgbt["grupo"] = list()
    anarede.dgbt["tensao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dgbt["grupo"].append(anarede.lines[anarede.linecount][:2])
            anarede.dgbt["tensao"].append(anarede.lines[anarede.linecount][3:8])
        anarede.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    anarede.dgbtDF = DF(data=anarede.dgbt)
    anarede.dgbt = deepcopy(anarede.dgbtDF)
    anarede.dgbtDF = anarede.dgbtDF.replace(r"^\s*$", "0", regex=True)
    anarede.dgbtDF = anarede.dgbtDF.astype(
        {
            "grupo": "object",
            "tensao": "float",
        }
    )
    if anarede.dgbtDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGBT`!\033[0m"
        )
    else:
        anarede.pwfblock["DGBT"] = True

        for idx, value in anarede.dgbtDF.iterrows():
            anarede.dgbtDF.at[idx, "grupo"] = value["grupo"].strip()
            if value["tensao"] == 0.0:
                anarede.dgbtDF.at[idx, "tensao"] = 1.0


def dger(
    anarede,
):
    """inicialização para leitura de dados de geradores

    Args
        anarede:
    """
    ## Inicialização
    anarede.dger["numero"] = list()
    anarede.dger["operacao"] = list()
    anarede.dger["potencia_ativa_minima"] = list()
    anarede.dger["potencia_ativa_maxima"] = list()
    anarede.dger["fator_participacao"] = list()
    anarede.dger["fator_participacao_controle_remoto"] = list()
    anarede.dger["fator_potencia_nominal"] = list()
    anarede.dger["fator_servico_armadura"] = list()
    anarede.dger["fator_servico_rotor"] = list()
    anarede.dger["angulo_maximo_carga"] = list()
    anarede.dger["reatancia_maquina"] = list()
    anarede.dger["potencia_aparente_nominal"] = list()
    anarede.dger["estatismo"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dger["numero"].append(anarede.lines[anarede.linecount][:5])
            anarede.dger["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dger["potencia_ativa_minima"].append(
                anarede.lines[anarede.linecount][8:14]
            )
            anarede.dger["potencia_ativa_maxima"].append(
                anarede.lines[anarede.linecount][15:21]
            )
            anarede.dger["fator_participacao"].append(
                anarede.lines[anarede.linecount][22:27]
            )
            anarede.dger["fator_participacao_controle_remoto"].append(
                anarede.lines[anarede.linecount][28:33]
            )
            anarede.dger["fator_potencia_nominal"].append(
                anarede.lines[anarede.linecount][34:39]
            )
            anarede.dger["fator_servico_armadura"].append(
                anarede.lines[anarede.linecount][40:44]
            )
            anarede.dger["fator_servico_rotor"].append(
                anarede.lines[anarede.linecount][45:49]
            )
            anarede.dger["angulo_maximo_carga"].append(
                anarede.lines[anarede.linecount][50:54]
            )
            anarede.dger["reatancia_maquina"].append(
                anarede.lines[anarede.linecount][55:60]
            )
            anarede.dger["potencia_aparente_nominal"].append(
                anarede.lines[anarede.linecount][61:66]
            )
            anarede.dger["estatismo"].append(anarede.lines[anarede.linecount][66:72])
        anarede.linecount += 1

    # DataFrame dos Dados de Geradores
    anarede.dgerDF = DF(data=anarede.dger)
    anarede.dger = deepcopy(anarede.dgerDF)
    anarede.dgerDF = anarede.dgerDF.replace(r"^\s*$", "0", regex=True)
    anarede.dgerDF = anarede.dgerDF.astype(
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
    if anarede.dgerDF.empty:  # or (anarede.dgerDF.shape[0] != anarede.nger):
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGER`!\033[0m"
        )
    else:
        anarede.pwfblock["DGER"] = True

        if anarede.dgerDF["fator_participacao"].sum() == 0:
            import pandas as pd

            geradores = pd.merge(
                anarede.dgerDF[["numero"]],
                anarede.dbarDF,
                on="numero",
            )
            geradores["fator_participacao"] = (
                geradores["potencia_ativa"] * 1e2 / geradores["potencia_ativa"].sum()
            )

            geradores.set_index("numero", inplace=True)
            anarede.dgerDF.set_index("numero", inplace=True)

            anarede.dgerDF["fator_participacao"].update(geradores["fator_participacao"])
            anarede.dgerDF.reset_index(inplace=True)

        anarede.nger = anarede.dgerDF.shape[0]


def dglt(
    anarede,
):
    """inicialização para leitura de dados de grupos de limites de tensão

    Args
        anarede:
    """
    ## Inicialização
    anarede.dglt["grupo_limite_tensao"] = list()
    anarede.dglt["limite_minimo"] = list()
    anarede.dglt["limite_maximo"] = list()
    anarede.dglt["limite_minimo_E"] = list()
    anarede.dglt["limite_maximo_E"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dglt["grupo_limite_tensao"].append(
                anarede.lines[anarede.linecount][:2]
            )
            anarede.dglt["limite_minimo"].append(anarede.lines[anarede.linecount][3:8])
            anarede.dglt["limite_maximo"].append(anarede.lines[anarede.linecount][9:14])
            anarede.dglt["limite_minimo_E"].append(
                anarede.lines[anarede.linecount][15:20]
            )
            anarede.dglt["limite_maximo_E"].append(
                anarede.lines[anarede.linecount][21:26]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    anarede.dgltDF = DF(data=anarede.dglt)
    anarede.dglt = deepcopy(anarede.dgltDF)
    anarede.dgltDF = anarede.dgltDF.replace(r"^\s*$", "0", regex=True)
    anarede.dgltDF = anarede.dgltDF.astype(
        {
            "grupo_limite_tensao": "object",
            "limite_minimo": "float",
            "limite_maximo": "float",
            "limite_minimo_E": "float",
            "limite_maximo_E": "float",
        }
    )
    if anarede.dgltDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DGLT`!\033[0m"
        )
    else:
        anarede.pwfblock["DGLT"] = True

        for idx, value in anarede.dgltDF.iterrows():
            anarede.dgltDF.at[idx, "grupo_limite_tensao"] = value[
                "grupo_limite_tensao"
            ].strip()
            if value["limite_minimo"] == 0.0:
                anarede.dgltDF.at[idx, "limite_minimo"] = 0.8

            if value["limite_maximo"] == 0.0:
                anarede.dgltDF.at[idx, "limite_maximo"] = 1.2

            if value["limite_minimo_E"] == 0.0:
                anarede.dgltDF.at[idx, "limite_minimo_E"] = value["limite_minimo"]

            if value["limite_maximo_E"] == 0.0:
                anarede.dgltDF.at[idx, "limite_maximo_E"] = value["limite_maximo"]

        anarede.dbarDF = anarede.dbarDF.merge(
            anarede.dgltDF, on="grupo_limite_tensao", how="left"
        )


def dinc(
    anarede,
):
    """inicialização para leitura de dados de incremento do nível de carregamento

    Args
        anarede:
    """
    ## Inicialização
    anarede.dinc["tipo_incremento_1"] = list()
    anarede.dinc["identificacao_incremento_1"] = list()
    anarede.dinc["condicao_incremento_1"] = list()
    anarede.dinc["tipo_incremento_2"] = list()
    anarede.dinc["identificacao_incremento_2"] = list()
    anarede.dinc["condicao_incremento_2"] = list()
    anarede.dinc["tipo_incremento_3"] = list()
    anarede.dinc["identificacao_incremento_3"] = list()
    anarede.dinc["condicao_incremento_3"] = list()
    anarede.dinc["tipo_incremento_4"] = list()
    anarede.dinc["identificacao_incremento_4"] = list()
    anarede.dinc["condicao_incremento_4"] = list()
    anarede.dinc["passo_incremento_potencia_ativa"] = list()
    anarede.dinc["passo_incremento_potencia_reativa"] = list()
    anarede.dinc["maximo_incremento_potencia_ativa"] = list()
    anarede.dinc["maximo_incremento_potencia_reativa"] = list()
    anarede.dinc["tratamento_incremento_potencia_ativa"] = list()
    anarede.dinc["tratamento_incremento_potencia_reativa"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dinc["tipo_incremento_1"].append(
                anarede.lines[anarede.linecount][:4]
            )
            anarede.dinc["identificacao_incremento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dinc["condicao_incremento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dinc["tipo_incremento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dinc["identificacao_incremento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dinc["condicao_incremento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dinc["tipo_incremento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dinc["identificacao_incremento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dinc["condicao_incremento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dinc["tipo_incremento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dinc["identificacao_incremento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dinc["condicao_incremento_4"].append(
                anarede.lines[anarede.linecount][50]
            )
            anarede.dinc["passo_incremento_potencia_ativa"].append(
                anarede.lines[anarede.linecount][52:57]
            )
            anarede.dinc["passo_incremento_potencia_reativa"].append(
                anarede.lines[anarede.linecount][58:63]
            )
            anarede.dinc["maximo_incremento_potencia_ativa"].append(
                anarede.lines[anarede.linecount][64:69]
            )
            anarede.dinc["maximo_incremento_potencia_reativa"].append(
                anarede.lines[anarede.linecount][70:75]
            )
            anarede.dinc["tratamento_incremento_potencia_ativa"].append(
                False if anarede.lines[anarede.linecount][64:69] != "" else True
            )
            anarede.dinc["tratamento_incremento_potencia_reativa"].append(
                False if anarede.lines[anarede.linecount][70:75] != "" else True
            )
        anarede.linecount += 1

    # DataFrame dos dados de Incremento do Nível de Carregamento
    anarede.dincDF = DF(data=anarede.dinc)
    anarede.dinc = deepcopy(anarede.dincDF)
    anarede.dincDF = anarede.dincDF.replace(r"^\s*$", "0", regex=True)
    anarede.dincDF = anarede.dincDF.astype(
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
    if anarede.dincDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DINC`!\033[0m"
        )
    else:
        anarede.pwfblock["DINC"] = True

        for idx, value in anarede.dincDF.iterrows():
            anarede.dincDF.at[idx, "passo_incremento_potencia_ativa"] *= 1e-2
            if value["tratamento_incremento_potencia_ativa"]:
                anarede.dincDF.at[idx, "maximo_incremento_potencia_ativa"] = 99.99
            else:
                anarede.dincDF.at[idx, "maximo_incremento_potencia_ativa"] *= 1e-2

            anarede.dincDF.at[idx, "passo_incremento_potencia_reativa"] *= 1e-2
            if value["tratamento_incremento_potencia_reativa"]:
                anarede.dincDF.at[idx, "maximo_incremento_potencia_reativa"] = 99.99
            else:
                anarede.dincDF.at[idx, "maximo_incremento_potencia_reativa"] *= 1e-2


def dinj(
    anarede,
):
    """inicialização para leitura de dados de injeções de potências, shunts e fatores de participação de geração do modelo equivalente

    Args
        anarede:
    """
    ## Inicialização
    anarede.dinj["numero"] = list()
    anarede.dinj["operacao"] = list()
    anarede.dinj["injecao_ativa_eq"] = list()
    anarede.dinj["injecao_reativa_eq"] = list()
    anarede.dinj["shunt_eq"] = list()
    anarede.dinj["fator_participacao_eq"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dinj["numero"].append(anarede.lines[anarede.linecount][:5])
            anarede.dinj["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dinj["injecao_ativa_eq"].append(
                anarede.lines[anarede.linecount][8:15]
            )
            anarede.dinj["injecao_reativa_eq"].append(
                anarede.lines[anarede.linecount][15:22]
            )
            anarede.dinj["shunt_eq"].append(anarede.lines[anarede.linecount][22:29])
            anarede.dinj["fator_participacao_eq"].append(
                anarede.lines[anarede.linecount][29:36]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Injeção de Potências, Shunts e Fatores de Participação de Geração do Modelo Equivalente
    anarede.dinjDF = DF(data=anarede.dinj)
    anarede.dinj = deepcopy(anarede.dinjDF)
    anarede.dinjDF = anarede.dinjDF.replace(r"^\s*$", "0", regex=True)
    anarede.dinjDF = anarede.dinjDF.astype(
        {
            "numero": "int",
            "operacao": "object",
            "injecao_ativa_eq": "float",
            "injecao_reativa_eq": "float",
            "shunt_eq": "float",
            "fator_participacao_eq": "float",
        }
    )
    if anarede.dinjDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DINJ`!\033[0m"
        )
    else:
        anarede.pwfblock["DINJ"] = True
        # precision = lambda x: tuple(len(p) for p in str(x).split("."))

        # for idx, value in anarede.dinjDF.iterrows():
        #     precision(anarede.dinj.injecao_ativa_eq[idx])
        #     precision(anarede.dinj.injecao_reativa_eq[idx])
        #     precision(anarede.dinj.shunt_eq[idx])
        #     anarede.dbarDF.loc[
        #         anarede.dbarDF["numero"] == value["numero"], "demanda_ativa"
        #     ] += -value["injecao_ativa_eq"]

        #     anarede.dbarDF.loc[
        #         anarede.dbarDF["numero"] == value["numero"], "demanda_reativa"
        #     ] += (-value["injecao_reativa_eq"] + value["shunt_eq"])

        #     # anarede.dbarDF.loc[
        #     #     anarede.dbarDF["numero"] == value["numero"], "shunt_barra"
        #     # ] += round(value["shunt_eq"])

        #     if anarede.pwfblock["DGER"]:
        #         anarede.dgerDF.loc[
        #             anarede.dbarDF["numero"] == value["numero"],
        #             "fator_participacao",
        #         ] += value["fator_participacao_eq"]

        # anarede.dbar.demanda_ativa = anarede.dbarDF.demanda_ativa.values
        # anarede.dbar.demanda_reativa = anarede.dbarDF.demanda_reativa.values
        # anarede.dbar.shunt_barra = anarede.dbarDF.shunt_barra.values


def dlin(
    anarede,
):
    """inicialização para leitura de dados de linha de transmissão CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dlin["de"] = list()
    anarede.dlin["abertura_de"] = list()
    anarede.dlin["operacao"] = list()
    anarede.dlin["abertura_para"] = list()
    anarede.dlin["para"] = list()
    anarede.dlin["circuito"] = list()
    anarede.dlin["estado"] = list()
    anarede.dlin["proprietario"] = list()
    anarede.dlin["manobravel"] = list()
    anarede.dlin["resistencia"] = list()
    anarede.dlin["reatancia"] = list()
    anarede.dlin["susceptancia"] = list()
    anarede.dlin["tap"] = list()
    anarede.dlin["tap_minimo"] = list()
    anarede.dlin["tap_maximo"] = list()
    anarede.dlin["tap_defasagem"] = list()
    anarede.dlin["barra_controlada"] = list()
    anarede.dlin["capacidade_normal"] = list()
    anarede.dlin["capacidade_emergencial"] = list()
    anarede.dlin["numero_taps"] = list()
    anarede.dlin["capacidade_equipamento"] = list()
    anarede.dlin["agreg1"] = list()
    anarede.dlin["agreg2"] = list()
    anarede.dlin["agreg3"] = list()
    anarede.dlin["agreg4"] = list()
    anarede.dlin["agreg5"] = list()
    anarede.dlin["agreg6"] = list()
    anarede.dlin["agreg7"] = list()
    anarede.dlin["agreg8"] = list()
    anarede.dlin["agreg9"] = list()
    anarede.dlin["agreg10"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dlin["de"].append(anarede.lines[anarede.linecount][:5])
            anarede.dlin["abertura_de"].append(anarede.lines[anarede.linecount][5])
            anarede.dlin["operacao"].append(anarede.lines[anarede.linecount][7])
            anarede.dlin["abertura_para"].append(anarede.lines[anarede.linecount][9])
            anarede.dlin["para"].append(anarede.lines[anarede.linecount][10:15])
            anarede.dlin["circuito"].append(anarede.lines[anarede.linecount][15:17])
            anarede.dlin["estado"].append(anarede.lines[anarede.linecount][17])
            anarede.dlin["proprietario"].append(anarede.lines[anarede.linecount][18])
            anarede.dlin["manobravel"].append(anarede.lines[anarede.linecount][19])
            anarede.dlin["resistencia"].append(anarede.lines[anarede.linecount][20:26])
            anarede.dlin["reatancia"].append(anarede.lines[anarede.linecount][26:32])
            anarede.dlin["susceptancia"].append(anarede.lines[anarede.linecount][32:38])
            anarede.dlin["tap"].append(anarede.lines[anarede.linecount][38:43])
            anarede.dlin["tap_minimo"].append(anarede.lines[anarede.linecount][43:48])
            anarede.dlin["tap_maximo"].append(anarede.lines[anarede.linecount][48:53])
            anarede.dlin["tap_defasagem"].append(
                anarede.lines[anarede.linecount][53:58]
            )
            anarede.dlin["barra_controlada"].append(
                anarede.lines[anarede.linecount][58:64]
            )
            anarede.dlin["capacidade_normal"].append(
                anarede.lines[anarede.linecount][64:68]
            )
            anarede.dlin["capacidade_emergencial"].append(
                anarede.lines[anarede.linecount][68:72]
            )
            anarede.dlin["numero_taps"].append(anarede.lines[anarede.linecount][72:74])
            anarede.dlin["capacidade_equipamento"].append(
                anarede.lines[anarede.linecount][74:78]
            )
            anarede.dlin["agreg1"].append(anarede.lines[anarede.linecount][78:81])
            anarede.dlin["agreg2"].append(anarede.lines[anarede.linecount][81:84])
            anarede.dlin["agreg3"].append(anarede.lines[anarede.linecount][84:87])
            anarede.dlin["agreg4"].append(anarede.lines[anarede.linecount][87:90])
            anarede.dlin["agreg5"].append(anarede.lines[anarede.linecount][90:93])
            anarede.dlin["agreg6"].append(anarede.lines[anarede.linecount][93:96])
            anarede.dlin["agreg7"].append(anarede.lines[anarede.linecount][96:99])
            anarede.dlin["agreg8"].append(anarede.lines[anarede.linecount][99:102])
            anarede.dlin["agreg9"].append(anarede.lines[anarede.linecount][102:105])
            anarede.dlin["agreg10"].append(anarede.lines[anarede.linecount][105:108])
        anarede.linecount += 1

    # DataFrame dos Dados de Linha
    anarede.dlinDF = DF(data=anarede.dlin)
    anarede.dlin = deepcopy(anarede.dlinDF)
    anarede.dlinDF = anarede.dlinDF.replace(r"^\s*$", "0", regex=True)
    anarede.dlinDF = anarede.dlinDF.astype(
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
    if anarede.dlinDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DLIN`!\033[0m"
        )
    else:
        anarede.pwfblock["DLIN"] = True

        anarede.dlinDF["resistencia"] *= 1e-2
        anarede.dlinDF["reatancia"] *= 1e-2
        anarede.dlinDF["susceptancia"] /= (
            2
            * anarede.dcteDF.loc[anarede.dcteDF.constante == "BASE"].valor_constante[0]
        )

        anarede.dlinDF["circuito"] = anarede.dlinDF["circuito"].replace("0", "1")

        anarede.dlinDF["estado"] = (anarede.dlinDF["estado"] == "0") | (
            anarede.dlinDF["estado"] == "L"
        )
        anarede.dlinDF["transf"] = (anarede.dlinDF["tap"] != 0.0) & anarede.dlinDF[
            "estado"
        ]

        anarede.dlinDF["tap"] = anarede.dlinDF["tap"].tolist() + 1 * (
            ~anarede.dlinDF["transf"].values
        )
        anarede.dlinDF["tapp"] = deepcopy(anarede.dlinDF["tap"])
        anarede.dlinDF["tap"] = anarede.dlinDF["tap"] * exp(
            1j * pi / 180 * anarede.dlinDF["tap_defasagem"]
        )  ## add phase shifters

        # Número de barras do sistema
        anarede.nlin = len(anarede.dlinDF.de.values)

        anarede.dlinDF["de-idx"] = anarede.dlinDF["de"].map(
            anarede.dbarDF.set_index("numero")["index"]
        )
        anarede.dlinDF["para-idx"] = anarede.dlinDF["para"].map(
            anarede.dbarDF.set_index("numero")["index"]
        )


def dmet(
    anarede,
):
    """inicialização para leitura de dados de monitoração para estabilidade de tensão em barra CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dmte["tipo_elemento_1"] = list()
    anarede.dmte["identificacao_elemento_1"] = list()
    anarede.dmte["condicao_elemento_1"] = list()
    anarede.dmte["tipo_elemento_2"] = list()
    anarede.dmte["identificacao_elemento_2"] = list()
    anarede.dmte["condicao_elemento_2"] = list()
    anarede.dmte["tipo_elemento_3"] = list()
    anarede.dmte["identificacao_elemento_3"] = list()
    anarede.dmte["condicao_elemento_3"] = list()
    anarede.dmte["tipo_elemento_4"] = list()
    anarede.dmte["identificacao_elemento_4"] = list()
    anarede.dmte["operacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dmte["tipo_elemento_1"].append(anarede.lines[anarede.linecount][:4])
            anarede.dmte["identificacao_elemento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dmte["condicao_elemento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dmte["tipo_elemento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dmte["identificacao_elemento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dmte["condicao_elemento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dmte["tipo_elemento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dmte["identificacao_elemento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dmte["condicao_elemento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dmte["tipo_elemento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dmte["identificacao_elemento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dmte["operacao"].append(anarede.lines[anarede.linecount][50])
        anarede.linecount += 1

    # DataFrame dos Dados de Monitoração para Estabilidade de Tensão em Barra CA
    anarede.dmteDF = DF(data=anarede.dmte)
    anarede.dmte = deepcopy(anarede.dmteDF)
    anarede.dmteDF = anarede.dmteDF.replace(r"^\s*$", "0", regex=True)
    anarede.dmteDF = anarede.dmteDF.astype(
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
        }
    )
    if anarede.dmteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMET`!\033[0m"
        )
    else:
        anarede.pwfblock["DMET"] = True


def dmfl(
    anarede,
):
    """inicialização para leitura de dados de monitoração de fluxo em circuito CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dmfl["tipo_elemento_1"] = list()
    anarede.dmfl["identificacao_elemento_1"] = list()
    anarede.dmfl["condicao_elemento_1"] = list()
    anarede.dmfl["tipo_elemento_2"] = list()
    anarede.dmfl["identificacao_elemento_2"] = list()
    anarede.dmfl["condicao_elemento_2"] = list()
    anarede.dmfl["tipo_elemento_3"] = list()
    anarede.dmfl["identificacao_elemento_3"] = list()
    anarede.dmfl["condicao_elemento_3"] = list()
    anarede.dmfl["tipo_elemento_4"] = list()
    anarede.dmfl["identificacao_elemento_4"] = list()
    anarede.dmfl["operacao"] = list()
    anarede.dmfl["interligacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dmfl["tipo_elemento_1"].append(anarede.lines[anarede.linecount][:4])
            anarede.dmfl["identificacao_elemento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dmfl["condicao_elemento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dmfl["tipo_elemento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dmfl["identificacao_elemento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dmfl["condicao_elemento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dmfl["tipo_elemento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dmfl["identificacao_elemento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dmfl["condicao_elemento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dmfl["tipo_elemento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dmfl["identificacao_elemento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][50])
            anarede.dmfl["interligacao"].append(anarede.lines[anarede.linecount][52])
        anarede.linecount += 1

    # DataFrame dos dados de Monitoração de Fluxo em Circuito CA
    anarede.dmflDF = DF(data=anarede.dmfl)
    anarede.dmfl = deepcopy(anarede.dmflDF)
    anarede.dmflDF = anarede.dmflDF.replace(r"^\s*$", "0", regex=True)
    anarede.dmflDF = anarede.dmflDF.astype(
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
    if anarede.dmflDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMFL`!\033[0m"
        )
    else:
        anarede.pwfblock["DMFL"] = True


def dmfl_circ(
    anarede,
):
    """inicialização para leitura de dados de monitoração de fluxo em circuito CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dmfl["de"] = list()
    anarede.dmfl["para"] = list()
    anarede.dmfl["circuito"] = list()
    anarede.dmfl["operacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            try:
                anarede.dmfl["de"].append(anarede.lines[anarede.linecount][:5])
                anarede.dmfl["para"].append(anarede.lines[anarede.linecount][6:11])
                anarede.dmfl["circuito"].append(anarede.lines[anarede.linecount][12:14])
                anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dmfl["de"].append(anarede.lines[anarede.linecount][15:20])
                anarede.dmfl["para"].append(anarede.lines[anarede.linecount][21:26])
                anarede.dmfl["circuito"].append(anarede.lines[anarede.linecount][27:29])
                anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dmfl["de"].append(anarede.lines[anarede.linecount][30:35])
                anarede.dmfl["para"].append(anarede.lines[anarede.linecount][36:41])
                anarede.dmfl["circuito"].append(anarede.lines[anarede.linecount][42:44])
                anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dmfl["de"].append(anarede.lines[anarede.linecount][45:50])
                anarede.dmfl["para"].append(anarede.lines[anarede.linecount][51:56])
                anarede.dmfl["circuito"].append(anarede.lines[anarede.linecount][57:59])
                anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dmfl["de"].append(anarede.lines[anarede.linecount][60:65])
                anarede.dmfl["para"].append(anarede.lines[anarede.linecount][66:71])
                anarede.dmfl["circuito"].append(anarede.lines[anarede.linecount][72:74])
                anarede.dmfl["operacao"].append(anarede.lines[anarede.linecount][75])
            except:
                anarede.dmfl["de"] = anarede.dmfl["de"][:-1]
                break
        anarede.linecount += 1

    # DataFrame dos Dados de Constantes
    anarede.dmflDF = DF(data=anarede.dmfl)
    anarede.dmfl = deepcopy(anarede.dmflDF)
    anarede.dmflDF = anarede.dmflDF.replace(r"^\s*$", "0", regex=True)
    anarede.dmflDF = anarede.dmflDF.astype(
        {
            "de": "int",
            "para": "int",
            "circuito": "int",
            "operacao": "object",
        }
    )

    if anarede.dmflDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMFL`!\033[0m"
        )
    else:
        anarede.pwfblock["DMFL"] = True


def dmte(
    anarede,
):
    """inicialização para leitura de dados de monitoração de tensão em barra CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dmte["tipo_elemento_1"] = list()
    anarede.dmte["identificacao_elemento_1"] = list()
    anarede.dmte["condicao_elemento_1"] = list()
    anarede.dmte["tipo_elemento_2"] = list()
    anarede.dmte["identificacao_elemento_2"] = list()
    anarede.dmte["condicao_elemento_2"] = list()
    anarede.dmte["tipo_elemento_3"] = list()
    anarede.dmte["identificacao_elemento_3"] = list()
    anarede.dmte["condicao_elemento_3"] = list()
    anarede.dmte["tipo_elemento_4"] = list()
    anarede.dmte["identificacao_elemento_4"] = list()
    anarede.dmte["operacao"] = list()
    anarede.dmte["interligacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dmte["tipo_elemento_1"].append(anarede.lines[anarede.linecount][:4])
            anarede.dmte["identificacao_elemento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dmte["condicao_elemento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dmte["tipo_elemento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dmte["identificacao_elemento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dmte["condicao_elemento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dmte["tipo_elemento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dmte["identificacao_elemento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dmte["condicao_elemento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dmte["tipo_elemento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dmte["identificacao_elemento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dmte["operacao"].append(anarede.lines[anarede.linecount][50])
            anarede.dmte["interligacao"].append(anarede.lines[anarede.linecount][52])
        anarede.linecount += 1

    # DataFrame dos dados de Monitoração de Tensão em Circuito CA
    anarede.dmteDF = DF(data=anarede.dmte)
    anarede.dmte = deepcopy(anarede.dmteDF)
    anarede.dmteDF = anarede.dmteDF.replace(r"^\s*$", "0", regex=True)
    anarede.dmteDF = anarede.dmteDF.astype(
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
    if anarede.dmteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMTE`!\033[0m"
        )
    else:
        anarede.pwfblock["DMTE"] = True


def dopc(
    anarede,
):
    """inicialização para leitura de dados de código de opções de controle e execução padrão

    Args
        anarede:
    """
    ## Inicialização
    anarede.dopc["opcao"] = list()
    anarede.dopc["padrao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            try:
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][:4])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][5])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][7:11])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][12])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][14:18])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][19])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][21:25])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][26])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][28:32])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][33])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][35:39])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][40])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][42:46])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][47])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][49:53])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][54])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][56:60])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][61])
                anarede.dopc["opcao"].append(anarede.lines[anarede.linecount][63:67])
                anarede.dopc["padrao"].append(anarede.lines[anarede.linecount][68])
            except:
                anarede.dopc["opcao"] = anarede.dopc["opcao"][:-1]
                break
        anarede.linecount += 1

    # DataFrame dos Dados de Constantes
    anarede.dopcDF = DF(data=anarede.dopc)
    anarede.dopc = deepcopy(anarede.dopcDF)
    anarede.dopcDF = anarede.dopcDF.replace(r"^\s*$", "0", regex=True)
    anarede.dopcDF = anarede.dopcDF.astype(
        {
            "opcao": "object",
            "padrao": "object",
        }
    )
    if anarede.dopcDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DOPC`!\033[0m"
        )
    else:
        anarede.pwfblock["DOPC"] = True

        anarede.dopcDF["opcao"] = anarede.dopcDF["opcao"].replace("0", nan)
        anarede.dopcDF = anarede.dopcDF.dropna(axis=0, subset=["opcao"])
        anarede.dopcDF = anarede.dopcDF.drop_duplicates(
            subset=["opcao"], keep="last"
        ).reset_index(drop=True)


def dshl(
    anarede,
):
    """inicialização para leitura de dados de dispositivos shunt de circuito CA

    Args
        anarede:
    """
    ## Inicialização
    anarede.dshl["from"] = list()
    anarede.dshl["operacao"] = list()
    anarede.dshl["to"] = list()
    anarede.dshl["circuito"] = list()
    anarede.dshl["shunt_from"] = list()
    anarede.dshl["shunt_to"] = list()
    anarede.dshl["estado_shunt_from"] = list()
    anarede.dshl["estado_shunt_to"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dshl["from"].append(anarede.lines[anarede.linecount][:5])
            anarede.dshl["operacao"].append(anarede.lines[anarede.linecount][6])
            anarede.dshl["to"].append(anarede.lines[anarede.linecount][9:14])
            anarede.dshl["circuito"].append(anarede.lines[anarede.linecount][14:16])
            anarede.dshl["shunt_from"].append(anarede.lines[anarede.linecount][17:23])
            anarede.dshl["shunt_to"].append(anarede.lines[anarede.linecount][23:29])
            anarede.dshl["estado_shunt_from"].append(
                anarede.lines[anarede.linecount][30:32]
            )
            anarede.dshl["estado_shunt_to"].append(
                anarede.lines[anarede.linecount][33:35]
            )
        anarede.linecount += 1

    # DataFrame dos Dados de Constantes
    anarede.dshlDF = DF(data=anarede.dshl)
    anarede.dshl = deepcopy(anarede.dshlDF)
    anarede.dshlDF = anarede.dshlDF.replace(r"^\s*$", "0", regex=True)
    anarede.dshlDF = anarede.dshlDF.astype(
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
    if anarede.dshlDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DSHL`!\033[0m"
        )
    else:
        anarede.pwfblock["DSHL"] = True


def dtpf(
    anarede,
):
    """inicialização para leitura de dados de fixação na aplicação do controle de tensão por variação automática de tap

    Args
        anarede:
    """
    ## Inicialização
    anarede.dtpf["tipo_elemento_1"] = list()
    anarede.dtpf["identificacao_elemento_1"] = list()
    anarede.dtpf["condicao_elemento_1"] = list()
    anarede.dtpf["tipo_elemento_2"] = list()
    anarede.dtpf["identificacao_elemento_2"] = list()
    anarede.dtpf["condicao_elemento_2"] = list()
    anarede.dtpf["tipo_elemento_3"] = list()
    anarede.dtpf["identificacao_elemento_3"] = list()
    anarede.dtpf["condicao_elemento_3"] = list()
    anarede.dtpf["tipo_elemento_4"] = list()
    anarede.dtpf["identificacao_elemento_4"] = list()
    anarede.dtpf["operacao"] = list()
    anarede.dtpf["interligacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            anarede.dtpf["tipo_elemento_1"].append(anarede.lines[anarede.linecount][:4])
            anarede.dtpf["identificacao_elemento_1"].append(
                anarede.lines[anarede.linecount][5:10]
            )
            anarede.dtpf["condicao_elemento_1"].append(
                anarede.lines[anarede.linecount][11]
            )
            anarede.dtpf["tipo_elemento_2"].append(
                anarede.lines[anarede.linecount][13:17]
            )
            anarede.dtpf["identificacao_elemento_2"].append(
                anarede.lines[anarede.linecount][18:23]
            )
            anarede.dtpf["condicao_elemento_2"].append(
                anarede.lines[anarede.linecount][24]
            )
            anarede.dtpf["tipo_elemento_3"].append(
                anarede.lines[anarede.linecount][26:30]
            )
            anarede.dtpf["identificacao_elemento_3"].append(
                anarede.lines[anarede.linecount][31:36]
            )
            anarede.dtpf["condicao_elemento_3"].append(
                anarede.lines[anarede.linecount][37]
            )
            anarede.dtpf["tipo_elemento_4"].append(
                anarede.lines[anarede.linecount][39:43]
            )
            anarede.dtpf["identificacao_elemento_4"].append(
                anarede.lines[anarede.linecount][44:49]
            )
            anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][50])
            anarede.dtpf["interligacao"].append(anarede.lines[anarede.linecount][52])
        anarede.linecount += 1

    # DataFrame dos dados de Fixação na Aplicação do Controle de Tensão por Variação Automática de Tap
    anarede.dtpfDF = DF(data=anarede.dtpf)
    anarede.dtpf = deepcopy(anarede.dtpfDF)
    anarede.dtpfDF = anarede.dtpfDF.replace(r"^\s*$", "0", regex=True)
    anarede.dtpfDF = anarede.dtpfDF.astype(
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
    if anarede.dtpfDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DTPF`!\033[0m"
        )
    else:
        anarede.pwfblock["DTPF"] = True


def dtpf_circ(
    anarede,
):
    """inicialização para leitura de dados de fixação na aplicação do controle de tensão por variação automática de tap

    Args
        anarede:
    """
    ## Inicialização
    anarede.dtpf["de"] = list()
    anarede.dtpf["para"] = list()
    anarede.dtpf["circuito"] = list()
    anarede.dtpf["operacao"] = list()

    while anarede.lines[anarede.linecount].strip() not in anarede.end_block:
        if anarede.lines[anarede.linecount][0] == anarede.comment:
            pass
        else:
            try:
                anarede.dtpf["de"].append(anarede.lines[anarede.linecount][:5])
                anarede.dtpf["para"].append(anarede.lines[anarede.linecount][6:11])
                anarede.dtpf["circuito"].append(anarede.lines[anarede.linecount][12:14])
                anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dtpf["de"].append(anarede.lines[anarede.linecount][15:20])
                anarede.dtpf["para"].append(anarede.lines[anarede.linecount][21:26])
                anarede.dtpf["circuito"].append(anarede.lines[anarede.linecount][27:29])
                anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dtpf["de"].append(anarede.lines[anarede.linecount][30:35])
                anarede.dtpf["para"].append(anarede.lines[anarede.linecount][36:41])
                anarede.dtpf["circuito"].append(anarede.lines[anarede.linecount][42:44])
                anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dtpf["de"].append(anarede.lines[anarede.linecount][45:50])
                anarede.dtpf["para"].append(anarede.lines[anarede.linecount][51:56])
                anarede.dtpf["circuito"].append(anarede.lines[anarede.linecount][57:59])
                anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][75])
                anarede.dtpf["de"].append(anarede.lines[anarede.linecount][60:65])
                anarede.dtpf["para"].append(anarede.lines[anarede.linecount][66:71])
                anarede.dtpf["circuito"].append(anarede.lines[anarede.linecount][72:74])
                anarede.dtpf["operacao"].append(anarede.lines[anarede.linecount][75])
            except:
                anarede.dtpf["de"] = anarede.dtpf["de"][:-1]
                break
        anarede.linecount += 1

    # DataFrame dos dados de Fixação na Aplicação do Controle de Tensão por Variação Automática de Tap
    anarede.dtpfDF = DF(data=anarede.dtpf)
    anarede.dtpf = deepcopy(anarede.dtpfDF)
    anarede.dtpfDF = anarede.dtpfDF.replace(r"^\s*$", "0", regex=True)
    anarede.dtpfDF = anarede.dtpfDF.astype(
        {
            "de": "int",
            "para": "int",
            "circuito": "int",
            "operacao": "object",
        }
    )
    if anarede.dtpfDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DTPF`!\033[0m"
        )
    else:
        anarede.pwfblock["DTPF"] = True
