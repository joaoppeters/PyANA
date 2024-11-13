# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import shutil


def savmove(
    filename: str,
    filedir: str,
):
    """

    Args:
        filename:
        filedir:
    """

    ## Inicialização
    savcheck(filename)
    shutil.copy2(filename, filedir)


def savcheck(
    filename: str,
):
    """

    Args:
        filename:
    """
    from os.path import exists

    ## Inicialização
    name = filename.split("\\")[-1]
    if exists(filename) is True:
        return True
    else:
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` não contém o arquivo `{name}` do SEP informado.\nInsira o arquivo `{name}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
        )
