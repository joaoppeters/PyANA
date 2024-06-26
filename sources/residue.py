# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import array, concatenate, conj, diag, exp, sin, zeros

from ctrl import controlres

# from generator import md01peut


def residue(
    powerflow,
    case: int = 0,
    stage: str = None,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    I = powerflow.Yb @ V
    S = diag(V) @ conj(I)

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

    if powerflow.solution["method"] == "EXIC":
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, array([0])), axis=0)

    powerflow.deltaPQY = powerflow.deltaPQY[powerflow.mask]

    # Resíduo de Fluxo de Potência Continuado
    # Condição de previsão
    if stage == "p":
        powerflow.deltaPQY = zeros(powerflow.deltaPQY.shape[0] + 1)
        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            if not powerflow.solution["pmc"]:
                powerflow.deltaPQY[-1] = powerflow.options["LMBD"] * (
                    5e-1 ** powerflow.solution["ndiv"]
                )

            elif powerflow.solution["pmc"]:
                powerflow.deltaPQY[-1] = (
                    -1
                    * powerflow.options["LMBD"]
                    * (5e-1 ** powerflow.solution["ndiv"])
                )

        elif powerflow.solution["varstep"] == "volt":
            powerflow.deltaPQY[-1] = (
                -1 * powerflow.options["ICMV"] * (5e-1 ** powerflow.solution["ndiv"])
            )

    # Condição de correção
    elif stage == "c":
        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            powerflow.deltaY = array(
                [powerflow.solution["stepsch"] - powerflow.solution["step"]]
            )

        elif powerflow.solution["varstep"] == "volt":
            powerflow.deltaY = array(
                [
                    powerflow.solution["vsch"]
                    - powerflow.solution["voltage"][powerflow.nodevarvolt]
                ]
            )

        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)


def md01residue(
    powerflow,
    generator,
    gen,
):
    """calculo dos residuos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.deltagen[2 * gen] = (
        powerflow.solution["delta"][gen]
        - powerflow.solution["delta0"][gen]
        - powerflow.dsimDF.step.values[0]
        * 0.5
        * (powerflow.solution["omega"][gen] + powerflow.solution["omega0"][gen])
    )

    powerflow.deltagen[2 * gen + 1] = (
        powerflow.solution["omega"][gen]
        - powerflow.solution["omega0"][gen]
        - (powerflow.dsimDF.step.values[0] * 0.5 / powerflow.generator[generator][1])
        * (
            2 * powerflow.solution["active"][generator - 1]
            - (
                powerflow.solution["fem"][gen]
                * powerflow.solution["voltage"][generator - 1]
                * sin(
                    powerflow.solution["delta"][gen]
                    - powerflow.solution["theta"][generator - 1]
                )
                / powerflow.generator[generator][3]
            )
            - (
                powerflow.solution["fem"][gen]
                * powerflow.solution["voltage"][generator - 1]
                * sin(
                    powerflow.solution["delta0"][gen]
                    - powerflow.solution["theta"][generator - 1]
                )
                / powerflow.generator[generator][3]
            )
            - powerflow.generator[generator][2] * powerflow.solution["omega"][gen]
            - powerflow.generator[generator][2] * powerflow.solution["omega0"][gen]
        )
    )


def resexsi(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    ev0 = concatenate((powerflow.solution["fem0"], powerflow.solution["voltage0"]), axis=0)
    dt0 = concatenate((powerflow.solution["delta0"], powerflow.solution["theta0"]), axis=0)
    V0 = ev0 * exp(1j * dt0)
    I0 = powerflow.Yblc.A @ V0
    S0 = diag(V0) @ conj(I0)

    ev = concatenate((powerflow.solution["fem"], powerflow.solution["voltage"]), axis=0)
    dt = concatenate((powerflow.solution["delta"], powerflow.solution["theta"]), axis=0)
    V = ev * exp(1j * dt)
    I = powerflow.Yblc.A @ V
    S = diag(V) @ conj(I)

    powerflow.deltagen[2 * powerflow.nger : 3 * powerflow.nger + powerflow.nbus] = S.real - S0.real
    powerflow.deltagen[3 * powerflow.nger + powerflow.nbus :] = S.imag - S0.imag
