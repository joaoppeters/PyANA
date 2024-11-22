# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import realpath
from datetime import datetime as dt

from sav import savmove


def wulog(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder
        + "/"
        + powerflow.namecase
        + "{}.pwf".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")
    savfile = "_".join(powerflow.name.split("_")[:-1]) + ".SAV"
    case = powerflow.name.split("_")[-1][1:]

    savmove(
        filename=powerflow.maindir + "\\sistemas\\" + savfile,
        filedir=powerflow.filefolder,
    )

    # Cabecalho
    uheader(
        file,
    )

    # Corpo
    uarq(
        file,
        savfile,
        case,
    )

    if powerflow.codes["DBAR"]:
        udbar(
            powerflow.dbar,
            file,
        )

    if powerflow.codes["DGER"]:
        udger(
            powerflow.dger,
            file,
        )

    if powerflow.codes["DINC"]:
        udinc(
            powerflow.dinc,
            file,
        )

    if powerflow.codes["DMET"]:
        udmet(
            powerflow.dmet,
            file,
        )

    if powerflow.codes["DCTG"]:
        udctg(
            powerflow.dctg,
            powerflow.dctg1,
            powerflow.dctg2,
            file,
        )
    if powerflow.codes["DMFL"]:
        if "CIRC" in powerflow.dmfl.dmfl.iloc[0]:
            udmfl_circ(
                powerflow.dmfl,
                file,
            )
        else:
            udmfl(
                powerflow.dmfl,
                file,
            )

    if powerflow.codes["DMTE"]:
        udmte(
            powerflow.dmte,
            file,
        )

    # Saida
    usxsc(
        powerflow,
        file,
    )


def uheader(
    file,
):
    """

    Args
        file:
    """

    ## Inicialização
    file.write("(")
    file.write("\n")
    file.write("( Modificacao Automatica de Dados .PWF")
    file.write("\n")
    file.write("( Joao Pedro Peters Barbosa - jpeters@usp.br")
    file.write("\n")
    file.write(
        "( Data e Hora da Gravacao: {} {}, {}  -  {}:{}:{}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
            dt.now().strftime("%H"),
            dt.now().strftime("%M"),
            dt.now().strftime("%S"),
        )
    )
    file.write("\n")
    file.write("( ")
    file.write("\n")


def uarq(
    file,
    savfile,
    case,
):
    """

    Args
        file:
    """

    ## Inicialização
    file.write("ULOG")
    file.write("\n")
    file.write("2")
    file.write("\n")
    file.write("{}".format(savfile))
    file.write("\n")
    file.write("ARQV REST")
    file.write("\n")
    file.write("{}".format(case))
    file.write("\n")


def udbar(
    dbar,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dbar.dbar.iloc[0]))
    file.write(format(dbar.ruler.iloc[0]))

    for idx, value in dbar.iterrows():
        if "EOL" not in value["nome"]:
            dbar.loc[idx, "potencia_ativa"] = 5 * ""

        if value["demanda_ativa"] != 5 * " ":
            value["demanda_ativa"] = float(value["demanda_ativa"])
            if value["demanda_ativa"] >= 0.0:
                if value["demanda_ativa"] / 1e3 >= 1.0:
                    pl = str(
                        round(
                            value["demanda_ativa"],
                        )
                    )
                elif (
                    value["demanda_ativa"] / 1e3 >= 0.1
                    and value["demanda_ativa"] / 1e3 < 1.0
                ):
                    pl = str(round(value["demanda_ativa"], 1))
                else:
                    pl = str(round(value["demanda_ativa"], 1))
            else:
                if value["demanda_ativa"] / 1e3 < -0.1:
                    pl = str(
                        round(
                            value["demanda_ativa"],
                        )
                    )
                else:
                    pl = str(round(value["demanda_ativa"], 1))
        else:
            pl = 5 * " "

        if value["demanda_reativa"] != 5 * " ":
            value["demanda_reativa"] = float(value["demanda_reativa"])
            if value["demanda_reativa"] >= 0.0:
                if value["demanda_reativa"] / 1e3 >= 1.0:
                    ql = str(
                        round(
                            value["demanda_reativa"],
                        )
                    )
                elif (
                    value["demanda_reativa"] / 1e3 >= 0.1
                    and value["demanda_reativa"] / 1e3 < 1.0
                ):
                    ql = str(round(value["demanda_reativa"], 1))
                else:
                    ql = str(round(value["demanda_reativa"], 1))
            else:
                if value["demanda_reativa"] / 1e3 < -0.1:
                    ql = str(
                        round(
                            value["demanda_reativa"],
                        )
                    )
                else:
                    ql = str(round(value["demanda_reativa"], 1))
        else:
            ql = 5 * " "

        if value["shunt_barra"] != 5 * " ":
            value["shunt_barra"] = float(value["shunt_barra"])
            if value["shunt_barra"] >= 0.0:
                if value["shunt_barra"] / 1e3 >= 1.0:
                    sb = str(
                        round(
                            value["shunt_barra"],
                        )
                    )
                elif (
                    value["shunt_barra"] / 1e3 >= 0.1
                    and value["shunt_barra"] / 1e3 < 1.0
                ):
                    sb = str(round(value["shunt_barra"], 1))
                else:
                    sb = str(round(value["shunt_barra"], 2))
            else:
                if value["shunt_barra"] / 1e3 < -0.1:
                    sb = str(
                        round(
                            value["shunt_barra"],
                        )
                    )
                else:
                    sb = str(round(value["shunt_barra"], 1))
        else:
            sb = 5 * " "
        file.write(
            f"{value['numero']:>5}{'M':1}{26*' ':>26}{value['potencia_ativa']:>5}{21*' ':21}{pl:>5}{ql:>5}{sb:>5}{value['area']:>3}{35*' ':>35}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udctg(
    dctg,
    dctg1,
    dctg2,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    ctg = 0
    file.write(format(dctg["dctg"]))
    for idx1, value in dctg1.iterrows():
        file.write(value.ruler)
        file.write(
            f"{value['identificacao']:>4} {value['operacao']:1} {value['prioridade']:>2} {value['nome']:<47}"
        )
        file.write("\n")
        file.write(dctg2.ruler.iloc[0])
        for idx2 in range(0, value["ndctg2"]):
            file.write(
                f"{dctg2.tipo.iloc[idx2 + ctg]:>4} {dctg2.de.iloc[idx2 + ctg]:>5} {dctg2.para.iloc[idx2 + ctg]:>5} {dctg2.circuito.iloc[idx2 + ctg]:>2} {dctg2.extremidade.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa_minima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa_maxima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa_minima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa_maxima.iloc[idx2 + ctg]:>5} {dctg2.variacao_fator_participacao.iloc[idx2 + ctg]:>5}"
            )
            file.write("\n")
        ctg += value["ndctg2"]
        file.write("FCAS")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udger(
    dger,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dger.dger.iloc[0]))
    file.write(format(dger.ruler.iloc[0]))
    for idx, value in dger.iterrows():
        file.write(
            f"{value.numero:>5} {value.operacao:1} {6*' ':>6} {6*' ':>6} {value.fator_participacao:>5} {5*' ':>5} {5*' ':>5} {4*' ':>4} {4*' ':>4} {4*' ':>4} {5*' ':>5} {5*' ':>5}{6*' ':>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udinc(
    dinc,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dinc.dinc.iloc[0]))
    file.write(format(dinc.ruler.iloc[0]))
    for idx, value in dinc.iterrows():
        file.write(
            f"{value['tipo_incremento_1']:>4} {value['identificacao_incremento_1']:>5} {value['condicao_incremento_1']:1} {value['tipo_incremento_2']:>4} {value['identificacao_incremento_2']:>5} {value['condicao_incremento_2']:1} {value['tipo_incremento_3']:>4} {value['identificacao_incremento_3']:>5} {value['condicao_incremento_3']:1} {value['tipo_incremento_4']:>4} {value['identificacao_incremento_4']:>5} {value['condicao_incremento_4']:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udmet(
    dmet,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dmet.dmet.iloc[0]))
    file.write(format(dmet.ruler.iloc[0]))
    file.write(f"{'AREA':>4} {'1':>5} {'A':1} {'AREA':>4} {'999':>5}")
    file.write("\n")
    file.write("99999")
    file.write("\n")


def udmfl(
    dmfl,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dmfl.dmfl.iloc[0]))
    file.write(format(dmfl.ruler.iloc[0]))

    for idx, value in dmfl.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['interligacao']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udmfl_circ(
    dmfl,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dmfl.dmfl.iloc[0]))
    file.write(format(dmfl.ruler.iloc[0]))
    for idx, value in dmfl.iterrows():
        file.write(f"{value['de']:>5} {value['para']:>5} {value['circuito']:>2} ")

        if (idx + 1) % 5 == 0:
            file.write(f"{value['operacao']:1}")
            file.write("\n")

    file.write("\n")
    file.write("99999")
    file.write("\n")


def udmte(
    dmte,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write(format(dmte.dinc.iloc[0]))
    file.write(format(dmte.ruler.iloc[0]))
    for idx, value in dmte.iterrows():
        file.write(
            f"{value['tipo_incremento_1']:>4} {value['identificacao_incremento_1']:>5} {value['condicao_incremento_1']:1} {value['tipo_incremento_2']:>4} {value['identificacao_incremento_2']:>5} {value['condicao_incremento_2']:1} {value['tipo_incremento_3']:>4} {value['identificacao_incremento_3']:>5} {value['condicao_incremento_3']:1} {value['tipo_incremento_4']:>4} {value['identificacao_incremento_4']:>5} {value['condicao_incremento_4']:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def usxsc(
    powerflow,
    file,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    file.write("( ")
    file.write("\n")

    file.write("EXLF BPSI")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("2")
    file.write("\n")
    file.write(powerflow.namecase + str(powerflow.ones) + ".SAV")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("ARQV INIC IMPR")
    file.write("\n")
    file.write("SIM")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("ARQV GRAV IMPR NOVO")
    file.write("\n")
    file.write("1")
    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write("EXLF" + powerflow.namecase + str(powerflow.ones) + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXLF BPSI RINT")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")


def usxic(
    powerflow,
    savfile,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder
        + "/SXIC_"
        + powerflow.namecase
        + "{}.pwf".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")

    # Cabecalho
    uheader(
        file,
    )

    # Corpo
    uarq(
        file,
        savfile,
        case=1,
    )

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write("EXIC" + powerflow.namecase + str(powerflow.ones) + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXIC BPSI RINT")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("FIM")


def usxct(
    powerflow,
    savfile,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder
        + "/SXCT_"
        + powerflow.namecase
        + "{}.pwf".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")

    # Cabecalho
    uheader(
        file,
    )

    # Corpo
    uarq(
        file,
        savfile,
        case=1,
    )

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write("EXCT" + powerflow.namecase + str(powerflow.ones) + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXCT BPSI RCVC RINT")
    file.write("\n")
    file.write("(P Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr Pr")
    file.write("\n")
    file.write(" 1  2  3  4  5  6  7  8  9 10 11 12")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("FIM")


def uspvct(
    powerflow,
    savfile,
):
    """

    Args
        powerflow:
        file:
    """

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder
        + "/SPVCT_"
        + powerflow.namecase
        + "{}.pwf".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")

    # Cabecalho
    uheader(
        file,
    )

    # Corpo
    uarq(
        file,
        savfile,
        case=1,
    )

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write("EXICCT" + powerflow.namecase + str(powerflow.ones) + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXIC BPSI PVCT")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("FIM")
