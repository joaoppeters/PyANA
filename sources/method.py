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
        from matrices import admittance
        from linear import linear
        from monitor import monitorfile
        from report import reportfile

        admittance(
            powerflow,
        )

        linear(
            powerflow,
        )

        monitorfile(
            powerflow,
        )

        reportfile(
            powerflow,
        )

    # Chamada específica método Desacoplado
    elif powerflow.method == "DECOUP":
        # self.decoupledpowerflow(
        #     powerflow,
        # )
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
        from matrices import admittance
        from stochastic import (
            stoch_apparent_1,
            stoch_apparent_2,
            stoch_apparent_3,
            multivariate_normal,
            rand0m,
        )

        admittance(
            powerflow,
        )

        stoch_apparent_1(
            powerflow,
        )

        stoch_apparent_2(
            powerflow,
        )

        stoch_apparent_3(
            powerflow,
        )

        multivariate_normal(
            powerflow,
        )

        rand0m(
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

    # DATA MANIPULATION - CASE BY CASE DEMAND
    elif powerflow.method == "DATA":
        from fdata import fdata

        fdata(
            powerflow,
        )

    # ROMAN KUIAVA REQUIREMENTS
    elif powerflow.method == "RPWF":
        from rewrite import rewrite

        rewrite(
            powerflow,
        )

    # BATCH
    elif powerflow.method == "BPWF":
        from batch import batch

        powerflow.namecase = powerflow.name + "jpmod"

        batch(
            powerflow,
        )

    # Simulação Dinâmica
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


    # PSS/E EXCEL FILE FORMATTING
    elif powerflow.method == "PSSe":
        from psse import pssexcel

        pssexcel(
            powerflow,
        )