# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import reportsfolder

from datetime import datetime as dt
from numpy import (
    absolute,
    argsort,
    degrees,
    pi,
    sum,
)


def reportfile(
    anarede,
):
    """

    Args
        anarede:
    """

    # Pasta resultados/Relatorios/sepname
    reportsfolder(
        anarede,
    )

    # Arquivo
    filedirname = anarede.reportsfolder + anarede.name + "-report.txt"

    # Manipulacao
    file = open(filedirname, "w")

    # Cabecalho
    rheader(
        file,
        anarede,
    )

    if anarede.method != "EXPC":
        # Relatorio de Convergencia
        RCONV(
            file,
            anarede,
        )

    else:
        RPoC(
            file,
            anarede,
        )

    # Relatorios Extras - ordem de prioridade
    if anarede.report:
        for r in anarede.report:
            # relatorio de barra
            if r == "RBAR":
                RBAR(
                    file,
                    anarede,
                )
            # relatorio de linha
            elif r == "RLIN":
                from lineflow import lineflow

                lineflow(
                    anarede,
                )

                RLIN(
                    file,
                    anarede,
                )
            # relatorio de geradores
            elif (r == "RGER") and (anarede.pwfblock["DGER"]):
                RGER(
                    file,
                    anarede,
                )
            # relatorio de compensadores estaticos de potencia reativa
            elif (r == "RSVC") and (anarede.pwfblock["DCER"]):
                RSVC(
                    file,
                    anarede,
                )

    # relatorio de fluxo de potencia continuado
    if anarede.method == "EXIC":
        exiconv(
            file,
            anarede,
        )
        tobecontinued(
            anarede,
        )

    file.write("fim do relatorio do sistema " + anarede.name)
    file.close()


def rheader(
    file,
    anarede,
):
    """cabecalho do relatorio

    Args
        anarede:
    """
    ## Inicialização
    file.write(
        "{} {}, {}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
        )
    )
    file.write("\n\n\n")
    file.write("relatorio do sistema " + anarede.name)
    file.write("\n\n")
    file.write("solucao do fluxo de potencia via metodo ")
    # Chamada específica metodo de Newton-Raphson Nao-Linear
    if anarede.method == "EXLF":
        file.write("newton-raphson")
    # Chamada específica metodo de Gauss-Seidel
    elif anarede.method == "GAUSS":
        file.write("gauss-seidel")
    # Chamada específica metodo de Newton-Raphson Linearizado
    elif anarede.method == "LINEAR":
        file.write("linearizado")
    # Chamada específica metodo Desacoplado
    elif anarede.method == "DECOUP":
        file.write("desacoplado")
    # Chamada específica metodo Desacoplado Rapido
    elif anarede.method == "fDECOUP":
        file.write("desacoplado rapido")
    # Chamada específica metodo Continuado
    elif anarede.method == "EXIC":
        file.write("do fluxo de potencia continuado")
    # Chamada específica metodo direto (Canizares, 1993)
    elif anarede.method == "EXPC":
        file.write("do fluxo de potencia direto (Canizares, 1993)")
    file.write("\n\n")
    file.write("opcoes de controle ativadas: ")
    if anarede.control:
        for k in anarede.control:
            file.write(f"{k} ")
    else:
        file.write("Nenhum controle ativo!")
    file.write("\n\n")
    file.write("opcoes de relatorio ativadas: ")
    if anarede.report:
        for k in anarede.report:
            file.write(f"{k} ")
    file.write("\n\n\n\n")


def RCONV(
    file,
    anarede,
):
    """relatorio de convergencia tradicional

    Args
        anarede:
    """
    ## Inicialização
    file.write("vv relatorio de convergencia vv")
    if anarede.method != "LINEAR":
        file.write("\n\n")
        file.write(
            "       |  FREQ  |  ERROR  | BARRA |  ERROR  | BARRA |  ERROR  | BARRA |"
        )
        file.write("\n")
        file.write(
            "| ITER |    Hz  |     MW  |   NUM |   MVAr  |   NUM |   CTRL  |   NUM |"
        )
        file.write("\n")
        file.write("-" * 71)
        if anarede.method != "EXIC":
            for i in range(0, anarede.solution["iter"]):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {anarede.solution['freqiter'][i]:^6.3f} | {anarede.solution['convP'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busP'][i]]:^5d} | {anarede.solution['convQ'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busQ'][i]]:^5d} | {anarede.solution['convY'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busY'][i]]:^5d} |"
                )

        elif anarede.method == "EXIC":
            for i in range(0, anarede.operationpoint[0]["iter"]):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {anarede.operationpoint[0]['freqiter'][i]:^6.3f} | {anarede.operationpoint[0]['convP'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busP'][i]]:^5d} | {anarede.operationpoint[0]['convQ'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busQ'][i]]:^5d} | {anarede.operationpoint[0]['convY'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busY'][i]]:^5d} |"
                )

        file.write("\n")
        file.write("-" * 71)
    if anarede.method == "LINEAR":
        i = anarede.solution["iter"] - 2
    file.write("\n\n")
    file.write(" * * * * " + anarede.solution["convergence"] + " * * * * ")
    file.write("\n\n")
    file.write(
        "       |  FREQ  |  ERROR  | BARRA |  ERROR  | BARRA |  ERROR  | BARRA |"
    )
    file.write("\n")
    file.write(
        "| ITER |    Hz  |     MW  |   NUM |   MVAr  |   NUM |   CTRL  |   NUM |"
    )
    file.write("\n")
    file.write("-" * 71)
    file.write("\n")
    if (anarede.method != "EXIC") and (
        anarede.solution["convergence"] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {anarede.solution['freqiter'][i+1]:^6.3f} | {anarede.solution['convP'][i+1]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busP'][i+1]]:^5d} | {anarede.solution['convQ'][i+1]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busQ'][i+1]]:^5d} | {anarede.solution['convY'][i+1]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.solution['busY'][i+1]]:^5d} |"
        )

    elif (anarede.method == "EXIC") and (
        anarede.operationpoint[0]["convergence"] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {anarede.operationpoint[0]['freqiter'][i]:^6.3f} | {anarede.operationpoint[0]['convP'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busP'][i]]:^5d} | {anarede.operationpoint[0]['convQ'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busQ'][i]]:^5d} | {anarede.operationpoint[0]['convY'][i]*anarede.cte['BASE']:^7.3f} | {anarede.dbarDF['numero'][anarede.operationpoint[0]['busY'][i]]:^5d} |"
        )

    file.write("\n")
    file.write("-" * 71)
    file.write("\n\n\n\n")


def RBAR(
    file,
    anarede,
):
    """relatorio de barra

    Args
        anarede:
    """
    ## Inicialização
    # Loop por area
    for area in anarede.dbarDF["area"].unique():
        file.write("vv relatorio de barras vv area {} vv".format(area))
        file.write("\n\n")
        file.write(
            "|          BARRA           |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |"
        )
        file.write("\n")
        file.write(
            "| NUM |     NOME     |  T  |    MOD    |    ANG   |    MW    |   MVAr   |    MW    |   MVAr   |    MVAr  |"
        )
        file.write("\n")
        file.write("-" * 106)
        for i in range(0, anarede.nbus):
            if anarede.dbarDF["area"][i] == area:
                if (i % 10 == 0) and (i != 0):
                    file.write("\n\n")
                    file.write(
                        "|          BARRA           |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |"
                    )
                    file.write("\n")
                    file.write(
                        "| NUM |     NOME     |  T  |    MOD    |    ANG   |    MW    |   MVAr   |    MW    |   MVAr   |    MVAr  |"
                    )
                    file.write("\n")
                    file.write("-" * 106)

                file.write("\n")
                if anarede.method != "EXIC":
                    file.write(
                        f"| {anarede.dbarDF['numero'][i]:^3d} | {anarede.dbarDF['nome'][i]:^12} | {anarede.dbarDF['tipo'][i]:^3} |  {anarede.solution['voltage'][i]:^8.3f} | {degrees(anarede.solution['theta'][i]):^+8.2f} | {anarede.solution['active'][i]:^8.3f} | {anarede.solution['reactive'][i]:^8.3f} | {anarede.dbarDF['demanda_ativa'][i]:^8.3f} | {anarede.dbarDF['demanda_reativa'][i]:^8.3f} | {(anarede.solution['voltage'][i]**2)*anarede.dbarDF['shunt_barra'][i]:^8.3f} |"
                    )

                elif anarede.method == "EXIC":
                    file.write(
                        f"| {anarede.dbarDF['numero'][i]:^3d} | {anarede.dbarDF['nome'][i]:^12} | {anarede.dbarDF['tipo'][i]:^3} |  {anarede.operationpoint[0]['voltage'][i]:^8.3f} | {degrees(anarede.operationpoint[0]['theta'][i]):^+8.2f} | {anarede.operationpoint[0]['active'][i]:^8.3f} | {anarede.operationpoint[0]['reactive'][i]:^8.3f} | {anarede.dbarDF['demanda_ativa'][i]:^8.3f} | {anarede.dbarDF['demanda_reativa'][i]:^8.3f} | {(anarede.solution['voltage'][i]**2)*anarede.dbarDF['shunt_barra'][i]:^8.3f} |"
                    )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")


def RLIN(
    file,
    anarede,
):
    """relatorio de linha

    Args
        anarede:
    """
    ## Inicialização
    file.write("vv relatorio de linhas vv")
    file.write("\n\n")
    file.write(
        "|            BARRA            |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELeTRICAS |"
    )
    file.write("\n")
    file.write(
        "|      DE      |     PARA     |   Pkm[MW]  |  Qkm[MVAr] |   Pmk[MW]  |  Qmk[MVAr] |    MW   |  MVAr  |"
    )
    file.write("\n")
    file.write("-" * 102)
    for i in range(0, anarede.nlin):
        if (i % 10 == 0) and (i != 0):
            file.write("\n\n")
            file.write(
                "|            BARRA            |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELeTRICAS |"
            )
            file.write("\n")
            file.write(
                "|      DE      |     PARA     |   Pkm[MW]  |  Qkm[MVAr] |   Pmk[MW]  |  Qmk[MVAr] |    MW   |  MVAr  |"
            )
            file.write("\n")
            file.write("-" * 102)

        file.write("\n")
        if anarede.method != "EXIC":
            file.write(
                f"| {anarede.dbarDF['nome'][anarede.dbarDF.index[anarede.dbarDF['numero'] == anarede.dlinDF['de'][i]][0]]:^12} | {anarede.dbarDF['nome'][anarede.dbarDF.index[anarede.dbarDF['numero'] == anarede.dlinDF['para'][i]][0]]:^12} | {anarede.solution['active_flow_F2'][i]:^+10.3f} | {anarede.solution['reactive_flow_F2'][i]:^+10.3f} | {anarede.solution['active_flow_2F'][i]:^+10.3f} | {anarede.solution['reactive_flow_2F'][i]:^+10.3f} | {anarede.solution['active_flow_loss'][i]:^7.3f} | {anarede.solution['reactive_flow_loss'][i]:^6.3f} |"
            )

        elif anarede.method == "EXIC":
            file.write(
                f"| {anarede.dbarDF['nome'][anarede.dbarDF.index[anarede.dbarDF['numero'] == anarede.dlinDF['de'][i]][0]]:^12} | {anarede.dbarDF['nome'][anarede.dbarDF.index[anarede.dbarDF['numero'] == anarede.dlinDF['para'][i]][0]]:^12} | {anarede.operationpoint[0]['active_flow_F2'][i]:^+10.3f} | {anarede.operationpoint[0]['reactive_flow_F2'][i]:^+10.3f} | {anarede.operationpoint[0]['active_flow_2F'][i]:^+10.3f} | {anarede.operationpoint[0]['reactive_flow_2F'][i]:^+10.3f} | {anarede.solution['active_flow_loss'][i]:^7.3f} | {anarede.solution['reactive_flow_loss'][i]:^6.3f} |"
            )

        file.write("\n")
        file.write("-" * 102)

    file.write("\n\n")
    file.write("|  GERACAO |   CARGA  |    SHUNT |   PERDAS |")
    file.write("\n")
    file.write("|       MW |       MW |       MW |       MW | ")
    file.write("\n")
    if anarede.method != "LINEAR":
        file.write("|     MVAr |     MVAr |     MVAr |     MVAr |")
        file.write("\n")
    file.write("-" * 45)
    file.write("\n")
    if anarede.method != "EXIC":
        file.write(
            f"| {sum(anarede.solution['active']):^+8.3f} | {sum(anarede.dbarDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(anarede.solution['active_flow_loss']):^8.3f} |"
        )

    elif anarede.method == "EXIC":
        file.write(
            f"| {sum(anarede.operationpoint[0]['active']):^+8.3f} | {sum(anarede.dbarDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(anarede.solution['active_flow_loss']):^8.3f} |"
        )

    file.write("\n")
    if anarede.method != "LINEAR":
        if anarede.method != "EXIC":
            file.write(
                f"| {sum(anarede.solution['reactive']):^+8.3f} | {sum(anarede.dbarDF['demanda_reativa']):^+8.3f} | {sum((anarede.solution['voltage']**2)*anarede.dbarDF['shunt_barra'].values.T):^8.3f} | {sum(anarede.solution['reactive_flow_loss']):^8.3f} |"
            )

        elif anarede.method == "EXIC":
            file.write(
                f"| {sum(anarede.operationpoint[0]['reactive']):^+8.3f} | {sum(anarede.dbarDF['demanda_reativa']):^+8.3f} | {sum((anarede.operationpoint[0]['voltage']**2)*anarede.dbarDF['shunt_barra'].values.T):^8.3f} | {sum(anarede.solution['arective_flow_loss']):^8.3f} |"
            )

        file.write("\n")
    file.write("-" * 45)
    file.write("\n")
    file.write("\n\n\n\n")


def RGER(
    self,
    anarede,
):
    """relatorio de geradores

    Args
        anarede:
    """
    ## Inicialização
    pass


def RSVC(
    file,
    anarede,
):
    """relatorio de compensadores estaticos de potencia reativa

    Args
        anarede:
    """
    ## Inicialização
    file.write("vv relatorio de compensadores estaticos de potencia reativa vv")
    file.write("\n\n")
    if (anarede.dcerDF["controle"][0] == "A") or (anarede.dcerDF["controle"][0] == "P"):
        file.write(
            "|              BARRA             | DROOP |    V0     |          GERACAO MVAr          |  BARRA CONTROL  |              CONTROL            |"
        )

    elif anarede.dcerDF["controle"][0] == "I":
        file.write(
            "|              BARRA             | DROOP |    V0     |        INJECAO CORRENTE        |  BARRA CONTROL  |              CONTROL            |"
        )

    file.write("\n")
    file.write(
        "| NUM |     NOME     |  TENSAO   |  [%]  |  [p.u.]   |  MINIMA  |  ATUAL   |  MAXIMA  | NUM |  TENSAO   | T | UNIDADES | GRP |   REGIAO   |"
    )
    file.write("\n")
    file.write("-" * 139)
    for i in range(0, anarede.ncer):
        idxcer = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == anarede.dcerDF["barra"][i]
        ][0]
        idxctrl = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == anarede.dcerDF["barra_controlada"][i]
        ][0]
        if anarede.dcerDF["controle"][i] == "P":
            if anarede.solution["reactive"][idxcer] <= (
                anarede.dcerDF["potencia_reativa_minima"][i]
                * anarede.dcerDF["unidades"][i]
                * (anarede.solution["voltage"][idxcer] ** 2)
            ):
                regiao = "INDUTIVA"

            elif anarede.solution["reactive"][idxcer] >= (
                anarede.dcerDF["potencia_reativa_maxima"][i]
                * anarede.dcerDF["unidades"][i]
                * (anarede.solution["voltage"][idxcer] ** 2)
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {anarede.dcerDF['barra'][i]:^3d} | {anarede.dbarDF['nome'][idxcer]:^12} | {anarede.solution['voltage'][idxcer]:^9.3f} | {(-anarede.dcerDF['droop'][i] * 1E2):^5.2f} | {(anarede.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(anarede.dcerDF['potencia_reativa_minima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer] ** 2)):^8.3f} | {anarede.solution['svc_generation'][i]:^8.3f} | {(anarede.dcerDF['potencia_reativa_maxima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer] ** 2)):^8.3f} | {anarede.dcerDF['barra_controlada'][i]:^3d} | {anarede.solution['voltage'][idxctrl]:^9.3f} | {anarede.dcerDF['controle'][i]:1} | {anarede.dcerDF['unidades'][i]:^8d} | {anarede.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

        elif anarede.dcerDF["controle"][i] == "A":
            if anarede.solution["alpha"] == pi / 2:
                regiao = "INDUTIVA"

            elif anarede.solution["alpha"] == pi:
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {anarede.dcerDF['barra'][i]:^3d} | {anarede.dbarDF['nome'][idxcer]:^12} | {anarede.solution['voltage'][idxcer]:^9.3f} | {(-anarede.dcerDF['droop'][i] * 1E2):^5.2f} | {(anarede.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(anarede.dcerDF['potencia_reativa_minima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer] ** 2)):^8.3f} | {anarede.solution['svc_generation'][i]:^8.3f} | {(anarede.dcerDF['potencia_reativa_maxima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer] ** 2)):^8.3f} | {anarede.dcerDF['barra_controlada'][i]:^3d} | {anarede.solution['voltage'][idxctrl]:^9.3f} | {anarede.dcerDF['controle'][i]:1} | {anarede.dcerDF['unidades'][i]:^8d} | {anarede.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write(
                f"| {' '*3} | {' '*12} | {' '*9} | {' '*5} | {' '*9} | {90.00:^8.2f} | {anarede.solution['alpha'] * (180 / pi):^8.2f} | {180.00:8.2f} | {' '*3} | {' '*9} | {' '*1} | {' '*8} | {' '*3} | {' '*10} |"
            )
            file.write("\n")
            file.write("-" * 139)
            file.write("\n")
            file.write(
                "                                                    |  MINIMO  |  ATUAL   |  MAXIMO  |                                                    "
            )
            file.write("\n")
            file.write(
                "                                                    | aNGULO DISPARO DO TIRISTOR [C] |                                                    "
            )

        elif anarede.dcerDF["controle"][i] == "I":
            if anarede.solution["reactive"][idxcer] <= (
                anarede.dcerDF["potencia_reativa_minima"][i]
                * anarede.dcerDF["unidades"][i]
                * (anarede.solution["voltage"][idxcer])
            ):
                regiao = "INDUTIVA"

            elif anarede.solution["reactive"][idxcer] >= (
                anarede.dcerDF["potencia_reativa_maxima"][i]
                * anarede.dcerDF["unidades"][i]
                * (anarede.solution["voltage"][idxcer])
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {anarede.dcerDF['barra'][i]:^3d} | {anarede.dbarDF['nome'][idxcer]:^12} | {anarede.solution['voltage'][idxcer]:^9.3f} | {(-anarede.dcerDF['droop'][i] * 1E2):^5.2f} | {(anarede.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(anarede.dcerDF['potencia_reativa_minima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer])):^8.3f} | {anarede.solution['svc_generation'][i]:^8.3f} | {(anarede.dcerDF['potencia_reativa_maxima'][i] * anarede.dcerDF['unidades'][i] * (anarede.solution['voltage'][idxcer])):^8.3f} | {anarede.dcerDF['barra_controlada'][i]:^3d} | {anarede.solution['voltage'][idxctrl]:^9.3f} | {anarede.dcerDF['controle'][i]:1} | {anarede.dcerDF['unidades'][i]:^8d} | {anarede.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

    file.write("\n")
    file.write("\n\n\n\n")


def exiconv(
    file,
    anarede,
):
    """relatorio de fluxo de potencia continuado

    Args
        anarede:
    """
    ## Inicialização
    var = False
    file.write("vv relatorio de execucao do fluxo de potencia continuado vv")
    file.write("\n\n")
    file.write(
        "              | INCREMENTO DE CARGA |     CARGA TOTAL     |         PASSO        |"
    )
    file.write("\n")
    file.write(
        "| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIaVEL | VALOR [%] |"
    )
    file.write("\n")
    file.write("-" * 82)
    for key, value in anarede.operationpoint.items():
        file.write("\n")
        if key == 0:
            file.write(
                f"| {key:^4} | {value['iter']:^4} |   0.0    |   0.0    | {anarede.MW[key]:^8.3f} | {anarede.MVAr[key]:^8.3f} |  lambda  | {(anarede.cte['LMBD'] * 1E2):^9} |"
            )

        elif key > 0:
            if key % 5 == 0:
                file.write("\n")
                file.write(
                    "              | INCREMENTO DE CARGA |     CARGA TOTAL     |         PASSO        |"
                )
                file.write("\n")
                file.write(
                    "| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIaVEL | VALOR [%] |"
                )
                file.write("\n")
                file.write("-" * 82)
                file.write("\n")

            if not var and (value["c"]["varstep"] == "lambda"):
                file.write(
                    f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(anarede.MW[key]):^8.3f} | {(anarede.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(anarede.cte['LMBD'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                )

            else:
                var = True
                if value["c"]["varstep"] == "volt":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(anarede.MW[key]):^8.3f} | {(anarede.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * anarede.cte['cpfVolt'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                    )

                elif value["c"]["varstep"] == "lambda":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(anarede.MW[key]):^8.3f} | {(anarede.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * anarede.cte['LMBD'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                    )

        file.write("\n")
        file.write("-" * 82)

    file.write("\n\n\n\n")

    # Loop por area
    for area in anarede.dbarDF["area"].unique():
        file.write("vv relatorio de barras vv area {} vv".format(area))
        file.write("\n\n")
        file.write(
            "|          BARRA           |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |"
        )
        file.write("\n")
        file.write(
            "| NUM |     NOME     |  T  |    MOD    |    ANG   |    MW    |   MVAr   |    MW    |   MVAr   |    MVAr  |"
        )
        file.write("\n")
        file.write("-" * 106)
        for i in range(0, anarede.nbus):
            if anarede.dbarDF["area"][i] == area:
                if (i % 10 == 0) and (i != 0):
                    file.write("\n\n")
                    file.write(
                        "|          BARRA           |         TENSAO       |        GERACAO      |         CARGA       |   SHUNT  |"
                    )
                    file.write("\n")
                    file.write(
                        "| NUM |     NOME     |  T  |    MOD    |    ANG   |    MW    |   MVAr   |    MW    |   MVAr   |    MVAr  |"
                    )
                    file.write("\n")
                    file.write("-" * 106)

                file.write("\n")
                file.write(
                    f"| {anarede.dbarDF['numero'][i]:^3d} | {anarede.dbarDF['nome'][i]:^12} | {anarede.dbarDF['tipo'][i]:^3} |  {anarede.operationpoint[key]['c']['voltage'][i]:^8.3f} | {degrees(anarede.operationpoint[key]['c']['theta'][i]):^+8.2f} | {anarede.operationpoint[key]['c']['active'][i]:^8.3f} | {anarede.operationpoint[key]['c']['reactive'][i]:^8.3f} | {anarede.dbarDF['demanda_ativa'][i]:^8.3f} | {anarede.dbarDF['demanda_reativa'][i]:^8.3f} | {(anarede.solution['voltage'][i]**2)*anarede.dbarDF['shunt_barra'][i]:^8.3f} |"
                )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")


def tobecontinued(
    anarede,
):
    """armazena o resultado do fluxo de potencia continuado em formato txt e formato png

    Args
        anarede:
    """
    ## Inicialização
    var = False

    # Manipulacao
    filevtan = open(
        anarede.systemcontinuationfolder + anarede.name + "-tangent.txt", "w"
    )
    filevarv = open(
        anarede.systemcontinuationfolder + anarede.name + "-voltagevar.txt", "w"
    )
    if anarede.solution["eigencalculation"]:
        filedeteigen = open(
            anarede.systemcontinuationfolder + anarede.name + "-det&eigen.txt", "w"
        )

    # Cabecalho FILEVTAN
    filevtan.write(
        "{} {}, {}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
        )
    )
    filevtan.write("\n\n\n")
    filevtan.write(
        "relatorio de analise da variacao do vetor tangente do sistema " + anarede.name
    )
    filevtan.write("\n\n")
    filevtan.write("opcoes de controle ativadas: ")
    if anarede.control:
        for k in anarede.control:
            filevtan.write(f"{k} ")
    else:
        filevtan.write("Nenhum controle ativo!")
    filevtan.write("\n\n")
    filevtan.write("opcoes de relatorio ativadas: ")
    if anarede.report:
        for k in anarede.report:
            filevtan.write(f"{k} ")
    filevtan.write("\n\n")

    # Cabecalho FILEVARV
    filevarv.write(
        "{} {}, {}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
        )
    )
    filevarv.write("\n\n\n")
    filevarv.write(
        "relatorio de analise da variacao da magnitude de tensao do sistema "
        + anarede.name
    )
    filevarv.write("\n\n")
    filevarv.write("opcoes de controle ativadas: ")
    if anarede.control:
        for k in anarede.control:
            filevarv.write(f"{k} ")
    else:
        filevarv.write("Nenhum controle ativo!")
    filevarv.write("\n\n")
    filevarv.write("opcoes de relatorio ativadas: ")
    if anarede.report:
        for k in anarede.report:
            filevarv.write(f"{k} ")
    filevarv.write("\n\n")

    # Cabecalho FILEDETEIGEN
    if anarede.solution["eigencalculation"]:
        filedeteigen.write(
            "{} {}, {}".format(
                dt.now().strftime("%B"),
                dt.now().strftime("%d"),
                dt.now().strftime("%Y"),
            )
        )
        filedeteigen.write("\n\n\n")
        filedeteigen.write(
            "relatorio de analise da variacao do valor do determinante e autovalores da matriz de sensibilidade QV do sistema "
            + anarede.name
        )
        filedeteigen.write("\n\n")
        filedeteigen.write("opcoes de controle ativadas: ")
        if anarede.control:
            for k in anarede.control:
                filedeteigen.write(f"{k} ")
        else:
            filedeteigen.write("Nenhum controle ativo!")
        filedeteigen.write("\n\n")
        filedeteigen.write("opcoes de relatorio ativadas: ")
        if anarede.report:
            for k in anarede.report:
                filedeteigen.write(f"{k} ")
        filedeteigen.write("\n\n")

    # Loop
    for key, value in anarede.operationpoint.items():
        if key == 0:
            # Variavel de variacao de tensao
            varv = value["voltage"] - (anarede.dbarDF["tensao"] * 1e-3)
            arg = argsort(varv)

            # FILEVARV
            filevarv.write("\n\n")
            filevarv.write(f"Caso {key}")
            filevarv.write("\n")
            filevarv.write(
                f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
            )
            filevarv.write("\n\n")
            filevarv.write("|      BARRA         |        TENSaO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAcaO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, anarede.nbus):
                filevarv.write(
                    f"| {anarede.dbarDF['numero'][arg[n]]:^3d} | {anarede.dbarDF['nome'][arg[n]]:^12} | {value['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                )
                filevarv.write("\n")
                filevarv.write("-" * 44)
                filevarv.write("\n")

            # FILEDETEIGEN
            if anarede.solution["eigencalculation"]:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {anarede.operationpoint[key]['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {anarede.operationpoint[key]['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, anarede.jacQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(anarede.operationpoint[key]['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participacao:")
                for b in range(0, anarede.jacQVpfactor.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {anarede.operationpoint[key]['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

        elif key > 0:
            # Variavel de variacao de tensao
            if key == 1:
                varv = value["c"]["voltage"] - anarede.operationpoint[0]["voltage"]

            elif key > 1:
                varv = (
                    value["c"]["voltage"]
                    - anarede.operationpoint[key - 1]["c"]["voltage"]
                )

            arg = argsort(varv)

            # FILEVTAN
            filevtan.write("\n\n")
            filevtan.write(f"Caso {key}")
            filevtan.write("\n")
            filevtan.write(
                f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
            )
            filevtan.write("\n")
            if not var and (value["c"]["varstep"] == "lambda"):
                filevtan.write(
                    f"Variavel de Passo: {value['c']['varstep']}, {(5E-1 ** value['c']['ndiv']) * (anarede.cte['LMBD']) * 1E2:.2f}% "
                )
            else:
                var = True
                if value["c"]["varstep"] == "lambda":
                    filevtan.write(
                        f"Variavel de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['ndiv']) * (anarede.cte['LMBD']) * 1E2:.2f}% "
                    )

                elif value["c"]["varstep"] == "volt":
                    filevtan.write(
                        f"Variavel de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['ndiv']) * (anarede.cte['cpfVolt']) * 1E2:.2f}% "
                    )

            filevtan.write("\n\n")
            filevtan.write(
                "|       BARRA        |    VETOR TANGENTE   |       CORREcaO      |"
            )
            filevtan.write("\n")
            filevtan.write(
                "| NUM |     NOME     |    MOD   |    ANG   |    MOD   |    ANG   |"
            )
            filevtan.write("\n")
            filevtan.write("-" * 66)
            filevtan.write("\n")

            # FILEVARV
            filevarv.write("\n\n")
            filevarv.write(f"Caso {key}")
            filevarv.write("\n")
            filevarv.write(
                f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
            )
            filevarv.write("\n\n")
            filevarv.write("|       BARRA        |        TENSaO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAcaO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, anarede.nbus):
                # FILEVTAN
                filevtan.write(
                    f"| {anarede.dbarDF['numero'][n]:^3d} | {anarede.dbarDF['nome'][n]:^12} | {value['p']['voltage'][n]:^8.4f} | {degrees(value['p']['theta'][n]):^+8.4f} | {value['c']['voltage'][n]:^8.4f} | {degrees(value['c']['theta'][n]):^+8.4f} |"
                )
                filevtan.write("\n")
                filevtan.write("-" * 66)
                filevtan.write("\n")

                # FILEVARV
                if key == 1:
                    filevarv.write(
                        f"| {anarede.dbarDF['numero'][arg[n]]:^3d} | {anarede.dbarDF['nome'][arg[n]]:^12} | {value['c']['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                    )
                elif key > 1:
                    filevarv.write(
                        f"| {anarede.dbarDF['numero'][arg[n]]:^3d} | {anarede.dbarDF['nome'][arg[n]]:^12} | {value['c']['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                    )
                filevarv.write("\n")
                filevarv.write("-" * 43)
                filevarv.write("\n")

            # FILEDETEIGEN
            if anarede.solution["eigencalculation"]:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {anarede.operationpoint[key]['c']['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {anarede.operationpoint[key]['c']['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, anarede.jacQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(anarede.operationpoint[key]['c']['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participacao:")
                for b in range(0, anarede.jacQVpfactor.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {anarede.operationpoint[key]['c']['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

    # FILEVTAN
    filevtan.write("\n\n\n\n")
    filevtan.write(
        "fim do relatorio de analise da variacao do vetor tangente do sistema "
        + anarede.name
    )
    filevtan.close()

    # FILEVARV
    filevarv.write("\n\n\n\n")
    filevarv.write(
        "fim do relatorio de analise da variacao da magnitude de tensao do sistema "
        + anarede.name
    )
    filevarv.close()

    # FILEDETEIGEN
    if anarede.solution["eigencalculation"]:
        filedeteigen.write("\n\n\n\n")
        filedeteigen.write(
            "fim do relatorio de analise da variacao do valor do determinante e autovalores da matriz de sensibilidade QV do sistema "
            + anarede.name
        )
        filedeteigen.close()

        # # FILEJACOBIAN@PMC
        # file = anarede.systemcontinuationfolder + anarede.name + "-jacobi@PMC.csv"
        # header = (
        #     "vv Sistema "
        #     + anarede.name
        #     + " vv Matriz Jacobiana vv Formulacao Completa vv Caso "
        #     + str(anarede.pointkeymin)
        #     + " vv"
        # )

        # if exists(file) is False:
        #     open(file, "a").close()
        # elif True and anarede.solution['iter'] == 0:
        #     remove(file)
        #     open(file, "a").close()

        # with open(file, "a") as of:
        #     savetxt(
        #         of,
        #         anarede.operationpoint[anarede.pointkeymin]['c']['jacobian'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # FILEJACOBIAN-QV@PMC
        # file = (
        #     anarede.systemcontinuationfolder + anarede.name + "-jacobiQV@PMC.csv"
        # )
        # header = (
        #     "vv Sistema "
        #     + anarede.name
        #     + " vv Matriz Jacobiana Reduzida vv Formulacao Completa vv Caso "
        #     + str(anarede.pointkeymin)
        #     + " vv"
        # )

        # if exists(file) is False:
        #     open(file, "a").close()
        # elif True and anarede.solution['iter'] == 0:
        #     remove(file)
        #     open(file, "a").close()

        # with open(file, "a") as of:
        #     savetxt(
        #         of,
        #         anarede.operationpoint[anarede.pointkeymin]['c']['jacobian-QV'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # Arquivos em Loop
        # for key, value in anarede.pqtv.items():
        #     savetxt(
        #         anarede.systemcontinuationfoldertxt
        #         + anarede.name
        #         + "-"
        #         + key
        #         + ".txt",
        #         column_stack([anarede.MW, value]),
        #     )

    # Smooth
    if ("QLIMs" in anarede.control) or ("QLIMn" in anarede.control):
        for busname, cases in anarede.qlimkeys.items():
            busidx = anarede.dbarDF[anarede.dbarDF["nome"] == busname].index.values

            # Criacao do arquivo
            filesmooth = open(anarede.dirsmoothsys + "smooth-" + busname + ".txt", "w")

            # Cabecalho FILESMOOTH
            filesmooth.write(
                "{} {}, {}".format(
                    dt.now().strftime("%B"),
                    dt.now().strftime("%d"),
                    dt.now().strftime("%Y"),
                )
            )
            filesmooth.write("\n\n\n")
            filesmooth.write(
                "relatorio de analise da variacao da funcao suave referente a - "
                + busname
            )
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de controle ativadas: ")
            if anarede.control:
                for k in anarede.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de relatorio ativadas: ")
            if anarede.report:
                for k in anarede.report:
                    filesmooth.write(f"{k} ")
            filesmooth.write("\n\n")

            # Loop
            for key, items in cases.items():
                iter = 0
                filesmooth.write("\n\n")
                filesmooth.write(f"Caso {key}")
                filesmooth.write("\n")
                filesmooth.write(
                    f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
                )
                filesmooth.write("\n")
                if key == 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {anarede.operationpoint[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {anarede.operationpoint[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                filesmooth.write("\n")
                filesmooth.write(
                    f"Maxima Geracao de Potencia Reativa: {anarede.dbarDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr"
                )
                filesmooth.write("\n\n")

                filesmooth.write("| ITER | CH1 | CH2 | CH3 | CH4 |")
                filesmooth.write("\n")
                filesmooth.write("-" * 32)
                filesmooth.write("\n")

                for item in items[it:]:
                    filesmooth.write(
                        f"| {iter:^4d} | {float(item[0]):^3.2f} | {float(item[1]):^3.2f} | {float(item[2]):^3.2f} | {float(item[3]):^3.2f} |"
                    )
                    # filesmooth.write(f"| {iter:^4d} | {int(around(float(item[0]))):^3d} | {int(around(float(item[1]))):^3d} | {int(around(float(item[2]))):^3d} | {int(around(float(item[3]))):^3d} |")
                    filesmooth.write("\n")
                    iter += 1

                filesmooth.write("-" * 32)

            filesmooth.write("\n\n\n\n")
            filesmooth.write(
                "fim do relatorio de analise da variacao da funcao suave referente a - "
                + busname
            )
            filesmooth.close()

    elif "SVCs" in anarede.control:
        for busname, cases in anarede.svckeys.items():
            busidx = anarede.dbarDF[anarede.dbarDF["nome"] == busname].index.values

            # Criacao do arquivo
            filesmooth = open(anarede.dirsmoothsys + "smooth-" + busname + ".txt", "w")

            # Cabecalho FILESMOOTH
            filesmooth.write(
                "{} {}, {}".format(
                    dt.now().strftime("%B"),
                    dt.now().strftime("%d"),
                    dt.now().strftime("%Y"),
                )
            )
            filesmooth.write("\n\n\n")
            filesmooth.write(
                "relatorio de analise da variacao da funcao suave referente a - "
                + busname
            )
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de controle ativadas: ")
            if anarede.control:
                for k in anarede.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de relatorio ativadas: ")
            if anarede.report:
                for k in anarede.report:
                    filesmooth.write(f"{k} ")
            filesmooth.write("\n\n")

            # Loop
            for key, items in cases.items():
                iter = 0
                filesmooth.write("\n\n")
                filesmooth.write(f"Caso {key}")
                filesmooth.write("\n")
                filesmooth.write(
                    f"Carregamento do Sistema: {anarede.MW[key]} MW  | {anarede.MVAr[key]} MVAr"
                )
                filesmooth.write("\n")
                if key == 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {anarede.operationpoint[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {anarede.operationpoint[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                # filesmooth.write('\n')
                # filesmooth.write(f"Maxima Geracao de Potencia Reativa: {anarede.dbarDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr")
                filesmooth.write("\n\n")

                filesmooth.write("| ITER | CH1 | CH2 |")
                filesmooth.write("\n")
                filesmooth.write("-" * 20)
                filesmooth.write("\n")

                for item in items[it:]:
                    filesmooth.write(
                        f"| {iter:^4d} | {float(item[0]):^3.2f} | {float(item[1]):^3.2f} |"
                    )
                    filesmooth.write("\n")
                    iter += 1

                filesmooth.write("-" * 20)

            filesmooth.write("\n\n\n\n")
            filesmooth.write(
                "fim do relatorio de analise da variacao da funcao suave referente a - "
                + busname
            )
            filesmooth.close()


def RPoC(
    file,
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    file.write("vv relatorio de convergencia vv")
    file.write("\n\n")
    file.write(" * * * * " + anarede.solution["convergence"] + " * * * * ")
    file.write("\n\n")
    file.write("Ponto de Maximo Carregamento: " + f"{anarede.solution['lambda']:^f}")
    file.write("\n")
    # file.write("Autovalores: " + str(anarede.H))
    # file.write("\n")
    file.write("Iteracoes: " + str(anarede.solution["iter"]))
    file.write("\n\n")
