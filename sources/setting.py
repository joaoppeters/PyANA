# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from options import optionspwf, optionsstb
from path import pathpwf, pathstb
from pwf import pwf
from stb import stb


def pwfsetting(
    anarede,
):
    """configuracoes iniciais para simulacao estatica de fluxo de potencia

    Args
        anarede:  objeto da classe PowerFlowContainer
    """
<<<<<<< HEAD
    ## Inicializacao
    # Verificacao de diretorio
=======
    # Verificação de diretório
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    pathpwf(
        anarede,
    )

    # Classe para leitura de arquivo .pwf
    pwf(
        anarede,
        anarede.dirPWF,
    )

    # Classe para determinacao dos valores padrao das variaveis de tolerância
    optionspwf(
        anarede,
    )


def stbsetting(
    anarede,
    anatem,
):
    """configuracoes iniciais para simulacao dinâmica de fluxo de potencia

    Args
        anarede: objeto da classe PowerFlowContainer
        anatem:  objeto da classe PowerFlowContainer
    """
<<<<<<< HEAD
    ## Inicializacao
    # Verificacao de diretorio
=======
    # Verificação de diretório
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    pathstb(
        anarede,
        anatem,
    )

    # Classe para leitura de arquivo .stb
    stb(
        anatem,
    )

    # Classe para determinacao dos valores padrao das variaveis de tolerância
    optionsstb(
        anatem,
    )
