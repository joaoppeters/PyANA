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
    anarede,
    case: int = 0,
    stage: str = None,
):
    """cálculo de resíduos das equações diferenciáveis

    Args
        anarede:
    """
    ## Inicialização
    # Vetores de resíduo
    V = anarede.solution["voltage"] * exp(1j * anarede.solution["theta"])
    I = anarede.Yb @ V
    S = diag(V) @ conj(I)

    # Resíduos de potência ativa e reativa
    anarede.deltaP = anarede.psch - S.real
    anarede.deltaQ = anarede.qsch - S.imag

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    anarede.deltaPQY = concatenate((anarede.deltaP, anarede.deltaQ), axis=0)

    # Resíduos de variáveis de estado de controle
    if anarede.controlcount > 0:
        controlres(
            anarede,
            case,
        )
        anarede.deltaPQY = concatenate((anarede.deltaP, anarede.deltaQ), axis=0)
        anarede.deltaPQY = concatenate((anarede.deltaPQY, anarede.deltaY), axis=0)
    else:
        anarede.deltaY = array([0])

    if anarede.solution["method"] == "EXIC":
        anarede.deltaPQY = concatenate((anarede.deltaPQY, array([0])), axis=0)

    anarede.deltaPQY = anarede.deltaPQY[anarede.mask]

    # Resíduo de Fluxo de Potência Continuado
    # Condição de previsão
    if stage == "p":
        anarede.deltaPQY = zeros(anarede.deltaPQY.shape[0] + 1)
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            if not anarede.solution["pmc"]:
                anarede.deltaPQY[-1] = anarede.cte["LMBD"] * (
                    5e-1 ** anarede.solution["ndiv"]
                )

            elif anarede.solution["pmc"]:
                anarede.deltaPQY[-1] = (
                    -1 * anarede.cte["LMBD"] * (5e-1 ** anarede.solution["ndiv"])
                )

        elif anarede.solution["varstep"] == "volt":
            anarede.deltaPQY[-1] = (
                -1 * anarede.cte["ICMV"] * (5e-1 ** anarede.solution["ndiv"])
            )

    # Condição de correção
    elif stage == "c":
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            anarede.deltaY = array(
                [anarede.solution["stepsch"] - anarede.solution["step"]]
            )

        elif anarede.solution["varstep"] == "volt":
            anarede.deltaY = array(
                [
                    anarede.solution["vsch"]
                    - anarede.solution["voltage"][anarede.nodevarvolt]
                ]
            )

        anarede.deltaPQY = concatenate((anarede.deltaPQY, anarede.deltaY), axis=0)


def md01residue(
    anarede,
    generator,
    gen,
):
    """calculo dos residuos

    Args
        anarede:
    """
    ## Inicialização
    anarede.deltagen[2 * gen] = (
        anarede.solution["delta"][gen]
        - anarede.solution["delta0"][gen]
        - anarede.dsimDF.step.values[0]
        * 0.5
        * (anarede.solution["omega"][gen] + anarede.solution["omega0"][gen])
    )

    anarede.deltagen[2 * gen + 1] = (
        anarede.solution["omega"][gen]
        - anarede.solution["omega0"][gen]
        - (anarede.dsimDF.step.values[0] * 0.5 / anarede.generator[generator][1])
        * (
            2 * anarede.solution["active"][generator - 1]
            - (
                anarede.solution["fem"][gen]
                * anarede.solution["voltage"][generator - 1]
                * sin(
                    anarede.solution["delta"][gen]
                    - anarede.solution["theta"][generator - 1]
                )
                / anarede.generator[generator][3]
            )
            - (
                anarede.solution["fem"][gen]
                * anarede.solution["voltage"][generator - 1]
                * sin(
                    anarede.solution["delta0"][gen]
                    - anarede.solution["theta"][generator - 1]
                )
                / anarede.generator[generator][3]
            )
            - anarede.generator[generator][2] * anarede.solution["omega"][gen]
            - anarede.generator[generator][2] * anarede.solution["omega0"][gen]
        )
    )


def resexsi(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    # Vetores de resíduo
    ev0 = concatenate((anarede.solution["fem0"], anarede.solution["voltage0"]), axis=0)
    dt0 = concatenate((anarede.solution["delta0"], anarede.solution["theta0"]), axis=0)
    V0 = ev0 * exp(1j * dt0)
    I0 = anarede.Yblc.A @ V0
    S0 = diag(V0) @ conj(I0)

    ev = concatenate((anarede.solution["fem"], anarede.solution["voltage"]), axis=0)
    dt = concatenate((anarede.solution["delta"], anarede.solution["theta"]), axis=0)
    V = ev * exp(1j * dt)
    I = anarede.Yblc.A @ V
    S = diag(V) @ conj(I)

    anarede.deltagen[2 * anarede.nger : 3 * anarede.nger + anarede.nbus] = (
        S.real - S0.real
    )
    anarede.deltagen[3 * anarede.nger + anarede.nbus :] = S.imag - S0.imag
