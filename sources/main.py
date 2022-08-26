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

control = ['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'SVC', 'VCTRL']

options = {
    'sbase': 100.,
    'itermx': 15,
    'tolP': 1E-6,
    'tolQ': 1E-6,
    'tolY': 1E-6,
    'vmax': 1.05,
    'vmin': 0.95,
    'cpfL': 1E-1,
    'cpfV': 1E-4,
    'cpfV2L': 0.85,
}

mon = ['PFLOW', 'PGMON', 'QGMON', 'VMON']

rel = ['RBARRA', 'RLINHA', 'RGERA', 'RSVC', 'RCPF']

PowerFlow(
    system=system,
    method=method,
    jacobi=jacobi,
    options=options,
    control=control,
    mon=mon,
    rel=rel,
)