# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from admittance import Ybus
from method import Method
from setup import Setup

class PowerFlow:
    """classe da rotina principal"""

    def __init__(
        self,
        system: str='',
        method: str='NEWTON',
        options: dict=dict(),
        control: list=list(),
        monitor: list=list(),
        report: list=list(),
    ):
        """inicialização

        Parâmetros:
            system: str, opcional, valor padrão ''
            method: str, opcional, valor padrão 'NEWTON'
            options: dict, opcional, valor padrão None
            control: list, opcional, valor padrão None
            monitor: list, opcional, valor padrão None
            report: list, opcional, valor padrão None 
        """

        ## Inicialização
        # Variáveis chamadas
        self.system = system    # SEP em estudo
        self.method = method    # Método de solução do fluxo de potência
        self.options = options  # Opções de convergência
        self.control = control  # Opções de controle
        self.monitor = monitor  # Opções de monitoramento
        self.report = report    # Opções de relatório

        # Classe para configuração do SEP em estudo
        self.setup = Setup(self)

        # Classe para construção da matriz Admitância
        Ybus(self,)

        # Classe para aplicação do método selecionado para análise de fluxo de potência
        Method(self,)