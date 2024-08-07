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

    # Chamada específica método de Newton-Raphson Linearizado
    elif powerflow.method == "LFDC":
        pass

    # Chamada específica método Desacoplado
    elif powerflow.method == "DECOUP":
        pass

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

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "EXSC":
        pass

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

    # Chamada específica para manipulação de dados (DATA MANIPULATION - CASE BY CASE DEMAND)
    elif powerflow.method == "DATA":
        from fdata import fdata

        fdata(
            powerflow,
        )

    # Chamada específica para reescrita de documentos .pwf (ROMAN KUIAVA REQUIREMENTS)
    elif powerflow.method == "RPWF":
        from rewrite import rewrite

        rewrite(
            powerflow,
        )

    # Chamada específica para ANAREDE BATCH RUNNING SCRIPT
    elif powerflow.method == "BPWF":
        from batch import batch

        powerflow.namecase = powerflow.name + "jpmod"
        powerflow.exicflag = False
        powerflow.exctflag = True

        if not powerflow.exicflag and not powerflow.exctflag:
            powerflow.batchtime = 5
        elif (powerflow.exicflag and not powerflow.exctflag) or (not powerflow.exicflag and powerflow.exctflag):
            powerflow.batchtime = 30
        elif powerflow.exicflag and powerflow.exctflag:
            powerflow.batchtime = 50

        batch(
            powerflow,
        )

    # Chamada Específica para simulação dinâmica
    elif powerflow.method == "EXSI":
        from matrices import admittance
        from dynamic import dynamic
        from newton import newton
        from setup import pathstb
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

    # Chamada específica para geração de arquivo contendo formatação de dados de simulação PSS/E (EXCEL FILE FORMATTING)
    elif powerflow.method == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )

    # Chamada específicada para análise de contingências
    elif powerflow.method == "EXCT":
        from rewrite import rewrite

        powerflow.namecase = powerflow.name + "-dctg"

        rewrite(
            powerflow,
        )

    # Chamada específica para análise de sensibilidade à variação de carga
    elif powerflow.method == "AROU":
        from increment import arou

        powerflow.namecase = powerflow.name + "-loadvar"

        arou(
            powerflow,
        )
        
    # Chamada específica para 
    elif powerflow.method == "REL":
        from rel import rel
        
        rel(
            powerflow,
        )
