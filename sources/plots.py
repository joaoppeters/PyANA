# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import arange, degrees, linspace, max, min, ones, pi

from folder import convergencefolder, statevarfolder


def convergence(
    powerflow,
):
    """inicialização

    Args
        powerflow: self do arquivo powerflow.py
        setting: self do arquivo setting.py
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

    Args
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
        powerflow.nbusconvergencefolder + powerflow.name + "-trajconv-deltaP.png",
        dpi=400,
    )


def convQ(
    powerflow,
):
    """trajetória de convergência de equação de potência reativa

    Args
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
        powerflow.nbusconvergencefolder + powerflow.name + "-trajconv-deltaQ.png",
        dpi=400,
    )


def convY(
    powerflow,
):
    """trajetória de convergência de equações de controle adicionais

    Args
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
        powerflow.nbusconvergencefolder + powerflow.name + "-trajconv-deltaY.png",
        dpi=400,
    )


def statevar(
    powerflow,
):
    """inicialização

    Args
        powerflow: self do arquivo powerflow.py
        setting: self do arquivo setting.py
    """

    ## Inicialização
    # Criação de pasta
    statevarfolder(
        powerflow,
    )

    # # Resultado final de convergência das magnitudes e ângulos de tensão
    # stateVT(
    #     powerflow,
    # )

    # # Condição
    # if powerflow.control:
    #     # Resultado final de convergência das variáveis de estado adicionais
    #     stateY(
    #         powerflow,
    #     )


def stateVT(
    self,
    powerflow,
):
    """resultado final de convergência das magnitudes e ângulos de tensão

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    fig, ax = plt.subplots(
        nrows=1, ncols=1, subplot_kw={"projection": "polar"}, figsize=(8, 9)
    )

    # Referência
    self.thetaref = powerflow.solution["theta"][
        powerflow.dbarDF.loc[powerflow.dbarDF["tipo"] == 2].index[0]
    ]

    # Plots
    colors = plt.cm.viridis(arange(powerflow.nbus) / powerflow.nbus)
    bars = ax.bar(
        powerflow.solution["theta"],
        powerflow.solution["voltage"],
        width=0.005,
        bottom=0.0,
        color=colors,
        alpha=0.5,
        zorder=3,
    )

    # Limite tensão
    ax.plot(
        linspace(
            0,
            2 * pi,
            360,
            endpoint=False,
        ),
        ones(360),
        linestyle="--",
        color=(0.0, 0.0, 0.0),
        alpha=1.0,
        zorder=2,
    )
    ax.plot(
        linspace(
            0,
            2 * pi,
            360,
            endpoint=False,
        ),
        powerflow.options["vmax"] * ones(360),
        linestyle="--",
        color=(1.0, 0.8, 0.7961),
        alpha=1.0,
        zorder=2,
    )
    ax.plot(
        linspace(
            0,
            2 * pi,
            360,
            endpoint=False,
        ),
        powerflow.options["vmin"] * ones(360),
        linestyle="--",
        color=(1.0, 0.8, 0.7961),
        alpha=1.0,
        zorder=2,
    )

    for theta, rotation, label in zip(
        powerflow.solution["theta"],
        degrees(powerflow.solution["theta"]),
        powerflow.dbarDF["nome"].values,
    ):
        ax.text(
            theta,
            ax.get_ylim()[1] + 0.075,
            label,
            ha="left",
            va="center",
            rotation=rotation - degrees(self.thetaref),
            rotation_mode="anchor",
            fontsize=5,
        )

    # Label
    ax.set_title("Magnitude e Ângulo de Tensão dos Barramentos")
    ax.set_thetamax(max(degrees(powerflow.solution["theta"])) + 5)
    ax.set_thetamin(min(degrees(powerflow.solution["theta"])) - 5)
    ax.set_rticks(
        [
            1.0,
        ]
    )
    ax.set_yticklabels({"1 p.u."})
    ax.legend(
        bars,
        powerflow.dbarDF["nome"].values.tolist(),
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.025),
        fancybox=True,
        ncol=int(5),
        prop={"size": 7},
    )
    ax.set_theta_offset(-self.thetaref)

    # Save
    fig.savefig(
        powerflow.nbusstatevarfolder + powerflow.name + "-stateVT.png",
        dpi=400,
    )


def stateY(
    self,
    powerflow,
):
    """resultado final de convergência das variáveis de estado adicionais

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
