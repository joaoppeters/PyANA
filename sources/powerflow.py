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
        sim: str = "EXLF",
        control: list = list(),
        monitor: list = list(),
        report: list = list(),
    ):
        """initialization

        Args:
            system: str, optional, default ''
            sim: str, optional, default 'EXLF'
            control: list, optional, default None
            monitor: list, optional, default None
            report: list, optional, default None
        """

        ## Inicialization
        # Variables
        self.system = system
        self.sim = sim
        self.control = control
        self.monitor = monitor
        self.report = report

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
