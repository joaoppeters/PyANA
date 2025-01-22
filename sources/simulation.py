# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def simulation(
    powerflow,
):
    """chamada automática do método de solução selecionado

    Args
        powerflow:
    """
    ## Inicialização
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.sim == "EXLF":
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
    elif powerflow.sim == "EXIC":
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
    elif powerflow.sim == "EXPC":
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
    elif powerflow.sim == "EXSI":
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
    elif powerflow.sim == "BXLF":
        from anarede import batchrunning

        batchrunning(
            file=powerflow.dirPWF,
            time=2,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.sim == "BXIC":
        from anarede import batchrunning

        batchrunning(
            file=powerflow.dirPWF,
            time=60,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.sim == "BXCT":
        from anarede import batchrunning

        batchrunning(
            file=powerflow.dirPWF,
            time=20,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.sim == "SXLF":
        from areas import q2024, ne224
        from batch import stochsxlf
        from factor import generator_participation
        from folder import areasfolder
        from setting import pathstb
        from stb import stb
        from ulog import basexlf

        pathstb(
            powerflow,
        )

        stb(
            powerflow,
        )

        powerflow.namecase = powerflow.name + "jpmod"

        areasfolder(
            powerflow,
        )
        if "NE224" in powerflow.name:
            ne224(
                powerflow,
            )
        elif "Q2024" in powerflow.name:
            q2024(
                powerflow,
            )

        powerflow.mdger = generator_participation(
            name=powerflow.name,
            dbarDF=powerflow.dbarDF.copy(),
            dger=powerflow.dger.copy(),
        )

        basexlf(
            powerflow,
        )

        # stochsxlf(
        #     powerflow,
        # )

    # Chamada especifica para analise de fluxo de potência continuado em arquivos com dados estocasticos
    elif powerflow.sim == "SXIC":
        from areas import q2024, ne224
        from batch import stochsxic
        from factor import generator_participation
        from folder import areasfolder
        from strat import strat
        from ulog import basexic

        areasfolder(
            powerflow,
        )
        if "NE224" in powerflow.name:
            ne224(
                powerflow,
            )
        elif "Q2024" in powerflow.name:
            q2024(
                powerflow,
            )

        powerflow.mdger = generator_participation(
            name=powerflow.name,
            dbarDF=powerflow.dbarDF.copy(),
            dger=powerflow.dger.copy(),
        )

        # strat(
        #     powerflow,
        # )

        basexic(
            powerflow,
            start=6,
            stop=15,
            midstop=10,
            mult=0.1,
            time=300,
        )

        # stochsxic(
        #     powerflow,
        # )

    # Chamada especifica para analise de contingencia em arquivos com dados estocasticos
    elif powerflow.sim == "SXCT":
        from batch import stochsxct

        stochsxct(
            powerflow,
        )

    # Chamada especifica para analise de fluxo de potência continuado e contingencia em arquivos com dados estocasticos
    elif powerflow.sim == "SPVCT":
        from batch import stochspvct

        stochspvct(
            powerflow,
        )

    # Chamada específica para geração de arquivo contendo formatação de dados de simulação PSS/E (EXCEL FILE FORMATTING)
    elif powerflow.sim == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )

    # Chamada específica para leitura de arquivos .REL
    elif powerflow.sim == "RREL":
        from rela import rrel

        rrel(
            powerflow,
        )

    # Chamada específica para manipulação de dados (DATA MANIPULATION - CASE BY CASE DEMAND)
    elif powerflow.sim == "DATA":
        from fdata import fdata

        fdata(
            powerflow,
        )

    # Chamada especifica metodo Cross-Entropy
    elif powerflow.sim == "CENT":
        from matrices import admittance
        from crossentropy import cent

        admittance(
            powerflow,
        )

        cent(
            powerflow,
        )

    # Chamada específica para análise de areas
    elif powerflow.sim == "AREA":
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
    elif powerflow.sim == "RPVCT":
        from rela import relpvct

        relpvct(
            powerflow,
        )

    elif powerflow.sim == "Q2024":
        from rela import q2024

        q2024(
            powerflow,
        )

    elif powerflow.sim == "VSM":
        from rela import vsm

        vsm(
            powerflow,
        )
