# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def methodo(
    powerflow,
):
    """chamada automática do método de solução selecionado

    Args
        powerflow:
    """

    ## Inicialização
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.method == "EXLF":
        from matrices import admittance
        from monitor import monitorfile
        from newton import newton
        from report import reportfile

        admittance(
            powerflow,
        )

        newton(
            powerflow,
        )

        reportfile(
            powerflow,
        )

        monitorfile(
            powerflow,
        )

    # Chamada específica método Continuado
    elif powerflow.method == "EXIC":
        from matrices import admittance
        from continuation import prediction_correction
        from newton import newton
        from report import reportfile

        admittance(
            powerflow,
        )

        newton(
            powerflow,
        )

        prediction_correction(
            powerflow,
        )

        reportfile(
            powerflow,
        )

    # Chamada especifica metodo direto (Canizares, 1993)
    elif powerflow.method == "EXPC":
        from matrices import admittance
        from newton import newton
        from poc import poc
        from report import reportfile

        admittance(
            powerflow,
        )

        newton(
            powerflow,
        )

        poc(
            powerflow,
        )

        reportfile(
            powerflow,
        )

    # Chamada Específica para simulação dinâmica
    elif powerflow.method == "EXSI":
        from matrices import admittance
        from dynamic import dynamic
        from newton import newton
        from setting import pathstb
        from stb import stb

        pathstb(
            powerflow,
        )

        stb(
            powerflow,
        )

        admittance(
            powerflow,
        )

        newton(
            powerflow,
        )

        dynamic(
            powerflow,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BXLF":
        from anarede import anarede

        powerflow.batchtime = 10

        anarede(
            powerflow.batchtime,
            powerflow.dirPWF,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BXIC":
        from anarede import anarede

        powerflow.batchtime = 10

        anarede(
            powerflow.batchtime,
            powerflow.dirPWF,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BXCT":
        from anarede import anarede

        powerflow.batchtime = 10

        anarede(
            powerflow.batchtime,
            powerflow.dirPWF,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "SXSC":
        from batch import stochsxsc
        from setting import pathstb
        from stb import stb

        pathstb(
            powerflow,
        )

        stb(
            powerflow,
        )

        powerflow.namecase = powerflow.name + "jpmod"

        stochsxsc(
            powerflow,
        )

    # Chamada especifica para analise de fluxo de potência continuado em arquivos com dados estocasticos
    elif powerflow.method == "SXIC":
        from batch import stochsxic

        stochsxic(
            powerflow,
        )

    # Chamada especifica para analise de contingencia em arquivos com dados estocasticos
    elif powerflow.method == "SXCT":
        from batch import stochsxct

        stochsxct(
            powerflow,
        )

    # Chamada especifica para analise de fluxo de potência continuado e contingencia em arquivos com dados estocasticos
    elif powerflow.method == "SXICT":
        from batch import stochsxict

        stochsxict(
            powerflow,
        )

    # Chamada específica para geração de arquivo contendo formatação de dados de simulação PSS/E (EXCEL FILE FORMATTING)
    elif powerflow.method == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )

    # Chamada específica para leitura de arquivos .REL
    elif powerflow.method == "RELR":
        from rel import relr

        relr(
            powerflow,
        )

    # Chamada específica para manipulação de dados (DATA MANIPULATION - CASE BY CASE DEMAND)
    elif powerflow.method == "DATA":
        from fdata import fdata

        fdata(
            powerflow,
        )

    # Chamada especifica metodo Cross-Entropy
    elif powerflow.method == "CENT":
        from matrices import admittance
        from crossentropy import cent

        admittance(
            powerflow,
        )

        cent(
            powerflow,
        )

    # Chamada específica para análise de areas
    elif powerflow.method == "AREA":
        from areas import q2024, ne224
        from folder import areasfolder

        areasfolder(
            powerflow,
        )

        if "2Q2024" in powerflow.name:
            q2024(
                powerflow,
            )

        elif "NE224" in powerflow.name:
            ne224(
                powerflow,
            )

    # Chamada específica para leitura dos relatórios de fluxo de potência continuado com contingência
    elif powerflow.method == "RPVCT":
        from rel import relpvct

        relpvct(
            powerflow,
        )
