# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = 'ieee14.pwf'

method = 'NEWTON'
# method = 'CPF'
# method = 'STOCH'

# control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVCs']
# control = ['SVCs']
# control = ['SVCs']
control = ['QLIMs', 'SVCs',]
# control = []

monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = ['QGMON', 'VMON']
monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = []

report = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC',]
report = ['RBARRA', 'RSVC',]

PowerFlow(
    system=system,
    method=method,
    control=control,
    monitor=monitor,
    report=report,
)