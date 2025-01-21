# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from pandas import DataFrame as DF
from os.path import dirname, exists


def darq(
    powerflow,
):
    """inicialização para leitura de dados de entrada e saida de arquivos

    Args
        powerflow:
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

    Args
        powerflow:
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
            powerflow.devt["elemento"].append(
                powerflow.lines[powerflow.linecount][13:19]
            )
            powerflow.devt["para"].append(powerflow.lines[powerflow.linecount][19:24])
            powerflow.devt["ncircuito"].append(
                powerflow.lines[powerflow.linecount][24:26]
            )
            powerflow.devt["extremidade"].append(
                powerflow.lines[powerflow.linecount][26:31]
            )
            powerflow.devt["v-percentual"].append(
                powerflow.lines[powerflow.linecount][32:37]
            )
            powerflow.devt["v-absoluto"].append(
                powerflow.lines[powerflow.linecount][38:44]
            )
            powerflow.devt["grupo"].append(powerflow.lines[powerflow.linecount][45:47])
            powerflow.devt["unidades"].append(
                powerflow.lines[powerflow.linecount][48:51]
            )
            powerflow.devt["bloco-cdu"].append(
                powerflow.lines[powerflow.linecount][60:64]
            )
            powerflow.devt["polaridade"].append(
                powerflow.lines[powerflow.linecount][64]
            )
            powerflow.devt["resistencia"].append(
                powerflow.lines[powerflow.linecount][66:72]
            )
            powerflow.devt["reatancia"].append(
                powerflow.lines[powerflow.linecount][73:79]
            )
            powerflow.devt["susceptancia"].append(
                powerflow.lines[powerflow.linecount][80:86]
            )
            powerflow.devt["defasagem"].append(
                powerflow.lines[powerflow.linecount][87:94]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    powerflow.devtDF = DF(data=powerflow.devt)
    powerflow.devt = deepcopy(powerflow.devtDF)
    powerflow.devtDF = powerflow.devtDF.replace(r"^\s*$", "0", regex=True)
    powerflow.devtDF = powerflow.devtDF.sort_values(by=["tempo"], ascending=True)
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
        pass
    else:
        powerflow.codes["DEVT"] = True


def dsim(
    powerflow,
):
    """inicialização para leitura de dados de controle de simulação

    Args
        powerflow:
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
    arquivo,
    arquivoname,
):
    """inicialização para leitura de dados

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.linecount = 0
    f = open(f"{arquivo}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    powerflow.dmaq = dict()
    powerflow.dmaq["numero"] = list()
    powerflow.dmaq["grupo"] = list()
    powerflow.dmaq["percentual-ativa"] = list()
    powerflow.dmaq["percentual-reativa"] = list()
    powerflow.dmaq["unidades"] = list()
    powerflow.dmaq["gerador"] = list()
    powerflow.dmaq["tensao"] = list()
    powerflow.dmaq["user-tensao"] = list()
    powerflow.dmaq["velocidade"] = list()
    powerflow.dmaq["user-velocidade"] = list()
    powerflow.dmaq["estabilizador"] = list()
    powerflow.dmaq["user-estabilizador"] = list()
    powerflow.dmaq["reatancia-compensacao"] = list()
    powerflow.dmaq["barra-controlada"] = list()

    powerflow.linecount += 1
    powerflow.dmaq["ruler"] = powerflow.lines[powerflow.linecount][:]

    # Loop de leitura de linhas do `.stb`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Arquivos de Máquina
        while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
            if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                pass
            else:
                powerflow.dmaq["numero"].append(
                    powerflow.lines[powerflow.linecount][:5]
                )
                powerflow.dmaq["grupo"].append(
                    powerflow.lines[powerflow.linecount][8:10]
                )
                powerflow.dmaq["percentual-ativa"].append(
                    powerflow.lines[powerflow.linecount][11:14]
                )
                powerflow.dmaq["percentual-reativa"].append(
                    powerflow.lines[powerflow.linecount][15:18]
                )
                powerflow.dmaq["unidades"].append(
                    powerflow.lines[powerflow.linecount][19:22]
                )
                powerflow.dmaq["gerador"].append(
                    powerflow.lines[powerflow.linecount][23:29]
                )
                powerflow.dmaq["tensao"].append(
                    powerflow.lines[powerflow.linecount][30:36]
                )
                powerflow.dmaq["user-tensao"].append(
                    powerflow.lines[powerflow.linecount][36]
                )
                powerflow.dmaq["velocidade"].append(
                    powerflow.lines[powerflow.linecount][37:43]
                )
                powerflow.dmaq["user-velocidade"].append(
                    powerflow.lines[powerflow.linecount][43]
                )
                powerflow.dmaq["estabilizador"].append(
                    powerflow.lines[powerflow.linecount][44:50]
                )
                powerflow.dmaq["user-estabilizador"].append(
                    powerflow.lines[powerflow.linecount][50]
                )
                powerflow.dmaq["reatancia-compensacao"].append(
                    powerflow.lines[powerflow.linecount][51:56]
                )
                powerflow.dmaq["barra-controlada"].append(
                    powerflow.lines[powerflow.linecount][56:61]
                )
            powerflow.linecount += 1
        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{arquivoname}`!\033[0m")

    # DataFrame dos Dados de Agregadores Genericos
    powerflow.dmaqDF = DF(data=powerflow.dmaq)
    powerflow.dmaq = deepcopy(powerflow.dmaqDF)
    powerflow.dmaqDF = powerflow.dmaqDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dmaqDF = powerflow.dmaqDF.astype(
        {
            "numero": "int",
            "grupo": "int",
            "percentual-ativa": "float",
            "percentual-reativa": "float",
            "unidades": "int",
            "gerador": "int",
            "tensao": "int",
            "user-tensao": "object",
            "velocidade": "int",
            "user-velocidade": "object",
            "estabilizador": "int",
            "user-estabilizador": "object",
            "reatancia-compensacao": "float",
            "barra-controlada": "int",
        }
    )
    if powerflow.dmaqDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMAQ`!\033[0m"
        )
    else:
        powerflow.codes["DMAQ"] = True

        powerflow.dmaqDF = powerflow.dmaqDF.sort_values(by=["numero"], ascending=True)


def blt(
    powerflow,
    arquivo,
    arquivoname,
):
    """inicialização para leitura de dados

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.linecount = 0
    f = open(f"{arquivo}", "r", encoding="latin-1")
    powerflow.lines = f.readlines()
    f.close()

    # # Loop de leitura de linhas do `.stb`
    # while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
    # Dados de Arquivos de Entrada e Saida
    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount].strip() == "DMDG MD01":
            powerflow.linecount += 1
            powerflow.dmdg = dict()
            powerflow.dmdg["ruler"] = powerflow.lines[powerflow.linecount][:]
            md01(
                powerflow,
            )
            powerflow.linecount -= 1
        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f"\033[32mSucesso na leitura de arquivo `{arquivoname}`!\033[0m")


def md01(
    powerflow,
):
    """ "

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.dmdg["tipo"] = list()
    powerflow.dmdg["numero"] = list()
    powerflow.dmdg["l-transitoria"] = list()
    powerflow.dmdg["r-armadura"] = list()
    powerflow.dmdg["inercia"] = list()
    powerflow.dmdg["amortecimento"] = list()
    powerflow.dmdg["aparente"] = list()
    powerflow.dmdg["freq-sincrona"] = list()
    powerflow.dmdg["freq-correcao"] = list()

    while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
        if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
            pass
        else:
            powerflow.dmdg["tipo"].append("MD01")
            powerflow.dmdg["numero"].append(powerflow.lines[powerflow.linecount][:4])
            powerflow.dmdg["l-transitoria"].append(
                powerflow.lines[powerflow.linecount][7:12]
            )
            powerflow.dmdg["r-armadura"].append(
                powerflow.lines[powerflow.linecount][12:17]
            )
            powerflow.dmdg["inercia"].append(
                powerflow.lines[powerflow.linecount][17:22]
            )
            powerflow.dmdg["amortecimento"].append(
                powerflow.lines[powerflow.linecount][22:27]
            )
            powerflow.dmdg["aparente"].append(
                powerflow.lines[powerflow.linecount][27:32]
            )
            powerflow.dmdg["freq-sincrona"].append(
                powerflow.lines[powerflow.linecount][32:34]
            )
            powerflow.dmdg["freq-correcao"].append(
                powerflow.lines[powerflow.linecount][35]
            )
        powerflow.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    powerflow.dmdgDF = DF(data=powerflow.dmdg)
    powerflow.dmdg = deepcopy(powerflow.dmdgDF)
    powerflow.dmdgDF = powerflow.dmdgDF.replace(r"^\s*$", "0", regex=True)
    powerflow.dmdgDF = powerflow.dmdgDF.astype(
        {
            "tipo": "object",
            "numero": "int",
            "l-transitoria": "float",
            "r-armadura": "float",
            "inercia": "float",
            "amortecimento": "float",
            "aparente": "float",
            "freq-sincrona": "float",
            "freq-correcao": "object",
        }
    )
    if powerflow.dmdgDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DMDG MD01`!\033[0m"
        )
    else:
        powerflow.codes["DMDG MD01"] = True


def checktem(
    powerflow,
    arquivo,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    pasta = dirname(powerflow.dirSTB)
    arquivo = arquivo[1:].strip().replace("\\", "/")
    dirarquivo = pasta + arquivo

    if exists(dirarquivo) is True:
        print(
            f"\033[93mArquivo `{arquivo}` encontrado dentro de pasta `PyANA/sistemas/BDADOS/` conforme solicitado!\033[0m"
        )
        return dirarquivo, arquivo

    else:
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/BDADOS/` não contém o arquivo `{arquivo}` do SEP informado.\nInsira o arquivo `{arquivo}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
        )
