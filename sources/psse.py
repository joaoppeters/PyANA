# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import pssefolder

from pandas import ExcelWriter


def pssexcel(
    powerflow,
):
    """salva arquivo no formato do PSS/E

    Args
        powerflow:
    """

    ## Inicialização

    pssefolder(
        powerflow,
    )

    excel_file = powerflow.pssefolder + f"{powerflow.system.split('.')[0]}.xlsx"

    busDF = powerflow.dbarDF[
        [
            "numero",
            "nome",
            "tipo",
            "tensao",
            "angulo",
        ]
    ]
    busDF["angulo"] = powerflow.dbar.angulo
    busDF["dgbt"] = powerflow.dbarDF.grupo_base_tensao.map(
        powerflow.dgbtDF.set_index("grupo")["tensao"].to_dict()
    )
    busDF["vmn"] = powerflow.dbarDF.grupo_limite_tensao.map(
        powerflow.dgltDF.set_index("grupo")["limite_minimo"].to_dict()
    )
    busDF["vmx"] = powerflow.dbarDF.grupo_limite_tensao.map(
        powerflow.dgltDF.set_index("grupo")["limite_maximo"].to_dict()
    )
    busDF["vmne"] = powerflow.dbarDF.grupo_limite_tensao.map(
        powerflow.dgltDF.set_index("grupo")["limite_minimo_E"].to_dict()
    )
    busDF["vmxe"] = powerflow.dbarDF.grupo_limite_tensao.map(
        powerflow.dgltDF.set_index("grupo")["limite_maximo_E"].to_dict()
    )

    machineDF = powerflow.dbarDF[powerflow.dbarDF.tipo != 0][
        [
            "numero",
            "tensao",
            "potencia_ativa",
            "potencia_reativa",
            "potencia_reativa_maxima",
            "potencia_reativa_minima",
        ]
    ]

    loadDF = powerflow.dbarDF[powerflow.dbarDF.tipo == 0][
        [
            "numero",
            "area",
            "demanda_ativa",
            "demanda_reativa",
        ]
    ]

    shuntDF = powerflow.dbarDF[powerflow.dbarDF.shunt_barra != 0][
        [
            "numero",
            "shunt_barra",
        ]
    ]

    branchDF = powerflow.dlinDF[powerflow.dlin.tap == 5 * " "][
        [
            "de",
            "para",
            "circuito",
            "resistencia",
            "reatancia",
            "susceptancia",
        ]
    ]
    branchDF["nomede"] = branchDF.de.map(
        powerflow.dbarDF.set_index("numero")["nome"].to_dict()
    )
    branchDF["nomepara"] = branchDF.para.map(
        powerflow.dbarDF.set_index("numero")["nome"].to_dict()
    )

    windingDF = powerflow.dlinDF[powerflow.dlin.tap != 5 * " "][
        [
            "de",
            "para",
            "circuito",
            "reatancia",
            "tap",
        ]
    ]
    windingDF["tap"] = windingDF.tap.map(lambda x: abs(x))
    windingDF["nomede"] = windingDF.de.map(
        powerflow.dbarDF.set_index("numero")["nome"].to_dict()
    )
    windingDF["nomepara"] = windingDF.para.map(
        powerflow.dbarDF.set_index("numero")["nome"].to_dict()
    )

    # Save to different worksheets
    with ExcelWriter(excel_file, engine="openpyxl") as writer:
        busDF.to_excel(writer, sheet_name="Bus", index=False)
        machineDF.to_excel(writer, sheet_name="Machine", index=False)
        loadDF.to_excel(writer, sheet_name="Load", index=False)
        shuntDF.to_excel(writer, sheet_name="Shunt", index=False)
        branchDF.to_excel(writer, sheet_name="Branch", index=False)
        windingDF.to_excel(writer, sheet_name="Winding", index=False)

    print(f"\033[32mData has been saved to {excel_file}!\033[0m")
