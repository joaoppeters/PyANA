# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os import listdir
import re


def convergence(
    rflines,
    linecount,
):
    """

    Args
        rflines (_type_): _description_
        linecount (_type_): _description_
    """
    ## Inicialização
    if rflines[linecount - 2] == " CONVERGENCIA FINAL\n":
        return True
    else:
        return False


def bint(
    powerflow,
    where: str="EXLF",
    rfile: str="",
):
    """

    Args
        powerflow (_type_): _description_
        relfile (str, optional): ".
    """

    from folder import bxlffolder, bxicfolder, bxctfolder

    import pandas as pd

    ## Inicialização
    rintheaderlong = " X----X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X\n"
    rintheadershort = " X----X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X\n"
    conv_header = " X-----------X------X------X---------------X---------------X---------------X\n"

    if where == "EXLF":
        bxlffolder(
            powerflow,
        )
        relfile = powerflow.bxlffolder + "EXLF_" + powerflow.name + ".REL"

    elif where == "EXIC":
        bxicfolder(
            powerflow,
        )
        relfile = powerflow.bxicfolder + "EXIC_" + powerflow.name + "_1.REL"

    elif where == 'EXCT':
        bxctfolder(
            powerflow,
        )
        relfile = powerflow.bxctfolder + "EXLF_" + powerflow.name + ".REL"

        if rfile:
            relfile = powerflow.bxctfolder + rfile	

    linecount = 0
    rf = open(f"{relfile}", "r", encoding="utf-8", errors="ignore")
    rflines = rf.readlines()
    rf.close()

    areas = powerflow.dbarDF.area.drop_duplicates().sort_values().tolist()
    intercambio = pd.DataFrame(
        index=areas,
        columns=areas,
        dtype="object",
    )

    while linecount < len(rflines):
        linecount += 1
        try:
            if rflines[linecount] == conv_header:
                flag = convergence(rflines, linecount)
                if not flag:
                    break
            elif (
                rflines[linecount] == rintheaderlong
                or rflines[linecount] == rintheadershort
            ):
                linecount += 3
                header = rflines[linecount - 1].split()[1:]
                for row in range(0, 15):
                    r = int(rflines[linecount + 2].split()[0])
                    for col in range(0, len(header)):
                        c = int(header[col])
                        p = float(rflines[linecount + 2].split()[col + 1])
                        q = float(rflines[linecount + 3].split()[col])
                        intercambio.at[r, c] = (p, q)
                    linecount += 3
        except:
            pass

    nnz_dict = {
        f"d{row}p{col}": intercambio.at[row, col]
        for row in intercambio.index
        for col in intercambio.columns
        if isinstance(intercambio.at[row, col], tuple)
        and intercambio.at[row, col] != (0, 0)
    }

    # Convert to a DataFrame with columns as (row, col) pairs and the index as file_index
    nnz_df = pd.DataFrame([list(nnz_dict.values())], columns=nnz_dict.keys(), index=[0])
    nnz_df.index.name = "CASO"
    if rfile:
        nnz_df['filename'] = rfile
    else:
        nnz_df['filename'] = powerflow.name

    return nnz_df


def btot(
    powerflow,
    relfile: str = "",
):
    """

    Args
        powerflow:
        relfile:
    """

    from folder import bxlffolder

    ## Inicialização
    conv_header = " X-----------X------X------X---------------X---------------X---------------X\n"
    bxlffolder(
        powerflow,
    )
    if not relfile:
        relfile = powerflow.bxlffolder + "EXLF_" + powerflow.name + ".REL"
    linecount = 0
    rf = open(f"{relfile}", "r", encoding="utf-8", errors="ignore")
    rflines = rf.readlines()
    rf.close()
    flag = True
    while flag:
        linecount += 1
        if rflines[linecount] == conv_header:
            flag = convergence(rflines, linecount)
            if not flag:
                break
        elif rflines[linecount] == " RELATORIO DE TOTAIS DE AREA\n":
            while linecount < len(rflines):
                linecount += 1
                try:
                    if rflines[linecount].split()[0] == "TOTAL":
                        basecase = [
                            float(rflines[linecount].split()[1]),
                            float(rflines[linecount + 1].split()[0]),
                            float(rflines[linecount].split()[3]),
                            float(rflines[linecount + 1].split()[2]),
                        ]
                        flag = False
                        break
                except:
                    pass
    return basecase


def rxic(folder, relfiles, vsmfile, option=0,):
    """

    Args:
        folder:
        relfiles:
        vsmfile:
        string:
    """
    ## Inicialização
    initstring = " RELATORIO DE EXECUCAO DO FLUXO DE POTENCIA CONTINUADO\n"
    rxicstring = [" Atingido incremento minimo\n", " **************************** PATAMAR VIOLADO *****************************\n"]

    base = None
    surface = list()
    for relfile in relfiles:
        if option:
            case = 0
        elif not option:
            case = re.search(r"C(\d+)\_(\d+)\.REL", relfile).group(2)

        with open(folder + "\\" + relfile, "r") as rf:
            lines = rf.readlines()

            for line_number, line in enumerate(lines):
                if not base and initstring in line:
                    base = line_number + 10
                if line in rxicstring:
                    break

            for ln in range(line_number - 1, -1, -1):
                try:
                    if lines[ln].split()[1] == "Convergente":
                        premlp = int(lines[ln].split()[0])
                        with open(vsmfile, "a") as vf:
                            vf.write(
                                "{};{};{};{};{}\n".format(
                                    case,
                                    lines[base].split()[6],
                                    lines[base + 1].split()[4],
                                    lines[ln].split()[6],
                                    lines[ln + 1].split()[4],
                                )
                            )
                        break
                except:
                    pass
            surface.extend(
                [
                    1,
                    1,
                    float(lines[ln].split()[6]) / float(lines[base].split()[6]),
                    float(lines[ln + 1].split()[4]) / float(lines[base + 1].split()[4]),
                ]
            )
    return surface, premlp


def rbar(
    powerflow,
    where: str="EXLF",
    rfile: str="",
):
    """

    Args
        powerflow (_type_): _description_
        where (str, optional): Defaults to "EXLF".
    """

    import pandas as pd

    from folder import rbarfolder

    ## Inicialização
    rbarfolder(
        powerflow,
    )

    area = 0
    nbus_per_area = powerflow.dbarDF.groupby("area").size().to_list()
    header = " X-----X------------X--X-----X-----X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X---X\n"
    conv_header = " X-----------X------X------X---------------X---------------X---------------X\n"

    dbar = pd.DataFrame(columns=["numero", "nome", "tipo", "tensao", "angulo", "potencia_ativa", "potencia_reativa", "demanda_ativa", "demanda_reativa", "shunt_barra", "area"])
    if where == "EXLF":
        folder = powerflow.bxlffolder
        relfile = folder + "\\" + where + "_" + powerflow.name + ".REL"
        rbfolder = powerflow.rbarxlffolder

    elif where == "EXIC":
        folder = powerflow.bxicfolder
        relfile = folder + "\\" + where + "_" + powerflow.name + "_1.REL"
        rbfolder = powerflow.rbarxicfolder

    elif where == "EXCT":
        folder = powerflow.bxctfolder
        relfile = folder + "\\EXLF_" + powerflow.name + ".REL"
        rbfolder = powerflow.rbarxctfolder
    
    if rfile:
        relfile = folder + rfile

    linecount = 0
    rf = open(f"{relfile}", "r", encoding="utf-8", errors="ignore")
    rflines = rf.readlines()
    rf.close()
    flag = True
    while flag:
        linecount += 1
        try:
            if rflines[linecount] == conv_header:
                flag = convergence(rflines, linecount)
                if not flag:
                    break
            elif rflines[linecount] == header and area != len(nbus_per_area):
                linecount += 2
                for bus in range(0, nbus_per_area[area]):
                    dict = {
                        "numero": int(rflines[linecount].split()[0]),
                        "nome": rflines[linecount].split()[1],
                        "tipo": rflines[linecount].split()[2],
                        "tensao": float(rflines[linecount].split()[3]),
                        "angulo": float(rflines[linecount].split()[4]),	
                        "potencia_ativa": float(rflines[linecount].split()[5]),
                        "potencia_reativa": float(rflines[linecount].split()[6]),
                        "demanda_ativa": float(rflines[linecount].split()[9]),
                        "demanda_reativa": float(rflines[linecount].split()[10]),
                        "shunt_barra": float(rflines[linecount].split()[13]),
                        "area": area+1,
                    }
                    dbar = pd.concat([dbar, pd.DataFrame([dict])], ignore_index=True)
                area += 1
        except:
            break
    
    if rfile and flag:
        dbar.to_csv(rbfolder + where + "_" + rfile + ".txt", sep=";", index=False)
        dbar["filename"] = rfile
    elif not rfile and flag:
        dbar.to_csv(rbfolder + where + "_" + powerflow.name + ".txt", sep=";", index=False)
        dbar["filename"] = powerflow.name

    return dbar

def rint(
    powerflow,
):
    """

    Args
        powerflow (_type_): _description_
        string (str, optional): Defaults to r"MOD(\d+)\.REL".
    """

    import pandas as pd

    from folder import rintfolder

    ## Inicialização
    rintheaderlong = " X----X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X\n"
    rintheadershort = " X----X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X-------X\n"
    conv_header = " X-----------X------X------X---------------X---------------X---------------X\n"

    rintfolder(
        powerflow,
    )
    areas = powerflow.dbarDF.area.drop_duplicates().sort_values().tolist()

    folders = [
        f
        for f in listdir(powerflow.exlffolder)
        if f.startswith("EXLF_" + powerflow.name + "_")
    ]

    for folder in folders:
        relfiles = [
            f
            for f in listdir(powerflow.exlffolder + folder)
            if f.startswith("EXLF") and f.endswith(".REL")
        ]

        intercambio = pd.DataFrame(
            index=areas,
            columns=areas,
            dtype="object",
        )
        nnz_df = pd.DataFrame()

        for relfile in relfiles:
            index = relfile.removesuffix(".REL").split("JPMOD")[-1]
            linecount = 0
            rf = open(
                f"{powerflow.exlffolder + folder + '/' + relfile}",
                "r",
                encoding="utf-8",
                errors="ignore",
            )
            rflines = rf.readlines()
            rf.close()

            while linecount < len(rflines):
                linecount += 1
                try:
                    if rflines[linecount] == conv_header:
                        flag = convergence(rflines, linecount)
                        if not flag:
                            break
                    elif (
                        rflines[linecount] == rintheaderlong
                        or rflines[linecount] == rintheadershort
                    ):
                        linecount += 3
                        header = rflines[linecount - 1].split()[1:]
                        for row in range(0, 15):
                            r = int(rflines[linecount + 2].split()[0])
                            for col in range(0, len(header)):
                                c = int(header[col])
                                p = float(rflines[linecount + 2].split()[col + 1])
                                q = float(rflines[linecount + 3].split()[col])
                                intercambio.at[r, c] = (p, q)
                            linecount += 3
                except:
                    pass

            nnz_dict = {
                f"d{row}p{col}": intercambio.at[row, col]
                for row in intercambio.index
                for col in intercambio.columns
                if isinstance(intercambio.at[row, col], tuple)
                and intercambio.at[row, col] != (0, 0)
            }

            # Convert to a DataFrame with columns as (row, col) pairs and the index as file_index
            temp_df = pd.DataFrame(
                [list(nnz_dict.values())], columns=nnz_dict.keys(), index=[index]
            )

            # Concatenate results
            nnz_df = pd.concat([nnz_df, temp_df], ignore_index=False)

        nnz_df.index.name = "CASO"
        nnz_df.to_csv(powerflow.rintfolder + folder + ".txt", sep=";", index=True)


def rtot(powerflow, string=r"MOD(\d+)\.REL"):
    """

    Args
        folder:
        string:
    """

    from folder import rtotfolder

    ## Inicialização
    rtotstring = " RELATORIO DE TOTAIS DE AREA\n"
    conv_header = " X-----------X------X------X---------------X---------------X---------------X\n"

    rtotfolder(
        powerflow,
    )

    folders = [
        f
        for f in listdir(powerflow.exlffolder)
        if f.startswith("EXLF_" + powerflow.name + "_") and f.endswith(".REL")
    ]

    for folder in folders:
        with open(
            powerflow.rtotfolder + folder + ".txt",
            "w",
        ) as rtotfile:
            rtotfile.write("CASO;pATIVA;pREATIVA;dATIVA;dREATIVA\n")

        relfiles = [
            f
            for f in listdir(powerflow.exlffolder + folder)
            if f.startswith("EXLF") and f.endswith(".REL")
        ]

        for relfile in relfiles:
            linecount = 0
            rf = open(
                f"{powerflow.exlffolder + folder + '/' + relfile}",
                "r",
                encoding="utf-8",
                errors="ignore",
            )
            rflines = rf.readlines()
            rf.close()
            flag = True

            while linecount < len(rflines) and flag:
                linecount += 1
                if rflines[linecount] == conv_header:
                    flag = convergence(rflines, linecount)
                    if not flag:
                        break
                elif rflines[linecount] == rtotstring:
                    while linecount < len(rflines):
                        linecount += 1
                        try:
                            if rflines[linecount].split()[0] == "TOTAL":
                                with open(rtotfile.name, "a") as af:
                                    af.write(
                                        "{};{};{};{};{}\n".format(
                                            re.search(string, relfile).group(1),
                                            rflines[linecount].split()[1],
                                            rflines[linecount + 1].split()[0],
                                            rflines[linecount].split()[3],
                                            rflines[linecount + 1].split()[2],
                                        )
                                    )
                                flag = False
                                break
                        except:
                            pass

        # Open and read the file
        with open(powerflow.rtotfolder + folder + ".txt", "r") as f:
            lines = f.readlines()

        # Separate the header and data
        header = lines[0]
        data = lines[1:]

        # Sort the data lines based on the first column (split by `;`)
        sorted_data = sorted(data, key=lambda x: int(x.split(";")[0]))

        # Combine the header and sorted data
        sorted_lines = [header] + sorted_data

        # Write the sorted lines to a new file
        with open(powerflow.rtotfolder + folder + ".txt", "w") as f:
            f.writelines(sorted_lines)


def vsm(
    powerflow,
    base=False,
):
    """

    Args:
        powerflow (_type_): _description_
    """

    from matplotlib.pyplot import (
        figure,
        legend,
        plot,
        savefig,
        scatter,
        title,
        xlabel,
        ylabel,
    )

    from folder import vsmfolder

    ## Inicialização
    vsmfolder(
        powerflow,
    )

    if base:
        sxic = powerflow.bxicfolder
        option = 1
    else:
        sxic = powerflow.exicfolder
        option = 0

    relfiles = [
        f
        for f in listdir(sxic)
        if f.startswith("EXIC_" + powerflow.name + "_") and f.endswith(".REL")
    ]

    vsmfile = powerflow.vsmfolder + "\\VSM_" + powerflow.name + ".txt"
    with open(vsmfile, "w") as vf:
        vf.write("CASO;dATIVA;dREATIVA;dATIVA_VSM;dREATIVA_VSM\n")

    powerflow.surface, powerflow.premlp = rxic(
        folder=powerflow.bxicfolder,
        relfiles=relfiles,
        vsmfile=vsmfile,
        option=option,
    )

    # figure(1, figsize=(10, 6))
    # scatter(surface[0], surface[1], marker="*", color="black", label="Base Case Load")
    # for s in range(0, 9):
    #     scatter(
    #         surface[4 * s + 2],
    #         surface[4 * s + 3],
    #         marker="o",
    #         color="blue",
    #         label=f"Increment #{s+1}",
    #     )
    # plot(
    #     (surface[0], surface[2]),
    #     (surface[1], surface[3]),
    #     linestyle="--",
    #     color="blue",
    # )
    # plot(
    #     (surface[0], surface[-2]),
    #     (surface[1], surface[-1]),
    #     linestyle="--",
    #     color="blue",
    # )
    # xlabel("Active Power Load")
    # ylabel("Reactive Power Load")
    # title("Bifurcation Surface")
    # legend()
    # savefig(
    #     powerflow.vsmfolder + "\\VSM_" + powerflow.name + ".pdf",
    #     dpi=500,
    # )
