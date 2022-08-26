# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import dirname, exists, realpath
from os import mkdir

from admittance import Ybus
from control import Control
from folder import Folder
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
            # Verificação de diretório
            self.checkpath(powerflow,)

            # Classe para leitura de arquivo .pwf
            PWF(powerflow, self,)

            # Classe para determinação dos valores padrão das variáveis de tolerância
            Options(powerflow,)

            # Classe para determinar a realização das opções de controle escolhidas
            Control(powerflow,)

            # Classe para determinar a realização de monitoramento de valores
            Monitor(powerflow,)

            # # Classe para criação automática de diretórios para armazenar resultados  ------------ COLOCAR SOMENTE AO FINAL DA CHAMADA DO FLUXO DE POTENCIA
            # Folder(powerflow, self,)

            # Classe para construção da matriz Admitância
            Ybus(powerflow, self,)
        
        else:
            ## ERROR - VERMELHO
            raise ValueError('\033[91mNenhum sistema foi selecionado.\033[0m')



    def checkpath(
        self,
        powerflow,
        ):
        """verificação automática de diretório sistemas
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        ## Inicialização
        self.maindir = dirname(dirname(__file__))
        self.name = powerflow.system.split('.')[0]

        if exists(self.maindir + '/sistemas/') is True:
            if exists(self.maindir + '/sistemas/' + powerflow.system) is True:
                self.dirSEP = realpath(dirname(dirname(__file__)) + '/sistemas/' + powerflow.system)
                print(f'\033[93mArquivo `{powerflow.system}` contendo dados do SEP encontrado dentro de pasta `PowerFlow/sistemas/` conforme solicitado!\033[0m')
            else:
                raise ValueError(f'\033[91mERROR: Pasta `PowerFlow/sistemas/` não contém o arquivo `{powerflow.system}` do SEP informado.\nInsira o arquivo `{powerflow.system}` que contém os dados do SEP que gostaria de analisar na pasta e rode novemente!\033[0m')

        else:
            mkdir(self.maindir + '/sistemas/')
            raise ValueError(f'\033[91mERROR: Pasta `PowerFlow/sistemas/` acabou de ser criada.\nLembre-se de inserir o arquivo `{powerflow.system}` que contém os dados do SEP que gostaria de analisar na pasta e rode novamente!\033[0m')
