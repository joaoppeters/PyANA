# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import matplotlib.pyplot as plt
from numpy import (
    arccos,
    arctan,
    clip,
    cos,
    exp,
    eye,
    linalg,
    linspace,
    ones,
    pi,
    sin,
    sqrt,
    sum,
    random,
    zeros,
)
import pandas as pd
import random as rd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.stats import beta
import seaborn as sns


def stocharou(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    # ACTIVE DEMAND
    nsamples = 5000

    pmean = powerflow.dbarDF.demanda_ativa[powerflow.dbarDF.demanda_ativa > 0].sum()
    pstddev = 0.06 * pmean
    x = linspace(pmean - 4 * pstddev, pmean + 4 * pstddev, nsamples)

    pdf = (1 / (pstddev * sqrt(2 * pi))) * exp(-0.5 * ((x - pmean) / pstddev) ** 2)

    psamples = random.normal(pmean, pstddev, nsamples)

    # # Plot the PDF
    # plt.figure(1, figsize=(10, 6))
    # # plt.plot(x, pdf, "r", label="Theoretical PDF")
    # plt.hist(psamples, bins=500, density=True, alpha=0.6, color="b")
    # plt.xlabel('Total Active Demand', fontsize=18)
    # plt.ylabel('Probability Density', fontsize=18)
    # plt.savefig("C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\active_demand.pdf", dpi=500)


    # WIND POWER
    # shape = 8.46
    # scale = 3.18

    # wdata = powerflow.dbarDF[powerflow.dbarDF['nome'].str.contains('EOL')]["potencia_ativa"].reset_index()
    # neol = wdata.shape[0]

    # vci = 3
    # vco = 25
    # vrd = 15
    # wscaled = dict()
    # wpower = dict()
    # pwtotal = zeros(nsamples)

    # for eol in range(0, neol):
    #     wsamples = random.weibull(scale, nsamples)
    #     wscaled[eol] = wsamples * shape
    #     wpower[eol] = zeros(nsamples)

    # for i in range(0, nsamples):
    #     for j in range(0, neol):
    #         if wscaled[j][i] < vci or wscaled[j][i] > vco:
    #             wpower[j][i] = 0
    #         elif wscaled[j][i] >= vci and wscaled[j][i] <= vrd:
    #             wpower[j][i] = wdata.iloc[j].potencia_ativa * (wscaled[j][i] - vci) / (vrd - vci)
    #         else:
    #             wpower[j][i] = wdata.iloc[j].potencia_ativa

    #         pwtotal[i] += wpower[j][i]

    
    # plt.figure(2, figsize=(10, 6))
    # plt.hist(pwtotal, bins=500, density=True, alpha=0.6, color="g")
    # plt.xlabel('Total Wind Power Generation', fontsize=18)
    # plt.ylabel('Probability Density', fontsize=18)
    # plt.savefig("C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas\\eolic_power.pdf", dpi=500)
    return psamples, 1


def stoch_apparent_1(
    powerflow,
):
    """analise de pontos de operacao pela potencia aparente total demandada pelo sistema

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = 1e-2 * powerflow.dbarDF.demanda_ativa.sum()
    qtload0 = 1e-2 * powerflow.dbarDF.demanda_reativa.sum()

    stload0 = sqrt(ptload0**2 + qtload0**2)
    powerfactor = arccos(ptload0 / stload0)

    mean = stload0
    stdd = mean * 0.2  # mean - 5*stdd > 0

    points = 100

    x = linspace(
        mean - 5 * stdd,
        mean + 5 * stdd,
        points,
    )

    y = (1 / (sqrt(2 * pi) * stdd)) * exp(-((x - mean) ** 2) / (2 * stdd**2))

    ## Distribuicao de cargas
    plt.figure(1)
    plt.scatter(x, y)
    plt.title("Load Distribution (%d points)" % points)
    plt.xlabel("Total Apparent Power Demand (MVA)")
    plt.ylabel("Probability Density")

    ## Redistribuicao por fator de potencia
    p = x * cos(powerfactor)
    q = x * sin(powerfactor)

    plt.figure(2)
    plt.title("Power Factor Redistribution of Loads (%d points)" % points)
    plt.scatter(p, q)
    plt.xlabel("Total Active Power Demand (MW)")
    plt.ylabel("Total Reactive Power Demand (Mvar)")

    ## Redistribuicao por fator de potencia e convolucao entre pontos
    p, q = convolution(p, q)

    plt.figure(3)
    plt.title("Convolution of Active and Reactive Power Demands (%d points)" % len(p))
    plt.scatter(p, q)
    plt.xlabel("Total Active Power Demand (MW)")
    plt.ylabel("Total Reactive Power Demand (Mvar)")


def stoch_apparent_2(
    powerflow,
):
    """analise de pontos de operacao pela potencia aparente demandada por cada barra do sistema

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    pload0 = 1e-2 * powerflow.dbarDF.demanda_ativa.values
    qload0 = 1e-2 * powerflow.dbarDF.demanda_reativa.values

    ptload = sum(pload0)
    ptl = []
    qtload = sum(qload0)
    qtl = []

    sload0 = sqrt(pload0**2 + qload0**2)
    stload = sum(sload0)
    stl = []
    powerfactor = arccos(pload0 / sload0)
    maskLs = sload0 > 0

    points = 100

    for idx, value in enumerate(maskLs):
        if value:
            mean = sload0[idx]
            stdd = mean * 0.2  # mean - 5*stdd > 0

            x = linspace(
                mean - 5 * stdd,
                mean + 5 * stdd,
                points,
            )

            y = (1 / (sqrt(2 * pi) * stdd)) * exp(-((x - mean) ** 2) / (2 * stdd**2))

            ## Distribuicao de cargas
            plt.figure(4)
            plt.scatter(x, y, label="Bus %d" % (idx + 1))
            plt.title("Load Distribution per Bus (%d points)" % points)
            plt.xlabel("Apparent Power Demand (MVA) per Bus")
            plt.ylabel("Probability Density")
            plt.legend()

            ## Redistribuicao por fator de potencia
            p = x * cos(powerfactor[idx])
            q = x * sin(powerfactor[idx])

            plt.figure(5)
            plt.title(
                "Power Factor Redistribution of Loads per Bus (%d points)" % points
            )
            plt.scatter(p, q, label="Bus %d" % (idx + 1))
            plt.xlabel("Active Power Demand (MW) per Bus")
            plt.ylabel("Reactive Power Demand (Mvar) per Bus")
            plt.legend()

            ## Redistribuicao por fator de potencia e convolucao entre pontos
            p = ptload - pload0[idx] + p  # 100 points each
            q = qtload - qload0[idx] + q  # 100 points each
            p, q = convolution(p, q)  # 10000 points each
            ptl.extend(p)
            qtl.extend(q)

            plt.figure(6)
            plt.title(
                "Convolution of Active and Reactive Power Demand per Bus (%d points)"
                % len(p)
            )
            plt.scatter(p, q, label="Bus %d" % (idx + 1))
            plt.xlabel("Active Power Demand (MW) per Bus")
            plt.ylabel("Reactive Power Demand (Mvar) per Bus")
            plt.legend()

    plt.figure(7)
    plt.title(
        "Convolution of Total Active and Reactive Power Demand (%d points)" % len(ptl)
    )
    plt.scatter(ptl, qtl)
    plt.xlabel("Active Power Demand (MW)")
    plt.ylabel("Reactive Power Demand (Mvar)")


def stoch_apparent_3(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    pload = 1e-2 * powerflow.dbarDF.demanda_ativa.values
    qload = 1e-2 * powerflow.dbarDF.demanda_reativa.values

    active_mean = 1e-2 * powerflow.dbarDF.demanda_ativa.mean()
    active_stdd = 1e-2 * powerflow.dbarDF.demanda_ativa.std()
    active_factor = pload / active_mean

    reactive_mean = 1e-2 * powerflow.dbarDF.demanda_reativa.mean()
    reactive_stdd = 1e-2 * powerflow.dbarDF.demanda_reativa.std()
    reactive_factor = qload / reactive_mean

    pl = []
    ql = []

    points = 100

    xp = linspace(active_mean - 5 * active_stdd, active_mean + 5 * active_stdd, points)
    yp = (1 / (sqrt(2 * pi) * active_stdd)) * exp(
        -((xp - active_mean) ** 2) / (2 * active_stdd**2)
    )

    for x in xp:
        pl.extend(x * active_factor)
        ql.extend(reactive_mean * ones(powerflow.nbus))

    plt.figure(8)
    plt.scatter(pl, ql)

    pl = []
    ql = []

    xq = linspace(
        reactive_mean - 5 * reactive_stdd, reactive_mean + 5 * reactive_stdd, points
    )
    yq = (1 / (sqrt(2 * pi) * reactive_stdd)) * exp(
        -((xq - reactive_mean) ** 2) / (2 * reactive_stdd**2)
    )

    for x in xq:
        pl.extend(active_mean * ones(powerflow.nbus))
        ql.extend(x * reactive_factor)

    plt.figure(9)
    plt.scatter(pl, ql)

    xp = linspace(pload.sum() - 5 * active_stdd, pload.sum() + 5 * active_stdd, points)
    xq = linspace(
        qload.sum() - 5 * reactive_stdd, qload.sum() + 5 * reactive_stdd, points
    )

    pl, ql = convolution(xp, xq)

    plt.figure(10)
    plt.scatter(pl, ql)
    plt.title("Power Factor Redistribution of Loads (%d points)" % len(pl))
    plt.xlabel("Total Active Power Demand (MW)")
    plt.ylabel("Total Reactive Power Demand (Mvar)")


def multivariate_normal(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = sum(1e-2 * powerflow.dbarDF.demanda_ativa.values)
    qtload0 = sum(1e-2 * powerflow.dbarDF.demanda_reativa.values)

    mean = [ptload0, qtload0]
    cov = [[0.1, 0], [0, 0.1]]
    points = 1000
    y = 1

    x, y = random.multivariate_normal(mean=mean, cov=cov, size=points).T

    plt.figure(11)
    plt.scatter(x, y, alpha=0.5)
    plt.axis("equal")

    df = pd.DataFrame(
        {
            "x": x,
            "y": y,
        }
    )
    z = linkage(df, method="ward", metric="euclidean")
    df["cluster"] = fcluster(z, 4, criterion="maxclust")

    # Plot the dendrogram
    plt.figure(12, figsize=(10, 5))
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample Index")
    plt.ylabel("Distance")
    dendrogram(
        z,
        leaf_rotation=90.0,
        leaf_font_size=8.0,
    )

    plt.figure(13)
    sns.scatterplot(x="x", y="y", hue="cluster", data=df)
    plt.axis("equal")


def rand0m(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    random.seed(1)

    ptload0 = 1e-2 * powerflow.dbarDF.demanda_ativa.sum()
    qtload0 = 1e-2 * powerflow.dbarDF.demanda_reativa.sum()

    central_point = (ptload0, qtload0)
    stdd = 0.1
    points = 1000

    random_points = generate_random_points_normal(central_point, stdd, points)
    x_coords, y_coords = zip(*random_points)

    plt.figure(
        14,
    )
    plt.scatter(x_coords, y_coords, color="blue", s=10, alpha=0.5)
    plt.scatter(
        central_point[0],
        central_point[1],
        color="red",
        marker="x",
        s=10,
        label="Central Point",
    )
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Random Points Following Normal Distribution")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")  # Equal aspect ratio for better visualization

    plt.show()


def convolution(list1, list2):
    """
    Convolute two lists of floats into a single list of tuples.

    Args:
    list1: First list containing floats.
    list2: Second list containing floats.

    Returns:
    List of tuples representing all possible combinations of floats from input lists.
    """
    x = []
    y = []
    for item1 in list1:
        for item2 in list2:
            x.append(item1)
            y.append(item2)
    return x, y


# Define a function to remove superposed points
def remove_superposed_points(points, threshold):
    unique_points = []
    for point in points:
        if not any(
            linalg.norm(point - existing_point) < threshold
            for existing_point in unique_points
        ):
            unique_points.append(point)
    return unique_points[0], unique_points[1]


def generate_random_points_normal(center, std_dev, num_points):
    random_points = []
    for _ in range(num_points):
        # Generate random offsets following normal distribution
        offset_x = rd.gauss(0, std_dev)
        offset_y = rd.gauss(0, std_dev)

        # Apply offsets to central point
        random_point = (center[0] + offset_x, center[1] + offset_y)
        random_points.append(random_point)
    return random_points
