# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from setup import Setup

class PowerFlow:
    """rotina principal"""

    def __init__(
        self,
        arqv: str='',
        method: str='NEWTON',
        jacobi: str='COMPLETA',
        options: dict=None,
        control: str=None,
        rel: str='',
    ):
        """inicialização

        Parameters:
            arqv: str, opcional, valor padrão None
            method: str, opcional, valor padrão 'NEWTON'
            jacobi: str, opcional, valor padrão 'COMPLETA'
            options: dict, opcional, valor padrão None
            control: str, opcional, valor padrão None
            rel: str, opcional, valor padrão None    
        """

        # Classe para
        Setup.__init__(arqv)