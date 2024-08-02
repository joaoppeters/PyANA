# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from rewrite import rewrite


def increment(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarDF["demanda_ativa"].to_numpy())

    ## Point of Collapse Method (Canizares, 1992)
    if powerflow.solution["method"] == "EXPC":
        # Incremento de carga
        for idxbar, _ in powerflow.dbarDF.iterrows():
            # Incremento de Carregamento
            powerflow.dbarDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
                "demanda_ativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])
            powerflow.dbarDF.at[idxbar, "demanda_reativa"] = powerflow.solution[
                "demanda_reativa"
            ][idxbar] * (1 + powerflow.solution["lambda"])

    # Prediction-Correction Method (Ajjarapu & Christy, 1992)
    elif powerflow.solution["method"] == "EXIC":
        for idxinc, valueinc in powerflow.dincDF.iterrows():
            # Incremento de carregamento específico por AREA
            if valueinc["tipo_incremento_1"] == "AREA":
                for idxbar, valuebar in powerflow.dbarDF.iterrows():
                    if valuebar["area"] == valueinc["identificacao_incremento_1"]:
                        # Incremento de Carregamento
                        powerflow.dbarDF.at[idxbar, "demanda_ativa"] = (
                            powerflow.solution["demanda_ativa"][idxbar]
                            * (1 + powerflow.solution["stepsch"])
                        )
                        powerflow.dbarDF.at[idxbar, "demanda_reativa"] = (
                            powerflow.solution["demanda_reativa"][idxbar]
                            * (1 + powerflow.solution["stepsch"])
                        )

            # Incremento de carregamento específico por BARRA
            elif valueinc["tipo_incremento_1"] == "BARR":
                # Reconfiguração da variável de índice
                idxinc = valueinc["identificacao_incremento_1"] - 1
                powerflow.dbarDF.at[idxinc, "demanda_ativa"] = powerflow.solution[
                    "demanda_ativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])
                powerflow.dbarDF.at[idxinc, "demanda_reativa"] = powerflow.solution[
                    "demanda_reativa"
                ][idxinc] * (1 + powerflow.solution["stepsch"])

        deltaincrement = (
            sum(powerflow.dbarDF["demanda_ativa"].to_numpy()) - preincrement
        )

        # Incremento de geração
        if powerflow.codes["DGER"]:
            for _, valueger in powerflow.dgerDF.iterrows():
                idx = valueger["numero"] - 1
                powerflow.dbarDF.at[idx, "potencia_ativa"] = powerflow.dbarDF[
                    "potencia_ativa"
                ][idx] + (deltaincrement * valueger["fator_participacao"])

            powerflow.solution["potencia_ativa"] = deepcopy(
                powerflow.dbarDF["potencia_ativa"]
            )

        # Condição de atingimento do máximo incremento do nível de carregamento delimitado
        if (
            powerflow.solution["stepsch"]
            == powerflow.dincDF.loc[0, "maximo_incremento_potencia_ativa"]
        ):
            powerflow.solution["pmc"] = True


def arou(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
        file
    """

    from anarede import anarede
    import pandas as pd

    ## Inicialização
    powerflow.tenths = 0
    powerflow.ones = 1
    powerflow.nc = deepcopy(powerflow.namecase)

    # Read all sheets
    excel_file = powerflow.maindir + "/sistemas/subsestacoes.xlsx"
    all_sheets = [
        "RJ-ES",
        "MG",
        "SP",
    ]

    for sheet in all_sheets:
        readfile = pd.read_excel(excel_file, sheet_name=sheet, header=2)

        for bus in readfile.Nome:
            idx = powerflow.dbarDF[powerflow.dbarDF.nome == bus].index[0]

            if powerflow.dbarDF.demanda_ativa.iloc[idx] > 0.0:
                powerflow.dbarDF.at[idx, "demanda_ativa"] = (
                    1.01 * powerflow.dbarDF.demanda_ativa.iloc[idx]
                )

                powerflow.namecase = powerflow.nc + "-" + bus
                rewrite(
                    powerflow,
                )
                filepath = powerflow.maindir + "/sistemas"
                # anarede(filepath=filepath, filenamecase=powerflow.namecase)

    # powerflow.dbar["fator_demanda_ativa"] = (
    #     powerflow.dbarDF.demanda_ativa / pmean
    # )
    # powerflow.dbar["fator_potencia"] = (
    #     powerflow.dbarDF.demanda_reativa / powerflow.dbarDF.demanda_ativa
    # )
    # powerflow.dbar["fator_eol"] = [value['potencia_ativa'] / wmean if 'EOL' in value['nome'] else 0 for idx, value in powerflow.dbarDF.iterrows()]

    # powerflow.tenths = 1
    # powerflow.ones = 0

    # for s in range(0, len(psamples)):
    #     powerfactor(
    #         powerflow,
    #         psamples,
    #         s,
    #     )
    #     eol(powerflow, wsamples, s, wmean)
    #     powerflow.ones += 1

    #     rewrite(
    #         powerflow,
    #     )

    #     filepath = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\outros\\github\\gitPyANA\\PyANA\\sistemas"
    #     anarede(filepath=filepath, filenamecase=powerflow.namecase)
    #     if powerflow.ones == 10:
    #         powerflow.tenths += 1
    #         powerflow.ones = 0

    # ## Inicialização
    # pr = 1
    # file.write("DCTG")
    # file.write("\n")
    # for idx, value in powerflow.dlinDF.iterrows():
    #     file.write(f"(Nc) O Pr (       IDENTIFICACAO DA CONTINGENCIA        )")
    #     file.write("\n")
    #     file.write(
    #         f"{idx+1:>4}   {pr:>2} CTG CIRC {value['de']}-{value['para']}"
    #     )
    #     file.write("\n")
    #     file.write(f"(Tp) (El ) (Pa ) Nc (Ext) (DV1) (DV2) (DV3) (DV4) (DV5) (DV6) (DV7) Gr Und    ")
    #     file.write("\n")
    #     file.write(
    #         f"CIRC {value['de']:>5} {value['para']:>5} {value['circuito']:>2}"
    #     )
    #     file.write("\n")
    #     file.write("FCAS")
    #     file.write("\n")
    # file.write("99999")

    # file.write("\n")
    # file.write("( ")
    # file.write("\n")

    # file.write("EXLF")

    # file.write("\n")
    # file.write("( ")
    # file.write("\n")

    # file.write("EXCT RMON")

    # file.write("\n")
    # file.write("(P Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr")
    # file.write("\n")
    # file.write(" 1  2  3  4  5  6  7  8  9 10 11 12")

    # file.write("\n")
    # file.write("( ")
    # file.write("\n")

    # file.write("EXIC PVCT GSAV RMON")

    # file.write("\n")
    # file.write("( ")
    # file.write("\n")

    # file.write("FIM")
