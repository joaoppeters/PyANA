# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import dot, eye, inf
from numpy.linalg import norm, solve
from scipy.sparse.linalg import inv, spsolve, lsqr, lsmr

def inverse(
    powerflow,
    mu=0.5,
    tol=1e-6,
):
    """inverse power method - (Canizares, 1992)
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    x0 = 1.0 * (powerflow.mask[powerflow.mask])
    I = eye(sum(powerflow.mask))

    while True:
        x1 = solve(powerflow.jacobian.A - mu * I, x0)
        x1 /= norm(x1, inf)  # Normalize eigenvector
        mu = dot(x0, x1)  # Approximation of eigenvalue
        print(norm(x1 - x0, inf))
        if norm(x1 - x0, inf) < tol:
            break
        x0 = x1
    
    powerflow.solution["eigen"] = x1
