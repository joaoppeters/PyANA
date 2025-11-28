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
    anatem,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    # Variável para armazenamento de solução
    anatem.solution.update(
        {
            "method": "EXSI",
            "active": anatem.solution["active"] * 1e-2,
            "eventname": "",
        }
    )

    # Transformação das cargas para impedância constante e expansao da matriz admitância
    # load2ycte(
    #     anatem,
    # )
    postflow(
        anatem,
    )

    # Estado SEP após fluxo de potência
    V = anatem.solution["voltage"] * exp(1j * anatem.solution["theta"])
    I = anatem.Yb @ V

    Ig = append(I[~anatem.maskQ], zeros((anatem.nbus), dtype=complex))
    Eg = inv(anatem.Yblc.A) @ Ig

    Eg = Eg[: anatem.nger]
    delta = arctan(Eg.imag / Eg.real)
    Eg = abs(Eg) * exp(1j * delta)

    anatem.solution["fem"] = abs(Eg)
    anatem.solution["delta"] = delta  # - deltaref
    anatem.solution["omega"] = zeros(anatem.nger)

    anatem.solution["fem0"] = deepcopy(anatem.solution["fem"])
    anatem.solution["delta0"] = deepcopy(anatem.solution["delta"])
    anatem.solution["omega0"] = deepcopy(anatem.solution["omega"])
    anatem.solution["theta0"] = deepcopy(anatem.solution["theta"])
    anatem.solution["voltage0"] = deepcopy(anatem.solution["voltage"])

    y = list()
    event = 0
    anatem.YblcOG = deepcopy(anatem.Yblc)

    t = arange(
        0.0,
        anatem.dsimDF.tmax.values[0] + anatem.dsimDF.step.values[0],
        anatem.dsimDF.step.values[0],
    )

    for _, tempo in enumerate(t):
        try:
            if tempo in anatem.devtDF.tempo.tolist():
                allevents = anatem.devtDF.loc[
                    anatem.devtDF.tempo == tempo, "tipo"
                ].tolist()
                for event in allevents:
                    if event == "APCB":
                        anatem.Yblc = deepcopy(anatem.YblcOG)
                        anatem.solution["eventname"] += "APCB"
                        apcb(
                            anatem,
                            anatem.devtDF.loc[anatem.devtDF.tipo == event].index[0],
                        )
                    elif event == "RMCB":
                        anatem.Yblc = deepcopy(anatem.YblcOG)
                        anatem.solution["eventname"] += "RMCB"
                    elif event == "RMGR":
                        anatem.Yblc = deepcopy(anatem.YblcOG)
                        anatem.solution["eventname"] += "RMGR"
                        rmgr(
                            anatem,
                            anatem.devtDF.loc[anatem.devtDF.tipo == event].index[0],
                        )
                    elif event == "ABCI":
                        anatem.solution["eventname"] += "ABCI"
                        abci(
                            anatem,
                            anatem.devtDF.loc[anatem.devtDF.tipo == event].index[0],
                        )

                timenewt(
                    anatem,
                )

            elif (
                tempo not in anatem.devtDF.tempo.tolist()
                and tempo > anatem.devtDF.tempo.tolist()[0]
            ):
                timenewt(
                    anatem,
                )

        except:
            pass

        y.append(
            concatenate(
                (
                    [tempo],
                    anatem.solution["delta"],
                    anatem.solution["omega"],
                    anatem.solution["theta"],
                    anatem.solution["voltage"],
                )
            )
        )
        anatem.solution["delta0"] = deepcopy(anatem.solution["delta"])
        anatem.solution["omega0"] = deepcopy(anatem.solution["omega"])
        anatem.solution["theta0"] = deepcopy(anatem.solution["theta"])
        anatem.solution["voltage0"] = deepcopy(anatem.solution["voltage"])

    y = array(y)
    timeplot(
        anatem,
        y,
    )


def timenewt(
    anatem,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    anatem.solution["iter"] = 0
    anatem.deltagen = zeros((2 * (2 * anatem.nger + anatem.nbus)))

    while True:
        gen = 0
        for generator in anatem.generator:
            if anatem.generator[generator][0] == "MD01":
                md01residue(
                    anatem,
                    generator,
                    gen,
                )
                md01jacob(
                    anatem,
                    generator,
                    gen,
                )
            gen += 1

        resexsi(
            anatem,
        )

        jacexsi(
            anatem,
        )

        try:
            # Your sparse matrix computation using spsolve here
            anatem.timestatevar, residuals, rank, singular = lstsq(
                anatem.jacobiangen,
                -anatem.deltagen,
                rcond=None,
            )
        except LinAlgError:
            raise ValueError(
                "\033[91mERROR: Falha ao inverter a Matriz (singularidade)!\033[0m"
            )

        # Atualização das Variáveis de estado
        updttm(
            anatem,
        )

        # Incremento de iteração
        anatem.solution["iter"] += 1

        # Condição de Divergência por iterações
        if anatem.solution["iter"] > anatem.options["ACIT"]:
            anatem.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

        elif (norm(anatem.timestatevar) <= anatem.options["CTOL"]) and (
            anatem.solution["iter"] <= anatem.options["ACIT"]
        ):
            break


def timeplot(
    anatem,
    y,
):
    """

    Args
        anatem:
        y:
    """
    ## Inicialização
    # savetxt(anatem.maindir + "\\sistemas\\" + anatem.name + anatem.solution["eventname"] + '.txt', y, fmt='%.4f')

    linestyles = [
        "--",
        ":",
        "-",
        "-.",
        "-",
    ]

    for gen in range(0, anatem.nger):
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
            y[:, gen + anatem.nger + 1],
            label="Gerador {}".format(gen + 1),
            linestyle=linestyles[gen],
        )
        plt.ylabel("Velocidade (rad/s)")
        plt.xlabel("Tempo (s)")
        plt.legend()

    plt.show()
