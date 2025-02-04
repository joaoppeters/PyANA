# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from glob import glob
from os.path import join


def rrel(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """
    ## Inicialização
    if "2q2024" in powerflow.name:
        for stddev in range(1, 11, 1):
            # Specify the folder path and file extension
            folder_path = (
                powerflow.maindir
                + "\\sistemas\\"
                + powerflow.name
                + "_loadstd{}_geolstd{}".format(
                    stddev,
                    stddev,
                )
            )

    string = (
        " X----X------------X---X--------X--------X--------X-------------X---------X\n"
    )

    folder = powerflow.maindir + "\\sistemas\\2Q2024_C6EOL_EXIC_std10\\"

    rel_files = glob(join(folder, "EXIC*"))
    idx = 0
    cases = list()

    for rel_file in rel_files:
        flag = False
        with open(rel_file, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                print(line)
                if line == string and not flag:
                    flag = True

                elif flag:
                    content = line.split()
                    try:
                        if float(content[-6]) >= 7.0:
                            case = True
                        else:
                            case = False
                    except:
                        pass

        cases.append(case)
        idx += 1

    print("Trues", cases.count(True))
    print("Falses", cases.count(False))
    print()


def relpvct(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """
    ## Inicialização
    string0 = (
        " X----X------------X---X--------X--------X--------X-------------X---------X\n"
    )
    string1 = " X-----X----------------------------------------------X-------------X------------X\n"

    folder = powerflow.maindir + "\\sistemas\\"

    rel_files = glob(join(folder, "PVCT*"))

    for rel_file in rel_files:
        load = dict()
        flag = False
        with open(rel_file, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                if ((line == string0) or (line == string1)) and not flag:
                    flag = True

                elif flag:
                    content = line.split()
                    try:
                        if (content[0] == "0") and (content[-2] == "MW"):
                            load0 = float(content[-3])
                            flag = False
                        elif (content[1] != "Convergente") and (content[-2] == "MW"):
                            load[content[0]] = (
                                (float(content[-3]) - load0) * 100 / load0
                            )
                        else:
                            pass
                    except:
                        pass

        print(rel_file)
        print(*[f"{k}: {v}" for k, v in load.items()], sep="\n")


def rxic(folder, relfiles, vsmfile, string=r"C(\d+)\_(\d+)\.REL"):
    """

    Args:
        folder:
        relfiles:
        vsmfile:
    """

    from os.path import dirname
    import re

    ## Inicialização
    initstring = " RELATORIO DE EXECUCAO DO FLUXO DE POTENCIA CONTINUADO\n"
    rxicstring = " Atingido incremento minimo\n"

    base = None
    surface = list()
    for relfile in relfiles:
        with open(dirname(folder) + "\\" + relfile, "r") as rf:
            lines = rf.readlines()

            for line_number, line in enumerate(lines):
                if not base and initstring in line:
                    base = line_number + 10
                if rxicstring in line:
                    break

            for ln in range(line_number - 1, -1, -1):
                try:
                    if lines[ln].split()[1] == "Convergente":
                        with open(vsmfile, "a") as vf:
                            vf.write(
                                "{};{};{};{};{}\n".format(
                                    re.search(string, relfile).group(2),
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
    return surface


def rxct(
    powerflow,
):
    """

    Args:
        powerflow:
    """
    ## Inicialização
    pass


def rpvct(
    powerflow,
):
    """

    Args:
        powerflow:
    """
    ## Inicialização
    pass


def rint(folder, relfiles, file, string=r"MOD(\d+)\.REL"):
    """

    Args
        powerflow:
    """

    import re

    ## Inicialização
    rintstring = " RELATORIO DE INTERCAMBIO ENTRE AREAS\n"

    for relfile in relfiles:
        linecount = 0
        rf = open(f"{folder + '/' + relfile}", "r", encoding="utf-8", errors="ignore")
        rflines = rf.readlines()
        rf.close()

        while linecount < len(rflines):
            if rflines[linecount] == rintstring:
                while linecount < len(rflines):
                    linecount += 1

                    try:
                        if rflines[linecount].split()[0] == "TOTAL":
                            with open(file.name, "a") as af:
                                af.write(
                                    "{};{};{};{};{}\n".format(
                                        re.search(string, relfile).group(1),
                                        rflines[linecount].split()[1],
                                        rflines[linecount + 1].split()[0],
                                        rflines[linecount].split()[3],
                                        rflines[linecount + 1].split()[2],
                                    )
                                )
                            break
                    except:
                        pass


def rtot(powerflow, string=r"MOD(\d+)\.REL"):
    """

    Args
        folder:
        relfiles:
        file:
        string:
    """

    from os import listdir
    import re

    from folder import rtotfolder

    ## Inicialização
    rtotstring = " RELATORIO DE TOTAIS DE AREA\n"

    rtotfolder(
        powerflow,
    )

    folders = [
        f
        for f in listdir(powerflow.exlffolder)
        if f.startswith("EXLF_" + powerflow.name + "_")
    ]

    if folders:
        for folder in folders:
            with open(
                folder + ".txt",
                "w",
            ) as rtotfile:
                rtotfile.write("CASO;pATIVA;pREATIVA;dATIVA;dREATIVA\n")

            relfiles = [
                f
                for f in listdir(folder)
                if f.startswith("EXLF") and f.endswith(".REL")
            ]

            for relfile in relfiles:
                linecount = 0
                rf = open(
                    f"{folder + '/' + relfile}", "r", encoding="utf-8", errors="ignore"
                )
                rflines = rf.readlines()
                rf.close()

                while linecount < len(rflines):
                    if rflines[linecount] == rtotstring:
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
                                    break
                            except:
                                pass

    else:
        relfiles = [
            f
            for f in listdir(powerflow.exlffolder)
            if f.startswith("EXLF_" + powerflow.name) and f.endswith(".REL")
        ]


# def basecase(
#     powerflow,
# ):
#     """

#     Args:
#         powerflow (_type_): _description_
#     """

#     from os import listdir

#     from strat import get_mean_stddev

#     ## Inicialização
#     folder_path = powerflow.maindir + "\\sistemas\\EXLF\\"
#     relfiles = [
#         f
#         for f in listdir(folder_path)
#         if f.startswith("SXLF")
#         and f.endswith(".REL")
#     ]

#     with open(
#         folder_path + powerflow.sim + ".txt",
#         "w",
#     ) as file:
#         file.write("CASO;pATIVA;pREATIVA;dATIVA;dREATIVA\n")

#     # rxlf(
#     #     folder=folder_path,
#     #     relfiles=relfiles,
#     #     file=file,
#     #     string=r"C(\d+)\.REL"
#     # )

#     # Open and read the file
#     with open(folder_path + powerflow.sim + ".txt", "r") as f:
#         lines = f.readlines()

#     # Separate the header and data
#     header = lines[0]
#     data = lines[1:]

#     # Sort the data lines based on the first column (split by `;`)
#     sorted_data = sorted(data, key=lambda x: int(x.split(";")[0]))

#     # Combine the header and sorted data
#     sorted_lines = [header] + sorted_data

#     # Write the sorted lines to a new file
#     with open(folder_path + powerflow.sim + ".txt", "w") as f:
#         f.writelines(sorted_lines)


#     get_mean_stddev(filename=folder_path + powerflow.sim + ".txt")


def vsm(
    powerflow,
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
        show,
        title,
        xlabel,
        ylabel,
    )
    from os import listdir
    from os.path import dirname

    from folder import vsmfolder

    ## Inicialização
    vsmfolder(
        powerflow,
    )
    sxic = dirname(powerflow.vsmfolder)
    relfiles = [
        f
        for f in listdir(sxic)
        if f.startswith("SXIC_" + powerflow.name + "_") and f.endswith(".REL")
    ]

    vsmfile = powerflow.vsmfolder + "\\VSM_" + powerflow.name + ".txt"
    with open(vsmfile, "w") as vf:
        vf.write("CASO;dATIVA;dREATIVA;dATIVA_VSM;dREATIVA_VSM\n")

    surface = rxic(
        folder=powerflow.vsmfolder,
        relfiles=relfiles,
        vsmfile=vsmfile,
    )

    figure(1, figsize=(10, 6))
    scatter(surface[0], surface[1], marker="*", color="black", label="Base Case Load")
    for s in range(0, 9):
        scatter(
            surface[4 * s + 2],
            surface[4 * s + 3],
            marker="o",
            color="blue",
            label=f"Increment #{s+1}",
        )
    plot(
        (surface[0], surface[2]),
        (surface[1], surface[3]),
        linestyle="--",
        color="blue",
    )
    plot(
        (surface[0], surface[-2]),
        (surface[1], surface[-1]),
        linestyle="--",
        color="blue",
    )
    xlabel("Active Power Load")
    ylabel("Reactive Power Load")
    title("Bifurcation Surface")
    legend()
    savefig(
        powerflow.vsmfolder + "\\VSM_" + powerflow.name + ".pdf",
        dpi=500,
    )
