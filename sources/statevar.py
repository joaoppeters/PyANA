# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import arange, degrees, linspace, max, min, ones, pi

from folder import statevarfolder

def statevar(
    powerflow,
):
    '''inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
        setup: self do arquivo setup.py
    '''

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
    # if powerflow.nbuscontrol:
    #     # Resultado final de convergência das variáveis de estado adicionais
    #     stateY(
    #         powerflow,
    #     )

def stateVT(
    self,
    powerflow,
):
    '''resultado final de convergência das magnitudes e ângulos de tensão

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    fig, ax = plt.subplots(
        nrows=1, ncols=1, subplot_kw={'projection': 'polar'}, figsize=(8, 9)
    )

    # Referência
    self.thetaref = powerflow.solution['theta'][
        powerflow.nbusdbarraDF.loc[powerflow.nbusdbarraDF['tipo'] == 2].index[0]
    ]

    # Plots
    colors = plt.cm.viridis(arange(powerflow.nbusnbus) / powerflow.nbusnbus)
    bars = ax.bar(
        powerflow.solution['theta'],
        powerflow.solution['voltage'],
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
        linestyle='--',
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
        powerflow.nbusoptions['vmax'] * ones(360),
        linestyle='--',
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
        powerflow.nbusoptions['vmin'] * ones(360),
        linestyle='--',
        color=(1.0, 0.8, 0.7961),
        alpha=1.0,
        zorder=2,
    )

    for theta, rotation, label in zip(
        powerflow.solution['theta'],
        degrees(powerflow.solution['theta']),
        powerflow.nbusdbarraDF['nome'].values,
    ):
        ax.text(
            theta,
            ax.get_ylim()[1] + 0.075,
            label,
            ha='left',
            va='center',
            rotation=rotation - degrees(self.thetaref),
            rotation_mode='anchor',
            fontsize=5,
        )

    # Label
    ax.set_title('Magnitude e Ângulo de Tensão dos Barramentos')
    ax.set_thetamax(max(degrees(powerflow.solution['theta'])) + 5)
    ax.set_thetamin(min(degrees(powerflow.solution['theta'])) - 5)
    ax.set_rticks(
        [
            1.0,
        ]
    )
    ax.set_yticklabels({'1 p.u.'})
    ax.legend(
        bars,
        powerflow.nbusdbarraDF['nome'].values.tolist(),
        frameon=False,
        loc='upper center',
        bbox_to_anchor=(0.5, -0.025),
        fancybox=True,
        ncol=int(5),
        prop={'size': 7},
    )
    ax.set_theta_offset(-self.thetaref)

    # Save
    fig.savefig(
        powerflow.nbusdirRstatevar + powerflow.nbusname + '-stateVT.png',
        dpi=400,
    )

def stateY(
    self,
    powerflow,
):
    '''resultado final de convergência das variáveis de estado adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    pass
