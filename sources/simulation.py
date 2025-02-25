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
        from areas import q2024, ne224
        from factor import generator_participation
        from folder import areasfolder
        from ulog import basexlf

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

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BXIC":
        from factor import generator_participation
        from strat import strat
        from ulog import multexic

        powerflow.mdger = generator_participation(
            name=powerflow.name,
            dbarDF=powerflow.dbarDF.copy(),
            dger=powerflow.dger.copy(),
        )

        # strat(
        #     powerflow,
        # )

        multexic(
            powerflow,
            start=6,
            stop=15,
            midstop=10,
            mult=0.1,
            time=300,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BXCT":
        from anarede import anarede

        anarede(
            file=powerflow.dirPWF,
            time=20,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "SXLF":
        from areas import q2024, ne224
        from factor import generator_participation
        from folder import areasfolder
        from stochastic import sxlf

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

        powerflow.namecase = powerflow.name + "jpmod"

        sxlf(
            powerflow,
        )

    # Chamada especifica para analise de fluxo de potência continuado em arquivos com dados estocasticos
    elif powerflow.method == "SXIC":
        from stochastic import sxic

        sxic(
            powerflow,
        )

    # Chamada especifica para analise de contingencia em arquivos com dados estocasticos
    elif powerflow.method == "SXCT":
        from stochastic import sxct

        sxct(
            powerflow,
        )

    # Chamada especifica para analise de fluxo de potência continuado e contingencia em arquivos com dados estocasticos
    elif powerflow.method == "SPVCT":
        from stochastic import spvct

        spvct(
            powerflow,
        )

    # Chamada específica para geração de arquivo contendo formatação de dados de simulação PSS/E (EXCEL FILE FORMATTING)
    elif powerflow.method == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )

    # Chamada específica para leitura de arquivos .REL (RELATORIO TOTAL DE AREA)
    elif powerflow.method == "RTOT":
        from rela import rtot

        rtot(
            powerflow,
        )

    # Chamada específica para leitura de arquivos .REL (RELATORIO DE INTERCAMBIOS)
    elif powerflow.method == "RINT":
        from rela import rint

        rint(
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
        from rela import relpvct

        relpvct(
            powerflow,
        )

    elif powerflow.method == "VSM":
        from rela import vsm

        vsm(
            powerflow,
        )

    elif powerflow.method == "CXLF":
        from areas import q2024, ne224
        from cluster import cxlf
        from folder import areasfolder
        from normal import samples

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
            powerflow.lmean = powerflow.cargas.demanda_ativa[
                powerflow.cargas.demanda_ativa > 0
            ].sum()
            powerflow.sload = samples(
                mean=powerflow.lmean,
                stddev=(15 * 1e-2) * powerflow.lmean,
                seed=1,
                samples=1000,
            )
            powerflow.wmean = powerflow.nordeste[
                powerflow.nordeste.nome.str.contains("EOL|EO-")
                & (powerflow.nordeste.potencia_ativa > 0.0)
            ].potencia_ativa.sum()
            powerflow.swind = samples(
                mean=powerflow.wmean,
                stddev=(15 * 1e-2) * powerflow.wmean,
                seed=1,
                samples=1000,
            )

        cxlf(
            powerflow,
        )

    elif powerflow.method == "CXIC":
        from areas import q2024, ne224
        from cluster import cxic
        from folder import areasfolder
        from normal import samples

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
            powerflow.lmean = powerflow.cargas.demanda_ativa[
                powerflow.cargas.demanda_ativa > 0
            ].sum()
            powerflow.sload = samples(
                mean=powerflow.lmean,
                stddev=(15 * 1e-2) * powerflow.lmean,
                seed=1,
                samples=1000,
            )
            powerflow.wmean = powerflow.nordeste[
                powerflow.nordeste.nome.str.contains("EOL|EO-")
                & (powerflow.nordeste.potencia_ativa > 0.0)
            ].potencia_ativa.sum()
            powerflow.swind = samples(
                mean=powerflow.wmean,
                stddev=(15 * 1e-2) * powerflow.wmean,
                seed=1,
                samples=1000,
            )

        cxic(
            powerflow,
        )

    elif powerflow.method == "CXCT":
        from cluster import cxct

        cxct(
            powerflow,
        )

    elif powerflow.method == "SNTS":
        from  snts import snts

        snts(
            powerflow,
        )