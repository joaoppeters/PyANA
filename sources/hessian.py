# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from ctrl import controlhess, controljacsym

def hessian(
    powerflow,
):
    """cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    