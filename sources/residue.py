# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import array, concatenate, conj, diag, exp
from ctrl import controlres


def residue(
    powerflow,
    case: int = 0,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    I = powerflow.Ybus@V
    S = diag(V)@conj(I)

    # Resíduos de potência ativa e reativa
    powerflow.deltaP = powerflow.psch - S.real
    powerflow.deltaQ = powerflow.qsch - S.imag

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)

    # Resíduos de variáveis de estado de controle
    if powerflow.controlcount > 0:
        controlres(
            powerflow,
            case,
        )
        powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)
    else:
        powerflow.deltaY = array([0])

    if powerflow.solution["method"] == "CPF":
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, array([0])), axis=0)
        
    powerflow.deltaPQY = powerflow.deltaPQY[powerflow.mask]
