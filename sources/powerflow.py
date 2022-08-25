# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from setup import Setup

class PowerFlow:
    """classe da rotina principal"""

    def __init__(
        self,
        system: str='',
        method: str='NEWTON',
        jacobi: str='COMPLETA',
        options: dict=None,
        control: str='',
        mon: str='',
        rel: str='',
    ):
        """inicialização

        Parâmetros:
            arqv: str, opcional, valor padrão ''
            method: str, opcional, valor padrão 'NEWTON'
            jacobi: str, opcional, valor padrão 'COMPLETA'
            options: dict, opcional, valor padrão None
            control: str, opcional, valor padrão ''
            mon: str, opcional, valor padrão ''
            rel: str, opcional, valor padrão ''   
        """

        ## Inicialização
        # Variáveis
        self.system = system    # SEP em estudo
        self.method = method    # Método de solução do fluxo de potência
        self.jacobi = jacobi    # Formulação da matriz Jacobiana
        self.options = options  # Opções de convergência
        self.control = control  # Opções de controle
        self.mon = mon          # Opções de monitoramento
        self.rel = rel          # Opções de relatório


        # Classe para configuração inicial do SEP em estudo
        Setup(self)