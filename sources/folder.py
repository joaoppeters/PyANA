# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists
from os import mkdir


class Folder:
    """classe para criação automática de diretórios para armazenar resultados"""

    def __init__(
        self,
        setup,
    ):
        """inicialização

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        # Diretório de Sistemas
        dirSistemas = dirname(setup.dirSEP)

        # Criação de diretório Resultados
        setup.dirResultados = dirname(dirSistemas) + "/resultados/"
        if exists(setup.dirResultados) is False:
            mkdir(setup.dirResultados)

    def admittance(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados de matriz admitância

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRadmittance = setup.dirResultados + "MatrizAdmitancia/"
        if exists(setup.dirRadmittance) is False:
            mkdir(setup.dirRadmittance)

        setup.dirRadmittance = setup.dirRadmittance + setup.name + "/"
        if exists(setup.dirRadmittance) is False:
            mkdir(setup.dirRadmittance)

    def convergence(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados da trajetória de convergência

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRconvergence = setup.dirResultados + "TrajetoriaConvergencia/"
        if exists(setup.dirRconvergence) is False:
            mkdir(setup.dirRconvergence)

        setup.dirRconvergence = setup.dirRconvergence + setup.name + "/"
        if exists(setup.dirRconvergence) is False:
            mkdir(setup.dirRconvergence)

    def continuation(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados de fluxo de potência continuado

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRcpf = setup.dirResultados + "Continuado/"
        if exists(setup.dirRcpf) is False:
            mkdir(setup.dirRcpf)

        self.continuationsystem(
            setup,
        )

    def continuationsystem(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados de fluxo de potência continuado (arquivos e imagens)
        específico para cada sistema analisado

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dircpfsys = setup.dirRcpf + setup.name + "/"
        if exists(setup.dircpfsys) is False:
            mkdir(setup.dircpfsys)

        setup.dircpfsysimag = setup.dircpfsys + "imagens/"
        if exists(setup.dircpfsysimag) is False:
            mkdir(setup.dircpfsysimag)

        setup.dircpfsystxt = setup.dircpfsys + "txt/"
        if exists(setup.dircpfsystxt) is False:
            mkdir(setup.dircpfsystxt)

    def jacobi(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados de matriz jacobiana

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRjacobi = setup.dirResultados + "MatrizJacobiana/"
        if exists(setup.dirRjacobi) is False:
            mkdir(setup.dirRjacobi)

        setup.dirRjacobi = setup.dirRjacobi + setup.name + "/"
        if exists(setup.dirRjacobi) is False:
            mkdir(setup.dirRjacobi)

    def reports(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados de relatórios

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRreports = setup.dirResultados + "Relatorios/"
        if exists(setup.dirRreports) is False:
            mkdir(setup.dirRreports)

        setup.dirRreports = setup.dirRreports + setup.name + "/"
        if exists(setup.dirRreports) is False:
            mkdir(setup.dirRreports)

    def smooth(
        self,
        powerflow,
        setup,
    ):
        """criação de diretório para armazenar resultados suaves

        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        # Condição de método
        if powerflow.method == "NEWTON":
            setup.dirsmooth = setup.dirResultados + "Smooth/"
            if exists(setup.dirsmooth) is False:
                mkdir(setup.dirsmooth)

            setup.dirsmoothsys = setup.dirsmooth + setup.name + "/"
            if exists(setup.dirsmoothsys) is False:
                mkdir(setup.dirsmoothsys)

        elif powerflow.method == "CPF":
            setup.dirsmoothsys = setup.dircpfsys + "smooth/"
            if exists(setup.dirsmoothsys) is False:
                mkdir(setup.dirsmoothsys)

    def statevar(
        self,
        setup,
    ):
        """criação de diretório para armazenar resultados finais de convergência das variáveis de estado

        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        setup.dirRstatevar = setup.dirResultados + "VariaveisEstado/"
        if exists(setup.dirRstatevar) is False:
            mkdir(setup.dirRstatevar)

        setup.dirRstatevar = setup.dirRstatevar + setup.name + "/"
        if exists(setup.dirRstatevar) is False:
            mkdir(setup.dirRstatevar)
