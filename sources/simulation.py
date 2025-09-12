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