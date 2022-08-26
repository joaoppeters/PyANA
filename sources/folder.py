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
            powerflow: self do arquivo powerflow.py
        """
        
        if setup.arqv:
            # Diretório de Sistemas
            self.dirSistemas = dirname(self.arqv)



    def rpf(
        self,
    ):
        # Criação de diretório para armazenar Resultados
        self.dirResultados = dirname(self.dirSistemas) + '/Resultados/'
        if exists(self.dirResultados) is False:
            mkdir(self.dirResultados)

        # Criação de diretório para armazenar Resultados de Matriz Admitância
        dirRAdmitancia = self.dirResultados + 'MatrizAdmitancia/'
        if exists(dirRAdmitancia) is False:
            mkdir(dirRAdmitancia)

        # Criação de diretório para armazenar Resultados de Matriz Jacobiana
        dirRJacobiana = self.dirResultados + 'MatrizJacobiana/'
        if exists(dirRJacobiana) is False:
            mkdir(dirRJacobiana)

        # Criação de diretório para armazenar Resultados de Relatórios
        dirRRelatorios = self.dirResultados + 'Relatorios/'
        if exists(dirRRelatorios) is False:
            mkdir(dirRRelatorios)


    def rcpf(
        self,
        arqv: str='',
    ):
        """criação automática de folder para armazenar resultados específicos do fluxo de potência continuado

        Parâmetros:
            arqv: str, obrigatório, valor padrão ''
                Diretório onde está localizado arquivo .pwf contendo os dados do sistema elétrico em estudo
        """
        if arqv:

            # Criação de diretório para armazenar Resultados de Fluxo de Potência Continuado
            dirRCPF = self.dirResultados + 'Continuado/'
            if exists(dirRCPF) is False:
                mkdir(dirRCPF)
