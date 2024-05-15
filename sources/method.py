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
        from monitor import monitorfile
        from newtonraphson import newton
        from report import reportfile

        admit(
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

    # Chamada específica método de Gauss-Seidel
    elif powerflow.method == "GAUSS":
        # self.gaussseidel(
        #     powerflow,
        # )
        pass

    # Chamada específica método de Newton-Raphson Linearizado
    elif powerflow.method == "LINEAR":
        from admittance import admitlinear
        from linear import lpf
        from monitor import monitorfile
        from report import reportfile

        admitlinear(
            powerflow,
        )

        lpf(
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

    # Chamada específica método Desacoplado Rápido
    elif powerflow.method == "fDECOUP":
        # self.fastdecoupledpowerflow(
        #     powerflow,
        # )
        pass

    # Chamada específica método Continuado
    elif powerflow.method == "EXIC":
        from admittance import admit
        from continuation import prediction_correction
        from newtonraphson import newton
        from report import reportfile

        admit(
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
        from direct import poc
        from newtonraphson import newton
        from report import reportfile

        admit(
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

    #
    elif powerflow.method == "EXDT":
        from fdata import fdata

        fdata(
            powerflow,
        )

    #
    elif powerflow.method == "PWF":
        from dwrite import savepwf

        savepwf(
            powerflow,
        )
