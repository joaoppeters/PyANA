# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "ieee14.pwf"

method = "NEWTON"
method = "CPF"
# method = "CE"
# method = "STOCH"
# method = "tPoC"
# method = "fDATA"
# method = "PWF"

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
