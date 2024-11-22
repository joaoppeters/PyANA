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
    savetxt,
    zeros,
    abs,
    angle,
    rad2deg,
    pi,
)
from numpy.linalg import inv, LinAlgError, lstsq, norm

from devt import *
from generator import *
from matrices import load2ycte, md01jacob, jacexsi
from residue import md01residue, resexsi
from update import updttm


def dynamic(
    powerflow,
):
    """

    Args
        powerflow:
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution.update(
        {
            "method": "EXSI",
            "active": powerflow.solution["active"] * 1e-2,
            "eventname": "",
        }
    )

    # Transformação das cargas para impedância constante e expansao da matriz admitância
    # load2ycte(
    #     powerflow,
    # )
    postflow(
        powerflow,
    )

    # Estado SEP após fluxo de potência
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    I = powerflow.Yb @ V

    Ig = append(I[~powerflow.maskQ], zeros((powerflow.nbus), dtype=complex))
    Eg = inv(powerflow.Yblc.A) @ Ig

    Eg = Eg[: powerflow.nger]
    delta = arctan(Eg.imag / Eg.real)
    Eg = abs(Eg) * exp(1j * delta)

    powerflow.solution["fem"] = abs(Eg)
    powerflow.solution["delta"] = delta  # - deltaref
    powerflow.solution["omega"] = zeros(powerflow.nger)

    powerflow.solution["fem0"] = deepcopy(powerflow.solution["fem"])
    powerflow.solution["delta0"] = deepcopy(powerflow.solution["delta"])
    powerflow.solution["omega0"] = deepcopy(powerflow.solution["omega"])
    powerflow.solution["theta0"] = deepcopy(powerflow.solution["theta"])
    powerflow.solution["voltage0"] = deepcopy(powerflow.solution["voltage"])

    y = list()
    event = 0
    powerflow.YblcOG = deepcopy(powerflow.Yblc)

    t = arange(
        0.0,
        powerflow.dsimDF.tmax.values[0] + powerflow.dsimDF.step.values[0],
        powerflow.dsimDF.step.values[0],
    )

    for _, tempo in enumerate(t):
        try:
            if tempo in powerflow.devtDF.tempo.tolist():
                allevents = powerflow.devtDF.loc[
                    powerflow.devtDF.tempo == tempo, "tipo"
                ].tolist()
                for event in allevents:
                    if event == "APCB":
                        powerflow.Yblc = deepcopy(powerflow.YblcOG)
                        powerflow.solution["eventname"] += "APCB"
                        apcb(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                        )
                    elif event == "RMCB":
                        powerflow.Yblc = deepcopy(powerflow.YblcOG)
                        powerflow.solution["eventname"] += "RMCB"
                    elif event == "RMGR":
                        powerflow.Yblc = deepcopy(powerflow.YblcOG)
                        powerflow.solution["eventname"] += "RMGR"
                        rmgr(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                        )
                    elif event == "ABCI":
                        powerflow.solution["eventname"] += "ABCI"
                        abci(
                            powerflow,
                            powerflow.devtDF.loc[powerflow.devtDF.tipo == event].index[
                                0
                            ],
                        )

                timenewt(
                    powerflow,
                )

            elif (
                tempo not in powerflow.devtDF.tempo.tolist()
                and tempo > powerflow.devtDF.tempo.tolist()[0]
            ):
                timenewt(
                    powerflow,
                )

        except:
            pass

        y.append(
            concatenate(
                (
                    [tempo],
                    powerflow.solution["delta"],
                    powerflow.solution["omega"],
                    powerflow.solution["theta"],
                    powerflow.solution["voltage"],
                )
            )
        )
        powerflow.solution["delta0"] = deepcopy(powerflow.solution["delta"])
        powerflow.solution["omega0"] = deepcopy(powerflow.solution["omega"])
        powerflow.solution["theta0"] = deepcopy(powerflow.solution["theta"])
        powerflow.solution["voltage0"] = deepcopy(powerflow.solution["voltage"])

    y = array(y)
    timeplot(
        powerflow,
        y,
    )


def timenewt(
    powerflow,
):
    """

    Args
        powerflow:
    """

    ## Inicialização
    powerflow.solution["iter"] = 0
    powerflow.deltagen = zeros((2 * (2 * powerflow.nger + powerflow.nbus)))

    while True:
        gen = 0
        for generator in powerflow.generator:
            if powerflow.generator[generator][0] == "MD01":
                md01residue(
                    powerflow,
                    generator,
                    gen,
                )
                md01jacob(
                    powerflow,
                    generator,
                    gen,
                )
            gen += 1

        resexsi(
            powerflow,
        )

        jacexsi(
            powerflow,
        )

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
            powerflow.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

        elif (norm(powerflow.timestatevar) <= powerflow.options["CTOL"]) and (
            powerflow.solution["iter"] <= powerflow.options["ACIT"]
        ):
            break


def timeplot(
    powerflow,
    y,
):
    """

    Args
        powerflow:
        y:
    """

    ## Inicialização
    # savetxt(powerflow.maindir + "/sistemas/" + powerflow.name + powerflow.solution["eventname"] + '.txt', y, fmt='%.4f')

    linestyles = [
        "--",
        ":",
        "-",
        "-.",
        "-",
    ]

    for gen in range(0, powerflow.nger):
        plt.figure(1)
        plt.plot(
            y[:, 0],
            y[:, gen + 1],
            label="Gerador {}".format(gen + 1),
            linestyle=linestyles[gen],
        )
        plt.ylabel("Ângulo (rad)")
        plt.xlabel("Tempo (s)")
        plt.legend()

        plt.figure(2)
        plt.plot(
            y[:, 0],
            y[:, gen + powerflow.nger + 1],
            label="Gerador {}".format(gen + 1),
            linestyle=linestyles[gen],
        )
        plt.ylabel("Velocidade (rad/s)")
        plt.xlabel("Tempo (s)")
        plt.legend()

    plt.show()
