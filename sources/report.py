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


def report(
    powerflow,
):
    """Inicialização

    Args
        powerflow:
    """
    ## Inicialização
    if powerflow.report:
        print("\033[96mOpcoes de relatorio escolhidas: ", end="")
        for k in powerflow.report:
            print(f"{k}", end=" ")
        print("\033[0m")

    else:
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")


def reportfile(
    powerflow,
):
    """

    Args
        powerflow:
    """

    # Pasta resultados/Relatorios/sepname
    reportsfolder(
        powerflow,
    )

    # Arquivo
    filedirname = powerflow.reportsfolder + powerflow.name + "-report.txt"

    # Manipulacao
    file = open(filedirname, "w")

    # Cabecalho
    rheader(
        file,
        powerflow,
    )

    if powerflow.method != "EXPC":
        # Relatorio de Convergencia
        RCONV(
            file,
            powerflow,
        )

    else:
        RPoC(
            file,
            powerflow,
        )

    # Relatorios Extras - ordem de prioridade
    if powerflow.report:
        for r in powerflow.report:
            # relatorio de barra
            if r == "RBAR":
                RBAR(
                    file,
                    powerflow,
                )
            # relatorio de linha
            elif r == "RLIN":
                from lineflow import lineflow

                lineflow(
                    powerflow,
                )

                RLIN(
                    file,
                    powerflow,
                )
            # relatorio de geradores
            elif (r == "RGER") and (powerflow.codes["DGER"]):
                RGER(
                    file,
                    powerflow,
                )
            # relatorio de compensadores estaticos de potencia reativa
            elif (r == "RSVC") and (powerflow.codes["DCER"]):
                RSVC(
                    file,
                    powerflow,
                )

    # relatorio de fluxo de potencia continuado
    if powerflow.method == "EXIC":
        exiconv(
            file,
            powerflow,
        )
        tobecontinued(
            powerflow,
        )

    file.write("fim do relatorio do sistema " + powerflow.name)
    file.close()


def rheader(
    file,
    powerflow,
):
    """cabecalho do relatorio

    Args
        powerflow:
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
    file.write("relatorio do sistema " + powerflow.name)
    file.write("\n\n")
    file.write("solucao do fluxo de potencia via metodo ")
    # Chamada específica metodo de Newton-Raphson Nao-Linear
    if powerflow.method == "EXLF":
        file.write("newton-raphson")
    # Chamada específica metodo de Gauss-Seidel
    elif powerflow.method == "GAUSS":
        file.write("gauss-seidel")
    # Chamada específica metodo de Newton-Raphson Linearizado
    elif powerflow.method == "LINEAR":
        file.write("linearizado")
    # Chamada específica metodo Desacoplado
    elif powerflow.method == "DECOUP":
        file.write("desacoplado")
    # Chamada específica metodo Desacoplado Rapido
    elif powerflow.method == "fDECOUP":
        file.write("desacoplado rapido")
    # Chamada específica metodo Continuado
    elif powerflow.method == "EXIC":
        file.write("do fluxo de potencia continuado")
    # Chamada específica metodo direto (Canizares, 1993)
    elif powerflow.method == "EXPC":
        file.write("do fluxo de potencia direto (Canizares, 1993)")
    file.write("\n\n")
    file.write("opcoes de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            file.write(f"{k} ")
    else:
        file.write("Nenhum controle ativo!")
    file.write("\n\n")
    file.write("opcoes de relatorio ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
            file.write(f"{k} ")
    file.write("\n\n\n\n")


def RCONV(
    file,
    powerflow,
):
    """relatorio de convergencia tradicional

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv relatorio de convergencia vv")
    if powerflow.method != "LINEAR":
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
        if powerflow.method != "EXIC":
            for i in range(0, powerflow.solution["iter"]):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {powerflow.solution['freqiter'][i]:^6.3f} | {powerflow.solution['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busP'][i]]:^5d} | {powerflow.solution['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busQ'][i]]:^5d} | {powerflow.solution['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busY'][i]]:^5d} |"
                )

        elif powerflow.method == "EXIC":
            for i in range(0, powerflow.operationpoint[0]["iter"]):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {powerflow.operationpoint[0]['freqiter'][i]:^6.3f} | {powerflow.operationpoint[0]['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busP'][i]]:^5d} | {powerflow.operationpoint[0]['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busQ'][i]]:^5d} | {powerflow.operationpoint[0]['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busY'][i]]:^5d} |"
                )

        file.write("\n")
        file.write("-" * 71)
    if powerflow.method == "LINEAR":
        i = powerflow.solution["iter"] - 2
    file.write("\n\n")
    file.write(" * * * * " + powerflow.solution["convergence"] + " * * * * ")
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
    if (powerflow.method != "EXIC") and (
        powerflow.solution["convergence"] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {powerflow.solution['freqiter'][i+1]:^6.3f} | {powerflow.solution['convP'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busP'][i+1]]:^5d} | {powerflow.solution['convQ'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busQ'][i+1]]:^5d} | {powerflow.solution['convY'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.solution['busY'][i+1]]:^5d} |"
        )

    elif (powerflow.method == "EXIC") and (
        powerflow.operationpoint[0]["convergence"] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {powerflow.operationpoint[0]['freqiter'][i]:^6.3f} | {powerflow.operationpoint[0]['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busP'][i]]:^5d} | {powerflow.operationpoint[0]['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busQ'][i]]:^5d} | {powerflow.operationpoint[0]['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarDF['numero'][powerflow.operationpoint[0]['busY'][i]]:^5d} |"
        )

    file.write("\n")
    file.write("-" * 71)
    file.write("\n\n\n\n")


def RBAR(
    file,
    powerflow,
):
    """relatorio de barra

    Args
        powerflow:
    """
    ## Inicialização
    # Loop por area
    for area in powerflow.dbarDF["area"].unique():
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
        for i in range(0, powerflow.nbus):
            if powerflow.dbarDF["area"][i] == area:
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
                if powerflow.method != "EXIC":
                    file.write(
                        f"| {powerflow.dbarDF['numero'][i]:^3d} | {powerflow.dbarDF['nome'][i]:^12} | {powerflow.dbarDF['tipo'][i]:^3} |  {powerflow.solution['voltage'][i]:^8.3f} | {degrees(powerflow.solution['theta'][i]):^+8.2f} | {powerflow.solution['active'][i]:^8.3f} | {powerflow.solution['reactive'][i]:^8.3f} | {powerflow.dbarDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarDF['shunt_barra'][i]:^8.3f} |"
                    )

                elif powerflow.method == "EXIC":
                    file.write(
                        f"| {powerflow.dbarDF['numero'][i]:^3d} | {powerflow.dbarDF['nome'][i]:^12} | {powerflow.dbarDF['tipo'][i]:^3} |  {powerflow.operationpoint[0]['voltage'][i]:^8.3f} | {degrees(powerflow.operationpoint[0]['theta'][i]):^+8.2f} | {powerflow.operationpoint[0]['active'][i]:^8.3f} | {powerflow.operationpoint[0]['reactive'][i]:^8.3f} | {powerflow.dbarDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarDF['shunt_barra'][i]:^8.3f} |"
                    )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")


def RLIN(
    file,
    powerflow,
):
    """relatorio de linha

    Args
        powerflow:
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
    for i in range(0, powerflow.nlin):
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
        if powerflow.method != "EXIC":
            file.write(
                f"| {powerflow.dbarDF['nome'][powerflow.dbarDF.index[powerflow.dbarDF['numero'] == powerflow.dlinDF['de'][i]][0]]:^12} | {powerflow.dbarDF['nome'][powerflow.dbarDF.index[powerflow.dbarDF['numero'] == powerflow.dlinDF['para'][i]][0]]:^12} | {powerflow.solution['active_flow_F2'][i]:^+10.3f} | {powerflow.solution['reactive_flow_F2'][i]:^+10.3f} | {powerflow.solution['active_flow_2F'][i]:^+10.3f} | {powerflow.solution['reactive_flow_2F'][i]:^+10.3f} | {powerflow.solution['active_flow_loss'][i]:^7.3f} | {powerflow.solution['reactive_flow_loss'][i]:^6.3f} |"
            )

        elif powerflow.method == "EXIC":
            file.write(
                f"| {powerflow.dbarDF['nome'][powerflow.dbarDF.index[powerflow.dbarDF['numero'] == powerflow.dlinDF['de'][i]][0]]:^12} | {powerflow.dbarDF['nome'][powerflow.dbarDF.index[powerflow.dbarDF['numero'] == powerflow.dlinDF['para'][i]][0]]:^12} | {powerflow.operationpoint[0]['active_flow_F2'][i]:^+10.3f} | {powerflow.operationpoint[0]['reactive_flow_F2'][i]:^+10.3f} | {powerflow.operationpoint[0]['active_flow_2F'][i]:^+10.3f} | {powerflow.operationpoint[0]['reactive_flow_2F'][i]:^+10.3f} | {powerflow.solution['active_flow_loss'][i]:^7.3f} | {powerflow.solution['reactive_flow_loss'][i]:^6.3f} |"
            )

        file.write("\n")
        file.write("-" * 102)

    file.write("\n\n")
    file.write("|  GERACAO |   CARGA  |    SHUNT |   PERDAS |")
    file.write("\n")
    file.write("|       MW |       MW |       MW |       MW | ")
    file.write("\n")
    if powerflow.method != "LINEAR":
        file.write("|     MVAr |     MVAr |     MVAr |     MVAr |")
        file.write("\n")
    file.write("-" * 45)
    file.write("\n")
    if powerflow.method != "EXIC":
        file.write(
            f"| {sum(powerflow.solution['active']):^+8.3f} | {sum(powerflow.dbarDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(powerflow.solution['active_flow_loss']):^8.3f} |"
        )

    elif powerflow.method == "EXIC":
        file.write(
            f"| {sum(powerflow.operationpoint[0]['active']):^+8.3f} | {sum(powerflow.dbarDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(powerflow.solution['active_flow_loss']):^8.3f} |"
        )

    file.write("\n")
    if powerflow.method != "LINEAR":
        if powerflow.method != "EXIC":
            file.write(
                f"| {sum(powerflow.solution['reactive']):^+8.3f} | {sum(powerflow.dbarDF['demanda_reativa']):^+8.3f} | {sum((powerflow.solution['voltage']**2)*powerflow.dbarDF['shunt_barra'].values.T):^8.3f} | {sum(powerflow.solution['reactive_flow_loss']):^8.3f} |"
            )

        elif powerflow.method == "EXIC":
            file.write(
                f"| {sum(powerflow.operationpoint[0]['reactive']):^+8.3f} | {sum(powerflow.dbarDF['demanda_reativa']):^+8.3f} | {sum((powerflow.operationpoint[0]['voltage']**2)*powerflow.dbarDF['shunt_barra'].values.T):^8.3f} | {sum(powerflow.solution['arective_flow_loss']):^8.3f} |"
            )

        file.write("\n")
    file.write("-" * 45)
    file.write("\n")
    file.write("\n\n\n\n")


def RGER(
    self,
    powerflow,
):
    """relatorio de geradores

    Args
        powerflow:
    """
    ## Inicialização
    pass


def RSVC(
    file,
    powerflow,
):
    """relatorio de compensadores estaticos de potencia reativa

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv relatorio de compensadores estaticos de potencia reativa vv")
    file.write("\n\n")
    if (powerflow.dcerDF["controle"][0] == "A") or (
        powerflow.dcerDF["controle"][0] == "P"
    ):
        file.write(
            "|              BARRA             | DROOP |    V0     |          GERACAO MVAr          |  BARRA CONTROL  |              CONTROL            |"
        )

    elif powerflow.dcerDF["controle"][0] == "I":
        file.write(
            "|              BARRA             | DROOP |    V0     |        INJECAO CORRENTE        |  BARRA CONTROL  |              CONTROL            |"
        )

    file.write("\n")
    file.write(
        "| NUM |     NOME     |  TENSAO   |  [%]  |  [p.u.]   |  MINIMA  |  ATUAL   |  MAXIMA  | NUM |  TENSAO   | T | UNIDADES | GRP |   REGIAO   |"
    )
    file.write("\n")
    file.write("-" * 139)
    for i in range(0, powerflow.ncer):
        idxcer = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == powerflow.dcerDF["barra"][i]
        ][0]
        idxctrl = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == powerflow.dcerDF["barra_controlada"][i]
        ][0]
        if powerflow.dcerDF["controle"][i] == "P":
            if powerflow.solution["reactive"][idxcer] <= (
                powerflow.dcerDF["potencia_reativa_minima"][i]
                * powerflow.dcerDF["unidades"][i]
                * (powerflow.solution["voltage"][idxcer] ** 2)
            ):
                regiao = "INDUTIVA"

            elif powerflow.solution["reactive"][idxcer] >= (
                powerflow.dcerDF["potencia_reativa_maxima"][i]
                * powerflow.dcerDF["unidades"][i]
                * (powerflow.solution["voltage"][idxcer] ** 2)
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.solution['svc_generation'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

        elif powerflow.dcerDF["controle"][i] == "A":
            if powerflow.solution["alpha"] == pi / 2:
                regiao = "INDUTIVA"

            elif powerflow.solution["alpha"] == pi:
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.solution['svc_generation'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write(
                f"| {' '*3} | {' '*12} | {' '*9} | {' '*5} | {' '*9} | {90.00:^8.2f} | {powerflow.solution['alpha'] * (180 / pi):^8.2f} | {180.00:8.2f} | {' '*3} | {' '*9} | {' '*1} | {' '*8} | {' '*3} | {' '*10} |"
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

        elif powerflow.dcerDF["controle"][i] == "I":
            if powerflow.solution["reactive"][idxcer] <= (
                powerflow.dcerDF["potencia_reativa_minima"][i]
                * powerflow.dcerDF["unidades"][i]
                * (powerflow.solution["voltage"][idxcer])
            ):
                regiao = "INDUTIVA"

            elif powerflow.solution["reactive"][idxcer] >= (
                powerflow.dcerDF["potencia_reativa_maxima"][i]
                * powerflow.dcerDF["unidades"][i]
                * (powerflow.solution["voltage"][idxcer])
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer])):^8.3f} | {powerflow.solution['svc_generation'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer])):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

    file.write("\n")
    file.write("\n\n\n\n")


def exiconv(
    file,
    powerflow,
):
    """relatorio de fluxo de potencia continuado

    Args
        powerflow:
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
    for key, value in powerflow.operationpoint.items():
        file.write("\n")
        if key == 0:
            file.write(
                f"| {key:^4} | {value['iter']:^4} |   0.0    |   0.0    | {powerflow.MW[key]:^8.3f} | {powerflow.MVAr[key]:^8.3f} |  lambda  | {(powerflow.options['LMBD'] * 1E2):^9} |"
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
                    f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(powerflow.options['LMBD'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                )

            else:
                var = True
                if value["c"]["varstep"] == "volt":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * powerflow.options['cpfVolt'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                    )

                elif value["c"]["varstep"] == "lambda":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * powerflow.options['LMBD'] * (5E-1 ** value['c']['ndiv']) * 1E2):^+9.2f} |"
                    )

        file.write("\n")
        file.write("-" * 82)

    file.write("\n\n\n\n")

    # Loop por area
    for area in powerflow.dbarDF["area"].unique():
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
        for i in range(0, powerflow.nbus):
            if powerflow.dbarDF["area"][i] == area:
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
                    f"| {powerflow.dbarDF['numero'][i]:^3d} | {powerflow.dbarDF['nome'][i]:^12} | {powerflow.dbarDF['tipo'][i]:^3} |  {powerflow.operationpoint[key]['c']['voltage'][i]:^8.3f} | {degrees(powerflow.operationpoint[key]['c']['theta'][i]):^+8.2f} | {powerflow.operationpoint[key]['c']['active'][i]:^8.3f} | {powerflow.operationpoint[key]['c']['reactive'][i]:^8.3f} | {powerflow.dbarDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarDF['shunt_barra'][i]:^8.3f} |"
                )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")


def tobecontinued(
    powerflow,
):
    """armazena o resultado do fluxo de potencia continuado em formato txt e formato png

    Args
        powerflow:
    """
    ## Inicialização
    var = False

    # Manipulacao
    filevtan = open(
        powerflow.systemcontinuationfolder + powerflow.name + "-tangent.txt", "w"
    )
    filevarv = open(
        powerflow.systemcontinuationfolder + powerflow.name + "-voltagevar.txt", "w"
    )
    if powerflow.solution["eigencalculation"]:
        filedeteigen = open(
            powerflow.systemcontinuationfolder + powerflow.name + "-det&eigen.txt", "w"
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
        "relatorio de analise da variacao do vetor tangente do sistema "
        + powerflow.name
    )
    filevtan.write("\n\n")
    filevtan.write("opcoes de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            filevtan.write(f"{k} ")
    else:
        filevtan.write("Nenhum controle ativo!")
    filevtan.write("\n\n")
    filevtan.write("opcoes de relatorio ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
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
        + powerflow.name
    )
    filevarv.write("\n\n")
    filevarv.write("opcoes de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            filevarv.write(f"{k} ")
    else:
        filevarv.write("Nenhum controle ativo!")
    filevarv.write("\n\n")
    filevarv.write("opcoes de relatorio ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
            filevarv.write(f"{k} ")
    filevarv.write("\n\n")

    # Cabecalho FILEDETEIGEN
    if powerflow.solution["eigencalculation"]:
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
            + powerflow.name
        )
        filedeteigen.write("\n\n")
        filedeteigen.write("opcoes de controle ativadas: ")
        if powerflow.control:
            for k in powerflow.control:
                filedeteigen.write(f"{k} ")
        else:
            filedeteigen.write("Nenhum controle ativo!")
        filedeteigen.write("\n\n")
        filedeteigen.write("opcoes de relatorio ativadas: ")
        if powerflow.report:
            for k in powerflow.report:
                filedeteigen.write(f"{k} ")
        filedeteigen.write("\n\n")

    # Loop
    for key, value in powerflow.operationpoint.items():
        if key == 0:
            # Variavel de variacao de tensao
            varv = value["voltage"] - (powerflow.dbarDF["tensao"] * 1e-3)
            arg = argsort(varv)

            # FILEVARV
            filevarv.write("\n\n")
            filevarv.write(f"Caso {key}")
            filevarv.write("\n")
            filevarv.write(
                f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
            )
            filevarv.write("\n\n")
            filevarv.write("|      BARRA         |        TENSaO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAcaO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, powerflow.nbus):
                filevarv.write(
                    f"| {powerflow.dbarDF['numero'][arg[n]]:^3d} | {powerflow.dbarDF['nome'][arg[n]]:^12} | {value['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                )
                filevarv.write("\n")
                filevarv.write("-" * 44)
                filevarv.write("\n")

            # FILEDETEIGEN
            if powerflow.solution["eigencalculation"]:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {powerflow.operationpoint[key]['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {powerflow.operationpoint[key]['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, powerflow.jacQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(powerflow.operationpoint[key]['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participacao:")
                for b in range(0, powerflow.jacQVpfactor.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {powerflow.operationpoint[key]['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

        elif key > 0:
            # Variavel de variacao de tensao
            if key == 1:
                varv = value["c"]["voltage"] - powerflow.operationpoint[0]["voltage"]

            elif key > 1:
                varv = (
                    value["c"]["voltage"]
                    - powerflow.operationpoint[key - 1]["c"]["voltage"]
                )

            arg = argsort(varv)

            # FILEVTAN
            filevtan.write("\n\n")
            filevtan.write(f"Caso {key}")
            filevtan.write("\n")
            filevtan.write(
                f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
            )
            filevtan.write("\n")
            if not var and (value["c"]["varstep"] == "lambda"):
                filevtan.write(
                    f"Variavel de Passo: {value['c']['varstep']}, {(5E-1 ** value['c']['ndiv']) * (powerflow.options['LMBD']) * 1E2:.2f}% "
                )
            else:
                var = True
                if value["c"]["varstep"] == "lambda":
                    filevtan.write(
                        f"Variavel de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['ndiv']) * (powerflow.options['LMBD']) * 1E2:.2f}% "
                    )

                elif value["c"]["varstep"] == "volt":
                    filevtan.write(
                        f"Variavel de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['ndiv']) * (powerflow.options['cpfVolt']) * 1E2:.2f}% "
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
                f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
            )
            filevarv.write("\n\n")
            filevarv.write("|       BARRA        |        TENSaO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAcaO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, powerflow.nbus):
                # FILEVTAN
                filevtan.write(
                    f"| {powerflow.dbarDF['numero'][n]:^3d} | {powerflow.dbarDF['nome'][n]:^12} | {value['p']['voltage'][n]:^8.4f} | {degrees(value['p']['theta'][n]):^+8.4f} | {value['c']['voltage'][n]:^8.4f} | {degrees(value['c']['theta'][n]):^+8.4f} |"
                )
                filevtan.write("\n")
                filevtan.write("-" * 66)
                filevtan.write("\n")

                # FILEVARV
                if key == 1:
                    filevarv.write(
                        f"| {powerflow.dbarDF['numero'][arg[n]]:^3d} | {powerflow.dbarDF['nome'][arg[n]]:^12} | {value['c']['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                    )
                elif key > 1:
                    filevarv.write(
                        f"| {powerflow.dbarDF['numero'][arg[n]]:^3d} | {powerflow.dbarDF['nome'][arg[n]]:^12} | {value['c']['voltage'][arg[n]]:^8.4f} | {varv[arg[n]]:^+8.4f} |"
                    )
                filevarv.write("\n")
                filevarv.write("-" * 43)
                filevarv.write("\n")

            # FILEDETEIGEN
            if powerflow.solution["eigencalculation"]:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {powerflow.operationpoint[key]['c']['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {powerflow.operationpoint[key]['c']['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, powerflow.jacQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(powerflow.operationpoint[key]['c']['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participacao:")
                for b in range(0, powerflow.jacQVpfactor.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {powerflow.operationpoint[key]['c']['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

    # FILEVTAN
    filevtan.write("\n\n\n\n")
    filevtan.write(
        "fim do relatorio de analise da variacao do vetor tangente do sistema "
        + powerflow.name
    )
    filevtan.close()

    # FILEVARV
    filevarv.write("\n\n\n\n")
    filevarv.write(
        "fim do relatorio de analise da variacao da magnitude de tensao do sistema "
        + powerflow.name
    )
    filevarv.close()

    # FILEDETEIGEN
    if powerflow.solution["eigencalculation"]:
        filedeteigen.write("\n\n\n\n")
        filedeteigen.write(
            "fim do relatorio de analise da variacao do valor do determinante e autovalores da matriz de sensibilidade QV do sistema "
            + powerflow.name
        )
        filedeteigen.close()

        # # FILEJACOBIAN@PMC
        # file = powerflow.systemcontinuationfolder + powerflow.name + "-jacobi@PMC.csv"
        # header = (
        #     "vv Sistema "
        #     + powerflow.name
        #     + " vv Matriz Jacobiana vv Formulacao Completa vv Caso "
        #     + str(powerflow.pointkeymin)
        #     + " vv"
        # )

        # if exists(file) is False:
        #     open(file, "a").close()
        # elif True and powerflow.solution['iter'] == 0:
        #     remove(file)
        #     open(file, "a").close()

        # with open(file, "a") as of:
        #     savetxt(
        #         of,
        #         powerflow.operationpoint[powerflow.pointkeymin]['c']['jacobian'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # FILEJACOBIAN-QV@PMC
        # file = (
        #     powerflow.systemcontinuationfolder + powerflow.name + "-jacobiQV@PMC.csv"
        # )
        # header = (
        #     "vv Sistema "
        #     + powerflow.name
        #     + " vv Matriz Jacobiana Reduzida vv Formulacao Completa vv Caso "
        #     + str(powerflow.pointkeymin)
        #     + " vv"
        # )

        # if exists(file) is False:
        #     open(file, "a").close()
        # elif True and powerflow.solution['iter'] == 0:
        #     remove(file)
        #     open(file, "a").close()

        # with open(file, "a") as of:
        #     savetxt(
        #         of,
        #         powerflow.operationpoint[powerflow.pointkeymin]['c']['jacobian-QV'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # Arquivos em Loop
        # for key, value in powerflow.pqtv.items():
        #     savetxt(
        #         powerflow.systemcontinuationfoldertxt
        #         + powerflow.name
        #         + "-"
        #         + key
        #         + ".txt",
        #         column_stack([powerflow.MW, value]),
        #     )

    # Smooth
    if ("QLIMs" in powerflow.control) or ("QLIMn" in powerflow.control):
        for busname, cases in powerflow.qlimkeys.items():
            busidx = powerflow.dbarDF[powerflow.dbarDF["nome"] == busname].index.values

            # Criacao do arquivo
            filesmooth = open(
                powerflow.dirsmoothsys + "smooth-" + busname + ".txt", "w"
            )

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
            if powerflow.control:
                for k in powerflow.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de relatorio ativadas: ")
            if powerflow.report:
                for k in powerflow.report:
                    filesmooth.write(f"{k} ")
            filesmooth.write("\n\n")

            # Loop
            for key, items in cases.items():
                iter = 0
                filesmooth.write("\n\n")
                filesmooth.write(f"Caso {key}")
                filesmooth.write("\n")
                filesmooth.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filesmooth.write("\n")
                if key == 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {powerflow.operationpoint[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {powerflow.operationpoint[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                filesmooth.write("\n")
                filesmooth.write(
                    f"Maxima Geracao de Potencia Reativa: {powerflow.dbarDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr"
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

    elif "SVCs" in powerflow.control:
        for busname, cases in powerflow.svckeys.items():
            busidx = powerflow.dbarDF[powerflow.dbarDF["nome"] == busname].index.values

            # Criacao do arquivo
            filesmooth = open(
                powerflow.dirsmoothsys + "smooth-" + busname + ".txt", "w"
            )

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
            if powerflow.control:
                for k in powerflow.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opcoes de relatorio ativadas: ")
            if powerflow.report:
                for k in powerflow.report:
                    filesmooth.write(f"{k} ")
            filesmooth.write("\n\n")

            # Loop
            for key, items in cases.items():
                iter = 0
                filesmooth.write("\n\n")
                filesmooth.write(f"Caso {key}")
                filesmooth.write("\n")
                filesmooth.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filesmooth.write("\n")
                if key == 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {powerflow.operationpoint[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geracao de Potencia Reativa: {powerflow.operationpoint[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                # filesmooth.write('\n')
                # filesmooth.write(f"Maxima Geracao de Potencia Reativa: {powerflow.dbarDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr")
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
    powerflow,
):
    """

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv relatorio de convergencia vv")
    file.write("\n\n")
    file.write(" * * * * " + powerflow.solution["convergence"] + " * * * * ")
    file.write("\n\n")
    file.write("Ponto de Maximo Carregamento: " + f"{powerflow.solution['lambda']:^f}")
    file.write("\n")
    # file.write("Autovalores: " + str(powerflow.H))
    # file.write("\n")
    file.write("Iteracoes: " + str(powerflow.solution["iter"]))
    file.write("\n\n")
