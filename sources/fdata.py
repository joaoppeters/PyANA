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

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    ## ESTADOS NORTE DO BRASIL: AC, AP, AM, PA, TO, RO, RR
    ## ESTADOS NORDESTE DO BRASIL: AL, BA, CE, MA, PB, PE, PI, RN, SE
    ## ESTADOS CENTRO-OESTE DO BRASIL: DF, GO, MS, MT
    ## ESTADOS SUDESTE DO BRASIL: ES, MG, RJ, SP
    ## ESTADOS SUL DO BRASIL: PR, RS, SC

    # SLACKS
    slack = powerflow.dbarraDF.loc[powerflow.dbarraDF["tipo"] == 2]

    # UHEs
    uhe = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("UHE")]
    uhegbt = uhe["grupo_base_tensao"].unique()
    uhegbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(uhegbt)
    ].reset_index(drop=True)
    uhegbtvalue["quantidade"] = uhe["grupo_base_tensao"].value_counts().to_list()

    # UTEs
    ute = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("UTE")]
    utegbt = ute["grupo_base_tensao"].unique()
    utegbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(utegbt)
    ].reset_index(drop=True)
    utegbtvalue["quantidade"] = ute["grupo_base_tensao"].value_counts().to_list()

    # EOLs
    eol = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("EOL")]
    eolgbt = eol["grupo_base_tensao"].unique()
    eolgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(eolgbt)
    ].reset_index(drop=True)
    eolgbtvalue["quantidade"] = eol["grupo_base_tensao"].value_counts().to_list()

    # PCHs
    pch = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("PCH")]
    pchgbt = pch["grupo_base_tensao"].unique()
    pchgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(pchgbt)
    ].reset_index(drop=True)
    pchgbtvalue["quantidade"] = pch["grupo_base_tensao"].value_counts().to_list()

    # UFVs
    ufv = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("UFV")]
    ufvgbt = ufv["grupo_base_tensao"].unique()
    ufvgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(ufvgbt)
    ].reset_index(drop=True)
    ufvgbtvalue["quantidade"] = ufv["grupo_base_tensao"].value_counts().to_list()

    # BIOs
    # bio = powerflow.dbarraDF.loc[powerflow.dbarraDF["nome"].str.contains("BIO")]
    # biogbt = ufv["grupo_base_tensao"].unique()
    # biogbtvalue = powerflow.dgbtDF.loc[
    #     powerflow.dgbtDF["grupo"].isin(biogbt)
    # ].reset_index(drop=True)
    # biogbtvalue["quantidade"] = bio["grupo_base_tensao"].value_counts().to_list()

    # DGBTs
    gbt = powerflow.dbarraDF["grupo_base_tensao"].unique()
    gbtvalue = powerflow.dgbtDF.loc[powerflow.dgbtDF["grupo"].isin(gbt)].reset_index(
        drop=True
    )
    gbtvalue["quantidade"] = (
        powerflow.dbarraDF["grupo_base_tensao"].value_counts().to_list()
    )

    # DAREs
    area = powerflow.dbarraDF["area"].unique()
    areavalue = powerflow.dareaDF.loc[
        powerflow.dareaDF["numero"].isin(area)
    ].reset_index(drop=True)
    areavalue["quantidade"] = powerflow.dbarraDF["area"].value_counts().to_list()

    # 500 kV, 230 kV, 138 kV, 69 kV,ßß
    trans = sorted(
        powerflow.dgbtDF.loc[
            (
                (powerflow.dgbtDF["tensao"] >= 138.0)
                & (powerflow.dgbtDF["tensao"] <= 800.0)
            ),
            "grupo",
        ]
    )
    transmissao = powerflow.dbarraDF.query("grupo_base_tensao in @trans").reset_index(
        drop=True
    )

    #
    dist = sorted(
        powerflow.dgbtDF.loc[
            (
                (powerflow.dgbtDF["tensao"] >= 6.9)
                & (powerflow.dgbtDF["tensao"] < 138.0)
            ),
            "grupo",
        ]
    )
    distribuicao = powerflow.dbarraDF.query("grupo_base_tensao in @dist").reset_index(
        drop=True
    )

    #
    fic = sorted(
        powerflow.dgbtDF.loc[
            ((powerflow.dgbtDF["tensao"] > 900) | (powerflow.dgbtDF["tensao"] < 6.9)),
            "grupo",
        ]
    )
    ficticia = powerflow.dbarraDF.query("grupo_base_tensao in @fic").reset_index(
        drop=True
    )

    print("Total de barramentos: ", powerflow.nbus)
    print("Transmissao: ", transmissao.shape[0])
    print("Distribuicao: ", distribuicao.shape[0])
    print("Ficticia: ", ficticia.shape[0])

    print()

    print("UHEs: ", uhe.shape[0])
    print("UHEs GBTs: ", uhegbtvalue)

    print()

    print("UTEs: ", ute.shape[0])
    print("UTEs GBTs: ", utegbtvalue)

    print()

    print("EOLs: ", eol.shape[0])
    print("EOLs GBTs: ", eolgbtvalue)

    print()

    print("PCHs: ", pch.shape[0])
    print("PCHs GBTs: ", pchgbtvalue)

    print()

    print("UFVs: ", ufv.shape[0])
    print("UFVs GBTs: ", ufvgbtvalue)

    # print()

    # print("BIOs: ", bio.shape[0])
    # print("BIOs GBTs: ", biogbtvalue)

    print()

    print("GBTs: ", gbtvalue)

    print()

    print("Areas: ", areavalue)
