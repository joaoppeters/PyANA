# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from datetime import datetime as dt
from numpy import mean


def monitor(
    powerflow,
):
    """inicialização

    Args
        powerflow:
        setting: self do arquivo setting.py
    """
    ## Inicialização
    if powerflow.monitor:
        print("\033[96mOpções de monitoramento escolhidas: ", end="")
        for k in powerflow.monitor:
            print(f"{k}", end=" ")
        print("\033[0m")

    else:
        powerflow.monitor = dict()
        print("\033[96mNenhuma opção de monitoramento foi escolhida.\033[0m")


def monitorfile(
    powerflow,
):
    """

    Parâmetro
        powerflow:
    """
    ## Inicialização
    filedirname = powerflow.reportsfolder + powerflow.name + "-monitor.txt"

    # Manipulação
    file = open(filedirname, "w")

    # Cabeçalho
    rheader(
        file,
        powerflow,
    )

    # Relatórios Extras - ordem de prioridade
    if powerflow.monitor:
        for r in powerflow.monitor:
            # monitoramento de fluxo de potência ativa em linhas de transmissão
            if r == "PFLOW":
                monitorpflow(
                    file,
                    powerflow,
                )
            # monitoramento de potência ativa gerada
            elif r == "PGMON":
                monitorpgmon(
                    file,
                    powerflow,
                )
            # monitoramento de potência reativa gerada
            elif (r == "QGMON") and (powerflow.method != "LINEAR"):
                monitorqgmon(
                    file,
                    powerflow,
                )
            # monitoramento de magnitude de tensão de barramentos
            elif r == "VMON":
                monitorvmon(
                    file,
                    powerflow,
                )

    file.write("fim do relatório de monitoramento do sistema " + powerflow.name)
    file.close()


def rheader(
    file,
    powerflow,
):
    """cabeçalho do relatório

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
    file.write("relatório de monitoramento do sistema " + powerflow.name)
    file.write("\n")
    file.write("solução do fluxo de potência via método ")
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.method == "EXLF":
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
    elif powerflow.method == "EXIC":
        file.write("do fluxo de potência continuado")
    file.write("\n\n")
    file.write("opções de monitoramento ativadas: ")
    for k in powerflow.monitor:
        file.write(f"{k} ")
    file.write("\n\n\n")


def monitorpflow(
    file,
    powerflow,
):
    """monitoramento de fluxo de potência ativa em linhas de transmissão

    Args
        powerflow:
    """
    ## Inicialização
    file.write(
        "vv monitoramento de fluxo de potência ativa em linhas de transmissão vv"
    )
    file.write("\n\n")

    # Rankeamento das linhas com maiores fluxos de potência ativa
    rank_active_flow = [
        (
            powerflow.solution["active_flow_F2"][i]
            if powerflow.solution["active_flow_F2"][i]
            > powerflow.solution["active_flow_2F"][i]
            else powerflow.solution["active_flow_2F"][i]
        )
        for i in range(0, powerflow.nlin)
    ]
    mean_active_flow = mean(rank_active_flow)
    file.write("\n")
    file.write("linhas com maiores fluxos de potência ativa:")
    file.write("\n")
    for lin in range(0, powerflow.nlin):
        if rank_active_flow[lin] >= mean_active_flow:
            file.write(
                "A linha "
                + str(powerflow.dlinDF["de"][lin])
                + " para "
                + str(powerflow.dlinDF["para"][lin])
                + " possui fluxo de potência ativa acima da média do SEP: "
                + f"{rank_active_flow[lin]:.3f}"
                + " MW"
            )
            file.write("\n")

    # Rankeamento das linhas com maiores perdas ativas
    mean_active_flow_loss = mean(powerflow.solution["active_flow_loss"])
    file.write("\n")
    file.write("linhas com maiores perdas de potência ativa")
    file.write("\n")
    for lin in range(0, powerflow.nlin):
        if powerflow.solution["active_flow_loss"][lin] >= mean_active_flow_loss:
            file.write(
                "A linha "
                + str(powerflow.dlinDF["de"][lin])
                + " para "
                + str(powerflow.dlinDF["para"][lin])
                + " possui perdas de fluxo de potência ativa acima da média do SEP: "
                + f'{powerflow.solution["active_flow_loss"][lin]:.3f}'
                + " MW"
            )
            file.write("\n")

    # Rankeamento das linhas com maiores fluxos de potência reativa
    rank_reactive_flow = [
        (
            powerflow.solution["reactive_flow_F2"][i]
            if powerflow.solution["reactive_flow_F2"][i]
            > powerflow.solution["reactive_flow_2F"][i]
            else powerflow.solution["reactive_flow_2F"][i]
        )
        for i in range(0, powerflow.nlin)
    ]
    mean_reactive_flow = mean(rank_reactive_flow)
    file.write("\n")
    file.write("linhas com maiores fluxos de potência reativa")
    file.write("\n")
    for lin in range(0, powerflow.nlin):
        if rank_reactive_flow[lin] >= mean_reactive_flow:
            file.write(
                "A linha "
                + str(powerflow.dlinDF["de"][lin])
                + " para "
                + str(powerflow.dlinDF["para"][lin])
                + " possui fluxo de potência reativa acima da média do SEP: "
                + f"{rank_reactive_flow[lin]:.3f}"
                + " MVAr"
            )
            file.write("\n")

    # Rankeamento das linhas com maiores perdas reativas
    mean_reactive_flow_loss = mean(powerflow.solution["reactive_flow_loss"])
    file.write("\n")
    file.write("linhas com maiores perdas de potência reativa")
    file.write("\n")
    for lin in range(0, powerflow.nlin):
        if powerflow.solution["reactive_flow_loss"][lin] >= mean_reactive_flow_loss:
            file.write(
                "A linha "
                + str(powerflow.dlinDF["de"][lin])
                + " para "
                + str(powerflow.dlinDF["para"][lin])
                + " possui perdas de fluxo de potência reativa acima da média do SEP: "
                + f'{powerflow.solution["reactive_flow_loss"][lin]:.3f}'
                + " MVAr"
            )
            file.write("\n")

    file.write("\n\n")


def monitorpgmon(
    file,
    powerflow,
):
    """monitoramento de potência ativa gerada

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv monitoramento de potência ativa gerada vv")
    file.write("\n\n")

    # Loop
    for item, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            file.write(
                "O gerador da "
                + str(value["nome"])
                + " está gerando "
                + f'{(powerflow.solution["active"][item] * 1E2) / sum(powerflow.solution["active"]):.2f}'
                + "% de toda a potência ativa fornecida ao SEP."
            )
            file.write("\n")

    file.write("\n\n")


def monitorqgmon(
    file,
    powerflow,
):
    """monitoramento de potência reativa gerada

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv monitoramento de potência reativa gerada vv")
    file.write("\n\n")
    qgmon = 0
    for i in range(0, powerflow.nbus):
        if powerflow.dbarDF["tipo"][i] != 0:
            if (
                powerflow.solution["reactive"][i]
                >= powerflow.dbarDF["potencia_reativa_maxima"][i]
            ):
                file.write(
                    "A geração de potência reativa da "
                    + powerflow.dbarDF["nome"][i]
                    + " violou o limite máximo estabelecido para análise ( {:.2f} >= {} ).".format(
                        powerflow.solution["reactive"][i],
                        powerflow.dbarDF["potencia_reativa_maxima"][i],
                    )
                )
                file.write("\n")
            elif (
                powerflow.solution["reactive"][i]
                <= powerflow.dbarDF["potencia_reativa_minima"][i]
            ):
                file.write(
                    "A geração de potência reativa da "
                    + powerflow.dbarDF["nome"][i]
                    + " violou o limite mínimo estabelecido para análise ( {:.2f} <= {} ).".format(
                        powerflow.solution["reactive"][i],
                        powerflow.dbarDF["potencia_reativa_minima"][i],
                    )
                )
                file.write("\n")
            else:
                qgmon += 1
    if qgmon == (powerflow.npv + 1):
        file.write(
            "Nenhuma barra de geração violou os limites máximo e mínimo de geração de potência reativa!"
        )
    file.write("\n\n\n")


def monitorvmon(
    file,
    powerflow,
):
    """monitoramento de magnitude de tensão de barramentos

    Args
        powerflow:
    """
    ## Inicialização
    file.write("vv monitoramento de magnitude de tensão de barramentos vv")
    file.write("\n\n")
    vmon = 0
    for i in range(0, powerflow.nbus):
        if powerflow.solution["voltage"][i] >= powerflow.options["vmax"]:
            file.write(
                "A magnitude de tensão da "
                + powerflow.dbarDF["nome"][i]
                + " violou o limite máximo estabelecido para análise ( {:.3f} >= {} ).".format(
                    powerflow.solution["voltage"][i],
                    powerflow.options["vmax"],
                )
            )
            file.write("\n")
        elif powerflow.solution["voltage"][i] <= powerflow.options["vmin"]:
            file.write(
                "A magnitude de tensão da "
                + powerflow.dbarDF["nome"][i]
                + " violou o limite mínimo estabelecido para análise ( {:.3f} <= {} ).".format(
                    powerflow.solution["voltage"][i],
                    powerflow.options["vmin"],
                )
            )
            file.write("\n")
        else:
            vmon += 1
    if vmon == powerflow.nbus:
        file.write(
            "Nenhum barramento violou os limites máximo e mínimo de magnitude de tensão!"
        )
    file.write("\n\n\n")
