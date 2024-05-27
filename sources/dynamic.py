# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from matplotlib import pyplot as plt
from numpy import (
    append,
    arange,
    arctan,
    array,
    concatenate,
    diag,
    exp,
    ones,
    pi,
    zeros,
)
from numpy.linalg import inv

from devt import *
from newton import timenewt


def dynamic(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Transformação das cargas para impedância constante
    load2ycte = diag(
        (
            powerflow.dbarDF.demanda_ativa.values
            - 1j * powerflow.dbarDF.demanda_reativa.values
        )
        * 1e-2
        / powerflow.solution["voltage"] ** 2
    )
    Ybl = powerflow.Yb.A + load2ycte

    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    Ig = Ybl @ V

    Ya = zeros([powerflow.nger, powerflow.nger], dtype=complex)
    Yb = zeros([powerflow.nger, powerflow.nbus], dtype=complex)

    powerflow.generator = dict()
    for idx, value in powerflow.dmaqDF.iterrows():
        gen = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "numero"
        ].values[0]
        powerflow.generator[gen] = list()
        value2 = powerflow.dmdgDF.loc[powerflow.dmdgDF["numero"] == value["gerador"]]
        if value2.tipo.values[0] == "MD01":
            md01(
                powerflow,
                gen,
                value2,
            )

            Ya[idx, idx] = 1 / (1j * powerflow.generator[gen][3])
            Yb[idx, value["numero"] - 1] = -1 / (1j * powerflow.generator[gen][3])
            Ybl[value["numero"] - 1, value["numero"] - 1] += 1 / (
                1j * powerflow.generator[gen][3]
            )

    I = Ig[~powerflow.maskQ]
    I = append(I, zeros((powerflow.nbus), dtype=complex))

    Yblc = concatenate(
        (concatenate((Ya, Yb), axis=1), concatenate((Yb.T, Ybl), axis=1)),
        axis=0,
    )
    Yblcaux = deepcopy(Yblc)

    E = inv(Yblc) @ I
    Eg = E[: powerflow.nger]
    delta = arctan(Eg.imag / Eg.real)
    Eg = abs(Eg) * exp(1j * delta)
    
    powerflow.solution["fem"] = abs(Eg)
    powerflow.solution["delta"] = arctan(Eg.imag / Eg.real)
    powerflow.solution["omega"] = ones(powerflow.nger)

    x0 = concatenate(
        (
            delta,
            ones(powerflow.nger),
        )
    )

    y = list()
    event = 0

    t = arange(
        0.0,
        powerflow.dsimDF.tmax.values[0] + powerflow.dsimDF.step.values[0],
        powerflow.dsimDF.step.values[0],
    )

    for idx, value in enumerate(t):
        try:
            if value == powerflow.devtDF.iloc[event]["tempo"]:
                if powerflow.devtDF.iloc[event]["tipo"] == "APCB":
                    Yr = apcb(
                        powerflow,
                        event,
                        Yblc,
                    )
                elif powerflow.devtDF.iloc[event]["tipo"] == "RMCB":
                    Yr = rmcb(
                        powerflow,
                        Yblc,
                    )
                elif powerflow.devtDF.iloc[event]["tipo"] == "RMGR":
                    Yr = rmgr(
                        powerflow,
                        event,
                        Yblc,
                    )
                elif powerflow.devtDF.iloc[event]["tipo"] == "ABCI":
                    Yr = abci(
                        powerflow,
                        event,
                        Yblc,
                    )

                Yblc = deepcopy(Yblcaux)
                event += 1
                x0 = timenewt(powerflow, Yblc, x0)

            elif value > powerflow.devtDF.iloc[event - 1]["tempo"]:
                x0 = timenewt(powerflow, Yblc, x0)
                
        except:
            pass
        y.append(x0)

    y = array(y)

    for gen in range(0, powerflow.nger):
        plt.figure(1)
        plt.plot(t, y[:, gen], label="d{}".format(gen + 1))

        plt.figure(2)
        plt.plot(t, y[:, gen + powerflow.nger], label="w{}".format(gen + 1))

    plt.legend()
    plt.show()
    print()    


def md01(
    powerflow,
    gen,
    value2,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.generator[gen].append("MD01")
    powerflow.generator[gen].append(value2["inercia"].values[0])
    powerflow.generator[gen].append(value2["amortecimento"].values[0])
    powerflow.generator[gen].append(value2["l-transitoria"].values[0] * 2 * pi * 1)
    powerflow.generator[gen].append(value2["r-armadura"].values[0])
