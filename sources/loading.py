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
    anarede,
):
    """inicialização

    Args
        anarede:
    """
    ## Inicialização
    # Criação automática de diretório
    continuationfolder(
        anarede,
    )

    # Variáveis para geração dos gráficos de fluxo de potência continuado
    var(
        anarede,
    )

    # # Gráficos de variáveis de estado e controle em função do carregamento
    # self.pqvt(
    #     anarede,
    # )

    # # Gráfico de rootlocus
    # self.ruthe(anarede,)


def var(
    anarede,
):
    """variáveis para geração dos gráficos de fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.pqtv = {}
    anarede.MW = array([])
    anarede.MVAr = array([])
    anarede.nbuseigenvalues = array([])
    anarede.nbuseigenvaluesPT = array([])
    anarede.nbuseigenvaluesQV = array([])
    if "FREQ" in anarede.control:
        anarede.pqtv["FREQbase" + str(anarede.cte["FBSE"])] = array([])

    # Loop de Inicialização da Variável
    for _, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Variável de Armazenamento de Potência Ativa
            anarede.pqtv["P-" + value["nome"]] = array([])

            # Variável de Armazenamento de Potência Reativa
            anarede.pqtv["Q-" + value["nome"]] = array([])

        elif (value["tipo"] == 0) and (
            ("SVCs" in anarede.control)
            and (value["numero"] in anarede.dcerDF["barra"].to_numpy())
        ):
            # Variável de Armazenamento de Potência Reativa
            anarede.pqtv["Q-" + value["nome"]] = array([])

        # Variável de Armazenamento de Magnitude de Tensão Corrigida
        anarede.pqtv["Vcorr-" + value["nome"]] = array([])

        # Variável de Armazenamento de Defasagem Angular Corrigida
        anarede.pqtv["Tcorr-" + value["nome"]] = array([])

    # Loop de Armazenamento
    for key, item in anarede.operationpoint.items():
        # Condição
        if key == 0:
            aux = anarede.dbarDF["nome"][0]  # usado no loop seguinte
            for value in range(0, item["voltage"].shape[0]):
                if anarede.dbarDF["tipo"][value] != 0:
                    # Armazenamento de Potência Ativa
                    anarede.pqtv["P-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["P-" + anarede.dbarDF["nome"][value]],
                        item["active"][value],
                    )

                    # Armazenamento de Potência Reativa
                    anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]],
                        item["reactive"][value],
                    )

                elif (anarede.dbarDF["tipo"][value] == 0) and (
                    ("SVCs" in anarede.control)
                    and (
                        anarede.dbarDF["numero"][value]
                        in anarede.dcerDF["barra"].to_numpy()
                    )
                ):
                    busidxcer = anarede.dcerDF.index[
                        anarede.dcerDF["barra"] == anarede.dbarDF["numero"].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]],
                        item["svc_generation"][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão
                anarede.pqtv["Vcorr-" + anarede.dbarDF["nome"][value]] = append(
                    anarede.pqtv["Vcorr-" + anarede.dbarDF["nome"][value]],
                    item["voltage"][value],
                )

                # Variável de Armazenamento de Defasagem Angular
                anarede.pqtv["Tcorr-" + anarede.dbarDF["nome"][value]] = append(
                    anarede.pqtv["Tcorr-" + anarede.dbarDF["nome"][value]],
                    degrees(item["theta"][value]),
                )

            # Demanda
            anarede.MW = append(anarede.MW, sum(anarede.solution["demanda_ativa"]))
            anarede.MVAr = append(
                anarede.MVAr, sum(anarede.solution["demanda_reativa"])
            )

            # Determinante e Autovalores
            if anarede.solution["eigencalculation"]:
                anarede.nbuseigenvalues = append(
                    anarede.nbuseigenvalues, item["eigenvalues"]
                )
                anarede.nbuseigenvaluesQV = append(
                    anarede.nbuseigenvaluesQV, item["eigenvalues-QV"]
                )

            # Frequência
            if "FREQ" in anarede.control:
                anarede.pqtv["FREQbase" + str(anarede.cte["FBSE"])] = append(
                    anarede.pqtv["FREQbase" + str(anarede.cte["FBSE"])],
                    item["freq"] * anarede.cte["FBSE"],
                )

        elif key > 0:
            for value in range(0, item["c"]["voltage"].shape[0]):
                if anarede.dbarDF["tipo"][value] != 0:
                    # Armazenamento de Potência Ativa
                    anarede.pqtv["P-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["P-" + anarede.dbarDF["nome"][value]],
                        item["c"]["active"][value],
                    )

                    # Armazenamento de Potência Reativa
                    anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]],
                        item["c"]["reactive"][value],
                    )

                elif (anarede.dbarDF["tipo"][value] == 0) and (
                    ("SVCs" in anarede.control)
                    and (
                        anarede.dbarDF["numero"][value]
                        in anarede.dcerDF["barra"].to_numpy()
                    )
                ):
                    busidxcer = anarede.dcerDF.index[
                        anarede.dcerDF["barra"] == anarede.dbarDF["numero"].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]] = append(
                        anarede.pqtv["Q-" + anarede.dbarDF["nome"][value]],
                        item["c"]["svc_generation"][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão Corrigida
                anarede.pqtv["Vcorr-" + anarede.dbarDF["nome"][value]] = append(
                    anarede.pqtv["Vcorr-" + anarede.dbarDF["nome"][value]],
                    item["c"]["voltage"][value],
                )

                # Variável de Armazenamento de Defasagem Angular Corrigida
                anarede.pqtv["Tcorr-" + anarede.dbarDF["nome"][value]] = append(
                    anarede.pqtv["Tcorr-" + anarede.dbarDF["nome"][value]],
                    degrees(item["c"]["theta"][value]),
                )

            # Demanda
            totalmw = sum(anarede.solution["demanda_ativa"])
            totalmvar = sum(anarede.solution["demanda_reativa"])
            for _, valueinc in anarede.dincDF.iterrows():
                if valueinc["tipo_incremento_1"] == "AREA":
                    # MW
                    areamw = (1 + item["c"]["step"]) * sum(
                        array(
                            [
                                anarede.solution["demanda_ativa"][idxarea]
                                for idxarea, valuearea in anarede.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )
                    totalmw += areamw - sum(
                        array(
                            [
                                anarede.solution["demanda_ativa"][idxarea]
                                for idxarea, valuearea in anarede.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )

                    # MVAr
                    areamvar = (1 + item["c"]["step"]) * sum(
                        array(
                            [
                                anarede.solution["demanda_reativa"][idxarea]
                                for idxarea, valuearea in anarede.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )
                    totalmvar += areamvar - sum(
                        array(
                            [
                                anarede.solution["demanda_reativa"][idxarea]
                                for idxarea, valuearea in anarede.dbarDF.iterrows()
                                if valuearea["area"]
                                == valueinc["identificacao_incremento_1"]
                            ]
                        )
                    )

                elif anarede.dincDF.loc[0, "tipo_incremento_1"] == "BARR":
                    # MW
                    barramw = (1 + item["c"]["step"]) * anarede.solution[
                        "demanda_ativa"
                    ][anarede.dincDF.loc[0, "identificacao_incremento_1"] - 1]
                    totalmw += (
                        barramw
                        - anarede.solution["demanda_ativa"][
                            anarede.dincDF.loc[0, "identificacao_incremento_1"] - 1
                        ]
                    )

                    # MVAr
                    barramvar = (1 + item["c"]["step"]) * anarede.solution[
                        "demanda_reativa"
                    ][anarede.dincDF.loc[0, "identificacao_incremento_1"] - 1]
                    totalmvar += (
                        barramvar
                        - anarede.solution["demanda_reativa"][
                            anarede.dincDF.loc[0, "identificacao_incremento_1"] - 1
                        ]
                    )

            anarede.MW = append(anarede.MW, totalmw)
            anarede.MVAr = append(anarede.MVAr, totalmvar)

            # Determinante e Autovalores
            if anarede.solution["eigencalculation"]:
                anarede.nbuseigenvalues = append(
                    anarede.nbuseigenvalues, item["c"]["eigenvalues"]
                )
                anarede.nbuseigenvaluesQV = append(
                    anarede.nbuseigenvaluesQV, item["c"]["eigenvalues-QV"]
                )

            # Frequência
            if "FREQ" in anarede.control:
                anarede.pqtv["FREQbase" + str(anarede.cte["FBSE"])] = append(
                    anarede.pqtv["FREQbase" + str(anarede.cte["FBSE"])],
                    item["c"]["freq"] * anarede.cte["FBSE"],
                )


def pqvt(
    self,
    anarede,
):
    """geração e armazenamento de gráficos de variáveis de estado e controle em função do carregamento

    Args
        anarede:
    """
    ## Inicialização
    # Geração de Gráfico
    color = 0
    for key, item in anarede.pqtv.items():
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
                anarede.MW[: anarede.nbuspmcidx + 1],
                item[: anarede.nbuspmcidx + 1],
                color=f"C{color}",
                linestyle="solid",
                linewidth=2,
                alpha=0.85,
                label=busname,
                zorder=2,
            )

            if anarede.cte["FULL"]:
                (dashed,) = ax.plot(
                    anarede.MW[(anarede.nbuspmcidx + 1) : (anarede.nbusv2lidx)],
                    item[(anarede.nbuspmcidx + 1) : (anarede.nbusv2lidx)],
                    color=f"C{color}",
                    linestyle="dashed",
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                (dotted,) = ax.plot(
                    anarede.MW[anarede.nbusv2lidx :],
                    item[anarede.nbusv2lidx :],
                    color=f"C{color}",
                    linestyle="dotted",
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                ax.legend([(line, dashed, dotted)], [busname])

            elif not anarede.cte["FULL"]:
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
            anarede.nbussystemcontinuationfolderimag + key[0] + "-" + busname + ".png",
            dpi=400,
        )
        plt.close(fig)


def ruthe(
    self,
    anarede,
):
    """geração e armazenamento de gráfico rootlocus

    Args
        anarede:
    """
    ## Inicialização
    # Variáveis
    rows = list(anarede.operationpoint.keys())[-1]
    cols = sum(anarede.mask)
    colsP = sum(anarede.maskP)
    colsQ = sum(anarede.maskQ)

    # Reconfiguração
    anarede.nbuseigenvalues = anarede.nbuseigenvalues.reshape(rows, cols).T.astype(
        dtype=complex
    )
    anarede.nbuseigenvaluesPT = anarede.nbuseigenvaluesPT.reshape(rows, colsP).T.astype(
        dtype=complex
    )
    anarede.nbuseigenvaluesQV = anarede.nbuseigenvaluesQV.reshape(rows, colsQ).T.astype(
        dtype=complex
    )

    # Geração de Gráfico - Autovalores da matriz Jacobiana Reduzida
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, cols):
        ax.scatter(
            -anarede.nbuseigenvalues.real[eigen, 0],
            anarede.nbuseigenvalues.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -anarede.nbuseigenvalues.real[eigen, :],
            anarede.nbuseigenvalues.imag[eigen, :],
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
        anarede.nbussystemcontinuationfolder + anarede.name + "-rootlocus-Jacobian.png",
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensisbilidade PT
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsP):
        ax.scatter(
            -anarede.nbuseigenvaluesPT.real[eigen, 0],
            anarede.nbuseigenvaluesPT.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -anarede.nbuseigenvaluesPT.real[eigen, :],
            anarede.nbuseigenvaluesPT.imag[eigen, :],
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
        anarede.nbussystemcontinuationfolder + anarede.name + "-rootlocus-PTsens.png",
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensibilidade QV
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsQ):
        ax.scatter(
            -anarede.nbuseigenvaluesQV.real[eigen, 0],
            anarede.nbuseigenvaluesQV.imag[eigen, 0],
            marker="x",
            color=f"C{color}",
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -anarede.nbuseigenvaluesQV.real[eigen, :],
            anarede.nbuseigenvaluesQV.imag[eigen, :],
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
        anarede.nbussystemcontinuationfolder + anarede.name + "-rootlocus-QVsens.png",
        dpi=400,
    )
    plt.close(fig)
