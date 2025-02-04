# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists
from os import mkdir


def folder(
    powerflow,
):
    """inicialização

    Args
        powerflow:
    """
    ## Inicialização
    # Diretório de Sistemas
    dirSistemas = dirname(powerflow.dirPWF)

    # Criação de diretório Resultados
    powerflow.resultsfolder = dirname(dirSistemas) + "\\resultados\\"
    if exists(powerflow.resultsfolder) is False:
        mkdir(powerflow.resultsfolder)


def areasfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de análise de área

    Args
        powerflow:
        name: nome do diretório
    """
    ## Inicialização
    powerflow.infofolder = powerflow.resultsfolder + "iNFO\\"
    if exists(powerflow.infofolder) is False:
        mkdir(powerflow.infofolder)


def admittancefolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de matriz admitância

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.admittancefolder = powerflow.resultsfolder + "MatrizAdmitancia\\"
    if exists(powerflow.admittancefolder) is False:
        mkdir(powerflow.admittancefolder)

    powerflow.admittancefolder = powerflow.admittancefolder + powerflow.name + "\\"
    if exists(powerflow.admittancefolder) is False:
        mkdir(powerflow.admittancefolder)


def convergencefolder(
    powerflow,
):
    """criação de diretório para armazenar resultados da trajetória de convergência

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.convergencefolder = powerflow.resultsfolder + "TrajetoriaConvergencia\\"
    if exists(powerflow.convergencefolder) is False:
        mkdir(powerflow.convergencefolder)

    powerflow.convergencefolder = powerflow.convergencefolder + powerflow.name + "\\"
    if exists(powerflow.convergencefolder) is False:
        mkdir(powerflow.convergencefolder)


def continuationfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de fluxo de potência continuado

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.continuationfolder = powerflow.resultsfolder + "Continuado\\"
    if exists(powerflow.continuationfolder) is False:
        mkdir(powerflow.continuationfolder)

    powerflow.systemcontinuationfolder = (
        powerflow.continuationfolder + powerflow.name + "\\"
    )
    if exists(powerflow.systemcontinuationfolder) is False:
        mkdir(powerflow.systemcontinuationfolder)

    powerflow.systemcontinuationfolderimag = (
        powerflow.systemcontinuationfolder + "imagens\\"
    )
    if exists(powerflow.systemcontinuationfolderimag) is False:
        mkdir(powerflow.systemcontinuationfolderimag)

    powerflow.systemcontinuationfoldertxt = powerflow.systemcontinuationfolder + "txt\\"
    if exists(powerflow.systemcontinuationfoldertxt) is False:
        mkdir(powerflow.systemcontinuationfoldertxt)


def jacobifolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de matriz jacobiana

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.jacobifolder = powerflow.resultsfolder + "MatrizJacobiana\\"
    if exists(powerflow.jacobifolder) is False:
        mkdir(powerflow.jacobifolder)

    powerflow.jacobifolder = powerflow.jacobifolder + powerflow.name + "\\"
    if exists(powerflow.jacobifolder) is False:
        mkdir(powerflow.jacobifolder)


def pssefolder(
    powerflow,
):
    """criação de diretório para armazenar resultados no formato do PSSe

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.pssefolder = dirname(powerflow.dirPWF) + "\\PSSe\\"
    if exists(powerflow.pssefolder) is False:
        mkdir(powerflow.pssefolder)


def reportsfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de relatórios

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.reportsfolder = powerflow.resultsfolder + "Relatorios\\"
    if exists(powerflow.reportsfolder) is False:
        mkdir(powerflow.reportsfolder)

    powerflow.reportsfolder = powerflow.reportsfolder + powerflow.name + "\\"
    if exists(powerflow.reportsfolder) is False:
        mkdir(powerflow.reportsfolder)


def rintfolder(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        mkdir(powerflow.exlffolder)

    powerflow.rintfolder = dirname(powerflow.dirPWF) + "\\RINT\\"
    if exists(powerflow.rintfolder) is False:
        mkdir(powerflow.rintfolder)


def rtotfolder(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        mkdir(powerflow.exlffolder)

    powerflow.rtotfolder = dirname(powerflow.dirPWF) + "\\RTOT\\"
    if exists(powerflow.rtotfolder) is False:
        mkdir(powerflow.rtotfolder)


def smoothfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados suaves

    Args
        powerflow:
    """
    ## Inicialização
    # Condição de método
    if powerflow.sim == "EXLF":
        powerflow.dirsmooth = powerflow.resultsfolder + "Smooth\\"
        if exists(powerflow.dirsmooth) is False:
            mkdir(powerflow.dirsmooth)

        powerflow.dirsmoothsys = powerflow.dirsmooth + powerflow.name + "\\"
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)

    elif powerflow.sim == "EXIC":
        powerflow.dirsmoothsys = powerflow.systemcontinuationfolder + "smooth\\"
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)


def sxlffolder(
    powerflow,
    loadstd,
    geolstd,
):
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        powerflow:
        loadstd:
        geolstd:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        mkdir(powerflow.exlffolder)

    if geolstd > 0 and loadstd > 0:
        powerflow.sxlffolder = (
            powerflow.exlffolder
            + "EXLF_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        powerflow.sxlffolder = (
            powerflow.exlffolder
            + "EXLF_"
            + powerflow.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(powerflow.sxlffolder) is False:
        mkdir(powerflow.sxlffolder)


def sxicfolder(
    powerflow,
    loadstd,
    geolstd,
):
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        powerflow:
        loadstd:
        geolstd:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
        )

    powerflow.exicfolder = dirname(powerflow.dirPWF) + "\\EXIC\\"
    if exists(powerflow.exicfolder) is False:
        mkdir(powerflow.exicfolder)

    if geolstd > 0 and loadstd > 0:
        powerflow.sxic = (
            powerflow.exicfolder
            + "\\EXIC_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        powerflow.sxic = (
            powerflow.exicfolder
            + "\\EXIC_"
            + powerflow.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(powerflow.sxic) is False:
        mkdir(powerflow.sxic)


def sxctfolder(
    powerflow,
    loadstd,
    geolstd,
):
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        powerflow:
        loadstd:
        geolstd:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
        )

    powerflow.exctfolder = dirname(powerflow.dirPWF) + "\\EXCT\\"
    if exists(powerflow.exctfolder) is False:
        mkdir(powerflow.exctfolder)

    if geolstd > 0 and loadstd > 0:
        powerflow.sxct = (
            powerflow.exctfolder
            + "\\EXCT_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    elif loadstd > 0:
        powerflow.sxct = (
            powerflow.exctfolder
            + "\\EXCT_"
            + powerflow.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(powerflow.sxct) is False:
        mkdir(powerflow.sxct)


def spvctfolder(
    powerflow,
    loadstd,
    geolstd,
):
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        powerflow:
        loadstd:
        geolstd:
    """
    ## Inicialização
    powerflow.exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(powerflow.exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
        )

    powerflow.pvctfolder = dirname(powerflow.dirPWF) + "\\PVCT\\"
    if exists(powerflow.pvctfolder) is False:
        mkdir(powerflow.pvctfolder)

    if geolstd > 0:
        powerflow.spvct = (
            powerflow.pvctfolder
            + "\\PVCT_"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    else:
        powerflow.spvct = (
            powerflow.pvctfolder
            + "\\PVCT_"
            + powerflow.name
            + "_loadstd{}".format(
                loadstd,
            )
        )
    if exists(powerflow.spvct) is False:
        mkdir(powerflow.spvct)


def statevarfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados finais de convergência das variáveis de estado

    Args
        powerflow:
    """
    ## Inicialização
    powerflow.statevarfolder = powerflow.resultsfolder + "VariaveisEstado\\"
    if exists(powerflow.statevarfolder) is False:
        mkdir(powerflow.statevarfolder)

    powerflow.statevarfolder = powerflow.statevarfolder + powerflow.name + "\\"
    if exists(powerflow.statevarfolder) is False:
        mkdir(powerflow.statevarfolder)


def vsmfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados de análise de sensibilidade de tensão

    Args
        powerflow:
    """
    ## Inicialização
    exlffolder = dirname(powerflow.dirPWF) + "\\EXLF\\"
    if exists(exlffolder) is False:
        raise ValueError(
            f"\033[91mERROR: Diretório de simulação estocástica não encontrado\033[0m"
        )

    exicfolder = dirname(powerflow.dirPWF) + "\\EXIC"
    if exists(exicfolder) is False:
        mkdir(exicfolder)

    powerflow.vsmfolder = exicfolder + "\\VSM"
    if exists(powerflow.vsmfolder) is False:
        mkdir(powerflow.vsmfolder)
