# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import append, arange, arctan, concatenate, conj, diag, exp, pi, zeros
from numpy.linalg import inv


def dynamic(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Transformação das cargas para impedância constante
    load2zcte = diag(
        (
            powerflow.dbarDF.demanda_ativa.values
            - 1j * powerflow.dbarDF.demanda_reativa.values
        )
        / powerflow.solution["voltage"] ** 2
    )
    Ybl = powerflow.Yb.A + load2zcte

    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    Ig = Ybl @ V

    Ya = zeros([powerflow.nger, powerflow.nger], dtype=complex)
    Yb = zeros([powerflow.nbus, powerflow.nger], dtype=complex)
    powerflow.generator = dict()

    for idx, value in powerflow.dmaqDF.iterrows():
        nome = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "nome"
        ].values[0]
        powerflow.generator[nome] = list()
        value2 = powerflow.dmdgDF.loc[powerflow.dmdgDF["numero"] == value["gerador"]]
        if value2.tipo.values[0] == "MD01":
            powerflow.generator[nome].append(
                value2["l-transitoria"].values[0] * 2 * pi * powerflow.options["FBASE"]
            )
            powerflow.generator[nome].append(value2["r-armadura"].values[0])
            powerflow.generator[nome].append(value2["inercia"].values[0])
            powerflow.generator[nome].append(value2["amortecimento"].values[0])
            Ya[idx, idx] = 1 / (1j * powerflow.generator[nome][0])
            Yb[value["numero"] - 1, idx] = -1 / (1j * powerflow.generator[nome][0])
            Ybl[value["numero"] - 1, value["numero"] - 1] += 1 / (
                1j * powerflow.generator[nome][0]
            )

    Yr = Ya - Yb.T @ inv(Ybl) @ Yb
    I = Ig[~powerflow.maskQ]
    I = append(I, zeros((powerflow.nbus), dtype=complex))

    Yblt = concatenate(
        (concatenate((Ya, Yb.T), axis=1), concatenate((Yb, Ybl), axis=1)),
        axis=0,
    )

    Eg = inv(Yblt) @ I
    Eg = Eg[: powerflow.nger]

    delta = arctan(Eg.imag, Eg.real)
    Ig = Yr @ Eg
    peu = Eg @ conj(Ig)
    x0 = append([zeros(powerflow.nger), delta, peu.real])
    x = list()
    y = list()

    event = 0

    t = arange(
        0.0,
        powerflow.dsimDF.tmax.values[0] + powerflow.dsimDF.step.values[0],
        powerflow.dsimDF.step.values[0],
    )

    for idx, value in enumerate(t):
        if value == powerflow.devtDF.iloc[event]["tempo"]:
            if powerflow.devtDF.iloc[event]["tipo"] == "APCB":
                Yr = apcb(
                    powerflow,
                    Yblt,
                )
            elif powerflow.devtDF.iloc[event]["tipo"] == "RMCB":
                Yr = rmcb(
                    powerflow,
                    Yblt,
                )
            elif powerflow.devtDF.iloc[event]["tipo"] == "RMGR":
                Yr = rmgr(
                    powerflow,
                    Yblt,
                )
            event += 1
            Ig = Yr @ Eg
            peu = Eg @ conj(Ig)
            w = (
                pi * powerflow.dsimDF.step.values[0] / (2 * powerflow.dsimDF.inercia)
            ) * (
                (powerflow.solution["active"] * 1e-2 - peu.real)
                + x0[: powerflow.nger]
                * (powerflow.solution["active"] - x0[2 * powerflow.nger :])
            )
            d = (powerflow.dsimDF.step.values[0] / 2) * (
                w + x0[powerflow.nger : 2 * powerflow.nger] * x0[: powerflow.nger]
            )
            x0 = append(w, d, peu.real)

        else:
            Ig = Yr @ Eg
            peu = Eg @ conj(Ig)
            w = (
                pi * powerflow.dsimDF.step.values[0] / (2 * powerflow.dsimDF.inercia)
            ) * (
                (powerflow.solution["active"] * 1e-2 - peu.real)
                + x0[: powerflow.nger]
                * (powerflow.solution["active"] - x0[2 * powerflow.nger :])
            )
            d = (powerflow.dsimDF.step.values[0] / 2) * (
                w + x0[powerflow.nger : 2 * powerflow.nger] * x0[: powerflow.nger]
            )
            x0 = append(w, d, peu.real)
        y.append(x0)

    print()


def apcb(
    powerflow,
    Yblt,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def rmcb(
    powerflow,
    Yblt,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def rmgr(
    powerflow,
    Yblt,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
