# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import array, concatenate, zeros
from calc import pcalc, qcalc
from ctrl import controlres

def residue(
    powerflow,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    powerflow.deltaP = zeros(powerflow.nbus)
    powerflow.deltaQ = zeros(powerflow.nbus)

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Tipo PV ou PQ - Resíduo Potência Ativa
        if value["tipo"] != 2:
            powerflow.deltaP[idx] += powerflow.pqsch["potencia_ativa_especificada"][idx]
            powerflow.deltaP[idx] -= pcalc(
                powerflow,
                idx,
            )

        # Tipo PQ - Resíduo Potência Reativa
        if (
            ("QLIM" in powerflow.control)
            or ("QLIMs" in powerflow.control)
            or ("QLIMn" in powerflow.control)
            or (value["tipo"] == 0)
        ):
            powerflow.deltaQ[idx] += powerflow.pqsch["potencia_reativa_especificada"][
                idx
            ]
            powerflow.deltaQ[idx] -= qcalc(
                powerflow,
                idx,
            )

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)

    # Resíduos de variáveis de estado de controle
    if powerflow.controlcount > 0:
        controlres(
            powerflow,
        )
        powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)
    else:
        powerflow.deltaY = array([0])