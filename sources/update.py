# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import conj, diag, exp, sum

from ctrl import controlupdt


def updtstt(
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
    powerflow.solution["theta"][powerflow.maskP] += (
        powerflow.solution["sign"] * powerflow.statevar[0:(thetavalues)]
    )
    powerflow.solution["voltage"][powerflow.maskQ] += (
        powerflow.solution["sign"]
        * powerflow.statevar[(thetavalues) : (thetavalues + voltagevalues)]
    )

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    if powerflow.solution["method"] == "CANI":
        powerflow.solution["lambda"] += (
            powerflow.solution["sign"]
            * powerflow.statevar[(thetavalues + voltagevalues + powerflow.controldim)]
        )
        powerflow.solution["eigen"][powerflow.mask] += (
            powerflow.solution["sign"]
            * powerflow.statevar[
                (thetavalues + voltagevalues + powerflow.controldim + 1) :
            ]
        )


def updtpwr(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    I = powerflow.Ybus @ V
    S = diag(V) @ conj(I)

    powerflow.solution["active"] = (
        S.real * powerflow.options["BASE"]
        + powerflow.dbarraDF["demanda_ativa"].tolist()
    )
    powerflow.solution["reactive"] = (
        S.imag * powerflow.options["BASE"]
        + powerflow.dbarraDF["demanda_reativa"].tolist()
    )
