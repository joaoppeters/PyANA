# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import conj, ones, r_, vectorize
from scipy.sparse import csr_matrix as sparse


def admit(
    powerflow,
):
    """Método para cálculo dos parâmetros da matriz Admitância

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """ """Builds the bus admittance matrix and branch admittance matrices.

    Returns the full bus admittance matrix (i.e. for all buses) and the
    matrices C{Yf} and C{Yt} which, when multiplied by a complex voltage
    vector, yield the vector currents injected into each line from the
    "from" and "to" buses respectively of each line. Does appropriate
    conversions to p.u.

    @see: L{makeSbus}

    @author: Ray Zimmerman (PSERC Cornell)

    ALL RIGHTS RESERVED TO RAY ZIMMERMAN
    CODE RETRIEVED FROM: https://github.com/rwl/PYPOWER
    """

    ## Inicialização
    Ysr = 1 / vectorize(complex)(
        powerflow.dlinhaDF["resistencia"], powerflow.dlinhaDF["reatancia"]
    )
    Ysh = vectorize(complex)(
        0, powerflow.dbarraDF["shunt_barra"] / powerflow.options["BASE"]
    )

    Ytt = Ysr + vectorize(complex)(0, powerflow.dlinhaDF["susceptancia"])
    Yff = Ytt / (
        vectorize(complex)(powerflow.dlinhaDF["tap"] * conj(powerflow.dlinhaDF["tap"]))
    )
    Yft = -Ysr / conj(powerflow.dlinhaDF["tap"])
    Ytf = -Ysr / powerflow.dlinhaDF["tap"]

    f = (powerflow.dlinhaDF["de-idx"]).values
    t = (powerflow.dlinhaDF["para-idx"]).values

    ## connection matrix for line & from buses
    Cf = sparse(
        (ones(powerflow.nlin), (range(powerflow.nlin), f)),
        (powerflow.nlin, powerflow.nbus),
    )
    ## connection matrix for line & to buses
    Ct = sparse(
        (ones(powerflow.nlin), (range(powerflow.nlin), t)),
        (powerflow.nlin, powerflow.nbus),
    )

    ## build Yf and Yt such that Yf * V is the vector of complex branch currents injected
    ## at each branch's "from" bus, and Yt is the same for the "to" bus end
    i = r_[range(powerflow.nlin), range(powerflow.nlin)]  ## double set of row indices

    Yf = sparse((r_[Yff, Yft], (i, r_[f, t])), (powerflow.nlin, powerflow.nbus))
    Yt = sparse((r_[Ytf, Ytt], (i, r_[f, t])), (powerflow.nlin, powerflow.nbus))

    ## build Ybus
    powerflow.Ybus = sparse(
        Cf.T @ Yf
        + Ct.T @ Yt
        + sparse(
            (Ysh, (range(powerflow.nbus), range(powerflow.nbus))),
            (powerflow.nbus, powerflow.nbus),
        )
    )

    # Cf = sparse((powerflow.nlin, f, ones(powerflow) (powerflow.nlin, powerflow.nbus)))
    # Ct = sparse((t, (powerflow.nlin, powerflow.nbus)))

    # Yf = sparse((powerflow.nlin, powerflow.nlin, Yff, powerflow.nlin, powerflow.nlin)) @ Cf + sparse((powerflow.nlin, powerflow.nlin, Yft, powerflow.nlin, powerflow.nlin)) @ Ct
    # Yt = sparse((powerflow.nlin, powerflow.nlin, Ytf, powerflow.nlin, powerflow.nlin)) @ Cf + sparse((powerflow.nlin, powerflow.nlin, Ytt, powerflow.nlin, powerflow.nlin)) @ Ct

    # powerflow.Ybus = Cf.T @ Yf + Ct.T @ Yt + sparse(powerflow.nbus, powerflow.nbus, Ysh, powerflow.nbus, powerflow.nbus)


def admitLinear(
    powerflow,
):
    """Método para cálculo dos parâmetros da matriz Admitância
    simplificações do fluxo de potência linear

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
