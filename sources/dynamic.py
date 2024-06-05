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
    abs,
    angle,
    rad2deg,
    pi,
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
    # Variável para armazenamento de solução
    powerflow.solution.update(
        {
            "method": "EXSI",
        }
    )

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
        dmdg = powerflow.dmdgDF.loc[powerflow.dmdgDF["numero"] == value["gerador"]]
        if dmdg.tipo.values[0] == "MD01":
            md01(
                powerflow,
                gen,
                dmdg,
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

    deltaref = delta[powerflow.refgen]

    powerflow.solution["fem"] = abs(Eg)
    powerflow.solution["delta0"] = arctan(Eg.imag / Eg.real) - deltaref
    powerflow.solution["omega0"] = ones(powerflow.nger)
    powerflow.solution["delta"] = arctan(Eg.imag / Eg.real) - deltaref
    powerflow.solution["omega"] = ones(powerflow.nger)

    powerflow.deltagen = zeros((powerflow.nger * 2))

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
                allevents = powerflow.devtDF.loc[
                    powerflow.devtDF.tempo == value, "tipo"
                ].tolist()
                for event in allevents:
                    if event == "APCB":
                        Yred = apcb(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                            Yblc,
                        )
                    elif event == "RMCB":
                        Yred = rmcb(
                            powerflow,
                            Yblc,
                        )
                    elif event == "RMGR":
                        Yred = rmgr(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                            Yblc,
                        )
                    elif event == "ABCI":
                        Yred = abci(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                            Yblc,
                        )

                Yblc = deepcopy(Yblcaux)
                timenewt(
                    powerflow,
                    Yred,
                )

            elif value not in powerflow.devtDF.tempo.tolist():
                timenewt(
                    powerflow,
                    Yred,
                )

        except:
            pass

        y.append(
            concatenate((powerflow.solution["delta"], powerflow.solution["omega"]))
        )
        powerflow.solution["delta0"] = deepcopy(powerflow.solution["delta"])
        powerflow.solution["omega0"] = deepcopy(powerflow.solution["omega"])

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
    Yred,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.solution["iter"] = 0

    while True:
        gen = 0
        for generator in powerflow.generator:
            if powerflow.generator[generator][0] == "MD01":
                md01residue(
                    powerflow,
                    Yred,
                    generator,
                    gen,
                )
                md01jacob(
                    powerflow,
                    generator,
                    gen,
                    Yred,
                )
            gen += 1

        try:
            # Your sparse matrix computation using spsolve here
            powerflow.timestatevar, residuals, rank, singular = lstsq(
                powerflow.jacobiangen,
                -powerflow.deltagen,
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
