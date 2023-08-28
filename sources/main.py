# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = 'PD 2032-LEVE_NORTE SECO_2026.pwf'

method = 'NEWTON'
# method = 'CPF'

# control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVCs', 'VCTRL']
control = ['SVCs']
# control = ['SVCs']
# control = ['QLIM', 'SVCs',]
control = []

options = {
    'sbase': 100.,
    'itermx': 15,
    'tolP': 1E-8, #10
    'tolQ': 1E-8, #10
    'tolY': 1E-8, #10
    'vmax': 1.05,
    'vmin': 0.95,
    'vvar': 1E-8,
    'qvar': 1E-8,
    'cpfBeta': 0.,
    'cpfLambda': 1E-1,
    'cpfV2L': 0.95,
    'cpfVolt': 1E-4,
    'icmn': 1E-10,
    'full': False,
}

monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = ['QGMON', 'VMON']
monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = []

report = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC',]
report = ['RBARRA',]

PowerFlow(
    system=system,
    method=method,
    options=options,
    control=control,
    monitor=monitor,
    report=report,
)