# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import cos, sin


def pcalc(
    anarede,
    idx: int = None,
):
    """calculo da potencia ativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia ativa

    Retorno
        p: float
            potencia ativa calculada para o barramenpara `idx`
    """
    # Variável de potência ativa calculada para o barramento para `idx`
    p = anarede.gdiag[idx] * anarede.solution["voltage"][idx]

    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )

    p *= anarede.solution["voltage"][idx]

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["active"][idx] = (p * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_ativa"
    ][idx]

    return p


def qcalc(
    anarede,
    idx: int = None,
):
    """calculo da potencia reativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia reativa

    Retorno
        q: float
            potencia reativa calculada para o barramenpara `idx`
    """
    # Variável de potência reativa calculada para o barramento para `idx`
    q = -anarede.bdiag[idx] * anarede.solution["voltage"][idx]

    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                - anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][bus] - anarede.solution["theta"][idx])
                - anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][bus] - anarede.solution["theta"][idx])
            )

    q *= anarede.solution["voltage"][idx]

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["reactive"][idx] = (q * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_reativa"
    ][idx]

    return q


def pcalct(
    anarede,
    idx: int = None,
):
    """calculo da potencia ativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia ativa

    Retorno
        p: float
            potencia ativa calculada para o barramenpara `idx`
    """
    # Variável de potência ativa calculada para o barramento para `idx`
    p = anarede.gdiag[idx] * anarede.solution["voltage"][idx]

    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                -anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                -anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )

    p *= anarede.solution["voltage"][idx]

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["active"][idx] = (p * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_ativa"
    ][idx]

    return p


def pcalcv(
    anarede,
    idx: int = None,
):
    """calculo da potencia ativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia ativa

    Retorno
        p: float
            potencia ativa calculada para o barramenpara `idx`
    """
    # Variável de potência ativa calculada para o barramento para `idx`
    p = anarede.gdiag[idx]

    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            p -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["active"][idx] = (p * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_ativa"
    ][idx]

    return p


def qcalct(
    anarede,
    idx: int = None,
):
    """calculo da potencia reativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia reativa

    Retorno
        q: float
            potencia reativa calculada para o barramenpara `idx`
    """
    # Variável de potência reativa calculada para o barramento para `idx`
    q = -anarede.bdiag[idx] * anarede.solution["voltage"][idx]

    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                + anarede.admitancia[lin].imag
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )

    q *= anarede.solution["voltage"][idx]

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["reactive"][idx] = (q * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_reativa"
    ][idx]

    return q


def qcalcv(
    anarede,
    idx: int = None,
):
    """calculo da potencia reativa de cada barra

    Args
        anarede:
        idx: int, obrigatorio, valor padrao None
            referencia o indice da barra a qual vai ser calculada a potencia reativa

    Retorno
        q: float
            potencia reativa calculada para o barramenpara `idx`
    """

    # Variável de potência reativa calculada para o barramento para `idx`
    q = -anarede.bdiag[idx]
    for lin in range(0, anarede.nlin):
        if idx == anarede.dlinDF["de"].iloc[lin] - 1:
            bus = anarede.dlinDF["para"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                - anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )
        elif idx == anarede.dlinDF["para"].iloc[lin] - 1:
            bus = anarede.dlinDF["de"].iloc[lin] - 1
            q -= anarede.solution["voltage"][bus] * (
                anarede.admitancia[lin].real
                * sin(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
                - anarede.admitancia[lin].imag
                * cos(anarede.solution["theta"][idx] - anarede.solution["theta"][bus])
            )

    # Armazenamenpara da potencia ativa gerada equivalente do barramento para
    anarede.solution["reactive"][idx] = (q * anarede.cte["BMVA"]) + anarede.dbarDF[
        "demanda_reativa"
    ][idx]

    return q
