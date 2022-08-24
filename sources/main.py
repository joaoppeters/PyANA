from os import getcwd
from os.path import dirname, realpath
from powerflow import PowerFlow

sistema = 'ieee14.pwf'

arqv = realpath(dirname(dirname(__file__)) + '/sistemas/' + sistema)

method = 'NEWTON'

jacobi = 'COMPLETA'

control = ['CREM CST CTAP CTAPd FREQ QLIM SVC VCTRL']

options = {
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

rel = ['RBARRA RLINHA RGERA RSVC RCPF']

PowerFlow(
    # arqv=arqv,
    method=method,
    jacobi=jacobi,
    options=options,
    control=control,
    rel=rel,
)