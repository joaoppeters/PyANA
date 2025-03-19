# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def snts(
    powerflow,
):
    """
    
    Args
    ----
    powerflow : 
    """

    import matplotlib.pyplot as plt
    import seaborn as sns

    from os import listdir
    import pandas as pd

    from rela import bint, mocf, moct, rbar, vsm
    from ulog import basexlf, basexic, basexct

    ## Inicialização
    # basexlf(powerflow,)
    powerflow.rbar_base = rbar(powerflow, where="EXLF",)
    powerflow.rint_base = bint(powerflow, where="EXLF",)

    # basexic(powerflow,)
    powerflow.rbar_mlp = rbar(powerflow, where="EXIC",)
    vsm(powerflow, base=True,)
    powerflow.rint_vsm = bint(powerflow, where="EXIC",)

    # basexct(powerflow, where="EXIC",)
    powerflow.rbar_premlp = rbar(powerflow, where="EXCT",)
    powerflow.rint_premlp = bint(powerflow, where="EXCT",)
    rfiles = [
        f
        for f in listdir(powerflow.bxctfolder)
        if f.startswith("EXCT_" + powerflow.name) and f.endswith(".REL")
    ]
    
    nonconv = list()
    flow_violations = {
        "numero_de": list(),
        "nome_de": list(),
        "numero_para": list(),
        "nome_para": list(),
        "circuito": list(),
        "mw": list(),
        "mvar": list(),
        "mva/v": list(),
        "mva_viol": list(),
        "mva_lim": list(),
        "filename": list(),
    } 
    flow_violations = pd.DataFrame(flow_violations)

    volt_violations = {
        "numero": list(),
        "nome": list(),
        "area": list(),
        "limite_minimo": list(),
        "tensao": list(),
        "limite_maximo": list(),
        "violacao": list(),
        "filename": list(),
    }
    volt_violations = pd.DataFrame(volt_violations)
    volt_violations_E = volt_violations.copy()
    for rfile in rfiles:
        try:
            rb = rbar(powerflow, where="EXCT", rfile=rfile,)
            flow_violations = pd.concat([flow_violations, mocf(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True,)
            powerflow.rbar_premlp = pd.concat([powerflow.rbar_premlp, rb,], ignore_index=True,)
            powerflow.rint_premlp = pd.concat([powerflow.rint_premlp, bint(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True,)
            if (rb.tensao > powerflow.dbarDF.limite_maximo).any() or (rb.tensao < powerflow.dbarDF.limite_minimo).any():
                volt_violations = pd.concat([volt_violations, moct(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True,)
                volt_violations_E = pd.concat([volt_violations_E, moct(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True,)
        except:
            nonconv.append(rfile)

    # Criando uma cópia do DataFrame
    rbar_premlp_volt = powerflow.rbar_premlp[['tensao', 'numero',]].copy()
    rbar_premlp_volt_volt_violations = volt_violations[['tensao', 'numero',]].copy()
    rbar_premlp_volt_volt_violations_E = volt_violations_E[['tensao', 'numero',]].copy()
    rpv = {}
    rpvv = {}
    rpvvE = {}
    for numero in rbar_premlp_volt['numero'].unique():
        rpv[numero] = rbar_premlp_volt.loc[rbar_premlp_volt['numero'] == numero, 'tensao'].values
        rpvv[numero] = rbar_premlp_volt_volt_violations.loc[rbar_premlp_volt_volt_violations['numero'] == numero, 'tensao'].values
        rpvvE[numero] = rbar_premlp_volt_volt_violations_E.loc[rbar_premlp_volt_volt_violations_E['numero'] == numero, 'tensao'].values

    rbar_premlp_volt = pd.DataFrame(rpv)
    rbar_premlp_volt_volt_violations = pd.DataFrame(rpvv)
    rbar_premlp_volt_volt_violations_E = pd.DataFrame(rpvvE)

    # rbar_premlp_volt.to_csv(powerflow.bxctfolder + "rbar_premlp_volt.csv", index=False)
    # rbar_premlp_volt_volt_violations.to_csv(powerflow.bxctfolder + "rbar_premlp_volt_volt_violations.csv", index=False)
    # rbar_premlp_volt_volt_violations_E.to_csv(powerflow.bxctfolder + "rbar_premlp_volt_volt_violations_E.csv", index=False)

    flow_violations.to_csv(powerflow.bxctfolder + "flow_violations.csv", index=False)
    volt_violations.to_csv(powerflow.bxctfolder + "volt_violations.csv", index=False)
    volt_violations_E.to_csv(powerflow.bxctfolder + "volt_violations_E.csv", index=False)

    original = rbar_premlp_volt.iloc[0]
    rbar_premlp_volt = rbar_premlp_volt.tail(-1)

    # Criando o gráfico de dispersão
    plt.figure(figsize=(9, 6))
    col = 0
    cols = []
    for coluna in rbar_premlp_volt.columns:
        cols.append(col)
        plt.scatter([col] * len(rbar_premlp_volt), rbar_premlp_volt[coluna], label=coluna, alpha=0.9)
        col += 2

    plt.xticks([])
    plt.plot(cols, original.values, color='black', linestyle='--', linewidth=2,)
    plt.plot(cols, powerflow.dbarDF.limite_maximo, color="blue", linestyle='--', linewidth=1,)
    plt.plot(cols, powerflow.dbarDF.limite_maximo_E, color="red", linestyle='--', linewidth=1,)
    plt.plot(cols, powerflow.dbarDF.limite_minimo, color="blue", linestyle='--', linewidth=1,)
    plt.plot(cols, powerflow.dbarDF.limite_minimo_E, color="red", linestyle='--', linewidth=1,)
    plt.xlabel("Barras", fontsize=16)
    plt.ylabel("Variação da magnitude de tensão", fontsize=16)
    
    # # Criando o gráfico de dispersão
    # plt.figure(figsize=(9, 6))
    # col = 0
    # cols = []
    # for coluna in rbar_premlp_volt_volt_violations.columns:
    #     cols.append(col)
    #     plt.scatter([col] * len(rbar_premlp_volt_volt_violations), rbar_premlp_volt_volt_violations[coluna], label=coluna, alpha=0.9)
    #     col += 2

    # plt.xticks(cols, powerflow.rbar_base.nome.values, rotation=90)
    # plt.plot(cols, original.values, color='black', linestyle='--', linewidth=1,)
    # plt.plot(cols, powerflow.dbarDF.limite_maximo, color="blue", linestyle='--', linewidth=1,)
    # plt.plot(cols, powerflow.dbarDF.limite_maximo_E, color="red", linestyle='--', linewidth=1,)
    # plt.plot(cols, powerflow.dbarDF.limite_minimo, color="blue", linestyle='--', linewidth=1,)
    # plt.plot(cols, powerflow.dbarDF.limite_minimo_E, color="red", linestyle='--', linewidth=1,)
    # plt.xlabel("Barras")
    # plt.ylabel("Variação da magnitude de tensão")
    plt.show()



    print()

