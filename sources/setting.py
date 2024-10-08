# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists, realpath
from os import mkdir

from ctrl import control
from monitor import monitor
from options import options
from pwf import pwf
from report import report


def setting(
    powerflow,
):
    """initialization

    Args
        powerflow: powerflow do arquivo powerflow.py
    """

    ## Inicialização
    if powerflow.system:
        # Verificação de diretório
        pathpwf(
            powerflow,
        )

        # Classe para leitura de arquivo .pwf
        pwf(
            powerflow,
        )

        # Classe para determinação dos valores padrão das variáveis de tolerância
        options(
            powerflow,
        )

        # Classe para determinar a realização das opções de controle escolhidas
        control(
            powerflow,
        )

        # Classe para determinar a realização de monitoramento de valores
        monitor(
            powerflow,
        )

        # Classe para determinar a geração de relatórios
        report(
            powerflow,
        )

    else:
        ## ERROR - VERMELHO
        raise ValueError("\033[91mNenhum sistema foi selecionado.\033[0m")


def pathpwf(
    powerflow,
):
    """verificação automática de diretório sistemas

    Args
        powerflow: powerflow do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.anarede = powerflow.system

    # Variável de diretório principal
    powerflow.maindir = dirname(dirname(__file__))

    # Variável de nome do SEP em estudo
    powerflow.name = powerflow.anarede.split(".")[0]

    if exists(powerflow.maindir + "/sistemas/") is True:
        if exists(powerflow.maindir + "/sistemas/" + powerflow.anarede) is True:
            powerflow.dirPWF = realpath(
                powerflow.maindir + "/sistemas/" + powerflow.anarede
            )
            print(
                f"\033[93mArquivo `{powerflow.anarede}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
            )
        else:
            raise ValueError(
                f"\033[91mERROR: Pasta `PyANA/sistemas/` não contém o arquivo `{powerflow.anarede}` do SEP informado.\nInsira o arquivo `{powerflow.anarede}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
            )

    else:
        mkdir(powerflow.maindir + "/sistemas/")
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` acabou de ser criada.\nLembre-se de inserir o arquivo `{powerflow.anarede}` que contém os dados do SEP que gostaria de analisar na pasta e rode novamente!\033[0m"
        )


def pathstb(
    powerflow,
):
    """verificação automática de diretório sistemas

    Args
        powerflow: powerflow do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.anatem = powerflow.name + ".stb"
    if exists(powerflow.maindir + "/sistemas/" + powerflow.anatem) is True:
        powerflow.dirSTB = realpath(
            dirname(dirname(__file__)) + "/sistemas/" + powerflow.anatem
        )
        print(
            f"\033[93mArquivo `{powerflow.anatem}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
        )
    else:
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` não contém o arquivo `{powerflow.anatem}` do SEP informado.\nInsira o arquivo `{powerflow.anatem}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
        )
