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
        from admittance import admit
        from linear import linear
        from monitor import monitorfile
        from newton import newton
        from report import reportfile

        admit(
            powerflow,
        )

        linear(
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
        from admittance import admit
        from linear import linear
        from monitor import monitorfile
        from report import reportfile

        admit(
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
        from admittance import admit
        from continuation import prediction_correction
        from linear import linear
        from newton import newton
        from report import reportfile

        admit(
            powerflow,
        )

        linear(
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
        from admittance import admit
        from crossentropy import cent

        admit(
            powerflow,
        )

        cent(
            powerflow,
        )

    # Chamada especifica geracao estocastica inicial de valores
    elif powerflow.method == "EXSC":
        from admittance import admit
        from stochastic import stoch_apparent_1, stoch_apparent_2, stoch_apparent_3, multivariate_normal, rand0m

        admit(
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
        from admittance import admit
        from linear import linear
        from newton import newton
        from poc import poc
        from report import reportfile

        admit(
            powerflow,
        )

        linear(
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
    elif powerflow.method == "PWF":
        from rewrite import rewrite

        rewrite(
            powerflow,
        )

    # BATCH
    elif powerflow.method == "BATCH":
        from batch import batch

        batch(
            powerflow,
        )	
