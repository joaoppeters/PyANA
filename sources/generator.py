# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import append, array, concatenate, cos, pi, sin, zeros


def md01(
    powerflow,
    gen,
    dmdg,
):
    """armazenamento de dados dos geradores
    Posicao 0: modelo do gerador - de acordo com ANATEM
    Posicao 1: inercia (M)
    Posicao 2: amortecimento (D)
    Posicao 3: reatancia transitoria
    Posicao 4: resistencia

    Parâmetros
        powerflow: self do arquivo powerflow.py
        gen: indice do gerador
        dmdg: informacoes obtidas do dmdgDF
    """

    ## Inicialização
    powerflow.generator[gen].append("MD01")
    powerflow.generator[gen].append(
        dmdg["inercia"].values[0] / (powerflow.options["FBASE"] * pi)
    )
    powerflow.generator[gen].append(dmdg["amortecimento"].values[0])
    powerflow.generator[gen].append(
        dmdg["l-transitoria"].values[0] * 2 * pi * powerflow.options["FBASE"]
    )
    powerflow.generator[gen].append(dmdg["r-armadura"].values[0])


def md01residue(
    powerflow,
    Yred,
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
            - md01peut(powerflow, Yred, powerflow.solution["delta"], gen)
            - md01peut(powerflow, Yred, powerflow.solution["delta0"], gen)
            - powerflow.generator[generator][2] * powerflow.solution["omega"][gen]
            - powerflow.generator[generator][2] * powerflow.solution["omega0"][gen]
        )
    )


def md01peut(
    powerflow,
    Yred,
    delta,
    gen,
):
    """equação de potência eletrica do modelo clássico do gerador

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    return (
        powerflow.solution["fem"][gen]
        * array(
            [
                powerflow.solution["fem"][j]
                * (
                    Yred[gen, j].imag * sin(delta[gen] - delta[j])
                    + Yred[gen, j].real * cos(delta[gen] - delta[j])
                )
                for j in range(powerflow.nger)
            ]
        ).sum()
    )


def md01jacob(
    powerflow,
    generator,
    gen,
    Yred,
):
    """matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    if gen == 0:
        powerflow.jacobiangen = zeros((2, 2))
        powerflow.jacobiangen[0, 0] = 1
        powerflow.jacobiangen[0, 1] = -powerflow.dsimDF.step.values[0] * 0.5
        powerflow.jacobiangen[1, 0] = (
            (
                powerflow.dsimDF.step.values[0]
                * 0.5
                * 1
                / powerflow.generator[generator][1]
            )
            * powerflow.solution["fem"][gen]
            * array(
                [
                    powerflow.solution["fem"][j]
                    * (
                        Yred[gen, j].imag
                        * cos(
                            powerflow.solution["delta"][gen]
                            - powerflow.solution["delta"][j]
                        )
                        - Yred[gen, j].real
                        * sin(
                            powerflow.solution["delta"][gen]
                            - powerflow.solution["delta"][j]
                        )
                    )
                    for j in range(powerflow.nger)
                ]
            ).sum()
        )
        powerflow.jacobiangen[1, 1] = (
            1
            + powerflow.dsimDF.step.values[0]
            * 0.5
            * powerflow.generator[generator][2]
            / powerflow.generator[generator][1]
        )

    else:
        powerflow.jacobiangen = concatenate(
            (powerflow.jacobiangen, zeros((powerflow.jacobiangen.shape[0], 2))), axis=1
        )
        powerflow.jacobiangen = concatenate(
            (powerflow.jacobiangen, zeros((2, powerflow.jacobiangen.shape[1]))), axis=0
        )

        powerflow.jacobiangen[2 * gen, 2 * gen] = 1
        powerflow.jacobiangen[2 * gen, 2 * gen + 1] = (
            -powerflow.dsimDF.step.values[0] * 0.5
        )
        powerflow.jacobiangen[2 * gen + 1, 2 * gen] = (
            (
                powerflow.dsimDF.step.values[0]
                * 0.5
                * 1
                / powerflow.generator[generator][1]
            )
            * powerflow.solution["fem"][gen]
            * array(
                [
                    powerflow.solution["fem"][j]
                    * (
                        Yred[gen, j].imag
                        * cos(
                            powerflow.solution["delta"][gen]
                            - powerflow.solution["delta"][j]
                        )
                        - Yred[gen, j].real
                        * sin(
                            powerflow.solution["delta"][gen]
                            - powerflow.solution["delta"][j]
                        )
                    )
                    for j in range(powerflow.nger)
                ]
            ).sum()
        )
        powerflow.jacobiangen[2 * gen + 1, 2 * gen + 1] = (
            1
            + powerflow.dsimDF.step.values[0]
            * 0.5
            * powerflow.generator[generator][2]
            / powerflow.generator[generator][1]
        )


def md01jacoboffblock(
    powerflow,
    Yred,
    generator,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    for i in range(powerflow.nger):
        for j in range(powerflow.nger):
            if j != i:
                powerflow.jacobiangen[2 * i + 1, 2 * j] = (
                    (
                        powerflow.dsimDF.step.values[0]
                        * 0.5
                        * 1
                        / powerflow.generator[generator[i]][1]
                    )
                    * powerflow.solution["fem"][i]
                    * powerflow.solution["fem"][j]
                    * (
                        Yred[i, j].real
                        * sin(
                            powerflow.solution["delta"][i]
                            - powerflow.solution["delta"][j]
                        )
                        - Yred[i, j].imag
                        * cos(
                            powerflow.solution["delta"][i]
                            - powerflow.solution["delta"][j]
                        )
                    )
                )
