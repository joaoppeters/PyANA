# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def uheader(
    file,
):
    """

    Args
        file:
    """

    from datetime import datetime as dt

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
        if "EOL" not in value.nome:
            pg = 5 * " "
        else:
            # Positive numbers
            if value.potencia_ativa >= 10000:
                pg = f"{int(value.potencia_ativa)}"[
                    :5
                ]  # i) Maintain 5 digits (truncate without decimal point)
            elif value.potencia_ativa >= 1000:
                pg = f"{value.potencia_ativa:.4g}"  # ii) Maintain 4 digits, include decimal point
            elif value.potencia_ativa >= 100:
                pg = f"{value.potencia_ativa:.3g}"  # iii) Maintain 3 digits, include one decimal
            elif value.potencia_ativa >= 10:
                pg = f"{value.potencia_ativa:.2g}"  # iv) Maintain 2 digits, include two decimals
            elif value.potencia_ativa >= 1:
                pg = f"{value.potencia_ativa:.3f}".rstrip("0").rstrip(".")[
                    :5
                ]  # v) Maintain 1 digit and up to 3 decimals
            else:
                pg = f"{value.potencia_ativa:.4f}".rstrip("0")[
                    :5
                ]  # xi) Maintain 4 decimal places for small values

        if value.demanda_ativa > 0:
            # Positive numbers
            if value.demanda_ativa >= 10000:
                pl = f"{int(value.demanda_ativa)}"[
                    :5
                ]  # i) Maintain 5 digits (truncate without decimal point)
            elif value.demanda_ativa >= 1000:
                pl = f"{value.demanda_ativa:.4g}"  # ii) Maintain 4 digits, include decimal point
            elif value.demanda_ativa >= 100:
                pl = f"{value.demanda_ativa:.3g}"  # iii) Maintain 3 digits, include one decimal
            elif value.demanda_ativa >= 10:
                pl = f"{value.demanda_ativa:.2g}"  # iv) Maintain 2 digits, include two decimals
            elif value.demanda_ativa >= 1:
                pl = f"{value.demanda_ativa:.3f}".rstrip("0").rstrip(".")[
                    :5
                ]  # v) Maintain 1 digit and up to 3 decimals
            else:
                pl = f"{value.demanda_ativa:.4f}".rstrip("0")[
                    :5
                ]  # xi) Maintain 4 decimal places for small values
        elif value.demanda_ativa < 0:
            # Negative numbers
            if value.demanda_ativa <= -100:
                pl = f"{int(value.demanda_ativa):d}"  # vii) Maintain 4 digits without decimal point
            elif value.demanda_ativa <= -10:
                pl = f"{value.demanda_ativa:.1f}"  # viii) Maintain 3 digits with decimal point
            elif value.demanda_ativa <= -1:
                pl = f"{value.demanda_ativa:.2f}"[
                    :5
                ]  # ix) Maintain 2 digits and one decimal
            elif value.demanda_ativa > -1:
                pl = f"{value.demanda_ativa:.3f}"[
                    :5
                ]  # xii) Maintain decimal point and up to 3 decimals
        else:
            pl = 5 * " "

        if value.demanda_reativa > 0:
            # Positive numbers
            if value.demanda_reativa >= 10000:
                ql = f"{int(value.demanda_reativa)}"[
                    :5
                ]  # i) Maintain 5 digits (truncate without decimal point)
            elif value.demanda_reativa >= 1000:
                ql = f"{value.demanda_reativa:.4g}"  # ii) Maintain 4 digits, include decimal point
            elif value.demanda_reativa >= 100:
                ql = f"{value.demanda_reativa:.3g}"  # iii) Maintain 3 digits, include one decimal
            elif value.demanda_reativa >= 10:
                ql = f"{value.demanda_reativa:.2g}"  # iv) Maintain 2 digits, include two decimals
            elif value.demanda_reativa >= 1:
                ql = f"{value.demanda_reativa:.3f}".rstrip("0").rstrip(".")[
                    :5
                ]  # v) Maintain 1 digit and up to 3 decimals
            else:
                ql = f"{value.demanda_reativa:.4f}".rstrip("0")[
                    :5
                ]  # xi) Maintain 4 decimal places for small values
        elif value.demanda_reativa < 0:
            # Negative numbers
            if value.demanda_reativa <= -100:
                ql = f"{int(value.demanda_reativa)}"  # vii) Maintain 4 digits without decimal point
            elif value.demanda_reativa <= -10:
                ql = f"{int(value.demanda_reativa)}"  # viii) Maintain 3 digits with decimal point
            elif value.demanda_reativa <= -1:
                ql = f"{value.demanda_reativa:.2f}"[
                    :5
                ]  # ix) Maintain 2 digits and one decimal
            elif value.demanda_reativa > -1:
                ql = f"{value.demanda_reativa:.3f}"[
                    :5
                ]  # xii) Maintain decimal point and up to 3 decimals
        else:
            ql = 5 * " "

        if value.shunt_barra > 0:
            # Positive numbers
            if value.shunt_barra >= 10000:
                sb = f"{int(value.shunt_barra)}"[
                    :5
                ]  # i) Maintain 5 digits (truncate without decimal point)
            elif value.shunt_barra >= 1000:
                sb = f"{value.shunt_barra:.4g}"  # ii) Maintain 4 digits, include decimal point
            elif value.shunt_barra >= 100:
                sb = f"{value.shunt_barra:.3g}"  # iii) Maintain 3 digits, include one decimal
            elif value.shunt_barra >= 10:
                sb = f"{value.shunt_barra:.2g}"  # iv) Maintain 2 digits, include two decimals
            elif value.shunt_barra >= 1:
                sb = f"{value.shunt_barra:.3f}".rstrip("0").rstrip(".")[
                    :5
                ]  # v) Maintain 1 digit and up to 3 decimals
            else:
                sb = f"{value.shunt_barra:.4f}".rstrip("0")[
                    :5
                ]  # xi) Maintain 4 decimal places for small values
        elif value.shunt_barra < 0:
            # Negative numbers
            if value.shunt_barra <= -100:
                sb = f"{int(value.shunt_barra):d}"  # vii) Maintain 4 digits without decimal point
            elif value.shunt_barra <= -10:
                sb = f"{value.shunt_barra:.1f}"  # viii) Maintain 3 digits with decimal point
            elif value.shunt_barra <= -1:
                sb = f"{value.shunt_barra:.2f}"[
                    :5
                ]  # ix) Maintain 2 digits and one decimal
            elif value.shunt_barra > -1:
                sb = f"{value.shunt_barra:.3f}"[
                    :5
                ]  # xii) Maintain decimal point and up to 3 decimals
        else:
            sb = 5 * " "
        file.write(
            f"{value.numero:>5}{'M':1}{26*' ':>26}{pg:>5}{21*' ':21}{pl:>5}{ql:>5}{sb:>5}{value.area:>3}{35*' ':>35}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def udctg(
    dctg,
    value,
    ctg,
    dctg2,
    file,
):
    """

    Args
        powerflow:
        file:
    """
    ## Inicialização
    file.write(format(dctg["dctg"]))
    file.write(value.ruler)
    file.write(
        f"{value.identificacao:>4} {value.operacao:1} {value.prioridade:>2} {value.nome:<47}"
    )
    file.write("\n")
    file.write(dctg2.ruler.iloc[0])
    for idx2 in range(0, value.ndctg2):
        file.write(
            f"{dctg2.tipo.iloc[idx2 + ctg]:>4} {dctg2.de.iloc[idx2 + ctg]:>5} {dctg2.para.iloc[idx2 + ctg]:>5} {dctg2.circuito.iloc[idx2 + ctg]:>2} {dctg2.extremidade.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa_minima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_ativa_maxima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa_minima.iloc[idx2 + ctg]:>5} {dctg2.variacao_geracao_reativa_maxima.iloc[idx2 + ctg]:>5} {dctg2.variacao_fator_participacao.iloc[idx2 + ctg]:>5}"
        )
        file.write("\n")
    file.write("FCAS")
    file.write("\n")
    file.write("99999")
    file.write("\n")
    return ctg + value.ndctg2


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
            f"{value.numero:>5} {value.operacao:1} {6*' ':>6} {6*' ':>6} {value.fator_participacao:>5.2f} {5*' ':>5} {5*' ':>5} {4*' ':>4} {4*' ':>4} {4*' ':>4} {5*' ':>5} {5*' ':>5}{6*' ':>6}"
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
            f"{value.tipo_incremento_1:>4} {value.identificacao_incremento_1:>5} {value.condicao_incremento_1:1} {value.tipo_incremento_2:>4} {value.identificacao_incremento_2:>5} {value.condicao_incremento_2:1} {value.tipo_incremento_3:>4} {value.identificacao_incremento_3:>5} {value.condicao_incremento_3:1} {value.tipo_incremento_4:>4} {value.identificacao_incremento_4:>5} {value.condicao_incremento_4:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def sdinc(
    dinc,
    file,
    var,
):
    """

    Args
        dinc:
        inc:
        file:
    """
    ## Inicialização
    file.write(format(dinc.dinc.iloc[0]))
    file.write(format(dinc.ruler.iloc[0]))
    for idx, value in dinc.iterrows():
        file.write(
            f"{value.tipo_incremento_1:>4} {value.identificacao_incremento_1:>5} {value.condicao_incremento_1:1} {value.tipo_incremento_2:>4} {value.identificacao_incremento_2:>5} {value.condicao_incremento_2:1} {value.tipo_incremento_3:>4} {value.identificacao_incremento_3:>5} {value.condicao_incremento_3:1} {value.tipo_incremento_4:>4} {value.identificacao_incremento_4:>5} {value.condicao_incremento_4:1} {var[0]:>5} {var[1]:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
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
            f"{value.tipo_incremento_1:>4} {value.identificacao_incremento_1:>5} {value.condicao_incremento_1:1} {value.tipo_incremento_2:>4} {value.identificacao_incremento_2:>5} {value.condicao_incremento_2:1} {value.tipo_incremento_3:>4} {value.identificacao_incremento_3:>5} {value.condicao_incremento_3:1} {value.tipo_incremento_4:>4} {value.identificacao_incremento_4:>5} {value.condicao_incremento_4:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def uxlftail(
    powerflow,
    file,
    base=False,
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
    if base:
        file.write("EXLF_" + powerflow.name + ".SAV")
    else:
        file.write("EXLF_" + powerflow.namecase + str(powerflow.ones) + ".SAV")

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
    if base:
        file.write("EXLF_" + powerflow.name + ".REL")
    else:
        file.write("EXLF_" + powerflow.namecase + str(powerflow.ones) + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXLF BPSI RBAR RINT RTOT")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")
    file.close()


def uxictail(
    file,
    filename,
    var,
    start,
):
    """

    Args
        file:
        filename:
        var:
        start:
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
    file.write("EXIC_" + filename + ".SAV")

    file.write("\n")
    file.write("(")
    file.write("\n")

    if var == start:
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
    else:
        file.write("ARQV GRAV IMPR")
        file.write("\n")
        file.write("{}".format(var - (start - 1)))
        file.write("\n")
        file.write("(")
        file.write("\n")

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write("EXIC_" + filename + "_{}.REL".format(var - (start - 1)))

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("EXIC BPSI RTOT")

    file.write("\n")
    file.write("( ")
    file.write("\n")
