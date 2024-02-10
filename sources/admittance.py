# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import diag, ndarray, ones, vectorize, zeros

def checkdanc(
    powerflow,
):
    """checa alteração no nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    if powerflow.codes["DANC"]:
        for area in powerflow.dancDF["area"].values:
            for idx, value in powerflow.dbarraDF.iterrows():
                if value["area"] == area:
                    powerflow.dbarraDF.loc[idx, "demanda_ativa"] *= (
                        1
                        + powerflow.dancDF["fator_carga_ativa"][0]
                        / powerflow.options["BASE"]
                    )
                    powerflow.dbarraDF.loc[idx, "demanda_reativa"] *= (
                        1
                        + powerflow.dancDF["fator_carga_reativa"][0]
                        / powerflow.options["BASE"]
                    )
                    powerflow.dbarraDF.loc[idx, "shunt_barra"] *= (
                        1
                        + powerflow.dancDF["fator_shunt_barra"][0]
                        / powerflow.options["BASE"]
                    )


def admit(
    powerflow,
):
    """Método para cálculo dos parâmetros da matriz Admitância

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.ybus: ndarray = zeros(
        shape=[powerflow.nbus, powerflow.nbus], dtype="complex_"
    )
    # Checa alteração no nível de carregamento
    checkdanc(
        powerflow,
    )

    # Matriz Admitância
    powerflow.gdiag = zeros(powerflow.nbus)
    powerflow.bdiag = zeros(powerflow.nbus)
    powerflow.apont = ones(powerflow.nbus, dtype=int)
    powerflow.admitancia = 1 / vectorize(complex)(
        real=powerflow.dlinhaDF["resistencia"],
        imag=powerflow.dlinhaDF["reatancia"],
    )

    # Linhas de transmissão e transformadores
    for idx, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            if value["transf"]:
                value["tap"] = 1 / value["tap"]

                # Elementos da diagonal (elemento série)
                powerflow.admitancia[idx] *= value["tap"]

                powerflow.gdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[idx].real
                powerflow.bdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[idx].imag
                powerflow.gdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[idx].real
                powerflow.bdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[idx].imag

            # Elementos da diagonal (elemento série)
            powerflow.gdiag[value["de"] - 1] += powerflow.admitancia[idx].real
            powerflow.gdiag[value["para"] - 1] += powerflow.admitancia[idx].real
            powerflow.bdiag[value["de"] - 1] += (
                powerflow.admitancia[idx].imag + value["susceptancia"]
            )
            powerflow.bdiag[value["para"] - 1] += (
                powerflow.admitancia[idx].imag + value["susceptancia"]
            )

            # apontador auxiliar de conexões
            powerflow.apont[value["de"] - 1] += 1
            powerflow.apont[value["para"] - 1] += 1

            powerflow.ybus[value["de"] - 1, value["para"] - 1] = -powerflow.admitancia[idx]
            powerflow.ybus[value["para"] - 1, value["de"] - 1] = -powerflow.admitancia[idx]

    for idx, value in powerflow.dbarraDF.iterrows():
        if value["shunt_barra"] != 0.0:
            powerflow.bdiag[value["numero"] - 1] += (
                value["shunt_barra"] / powerflow.options["BASE"]
            )

        if idx != 0:
            powerflow.apont[value["numero"] - 1] += powerflow.apont[value["numero"] - 2]

    powerflow.ybus = powerflow.ybus + diag(powerflow.gdiag + 1j*powerflow.bdiag)



def admitLinear(
    powerflow,
):
    """Método para cálculo dos parâmetros da matriz Admitância
    simplificações do fluxo de potência linear

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Checa alteração no nível de carregamento
    checkdanc(
        powerflow,
    )

    # Matriz Admitância
    powerflow.ybus: ndarray = zeros(
        shape=[powerflow.nbus, powerflow.nbus], dtype="complex_"
    )
    powerflow.gdiag = zeros(powerflow.nbus)
    powerflow.bdiag = zeros(powerflow.nbus)
    powerflow.apont = ones(powerflow.nbus, dtype=int)
    powerflow.admitancia = 1 / vectorize(complex)(
        real=powerflow.dlinhaDF["resistencia"],
        imag=powerflow.dlinhaDF["reatancia"],
    )

    # Linhas de transmissão e transformadores
    for _, value in powerflow.dlinhaDF.iterrows():
        if value["estado"]:
            if value["transf"]:
                value["tap"] = 1 / value["tap"]

                # Elementos da diagonal (elemento série)
                powerflow.admitancia[_] *= value["tap"]

                powerflow.gdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[_].real
                powerflow.bdiag[value["de"] - 1] += (
                    value["tap"] - 1.0
                ) * powerflow.admitancia[_].imag
                powerflow.gdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[_].real
                powerflow.bdiag[value["para"] - 1] += (
                    1 / value["tap"] - 1.0
                ) * powerflow.admitancia[_].imag

            # Elementos da diagonal (elemento série)
            powerflow.gdiag[value["de"] - 1] += powerflow.admitancia[_].real
            powerflow.gdiag[value["para"] - 1] += powerflow.admitancia[_].real
            powerflow.bdiag[value["de"] - 1] += (
                powerflow.admitancia[_].imag + value["susceptancia"]
            )
            powerflow.bdiag[value["para"] - 1] += (
                powerflow.admitancia[_].imag + value["susceptancia"]
            )

            # apontador auxiliar de conexões
            powerflow.apont[value["de"] - 1] += 1
            powerflow.apont[value["para"] - 1] += 1

    for idx, value in powerflow.dbarraDF.iterrows():
        if value["shunt_barra"] != 0.0:
            powerflow.bdiag[value["numero"] - 1] += (
                value["shunt_barra"] / powerflow.options["BASE"]
            )

        if idx != 0:
            powerflow.apont[value["numero"] - 1] += powerflow.apont[value["numero"] - 2]
