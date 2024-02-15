# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def metodo(
    powerflow,
):
    """chamada automática do método de solução selecionado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.method == "NEWTON":
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
    elif powerflow.method == "CPF":
        from admittance import admit
        from continuation import cpf
        from newtonraphson import newton
        from report import reportfile

        admit(
            powerflow,
        )

        newton(
            powerflow,
        )

        cpf(
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
    elif powerflow.method == "STOCH":
        from admittance import admit
        from stochastic import stoch1, stoch2

        admit(
            powerflow,
        )

        stoch1(
            powerflow,
        )

        stoch2(
            powerflow,
        )

    # Chamada especifica metodo direto (Canizares, 1993)
    elif powerflow.method == "CANI":
        from admittance import admit
        from directmethod import cani
        from report import reportfile

        admit(
            powerflow,
        )

        cani(
            powerflow,
        )

        reportfile(
            powerflow,
        )

    #
    elif powerflow.method == "PWF":
        from filter import seletiva

        seletiva(
            powerflow,
        )
