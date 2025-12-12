# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "SISTEMA_REDUZIDO_NE_232B_CASO_A0.stb"

method = "EXLF"  # NEWTON-RAPHSON
# method =  "EXIC"  # CONTINUATION POWER FLOW
# method =  "EXPC"  # POINT OF COLLAPSE
method = "EXSI"  # DYNAMIC SIMULATION
# method = "ORGA"  # ORGANON

# control = [
#     # "CREM",
#     # "CTAP",
#     # "CTAPd",
#     # "FREQ",
#     # "QLIM",
#     # "QLIMs",
#     # "SVCs",
# ]

# report = [
#     "RBAR",
#     # "RLIN",
#     # "RGER",
#     # "RCER",
# ]

PowerFlow(
    system=system,
    method=method,
)
