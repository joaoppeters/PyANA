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
    '''inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Diretório de Sistemas
    dirSistemas = dirname(powerflow.dirSEP)

    # Criação de diretório Resultados
    powerflow.dirResultados = dirname(dirSistemas) + '/resultados/'
    if exists(powerflow.dirResultados) is False:
        mkdir(powerflow.dirResultados)

def admittancefolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados de matriz admitância

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRadmittance = powerflow.dirResultados + 'MatrizAdmitancia/'
    if exists(powerflow.dirRadmittance) is False:
        mkdir(powerflow.dirRadmittance)

    powerflow.dirRadmittance = powerflow.dirRadmittance + powerflow.name + '/'
    if exists(powerflow.dirRadmittance) is False:
        mkdir(powerflow.dirRadmittance)

def convergencefolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados da trajetória de convergência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRconvergence = powerflow.dirResultados + 'TrajetoriaConvergencia/'
    if exists(powerflow.dirRconvergence) is False:
        mkdir(powerflow.dirRconvergence)

    powerflow.dirRconvergence = powerflow.dirRconvergence + powerflow.name + '/'
    if exists(powerflow.dirRconvergence) is False:
        mkdir(powerflow.dirRconvergence)

def continuationfolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados de fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRcpf = powerflow.dirResultados + 'Continuado/'
    if exists(powerflow.dirRcpf) is False:
        mkdir(powerflow.dirRcpf)
        
    powerflow.dircpfsys = powerflow.dirRcpf + powerflow.name + '/'
    if exists(powerflow.dircpfsys) is False:
        mkdir(powerflow.dircpfsys)

    powerflow.dircpfsysimag = powerflow.dircpfsys + 'imagens/'
    if exists(powerflow.dircpfsysimag) is False:
        mkdir(powerflow.dircpfsysimag)

    powerflow.dircpfsystxt = powerflow.dircpfsys + 'txt/'
    if exists(powerflow.dircpfsystxt) is False:
        mkdir(powerflow.dircpfsystxt)

def jacobifolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados de matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRjacobi = powerflow.dirResultados + 'MatrizJacobiana/'
    if exists(powerflow.dirRjacobi) is False:
        mkdir(powerflow.dirRjacobi)

    powerflow.dirRjacobi = powerflow.dirRjacobi + powerflow.name + '/'
    if exists(powerflow.dirRjacobi) is False:
        mkdir(powerflow.dirRjacobi)

def reportsfolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados de relatórios

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRreports = powerflow.dirResultados + 'Relatorios/'
    if exists(powerflow.dirRreports) is False:
        mkdir(powerflow.dirRreports)

    powerflow.dirRreports = powerflow.dirRreports + powerflow.name + '/'
    if exists(powerflow.dirRreports) is False:
        mkdir(powerflow.dirRreports)

def smoothfolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados suaves

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Condição de método
    if powerflow.method == 'NEWTON':
        powerflow.dirsmooth = powerflow.dirResultados + 'Smooth/'
        if exists(powerflow.dirsmooth) is False:
            mkdir(powerflow.dirsmooth)

        powerflow.dirsmoothsys = powerflow.dirsmooth + powerflow.name + '/'
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)

    elif powerflow.method == 'CPF':
        powerflow.dirsmoothsys = powerflow.dircpfsys + 'smooth/'
        if exists(powerflow.dirsmoothsys) is False:
            mkdir(powerflow.dirsmoothsys)

def statevarfolder(
    powerflow,
):
    '''criação de diretório para armazenar resultados finais de convergência das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dirRstatevar = powerflow.dirResultados + 'VariaveisEstado/'
    if exists(powerflow.dirRstatevar) is False:
        mkdir(powerflow.dirRstatevar)

    powerflow.dirRstatevar = powerflow.dirRstatevar + powerflow.name + '/'
    if exists(powerflow.dirRstatevar) is False:
        mkdir(powerflow.dirRstatevar)
