# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def pcalc(
    powerflow,
    idx: int = None,
):
    """cálculo da potência ativa de cada barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência ativa

    Retorno
        p: float
            potência ativa calculada para o barramenpara `idx`
    """

    ## Inicialização
    from numpy import cos, sin

    # Variável de potência ativa calculada para o barramento para `idx`
    p = powerflow.gdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinhaDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["para"].iloc[lin] - 1
            p -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )
        elif idx == powerflow.dlinhaDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["de"].iloc[lin] - 1
            p -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )

    p *= powerflow.solution["voltage"][idx]

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["active"][idx] = (
        p * powerflow.options["BASE"]
    ) + powerflow.dbarraDF["demanda_ativa"][idx]

    return p


def qcalc(
    powerflow,
    idx: int = None,
):
    """cálculo da potência reativa de cada barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência reativa

    Retorno
        q: float
            potência reativa calculada para o barramenpara `idx`
    """

    ## Inicialização
    from numpy import cos, sin

    # Variável de potência reativa calculada para o barramento para `idx`
    q = -powerflow.bdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinhaDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["para"].iloc[lin] - 1
            q -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                - powerflow.admitancia[lin].imag
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )
        elif idx == powerflow.dlinhaDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["de"].iloc[lin] - 1
            q -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                - powerflow.admitancia[lin].imag
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )

    q *= powerflow.solution["voltage"][idx]

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["reactive"][idx] = (
        q * powerflow.options["BASE"]
    ) + powerflow.dbarraDF["demanda_reativa"][idx]

    return q


def pcalcsym(
    powerflow,
    v,
    t,
    idx: int = None,
):
    """cálculo da potência ativa de cada barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência ativa

    Retorno
        p: float
            potência ativa calculada para o barramenpara `idx`
    """

    ## Inicialização
    from sympy.functions import cos, sin

    # Variável de potência ativa calculada para o barramento para `idx`
    p = powerflow.gdiag[idx] * v[idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinhaDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["para"].iloc[lin] - 1
            p -= v[bus] * (
                powerflow.admitancia[lin].real * cos(t[idx] - t[bus])
                + powerflow.admitancia[lin].imag * sin(t[idx] - t[bus])
            )
        elif idx == powerflow.dlinhaDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["de"].iloc[lin] - 1
            p -= v[bus] * (
                powerflow.admitancia[lin].real * cos(t[idx] - t[bus])
                + powerflow.admitancia[lin].imag * sin(t[idx] - t[bus])
            )

    p *= v[idx]

    return p


def qcalcsym(
    powerflow,
    v,
    t,
    idx: int = None,
):
    """cálculo da potência reativa de cada barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência reativa

    Retorno
        q: float
            potência reativa calculada para o barramenpara `idx`
    """

    ## Inicialização
    from sympy.functions import cos, sin

    # Variável de potência reativa calculada para o barramento para `idx`
    q = -powerflow.bdiag[idx] * v[idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinhaDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["para"].iloc[lin] - 1
            q -= v[bus] * (
                powerflow.admitancia[lin].real * sin(t[idx] - t[bus])
                - powerflow.admitancia[lin].imag * cos(t[idx] - t[bus])
            )
        elif idx == powerflow.dlinhaDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinhaDF["de"].iloc[lin] - 1
            q -= v[bus] * (
                powerflow.admitancia[lin].real * sin(t[idx] - t[bus])
                - powerflow.admitancia[lin].imag * cos(t[idx] - t[bus])
            )

    q *= v[idx]

    return q
