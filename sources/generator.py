# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import append, array, concatenate, cos, pi, sin, zeros


def postflow(
    powerflow,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    Ya = zeros([powerflow.nger, powerflow.nger], dtype=complex)
    Yb = zeros([powerflow.nger, powerflow.nbus], dtype=complex)
    Yd = zeros([powerflow.nbus, powerflow.nbus], dtype=complex)

    powerflow.generator = dict()
    for idx, value in powerflow.dmaqDF.iterrows():
        gen = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "numero"
        ].values[0]
        powerflow.generator[gen] = list()
        dmdg = powerflow.dmdgDF.loc[powerflow.dmdgDF["numero"] == value["gerador"]]
        if dmdg.tipo.values[0] == "MD01":
            md01(
                powerflow,
                gen,
                dmdg,
            )

            Ya[idx, idx] = 1 / (1j * powerflow.generator[gen][3])
            Yb[idx, value["numero"] - 1] = -1 / (1j * powerflow.generator[gen][3])
            Yd[value["numero"] - 1, value["numero"] - 1] += 1 / (
                1j * powerflow.generator[gen][3]
            )

    powerflow.Yblc = concatenate(
        (
            concatenate((Ya, Yb), axis=1),
            concatenate((Yb.T, powerflow.Yb + Yd), axis=1),
        ),
        axis=0,
    )


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

    Args
        powerflow: self do arquivo powerflow.py
        gen: indice do gerador
        dmdg: informacoes obtidas do dmdgDF
    """

    ## Inicialização
    powerflow.generator[gen].append("MD01")
    powerflow.generator[gen].append(
        dmdg["inercia"].values[0] / (pi * powerflow.options["FBASE"])
    )
    powerflow.generator[gen].append(dmdg["amortecimento"].values[0])
    powerflow.generator[gen].append(
        dmdg["l-transitoria"].values[0] * 2 * pi * powerflow.options["FBASE"]
    )
    powerflow.generator[gen].append(dmdg["r-armadura"].values[0])


# def md01peut(
#     powerflow,
#     delta,
#     gen,
# ):
#     """equação de potência eletrica do modelo clássico do gerador

#     Args
#         powerflow: self do arquivo powerflow.py
#     """

#     ## Inicialização
#     return (
#         powerflow.solution["fem"][gen]
#         * array(
#             [
#                 powerflow.solution["fem"][j]
#                 * (
#                     Yred[gen, j].imag * sin(delta[gen] - delta[j])
#                     + Yred[gen, j].real * cos(delta[gen] - delta[j])
#                 )
#                 for j in range(powerflow.nger)
#             ]
#         ).sum()
#     )
