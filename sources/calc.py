# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import cos, sin


def pcalc(
    powerflow,
    idx: int = None,
):
    """cálculo da potência ativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência ativa

    Retorno
        p: float
            potência ativa calculada para o barramenpara `idx`
    """
    ## Inicialização
    # Variável de potência ativa calculada para o barramento para `idx`
    p = powerflow.gdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
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
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
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
    ) + powerflow.dbarDF["demanda_ativa"][idx]

    return p


def qcalc(
    powerflow,
    idx: int = None,
):
    """cálculo da potência reativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência reativa

    Retorno
        q: float
            potência reativa calculada para o barramenpara `idx`
    """
    ## Inicialização
    # Variável de potência reativa calculada para o barramento para `idx`
    q = -powerflow.bdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
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
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
            q -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * sin(
                    powerflow.solution["theta"][bus] - powerflow.solution["theta"][idx]
                )
                - powerflow.admitancia[lin].imag
                * cos(
                    powerflow.solution["theta"][bus] - powerflow.solution["theta"][idx]
                )
            )

    q *= powerflow.solution["voltage"][idx]

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["reactive"][idx] = (
        q * powerflow.options["BASE"]
    ) + powerflow.dbarDF["demanda_reativa"][idx]

    return q


def pcalct(
    powerflow,
    idx: int = None,
):
    """cálculo da potência ativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência ativa

    Retorno
        p: float
            potência ativa calculada para o barramenpara `idx`
    """
    ## Inicialização
    # Variável de potência ativa calculada para o barramento para `idx`
    p = powerflow.gdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
            p -= powerflow.solution["voltage"][bus] * (
                -powerflow.admitancia[lin].real
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
            p -= powerflow.solution["voltage"][bus] * (
                -powerflow.admitancia[lin].real
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )

    p *= powerflow.solution["voltage"][idx]

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["active"][idx] = (
        p * powerflow.options["BASE"]
    ) + powerflow.dbarDF["demanda_ativa"][idx]

    return p


def pcalcv(
    powerflow,
    idx: int = None,
):
    """cálculo da potência ativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência ativa

    Retorno
        p: float
            potência ativa calculada para o barramenpara `idx`
    """
    ## Inicialização
    # Variável de potência ativa calculada para o barramento para `idx`
    p = powerflow.gdiag[idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
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
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
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

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["active"][idx] = (
        p * powerflow.options["BASE"]
    ) + powerflow.dbarDF["demanda_ativa"][idx]

    return p


def qcalct(
    powerflow,
    idx: int = None,
):
    """cálculo da potência reativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência reativa

    Retorno
        q: float
            potência reativa calculada para o barramenpara `idx`
    """
    ## Inicialização
    # Variável de potência reativa calculada para o barramento para `idx`
    q = -powerflow.bdiag[idx] * powerflow.solution["voltage"][idx]

    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
            q -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
            q -= powerflow.solution["voltage"][bus] * (
                powerflow.admitancia[lin].real
                * cos(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
                + powerflow.admitancia[lin].imag
                * sin(
                    powerflow.solution["theta"][idx] - powerflow.solution["theta"][bus]
                )
            )

    q *= powerflow.solution["voltage"][idx]

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["reactive"][idx] = (
        q * powerflow.options["BASE"]
    ) + powerflow.dbarDF["demanda_reativa"][idx]

    return q


def qcalcv(
    powerflow,
    idx: int = None,
):
    """cálculo da potência reativa de cada barra

    Args
        powerflow:
        idx: int, obrigatório, valor padrão None
            referencia o índice da barra a qual vai ser calculada a potência reativa

    Retorno
        q: float
            potência reativa calculada para o barramenpara `idx`
    """

    ## Inicialização
    # Variável de potência reativa calculada para o barramento para `idx`
    q = -powerflow.bdiag[idx]
    for lin in range(0, powerflow.nlin):
        if idx == powerflow.dlinDF["de"].iloc[lin] - 1:
            bus = powerflow.dlinDF["para"].iloc[lin] - 1
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
        elif idx == powerflow.dlinDF["para"].iloc[lin] - 1:
            bus = powerflow.dlinDF["de"].iloc[lin] - 1
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

    # Armazenamenpara da potência ativa gerada equivalente do barramento para
    powerflow.solution["reactive"][idx] = (
        q * powerflow.options["BASE"]
    ) + powerflow.dbarDF["demanda_reativa"][idx]

    return q
