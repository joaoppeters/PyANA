# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import conj, ones, r_, vectorize, zeros
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

    f = (powerflow.dlinhaDF["de"] - 1).values
    t = (powerflow.dlinhaDF["para"] - 1).values

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
    powerflow.Ybus = (
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
    # Matriz Admitância
    powerflow.Ybus = zeros(shape=[powerflow.nbus, powerflow.nbus], dtype="complex_")
    powerflow.gdiag = zeros(powerflow.nbus)
    powerflow.bdiag = zeros(powerflow.nbus)
    powerflow.apont = ones(powerflow.nbus, dtype=int)
    powerflow.admitancia = 1 / vectorize(complex)(
        real=powerflow.dlinhaDF["resistencia"],
        imag=powerflow.dlinhaDF["reatancia"],
    )

    # Linhas de transmissão e transformadores
    for _, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            if value["transf"]:
                value["tap"] = 1 / value["tap"]

                # Elementos da diagonal (elemento série)
                powerflow.admitancia[_] *= value["tap"]

                powerflow.gdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[_].real
                powerflow.bdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[_].imag
                powerflow.gdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[_].real
                powerflow.bdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[_].imag

            # Elementos da diagonal (elemento série)
            powerflow.gdiag[value["de"] - 1] += powerflow.admitancia[_].real
            powerflow.gdiag[value["para"] - 1] += powerflow.admitancia[_].real
            powerflow.bdiag[value["de"] - 1] += (
                powerflow.admitancia[_].imag + value["susceptancia"]
            )
            powerflow.bdiag[value["para"] - 1] += (
                powerflow.admitancia[_].imag + value["susceptancia"]
            )

            # apontador auxiliar de conexões
            powerflow.apont[value["de"] - 1] += 1
            powerflow.apont[value["para"] - 1] += 1

    for idx, value in powerflow.dbarraDF.iterrows():
        if value["shunt_barra"] != 0.0:
            powerflow.bdiag[value["numero"] - 1] += (
                value["shunt_barra"] / powerflow.options["BASE"]
            )

        if idx != 0:
            powerflow.apont[value["numero"] - 1] += powerflow.apont[value["numero"] - 2]
