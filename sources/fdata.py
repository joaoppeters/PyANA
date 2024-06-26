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

    # cargas = powerflow.dbarDF[powerflow.dbarDF.tipo == 0]
    # cargas = cargas.groupby("area")['area'].count()

    bus = list()
    for idx, value in powerflow.dgerDF.iterrows():
        nome = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "nome"
        ].values[0]
        area = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "area"
        ].values[0]
        if "UHE" in nome:
            bus.append((nome, value["numero"], area))
            # print(value["numero"], nome, area)

    bus.sort()
    for i in bus:
        print(i)

    i = 1
    pgtotal = 0
    bus = [
        "3IRMAOUHE",
        "CAPIVAUHE",
        "ESTREIUHE",
        "FURNASUHE",
        "I.SOLTUHE",
        "ITUMBIUHE",
        "JUPI--UHE",
        "JUPI--UHE",
        "MARIMBUHE",
        "PCOLOMUHE",
        "TAQUARUHE",
        "V.GRD-UHE",
    ]
    for idx, value in powerflow.dgerDF.iterrows():
        pg = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "potencia_ativa"
        ].values[0]
        nome = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "nome"
        ].values[0]
        for n in bus:
            if n in nome:
                pgtotal += pg
                # print(value["numero"], pg, value["potencia_ativa_maxima"], pg*100/value["potencia_ativa_maxima"])
                i += 1

    i = 0
    for idx, value in powerflow.dgerDF.iterrows():
        flag = False
        pg = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "potencia_ativa"
        ].values[0]
        nome = powerflow.dbarDF.loc[
            powerflow.dbarDF["numero"] == value["numero"], "nome"
        ].values[0]
        for n in bus:
            if n in nome:
                flag = True
                break
        if flag:
            print(pg / pgtotal * 100)
            i += 1
        else:
            print(0)

    print(i)

    print(powerflow.dgerDF.shape[0])

    # barra500 = powerflow.dbarDF.loc[powerflow.dbarDF["grupo_base_tensao"] == 'B ']
    # lt500 = powerflow.dlinDF.loc[(powerflow.dlinDF["de"].isin(barra500.numero.values)) & (powerflow.dlinDF["para"].isin(barra500.numero.values))]

    # area = powerflow.dbarDF["area"].value_counts()
    # for value, count in area.items():
    #     print(f"{value}: {count}")

    # areatype = powerflow.dbarDF.groupby("area")["tipo"].value_counts()
    # for (value1, value2), count in areatype.items():
    #     print(f"AREA: {value1}, TYPE: {value2}, Count: {count}")

    area = powerflow.dbarDF.loc[powerflow.dbarDF.area == 1, "numero"].tolist()
    # print(area, len(area))

    for idx, value in powerflow.dlinDF.iterrows():
        if (value.de in area and value.para not in area) or (
            value.de not in area and value.para in area
        ):
            if value.de in area or value.para in area:
                # print(value.de, value.para)
                try:
                    area.remove(value.de)
                except:
                    area.remove(value.para)

    print(area, len(area))
    print("Pl", powerflow.dbarDF.demanda_ativa.sum())
    print("Ql", powerflow.dbarDF.demanda_reativa.sum())
    print("Pg", powerflow.dbarDF.potencia_ativa.sum())
    print("Qg", powerflow.dbarDF.potencia_reativa.sum())

    gen = powerflow.dbarDF.loc[
        (powerflow.dbarDF["tipo"] != 0) & (powerflow.dbarDF["potencia_ativa"] > 0.0)
    ]

    print()

    ## ESTADOS NORTE DO BRASIL: AC, AP, AM, PA, TO, RO, RR
    ## ESTADOS NORDESTE DO BRASIL: AL, BA, CE, MA, PB, PE, PI, RN, SE
    ## ESTADOS CENTRO-OESTE DO BRASIL: DF, GO, MS, MT
    ## ESTADOS SUDESTE DO BRASIL: ES, MG, RJ, SP
    ## ESTADOS SUL DO BRASIL: PR, RS, SC

    # SLACKS
    slack = powerflow.dbarDF.loc[powerflow.dbarDF["tipo"] == 2]

    # UHEs
    uhe = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("UHE")]
    uhegbt = uhe["grupo_base_tensao"].unique()
    uhegbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(uhegbt)
    ].reset_index(drop=True)
    uhegbtvalue["quantidade"] = uhe["grupo_base_tensao"].value_counts().to_list()

    # UTEs
    ute = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("UTE")]
    utegbt = ute["grupo_base_tensao"].unique()
    utegbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(utegbt)
    ].reset_index(drop=True)
    utegbtvalue["quantidade"] = ute["grupo_base_tensao"].value_counts().to_list()

    # EOLs
    eol = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("EOL")]
    eolgbt = eol["grupo_base_tensao"].unique()
    eolgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(eolgbt)
    ].reset_index(drop=True)
    eolgbtvalue["quantidade"] = eol["grupo_base_tensao"].value_counts().to_list()

    # PCHs
    pch = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("PCH")]
    pchgbt = pch["grupo_base_tensao"].unique()
    pchgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(pchgbt)
    ].reset_index(drop=True)
    pchgbtvalue["quantidade"] = pch["grupo_base_tensao"].value_counts().to_list()

    # UFVs
    ufv = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("UFV")]
    ufvgbt = ufv["grupo_base_tensao"].unique()
    ufvgbtvalue = powerflow.dgbtDF.loc[
        powerflow.dgbtDF["grupo"].isin(ufvgbt)
    ].reset_index(drop=True)
    ufvgbtvalue["quantidade"] = ufv["grupo_base_tensao"].value_counts().to_list()

    # BIOs
    # bio = powerflow.dbarDF.loc[powerflow.dbarDF["nome"].str.contains("BIO")]
    # biogbt = ufv["grupo_base_tensao"].unique()
    # biogbtvalue = powerflow.dgbtDF.loc[
    #     powerflow.dgbtDF["grupo"].isin(biogbt)
    # ].reset_index(drop=True)
    # biogbtvalue["quantidade"] = bio["grupo_base_tensao"].value_counts().to_list()

    # DGBTs
    gbt = powerflow.dbarDF["grupo_base_tensao"].unique()
    gbtvalue = powerflow.dgbtDF.loc[powerflow.dgbtDF["grupo"].isin(gbt)].reset_index(
        drop=True
    )
    gbtvalue["quantidade"] = (
        powerflow.dbarDF["grupo_base_tensao"].value_counts().to_list()
    )

    # DAREs
    area = powerflow.dbarDF["area"].unique()
    areavalue = powerflow.dareDF.loc[powerflow.dareDF["numero"].isin(area)].reset_index(
        drop=True
    )
    areavalue["quantidade"] = powerflow.dbarDF["area"].value_counts().to_list()

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
    transmissao = powerflow.dbarDF.query("grupo_base_tensao in @trans").reset_index(
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
    distribuicao = powerflow.dbarDF.query("grupo_base_tensao in @dist").reset_index(
        drop=True
    )

    #
    fic = sorted(
        powerflow.dgbtDF.loc[
            ((powerflow.dgbtDF["tensao"] > 900) | (powerflow.dgbtDF["tensao"] < 6.9)),
            "grupo",
        ]
    )
    ficticia = powerflow.dbarDF.query("grupo_base_tensao in @fic").reset_index(
        drop=True
    )

    # print("Total de barramentos: ", powerflow.nbus)
    # print("Transmissao: ", transmissao.shape[0])
    # print("Distribuicao: ", distribuicao.shape[0])
    # print("Ficticia: ", ficticia.shape[0])

    # print()

    # print("UHEs: ", uhe.shape[0])
    # print("UHEs GBTs: ", uhegbtvalue)

    # print()

    # print("UTEs: ", ute.shape[0])
    # print("UTEs GBTs: ", utegbtvalue)

    # print()

    # print("EOLs: ", eol.shape[0])
    # print("EOLs GBTs: ", eolgbtvalue)

    # print()

    # print("PCHs: ", pch.shape[0])
    # print("PCHs GBTs: ", pchgbtvalue)

    # print()

    # print("UFVs: ", ufv.shape[0])
    # print("UFVs GBTs: ", ufvgbtvalue)

    # # print()

    # # print("BIOs: ", bio.shape[0])
    # # print("BIOs GBTs: ", biogbtvalue)

    # print()

    # print("GBTs: ", gbtvalue)

    # print()

    # print("Areas: ", areavalue)
