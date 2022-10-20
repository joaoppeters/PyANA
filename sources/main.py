# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from powerflow import PowerFlow

system = 'ieee14.pwf'

method = 'NEWTON'

jacobi = 'COMPLETA'

control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVC', 'VCTRL']
control = ['QLIMs']

options = {
    'sbase': 100.,
    'itermx': 15,
    'tolP': 1E-6,
    'tolQ': 1E-6,
    'tolY': 1E-6,
    'vmax': 1.05,
    'vmin': 0.95,
    'cpfBeta': 0.,
    'cpfLambda': 1E-2,
    'cpfV2L': 0.95,
    'full': False,
}

monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = ['QGMON', 'VMON']

report = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC', 'RCPF']
report = ['RBARRA',]

PowerFlow(
    system=system,
    method=method,
    jacobi=jacobi,
    options=options,
    control=control,
    monitor=monitor,
    report=report,
)