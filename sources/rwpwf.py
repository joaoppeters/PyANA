# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import realpath
from datetime import datetime as dt


def rwpwf(
    powerflow,
):
    """Inicialização

    Args
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Arquivo
    powerflow.filedir = realpath(
        powerflow.filefolder + "/" + powerflow.namecase + "{}.pwf".format(powerflow.ones)
    )

    # Manipulacao
    file = open(powerflow.filedir, "w")

    # Cabecalho
    wheader(
        file,
    )

    if powerflow.codes["TITU"]:
        wtitu(
            powerflow,
            file,
        )

    if powerflow.codes["DOPC"]:
        wdopc(
            powerflow,
            file,
        )

    if powerflow.codes["DCTE"]:
        wdcte(
            powerflow,
            file,
        )

    if powerflow.codes["DBAR"]:
        wdbar(
            powerflow,
            file,
        )

    if powerflow.codes["DLIN"]:
        wdlin(
            powerflow,
            file,
        )

    if powerflow.codes["DCSC"]:
        wdcsc(
            powerflow,
            file,
        )

    if powerflow.codes["DBSH"]:
        wdbsh(
            powerflow,
            file,
        )

    if powerflow.codes["DGER"]:
        wdger(
            powerflow,
            file,
        )

    if powerflow.codes["DCER"]:
        wdcer(
            powerflow,
            file,
        )

    if powerflow.codes["DCTR"]:
        wdctr(
            powerflow,
            file,
        )

    if powerflow.codes["DGLT"]:
        wdglt(
            powerflow,
            file,
        )

    if powerflow.codes["DARE"]:
        wdare(
            powerflow,
            file,
        )

    if powerflow.codes["DTPF"]:
        if "CIRC" in powerflow.dtpf.dtpf.iloc[0]:
            wdtpf_circ(
                powerflow,
                file,
            )
        else:
            wdtpf(
                powerflow,
                file,
            )

    if powerflow.codes["DELO"]:
        wdelo(
            powerflow,
            file,
        )

    if powerflow.codes["DCBA"]:
        wdcba(
            powerflow,
            file,
        )

    if powerflow.codes["DCLI"]:
        wdcli(
            powerflow,
            file,
        )

    if powerflow.codes["DCNV"]:
        wdcnv(
            powerflow,
            file,
        )

    if powerflow.codes["DCCV"]:
        wdccv(
            powerflow,
            file,
        )

    if powerflow.codes["DGBT"]:
        wdgbt(
            powerflow,
            file,
        )

    if powerflow.codes["DAGR"]:
        wdagr(
            powerflow,
            file,
        )

    if powerflow.codes["DANC"]:
        if "ACLS" in powerflow.danc.danc.iloc[0]:
            wdanc_acls(
                powerflow,
                file,
            )
        else:
            wdanc(
                powerflow,
                file,
            )

    if powerflow.codes["DCAR"]:
        wdcar(
            powerflow,
            file,
        )

    if powerflow.codes["DINC"]:
        wdinc(
            powerflow,
            file,
        )

    if powerflow.codes["DINJ"]:
        wdinj(
            powerflow,
            file,
        )

    if powerflow.codes["DSHL"]:
        wdshl(
            powerflow,
            file,
        )

    if powerflow.codes["DCTG"]:
        wdctg(
            powerflow,
            file,
        )

    wtail(
        powerflow,
        file,
    )

    file.close()


def wheader(
    file,
):
    """

    Args
        file: arquivo de saída
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


def wtitu(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.titu["titu"]))
    file.write(format(powerflow.titu["ruler"]))


def wdagr(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    agr = 0
    file.write(format(powerflow.dagr.dagr.iloc[0]))
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


def wdanc(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.danc.danc.iloc[0]))
    file.write(format(powerflow.danc.ruler.iloc[0]))
    if "ACLS" in powerflow.danc.danc:
        pass
    else:
        for idx, value in powerflow.danc.iterrows():
            file.write(
                f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6}"
            )
            file.write("\n")
    file.write("99999")
    file.write("\n")


def wdanc_acls(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.danc.danc.iloc[0]))
    file.write(format(powerflow.danc.ruler.iloc[0]))
    for idx, value in powerflow.danc.iterrows():
        file.write(
            f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6} {value['ACLS']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdare(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dare.dare.iloc[0]))
    file.write(format(powerflow.dare.ruler.iloc[0]))
    for idx, value in powerflow.dare.iterrows():
        file.write(
            f"{value['numero']:3}    {value['intercambio_liquido']:>6}     {value['nome']:^35} {value['intercambio_minimo']:>6} {value['intercambio_maximo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdbar(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dbar.dbar.iloc[0]))
    file.write(format(powerflow.dbar.ruler.iloc[0]))

    for idx, value in powerflow.dbar.iterrows():
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
            f"{value['numero']:>5}{value['operacao']:1}{value['estado']:1}{value['tipo']:1}{value['grupo_base_tensao']:>2}{value['nome']:^12}{value['grupo_limite_tensao']:>2}{value['tensao']:>4}{value['angulo']:>4}{value['potencia_ativa']:>5}{value['potencia_reativa']:>5}{value['potencia_reativa_minima']:>5}{value['potencia_reativa_maxima']:>5}{value['barra_controlada']:>6}{pl:>5}{ql:>5}{sb:>5}{value['area']:>3}{value['tensao_base']:>4}{value['modo']:1}{value['agreg1']:<3}{value['agreg2']:<3}{value['agreg3']:<3}{value['agreg4']:<3}{value['agreg5']:<3}{value['agreg6']:<3}{value['agreg7']:<3}{value['agreg8']:<3}{value['agreg9']:<3}{value['agreg10']:<3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdbsh(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    bsh = 0
    file.write(format(powerflow.dbsh["dbsh"]))
    for idx1, value in powerflow.dbsh1.iterrows():
        file.write(value.ruler)
        file.write(
            f"{value['from']:>5} {value['operacao']:1} {value['to']:>5} {value['circuito']:>2} {value['modo_controle']:1} {value['tensao_minima']:>4} {value['tensao_maxima']:>4} {value['barra_controlada']:>5} {value['injecao_reativa_inicial']:>6} {value['tipo_controle']:1} {value['apagar']:1} {value['extremidade']:>5}"
        )
        file.write("\n")
        file.write(powerflow.dbsh2.ruler.iloc[0])
        for idx2 in range(0, value["ndbsh2"]):
            file.write(
                f"{powerflow.dbsh2.grupo_banco.iloc[idx2 + bsh]:>2}  {powerflow.dbsh2.operacao.iloc[idx2 + bsh]:1} {powerflow.dbsh2.estado.iloc[idx2 + bsh]:1} {powerflow.dbsh2.unidades.iloc[idx2 + bsh]:>3} {powerflow.dbsh2.unidades_operacao.iloc[idx2 + bsh]:>3} {powerflow.dbsh2.capacitor_reator.iloc[idx2 + bsh]:>6} {powerflow.dbsh2.manobravel.iloc[idx2 + bsh]:1}"
            )
            file.write("\n")
        bsh += value["ndbsh2"]
        file.write("FBAN")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcar(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcar.dcar.iloc[0]))
    file.write(format(powerflow.dcar.ruler.iloc[0]))

    for idx, value in powerflow.dcar.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['parametro_A']:>3} {value['parametro_B']:>3} {value['parametro_C']:>3} {value['parametro_D']:>3} {value['tensao_limite']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcba(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcba.dcba.iloc[0]))
    file.write(format(powerflow.dcba.ruler.iloc[0]))

    for idx, value in powerflow.dcba.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['tipo']:1}{value['polaridade']:1}{value['nome']:>11}{value['grupo_limite_tensao']:>2}{value['tensao']:>5}                                      {value['eletrodo_terra']:>5}{value['numero_elo_cc']:>4}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdccv(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dccv.dccv.iloc[0]))
    file.write(format(powerflow.dccv.ruler.iloc[0]))

    for idx, value in powerflow.dccv.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['folga']:1}{value['modo_controle_inversor']:1}{value['tipo_controle_conversor']:1} {value['valor_especificado']:>5} {value['margem_corrente']:>5} {value['maxima_sobrecorrente']:>5} {value['angulo_conversor']:>5} {value['angulo_conversor_minimo']:>5} {value['angulo_conversor_maximo']:>5} {value['tap_transformador_minimo']:>5} {value['tap_transformador_maximo']:>5} {value['tap_transformador_numero']:>2} {value['tensao_cc_minima']:>4} {value['tap_high']:>5} {value['tap_reduzido']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcer(
    powerflow,
    file,
):
    """

    Args:
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcer.dcer.iloc[0]))
    file.write(format(powerflow.dcer.ruler.iloc[0]))
    for idx, value in powerflow.dcer.iterrows():
        file.write(
            f"{value['barra']:>5} {value['operacao']:1} {value['grupo_base']:>2} {value['unidades']:>2} {value['barra_controlada']:>5} {value['droop']:>6} {value['potencia_reativa']:>5}{value['potencia_reativa_minima']:>5}{value['potencia_reativa_maxima']:>5} {value['controle']:1} {value['estado']:1} {value['modo_correcao_limites']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcli(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcli.dcli.iloc[0]))
    file.write(format(powerflow.dcli.ruler.iloc[0]))

    for idx, value in powerflow.dcli.iterrows():
        file.write(
            f"{value['de']:>4} {value['operacao']:1}  {value['para']:>4}{value['circuito']:>2} {value['proprietario']:1} {value['resistencia']:>6}{value['indutancia']:>6}                               {value['capacidade']:>4}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcnv(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcnv.dcnv.iloc[0]))
    file.write(format(powerflow.dcnv.ruler.iloc[0]))

    for idx, value in powerflow.dcnv.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['barra_CA']:>5} {value['barra_CC']:>4} {value['barra_neutra']:>4} {value['modo_operacao']:1} {value['pontes']:1} {value['corrente']:>5} {value['reatancia_comutacao']:>5} {value['tensao_secundario']:>5} {value['potencia_transformador']:>5} {value['resistencia_reator']:>5} {value['indutancia_reator']:>5} {value['capacitancia']:>5} {value['frequencia']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcsc(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcsc.dcsc.iloc[0]))
    file.write(format(powerflow.dcsc.ruler.iloc[0]))

    for idx, value in powerflow.dcsc.iterrows():
        file.write(
            f"{value['de']:>5} {value['operacao']:1}  {value['para']:>5}{value['circuito']:>2}{value['estado']:1}{value['proprietario']:1}{value['bypass']:1}      {value['reatancia_minima']:>6}{value['reatancia_maxima']:>6}{value['reatancia_inicial']:>6}{value['modo_controle']:1} {value['especificado']:>6} {value['extremidade']:>5}{value['estagios']:>3}{value['capacidade_normal']:>4}{value['capacidade_emergencia']:>4}{value['capacidade']:>4}{value['agreg1']:>3}{value['agreg2']:>3}{value['agreg3']:>3}{value['agreg4']:>3}{value['agreg5']:>3}{value['agreg6']:>3}{value['agreg7']:>3}{value['agreg8']:>3}{value['agreg9']:>3}{value['agreg10']:>3}\n"
        )
        # file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcte(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dcte.dcte.iloc[0]))
    file.write(format(powerflow.dcte.ruler.iloc[0]))
    for idx, value in powerflow.dcte.iterrows():
        file.write(f"{value['constante']:<4} {value['valor_constante']:>6} ")

        if (idx + 1) % 6 == 0:
            file.write("\n")
    if (idx + 1) % 6 != 0:
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdctg(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    ctg = 0
    file.write(format(powerflow.dctg["dctg"]))
    for idx1, value in powerflow.dctg1.iterrows():
        file.write(value.ruler)
        file.write(
            f"{value['identificacao']:>4} {value['operacao']:1} {value['prioridade']:>2} {value['nome']:<47}"
        )
        file.write("\n")
        file.write(powerflow.dctg2.ruler.iloc[0])
        for idx2 in range(0, value["ndctg2"]):
            file.write(
                f"{powerflow.dctg2.tipo.iloc[idx2 + ctg]:>4} {powerflow.dctg2.de.iloc[idx2 + ctg]:>5} {powerflow.dctg2.para.iloc[idx2 + ctg]:>5} {powerflow.dctg2.circuito.iloc[idx2 + ctg]:>2} {powerflow.dctg2.extremidade.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_ativa.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_ativa_minima.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_ativa_maxima.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_reativa.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_reativa_minima.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_geracao_reativa_maxima.iloc[idx2 + ctg]:>5} {powerflow.dctg2.variacao_fator_participacao.iloc[idx2 + ctg]:>5}"
            )
            file.write("\n")
        ctg += value["ndctg2"]
        file.write("FCAS")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdctr(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dctr.dctr.iloc[0]))
    file.write(format(powerflow.dctr.ruler.iloc[0]))

    for idx, value in powerflow.dctr.iterrows():
        file.write(
            f"{value['de']:>5} {value['operacao']:1} {value['para']:>5} {value['circuito']:>2} {value['tensao_minima']:>4} {value['tensao_maxima']:>4} {value['tipo_controle_1']:1} {value['modo_controle']:1} {value['fase_minima']:>6} {value['fase_maxima']:>6} {value['tipo_controle_2']:1} {value['valor_especificado']:>6} {value['extremidade']:>5} {value['taps']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdelo(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.delo.delo.iloc[0]))
    file.write(format(powerflow.delo.ruler.iloc[0]))

    for idx, value in powerflow.delo.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['tensao']:>5} {value['base']:>5} {value['nome']:>20} {value['modo_high']:1} {value['estado']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdgbt(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dgbt.dgbt.iloc[0]))
    file.write(format(powerflow.dgbt.ruler.iloc[0]))
    for idx, value in powerflow.dgbt.iterrows():
        file.write(f"{value['grupo']:2} {value['tensao']:>5}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdger(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dger.dger.iloc[0]))
    file.write(format(powerflow.dger.ruler.iloc[0]))
    for idx, value in powerflow.dger.iterrows():
        file.write(
            f"{value['numero']:>5} {value['operacao']:1} {value['potencia_ativa_minima']:>6} {value['potencia_ativa_maxima']:>6} {powerflow.dgerDF.fator_participacao.iloc[idx]:>5.3f} {value['fator_participacao_controle_remoto']:>5} {value['fator_potencia_nominal']:>5} {value['fator_servico_armadura']:>4} {value['fator_servico_rotor']:>4} {value['angulo_maximo_carga']:>4} {value['reatancia_maquina']:>5} {value['potencia_aparente_nominal']:>5}{value['estatismo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdglt(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dglt.dglt.iloc[0]))
    file.write(format(powerflow.dglt.ruler.iloc[0]))
    for idx, value in powerflow.dglt.iterrows():
        file.write(
            f"{value['grupo']:2} {str(value['limite_minimo']):>5} {str(value['limite_maximo']):>5} {str(value['limite_minimo_E']):>5} {str(value['limite_maximo_E']):>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdinc(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dinc.dinc.iloc[0]))
    file.write(format(powerflow.dinc.ruler.iloc[0]))
    for idx, value in powerflow.dinc.iterrows():
        file.write(
            f"{value['tipo_incremento_1']:>4} {value['identificacao_incremento_1']:>5} {value['condicao_incremento_1']:1} {value['tipo_incremento_2']:>4} {value['identificacao_incremento_2']:>5} {value['condicao_incremento_2']:1} {value['tipo_incremento_3']:>4} {value['identificacao_incremento_3']:>5} {value['condicao_incremento_3']:1} {value['tipo_incremento_4']:>4} {value['identificacao_incremento_4']:>5} {value['condicao_incremento_4']:1} {value['passo_incremento_potencia_ativa']:>5} {value['passo_incremento_potencia_reativa']:>5} {value['maximo_incremento_potencia_ativa']:>5} {value['maximo_incremento_potencia_reativa']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdinj(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dinj.dinj.iloc[0]))
    file.write(format(powerflow.dinj.ruler.iloc[0]))
    for idx, value in powerflow.dinj.iterrows():
        file.write(
            f"{value['numero']:>3} {value['injecao_ativa']:>6} {value['injecao_reativa']:>6} {value['barra']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdlin(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dlin.dlin.iloc[0]))
    file.write(format(powerflow.dlin.ruler.iloc[0]))
    for idx, value in powerflow.dlin.iterrows():
        file.write(
            f"{value['de']:>5}{value['abertura_de']:1} {value['operacao']:1} {value['abertura_para']:1}{value['para']:>5}{value['circuito']:>2}{value['estado']:1}{value['proprietario']:1}{value['manobravel']:1}{value['resistencia']:>6}{value['reatancia']:>6}{value['susceptancia']:>6}{value['tap']:>5}{value['tap_minimo']:>5}{value['tap_maximo']:>5}{value['tap_defasagem']:>5}{value['barra_controlada']:>6}{value['capacidade_normal']:>4}{value['capacidade_emergencial']:>4}{value['numero_taps']:>2}{value['capacidade_equipamento']:>4}{value['agreg1']:>3}{value['agreg2']:>3}{value['agreg3']:>3}{value['agreg4']:>3}{value['agreg5']:>3}{value['agreg6']:>3}{value['agreg7']:>3}{value['agreg8']:>3}{value['agreg9']:>3}{value['agreg10']:>3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdopc(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dopc.dopc.iloc[0]))
    file.write(format(powerflow.dopc.ruler.iloc[0]))
    for idx, value in powerflow.dopcDF.iterrows():
        file.write(f"{value['opcao']:4} {value['padrao']:1} ")

        if (idx + 1) % 10 == 0:
            file.write("\n")

    file.write("\nIMPR L FILE L 80CO L")
    file.write("\n")
    file.write("\nRINT L")
    file.write("\n")
    file.write("99999")
    file.write("\n")


def wdshl(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dshl.dshl.iloc[0]))
    file.write(format(powerflow.dshl.ruler.iloc[0]))
    for idx, value in powerflow.dshl.iterrows():
        file.write(
            f"{value['from']:>5} {value['operacao']:1}  {value['to']:>5}{value['circuito']:>2} {value['shunt_from']:>6}{value['shunt_to']:>6} {value['estado_shunt_from']:>2} {value['estado_shunt_to']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdtpf(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dtpf.dtpf.iloc[0]))
    file.write(format(powerflow.dtpf.ruler.iloc[0]))

    for idx, value in powerflow.dtpf.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['interligacao']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdtpf_circ(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write(format(powerflow.dtpf.dtpf.iloc[0]))
    file.write(format(powerflow.dtpf.ruler.iloc[0]))
    for idx, value in powerflow.dtpf.iterrows():
        file.write(f"{value['de']:>5} {value['para']:>5} {value['circuito']:>2} ")

        if (idx + 1) % 5 == 0:
            file.write(f"{value['operacao']:1}")
            file.write("\n")

    file.write("\n")
    file.write("99999")
    file.write("\n")


def wtail(
    powerflow,
    file,
):
    """

    Args
        powerflow: self do arquivo powerflow.py
        file: arquivo de saída
    """

    ## Inicialização
    file.write("(")
    file.write("\n")

    file.write("EXLF BPSI")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")
