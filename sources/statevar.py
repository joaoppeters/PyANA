# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from ctrl import controlupdt

def update(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    thetavalues = sum(powerflow.maskP)
    voltagevalues = sum(powerflow.maskQ)

    # configuração reduzida
    powerflow.solution["theta"][powerflow.maskP] += powerflow.solution["sign"] * powerflow.statevar[0:(thetavalues)]
    powerflow.solution["voltage"][powerflow.maskQ] += powerflow.solution["sign"] * powerflow.statevar[
        (thetavalues) : (thetavalues + voltagevalues)
    ]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    if powerflow.method == "CANI":
        powerflow.solution["lambda"] += powerflow.solution["sign"] * powerflow.statevar[
            (thetavalues + voltagevalues + powerflow.controldim)
        ]
        powerflow.solution["eigen"][powerflow.mask] += powerflow.solution["sign"] * powerflow.statevar[
            (thetavalues + voltagevalues + powerflow.controldim + 1) :
        ]
