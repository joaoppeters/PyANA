# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from glob import glob
from os.path import join

# for stddev in range(1, 11, 1):
#     loadstd = stddev
#     geolstd = stddev

#     # Specify the folder path and file extension
#     folder_path = (
#         powerflow.maindir
#         + "\\sistemas\\"
#         + powerflow.name
#         + "_loadstd{}_geolstd{}".format(
#             loadstd,
#             geolstd,
#         )
#     )
#     savextension = ".REL"  # Change to the extension you need


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

    folder = powerflow.maindir + "\\sistemas/2Q2024_C6EOL_EXIC_std10\\"

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


print()


def rxlf(
    folder,
    relfiles,
    balancefile,
    string=r"MOD(\d+)\.REL"
):
    """

    Args:
        folder:
        relfiles:
        balancefile:
        string:
    """

    import re

    ## Inicialização
    rtotstring = " RELATORIO DE TOTAIS DE AREA\n"
    rintstring = " RELATORIO DE INTERCAMBIO ENTRE AREAS\n"

    for relfile in relfiles:
        linecount = 0
        rf = open(f"{folder + '/' + relfile}", "r", encoding="utf-8", errors="ignore")
        rflines = rf.readlines()
        rf.close()

        while linecount < len(rflines):
            if rflines[linecount] == rintstring:
                pass
                # linecount = rint(
                #     powerflow,
                #     rflines,
                #     linecount,
                # )
            elif rflines[linecount] == rtotstring:
                linecount = rtot(
                    rflines=rflines,
                    linecount=linecount,
                    balancefile=balancefile,
                    rfilecount=re.search(string, relfile).group(1),
                )
            linecount += 1


def rxic(
    powerflow,
):
    """

    Args:
        powerflow:
    """
    ## Inicialização
    pass


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


def rint(powerflow, rflines, linecount):
    """

    Args
        powerflow:
    """
    ## Inicialização
    return linecount


def rtot(
    rflines,
    linecount,
    balancefile,
    rfilecount,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    while linecount < len(rflines):
        linecount += 1

        try:
            if rflines[linecount].split()[0] == "TOTAL":
                with open(balancefile.name, "a") as bf:
                    bf.write(
                        "{};{};{};{};{}\n".format(
                            rfilecount,
                            rflines[linecount].split()[1],
                            rflines[linecount + 1].split()[0],
                            rflines[linecount].split()[3],
                            rflines[linecount + 1].split()[2],
                        )
                    )
                break
        except:
            pass

    return linecount



def q2024(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """

    from os import listdir

    from strat import get_mean_stddev

    ## Inicialização
    folder_path = powerflow.maindir + "\\sistemas\\EXLF\\"
    relfiles = [
        f
        for f in listdir(folder_path)
        if f.startswith("SXLF")
        and f.endswith(".REL")
    ]

    with open(
        folder_path + powerflow.sim + ".txt",
        "w",
    ) as file:
        file.write("CASO;pATIVA;pREATIVA;dATIVA;dREATIVA\n")

    rxlf(
        folder=folder_path,
        relfiles=relfiles,
        balancefile=file,
        string=r"C(\d+)\.REL"
    )

    # Open and read the file
    with open(folder_path + powerflow.sim + ".txt", "r") as f:
        lines = f.readlines()

    # Separate the header and data
    header = lines[0]
    data = lines[1:]

    # Sort the data lines based on the first column (split by `;`)
    sorted_data = sorted(data, key=lambda x: int(x.split(";")[0]))

    # Combine the header and sorted data
    sorted_lines = [header] + sorted_data

    # Write the sorted lines to a new file
    with open(folder_path + powerflow.sim + ".txt", "w") as f:
        f.writelines(sorted_lines)
        

    get_mean_stddev(filename=folder_path + powerflow.sim + ".txt")

