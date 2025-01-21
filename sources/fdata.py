# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def fdata(
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    sp = [
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        209,
        210,
        211,
        212,
        213,
        214,
        215,
        216,
        217,
    ]
    pl = list()
    for idx, value in powerflow.dbarDF.iterrows():
        if value.area in sp:
            pl.append(value.demanda_ativa)

    print(sum(pl))

    # pg = list()
    # for idx, value in powerflow.dgerDF.iterrows():
    #     pg.append(powerflow.dbarDF[powerflow.dbarDF.numero == value.numero].potencia_ativa.values[0])

    # pgtotal = sum(pg)

    # print(pg, pgtotal)
    # barra_area = powerflow.dbarDF.loc[powerflow.dbarDF.area == 1, "numero"].tolist()
    # area = powerflow.dbarDF.loc[powerflow.dbarDF.area == 1, "numero"].tolist()
    # print(barra_area, len(barra_area))

    # for idx, value in powerflow.dlinDF.iterrows():
    #     # if (value.de in barra_area and value.para not in barra_area) or (
    #     #     value.de not in barra_area and value.para in barra_area
    #     # ):

    #     if ((value.de in barra_area) and (value.para not in barra_area)) or ((value.para in barra_area) and (value.de not in barra_area)):
    #     # if ((value.de in barra_area)) or ((value.para in barra_area)):
    #         print(value.de, value.para, powerflow.dbarDF.loc[value.de == powerflow.dbarDF.numero, "area"].values[0], powerflow.dbarDF.loc[value.para == powerflow.dbarDF.numero, "area"].values[0])
    #         # if value.de in area or value.para in area:
    #         #     # print(value.de, value.para)
    #         #     try:
    #         #         area.remove(value.de)
    #         #     except:
    #         #         area.remove(value.para)
