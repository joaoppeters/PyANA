# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import dirname, realpath

from admittance import Ybus
# from folder import Folder
# from jacobian import Jac
from monitor import Monitor
from options import Options
from pwf import PWF
# from report import Report


class Setup:
    """classe para configuração inicial da rotina"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        if powerflow.system:
            ## Inicialização
            self.arqv = realpath(dirname(dirname(__file__)) + '/sistemas/' + powerflow.system)

            # Classe para leitura de arquivo .pwf
            PWF(powerflow, self)

            # Classe para determinação dos valores padrão das variáveis de tolerância
            Options(powerflow)

            # Classe para determinar a realização de monitoramento de valores
            Monitor(powerflow)

            # Classe para construção da matriz Admitância
            Ybus(powerflow)
        
        else:
            ## ERROR - VERMELHO
            raise ValueError('\033[91mNenhum sistema foi selecionado.\033[0m')



    # def sFolder(
    #     self,
    #     ):
    #     """Criação automática de folders para caso"""

    #     # Chamada de classe para criação automática de folders
    #     Folder.__init__(self.arqv)