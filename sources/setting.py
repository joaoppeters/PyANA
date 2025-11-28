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
    """configurações iniciais para simulação estática de fluxo de potência

    Args
        anarede:  objeto da classe PowerFlowContainer
    """
    ## Inicialização
    # Verificação de diretório
    pathpwf(
        anarede,
    )

    # Classe para leitura de arquivo .pwf
    pwf(
        anarede,
        anarede.dirPWF,
    )

    # Classe para determinação dos valores padrão das variáveis de tolerância
    optionspwf(
        anarede,
    )


def stbsetting(
    anarede,
    anatem,
):
    """configurações iniciais para simulação dinâmica de fluxo de potência

    Args
        anarede: objeto da classe PowerFlowContainer
        anatem:  objeto da classe PowerFlowContainer
    """
    ## Inicialização
    # Verificação de diretório
    pathstb(
        anarede,
        anatem,
    )

    # Classe para leitura de arquivo .stb
    stb(
        anatem,
    )

    # Classe para determinação dos valores padrão das variáveis de tolerância
    optionsstb(
        anatem,
    )
