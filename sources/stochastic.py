# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib.pyplot import axis, close, figure, hist, plot, scatter, show, title
from numpy import (
    abs,
    array,
    exp,
    linspace,
    mean,
    nonzero,
    pi,
    sqrt,
    std,
    sum,
    random,
    where,
)


def stoch_individualized(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = 1e-2 * powerflow.dbarDF.demanda_ativa.sum()
    qtload0 = 1e-2 * powerflow.dbarDF.demanda_reativa.sum()

    mean_active = 1e-2 * powerflow.dbarDF["demanda_ativa"].values
    var_active = mean_active * 0.2
    mean_reactive = 1e-2 * powerflow.dbarDF["demanda_reativa"].values
    var_reactive = mean_reactive * 0.2

    points = 50
    pop = []
    qop = []

    for idx, value in enumerate(powerflow.maskpL):
        if value:
            x = linspace(
                mean_active[idx] - 5 * var_active[idx],
                mean_active[idx] + 5 * var_active[idx],
                points,
            )
            y = (1 / (sqrt(2 * pi) * var_active[idx])) * exp(
                -((x - mean_active[idx]) ** 2) / (2 * var_active[idx] ** 2)
            )

            ptload = ptload0 - powerflow.dbarDF["demanda_ativa"].values[idx] * 1e-2 + x

            for p in ptload:
                pop.append(p)

    for idx, value in enumerate(powerflow.maskqL):
        if value:
            x = linspace(
                mean_reactive[idx] - 5 * var_reactive[idx],
                mean_reactive[idx] + 5 * var_reactive[idx],
                points,
            )
            y = (1 / (sqrt(2 * pi) * var_reactive[idx])) * exp(
                -((x - mean_reactive[idx]) ** 2) / (2 * var_reactive[idx] ** 2)
            )

            qtload = (
                qtload0 - powerflow.dbarDF["demanda_reativa"].values[idx] * 1e-2 + x
            )

            for q in qtload:
                qop.append(q)

    figure(1)
    op = convolution(pop, qop)
    for (x, y) in op:
        scatter(x, y)

    show()
    print()


def stoch_generalized(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = sum(array(powerflow.dbarDF["demanda_ativa"].to_list()) * 1e-2)
    qtload0 = sum(array(powerflow.dbarDF["demanda_reativa"].to_list()) * 1e-2)

    mean = [ptload0, qtload0]
    cov = [[0.1, 0], [0, 0.1]]

    x, y = random.multivariate_normal(mean=mean, cov=cov, size=1000).T

    figure(4)
    scatter(x, y, alpha=0.5)
    axis("equal")
    show()

    print()


def convolution(list1, list2):
    """
    Convolute two lists of floats into a single list of tuples.

    Args:
    list1: First list containing floats.
    list2: Second list containing floats.

    Returns:
    List of tuples representing all possible combinations of floats from input lists.
    """
    result = []
    for item1 in list1:
        for item2 in list2:
            result.append((item1, item2))
    return result
