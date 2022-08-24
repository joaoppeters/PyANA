# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from admittance import Ybus
from folder import Folder
from jacobian import Jac
from pwf import PWF
from report import Report


class Setup:
    """configuração inicial da rotina"""

    def __init__(
        self,
        arqv: str='',
    ):

        if arqv:
            ## Inicialização
            # Classe para criação automática de folders
            Folder.__init__(arqv)

            # Classe para leitura de arquivo .pwf
            PWF.__init__(arqv)

        
        else:
            ## ERROR
            raise ValueError ('Nenhum arquivo foi repassado')
