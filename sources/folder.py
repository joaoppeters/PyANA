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
    # Diretório de Sistemas
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
    # Condição de método
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
