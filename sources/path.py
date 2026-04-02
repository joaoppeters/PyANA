# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists, realpath
from os import mkdir


def pathpwf(
    anarede,
):
    """verificacao automatica de diretorio sistemas

    Args
        anarede: objeto da classe PowerFlowContainer
    """
    ## Inicializacao
    # Variavel de diretorio principal
    anarede.maindir = dirname(dirname(__file__))

    # Variavel de nome do SEP em estudo
    anarede.name = anarede.system.split(".")[0]

    if exists(anarede.maindir + "\\sistemas\\") is True:
        if exists(anarede.maindir + "\\sistemas\\" + anarede.system) is True:
            anarede.dirPWF = realpath(
                anarede.maindir + "\\sistemas\\" + anarede.name + ".pwf"
            )
            print(
                f"\033[93mArquivo `{anarede.name + '.pwf'}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
            )
        else:
            raise ValueError(
                f"\033[91mERROR: Pasta `PyANA/sistemas/` nao contem o arquivo `{anarede.name + '.pwf'}` do SEP informado.\nInsira o arquivo `{anarede.name + '.pwf'}` que contem os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
            )

    else:
        mkdir(anarede.maindir + "\\sistemas\\")
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` acabou de ser criada.\nLembre-se de inserir o arquivo `{anarede.name + '.pwf'}` que contem os dados do SEP que gostaria de analisar na pasta e rode novamente!\033[0m"
        )


def pathstb(
    anarede,
    anatem,
):
    """verificacao automatica de diretorio sistemas

    Args
        anatem: objeto da classe PowerFlowContainer
    """
    ## Inicializacao
    # Variavel de diretorio principal
    anatem.maindir = dirname(dirname(__file__))
    if exists(anatem.maindir + "\\sistemas\\" + anatem.system) is True:
        anatem.dirSTB = realpath(
            anatem.maindir + "\\sistemas\\" + anarede.name + ".stb"
        )
        print(
            f"\033[93mArquivo `{anarede.name + '.stb'}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
        )
    else:
        raise ValueError(
            f"\033[91mERROR: Pasta `PyANA/sistemas/` nao contem o arquivo `{anarede.name + '.stb'}` do SEP informado.\nInsira o arquivo `{anarede.name + '.stb'}` que contem os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
        )


def pathdarq(
    anatem,
):
    """verificacao automatica de diretorio sistemas

    Args
        anatem: objeto da classe PowerFlowContainer
    """

    from darq import rdat, rcdu, rblt
    from folder import logfolder, outfolder, pltfolder

    ## Inicializacao
    for idx, value in anatem.darqDF.iterrows():
        if value.tipo.strip() in ["LOG", "OUT", "PLT"]:
            anatem.logfolder = (
                logfolder(anatem.maindir + "\\sistemas\\LOG\\")
                if (value.tipo.strip() == "LOG")
                else None
            )
            anatem.outfolder = (
                outfolder(anatem.maindir + "\\sistemas\\OUT\\")
                if (value.tipo.strip() == "OUT")
                else None
            )
            anatem.pltfolder = (
                pltfolder(anatem.maindir + "\\sistemas\\PLT\\")
                if (value.tipo.strip() == "PLT")
                else None
            )
        elif exists(anatem.maindir + "\\sistemas\\" + value.nome.strip()) is False:
            raise ValueError(
                f"\033[91mERROR: Pasta `PyANA/sistemas/` nao contem o arquivo `{value['nome']}` do SEP informado.\nInsira o arquivo `{value['nome']}` que contem os dados adicionais do SEP que gostaria de analisar na pasta e rode novemente!\033[0m"
            )
        else:
            print(
                f"\033[93mArquivo `{value.nome.strip()}` contendo dados do SEP encontrado dentro de pasta `PyANA/sistemas/` conforme solicitado!\033[0m"
            )
            (
                rdat(
                    anatem,
                    anatem.maindir + "\\sistemas\\" + value.nome.strip(),
                    value.nome.strip(),
                )
                if (value.tipo.strip() == "DAT")
                else None
            )
            (
                rcdu(
                    anatem,
                    anatem.maindir + "\\sistemas\\" + value.nome.strip(),
                    value.nome.strip(),
                )
                if (value.tipo.strip() == "CDU")
                else None
            )
            (
                rblt(
                    anatem,
                    anatem.maindir + "\\sistemas\\" + value.nome.strip(),
                    value.nome.strip(),
                )
                if (value.tipo.strip() == "BLT")
                else None
            )
