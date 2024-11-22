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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
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
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.reportsfolder = powerflow.resultsfolder + "Relatorios\\"
    if exists(powerflow.reportsfolder) is False:
        mkdir(powerflow.reportsfolder)

    powerflow.reportsfolder = powerflow.reportsfolder + powerflow.name + "\\"
    if exists(powerflow.reportsfolder) is False:
        mkdir(powerflow.reportsfolder)


def smoothfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados suaves

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição de método
    if powerflow.method == "EXLF":
        powerflow.dirsmooth = powerflow.resultsfolder + "Smooth\\"
        if exists(powerflow.dirsmooth) is False:
            mkdir(powerflow.dirsmooth)

        powerflow.dirsmoothsys = powerflow.dirsmooth + powerflow.name + "\\"
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)

    elif powerflow.method == "EXIC":
        powerflow.dirsmoothsys = powerflow.systemcontinuationfolder + "smooth\\"
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)


def stochasticfolder(
    powerflow,
    loadstd,
    geolstd,
):
    """criação de diretório para armazenar dados de simulação estocástica

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    if geolstd > 0:
        powerflow.stochasticsystems = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_loadstd{}_geolstd{}".format(
                loadstd,
                geolstd,
            )
        )
    else:
        powerflow.stochasticsystems = (
            powerflow.maindir
            + "\\sistemas\\"
            + powerflow.name
            + "_load std{}".format(
                loadstd,
            )
        )
    if exists(powerflow.stochasticsystems) is False:
        mkdir(powerflow.stochasticsystems)

    with open(powerflow.stochasticsystems + "\\BALANCE.txt", "w") as file:
        file.write("CASO;GERACAO;DEMANDA\n")

    powerflow.filefolder = powerflow.stochasticsystems


def statevarfolder(
    powerflow,
):
    """criação de diretório para armazenar resultados finais de convergência das variáveis de estado

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.statevarfolder = powerflow.resultsfolder + "VariaveisEstado\\"
    if exists(powerflow.statevarfolder) is False:
        mkdir(powerflow.statevarfolder)

    powerflow.statevarfolder = powerflow.statevarfolder + powerflow.name + "\\"
    if exists(powerflow.statevarfolder) is False:
        mkdir(powerflow.statevarfolder)
