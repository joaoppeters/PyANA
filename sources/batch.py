# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from anarede import anarede
from rewrite import rewrite


def batch(
    powerflow,
):
    """batch de execução

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    case = 1
    rewrite(
        powerflow,
        case,
    )

    filepath = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas"
    powerflow.namecase = powerflow.name + "-" + case + ".pwf"
    anarede(filepath=filepath, filename=powerflow.namecase)
