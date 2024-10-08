# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def allctgs(
    powerflow,
    file,
):
    """adição de dados de contingência em arquivo .pwf

    Args
        powerflow: self do arquivo powerflow.py
        file
    """

    ## Inicialização
    pr = 1
    file.write("DCTG")
    file.write("\n")
    for idx, value in powerflow.dlinDF.iterrows():
        file.write(f"(Nc) O Pr (       IDENTIFICACAO DA CONTINGENCIA        )")
        file.write("\n")
        file.write(f"{idx+1:>4}   {pr:>2} CTG CIRC {value['de']}-{value['para']}")
        file.write("\n")
        file.write(
            f"(Tp) (El ) (Pa ) Nc (Ext) (DV1) (DV2) (DV3) (DV4) (DV5) (DV6) (DV7) Gr Und    "
        )
        file.write("\n")
        file.write(f"CIRC {value['de']:>5} {value['para']:>5} {value['circuito']:>2}")
        file.write("\n")
        file.write("FCAS")
        file.write("\n")
    file.write("99999")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXLF")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXCT RMON")

    file.write("\n")
    file.write("(P Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr")
    file.write("\n")
    file.write(" 1  2  3  4  5  6  7  8  9 10 11 12")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXIC PVCT GSAV RMON")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("FIM")
