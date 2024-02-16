# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import time
from os.path import dirname, exists, realpath
from os import mkdir

from ctrl import control
from monitor import monitor
from options import options
from pwf import pwf
from report import report

def setup(
    powerflow,
):
    """initialization

    Parameters
        powerflow: powerflow do arquivo powerflow.py
    """

    ## Inicialização
    if powerflow.system:
        # Verificação de diretório
        checkpath(
            powerflow,
        )

        # Classe para leitura de arquivo .pwf
        t = time.process_time()
        pwf(
            powerflow,
        )
        print(f"Leitura dos dados em {time.process_time() - t:2.3f}[s].")

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


def checkpath(
    powerflow,
):
    """verificação automática de diretório sistemas

    Parâmetros
        powerflow: powerflow do arquivo powerflow.py
    """

    ## Inicialização
    # Variável de diretório principal
    powerflow.maindir = dirname(dirname(__file__))

    # Variável de nome do SEP em estudo
    powerflow.name = powerflow.system.split(".")[0]

    if exists(powerflow.maindir + "/sistemas/") is True:
        if exists(powerflow.maindir + "/sistemas/" + powerflow.system) is True:
            powerflow.dirSEP = realpath(
                dirname(dirname(__file__)) + "/sistemas/" + powerflow.system
            )
            print(
                f"\033[93mArquivo `{powerflow.system}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
            )
        else:
            raise ValueError(
                f"\033[91mERROR: Pasta `PyANA/sistemas/` não contém o arquivo `{powerflow.system}` do SEP informado.\nInsira o arquivo `{powerflow.system}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
            )

    else:
        mkdir(powerflow.maindir + "/sistemas/")
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` acabou de ser criada.\nLembre-se de inserir o arquivo `{powerflow.system}` que contém os dados do SEP que gostaria de analisar na pasta e rode novamente!\033[0m"
        )
