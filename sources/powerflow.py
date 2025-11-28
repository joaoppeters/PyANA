# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import folder
from os.path import dirname, exists
from simulation import *
from setting import pwfsetting, stbsetting


class PowerFlow:
    """powerflow class"""

    def __init__(
        self,
        system: str = "",
        method: str = "EXLF",
    ):
        # ---- create two objects of the SAME PowerFlow class ----
        self.anarede = PowerFlowContainer()
        self.anarede.system = system
        self.anarede.method = method

        self.anatem = PowerFlowContainer()
        self.anatem.system = system
        self.anatem.method = method

        # --- Safe system type detection ---
        if exists(dirname(dirname(__file__)) + "\\sistemas\\") is True:
            if exists(dirname(dirname(__file__)) + "\\sistemas\\" + system) is True:
                parts = system.split(".")
                sys_type = parts[1].casefold() if len(parts) > 1 else ""

                if sys_type == "pwf":
                    pwfsetting(self.anarede)
                    exlf(self.anarede) if method == "EXLF" else None
                    exic(self.anarede) if method == "EXIC" else None
                    expc(self.anarede) if method == "EXPC" else None
                    if method == "EXSI":
                        stbsetting(self.anarede, self.anatem)
                        exsi(self.anarede)
                    else:
                        raise ValueError(f"Unknown method: {method}")

                elif sys_type == "stb":
                    pwfsetting(self.anarede)
                    stbsetting(self.anarede, self.anatem)
                    if method != "EXSI":
                        raise ValueError(f"Unknown method: {method}")
                    exsi(self.anatem)

            else:
                raise ValueError("\033[91mNenhum sistema foi selecionado.\033[0m")
        else:
            raise ValueError("\033[91mA pasta 'sistemas' não foi encontrada.\033[0m")


# Container class inherits the SAME base class, but skips its __init__
class PowerFlowContainer(PowerFlow):
    def __init__(self):
        pass
