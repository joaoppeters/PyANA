# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, realpath
from datetime import datetime as dt


def rewrite(
    powerflow,
    case,
):
    """inicializacao

    Parametros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicializacao
    # Arquivo
    filedir = realpath(
        dirname(dirname(__file__)) + "/sistemas/" + powerflow.name + "-" + case + ".pwf"
    )

    # Manipulacao
    file = open(filedir, "w")

    # Cabecalho
    writeheader(
        file,
    )

    if powerflow.codes["TITU"]:
        writetitu(
            powerflow,
            file,
        )

    if powerflow.codes["DOPC"]:
        writedopc(
            powerflow,
            file,
        )

    if powerflow.codes["DCTE"]:
        writedcte(
            powerflow,
            file,
        )

    if powerflow.codes["DAGR"]:
        writedagr(
            powerflow,
            file,
        )

    if powerflow.codes["DBAR"]:
        writedbar(
            powerflow,
            file,
        )

    if powerflow.codes["DLIN"]:
        writedlin(
            powerflow,
            file,
        )

    if powerflow.codes["DGER"]:
        writedger(
            powerflow,
            file,
        )

    if powerflow.codes["DSHL"]:
        writedshl(
            powerflow,
            file,
        )

    if powerflow.codes["DBSH"]:
        writedbsh(
            powerflow,
            file,
        )

    if powerflow.codes["DCER"]:
        writedcer(
            powerflow,
            file,
        )

    if powerflow.codes["DARE"]:
        writedare(
            powerflow,
            file,
        )

    if powerflow.codes["DGBT"]:
        writedgbt(
            powerflow,
            file,
        )

    if powerflow.codes["DGLT"]:
        writedglt(
            powerflow,
            file,
        )

    if powerflow.codes["DANC"]:
        writedanc(
            powerflow,
            file,
        )

    if powerflow.codes["DINC"]:
        writedinc(
            powerflow,
            file,
        )

    file.close()


def writeheader(
    file,
):
    """

    Parâmetros
        file
        powerflow
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


def writetitu(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("TITU")
    file.write("\n")
    file.write(format(powerflow.titu))


def writedopc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DOPC IMPR")
    file.write("\n")
    file.write(format(powerflow.dopc.ruler.iloc[0]))
    for idx, value in powerflow.dopcDF.iterrows():
        file.write(f"{value['opcao']:4} {value['padrao']:1} ")

        if (idx + 1) % 10 == 0:
            file.write("\n")

    file.write("\n")
    file.write("99999")
    file.write("\n")


def writedcte(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DCTE")
    file.write("\n")
    file.write(format(powerflow.dcte.ruler.iloc[0]))
    for idx, value in powerflow.dcte.iterrows():
        file.write(f"{value['constante']:<4} {value['valor_constante']:>6} ")

        if (idx + 1) % 6 == 0:
            file.write("\n")
    if (idx + 1) % 6 != 0:
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedagr(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    agr = 0
    file.write("DAGR")
    file.write("\n")
    for idx, value in powerflow.dagr1.iterrows():
        file.write(value.ruler)
        file.write(f"{value['numero']:>3} {value['descricao']:>36}")
        file.write("\n")
        file.write(powerflow.dagr2.ruler.iloc[0])
        for idx in range(0, value["ndagr2"]):
            file.write(
                f"{powerflow.dagr2.numero.iloc[idx + agr]:>3} {powerflow.dagr2.operacao.iloc[idx + agr]:1} {powerflow.dagr2.descricao.iloc[idx + agr]:>36}"
            )
            file.write("\n")
        agr += value["ndagr2"]
        file.write("FAGR")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedbar(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DBAR")
    file.write("\n")
    file.write(format(powerflow.dbar.ruler.iloc[0]))

    # powerflow.dbar = powerflow.dbar.replace(r"^\s*$", "0", regex=True)
    # powerflow.dbar = powerflow.dbar.astype(
    #     {
    #         "numero": "object",
    #         "operacao": "object",
    #         "estado": "object",
    #         "tipo": "object",
    #         "grupo_base_tensao": "object",
    #         "nome": "object",
    #         "grupo_limite_tensao": "object",
    #         "tensao": "object",
    #         "angulo": "object",
    #         "potencia_ativa": "object",
    #         "potencia_reativa": "object",
    #         "potencia_reativa_minima": "object",
    #         "potencia_reativa_maxima": "object",
    #         "barra_controlada": "object",
    #         "demanda_ativa": "float",
    #         "demanda_reativa": "float",
    #         "shunt_barra": "float",
    #         "area": "object",
    #         "tensao_base": "object",
    #         "modo": "object",
    #         "agreg1": "object",
    #         "agreg2": "object",
    #         "agreg3": "object",
    #         "agreg4": "object",
    #         "agreg5": "object",
    #         "agreg6": "object",
    #         "agreg7": "object",
    #         "agreg8": "object",
    #         "agreg9": "object",
    #         "agreg10": "object",
    #     }
    # )

    for idx, value in powerflow.dbar.iterrows():
        if value["demanda_ativa"] != 5 * " ":
            value["demanda_ativa"] = float(value["demanda_ativa"])
            if value["demanda_ativa"] >= 0.0:
                if value["demanda_ativa"] / 1e3 >= 1.0:
                    pl = str(round(value["demanda_ativa"] * 1.1))
                elif (
                    value["demanda_ativa"] / 1e3 >= 0.1
                    and value["demanda_ativa"] / 1e3 < 1.0
                ):
                    pl = str(round(value["demanda_ativa"] * 1.1, 1))
                else:
                    pl = str(round(value["demanda_ativa"] * 1.1, 2))
            else:
                if value["demanda_ativa"] / 1e3 < -0.1:
                    pl = str(round(value["demanda_ativa"] * 1.1))
                else:
                    pl = str(round(value["demanda_ativa"] * 1.1, 1))
        else:
            pl = 5 * " "

        if value["demanda_reativa"] != 5 * " ":
            value["demanda_reativa"] = float(value["demanda_reativa"])
            if value["demanda_reativa"] >= 0.0:
                if value["demanda_reativa"] / 1e3 >= 1.0:
                    ql = str(round(value["demanda_reativa"] * 1.1))
                elif (
                    value["demanda_reativa"] / 1e3 >= 0.1
                    and value["demanda_reativa"] / 1e3 < 1.0
                ):
                    ql = str(round(value["demanda_reativa"] * 1.1, 1))
                else:
                    ql = str(round(value["demanda_reativa"] * 1.1, 2))
            else:
                if value["demanda_reativa"] / 1e3 < -0.1:
                    ql = str(round(value["demanda_reativa"] * 1.1))
                else:
                    ql = str(round(value["demanda_reativa"] * 1.1, 1))
        else:
            ql = 5 * " "

        if value["shunt_barra"] != 5 * " ":
            value["shunt_barra"] = float(value["shunt_barra"])
            if value["shunt_barra"] >= 0.0:
                if value["shunt_barra"] / 1e3 >= 1.0:
                    sb = str(round(value["shunt_barra"] * 1.1))
                elif (
                    value["shunt_barra"] / 1e3 >= 0.1
                    and value["shunt_barra"] / 1e3 < 1.0
                ):
                    sb = str(round(value["shunt_barra"] * 1.1, 1))
                else:
                    sb = str(round(value["shunt_barra"] * 1.1, 2))
            else:
                if value["shunt_barra"] / 1e3 < -0.1:
                    sb = str(round(value["shunt_barra"] * 1.1))
                else:
                    sb = str(round(value["shunt_barra"] * 1.1, 1))
        else:
            sb = 5 * " "
        file.write(
            f"{value['numero']:>5}{value['operacao']:1}{value['estado']:1}{value['tipo']:1}{value['grupo_base_tensao']:>2}{value['nome']:^12}{value['grupo_limite_tensao']:>2}{value['tensao']:>4}{value['angulo']:>4}{value['potencia_ativa']:>5}{value['potencia_reativa']:>5}{value['potencia_reativa_minima']:>5}{value['potencia_reativa_maxima']:>5}{value['barra_controlada']:>6}{pl:>5}{ql:>5}{sb:>5}{value['area']:>3}{value['tensao_base']:>4}{value['modo']:1}{value['agreg1']:<3}{value['agreg2']:<3}{value['agreg3']:<3}{value['agreg4']:<3}{value['agreg5']:<3}{value['agreg6']:<3}{value['agreg7']:<3}{value['agreg8']:<3}{value['agreg9']:<3}{value['agreg10']:<3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedlin(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DLIN")
    file.write("\n")
    file.write(format(powerflow.dlin.ruler.iloc[0]))
    for idx, value in powerflow.dlin.iterrows():
        file.write(
            f"{value['de']:>5}{value['abertura_de']:1} {value['operacao']:1} {value['abertura_para']:1}{value['para']:>5}{value['circuito']:>2}{value['estado']:1}{value['proprietario']:1}{value['manobravel']:1}{value['resistencia']:>6}{value['reatancia']:>6}{value['susceptancia']:>6}{value['tap']:>5}{value['tap_minimo']:>5}{value['tap_maximo']:>5}{value['tap_defasagem']:>5}{value['barra_controlada']:>6}{value['capacidade_normal']:>4}{value['capacidade_emergencial']:>4}{value['numero_taps']:>2}{value['capacidade_equipamento']:>4}{value['agreg1']:>3}{value['agreg2']:>3}{value['agreg3']:>3}{value['agreg4']:>3}{value['agreg5']:>3}{value['agreg6']:>3}{value['agreg7']:>3}{value['agreg8']:>3}{value['agreg9']:>3}{value['agreg10']:>3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedger(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DGER")
    file.write("\n")
    file.write(format(powerflow.dger.ruler.iloc[0]))
    for idx, value in powerflow.dger.iterrows():
        file.write(
            f"{value['numero']:>5} {value['operacao']:1} {value['potencia_ativa_minima']:>6} {value['potencia_ativa_maxima']:>6} {value['fator_participacao']:>5} {value['fator_participacao_controle_remoto']:>5} {value['fator_potencia_nominal']:>5} {value['fator_servico_armadura']:>4} {value['fator_servico_rotor']:>4} {value['angulo_maximo_carga']:>4} {value['reatancia_maquina']:>5} {value['potencia_aparente_nominal']:>5}{value['estatismo']}:>6"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedbsh(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    bsh = 0
    file.write("DBSH")
    file.write("\n")
    for idx, value in powerflow.dbsh1.iterrows():
        file.write(value.ruler)
        file.write(
            f"{value['from']:>5} {value['operacao']:1} {value['to']:>5} {value['circuito']:>2} {value['modo_controle']:1} {value['tensao_minima']:>4} {value['tensao_maxima']:>4} {value['barra_controlada']:>5} {value['injecao_reativa_inicial']:>6} {value['tipo_controle']:1} {value['apagar']:1} {value['extremidade']:>5}"
        )
        file.write("\n")
        file.write(powerflow.dbsh2.ruler.iloc[0])
        for idx in range(0, value["ndbsh2"]):
            file.write(
                f"{powerflow.dbsh2.grupo_banco.iloc[idx + bsh]:>2}  {powerflow.dbsh2.operacao.iloc[idx + bsh]:1} {powerflow.dbsh2.estado.iloc[idx + bsh]:1} {powerflow.dbsh2.unidades.iloc[idx + bsh]:>3} {powerflow.dbsh2.unidades_operacao.iloc[idx + bsh]:>3} {powerflow.dbsh2.capacitor_reator.iloc[idx + bsh]:>6}"
            )
            file.write("\n")
        bsh += value["ndbsh2"]
        file.write("FBAN")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedshl(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DSHL")
    file.write("\n")
    file.write(format(powerflow.dshl.ruler.iloc[0]))
    for idx, value in powerflow.dshl.iterrows():
        file.write(
            f"{value['from']:>5} {value['operacao']:1}  {value['to']:>5}{value['circuito']:>2} {value['shunt_from']:>6}{value['shunt_to']:>6} {value['estado_shunt_from']:>2} {value['estado_shunt_to']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedinj(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    file.write("DINJ")
    file.write("\n")
    file.write(format(powerflow.dinj.ruler.iloc[0]))
    for idx, value in powerflow.dinj.iterrows():
        file.write(
            f"{value['numero']:>3} {value['injecao_ativa']:>6} {value['injecao_reativa']:>6} {value['barra']:>5}"
        )
        file.write("\n")


def writedcer(
    powerflow,
    file,
):
    """

    Parâmetros:
        powerflow (_type_): _description_
        file (_type_): _description_
    """
    ## Inicialização
    file.write("DCER")
    file.write("\n")
    file.write(format(powerflow.dcer.ruler.iloc[0]))
    for idx, value in powerflow.dcer.iterrows():
        file.write(
            f"{value['barra']:>5} {value['operacao']:1} {value['grupo_base']:>2} {value['unidades']:>2} {value['barra_controlada']:>5} {value['droop']:>6} {value['potencia_reativa']:>5}{value['potencia_reativa_minima']:>5}{value['potencia_reativa_maxima']:>5} {value['controle']:1} {value['estado']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedare(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DARE")
    file.write("\n")
    file.write(format(powerflow.dare.ruler.iloc[0]))
    for idx, value in powerflow.dare.iterrows():
        file.write(
            f"{value['numero']:3}    {value['intercambio_liquido']:>6}     {value['nome']:^35} {value['intercambio_minimo']:>6} {value['intercambio_maximo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedgbt(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DGBT")
    file.write("\n")
    file.write(format(powerflow.dgbt.ruler.iloc[0]))
    for idx, value in powerflow.dgbt.iterrows():
        file.write(f"{value['grupo']:2} {value['tensao']:>5}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedglt(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DGLT")
    file.write("\n")
    file.write(format(powerflow.dglt.ruler.iloc[0]))
    for idx, value in powerflow.dglt.iterrows():
        file.write(
            f"{value['grupo']:2} {str(value['limite_minimo']):>5} {str(value['limite_maximo']):>5} {str(value['limite_minimo_E']):>5} {str(value['limite_maximo_E']):>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedanc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DANC")
    file.write("\n")
    file.write(format(powerflow.danc.ruler.iloc[0]))
    for idx, value in powerflow.danc.iterrows():
        file.write(
            f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedinc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    file.write("DINC")
    file.write("\n")
    file.write(format(powerflow.dinc.ruler.iloc[0]))
    for idx, value in powerflow.dinc.iterrows():
        file.write(
            f"{value['tipo_incremento_1']:>4} {value['identificacao_incremento_1']:>5} {value['condicao_incremento_1']:1} {value['tipo_incremento_2']:>4} {value['identificacao_incremento_2']:>5} {value['condicao_incremento_2']:1} {value['tipo_incremento_3']:>4} {value['identificacao_incremento_3']:>5} {value['condicao_incremento_3']:1} {value['tipo_incremento_4']:>4} {value['identificacao_incremento_4']:>5} {value['condicao_incremento_4']:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writetail(
    powerflow,
    file,
):
    """

    Parâmetros
        file
        powerflow
    """

    ## Inicialização
    file.write("(")
    file.write("\n")

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("2")
    file.write("\n")
    file.write(powerflow.namecase + ".SAV")

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
    file.write("01")
    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("ULOG")
    file.write("\n")
    file.write("(N")
    file.write("\n")
    file.write("4")
    file.write("\n")
    file.write(powerflow.namecase + ".REL")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("RELA FILE 80CO")

    file.write("\n")
    file.write("( ")
    file.write("\n")

    file.write("FIM")
