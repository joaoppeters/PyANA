# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

<<<<<<< HEAD
system = "SISTEMA_REDUZIDO_NE_232B_B1.stb"
system = "nordicoA-SVC.PWF"
=======
system = "SISTEMA_REDUZIDO_NE_232B_CASO_A0.stb"
# system = "1Q2026.PWF"
# system = "730.PWF"
# system = "2030-C6-MAY.pwf"
# system = "30AXD-C5b-t0.PWF"
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a

method = "EXLF"  # NEWTON-RAPHSON
# method =  "EXIC"  # CONTINUATION POWER FLOW
# method =  "EXPC"  # POINT OF COLLAPSE
# method = "EXSI"  # DYNAMIC SIMULATION
# method = "EXCT"  # CONTINGENCY ANALYSIS
# method = "ORGAt"  # ORGANON DATA TRANSCRIPTION
<<<<<<< HEAD
# method = "PSSEt"  # PSSE DATA TRANSCRIPTION
# method = "MATPt"  # MATPOWER DATA TRANSCRIPTION
=======
method = "PSSEt"  # PSSE DATA TRANSCRIPTION
# method = "SLEEP"  # SLEEP MODE
>>>>>>> f7a4f3cc9f2adfd6e5ead37f79750b46d7aab35a

PowerFlow(
    system=system,
    method=method,
)
