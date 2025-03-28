# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import folder
from simulation import simulation
from setting import setting


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

        Args:
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

        if self.system:
            # Data setting
            setting(
                self,
            )

            # Armazenamento dos resultados
            folder(
                self,
            )

            # Numerical Method
            simulation(
                self,
            )

        else:
            ## ERROR - VERMELHO
            raise ValueError("\033[91mNenhum sistema foi selecionado.\033[0m")
