# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import dirname, exists
from os import mkdir

class Folder:
    """criação automática de diretórios para armazenar resultados"""

    def __init__(
        self,
        arqv: str='',
    ):
        """ inicialização

        Parâmetros:
            arqv: str, obrigatório
                Diretório onde está localizado arquivo .pwf contendo os dados do sistema elétrico em estudo
        """
        
        if arqv:
            # Diretório de Sistemas
            dirSistemas = dirname(arqv)

            # Criação de diretório para armazenar Resultados
            dirResultados = dirSistemas + '/Resultados/'
            if exists(dirResultados) is False:
                mkdir(dirResultados)

            # Criação de diretório para armazenar Resultados de Fluxo de Potência Continuado
            dirRCPF = dirResultados + 'Continuado'
            if exists(dirRCPF) is False:
                mkdir(dirRCPF)

            # Criação de diretório para armazenar Resultados de Matriz Admitância
            dirRAdmitancia = dirResultados + 'MatrizAdmitancia/'
            if exists(dirRAdmitancia) is False:
                mkdir(dirRAdmitancia)

            # Criação de diretório para armazenar Resultados de Matriz Jacobiana
            dirRJacobiana = dirResultados + 'MatrizJacobiana/'
            if exists(dirRJacobiana) is False:
                mkdir(dirRJacobiana)

            # Criação de diretório para armazenar Resultados de Relatórios
            dirRRelatorios = dirResultados + 'Relatorios/'
            if exists(dirRRelatorios) is False:
                mkdir(dirRRelatorios)
