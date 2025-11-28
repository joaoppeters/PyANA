# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import append, array, concatenate, cos, pi, sin, zeros


def postflow(
    anatem,
):
    """

    Args
        anatem:
    """
    ## Inicialização
    Ya = zeros([anatem.nger, anatem.nger], dtype=complex)
    Yb = zeros([anatem.nger, anatem.nbus], dtype=complex)
    Yd = zeros([anatem.nbus, anatem.nbus], dtype=complex)

    anatem.generator = dict()
    for idx, value in anatem.dmaqDF.iterrows():
        gen = anatem.dbarDF.loc[
            anatem.dbarDF["numero"] == value["numero"], "numero"
        ].values[0]
        anatem.generator[gen] = list()
        dmdg = anatem.dmdgDF.loc[anatem.dmdgDF["numero"] == value["gerador"]]
        if dmdg.tipo.values[0] == "MD01":
            md01(
                anatem,
                gen,
                dmdg,
            )

            Ya[idx, idx] = 1 / (1j * anatem.generator[gen][3])
            Yb[idx, value["numero"] - 1] = -1 / (1j * anatem.generator[gen][3])
            Yd[value["numero"] - 1, value["numero"] - 1] += 1 / (
                1j * anatem.generator[gen][3]
            )

    anatem.Yblc = concatenate(
        (
            concatenate((Ya, Yb), axis=1),
            concatenate((Yb.T, anatem.Yb + Yd), axis=1),
        ),
        axis=0,
    )


def md01(
    anatem,
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
        anatem:
        gen: indice do gerador
        dmdg: informacoes obtidas do dmdgDF
    """
    ## Inicialização
    anatem.generator[gen].append("MD01")
    anatem.generator[gen].append(
        dmdg["inercia"].values[0] / (pi * anatem.options["FBSE"])
    )
    anatem.generator[gen].append(dmdg["amortecimento"].values[0])
    anatem.generator[gen].append(
        dmdg["l-transitoria"].values[0] * 2 * pi * anatem.options["FBSE"]
    )
    anatem.generator[gen].append(dmdg["r-armadura"].values[0])


# def md01peut(
#     anatem,
#     delta,
#     gen,
# ):
#     """equação de potência eletrica do modelo clássico do gerador

#     Args
#         anatem:
#     """

#     ## Inicialização
#     return (
#         anatem.solution["fem"][gen]
#         * array(
#             [
#                 anatem.solution["fem"][j]
#                 * (
#                     Yred[gen, j].imag * sin(delta[gen] - delta[j])
#                     + Yred[gen, j].real * cos(delta[gen] - delta[j])
#                 )
#                 for j in range(anatem.nger)
#             ]
#         ).sum()
#     )
