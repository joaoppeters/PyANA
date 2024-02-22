# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import abs, max, zeros
from numpy.linalg import eig, norm, solve
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
    x = zeros(sum(powerflow.mask))
    x[0] = 1
    x /= norm(x)  # Normalize eigenvector

    while True:
        y = solve(powerflow.jacobian.A, x)
        eigenvalue = max(abs(y))
        x = y / eigenvalue

        print(norm(powerflow.jacobian.A @ x - eigenvalue * x))
        if norm(powerflow.jacobian.A @ x - eigenvalue * x) < tol:
            break
    
    y = 1 / y
    powerflow.solution["eigen"] = x
