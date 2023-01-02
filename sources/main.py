# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from powerflow import PowerFlow

system = '107-Barras.pwf'

method = 'NEWTON'

control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'QLIMs', 'SVC', 'VCTRL']
control = ['QLIMs']
# control = []

options = {
    'sbase': 100.,
    'itermx': 15,
    'tolP': 1E-10,
    'tolQ': 1E-10,
    'tolY': 1E-10,
    'vmax': 1.05,
    'vmin': 0.95,
    'vvar': 1E-10,
    'qvar': 1E-8,
    'cpfBeta': 0.,
    'cpfLambda': 5E-3,
    'cpfV2L': 0.95,
    'cpfVolt': 1E-4,
    'icmn': 1E-14,
    'full': False,
}

monitor = ['PFLOW', 'PGMON', 'QGMON', 'VMON']
monitor = ['QGMON', 'VMON']

report = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC', 'RCPF']
report = ['RBARRA',]

PowerFlow(
    system=system,
    method=method,
    options=options,
    control=control,
    monitor=monitor,
    report=report,
)