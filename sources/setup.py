# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import dirname, exists, realpath
from os import mkdir

from ctrl import Control
from monitor import Monitor
from options import Options
from pwf import PWF
from report import Reports

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

        ## Inicialização
        if powerflow.system:
            # Verificação de diretório
            self.checkpath(powerflow,)

            # Classe para leitura de arquivo .pwf
            PWF(powerflow, self,)

            # Classe para determinação dos valores padrão das variáveis de tolerância
            Options(powerflow, self,)

            # Classe para determinar a realização das opções de controle escolhidas
            Control(powerflow, self,)

            # Classe para determinar a realização de monitoramento de valores
            Monitor(powerflow, self,)

            # Classe para determinar a geração de relatórios
            Reports(powerflow, self,)
        
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
        # Variável de diretório principal
        self.maindir = dirname(dirname(__file__))

        # Variável de nome do SEP em estudo
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
