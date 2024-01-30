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
    degrees,
    pi,
    sum,
)

def report(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    if powerflow.report:
        print("\033[96mOpções de relatório escolhidas: ", end="")
        for k in powerflow.report:
            print(f"{k}", end=" ")
        print("\033[0m")

    else:
        print("\033[96mNenhuma opção de relatório foi escolhida.\033[0m")

def reportfile(
    powerflow,
):
    '''
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    # Pasta resultados/Relatorios/sepname
    reportsfolder(powerflow,)

    # Arquivo
    filedirname = (
        powerflow.dirRreports + powerflow.name + "-report.txt"
    )

    # Manipulação
    file = open(filedirname, "w")

    # Cabeçalho
    rheader(
        file,
        powerflow,
    )

    # Relatório de Convergência
    rconv(
        file,
        powerflow,
    )

    # Relatórios Extras - ordem de prioridade
    if powerflow.report:
        for r in powerflow.report:
            # relatório de barra
            if r == "RBAR":
                RBAR(
                    file,
                    powerflow,
                )
            # relatório de linha
            elif r == "RLIN":
                RLIN(
                    file,
                    powerflow,
                )
            # relatório de geradores
            elif (r == "RGER") and (powerflow.codes['DGER']):
                RGER(
                    file,
                    powerflow,
                )
            # relatório de compensadores estáticos de potência reativa
            elif (r == "RSVC") and (powerflow.codes['DCER']):
                RSVC(
                    file,
                    powerflow,
                )

    # relatório de fluxo de potência continuado
    if powerflow.method == "CPF":
        RCPF(
            file,
            powerflow,
        )
        tobecontinued(
            file,
            powerflow,
        )

    file.write("fim do relatório do sistema " + powerflow.name)
    file.close()

def rheader(
    file,
    powerflow,
):
    """cabeçalho do relatório

    Parâmetros
        powerflow: self do arquivo powerflow.py
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
    file.write("relatório do sistema " + powerflow.name)
    file.write("\n\n")
    file.write("solução do fluxo de potência via método ")
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.method == "NEWTON":
        file.write("newton-raphson")
    # Chamada específica método de Gauss-Seidel
    elif powerflow.method == "GAUSS":
        file.write("gauss-seidel")
    # Chamada específica método de Newton-Raphson Linearizado
    elif powerflow.method == "LINEAR":
        file.write("linearizado")
    # Chamada específica método Desacoplado
    elif powerflow.method == "DECOUP":
        file.write("desacoplado")
    # Chamada específica método Desacoplado Rápido
    elif powerflow.method == "fDECOUP":
        file.write("desacoplado rápido")
    # Chamada específica método Continuado
    elif powerflow.method == "CPF":
        file.write("do fluxo de potência continuado")
    file.write("\n\n")
    file.write("opções de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            file.write(f"{k} ")
    else:
        file.write("Nenhum controle ativo!")
    file.write("\n\n")
    file.write("opções de relatório ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
            file.write(f"{k} ")
    file.write("\n\n\n\n")

def rconv(
    file,
    powerflow,
):
    """relatório de convergência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("vv relatório de convergência vv")
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
        if powerflow.method != "CPF":
            for i in range(0, powerflow.solution['iter']):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {powerflow.solution['freqiter'][i]:^6.3f} | {powerflow.solution['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busP'][i]]:^5d} | {powerflow.solution['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busQ'][i]]:^5d} | {powerflow.solution['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busY'][i]]:^5d} |"
                )

        elif powerflow.method == "CPF":
            for i in range(0, powerflow.case[0]['iter']):
                file.write("\n")
                file.write(
                    f"| {(i+1):^4d} | {powerflow.case[0]['freqiter'][i]:^6.3f} | {powerflow.case[0]['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busP'][i]]:^5d} | {powerflow.case[0]['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busQ'][i]]:^5d} | {powerflow.case[0]['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busY'][i]]:^5d} |"
                )

        file.write("\n")
        file.write("-" * 71)
    if powerflow.method == "LINEAR":
        i = powerflow.solution['iter'] - 2
    file.write("\n\n")
    file.write(" * * * * " + powerflow.solution['convergence'] + " * * * * ")
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
    if (powerflow.method != "CPF") and (
        powerflow.solution['convergence'] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {powerflow.solution['freqiter'][i+1]:^6.3f} | {powerflow.solution['convP'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busP'][i+1]]:^5d} | {powerflow.solution['convQ'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busQ'][i+1]]:^5d} | {powerflow.solution['convY'][i+1]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.solution['busY'][i+1]]:^5d} |"
        )

    elif (powerflow.method == "CPF") and (
        powerflow.case[0]['convergence'] == "SISTEMA CONVERGENTE"
    ):
        file.write(
            f"| {(i+1):^4d} | {powerflow.case[0]['freqiter'][i]:^6.3f} | {powerflow.case[0]['convP'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busP'][i]]:^5d} | {powerflow.case[0]['convQ'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busQ'][i]]:^5d} | {powerflow.case[0]['convY'][i]*powerflow.options['BASE']:^7.3f} | {powerflow.dbarraDF['numero'][powerflow.case[0]['busY'][i]]:^5d} |"
        )

    file.write("\n")
    file.write("-" * 71)
    file.write("\n\n\n\n")

def RBAR(
    file,
    powerflow,
):
    """relatório de barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Loop por área
    for area in powerflow.dbarraDF['area'].unique():
        file.write("vv relatório de barras vv área {} vv".format(area))
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
            if powerflow.dbarraDF['area'][i] == area:
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
                if powerflow.method != "CPF":
                    file.write(
                        f"| {powerflow.dbarraDF['numero'][i]:^3d} | {powerflow.dbarraDF['nome'][i]:^12} | {powerflow.dbarraDF['tipo'][i]:^3} |  {powerflow.solution['voltage'][i]:^8.3f} | {degrees(powerflow.solution['theta'][i]):^+8.2f} | {powerflow.solution['active'][i]:^8.3f} | {powerflow.solution['reactive'][i]:^8.3f} | {powerflow.dbarraDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarraDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarraDF['shunt_barra'][i]:^8.3f} |"
                    )

                elif powerflow.method == "CPF":
                    file.write(
                        f"| {powerflow.dbarraDF['numero'][i]:^3d} | {powerflow.dbarraDF['nome'][i]:^12} | {powerflow.dbarraDF['tipo'][i]:^3} |  {powerflow.case[0]['voltage'][i]:^8.3f} | {degrees(powerflow.case[0]['theta'][i]):^+8.2f} | {powerflow.case[0]['active'][i]:^8.3f} | {powerflow.case[0]['reactive'][i]:^8.3f} | {powerflow.dbarraDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarraDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarraDF['shunt_barra'][i]:^8.3f} |"
                    )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")

def RLIN(
    file,
    powerflow,
):
    """relatório de linha

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("vv relatório de linhas vv")
    file.write("\n\n")
    file.write(
        "|            BARRA            |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |"
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
                "|            BARRA            |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |"
            )
            file.write("\n")
            file.write(
                "|      DE      |     PARA     |   Pkm[MW]  |  Qkm[MVAr] |   Pmk[MW]  |  Qmk[MVAr] |    MW   |  MVAr  |"
            )
            file.write("\n")
            file.write("-" * 102)

        file.write("\n")
        if powerflow.method != "CPF":
            file.write(
                f"| {powerflow.dbarraDF['nome'][powerflow.dbarraDF.index[powerflow.dbarraDF['numero'] == powerflow.dlinhaDF['de'][i]][0]]:^12} | {powerflow.dbarraDF['nome'][powerflow.dbarraDF.index[powerflow.dbarraDF['numero'] == powerflow.dlinhaDF['para'][i]][0]]:^12} | {powerflow.solution['active_flow_F2'][i]:^+10.3f} | {powerflow.solution['reactive_flow_F2'][i]:^+10.3f} | {powerflow.solution['active_flow_2F'][i]:^+10.3f} | {powerflow.solution['reactive_flow_2F'][i]:^+10.3f} | {powerflow.solution['active_flow_loss'][i]:^7.3f} | {powerflow.solution['reactive_flow_loss'][i]:^6.3f} |"
            )

        elif powerflow.method == "CPF":
            file.write(
                f"| {powerflow.dbarraDF['nome'][powerflow.dbarraDF.index[powerflow.dbarraDF['numero'] == powerflow.dlinhaDF['de'][i]][0]]:^12} | {powerflow.dbarraDF['nome'][powerflow.dbarraDF.index[powerflow.dbarraDF['numero'] == powerflow.dlinhaDF['para'][i]][0]]:^12} | {powerflow.case[0]['active_flow_F2'][i]:^+10.3f} | {powerflow.case[0]['reactive_flow_F2'][i]:^+10.3f} | {powerflow.case[0]['active_flow_2F'][i]:^+10.3f} | {powerflow.case[0]['reactive_flow_2F'][i]:^+10.3f} | {powerflow.solution['active_flow_loss'][i]:^7.3f} | {powerflow.solution['reactive_flow_loss'][i]:^6.3f} |"
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
    if powerflow.method != "CPF":
        file.write(
            f"| {sum(powerflow.solution['active']):^+8.3f} | {sum(powerflow.dbarraDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(powerflow.solution['active_flow_loss']):^8.3f} |"
        )

    elif powerflow.method == "CPF":
        file.write(
            f"| {sum(powerflow.case[0]['active']):^+8.3f} | {sum(powerflow.dbarraDF['demanda_ativa']):^+8.3f} |    0.0   | {sum(powerflow.solution['active_flow_loss']):^8.3f} |"
        )

    file.write("\n")
    if powerflow.method != "LINEAR":
        if powerflow.method != "CPF":
            file.write(
                f"| {sum(powerflow.solution['reactive']):^+8.3f} | {sum(powerflow.dbarraDF['demanda_reativa']):^+8.3f} | {sum((powerflow.solution['voltage']**2)*powerflow.dbarraDF['shunt_barra'].values.T):^8.3f} | {sum(powerflow.solution['reactive_flow_loss']):^8.3f} |"
            )

        elif powerflow.method == "CPF":
            file.write(
                f"| {sum(powerflow.case[0]['reactive']):^+8.3f} | {sum(powerflow.dbarraDF['demanda_reativa']):^+8.3f} | {sum((powerflow.case[0]['voltage']**2)*powerflow.dbarraDF['shunt_barra'].values.T):^8.3f} | {sum(powerflow.solution['arective_flow_loss']):^8.3f} |"
            )

        file.write("\n")
    file.write("-" * 45)
    file.write("\n")
    file.write("\n\n\n\n")

def RGER(
    self,
    powerflow,
):
    """relatório de geradores

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass

def RSVC(
    file,
    powerflow,
):
    """relatório de compensadores estáticos de potência reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write(
        "vv relatório de compensadores estáticos de potência reativa vv"
    )
    file.write("\n\n")
    if (powerflow.dcerDF['controle'][0] == 'A') or (
        powerflow.dcerDF['controle'][0] == 'P'
    ):
        file.write(
            "|              BARRA             | DROOP |    V0     |          GERACAO MVAr          |  BARRA CONTROL  |              CONTROL            |"
        )

    elif powerflow.dcerDF['controle'][0] == 'I':
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
        idxcer = powerflow.dbarraDF.index[
            powerflow.dbarraDF['numero'] == powerflow.dcerDF['barra'][i]
        ][0]
        idxctrl = powerflow.dbarraDF.index[
            powerflow.dbarraDF['numero']
            == powerflow.dcerDF['barra_controlada'][i]
        ][0]
        if powerflow.dcerDF['controle'][i] == 'P':
            if powerflow.solution['reactive'][idxcer] <= (
                powerflow.dcerDF['potencia_reativa_minima'][i]
                * powerflow.dcerDF['unidades'][i]
                * (powerflow.solution['voltage'][idxcer] ** 2)
            ):
                regiao = "INDUTIVA"

            elif powerflow.solution['reactive'][idxcer] >= (
                powerflow.dcerDF['potencia_reativa_maxima'][i]
                * powerflow.dcerDF['unidades'][i]
                * (powerflow.solution['voltage'][idxcer] ** 2)
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarraDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarraDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.solution['svc_reactive_generation'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

        elif powerflow.dcerDF['controle'][i] == 'A':
            if powerflow.solution['alpha'] == pi / 2:
                regiao = "INDUTIVA"

            elif powerflow.solution['alpha'] == pi:
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarraDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarraDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.solution['svc_reactive_generation'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer] ** 2)):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
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
                "                                                    | âNGULO DISPARO DO TIRISTOR [C] |                                                    "
            )

        elif powerflow.dcerDF['controle'][i] == 'I':
            if powerflow.solution['reactive'][idxcer] <= (
                powerflow.dcerDF['potencia_reativa_minima'][i]
                * powerflow.dcerDF['unidades'][i]
                * (powerflow.solution['voltage'][idxcer])
            ):
                regiao = "INDUTIVA"

            elif powerflow.solution['reactive'][idxcer] >= (
                powerflow.dcerDF['potencia_reativa_maxima'][i]
                * powerflow.dcerDF['unidades'][i]
                * (powerflow.solution['voltage'][idxcer])
            ):
                regiao = "CAPACITIVA"

            else:
                regiao = "LINEAR"

            file.write("\n")
            file.write(
                f"| {powerflow.dcerDF['barra'][i]:^3d} | {powerflow.dbarraDF['nome'][idxcer]:^12} | {powerflow.solution['voltage'][idxcer]:^9.3f} | {(-powerflow.dcerDF['droop'][i] * 1E2):^5.2f} | {(powerflow.dbarraDF['tensao'][idxcer] * 1E-3):^9.3f} | {(powerflow.dcerDF['potencia_reativa_minima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer])):^8.3f} | {powerflow.solution['svc_current_injection'][i]:^8.3f} | {(powerflow.dcerDF['potencia_reativa_maxima'][i] * powerflow.dcerDF['unidades'][i] * (powerflow.solution['voltage'][idxcer])):^8.3f} | {powerflow.dcerDF['barra_controlada'][i]:^3d} | {powerflow.solution['voltage'][idxctrl]:^9.3f} | {powerflow.dcerDF['controle'][i]:1} | {powerflow.dcerDF['unidades'][i]:^8d} | {powerflow.dcerDF['grupo_base'][i]:^3d} | {regiao:^10} |"
            )
            file.write("\n")
            file.write("-" * 139)

    file.write("\n")
    file.write("\n\n\n\n")

def RCPF(
    file,
    powerflow,
):
    """relatório de fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    var = False
    file.write("vv relatório de execução do fluxo de potência continuado vv")
    file.write("\n\n")
    file.write(
        "              | INCREMENTO DE CARGA |     CARGA TOTAL     |         PASSO        |"
    )
    file.write("\n")
    file.write(
        "| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIÁVEL | VALOR [%] |"
    )
    file.write("\n")
    file.write("-" * 82)
    for key, value in powerflow.case.items():
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
                    "| CASO | ITER |  ATIVA   |  REATIVA |  ATIVA   |  REATIVA | VARIÁVEL | VALOR [%] |"
                )
                file.write("\n")
                file.write("-" * 82)
                file.write("\n")

            if not var and (value['c']['varstep'] == "lambda"):
                file.write(
                    f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(powerflow.options['LMBD'] * (5E-1 ** value['c']['div']) * 1E2):^+9.2f} |"
                )

            else:
                var = True
                if value['c']['varstep'] == "volt":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * powerflow.options['cpfVolt'] * (5E-1 ** value['c']['div']) * 1E2):^+9.2f} |"
                    )

                elif value['c']['varstep'] == "lambda":
                    file.write(
                        f"| {key:^4} | {value['c']['iter']:^4} | {(value['c']['step'] * 1E2):^8.3f} | {(value['c']['step'] * 1E2):^8.3f} | {(powerflow.MW[key]):^8.3f} | {(powerflow.MVAr[key]):^8.3f} | {value['c']['varstep']:^8} | {(-1 * powerflow.options['LMBD'] * (5E-1 ** value['c']['div']) * 1E2):^+9.2f} |"
                    )

        file.write("\n")
        file.write("-" * 82)

    file.write("\n\n\n\n")
    
    # Loop por área
    for area in powerflow.dbarraDF['area'].unique():
        file.write("vv relatório de barras vv área {} vv".format(area))
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
            if powerflow.dbarraDF['area'][i] == area:
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
                    f"| {powerflow.dbarraDF['numero'][i]:^3d} | {powerflow.dbarraDF['nome'][i]:^12} | {powerflow.dbarraDF['tipo'][i]:^3} |  {powerflow.case[key]['c']['voltage'][i]:^8.3f} | {degrees(powerflow.case[key]['c']['theta'][i]):^+8.2f} | {powerflow.case[key]['c']['active'][i]:^8.3f} | {powerflow.case[key]['c']['reactive'][i]:^8.3f} | {powerflow.dbarraDF['demanda_ativa'][i]:^8.3f} | {powerflow.dbarraDF['demanda_reativa'][i]:^8.3f} | {(powerflow.solution['voltage'][i]**2)*powerflow.dbarraDF['shunt_barra'][i]:^8.3f} |"
                )

                file.write("\n")
                file.write("-" * 106)
        file.write("\n\n\n\n")

def tobecontinued(
    self,
    powerflow,
):
    """armazena o resultado do fluxo de potência continuado em formato txt e formato png

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    var = False

    # Manipulação
    filevtan = open(
        powerflow.dircpfsys + powerflow.name + "-tangent.txt", "w"
    )
    filevarv = open(
        powerflow.dircpfsys + powerflow.name + "-voltagevar.txt", "w"
    )
    if powerflow.cpfsolution['eigencalculation']:
        filedeteigen = open(
            powerflow.dircpfsys + powerflow.name + "-det&eigen.txt", "w"
        )

    # Cabeçalho FILEVTAN
    filevtan.write(
        "{} {}, {}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
        )
    )
    filevtan.write("\n\n\n")
    filevtan.write(
        "relatório de análise da variação do vetor tangente do sistema "
        + powerflow.name
    )
    filevtan.write("\n\n")
    filevtan.write("opções de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            filevtan.write(f"{k} ")
    else:
        filevtan.write("Nenhum controle ativo!")
    filevtan.write("\n\n")
    filevtan.write("opções de relatório ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
            filevtan.write(f"{k} ")
    filevtan.write("\n\n")

    # Cabeçalho FILEVARV
    filevarv.write(
        "{} {}, {}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
        )
    )
    filevarv.write("\n\n\n")
    filevarv.write(
        "relatório de análise da variação da magnitude de tensão do sistema "
        + powerflow.name
    )
    filevarv.write("\n\n")
    filevarv.write("opções de controle ativadas: ")
    if powerflow.control:
        for k in powerflow.control:
            filevarv.write(f"{k} ")
    else:
        filevarv.write("Nenhum controle ativo!")
    filevarv.write("\n\n")
    filevarv.write("opções de relatório ativadas: ")
    if powerflow.report:
        for k in powerflow.report:
            filevarv.write(f"{k} ")
    filevarv.write("\n\n")

    # Cabeçalho FILEDETEIGEN
    if powerflow.cpfsolution['eigencalculation']:
        filedeteigen.write(
            "{} {}, {}".format(
                dt.now().strftime("%B"),
                dt.now().strftime("%d"),
                dt.now().strftime("%Y"),
            )
        )
        filedeteigen.write("\n\n\n")
        filedeteigen.write(
            "relatório de análise da variação do valor do determinante e autovalores da matriz de sensibilidade QV do sistema "
            + powerflow.name
        )
        filedeteigen.write("\n\n")
        filedeteigen.write("opções de controle ativadas: ")
        if powerflow.control:
            for k in powerflow.control:
                filedeteigen.write(f"{k} ")
        else:
            filedeteigen.write("Nenhum controle ativo!")
        filedeteigen.write("\n\n")
        filedeteigen.write("opções de relatório ativadas: ")
        if powerflow.report:
            for k in powerflow.report:
                filedeteigen.write(f"{k} ")
        filedeteigen.write("\n\n")

    # Loop
    for key, value in powerflow.case.items():
        if key == 0:
            # Variável de variação de tensão
            varv = value['voltage'] - (
                powerflow.dbarraDF['tensao'] * 1e-3
            )
            argsort = argsort(varv)

            # FILEVARV
            filevarv.write("\n\n")
            filevarv.write(f"Caso {key}")
            filevarv.write("\n")
            filevarv.write(
                f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
            )
            filevarv.write("\n\n")
            filevarv.write("|      BARRA         |        TENSÃO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAÇÃO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, powerflow.nbus):
                filevarv.write(
                    f"| {powerflow.dbarraDF['numero'][argsort[n]]:^3d} | {powerflow.dbarraDF['nome'][argsort[n]]:^12} | {value['voltage'][argsort[n]]:^8.4f} | {varv[argsort[n]]:^+8.4f} |"
                )
                filevarv.write("\n")
                filevarv.write("-" * 44)
                filevarv.write("\n")

            # FILEDETEIGEN
            if powerflow.cpfsolution['eigencalculation']:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {powerflow.case[key]['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {powerflow.case[key]['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, powerflow.jacobQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(powerflow.case[key]['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participação:")
                for b in range(0, powerflow.PFQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {powerflow.case[key]['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

        elif key > 0:
            # Variável de variação de tensão
            if key == 1:
                varv = value['c']['voltage'] - powerflow.case[0]['voltage']

            elif key > 1:
                varv = (
                    value['c']['voltage']
                    - powerflow.case[key - 1]['c']['voltage']
                )

            argsort = argsort(varv)

            # FILEVTAN
            filevtan.write("\n\n")
            filevtan.write(f"Caso {key}")
            filevtan.write("\n")
            filevtan.write(
                f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
            )
            filevtan.write("\n")
            if not var and (value['c']['varstep'] == "lambda"):
                filevtan.write(
                    f"Variável de Passo: {value['c']['varstep']}, {(5E-1 ** value['c']['div']) * (powerflow.options['LMBD']) * 1E2:.2f}% "
                )
            else:
                var = True
                if value['c']['varstep'] == "lambda":
                    filevtan.write(
                        f"Variável de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['div']) * (powerflow.options['LMBD']) * 1E2:.2f}% "
                    )

                elif value['c']['varstep'] == "volt":
                    filevtan.write(
                        f"Variável de Passo: {value['c']['varstep']}, {(-5E-1 ** value['c']['div']) * (powerflow.options['cpfVolt']) * 1E2:.2f}% "
                    )

            filevtan.write("\n\n")
            filevtan.write(
                "|       BARRA        |    VETOR TANGENTE   |       CORREÇÃO      |"
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
            filevarv.write("|       BARRA        |        TENSÃO       |")
            filevarv.write("\n")
            filevarv.write("| NUM |     NOME     |    MOD   | VARIAÇÃO |")
            filevarv.write("\n")
            filevarv.write("-" * 44)
            filevarv.write("\n")

            # LOOP
            for n in range(0, powerflow.nbus):
                # FILEVTAN
                filevtan.write(
                    f"| {powerflow.dbarraDF['numero'][n]:^3d} | {powerflow.dbarraDF['nome'][n]:^12} | {value['p']['voltage'][n]:^8.4f} | {degrees(value['p']['theta'][n]):^+8.4f} | {value['c']['voltage'][n]:^8.4f} | {degrees(value['c']['theta'][n]):^+8.4f} |"
                )
                filevtan.write("\n")
                filevtan.write("-" * 66)
                filevtan.write("\n")

                # FILEVARV
                if key == 1:
                    filevarv.write(
                        f"| {powerflow.dbarraDF['numero'][argsort[n]]:^3d} | {powerflow.dbarraDF['nome'][argsort[n]]:^12} | {value['c']['voltage'][argsort[n]]:^8.4f} | {varv[argsort[n]]:^+8.4f} |"
                    )
                elif key > 1:
                    filevarv.write(
                        f"| {powerflow.dbarraDF['numero'][argsort[n]]:^3d} | {powerflow.dbarraDF['nome'][argsort[n]]:^12} | {value['c']['voltage'][argsort[n]]:^8.4f} | {varv[argsort[n]]:^+8.4f} |"
                    )
                filevarv.write("\n")
                filevarv.write("-" * 43)
                filevarv.write("\n")

            # FILEDETEIGEN
            if powerflow.cpfsolution['eigencalculation']:
                filedeteigen.write("\n\n")
                filedeteigen.write(f"Caso {key}")
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Carregamento do Sistema: {powerflow.MW[key]} MW  | {powerflow.MVAr[key]} MVAr"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Determinante: {powerflow.case[key]['c']['determinant-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write(
                    f"Autovalores: {powerflow.case[key]['c']['eigenvalues-QV']}"
                )
                filedeteigen.write("\n")
                filedeteigen.write("Autovalores:")
                for b in range(0, powerflow.jacobQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"right eigen vector {b}: {absolute(powerflow.case[key]['c']['eigenvectors-QV'][:, b])}"
                    )
                filedeteigen.write("\n")
                filedeteigen.write("Fator de Participação:")
                for b in range(0, powerflow.PFQV.shape[0]):
                    filedeteigen.write("\n")
                    filedeteigen.write(
                        f"p{b}: {powerflow.case[key]['c']['participationfactor-QV'][:, b]}"
                    )
                filedeteigen.write("\n")

    # FILEVTAN
    filevtan.write("\n\n\n\n")
    filevtan.write(
        "fim do relatório de análise da variação do vetor tangente do sistema "
        + powerflow.name
    )
    filevtan.close()

    # FILEVARV
    filevarv.write("\n\n\n\n")
    filevarv.write(
        "fim do relatório de análise da variação da magnitude de tensão do sistema "
        + powerflow.name
    )
    filevarv.close()

    # FILEDETEIGEN
    if powerflow.cpfsolution['eigencalculation']:
        filedeteigen.write("\n\n\n\n")
        filedeteigen.write(
            "fim do relatório de análise da variação do valor do determinante e autovalores da matriz de sensibilidade QV do sistema "
            + powerflow.name
        )
        filedeteigen.close()

        # # FILEJACOBIAN@PMC
        # file = powerflow.dircpfsys + powerflow.name + "-jacobi@PMC.csv"
        # header = (
        #     "vv Sistema "
        #     + powerflow.name
        #     + " vv Matriz Jacobiana vv Formulação Completa vv Caso "
        #     + str(powerflow.casekeymin)
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
        #         powerflow.case[powerflow.casekeymin]['c']['jacobian'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # FILEJACOBIAN-QV@PMC
        # file = (
        #     powerflow.dircpfsys + powerflow.name + "-jacobiQV@PMC.csv"
        # )
        # header = (
        #     "vv Sistema "
        #     + powerflow.name
        #     + " vv Matriz Jacobiana Reduzida vv Formulação Completa vv Caso "
        #     + str(powerflow.casekeymin)
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
        #         powerflow.case[powerflow.casekeymin]['c']['jacobian-QV'],
        #         delimiter=",",
        #         header=header,
        #     )
        #     of.close()

        # # Arquivos em Loop
        # for key, value in powerflow.pqtv.items():
        #     savetxt(
        #         powerflow.dircpfsystxt
        #         + powerflow.name
        #         + "-"
        #         + key
        #         + ".txt",
        #         column_stack([powerflow.MW, value]),
        #     )

    # Smooth
    if ("QLIMs" in powerflow.control) or ("QLIMn" in powerflow.control):
        for busname, cases in powerflow.qlimkeys.items():
            busidx = powerflow.dbarraDF[
                powerflow.dbarraDF['nome'] == busname
            ].index.values

            # Criação do arquivo
            filesmooth = open(
                powerflow.dirsmoothsys + "smooth-" + busname + ".txt", "w"
            )

            # Cabeçalho FILESMOOTH
            filesmooth.write(
                "{} {}, {}".format(
                    dt.now().strftime("%B"),
                    dt.now().strftime("%d"),
                    dt.now().strftime("%Y"),
                )
            )
            filesmooth.write("\n\n\n")
            filesmooth.write(
                "relatório de análise da variação da função suave referente a - "
                + busname
            )
            filesmooth.write("\n\n")
            filesmooth.write("opções de controle ativadas: ")
            if powerflow.control:
                for k in powerflow.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opções de relatório ativadas: ")
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
                        f"Geração de Potência Reativa: {powerflow.case[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geração de Potência Reativa: {powerflow.case[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                filesmooth.write("\n")
                filesmooth.write(
                    f"Máxima Geração de Potência Reativa: {powerflow.dbarraDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr"
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
                "fim do relatório de análise da variação da função suave referente a - "
                + busname
            )
            filesmooth.close()

    elif "SVCs" in powerflow.control:
        for busname, cases in powerflow.svckeys.items():
            busidx = powerflow.dbarraDF[
                powerflow.dbarraDF['nome'] == busname
            ].index.values

            # Criação do arquivo
            filesmooth = open(
                powerflow.dirsmoothsys + "smooth-" + busname + ".txt", "w"
            )

            # Cabeçalho FILESMOOTH
            filesmooth.write(
                "{} {}, {}".format(
                    dt.now().strftime("%B"),
                    dt.now().strftime("%d"),
                    dt.now().strftime("%Y"),
                )
            )
            filesmooth.write("\n\n\n")
            filesmooth.write(
                "relatório de análise da variação da função suave referente a - "
                + busname
            )
            filesmooth.write("\n\n")
            filesmooth.write("opções de controle ativadas: ")
            if powerflow.control:
                for k in powerflow.control:
                    filesmooth.write(f"{k} ")
            else:
                filesmooth.write("Nenhum controle ativo!")
            filesmooth.write("\n\n")
            filesmooth.write("opções de relatório ativadas: ")
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
                        f"Geração de Potência Reativa: {powerflow.case[key]['reactive'][busidx][0]} MVAr"
                    )
                    it = 0

                elif key > 0:
                    filesmooth.write(
                        f"Geração de Potência Reativa: {powerflow.case[key]['c']['reactive'][busidx][0]} MVAr"
                    )
                    it = 1

                # filesmooth.write('\n')
                # filesmooth.write(f"Máxima Geração de Potência Reativa: {powerflow.dbarraDF.loc[busidx, 'potencia_reativa_maxima'].values[0]} MVAr")
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
                "fim do relatório de análise da variação da função suave referente a - "
                + busname
            )
            filesmooth.close()
