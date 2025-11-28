# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import realpath
from datetime import datetime as dt


def rwpwf(
    anarede,
    folder,
):
    """Inicialização

    Args
        anarede:
    """
    ## Inicialização
    # Arquivo
    anarede.filedir = realpath(
        folder + "\\" + anarede.namecase + "{}.pwf".format(anarede.ones)
    )

    # Manipulacao
    file = open(anarede.filedir, "w")

    # Cabecalho
    wheader(
        file,
    )

    if anarede.pwfblock["TITU"]:
        wtitu(
            anarede.titu,
            file,
        )

    if anarede.pwfblock["DOPC"]:
        wdopc(
            anarede.dopc,
            anarede.dopcDF,
            file,
        )

    if anarede.pwfblock["DCTE"]:
        wdcte(
            anarede.dcte,
            file,
        )

    if anarede.pwfblock["DBAR"]:
        wdbar(
            anarede.mdbar,
            file,
        )

    if anarede.pwfblock["DLIN"]:
        wdlin(
            anarede.dlin,
            file,
        )

    if anarede.pwfblock["DCSC"]:
        wdcsc(
            anarede.dcsc,
            file,
        )

    if anarede.pwfblock["DBSH"]:
        wdbsh(
            anarede.dbsh,
            anarede.dbsh1,
            anarede.dbsh2,
            file,
        )

    if anarede.pwfblock["DGER"]:
        wdger(
            anarede.dger,
            anarede.mdger,
            file,
        )

    if anarede.pwfblock["DCER"]:
        wdcer(
            anarede.dcer,
            file,
        )

    if anarede.pwfblock["DCTR"]:
        wdctr(
            anarede.dctr,
            file,
        )

    if anarede.pwfblock["DGLT"]:
        wdglt(
            anarede.dglt,
            file,
        )

    if anarede.pwfblock["DARE"]:
        wdare(
            anarede.dare,
            file,
        )

    if anarede.pwfblock["DTPF"]:
        if "CIRC" in anarede.dtpf.dtpf.iloc[0]:
            wdtpf_circ(
                anarede.dtpf,
                file,
            )
        else:
            wdtpf(
                anarede.dtpf,
                file,
            )

    if anarede.pwfblock["DELO"]:
        wdelo(
            anarede.delo,
            file,
        )

    if anarede.pwfblock["DCBA"]:
        wdcba(
            anarede.dcba,
            file,
        )

    if anarede.pwfblock["DCLI"]:
        wdcli(
            anarede.dcli,
            file,
        )

    if anarede.pwfblock["DCNV"]:
        wdcnv(
            anarede.dcnv,
            file,
        )

    if anarede.pwfblock["DCCV"]:
        wdccv(
            anarede.dccv,
            file,
        )

    if anarede.pwfblock["DGBT"]:
        wdgbt(
            anarede.dgbt,
            file,
        )

    if anarede.pwfblock["DAGR"]:
        wdagr(
            anarede.dagr,
            anarede.dagr1,
            anarede.dagr2,
            file,
        )

    if anarede.pwfblock["DANC"]:
        if "ACLS" in anarede.danc.danc.iloc[0]:
            wdanc_acls(
                anarede.danc,
                file,
            )
        else:
            wdanc(
                anarede.danc,
                file,
            )

    if anarede.pwfblock["DCAR"]:
        wdcar(
            anarede.dcar,
            file,
        )

    if anarede.pwfblock["DINC"]:
        wdinc(
            anarede.dinc,
            file,
        )

    if anarede.pwfblock["DMET"]:
        wdmet(
            anarede.dmte,
            file,
        )

    if anarede.pwfblock["DINJ"]:
        wdinj(
            anarede.dinj,
            file,
        )

    if anarede.pwfblock["DSHL"]:
        wdshl(
            anarede.dshl,
            file,
        )

    if anarede.pwfblock["DCTG"]:
        wdctg(
            anarede.dctg,
            anarede.dctg1,
            anarede.dctg2,
            file,
        )

    if anarede.pwfblock["DMFL"]:
        if "CIRC" in anarede.dmfl.dmfl.iloc[0]:
            wdmfl_circ(
                anarede.dmfl,
                file,
            )
        else:
            wdmfl(
                anarede.dmfl,
                file,
            )

    if anarede.pwfblock["DMTE"]:
        wdmte(
            anarede.dmte,
            file,
        )

    wtail(
        anarede,
        file,
    )

    file.close()


def wheader(
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


def wtitu(
    titu,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(titu["titu"]))
    file.write(format(titu["ruler"]))


def wdagr(
    dagr,
    dagr1,
    dagr2,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    agr = 0
    file.write(format(dagr.dagr.iloc[0]))
    for idx, value in dagr1.iterrows():
        file.write(value.ruler)
        file.write(f"{value['numero']:>3} {value['descricao']:>36}")
        file.write("\n")
        file.write(dagr2.ruler.iloc[0])
        for idx in range(0, value["ndagr2"]):
            file.write(
                f"{dagr2.numero.iloc[idx + agr]:>3} {dagr2.operacao.iloc[idx + agr]:1} {dagr2.descricao.iloc[idx + agr]:>36}"
            )
            file.write("\n")
        agr += value["ndagr2"]
        file.write("FAGR")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdanc(
    danc,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(danc.danc.iloc[0]))
    file.write(format(danc.ruler.iloc[0]))
    if "ACLS" in danc.danc:
        pass
    else:
        for idx, value in danc.iterrows():
            file.write(
                f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6}"
            )
            file.write("\n")
    file.write("99999")
    file.write("\n")


def wdanc_acls(
    danc,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(danc.danc.iloc[0]))
    file.write(format(danc.ruler.iloc[0]))
    for idx, value in danc.iterrows():
        file.write(
            f"{value['numero']:>3} {value['fator_carga_ativa']:>6} {value['fator_carga_reativa']:>6} {value['fator_shunt_barra']:>6} {value['ACLS']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdare(
    dare,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dare.dare.iloc[0]))
    file.write(format(dare.ruler.iloc[0]))
    for idx, value in dare.iterrows():
        file.write(
            f"{value['numero']:3}    {value['intercambio_liquido']:>6}     {value['nome']:^35} {value['intercambio_minimo']:>6} {value['intercambio_maximo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdbar(
    dbar,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dbar.dbar.iloc[0]))
    file.write(format(dbar.ruler_x.iloc[0]))
    for idx, value in dbar.iterrows():
        ag = str(value.angulo)[:4]
        pg = str(value.potencia_ativa)[:5]
        qg = str(value.potencia_reativa)[:5]
        qn = str(value.potencia_reativa_minima)[:5]
        qx = str(value.potencia_reativa_maxima)[:5]
        pl = str(value.demanda_ativa)[:5]
        ql = str(value.demanda_reativa)[:5]
        sb = str(value.shunt_barra)[:5]
        if value.barra_controlada == 0.0:
            bc = 6 * " "
        else:
            bc = f"{int(value.barra_controlada):>6}"
        file.write(
            f"{value['numero']:>5}{' ':1}{value.estado:1}{value['tipo']:1}{value['grupo_base_tensao']:>2}{value['nome']:^12}{value['grupo_limite_tensao']:>2}{int(value['tensao']):>4}{ag:>4}{pg:>5}{qg:>5}{qn:>5}{qx:>5}{bc:>6}{pl:>5}{ql:>5}{sb:>5}{value['area']:>3}{int(value['tensao_base']):>4}{value['modo']:1}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}{3*' ':<3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdbsh(
    dbsh,
    dbsh1,
    dbsh2,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    bsh = 0
    file.write(format(dbsh["dbsh"]))
    for idx1, value in dbsh1.iterrows():
        file.write(value.ruler)
        file.write(
            f"{value['from']:>5} {value['operacao']:1} {value['to']:>5} {value['circuito']:>2} {value['modo_controle']:1} {value['tensao_minima']:>4} {value['tensao_maxima']:>4} {value['barra_controlada']:>5} {value['injecao_reativa_inicial']:>6} {value['tipo_controle']:1} {value['apagar']:1} {value['extremidade']:>5}"
        )
        file.write("\n")
        file.write(dbsh2.ruler.iloc[0])
        for idx2 in range(0, value["ndbsh2"]):
            file.write(
                f"{dbsh2.grupo_banco.iloc[idx2 + bsh]:>2}  {dbsh2.operacao.iloc[idx2 + bsh]:1} {dbsh2.estado.iloc[idx2 + bsh]:1} {dbsh2.unidades.iloc[idx2 + bsh]:>3} {dbsh2.unidades_operacao.iloc[idx2 + bsh]:>3} {dbsh2.capacitor_reator.iloc[idx2 + bsh]:>6} {dbsh2.manobravel.iloc[idx2 + bsh]:1}"
            )
            file.write("\n")
        bsh += value["ndbsh2"]
        file.write("FBAN")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcar(
    dcar,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcar.dcar.iloc[0]))
    file.write(format(dcar.ruler.iloc[0]))
    for idx, value in dcar.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['parametro_A']:>3} {value['parametro_B']:>3} {value['parametro_C']:>3} {value['parametro_D']:>3} {value['tensao_limite']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcba(
    dcba,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcba.dcba.iloc[0]))
    file.write(format(dcba.ruler.iloc[0]))
    for idx, value in dcba.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['tipo']:1}{value['polaridade']:1}{value['nome']:>11}{value['grupo_limite_tensao']:>2}{value['tensao']:>5}                                      {value['eletrodo_terra']:>5}{value['numero_elo_cc']:>4}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdccv(
    dccv,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dccv.dccv.iloc[0]))
    file.write(format(dccv.ruler.iloc[0]))
    for idx, value in dccv.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['folga']:1}{value['modo_controle_inversor']:1}{value['tipo_controle_conversor']:1} {value['valor_especificado']:>5} {value['margem_corrente']:>5} {value['maxima_sobrecorrente']:>5} {value['angulo_conversor']:>5} {value['angulo_conversor_minimo']:>5} {value['angulo_conversor_maximo']:>5} {value['tap_transformador_minimo']:>5} {value['tap_transformador_maximo']:>5} {value['tap_transformador_numero']:>2} {value['tensao_cc_minima']:>4} {value['tap_high']:>5} {value['tap_reduzido']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcer(
    dcer,
    file,
):
    """

    Args:
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcer.dcer.iloc[0]))
    file.write(format(dcer.ruler.iloc[0]))
    for idx, value in dcer.iterrows():
        file.write(
            f"{value['barra']:>5} {value['operacao']:1} {value['grupo_base']:>2} {value['unidades']:>2} {value['barra_controlada']:>5} {value['droop']:>6} {value['potencia_reativa']:>5}{value['potencia_reativa_minima']:>5}{value['potencia_reativa_maxima']:>5} {value['controle']:1} {value['estado']:1} {value['modo_correcao_limites']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcli(
    dcli,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcli.dcli.iloc[0]))
    file.write(format(dcli.ruler.iloc[0]))
    for idx, value in dcli.iterrows():
        file.write(
            f"{value['de']:>4} {value['operacao']:1}  {value['para']:>4}{value['circuito']:>2} {value['proprietario']:1} {value['resistencia']:>6}{value['indutancia']:>6}                               {value['capacidade']:>4}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcnv(
    dcnv,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcnv.dcnv.iloc[0]))
    file.write(format(dcnv.ruler.iloc[0]))
    for idx, value in dcnv.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['barra_CA']:>5} {value['barra_CC']:>4} {value['barra_neutra']:>4} {value['modo_operacao']:1} {value['pontes']:1} {value['corrente']:>5} {value['reatancia_comutacao']:>5} {value['tensao_secundario']:>5} {value['potencia_transformador']:>5} {value['resistencia_reator']:>5} {value['indutancia_reator']:>5} {value['capacitancia']:>5} {value['frequencia']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcsc(
    dcsc,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcsc.dcsc.iloc[0]))
    file.write(format(dcsc.ruler.iloc[0]))
    for idx, value in dcsc.iterrows():
        file.write(
            f"{value['de']:>5} {value['operacao']:1}  {value['para']:>5}{value['circuito']:>2}{value['estado']:1}{value['proprietario']:1}{value['bypass']:1}      {value['reatancia_minima']:>6}{value['reatancia_maxima']:>6}{value['reatancia_inicial']:>6}{value['modo_controle']:1} {value['especificado']:>6} {value['extremidade']:>5}{value['estagios']:>3}{value['capacidade_normal']:>4}{value['capacidade_emergencia']:>4}{value['capacidade']:>4}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}\n"
        )
        # file.write("\n")
    file.write("99999")
    file.write("\n")


def wdcte(
    dcte,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dcte.dcte.iloc[0]))
    file.write(format(dcte.ruler.iloc[0]))
    for idx, value in dcte.iterrows():
        file.write(f"{value['constante']:<4} {value['valor_constante']:>6} ")
        if (idx + 1) % 6 == 0:
            file.write("\n")
    if (idx + 1) % 6 != 0:
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdctg(
    dctg,
    dctg1,
    dctg2,
    file,
):
    """

    Args
        anarede:
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


def wdctr(
    dctr,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dctr.dctr.iloc[0]))
    file.write(format(dctr.ruler.iloc[0]))
    for idx, value in dctr.iterrows():
        file.write(
            f"{value['de']:>5} {value['operacao']:1} {value['para']:>5} {value['circuito']:>2} {value['tensao_minima']:>4} {value['tensao_maxima']:>4} {value['tipo_controle_1']:1} {value['modo_controle']:1} {value['fase_minima']:>6} {value['fase_maxima']:>6} {value['tipo_controle_2']:1} {value['valor_especificado']:>6} {value['extremidade']:>5} {value['taps']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdelo(
    delo,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(delo.delo.iloc[0]))
    file.write(format(delo.ruler.iloc[0]))
    for idx, value in delo.iterrows():
        file.write(
            f"{value['numero']:>4} {value['operacao']:1} {value['tensao']:>5} {value['base']:>5} {value['nome']:>20} {value['modo_high']:1} {value['estado']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdgbt(
    dgbt,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dgbt.dgbt.iloc[0]))
    file.write(format(dgbt.ruler.iloc[0]))
    for idx, value in dgbt.iterrows():
        file.write(f"{value['grupo']:2} {value['tensao']:>5}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdger(
    dger,
    dgerDF,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dger.dger.iloc[0]))
    file.write(format(dger.ruler.iloc[0]))
    for idx, value in dger.iterrows():
        file.write(
            f"{value['numero']:>5} {value['operacao']:1} {value['potencia_ativa_minima']:>6} {value['potencia_ativa_maxima']:>6} {value['fator_participacao']:>5} {value['fator_participacao_controle_remoto']:>5} {value['fator_potencia_nominal']:>5} {value['fator_servico_armadura']:>4} {value['fator_servico_rotor']:>4} {value['angulo_maximo_carga']:>4} {value['reatancia_maquina']:>5} {value['potencia_aparente_nominal']:>5}{value['estatismo']:>6}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdglt(
    dglt,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dglt.dglt.iloc[0]))
    file.write(format(dglt.ruler.iloc[0]))
    for idx, value in dglt.iterrows():
        file.write(
            f"{value['grupo_limite_tensao']:2} {str(value['limite_minimo']):>5} {str(value['limite_maximo']):>5} {str(value['limite_minimo_E']):>5} {str(value['limite_maximo_E']):>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdinc(
    dinc,
    file,
):
    """

    Args
        anarede:
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


def wdinj(
    dinj,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dinj.dinj.iloc[0]))
    file.write(format(dinj.ruler.iloc[0]))
    for idx, value in dinj.iterrows():
        file.write(
            f"{value['numero']:>3} {value['injecao_ativa']:>6} {value['injecao_reativa']:>6} {value['barra']:>5}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdlin(
    dlin,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dlin.dlin.iloc[0]))
    file.write(format(dlin.ruler.iloc[0]))
    for idx, value in dlin.iterrows():
        file.write(
            f"{value['de']:>5}{value['abertura_de']:1} {value['operacao']:1} {value['abertura_para']:1}{value['para']:>5}{value['circuito']:>2}{value['estado']:1}{value['proprietario']:1}{value['manobravel']:1}{value['resistencia']:>6}{value['reatancia']:>6}{value['susceptancia']:>6}{value['tap']:>5}{value['tap_minimo']:>5}{value['tap_maximo']:>5}{value['tap_defasagem']:>5}{value['barra_controlada']:>6}{value['capacidade_normal']:>4}{value['capacidade_emergencial']:>4}{value['numero_taps']:>2}{value['capacidade_equipamento']:>4}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}{3*' ':>3}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmet(
    dmet,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dmet.dmet.iloc[0]))
    file.write(format(dmet.ruler.iloc[0]))
    for idx, value in dmet.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['interligacao']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdmfl(
    dmfl,
    file,
):
    """

    Args
        anarede:
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


def wdmfl_circ(
    dmfl,
    file,
):
    """

    Args
        anarede:
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


def wdmte(
    dmte,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dmte.dmte.iloc[0]))
    file.write(format(dmte.ruler.iloc[0]))

    for idx, value in dmte.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['interligacao']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdopc(
    dopc,
    dopcDF,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dopc.dopc.iloc[0]))
    file.write(format(dopc.ruler.iloc[0]))
    for idx, value in dopcDF.iterrows():
        file.write(f"{value['opcao']:4} {value['padrao']:1} ")

        if (idx + 1) % 10 == 0:
            file.write("\n")

    file.write("\nIMPR L FILE L 80CO L")
    file.write("\n")
    file.write("99999")
    file.write("\n")


def wdshl(
    dshl,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dshl.dshl.iloc[0]))
    file.write(format(dshl.ruler.iloc[0]))
    for idx, value in dshl.iterrows():
        file.write(
            f"{value['from']:>5} {value['operacao']:1}  {value['to']:>5}{value['circuito']:>2} {value['shunt_from']:>6}{value['shunt_to']:>6} {value['estado_shunt_from']:>2} {value['estado_shunt_to']:>2}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdtpf(
    dtpf,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dtpf.dtpf.iloc[0]))
    file.write(format(dtpf.ruler.iloc[0]))

    for idx, value in dtpf.iterrows():
        file.write(
            f"{value['tipo_elemento_1']:>4} {value['identificacao_elemento_1']:>5} {value['condicao_elemento_1']:1} {value['tipo_elemento_2']:>4} {value['identificacao_elemento_2']:>5} {value['condicao_elemento_2']:1} {value['tipo_elemento_3']:>4} {value['identificacao_elemento_3']:>5} {value['condicao_elemento_3']:1} {value['tipo_elemento_4']:>4} {value['identificacao_elemento_4']:>5} {value['operacao']:1} {value['interligacao']:1}"
        )
        file.write("\n")
    file.write("99999")
    file.write("\n")


def wdtpf_circ(
    dtpf,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write(format(dtpf.dtpf.iloc[0]))
    file.write(format(dtpf.ruler.iloc[0]))
    for idx, value in dtpf.iterrows():
        file.write(f"{value['de']:>5} {value['para']:>5} {value['circuito']:>2} ")

        if (idx + 1) % 5 == 0:
            file.write(f"{value['operacao']:1}")
            file.write("\n")

    file.write("\n")
    file.write("99999")
    file.write("\n")


def wtail(
    anarede,
    file,
):
    """

    Args
        anarede:
        file:
    """
    ## Inicialização
    file.write("(")
    file.write("\n")

    file.write("EXLF")

    file.write("\n")
    file.write("(")
    file.write("\n")

    file.write("FIM")
