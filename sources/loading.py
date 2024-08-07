# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import append, array, degrees, sum

from folder import continuationfolder


def loading(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Criação automática de diretório
    continuationfolder(
        powerflow,
    )

    # Variáveis para geração dos gráficos de fluxo de potência continuado
    var(
        powerflow,
    )

    # # Gráficos de variáveis de estado e controle em função do carregamento
    # self.pqvt(
    #     powerflow,
    # )

    # # Gráfico de rootlocus
    # self.ruthe(powerflow,)


def var(
    powerflow,
):
    """variáveis para geração dos gráficos de fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.pqtv = {}
    powerflow.MW = array([])
    powerflow.MVAr = array([])
    powerflow.nbuseigenvalues = array([])
    powerflow.nbuseigenvaluesPT = array([])
    powerflow.nbuseigenvaluesQV = array([])
    if "FREQ" in powerflow.control:
        powerflow.pqtv["FREQbase" + str(powerflow.options["FBASE"])] = array([])

    # Loop de Inicialização da Variável
    for _, value in powerflow.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Variável de Armazenamento de Potência Ativa
            powerflow.pqtv["P-" + value["nome"]] = array([])

            # Variável de Armazenamento de Potência Reativa
            powerflow.pqtv["Q-" + value["nome"]] = array([])

        elif (value["tipo"] == 0) and (
            ("SVCs" in powerflow.control)
            and (value["numero"] in powerflow.dcerDF["barra"].to_numpy())
        ):
            # Variável de Armazenamento de Potência Reativa
            powerflow.pqtv["Q-" + value["nome"]] = array([])

        # Variável de Armazenamento de Magnitude de Tensão Corrigida
        powerflow.pqtv["Vcorr-" + value["nome"]] = array([])

        # Variável de Armazenamento de Defasagem Angular Corrigida
        powerflow.pqtv["Tcorr-" + value["nome"]] = array([])

    # Loop de Armazenamento
    for key, item in powerflow.operationpoint.items():
        # Condição
        if key == 0:
            aux = powerflow.dbarDF["nome"][0]  # usado no loop seguinte
            for value in range(0, item["voltage"].shape[0]):
                if powerflow.dbarDF["tipo"][value] != 0:
                    # Armazenamento de Potência Ativa
                    powerflow.pqtv["P-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["P-" + powerflow.dbarDF["nome"][value]],
                        item["active"][value],
                    )

                    # Armazenamento de Potência Reativa
                    powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]],
                        item["reactive"][value],
                    )

                elif (powerflow.dbarDF["tipo"][value] == 0) and (
                    ("SVCs" in powerflow.control)
                    and (
                        powerflow.dbarDF["numero"][value]
                        in powerflow.dcerDF["barra"].to_numpy()
                    )
                ):
                    busidxcer = powerflow.dcerDF.index[
                        powerflow.dcerDF["barra"]
                        == powerflow.dbarDF["numero"].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]],
                        item["svc_generation"][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão
                powerflow.pqtv["Vcorr-" + powerflow.dbarDF["nome"][value]] = append(
                    powerflow.pqtv["Vcorr-" + powerflow.dbarDF["nome"][value]],
                    item["voltage"][value],
                )

                # Variável de Armazenamento de Defasagem Angular
                powerflow.pqtv["Tcorr-" + powerflow.dbarDF["nome"][value]] = append(
                    powerflow.pqtv["Tcorr-" + powerflow.dbarDF["nome"][value]],
                    degrees(item["theta"][value]),
                )

            # Demanda
            powerflow.MW = append(
                powerflow.MW, sum(powerflow.solution["demanda_ativa"])
            )
            powerflow.MVAr = append(
                powerflow.MVAr, sum(powerflow.solution["demanda_reativa"])
            )

            # Determinante e Autovalores
            if powerflow.solution["eigencalculation"]:
                powerflow.nbuseigenvalues = append(
                    powerflow.nbuseigenvalues, item["eigenvalues"]
                )
                powerflow.nbuseigenvaluesQV = append(
                    powerflow.nbuseigenvaluesQV, item["eigenvalues-QV"]
                )

            # Frequência
            if "FREQ" in powerflow.control:
                powerflow.pqtv["FREQbase" + str(powerflow.options["FBASE"])] = append(
                    powerflow.pqtv["FREQbase" + str(powerflow.options["FBASE"])],
                    item["freq"] * powerflow.options["FBASE"],
                )

        elif key > 0:
            for value in range(0, item["c"]["voltage"].shape[0]):
                if powerflow.dbarDF["tipo"][value] != 0:
                    # Armazenamento de Potência Ativa
                    powerflow.pqtv["P-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["P-" + powerflow.dbarDF["nome"][value]],
                        item["c"]["active"][value],
                    )

                    # Armazenamento de Potência Reativa
                    powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]],
                        item["c"]["reactive"][value],
                    )

                elif (powerflow.dbarDF["tipo"][value] == 0) and (
                    ("SVCs" in powerflow.control)
                    and (
                        powerflow.dbarDF["numero"][value]
                        in powerflow.dcerDF["barra"].to_numpy()
                    )
                ):
                    busidxcer = powerflow.dcerDF.index[
                        powerflow.dcerDF["barra"]
                        == powerflow.dbarDF["numero"].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]] = append(
                        powerflow.pqtv["Q-" + powerflow.dbarDF["nome"][value]],
                        item["c"]["svc_generation"][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão Corrigida
                powerflow.pqtv["Vcorr-" + powerflow.dbarDF["nome"][value]] = append(
                    powerflow.pqtv["Vcorr-" + powerflow.dbarDF["nome"][value]],
                    item["c"]["voltage"][value],
                )

                # Variável de Armazenamento de Defasagem Angular Corrigida
                powerflow.pqtv["Tcorr-" + powerflow.dbarDF["nome"][value]] = append(
                    powerflow.pqtv["Tcorr-" + powerflow.dbarDF["nome"][value]],
                    degrees(item["c"]["theta"][value]),
                )

            # Demanda
            totalmw = sum(powerflow.solution["demanda_ativa"])
            totalmvar = sum(powerflow.solution["demanda_reativa"])
            for _, valueinc in powerflow.dincDF.iterrows():
                if valueinc["tipo_incremento_1"] == "AREA":
                    # MW
                    areamw = (1 + item["c"]["step"]) * sum(
                        array(
                            [
                                powerflow.solution["demanda_ativa"][idxarea]
                                for idxarea, valuearea in powerflow.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )
                    totalmw += areamw - sum(
                        array(
                            [
                                powerflow.solution["demanda_ativa"][idxarea]
                                for idxarea, valuearea in powerflow.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )

                    # MVAr
                    areamvar = (1 + item["c"]["step"]) * sum(
                        array(
                            [
                                powerflow.solution["demanda_reativa"][idxarea]
                                for idxarea, valuearea in powerflow.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )
                    totalmvar += areamvar - sum(
                        array(
                            [
                                powerflow.solution["demanda_reativa"][idxarea]
                                for idxarea, valuearea in powerflow.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )

                elif powerflow.dincDF.loc[0, "tipo_incremento_1"] == "BARR":
                    # MW
                    barramw = (1 + item["c"]["step"]) * powerflow.solution[
                        "demanda_ativa"
                    ][powerflow.dincDF.loc[0, "identificacao_incremento_1"] - 1]
                    totalmw += (
                        barramw
                        - powerflow.solution["demanda_ativa"][
                            powerflow.dincDF.loc[0, "identificacao_incremento_1"] - 1
                        ]
                    )

                    # MVAr
                    barramvar = (1 + item["c"]["step"]) * powerflow.solution[
                        "demanda_reativa"
                    ][powerflow.dincDF.loc[0, "identificacao_incremento_1"] - 1]
                    totalmvar += (
                        barramvar
                        - powerflow.solution["demanda_reativa"][
                            powerflow.dincDF.loc[0, "identificacao_incremento_1"] - 1
                        ]
                    )

            powerflow.MW = append(powerflow.MW, totalmw)
            powerflow.MVAr = append(powerflow.MVAr, totalmvar)

            # Determinante e Autovalores
            if powerflow.solution["eigencalculation"]:
                powerflow.nbuseigenvalues = append(
                    powerflow.nbuseigenvalues, item["c"]["eigenvalues"]
                )
                powerflow.nbuseigenvaluesQV = append(
                    powerflow.nbuseigenvaluesQV, item["c"]["eigenvalues-QV"]
                )

            # Frequência
            if "FREQ" in powerflow.control:
                powerflow.pqtv["FREQbase" + str(powerflow.options["FBASE"])] = append(
                    powerflow.pqtv["FREQbase" + str(powerflow.options["FBASE"])],
                    item["c"]["freq"] * powerflow.options["FBASE"],
                )


def pqvt(
    self,
    powerflow,
):
    """geração e armazenamento de gráficos de variáveis de estado e controle em função do carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Geração de Gráfico
    color = 0
    for key, item in powerflow.pqtv.items():
        if (key[:5] != "Vprev") and (key[:5] != "Tprev"):
            fig, ax = plt.subplots(nrows=1, ncols=1)

            # Variáveis
            if key[1:5] == "c":
                busname = key[6:]
            else:
                busname = key[2:]
            if busname != aux:
                if key[1:5] == "c":
                    aux = key[6:]
                else:
                    aux = key[2:]
                color += 1

            # Plot
            (line,) = ax.plot(
                powerflow.MW[: powerflow.nbuspmcidx + 1],
                item[: powerflow.nbuspmcidx + 1],
                color=f"C{color}",
                linestyle="solid",
                linewidth=2,
                alpha=0.85,
                label=busname,
                zorder=2,
            )

            if powerflow.options["FULL"]:
                (dashed,) = ax.plot(
                    powerflow.MW[(powerflow.nbuspmcidx + 1) : (powerflow.nbusv2lidx)],
                    item[(powerflow.nbuspmcidx + 1) : (powerflow.nbusv2lidx)],
                    color=f"C{color}",
                    linestyle="dashed",
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                (dotted,) = ax.plot(
                    powerflow.MW[powerflow.nbusv2lidx :],
                    item[powerflow.nbusv2lidx :],
                    color=f"C{color}",
                    linestyle="dotted",
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                ax.legend([(line, dashed, dotted)], [busname])

            elif not powerflow.options["FULL"]:
                ax.legend([(line,)], [busname])

            # Labels
            # Condição de Potência Ativa
            if key[0] == "P":
                ax.set_title("Variação da Geração de Potência Ativa")
                ax.set_ylabel("Geração de Potência Ativa [MW]")

            # Condição de Potência Reativa
            elif key[0] == "Q":
                ax.set_title("Variação da Geração de Potência Reativa")
                ax.set_ylabel("Geração de Potência Reativa [MVAr]")

            # Magnitude de Tensão Nodal
            if key[0] == "V":
                ax.set_title("Variação da Magnitude de Tensão do Barramento")
                ax.set_ylabel("Magnitude de Tensão do Barramento [p.u.]")

            # Defasagem Angular de Tensão Nodal
            elif key[0] == "T":
                ax.set_title("Variação da Defasagem Angular do Barramento")
                ax.set_ylabel("Defasagem Angular do Barramento [graus]")

            # Frequência
            elif key[0] == "F":
                ax.set_title("Variação da Frequência do SEP")
                ax.set_ylabel("Frequência [Hz]")

            ax.set_xlabel("Carregamento [MW]")
            ax.grid()

        # Save
        fig.savefig(
            powerflow.nbussystemcontinuationfolderimag + key[0] + "-" + busname + ".png", dpi=400
        )
        plt.close(fig)


def ruthe(
    self,
    powerflow,
):
    """geração e armazenamento de gráfico rootlocus

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    rows = list(powerflow.operationpoint.keys())[-1]
    cols = sum(powerflow.mask)
    colsP = sum(powerflow.maskP)
    colsQ = sum(powerflow.maskQ)

    # Reconfiguração
    powerflow.nbuseigenvalues = powerflow.nbuseigenvalues.reshape(rows, cols).T.astype(
        dtype=complex
    )
    powerflow.nbuseigenvaluesPT = powerflow.nbuseigenvaluesPT.reshape(
        rows, colsP
    ).T.astype(dtype=complex)
    powerflow.nbuseigenvaluesQV = powerflow.nbuseigenvaluesQV.reshape(
        rows, colsQ
    ).T.astype(dtype=complex)

    # Geração de Gráfico - Autovalores da matriz Jacobiana Reduzida
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, cols):
        ax.scatter(
            -powerflow.nbuseigenvalues.real[eigen, 0],
            powerflow.nbuseigenvalues.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvalues.real[eigen, :],
            powerflow.nbuseigenvalues.imag[eigen, :],
            color=f"C{color}",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)

    ax.set_title("Autovalores da Matriz Jacobiana Reduzida")
    ax.set_ylabel(f"Eixo Imaginário ($j\omega$)")
    ax.set_xlabel(f"Eixo Real ($\sigma$)")

    # Save
    fig.savefig(
        powerflow.nbussystemcontinuationfolder + powerflow.name + "-rootlocus-Jacobian.png",
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensisbilidade PT
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsP):
        ax.scatter(
            -powerflow.nbuseigenvaluesPT.real[eigen, 0],
            powerflow.nbuseigenvaluesPT.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvaluesPT.real[eigen, :],
            powerflow.nbuseigenvaluesPT.imag[eigen, :],
            color=f"C{color}",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)

    ax.set_title(f"Autovalores da Matriz de Sensibilidade $P\\theta$")
    ax.set_ylabel(f"Eixo Imaginário ($j\omega$)")
    ax.set_xlabel(f"Eixo Real ($\sigma$)")

    # Save
    fig.savefig(
        powerflow.nbussystemcontinuationfolder + powerflow.name + "-rootlocus-PTsens.png",
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensibilidade QV
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsQ):
        ax.scatter(
            -powerflow.nbuseigenvaluesQV.real[eigen, 0],
            powerflow.nbuseigenvaluesQV.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvaluesQV.real[eigen, :],
            powerflow.nbuseigenvaluesQV.imag[eigen, :],
            color=f"C{color}",
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=":", color="k", linewidth=0.75, zorder=-20)

    ax.set_title(f"Autovalores da Matriz de Sensibilidade $QV$")
    ax.set_ylabel(f"Eixo Imaginário ($j\omega$)")
    ax.set_xlabel(f"Eixo Real ($\sigma$)")

    # Save
    fig.savefig(
        powerflow.nbussystemcontinuationfolder + powerflow.name + "-rootlocus-QVsens.png",
        dpi=400,
    )
    plt.close(fig)
