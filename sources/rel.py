# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from glob import glob
from os.path import join


def relr(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """

    string = (
        " X----X------------X---X--------X--------X--------X-------------X---------X\n"
    )

    folder = powerflow.maindir + "/sistemas/2Q2024_C6EOL_EXIC_std10/"

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

    string0 = (
        " X----X------------X---X--------X--------X--------X-------------X---------X\n"
    )
    string1 = " X-----X----------------------------------------------X-------------X------------X\n"

    folder = powerflow.maindir + "/sistemas/"

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
