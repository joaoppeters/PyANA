# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, exists
from simulation import *
from setting import pwfsetting, stbsetting
from transcript import orwudc, orwdyn, prwraw, prwdyr

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
                sys_type = system[-3:].casefold()

                if sys_type == "pwf":
                    pwfsetting(self.anarede)
                    exlf(self.anarede) if method == "EXLF" else None
                    exic(self.anarede) if method == "EXIC" else None
                    expc(self.anarede) if method == "EXPC" else None
                    if method == "EXSI":
                        stbsetting(self.anarede, self.anatem)
                        exsi(self.anarede)
                    elif method == "PSSEt":
                        self.psse = PowerFlowContainer()
                        prwraw(self.anarede, self.psse)
                    else:
                        raise ValueError(f"Unknown method: {method}")

                elif sys_type == "stb":
                    pwfsetting(self.anarede)
                    stbsetting(self.anarede, self.anatem)
                    if method == "ORGAt":
                        self.organon = PowerFlowContainer()
                        self.organon.system = system
                        self.organon.method = method
                        anatemfiles, organonfiles = orwudc(self.anarede, self.anatem, self.organon)
                        orwdyn(self.anarede, self.anatem, self.organon, anatemfiles, organonfiles)
                    elif method == "PSSEt":
                        self.psse = PowerFlowContainer()
                        prwraw(self.anarede, self.psse)
                        prwdyr(self.anarede, self.anatem, self.psse)
                    elif method != "EXSI":
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
