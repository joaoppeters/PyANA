# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import arange

from folder import convergencefolder


class Convergence:
    """classe para geração das trajetórias de convergência das variáveis de estado do fluxo de potência"""


def convergence(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
        setup: self do arquivo setup.py
    """

    ## Inicialização
    # Criação de pasta
    convergencefolder(
        powerflow,
    )

    # # Convergência de Potência Ativa
    # convP(
    #     powerflow,
    # )

    # # Convergência de Potência Reativa
    # convQ(
    #     powerflow,
    # )

    # # Condição
    # if powerflow.control:
    #     # Convergência de Equações de Controle Adicionais
    #     convY(
    #         powerflow,
    #     )


def convP(
    powerflow,
):
    """trajetória de convergência de equação de potência ativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    fig, ax = plt.subplots(nrows=1, ncols=1)

    # Plots
    if powerflow.solution["convergence"] == "SISTEMA CONVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convP"] * powerflow.options["BASE"]),
            color="C0",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convP"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    elif powerflow.solution["convergence"] == "SISTEMA DIVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convP"] * powerflow.options["BASE"]),
            color="C0",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convP"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    # Label
    ax.set_title("Trajetória de Convergência de Potência Ativa")
    ax.set_xlabel("Iterações")
    ax.set_xticks(arange(0, powerflow.solution["iter"] + 1))
    ax.set_ylabel("Resíduo de Potência Ativa [MW]")
    ax.legend(
        [
            (
                line,
                mark,
            )
        ],
        [f"abs(max($\Delta$P))"],
    )
    ax.grid()

    # Save
    fig.savefig(
        powerflow.nbusdirRconvergence + powerflow.name + "-trajconv-deltaP.png",
        dpi=400,
    )


def convQ(
    powerflow,
):
    """trajetória de convergência de equação de potência reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    fig, ax = plt.subplots(nrows=1, ncols=1)

    # Plots
    if powerflow.solution["convergence"] == "SISTEMA CONVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convQ"] * powerflow.options["BASE"]),
            color="C1",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convQ"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    elif powerflow.solution["convergence"] == "SISTEMA DIVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convQ"] * powerflow.options["BASE"]),
            color="C1",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convQ"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    # Label
    ax.set_title("Trajetória de Convergência de Potência Reativa")
    ax.set_xlabel("Iterações")
    ax.set_xticks(arange(0, powerflow.solution["iter"] + 1))
    ax.set_ylabel("Resíduo de Potência Reativa [MVAr]")
    ax.legend(
        [
            (
                line,
                mark,
            )
        ],
        [f"abs(max($\Delta$Q))"],
    )
    ax.grid()

    # Save
    fig.savefig(
        powerflow.nbusdirRconvergence + powerflow.name + "-trajconv-deltaQ.png",
        dpi=400,
    )


def convY(
    powerflow,
):
    """trajetória de convergência de equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    fig, ax = plt.subplots(nrows=1, ncols=1)

    # Plots
    if powerflow.solution["convergence"] == "SISTEMA CONVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convY"] * powerflow.options["BASE"]),
            color="C1",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"] + 1),
            (powerflow.solution["convY"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    elif powerflow.solution["convergence"] == "SISTEMA DIVERGENTE":
        (line,) = ax.plot(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convY"] * powerflow.options["BASE"]),
            color="C1",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        mark = ax.scatter(
            arange(0, powerflow.solution["iter"]),
            (powerflow.solution["convY"] * powerflow.options["BASE"]),
            color=(1.0, 1.0, 1.0),
            marker="*",
            edgecolor=(0.0, 0.0, 0.0),
            alpha=1.0,
            s=100,
            zorder=3,
        )

    # Label
    ax.set_title("Trajetória de Convergência de Potência Reativa")
    ax.set_xlabel("Iterações")
    ax.set_xticks(arange(0, powerflow.solution["iter"] + 1))
    ax.set_ylabel("Resíduo de Variável de Controle")
    ax.legend(
        [
            (
                line,
                mark,
            )
        ],
        [f"abs(max($\Delta$Y))"],
    )
    ax.grid()

    # Save
    fig.savefig(
        powerflow.nbusdirRconvergence + powerflow.name + "-trajconv-deltaY.png",
        dpi=400,
    )
