# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib.pyplot import axis, close, figure, hist, plot, scatter, show, title
from numpy import abs, array, exp, mean, nonzero, pi, sqrt, std, sum, random, where


def stoch1(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # random.seed(1)

    ptload0 = sum(array(powerflow.dbarraDF["demanda_ativa"].to_list()) * 1e-2)
    qtload0 = sum(array(powerflow.dbarraDF["demanda_reativa"].to_list()) * 1e-2)

    idx_pload_bus = nonzero(array(powerflow.dbarraDF["demanda_ativa"].to_list()))
    mup = array(powerflow.dbarraDF["demanda_ativa"].to_list()) * 1e-2
    mup = mup[where(mup != 0)]
    sigmap = [10e-2 if all(mup - 0.5 > 0) else (mup * 0.2)]

    idx_qload_bus = nonzero(array(powerflow.dbarraDF["demanda_reativa"].to_list()))
    muq = array(powerflow.dbarraDF["demanda_reativa"].to_list()) * 1e-2
    muq = muq[where(muq != 0)]
    sigmaq = [10e-2 if (all(muq - 0.5 > 0) or all(muq + 0.5 < 0)) else abs(muq * 0.2)]

    operative_points = {}
    idx_op = 1
    points = 1000

    for idx, value in enumerate(mup):
        figure(1)
        count, bins, ignored = hist(
            random.normal(mup[idx - 1], sigmap[idx - 1], points), 100, density=True
        )

        ptload = (
            ptload0
            - array(powerflow.dbarraDF["demanda_ativa"].to_list())[
                idx_pload_bus[0][idx]
            ]
            * 1e-2
            + bins
        )

        for valueptl in ptload:
            operative_points[idx_op] = (valueptl, qtload0)
            idx_op += 1

    for idx, value in enumerate(muq):
        figure(2)
        count, bins, ignored = hist(
            random.normal(muq[idx - 1], sigmaq[idx - 1], points), 100, density=True
        )

        qtload = (
            qtload0
            - array(powerflow.dbarraDF["demanda_reativa"].to_list())[
                idx_qload_bus[0][idx]
            ]
            * 1e-2
            + bins
        )

        for valueqtl in qtload:
            operative_points[idx_op] = (ptload0, valueqtl)
            idx_op += 1

    figure(3)
    for i in operative_points:
        (x, y) = operative_points.get(i)
        scatter(x, y)

    print()


def stoch2(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = sum(array(powerflow.dbarraDF["demanda_ativa"].to_list()) * 1e-2)
    qtload0 = sum(array(powerflow.dbarraDF["demanda_reativa"].to_list()) * 1e-2)

    mean = [ptload0, qtload0]
    cov = [[0.1, 0], [0, 0.1]]

    x, y = random.multivariate_normal(mean=mean, cov=cov, size=1000).T

    figure(4)
    scatter(x, y, alpha=0.5)
    axis("equal")
    show()

    print()
