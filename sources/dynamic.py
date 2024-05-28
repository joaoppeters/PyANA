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
    zeros,
)
from numpy.linalg import inv, LinAlgError, lstsq, norm

from devt import *
from generator import *
from update import updttm


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
    powerflow.solution["omega"] = zeros(powerflow.nger)

    x0 = concatenate(
        (
            delta,
            zeros(powerflow.nger),
        )
    )

    y = list()
    event = 0

    t = arange(
        0.0,
        powerflow.dsimDF.tmax.values[0] + powerflow.dsimDF.step.values[0],
        powerflow.dsimDF.step.values[0],
    )

    for _, value in enumerate(t):
        try:
            if value in powerflow.devtDF.tempo.tolist():
                allevents = powerflow.devtDF.loc[powerflow.devtDF.tempo == value, "tipo"].tolist()
                for event in allevents:
                    if event == "APCB":
                        Yr = apcb(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[0],
                            Yblc,
                        )
                    elif event == "RMCB":
                        Yr = rmcb(
                            powerflow,
                            Yblc,
                        )
                    elif event == "RMGR":
                        Yr = rmgr(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[0],
                            Yblc,
                        )
                    elif event == "ABCI":
                        Yr = abci(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[0],
                            Yblc,
                        )

                Yblc = deepcopy(Yblcaux)
                powerflow.solution["x"] = deepcopy(x0)
                x0 = timenewt(powerflow, Yr, x0)

            elif value not in powerflow.devtDF.tempo.tolist():
                powerflow.solution["x"] = deepcopy(x0)
                x0 = timenewt(powerflow, Yr, x0)
                
        except:
            pass
        y.append(x0)

    y = array(y)

    for gen in range(0, powerflow.nger):
        plt.figure(1)
        plt.plot(t, y[:, gen] * 180 / pi, label="d{}".format(gen + 1))
        plt.legend()

        plt.figure(2)
        plt.plot(t, y[:, gen + powerflow.nger], label="w{}".format(gen + 1))
        plt.legend()

    plt.show()
    print()    
    
    
def timenewt(
    powerflow,
    Yr,
    x0,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution.update(
        {
            "method": "EXSI",
            "iter": 0,
            "freq": 1.0,
        }
    )

    powerflow.deltagen = zeros(2 * powerflow.nger)

    while True:
        gen = 0
        A1, A2, A3, A4 = zeros((powerflow.nger, powerflow.nger)), zeros((powerflow.nger, powerflow.nger)), zeros((powerflow.nger, powerflow.nger)), zeros((powerflow.nger, powerflow.nger))
        for generator in powerflow.generator:
            if powerflow.generator[generator][0] == "MD01":
                md01newt(powerflow, Yr, x0, generator, gen,)
                md01jacob(powerflow, generator, gen, A1, A2, A3, A4, Yr,)
            gen += 1

        powerflow.jacobiangen = concatenate(
            (
                concatenate((A1, A2), axis=1),
                concatenate((A3, A4), axis=1),
            ),
            axis=0,
        )

        try:
            # Your sparse matrix computation using spsolve here
            powerflow.timestatevar, residuals, rank, singular = lstsq(
                powerflow.jacobiangen,
                powerflow.deltagen,
                rcond=None,
            )
        except LinAlgError:
            raise ValueError(
                "\033[91mERROR: Falha ao inverter a Matriz (singularidade)!\033[0m"
            )

        # Atualização das Variáveis de estado
        updttm(
            powerflow,

        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição de Divergência por iterações
        if powerflow.solution["iter"] > powerflow.options["ACIT"]:
            powerflow.solution[
                "convergence"
            ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

        elif (norm(powerflow.timestatevar) <= powerflow.options["CTOL"]) and (
            powerflow.solution["iter"] <= powerflow.options["ACIT"]
        ):
            break

    return powerflow.solution["x"]
