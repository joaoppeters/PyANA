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
    """inicialização

    Args
        anarede:
    """
    ## Inicialização
    # Diretório de Sistemas
    dirSistemas = dirname(anarede.dirPWF)

    # Criação de diretório Resultados
    anarede.resultsfolder = dirname(dirSistemas) + "\\resultados\\"
    if exists(anarede.resultsfolder) is False:
        mkdir(anarede.resultsfolder)


def areasfolder(
    anarede,
):
    """criação de diretório para armazenar resultados de análise de área

    Args
        anarede:
        name: nome do diretório
    """
    ## Inicialização
    anarede.infofolder = anarede.resultsfolder + "iNFO\\"
    if exists(anarede.infofolder) is False:
        mkdir(anarede.infofolder)


def admittancefolder(
    anarede,
):
    """criação de diretório para armazenar resultados de matriz admitância

    Args
        anarede:
    """
    ## Inicialização
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
    ## Inicialização
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
    ## Inicialização
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
    ## Inicialização
    bxicfolder(
        anarede,
    )

    anarede.exctfolder = dirname(anarede.dirPWF) + "\\EXCT\\"
    if exists(anarede.exctfolder) is False:
        mkdir(anarede.exctfolder)

    anarede.bxctfolder = anarede.exctfolder + "BASE\\"
    if exists(anarede.bxctfolder) is False:
        mkdir(anarede.bxctfolder)


def cdufolder(
    anarede,
):
    """criação de diretório para armazenar arquivos CDU

    Args
        none
    """
    ## Inicialização
    cdufolder = dirname(dirname(__file__)) + "\\sistemas\\cdu2udc\\"
    if not exists(cdufolder):
        mkdir(cdufolder)
    return cdufolder


def convergencefolder(
    anarede,
):
    """criação de diretório para armazenar resultados da trajetória de convergência

    Args
        anarede:
    """
    ## Inicialização
    anarede.convergencefolder = anarede.resultsfolder + "TrajetoriaConvergencia\\"
    if exists(anarede.convergencefolder) is False:
        mkdir(anarede.convergencefolder)

    anarede.convergencefolder = anarede.convergencefolder + anarede.name + "\\"
    if exists(anarede.convergencefolder) is False:
        mkdir(anarede.convergencefolder)


def continuationfolder(
    anarede,
):
    """criação de diretório para armazenar resultados de fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
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
    """criação de diretório para armazenar resultados de matriz jacobiana

    Args
        anarede:
    """
    ## Inicialização
    anarede.jacobifolder = anarede.resultsfolder + "MatrizJacobiana\\"
    if exists(anarede.jacobifolder) is False:
        mkdir(anarede.jacobifolder)

    anarede.jacobifolder = anarede.jacobifolder + anarede.name + "\\"
    if exists(anarede.jacobifolder) is False:
        mkdir(anarede.jacobifolder)


def logfolder(
    logfolder,
):
    """criação de diretório para armazenar arquivos de log

    Args
        directory:
    """
    ## Inicialização
    if exists(logfolder) is False:
        mkdir(logfolder)
    return logfolder


def outfolder(
    outfolder,
):
    """criação de diretório para armazenar arquivos de saída

    Args
        directory:
    """
    ## Inicialização
    if exists(outfolder) is False:
        mkdir(outfolder)
    return outfolder


def pltfolder(
    pltfolder,
):
    """criação de diretório para armazenar arquivos de plotagem

    Args
        directory:
    """
    ## Inicialização
    if exists(pltfolder) is False:
        mkdir(pltfolder)
    return pltfolder


def pssefolder(
    anarede,
):
    """criação de diretório para armazenar resultados no formato do PSSe

    Args
        anarede:
    """
    ## Inicialização
    anarede.pssefolder = dirname(anarede.dirPWF) + "\\PSSe\\"
    if exists(anarede.pssefolder) is False:
        mkdir(anarede.pssefolder)


def reportsfolder(
    anarede,
):
    """criação de diretório para armazenar resultados de relatórios

    Args
        anarede:
    """
    ## Inicialização
    anarede.reportsfolder = anarede.resultsfolder + "Relatorios\\"
    if exists(anarede.reportsfolder) is False:
        mkdir(anarede.reportsfolder)

    anarede.reportsfolder = anarede.reportsfolder + anarede.name + "\\"
    if exists(anarede.reportsfolder) is False:
        mkdir(anarede.reportsfolder)


def rbarfolder(
    anarede,
):
    """criação de diretório para armazenar resultados de análise de barra

    Args
        anarede:
    """
    ## Inicialização
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
    ## Inicialização
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
    """criação de diretório para armazenar resultados de análise de linha

    Args
        anarede:
    """
    ## Inicialização
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
    ## Inicialização
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
    """criação de diretório para armazenar resultados de SAGE

    Args
        anarede:
        pwffile:
    """
    ## Inicialização
    sagefolder = dirname(anarede.dirPWF) + "\\SAGE\\"
    if exists(sagefolder) is False:
        mkdir(sagefolder)

    anarede.sagefolder = sagefolder + pwffile.removesuffix(".PWF") + "\\"
    if exists(anarede.sagefolder) is False:
        mkdir(anarede.sagefolder)


def smoothfolder(
    anarede,
):
    """criação de diretório para armazenar resultados suaves

    Args
        anarede:
    """
    ## Inicialização
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
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        anarede:
        loadstd:
        geolstd:
    """
    ## Inicialização
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
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        anarede:
        loadstd:
        geolstd:
    """
    ## Inicialização
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
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
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        anarede:
        loadstd:
        geolstd:
    """
    ## Inicialização
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
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
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        anarede:
        loadstd:
        geolstd:
    """
    ## Inicialização
    anarede.exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(anarede.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
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
    """criação de diretório para armazenar resultados finais de convergência das variáveis de estado

    Args
        anarede:
    """
    ## Inicialização
    anarede.statevarfolder = anarede.resultsfolder + "VariaveisEstado\\"
    if exists(anarede.statevarfolder) is False:
        mkdir(anarede.statevarfolder)

    anarede.statevarfolder = anarede.statevarfolder + anarede.name + "\\"
    if exists(anarede.statevarfolder) is False:
        mkdir(anarede.statevarfolder)


def vsmfolder(
    anarede,
):
    """criação de diretório para armazenar resultados de análise de sensibilidade de tensão

    Args
        anarede:
    """
    ## Inicialização
    exlffolder = dirname(anarede.dirPWF) + "\\EXLF\\"
    if exists(exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
        )

    exicfolder = dirname(anarede.dirPWF) + "\\EXIC"
    if exists(exicfolder) is False:
        mkdir(exicfolder)

    anarede.vsmfolder = exicfolder + "\\VSM"
    if exists(anarede.vsmfolder) is False:
        mkdir(anarede.vsmfolder)
