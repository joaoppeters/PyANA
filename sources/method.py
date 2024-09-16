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

    Parâmetros
        powerflow: self do arquivo powerflow.py
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
    elif powerflow.method == "BPWF":
        from anarede import anarede

        powerflow.batchtime = 10
        
        anarede(
            powerflow.batchtime,
            powerflow.dirPWF,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "bXSC":
        from batch import stochbatch
        from setting import pathstb
        from stb import stb

        pathstb(
            powerflow,
        )

        stb(
            powerflow, 
        )

        powerflow.namecase = powerflow.name + "jpmod"

        stochbatch(
            powerflow,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "bXIC":
        pass

        

    # # Chamada especifica geracao estocastica inicial de valores
    # elif powerflow.method == "bXCT":
    #     from batch import stochbatch
    #     from setting import pathstb
    #     from stb import stb

    #     pathstb(
    #         powerflow,
    #     )

    #     stb(
    #         powerflow,
    #     )

    #     powerflow.namecase = powerflow.name + "jpmod"

    #     stochbatch(
    #         powerflow,
    #     )

    # Chamada específica para geração de arquivo contendo formatação de dados de simulação PSS/E (EXCEL FILE FORMATTING)
    elif powerflow.method == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )

    # Chamada específica para reescrita de documentos .pwf (ROMAN KUIAVA REQUIREMENTS)
    elif powerflow.method == "RPWF":
        from rwpwf import rwpwf

        rwpwf(
            powerflow,
        )
        
    # Chamada específica para leitura de arquivos .REL
    elif powerflow.method == "REL":
        from rel import rel
        
        rel(
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

    # Chamada específicada para análise de contingências
    elif powerflow.method == "EXCT":
        from rwpwf import rwpwf

        powerflow.namecase = powerflow.name + "-dctg"

        rwpwf(
            powerflow,
        )
