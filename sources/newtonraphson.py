# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    abs,
    append,
    argmax,
    array,
    concatenate,
    cos,
    max,
    radians,
    sin,
    zeros,
)
from scipy.sparse.linalg import spsolve

from calc import pcalc, qcalc
from ctrl import controlsol, controldelta, controlsch, controlres, controlupdt
from jacobian import jacobi


def newton(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution = {
        "system": powerflow.name,
        "iter": 0,
        "voltage": array(powerflow.dbarraDF["tensao"] * 1e-3),
        "theta": array(radians(powerflow.dbarraDF["angulo"])),
        "active": zeros(powerflow.nbus),
        "reactive": zeros(powerflow.nbus),
        "freq": 1.0,
        "freqiter": array([]),
        "convP": array([]),
        "busP": array([]),
        "convQ": array([]),
        "busQ": array([]),
        "convY": array([]),
        "busY": array([]),
        "active_flow_F2": zeros(powerflow.nlin),
        "reactive_flow_F2": zeros(powerflow.nlin),
        "active_flow_2F": zeros(powerflow.nlin),
        "reactive_flow_2F": zeros(powerflow.nlin),
    }

    # Controles
    controlsol(
        powerflow,
    )

    # Variáveis Especificadas
    scheduled(
        powerflow,
    )

    # Resíduos
    residue(
        powerflow,
    )

    while (
        (max(abs(powerflow.deltaP)) > powerflow.options["TEPA"])
        or (max(abs(powerflow.deltaQ)) > powerflow.options["TEPR"])
        or controldelta(
            powerflow,
        )
    ):

        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update_statevar(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição Divergência por iterações
        if powerflow.solution["iter"] > powerflow.options["ACIT"]:
            powerflow.solution["convergence"] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

    # Iteração Adicional
    if powerflow.solution["iter"] <= powerflow.options["ACIT"]:
        # Armazenamento da trajetória de convergência
        convergence(
            powerflow,
        )

        # Matriz Jacobiana
        jacobi(
            powerflow,
        )

        # Variáveis de estado
        powerflow.statevar = spsolve(
            powerflow.jacob, powerflow.deltaPQY, use_umfpack=True
        )

        # Atualização das Variáveis de estado
        update_statevar(
            powerflow,
        )

        # Atualização dos resíduos
        residue(
            powerflow,
        )

        # Fluxo em linhas de transmissão
        line_flow(
            powerflow,
        )

        # Convergência
        powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"


def scheduled(
    powerflow,
):
    """método para armazenamento dos parâmetros especificados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento das potências ativa e reativa especificadas
    powerflow.pqsch = {
        "potencia_ativa_especificada": zeros(powerflow.nbus),
        "potencia_reativa_especificada": zeros(powerflow.nbus),
    }

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Potência ativa especificada
        powerflow.pqsch["potencia_ativa_especificada"][idx] += value["potencia_ativa"]
        powerflow.pqsch["potencia_ativa_especificada"][idx] -= value["demanda_ativa"]

        # Potência reativa especificada
        powerflow.pqsch["potencia_reativa_especificada"][idx] += value[
            "potencia_reativa"
        ]
        powerflow.pqsch["potencia_reativa_especificada"][idx] -= value[
            "demanda_reativa"
        ]

    # Tratamento
    powerflow.pqsch["potencia_ativa_especificada"] /= powerflow.options["BASE"]
    powerflow.pqsch["potencia_reativa_especificada"] /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0:
        controlsch(
            powerflow,
        )


def residue(
    powerflow,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    powerflow.deltaP = zeros(powerflow.nbus)
    powerflow.deltaQ = zeros(powerflow.nbus)

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Tipo PV ou PQ - Resíduo Potência Ativa
        if value["tipo"] != 2:
            powerflow.deltaP[idx] += powerflow.pqsch["potencia_ativa_especificada"][idx]
            powerflow.deltaP[idx] -= pcalc(
                powerflow,
                idx,
            )

        # Tipo PQ - Resíduo Potência Reativa
        if (
            ("QLIM" in powerflow.control)
            or ("QLIMs" in powerflow.control)
            or ("QLIMn" in powerflow.control)
            or (value["tipo"] == 0)
        ):
            powerflow.deltaQ[idx] += powerflow.pqsch["potencia_reativa_especificada"][
                idx
            ]
            powerflow.deltaQ[idx] -= qcalc(
                powerflow,
                idx,
            )

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    concatresidue(
        powerflow,
    )

    # Resíduos de variáveis de estado de controle
    if powerflow.controlcount > 0:
        controlres(
            powerflow,
        )
        # concatresidue(
        #     powerflow,
        # )
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)
    else:
        powerflow.deltaY = array([0])


def concatresidue(
    powerflow,
):
    """concatenação de resíduos de potências ativa e reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)


def convergence(
    powerflow,
):
    """armazenamento da trajetória de convergência do processo de solução do fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Trajetória de convergência da frequência
    powerflow.solution["freqiter"] = append(
        powerflow.solution["freqiter"],
        powerflow.solution["freq"] * powerflow.options["FBASE"],
    )

    # Trajetória de convergência da potência ativa
    powerflow.solution["convP"] = append(
        powerflow.solution["convP"], max(abs(powerflow.deltaP))
    )
    powerflow.solution["busP"] = append(
        powerflow.solution["busP"], argmax(abs(powerflow.deltaP))
    )

    # Trajetória de convergência da potência reativa
    powerflow.solution["convQ"] = append(
        powerflow.solution["convQ"], max(abs(powerflow.deltaQ))
    )
    powerflow.solution["busQ"] = append(
        powerflow.solution["busQ"], argmax(abs(powerflow.deltaQ))
    )

    # Trajetória de convergência referente a cada equação de controle adicional
    if powerflow.deltaY.size != 0:
        powerflow.solution["convY"] = append(
            powerflow.solution["convY"], max(abs(powerflow.deltaY))
        )
        powerflow.solution["busY"] = append(
            powerflow.solution["busY"], argmax(abs(powerflow.deltaY))
        )
    else:
        powerflow.solution["convY"] = append(powerflow.solution["convY"], 0.0)
        powerflow.solution["busY"] = append(powerflow.solution["busY"], 0.0)


def update_statevar(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.solution["theta"] += powerflow.statevar[0 : (powerflow.nbus)]
    powerflow.solution["voltage"] += powerflow.statevar[
        (powerflow.nbus) : (2 * powerflow.nbus)
    ]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )


def line_flow(
    powerflow,
):
    """cálculo do fluxo de potência nas linhas de transmissão

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """
    ## Inicialização
    for idx, value in powerflow.dlinhaDF.iterrows():
        k = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["de"]][0]
        m = powerflow.dbarraDF.index[powerflow.dbarraDF["numero"] == value["para"]][0]
        yline = 1 / ((value["resistencia"] / 100) + 1j * (value["reatancia"] / 100))

        # Verifica presença de transformadores com tap != 1.
        if value["tap"] != 0:
            yline /= value["tap"]

        # Potência ativa k -> m
        powerflow.solution["active_flow_F2"][idx] = yline.real * (
            powerflow.solution["voltage"][k] ** 2
        ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
            yline.real
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            + yline.imag
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência reativa k -> m
        powerflow.solution["reactive_flow_F2"][idx] = -(
            (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
        ) * (powerflow.solution["voltage"][k] ** 2) + powerflow.solution["voltage"][
            k
        ] * powerflow.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            - yline.real
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência ativa m -> k
        powerflow.solution["active_flow_2F"][idx] = yline.real * (
            powerflow.solution["voltage"][m] ** 2
        ) - powerflow.solution["voltage"][k] * powerflow.solution["voltage"][m] * (
            yline.real
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            - yline.imag
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

        # Potência reativa m -> k
        powerflow.solution["reactive_flow_2F"][idx] = -(
            (value["susceptancia"] / (2 * powerflow.options["BASE"])) + yline.imag
        ) * (powerflow.solution["voltage"][m] ** 2) + powerflow.solution["voltage"][
            k
        ] * powerflow.solution[
            "voltage"
        ][
            m
        ] * (
            yline.imag
            * cos(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
            + yline.real
            * sin(powerflow.solution["theta"][k] - powerflow.solution["theta"][m])
        )

    # Active Flow
    powerflow.solution["active_flow_F2"] *= powerflow.options["BASE"]
    powerflow.solution["active_flow_2F"] *= powerflow.options["BASE"]
    powerflow.solution["active_flow_loss"] = deepcopy(
        powerflow.solution["active_flow_F2"] + powerflow.solution["active_flow_2F"]
    )

    # Reactive Flow
    powerflow.solution["reactive_flow_F2"] *= powerflow.options["BASE"]
    powerflow.solution["reactive_flow_2F"] *= powerflow.options["BASE"]
    powerflow.solution["reactive_flow_loss"] = deepcopy(
        powerflow.solution["reactive_flow_F2"] + powerflow.solution["reactive_flow_2F"]
    )
