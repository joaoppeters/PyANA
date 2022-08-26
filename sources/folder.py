# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import dirname, exists
from os import mkdir
from options import Options

class Folder:
    """classe para criação automática de diretórios para armazenar resultados"""

    def __init__(
        self,
        setup,
    ):
        """ inicialização

        Parâmetros
            setup: self do arquivo setup.py
        """
        
        # Diretório de Sistemas
        dirSistemas = dirname(setup.dirSEP)

        # Criação de diretório Resultados
        dirResultados = dirname(dirSistemas) + '/resultados/'
        if exists(dirResultados) is False:
            mkdir(dirResultados)
        
        setup.dirResultados = dirResultados


    
    def admittance(
        self,
        setup,
    ):
        """criação de diretório para armazenar Resultados de Matriz Admitância
        
        Parâmetros
            setup: self do arquivo setup.py
        """

        dirRadmittance = setup.dirResultados + 'MatrizAdmitancia/'
        if exists(dirRadmittance) is False:
            mkdir(dirRadmittance)
        
        setup.dirRadmittance = dirRadmittance



    def jacobi(
        self,
        setup,
    ):
        """criação de diretório para armazenar Resultados de Matriz Jacobiana
        
        Parâmetros
            setup: self do arquivo setup.py
        """

        dirRjacobi = setup.dirResultados + 'MatrizJacobiana/'
        if exists(dirRjacobi) is False:
            mkdir(dirRjacobi)
        
        setup.dirRjacobi = dirRjacobi




    def reports(
        self,
        setup,
    ):
        """criação de diretório para armazenar Resultados de Relatórios
        
        Parâmetros
            setup: self do arquivo setup.py
        """

        dirRreports = self.dirResultados + 'Relatorios/'
        if exists(dirRreports) is False:
            mkdir(dirRreports)
        
        setup.dirRreports = dirRreports



    def cpf(
        self,
        setup,
    ):
        """criação de diretório para armazenar Resultados de Fluxo de Potência Continuado
        
        Parâmetros
            setup: self do arquivo setup.py
        """

        dirRcpf = self.dirResultados + 'Continuado/'
        if exists(dirRcpf) is False:
            mkdir(dirRcpf)
        
        setup.dirRcpf = dirRcpf