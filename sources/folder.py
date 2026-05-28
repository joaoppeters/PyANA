# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists
from os import mkdir


def folder(
    anarede,
):
    """Inicializacao

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
    # Diretorio de Sistemas
=======
    # Diretório de Sistemas
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    dirSistemas = dirname(anarede.dirPWF)

    # Criacao de diretorio Resultados
    anarede.resultsfolder = dirname(dirSistemas) + "\\resultados\\"
    if exists(anarede.resultsfolder) is False:
        mkdir(anarede.resultsfolder)


def areasfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de analise de area

    Args
        anarede:
        name: nome do diretorio
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.infofolder = anarede.resultsfolder + "iNFO\\"
    if exists(anarede.infofolder) is False:
        mkdir(anarede.infofolder)


def admittancefolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de matriz admitância

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.admittancefolder = anarede.resultsfolder + "MatrizAdmitancia\\"
    if exists(anarede.admittancefolder) is False:
        mkdir(anarede.admittancefolder)

    anarede.admittancefolder = anarede.admittancefolder + anarede.name + "\\"
    if exists(anarede.admittancefolder) is False:
        mkdir(anarede.admittancefolder)


def bxlffolder(
    anarede,
):
    """

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        mkdir(anarede.exlffolder)

    anarede.bxlffolder = anarede.exlffolder + "BASE\\"
    if exists(anarede.bxlffolder) is False:
        mkdir(anarede.bxlffolder)


def bxicfolder(
    anarede,
):
    """

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    bxlffolder(
        anarede,
    )
    anarede.exicfolder = dirname(anarede.dirPWF) + "\\EXIC\\"
    if exists(anarede.exicfolder) is False:
        mkdir(anarede.exicfolder)

    anarede.bxicfolder = anarede.exicfolder + "BASE\\"
    if exists(anarede.bxicfolder) is False:
        mkdir(anarede.bxicfolder)


def bxctfolder(
    anarede,
    where: str = "EXLF",
):
    """

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    bxicfolder(
        anarede,
    )

    anarede.exctfolder = dirname(anarede.dirPWF) + "\\EXCT\\"
    if exists(anarede.exctfolder) is False:
        mkdir(anarede.exctfolder)

    anarede.bxctfolder = anarede.exctfolder + "BASE\\"
    if exists(anarede.bxctfolder) is False:
        mkdir(anarede.bxctfolder)


def convergencefolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados da trajetoria de convergencia

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.convergencefolder = anarede.resultsfolder + "TrajetoriaConvergencia\\"
    if exists(anarede.convergencefolder) is False:
        mkdir(anarede.convergencefolder)

    anarede.convergencefolder = anarede.convergencefolder + anarede.name + "\\"
    if exists(anarede.convergencefolder) is False:
        mkdir(anarede.convergencefolder)


def continuationfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de fluxo de potencia continuado

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.continuationfolder = anarede.resultsfolder + "Continuado\\"
    if exists(anarede.continuationfolder) is False:
        mkdir(anarede.continuationfolder)

    anarede.systemcontinuationfolder = anarede.continuationfolder + anarede.name + "\\"
    if exists(anarede.systemcontinuationfolder) is False:
        mkdir(anarede.systemcontinuationfolder)

    anarede.systemcontinuationfolderimag = (
        anarede.systemcontinuationfolder + "imagens\\"
    )
    if exists(anarede.systemcontinuationfolderimag) is False:
        mkdir(anarede.systemcontinuationfolderimag)

    anarede.systemcontinuationfoldertxt = anarede.systemcontinuationfolder + "txt\\"
    if exists(anarede.systemcontinuationfoldertxt) is False:
        mkdir(anarede.systemcontinuationfoldertxt)


def jacobifolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de matriz jacobiana

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.jacobifolder = anarede.resultsfolder + "MatrizJacobiana\\"
    if exists(anarede.jacobifolder) is False:
        mkdir(anarede.jacobifolder)

    anarede.jacobifolder = anarede.jacobifolder + anarede.name + "\\"
    if exists(anarede.jacobifolder) is False:
        mkdir(anarede.jacobifolder)


def logfolder(
    logfolder,
):
    """criacao de diretorio para armazenar arquivos de log

    Args
        directory:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    if exists(logfolder) is False:
        mkdir(logfolder)
    return logfolder


def matpowerfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados no formato do matpower

    Args
        anarede:
    """
    ## Inicializacao
    anarede.matpowerfolder = dirname(dirname(__file__)) + "\\sistemas\\matpower\\"
    if exists(anarede.matpowerfolder) is False:
        mkdir(anarede.matpowerfolder)
    return anarede.matpowerfolder


def organonfolder(
    anarede,
):
    """criacao de diretorio para armazenar arquivos CDU

    Args
        none
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    cdufolder = dirname(dirname(__file__)) + "\\sistemas\\organon\\"
    if not exists(cdufolder):
        mkdir(cdufolder)
    return cdufolder


def outfolder(
    outfolder,
):
    """criacao de diretorio para armazenar arquivos de saida

    Args
        directory:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    if exists(outfolder) is False:
        mkdir(outfolder)
    return outfolder


def pltfolder(
    pltfolder,
):
    """criacao de diretorio para armazenar arquivos de plotagem

    Args
        directory:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    if exists(pltfolder) is False:
        mkdir(pltfolder)
    return pltfolder


def pssefolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados no formato do PSSe

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.pssefolder = dirname(dirname(__file__)) + "\\sistemas\\psse\\"
    if exists(anarede.pssefolder) is False:
        mkdir(anarede.pssefolder)
    return anarede.pssefolder


def reportsfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de relatorios

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    folder(
        anarede,
    )
    anarede.reportsfolder = anarede.resultsfolder + anarede.name + "\\"
    if exists(anarede.reportsfolder) is False:
        mkdir(anarede.reportsfolder)


def rbarfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de analise de barra

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    bxctfolder(
        anarede,
    )
    anarede.rbarxlffolder = anarede.exlffolder + "RBAR\\"
    if exists(anarede.rbarxlffolder) is False:
        mkdir(anarede.rbarxlffolder)

    anarede.rbarxicfolder = anarede.exicfolder + "RBAR\\"
    if exists(anarede.rbarxicfolder) is False:
        mkdir(anarede.rbarxicfolder)

    anarede.rbarxctfolder = anarede.exctfolder + "RBAR\\"
    if exists(anarede.rbarxctfolder) is False:
        mkdir(anarede.rbarxctfolder)


def rintfolder(
    anarede,
):
    """

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    anarede.exicfolder = dirname(anarede.dirPWF) + "\\EXIC\\"
    if exists(anarede.exlffolder) is False:
        mkdir(anarede.exlffolder)
    if exists(anarede.exicfolder) is False:
        mkdir(anarede.exicfolder)

    anarede.rintfolder = anarede.exlffolder + "RINT\\"
    if exists(anarede.rintfolder) is False:
        mkdir(anarede.rintfolder)


def rlinfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de analise de linha

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    bxctfolder(
        anarede,
    )
    anarede.rlinxlffolder = anarede.exlffolder + "RLIN\\"
    if exists(anarede.rlinxlffolder) is False:
        mkdir(anarede.rlinxlffolder)

    anarede.rlinxicfolder = anarede.exicfolder + "RLIN\\"
    if exists(anarede.rlinxicfolder) is False:
        mkdir(anarede.rlinxicfolder)

    anarede.rlinxctfolder = anarede.exctfolder + "RLIN\\"
    if exists(anarede.rlinxctfolder) is False:
        mkdir(anarede.rlinxctfolder)


def rtotfolder(
    anarede,
):
    """

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        mkdir(anarede.exlffolder)

    anarede.rtotfolder = anarede.exlffolder + "RTOT\\"
    if exists(anarede.rtotfolder) is False:
        mkdir(anarede.rtotfolder)


def sagefolder(
    anarede,
    pwffile,
):
    """criacao de diretorio para armazenar resultados de SAGE

    Args
        anarede:
        pwffile:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    sagefolder = dirname(anarede.dirPWF) + "\\SAGE\\"
    if exists(sagefolder) is False:
        mkdir(sagefolder)

    anarede.sagefolder = sagefolder + pwffile.removesuffix(".PWF") + "\\"
    if exists(anarede.sagefolder) is False:
        mkdir(anarede.sagefolder)


def smoothfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados suaves

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
    # Condicao de metodo
=======
    # Condição de método
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    if anarede.method == "EXLF":
        anarede.dirsmooth = anarede.resultsfolder + "Smooth\\"
        if exists(anarede.dirsmooth) is False:
            mkdir(anarede.dirsmooth)

        anarede.dirsmoothsys = anarede.dirsmooth + anarede.name + "\\"
        if exists(anarede.dirsmoothsys) is False:
            mkdir(anarede.dirsmoothsys)

    elif anarede.method == "EXIC":
        anarede.dirsmoothsys = anarede.systemcontinuationfolder + "smooth\\"
        if exists(anarede.dirsmoothsys) is False:
            mkdir(anarede.dirsmoothsys)


def sxlffolder(
    anarede,
    loadstd,
    geolstd,
):
    """criacao de diretorio para armazenar dados de simulacao estocastica

    Args
        anarede:
        loadstd:
        geolstd:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        mkdir(anarede.exlffolder)

    if geolstd > 0 and loadstd > 0:
        anarede.sxlffolder = (
            anarede.exlffolder
            + "EXLF_"
            + anarede.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        anarede.sxlffolder = (
            anarede.exlffolder
            + "EXLF_"
            + anarede.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(anarede.sxlffolder) is False:
        mkdir(anarede.sxlffolder)


def sxicfolder(
    anarede,
    loadstd,
    geolstd,
):
    """criacao de diretorio para armazenar dados de simulacao estocastica

    Args
        anarede:
        loadstd:
        geolstd:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretorio de simulacao estocastica nao encontrado\033[0m"
        )

    anarede.exicfolder = dirname(anarede.dirPWF) + "\\EXIC\\"
    if exists(anarede.exicfolder) is False:
        mkdir(anarede.exicfolder)

    if geolstd > 0 and loadstd > 0:
        anarede.sxic = (
            anarede.exicfolder
            + "\\EXIC_"
            + anarede.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        anarede.sxic = (
            anarede.exicfolder
            + "\\EXIC_"
            + anarede.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(anarede.sxic) is False:
        mkdir(anarede.sxic)


def sxctfolder(
    anarede,
    loadstd,
    geolstd,
):
    """criacao de diretorio para armazenar dados de simulacao estocastica

    Args
        anarede:
        loadstd:
        geolstd:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretorio de simulacao estocastica nao encontrado\033[0m"
        )

    anarede.exctfolder = dirname(anarede.dirPWF) + "\\EXCT\\"
    if exists(anarede.exctfolder) is False:
        mkdir(anarede.exctfolder)

    if geolstd > 0 and loadstd > 0:
        anarede.sxct = (
            anarede.exctfolder
            + "\\EXCT_"
            + anarede.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        anarede.sxct = (
            anarede.exctfolder
            + "\\EXCT_"
            + anarede.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(anarede.sxct) is False:
        mkdir(anarede.sxct)


def spvctfolder(
    anarede,
    loadstd,
    geolstd,
):
    """criacao de diretorio para armazenar dados de simulacao estocastica

    Args
        anarede:
        loadstd:
        geolstd:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretorio de simulacao estocastica nao encontrado\033[0m"
        )

    anarede.pvctfolder = dirname(anarede.dirPWF) + "\\PVCT\\"
    if exists(anarede.pvctfolder) is False:
        mkdir(anarede.pvctfolder)

    if geolstd > 0:
        anarede.spvct = (
            anarede.pvctfolder
            + "\\PVCT_"
            + anarede.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    else:
        anarede.spvct = (
            anarede.pvctfolder
            + "\\PVCT_"
            + anarede.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(anarede.spvct) is False:
        mkdir(anarede.spvct)


def statevarfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados finais de convergencia das variaveis de estado

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    anarede.statevarfolder = anarede.resultsfolder + "VariaveisEstado\\"
    if exists(anarede.statevarfolder) is False:
        mkdir(anarede.statevarfolder)

    anarede.statevarfolder = anarede.statevarfolder + anarede.name + "\\"
    if exists(anarede.statevarfolder) is False:
        mkdir(anarede.statevarfolder)


def vsmfolder(
    anarede,
):
    """criacao de diretorio para armazenar resultados de analise de sensibilidade de tensao

    Args
        anarede:
    """
<<<<<<< HEAD
    ## Inicializacao
=======
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a
    exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretorio de simulacao estocastica nao encontrado\033[0m"
        )

    exicfolder = dirname(anarede.dirPWF) + "\\EXIC"
    if exists(exicfolder) is False:
        mkdir(exicfolder)

    anarede.vsmfolder = exicfolder + "\\VSM"
    if exists(anarede.vsmfolder) is False:
        mkdir(anarede.vsmfolder)
