# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "SISTEMA_REDUZIDO_NE_232B_B1.stb"
system = "1Q2026.PWF"
system = "730.PWF"

method = "EXLF"  # NEWTON-RAPHSON
# method =  "EXIC"  # CONTINUATION POWER FLOW
# method =  "EXPC"  # POINT OF COLLAPSE
# method = "EXSI"  # DYNAMIC SIMULATION
# method = "EXCT"  # CONTINGENCY ANALYSIS
# method = "ORGAt"  # ORGANON DATA TRANSCRIPTION
# method = "PSSEt"  # PSSE DATA TRANSCRIPTION

PowerFlow(
    system=system,
    method=method,
)
