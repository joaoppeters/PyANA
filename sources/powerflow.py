# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import folder
from method import methodo
from setup import setup


class PowerFlow:
    """powerflow class"""

    def __init__(
        self,
        system: str = "",
        method: str = "EXLF",
        control: list = list(),
        monitor: list = list(),
        report: list = list(),
    ):
        """initialization

        Parameters:
            system: str, optional, default ''
            method: str, optional, default 'EXLF'
            control: list, optional, default None
            monitor: list, optional, default None
            report: list, optional, default None
        """

        ## Inicialization
        # Variables
        self.system = system
        self.method = method
        self.control = control
        self.monitor = monitor
        self.report = report

        # Data Setup
        setup(
            self,
        )

        # Armazenamento dos resultados
        folder(
            self,
        )

        # Numerical Method
        methodo(
            self,
        )
