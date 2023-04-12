# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from powerflow import PowerFlow

system = 'libsvc.pwf'

method = 'NEWTON'
# method = 'CPF'

control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVCs', 'VCTRL']
# control = ['QLIMs']
control = ['SVCs']
# control = ['QLIM', 'SVCs',]
# control = []

options = {
    'sbase': 100.,
    'itermx': 15,
    'tolP': 1E-10, #10
    'tolQ': 1E-10, #10
    'tolY': 1E-10, #10
    'vmax': 1.05,
    'vmin': 0.95,
    'vvar': 1E-10,
    'qvar': 1E-8,
    'cpfBeta': 0.,
    'cpfLambda': 1E-1,
    'cpfV2L': 0.95,
    'cpfVolt': 1E-4,
    'icmn': 1E-14,
    'full': False,
}

monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = ['QGMON', 'VMON']
monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']

report = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC',]
report = ['RBARRA', 'RLINHA', 'RSVC',]

PowerFlow(
    system=system,
    method=method,
    options=options,
    control=control,
    monitor=monitor,
    report=report,
)