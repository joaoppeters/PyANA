# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "2Q2024_REV2_C6.pwf"
# system = "NE224_CASO1_MA.pwf"

method = "EXLF"  # NEWTON-RAPHSON
# method = "LFDC" # LINEARIZED NEWTON-RAPHSON
# method = "EXIC" # CONTINUATION POWER FLOW
# method = "EXCT" # CONTINGENCY ANALYSIS
# method = "EXCE" # CROSS-ENTROPY
method = "EXSC" # STOCHASTIC (ANAREDE BATCH RUNNING)
# method = "EXPC" # POINT OF COLLAPSE
# method = "EXSI"  # DYNAMIC SIMULATION
# method = "DATA" # DATA MANIPULATION
# method = "BPWF" # ANAREDE BATCH RUNNING
# method = "PSSe" # PSS/E EXCEL FILE FORMATTING
# method = "PWF"  # FILE MODIFYING AND SAVING AS REQUESTED BY PROF. RKUIAVA
# method = "REL"  # READING ANAREDE REL FILES

control = [
    # "CREM",
    # "CTAP",
    # "CTAPd",
    # "FREQ",
    # "QLIM",
    # "QLIMs",
    # "SVCs",
]

monitor = [
    # "PFLOW",
    # "PGMON",
    # "QGMON",
    # "VMON",
]

report = [
    "RBAR",
    # "RLIN",
    # "RGER",
    # "RCER",
]

PowerFlow(
    system=system,
    method=method,
    control=control,
    monitor=monitor,
    report=report,
)
