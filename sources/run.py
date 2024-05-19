# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "ieee14.pwf"

method = "EXLF" # NEWTON-RAPHSON
method = "LFDC" # LINEARIZED NEWTON-RAPHSON
# method = "EXIC" # CONTINUATION POWER FLOW
# method = "EXCE" # CROSS-ENTROPY
# method = "EXSC" # STOCHASTIC
# method = "EXPC" # POINT OF COLLAPSE
# method = "DATA" # DATA MANIPULATION
# method = "BATCH" # ANAREDE BATCH RUNNING
# method = "PWF" # FILE MODIFYING AND SAVING AS REQUESTED BY ROMAN KUIAVA

control = [
    # "CREM",
    # "CTAP",
    # "CTAPd",
    # "FREQ",
    # "QLIM",
    # "QLIMs",
    "SVCs",
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
    "RCER",
]

PowerFlow(
    system=system,
    method=method,
    control=control,
    monitor=monitor,
    report=report,
)
