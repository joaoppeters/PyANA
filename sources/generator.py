# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import array, cos, diag, ones, pi, sin


def md01(
    powerflow,
    gen,
    value2,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.generator[gen].append("MD01")
    powerflow.generator[gen].append(value2["inercia"].values[0])
    powerflow.generator[gen].append(value2["amortecimento"].values[0])
    powerflow.generator[gen].append(value2["l-transitoria"].values[0] * 2 * pi * 1)
    powerflow.generator[gen].append(value2["r-armadura"].values[0])


def md01newt(
    powerflow,
    Yr,
    x0,
    generator,
    gen,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.deltagen[gen] = powerflow.solution["x"][gen] - x0[gen] - powerflow.dsimDF.step.values[0] * 0.5 * (powerflow.solution["x"][gen + powerflow.nger] + x0[gen + powerflow.nger])
    powerflow.deltagen[gen + powerflow.nger] = powerflow.solution["x"][gen + powerflow.nger] - x0[gen + powerflow.nger] - powerflow.dsimDF.step.values[0] * 0.5 * ((pi * 1 / powerflow.generator[generator][1]) * (2 * powerflow.solution["active"][gen - 1] * 1e-2 - md01peut(powerflow, Yr, powerflow.solution["x"], gen,) - md01peut(powerflow, Yr, x0, gen,) - powerflow.generator[generator][2] * (powerflow.solution["x"][gen + powerflow.nger] + x0[gen + powerflow.nger])))


def md01peut(
    powerflow,
    Yr,
    x,
    gen,
):
    """
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    return powerflow.solution["fem"][gen] * array([powerflow.solution["fem"][j] * (Yr[gen, j].real * cos(x[gen] - x[j]) + Yr[gen, j].imag * sin(x[gen] - x[j])) for j in range(powerflow.nger)]).sum()


def md01jacob(
    powerflow,
    generator,
    gen,
    A1,
    A2,
    A3,
    A4,
    Yr,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    A1[gen, gen] = 1
    A2[gen, gen] = -powerflow.dsimDF.step.values[0] * 0.5
    A4[gen, gen] = 1 + powerflow.dsimDF.step.values[0] * 0.5 * (pi * 1 / powerflow.generator[generator][1]) * powerflow.generator[generator][2]

    for j in range(0, powerflow.nger):
        if gen != j:
            A3[gen, j] = powerflow.dsimDF.step.values[0] * 0.5 * (pi * 1 / powerflow.generator[generator][1]) * powerflow.solution["fem"][gen] * powerflow.solution["fem"][j] * (-Yr[gen, j].real * sin(powerflow.solution["x"][gen] - powerflow.solution["x"][j]) + Yr[gen, j].imag * cos(powerflow.solution["x"][gen] - powerflow.solution["x"][j]))
        A3[gen, j] -= A3[gen, j]