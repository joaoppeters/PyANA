# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "ieee14.pwf"

method = "NEWTON"
# method = "CPF"
# method = 'STOCH-CE'
method = "CANI"

# control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVCs']
control = [
    
]

# monitor = [
#     'PFLOW',
#     'PGMON',
#     'QGMON',
#     'VMON',
# ]
monitor = [
    
]

# report = [
#     'RBAR',
#     'RLIN',
#     'RGER',
#     'RSVC',
# ]
report = [
    "RBAR",
]

PowerFlow(
    system=system,
    method=method,
    control=control,
    monitor=monitor,
    report=report,
)
