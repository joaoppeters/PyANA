# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from matplotlib import pyplot as plt
from numpy import abs, array, exp as npexp, linspace, min as mn, pi, seterr
from sympy import Symbol
from sympy.functions import exp as spexp

from folder import smoothfolder


def qlims(
    powerflow,
    idx,
    value,
):
    """_summary_

    Parametros:
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    seterr(all="ignore")

    powerflow.qlimkeys[value["nome"]] = dict()
    powerflow.qlimkeys[value["nome"]][0] = list()

    powerflow.qlimsch[idx] = dict()
    powerflow.qlimsch[idx]["ch1"] = list()
    powerflow.qlimsch[idx]["ch2"] = list()
    powerflow.qlimsch[idx]["ch3"] = list()
    powerflow.qlimsch[idx]["ch4"] = list()

    # Variáveis Simbólicas
    qg = Symbol("qg%s" % idx)
    v = Symbol("v%s" % idx)
    vr = Symbol("vr%s" % idx)
    qgx = Symbol("qgx%s" % idx)
    qgn = Symbol("qgn%s" % idx)

    # Associação das variáveis
    powerflow.qlimsvar.update(
        {
            qg: powerflow.solution["qlim_reactive_generation"][idx]
            / powerflow.options["BASE"],
            v: powerflow.solution["voltage"][idx],
            vr: value["tensao"] * 1e-3,
            qgx: value["potencia_reativa_maxima"] / powerflow.options["BASE"],
            qgn: value["potencia_reativa_minima"] / powerflow.options["BASE"],
        }
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vr + powerflow.options["SIGV"]
    vliminf = vr - powerflow.options["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - powerflow.options["SIGQ"]
    qliminf = qgn + powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    powerflow.qlimsch[idx]["ch1"] = 1 / (
        1 + spexp(-powerflow.options["SIGK"] * (qg - qlimsup))
    )

    # Chave Inferior de Potência Reativa
    powerflow.qlimsch[idx]["ch2"] = 1 / (
        1 + spexp(powerflow.options["SIGK"] * (qg - qliminf))
    )

    # Chave Superior de Tensão
    powerflow.qlimsch[idx]["ch3"] = 1 / (
        1 + spexp(powerflow.options["SIGK"] * (v - vlimsup))
    )

    # Chave Inferior de Tensão
    powerflow.qlimsch[idx]["ch4"] = 1 / (
        1 + spexp(-powerflow.options["SIGK"] * (v - vliminf))
    )

    ## Equações de Controle
    # Normal
    Ynormal = (
        (1 - powerflow.qlimsch[idx]["ch1"] * powerflow.qlimsch[idx]["ch3"])
        * (1 - powerflow.qlimsch[idx]["ch2"] * powerflow.qlimsch[idx]["ch4"])
        * (v - vr)
    )

    # Superior
    Ysuperior = (
        (powerflow.qlimsch[idx]["ch1"] * powerflow.qlimsch[idx]["ch3"])
        * (1 - powerflow.qlimsch[idx]["ch2"] * powerflow.qlimsch[idx]["ch4"])
        * (qg - qgx)
    )

    # Inferior
    Yinferior = (
        (1 - powerflow.qlimsch[idx]["ch1"] * powerflow.qlimsch[idx]["ch3"])
        * (powerflow.qlimsch[idx]["ch2"] * powerflow.qlimsch[idx]["ch4"])
        * (qg - qgn)
    )

    powerflow.Y[idx] = [Ynormal, Ysuperior, Yinferior]

    ## Derivadas
    # Derivada Parcial de Y por Qg
    powerflow.diffyqg[idx] = (powerflow.Y[idx][0] + powerflow.Y[idx][1] + powerflow.Y[idx][2]).diff(qg)

    # Derivada Parcial de Y por V
    powerflow.diffyv[idx] = (powerflow.Y[idx][0] + powerflow.Y[idx][1] + powerflow.Y[idx][2]).diff(v)


def qlimssmooth(
    idx,
    powerflow,
    nger,
    case,
):
    """aplicação da função suave sigmoide para tratamento de limite de geração de potência reativa

    Parâmetros
        idx: índice da da barra geradora
        powerflow: self do arquivo powerflow.py
        nger: índice de geradores
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    if case not in powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]]:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case] = list()

    # Expressão Geral
    powerflow.diffqlim[idx] = array(
        [
            powerflow.diffyv[idx].subs(powerflow.qlimsvar),
            powerflow.diffyqg[idx].subs(powerflow.qlimsvar),
        ],
        dtype="float64",
    )

    ## Resíduo
    powerflow.deltaQlim[nger] = (
        - powerflow.Y[nger][0].subs(powerflow.qlimsvar)
        - powerflow.Y[nger][1].subs(powerflow.qlimsvar)
        - powerflow.Y[nger][2].subs(powerflow.qlimsvar)
    )

    ## Armazenamento de valores das chaves
    powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case].append(
        array(
            [
                powerflow.qlimsch[idx]["ch1"].subs(powerflow.qlimsvar),
                powerflow.qlimsch[idx]["ch2"].subs(powerflow.qlimsvar),
                powerflow.qlimsch[idx]["ch3"].subs(powerflow.qlimsvar),
                powerflow.qlimsch[idx]["ch4"].subs(powerflow.qlimsvar),
            ]
        )
    )


def qlimnsmooth(
    idx,
    powerflow,
    nger,
    case,
):
    """aplicação da função suave sigmoide para tratamento de limite de geração de potência reativa

    Parâmetros
        idx: índice da da barra geradora
        powerflow: self do arquivo powerflow.py
        nger: índice de geradores
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    if case not in powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]]:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case] = list()

    # Variáveis Simbólicas
    qg = powerflow.solution["qlim_reactive_generation"][idx] / powerflow.options["BASE"]
    v = powerflow.solution["voltage"][idx]
    vr = powerflow.dbarraDF.loc[idx, "tensao"] * 1e-3
    qgx = (
        powerflow.dbarraDF.loc[idx, "potencia_reativa_maxima"]
        / powerflow.options["BASE"]
    )
    qgn = (
        powerflow.dbarraDF.loc[idx, "potencia_reativa_minima"]
        / powerflow.options["BASE"]
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vr + powerflow.options["SIGV"]
    vliminf = vr - powerflow.options["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - powerflow.options["SIGQ"]
    qliminf = qgn + powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    ch1 = 1 / (1 + npexp(-powerflow.options["SIGK"] * (qg - qlimsup)))

    # Chave Inferior de Poência Reativa
    ch2 = 1 / (1 + npexp(powerflow.options["SIGK"] * (qg - qliminf)))

    # Chave Superior de Tensão
    ch3 = 1 / (1 + npexp(powerflow.options["SIGK"] * (v - vlimsup)))

    # Chave Inferior de Tensão
    ch4 = 1 / (1 + npexp(-powerflow.options["SIGK"] * (v - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (v - vr)

    # Superior
    Ysuperior = (ch1 * ch3) * (1 - ch2 * ch4) * (qg - qgx)

    # Inferior
    Yinferior = (1 - ch1 * ch3) * (ch2 * ch4) * (qg - qgn)

    ## Derivadas
    # Expressão Geral
    powerflow.diffqlim[idx] = array(
        [
            (1 - ch1 * ch3) * (1 - ch2 * ch4),  # Derivada Parcial de Y por V
            (ch1 * ch3) * (1 - ch2 * ch4)
            + (ch2 * ch4) * (1 - ch1 * ch3),  # Derivada Parcial de Y por Qg
        ],
        dtype="float64",
    )

    ## Resíduo
    powerflow.deltaQlim[nger] = -Ynormal - Ysuperior - Yinferior

    ## Armazenamento de valores das chaves
    powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case].append(
        array([ch1, ch2, ch3, ch4])
    )


def svcreactivesmooth(
    idxcer,
    idxctrl,
    powerflow,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por potência reativa injetada

    Parâmetros
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        powerflow: self do arquivo powerflow.py
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    seterr(all="ignore")

    # Variáveis
    if not hasattr(powerflow, "svckeys"):
        powerflow.svckeys = dict()
        powerflow.diffsvc = dict()

    if powerflow.svckeys.get(powerflow.dbarraDF.loc[idxcer, "nome"]) is None:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]] = dict()

    if case not in powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]]:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("Vk")
    vm = Symbol("Vm")

    qgk = Symbol("Qgk")
    r = Symbol("r")

    bmin = Symbol("Bmin")
    bmax = Symbol("Bmax")

    vmsch = powerflow.dbarraDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (r * bmin * (vk**2))
    vmmin = vmsch + (r * bmax * (vk**2))

    # Associação das variáveis
    powerflow.svcqvarkey = {
        vk: powerflow.solution["voltage"][idxcer],
        vm: powerflow.solution["voltage"][idxctrl],
        r: powerflow.dcerDF.loc[ncer, "droop"],
        bmin: powerflow.dcerDF.loc[ncer, "potencia_reativa_minima"]
        / (
            powerflow.options["BASE"]
            * (powerflow.dbarraDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
        ),
        bmax: powerflow.dcerDF.loc[ncer, "potencia_reativa_maxima"]
        / (
            powerflow.options["BASE"]
            * (powerflow.dbarraDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
        ),
    }

    powerflow.svcqvar = deepcopy(powerflow.svcqvarkey)
    powerflow.svcqvar[qgk] = (powerflow.solution["svc_reactive_generation"][ncer]) / (
        powerflow.options["BASE"]
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vmmax + powerflow.options["SIGV"]
    vliminf = vmmin - powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa - Região Indutiva
    ch1 = 1 / (1 + spexp(-powerflow.options["SIGK"] * (vm - vlimsup)))

    # Chave Inferior de Poência Reativa - Região Capacitiva
    ch2 = 1 / (1 + spexp(powerflow.options["SIGK"] * (vm - vliminf)))

    ## Equações de Controle
    # Região Indutiva
    Yindutiva = (ch1) * (-(vk**2) * bmin + qgk)

    # Região Linear
    Ylinear = (1 - ch1) * (1 - ch2) * (-vmsch - (r * qgk) + vm)

    # Região Capacitiva
    Ycapacitiva = (ch2) * (-(vk**2) * bmax + qgk)

    ## Derivadas
    # Derivada Parcial de Y por Vk
    powerflow.diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

    # Derivada Parcial de Y por Vm
    powerflow.diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

    # Derivada Parcial de Y por Qgk
    powerflow.diffyqgk = (Yindutiva + Ylinear + Ycapacitiva).diff(qgk)

    # Expressão Geral
    powerflow.diffsvc[idxcer] = array(
        [
            powerflow.diffyvk.subs(powerflow.svcqvar),
            powerflow.diffyvm.subs(powerflow.svcqvar),
            powerflow.diffyqgk.subs(powerflow.svcqvar),
        ],
        dtype="float64",
    )

    ## Resíduo
    powerflow.deltaSVC[ncer] = (
        -Yindutiva.subs(powerflow.svcqvar)
        - Ylinear.subs(powerflow.svcqvar)
        - Ycapacitiva.subs(powerflow.svcqvar)
    )

    ## Armazenamento de valores das chaves
    powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case].append(
        array(
            [
                ch1.subs(powerflow.svcqvarkey),
                ch2.subs(powerflow.svcqvarkey),
            ],
            dtype="float",
        )
    )


def svccurrentsmooth(
    idxcer,
    idxctrl,
    powerflow,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por corrente injetada

    Parâmetros
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        powerflow: self do arquivo powerflow.py
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    seterr(all="ignore")

    # Variáveis
    if not hasattr(powerflow, "svckeys"):
        powerflow.svckeys = dict()
        powerflow.diffsvc = dict()

    if powerflow.svckeys.get(powerflow.dbarraDF.loc[idxcer, "nome"]) is None:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]] = dict()

    if case not in powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]]:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("Vk")
    vm = Symbol("Vm")

    ik = Symbol("Ik")
    r = Symbol("r")

    bmin = Symbol("Bmin")
    bmax = Symbol("Bmax")

    vmsch = powerflow.dbarraDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (r * bmin * vk)
    vmmin = vmsch + (r * bmax * vk)

    # Associação das variáveis
    powerflow.svcivarkey = {
        vk: powerflow.solution["voltage"][idxcer],
        vm: powerflow.solution["voltage"][idxctrl],
        r: powerflow.dcerDF.loc[ncer, "droop"],
        bmin: powerflow.dcerDF.loc[ncer, "potencia_reativa_minima"]
        / (
            powerflow.options["BASE"]
            * powerflow.dbarraDF.loc[idxcer, "tensao_base"]
            * 1e-3
        ),
        bmax: powerflow.dcerDF.loc[ncer, "potencia_reativa_maxima"]
        / (
            powerflow.options["BASE"]
            * powerflow.dbarraDF.loc[idxcer, "tensao_base"]
            * 1e-3
        ),
    }

    powerflow.svcivar = deepcopy(powerflow.svcivarkey)
    powerflow.svcivar[ik] = (powerflow.solution["svc_current_injection"][ncer]) / (
        powerflow.options["BASE"]
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vmmax + powerflow.options["SIGV"]
    vliminf = vmmin - powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa - Região Indutiva
    ch1 = 1 / (1 + spexp(-powerflow.options["SIGK"] * (vm - vlimsup)))

    # Chave Inferior de Poência Reativa - Região Capacitiva
    ch2 = 1 / (1 + spexp(powerflow.options["SIGK"] * (vm - vliminf)))

    ## Equações de Controle
    # Região Indutiva
    Yindutiva = (ch1) * (-vk * bmin + ik)

    # Região Linear
    Ylinear = (1 - ch1) * (1 - ch2) * (-vmsch - (r * ik) + vm)

    # Região Capacitiva
    Ycapacitiva = (ch2) * (-vk * bmax + ik)

    ## Derivadas
    # Derivada Parcial de Y por Vk
    powerflow.diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

    # Derivada Parcial de Y por Vm
    powerflow.diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

    # Derivada Parcial de Y por Ik
    powerflow.diffyik = (Yindutiva + Ylinear + Ycapacitiva).diff(ik)

    # Expressão Geral
    powerflow.diffsvc[idxcer] = array(
        [
            powerflow.diffyvk.subs(powerflow.svcivar),
            powerflow.diffyvm.subs(powerflow.svcivar),
            powerflow.diffyik.subs(powerflow.svcivar),
        ],
        dtype="float64",
    )

    ## Resíduo
    powerflow.deltaSVC[ncer] = (
        -Yindutiva.subs(powerflow.svcivar)
        - Ylinear.subs(powerflow.svcivar)
        - Ycapacitiva.subs(powerflow.svcivar)
    )

    ## Armazenamento de valores das chaves
    powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case].append(
        array(
            [
                ch1.subs(powerflow.svcivarkey),
                ch2.subs(powerflow.svcivarkey),
            ],
            dtype="float",
        )
    )


def svcalphasmooth(
    idxcer,
    idxctrl,
    powerflow,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por ângulo de disparo

    Parâmetros
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        powerflow: self do arquivo powerflow.py
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    seterr(all="ignore")

    # Variáveis
    if not hasattr(powerflow, "svckeys"):
        powerflow.svckeys = dict()
        powerflow.diffsvc = dict()

    if powerflow.svckeys.get(powerflow.dbarraDF.loc[idxcer, "nome"]) is None:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]] = dict()

    if case not in powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]]:
        powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("Vk")
    vm = Symbol("Vm")

    r = Symbol("r")
    alpha = Symbol("alpha")

    vmsch = powerflow.dbarraDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (
        powerflow.dcerDF.loc[ncer, "droop"]
        * powerflow.alphabeq.subs(alpha, pi / 2)
        * (powerflow.solution["voltage"][idxcer] ** 2)
    )
    vmmin = vmsch + (
        powerflow.dcerDF.loc[ncer, "droop"]
        * powerflow.alphabeq.subs(alpha, pi)
        * (powerflow.solution["voltage"][idxcer] ** 2)
    )

    # Associação das variáveis
    powerflow.svcavar = {
        vk: powerflow.solution["voltage"][idxcer],
        vm: powerflow.solution["voltage"][idxctrl],
        r: powerflow.dcerDF.loc[ncer, "droop"],
        alpha: powerflow.solution["alpha"],
    }

    ## Limites
    # Limites de Ângulo de disparo
    alphalimsup = pi - powerflow.options["SIGA"]
    alphaliminf = pi / 2 + powerflow.options["SIGA"]

    # Limites de Tensão
    vlimsup = vmmax + powerflow.options["SIGV"]
    vliminf = vmmin - powerflow.options["SIGV"]

    ## Chaves
    # Chave Inferior de Ângulo de disparo
    ch1 = 1 / (
        1
        + npexp(powerflow.options["SIGK"] * (powerflow.solution["alpha"] - alphaliminf))
    )

    # Chave Superior de Ângulo de disparo
    ch2 = 1 / (
        1
        + npexp(
            -powerflow.options["SIGK"] * (powerflow.solution["alpha"] - alphalimsup)
        )
    )

    # Chave Inferior de Tensão
    ch3 = 1 / (
        1
        + npexp(
            powerflow.options["SIGK"]
            * float(powerflow.solution["voltage"][idxctrl] - vliminf)
        )
    )

    # Chave Superior de Tensao
    ch4 = 1 / (
        1
        + npexp(
            -powerflow.options["SIGK"]
            * float(powerflow.solution["voltage"][idxctrl] - vlimsup)
        )
    )

    # Equações de Controle

    # ch1 = sw10
    # ch2 = sw9
    # ch3 = sw12
    # ch4 = sw11

    # Região Indutiva
    Yindutiva = ch1 * (1 - ch3) * (alpha - pi / 2)

    # Região Linear
    Ylinear = (
        (1 - ch1) * (1 - ch3) * ch4
        + (1 - ch2) * (1 - ch4) * ch3
        + (1 - ch1) * (1 - ch2) * (1 - ch3) * (1 - ch4)
    ) * (-vmsch - (r * (vk**2) * powerflow.alphabeq) + vm)

    # Região Capacitiva
    Ycapacitiva = ch2 * (1 - ch4) * (alpha - pi)

    ## Derivadas
    # Derivada Parcial de Y por Vk
    powerflow.diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

    # Derivada Parcial de Y por Vm
    powerflow.diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

    # Derivada Parcial de Y por alpha
    powerflow.diffyalpha = (Yindutiva + Ylinear + Ycapacitiva).diff(alpha)

    if powerflow.solution["alpha"] <= pi / 2 + powerflow.options["SIGA"]:
        # powerflow.solution['alpha'] = pi/2
        if powerflow.solution["voltage"][idxctrl] <= vmmin:
            powerflow.solution["voltage"][idxctrl] = deepcopy(vmsch)
            powerflow.solution["alpha"] = deepcopy(powerflow.solution["alpha0"])

    elif powerflow.solution["alpha"] >= pi - powerflow.options["SIGA"]:
        # powerflow.solution['alpha'] = pi
        if powerflow.solution["voltage"][idxctrl] >= vmmax:
            powerflow.solution["voltage"][idxctrl] = deepcopy(vmsch)
            powerflow.solution["alpha"] = deepcopy(powerflow.solution["alpha0"])

    powerflow.svcavar = {
        vk: powerflow.solution["voltage"][idxcer],
        vm: powerflow.solution["voltage"][idxctrl],
        r: powerflow.dcerDF["droop"][0],
        alpha: powerflow.solution["alpha"],
    }

    powerflow.solution["svc_reactive_generation"][ncer] = (
        (powerflow.solution["voltage"][idxcer] ** 2)
        * powerflow.alphabeq.subs(alpha, powerflow.solution["alpha"])
        * powerflow.options["BASE"]
    )

    # Expressão Geral
    powerflow.diffsvc[idxcer] = array(
        [
            powerflow.diffyvk.subs(powerflow.svcavar),
            powerflow.diffyvm.subs(powerflow.svcavar),
            powerflow.diffyalpha.subs(powerflow.svcavar),
        ],
        dtype="float64",
    )

    ## Resíduo
    powerflow.deltaSVC[ncer] = (
        -Yindutiva.subs(
            {
                vm: powerflow.solution["voltage"][idxctrl],
                alpha: powerflow.solution["alpha"],
            }
        )
        - Ylinear.subs(powerflow.svcavar)
        - Ycapacitiva.subs(
            {
                vm: powerflow.solution["voltage"][idxctrl],
                alpha: powerflow.solution["alpha"],
            }
        )
    )

    ## Armazenamento de valores das chaves
    powerflow.svckeys[powerflow.dbarraDF.loc[idxcer, "nome"]][case].append(
        array(
            [
                ch1,
                ch2,
                ch3,
                ch4,
            ],
            dtype="float",
        )
    )


def qlimspop(
    powerflow,
    pop: int = 1,
):
    """deleta última instância salva em variável powerflow.qlimskeys

    Parâmetros
        powerflow: self do arquivo powerflow.py
        pop: quantidade de ações necessárias
    """

    ## Inicialização
    for _, value in powerflow.dbarraDF.iterrows():
        popped = 0
        if value["tipo"] != 0:
            while popped < pop:
                powerflow.qlimkeys[value["nome"]].popitem()
                popped += 1


def qlimstorage(
    powerflow,
):
    """armazenamento e geração de imagens referente a comutação das chaves

    Parâmetros:
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Criação automática de diretório
    smoothfolder(
        powerflow,
    )

    # Condição de método
    if powerflow.method == "CPF":
        # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
        for key, value in powerflow.point.items():
            if key == 0:
                casekeymin = key
                casevalmin = mn(abs(value["eigenvalues-QV"]))

            elif (
                (key > 0)
                and (mn(value["c"]["eigenvalues-QV"]) < casevalmin)
                and (mn(value["c"]["eigenvalues-QV"] > 0))
            ):
                casekeymin = key
                casevalmin = mn(abs(value["c"]["eigenvalues-QV"]))

        # Loop
        for busname, _ in powerflow.qlimkeys.items():
            # Variáveis
            busidx = powerflow.dbarraDF.index[
                powerflow.dbarraDF["nome"] == busname
            ].tolist()[0]

            qgx = powerflow.dbarraDF.loc[
                powerflow.dbarraDF["nome"] == busname,
                "potencia_reativa_maxima",
            ].values[0]
            qgn = powerflow.dbarraDF.loc[
                powerflow.dbarraDF["nome"] == busname,
                "potencia_reativa_minima",
            ].values[0]
            vr = (
                powerflow.dbarraDF.loc[
                    powerflow.dbarraDF["nome"] == busname, "tensao"
                ].values[0]
                * 1e-3
            )

            ch1space = linspace(
                start=(qgx - (powerflow.options["SIGQ"] * 1e1)),
                stop=(qgx + (powerflow.options["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch1value = 1 / (
                1
                + npexp(
                    -powerflow.options["SIGK"]
                    * (ch1space - qgx + powerflow.options["SIGQ"])
                )
            )

            ch2space = linspace(
                start=(qgn - (powerflow.options["SIGQ"] * 1e1)),
                stop=(qgn + (powerflow.options["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch2value = 1 / (
                1
                + npexp(
                    powerflow.options["SIGK"]
                    * (ch2space - qgn - powerflow.options["SIGQ"])
                )
            )

            chvspace = linspace(
                start=(vr - (powerflow.options["SIGV"] * 1e1)),
                stop=(vr + (powerflow.options["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch3value = 1 / (
                1
                + npexp(
                    powerflow.options["SIGK"]
                    * (chvspace - vr - powerflow.options["SIGV"])
                )
            )
            ch4value = 1 / (
                1
                + npexp(
                    -powerflow.options["SIGK"]
                    * (chvspace - vr + powerflow.options["SIGV"])
                )
            )

            caseitems = powerflow.qlimkeys[busname][casekeymin - 1]
            smooth1 = [item[0] for item in caseitems][-1]
            smooth2 = [item[1] for item in caseitems][-1]
            smooth3 = [item[2] for item in caseitems][-1]
            smooth4 = [item[3] for item in caseitems][-1]

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
            # fig.tight_layout()
            fig.suptitle(f"Caso {casekeymin}")

            # smooth1
            ax1.hlines(
                y=0.0,
                xmin=(qgx - 0.5),
                xmax=(qgx + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.vlines(
                x=qgx,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.hlines(
                y=1.0,
                xmin=(qgx - 1e-2),
                xmax=(qgx + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.plot(
                ch1space,
                ch1value,
                color="tab:blue",
                alpha=0.75,
            )
            ax1.scatter(
                powerflow.point[casekeymin]["c"]["reactive"][busidx],
                smooth1,
                color="tab:blue",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax1.set_title("Chave 1 - Mvar máximo", fontsize=8)

            # smooth2
            ax2.hlines(
                y=1.0,
                xmin=(qgn - 0.5),
                xmax=(qgn + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.vlines(
                x=qgn,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.hlines(
                y=0.0,
                xmin=(qgn - 1e-2),
                xmax=(qgn + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.plot(
                ch2space,
                ch2value,
                color="tab:orange",
                alpha=0.75,
            )
            ax2.scatter(
                powerflow.point[casekeymin]["c"]["reactive"][busidx],
                smooth2,
                color="tab:orange",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax2.set_title("Chave 2 - Mvar mínimo", fontsize=8)

            # smooth3
            ax3.hlines(
                y=1.0,
                xmin=(vr - 0.5),
                xmax=(vr + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax3.vlines(
                x=vr,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax3.hlines(
                y=0.0,
                xmin=(vr - 1e-2),
                xmax=(vr + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax3.plot(
                chvspace,
                ch3value,
                color="tab:green",
                alpha=0.75,
            )
            ax3.scatter(
                powerflow.point[casekeymin]["c"]["voltage"][busidx],
                smooth3,
                color="tab:green",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax3.set_title("Chave 3 - Volt máximo", fontsize=8)

            # smooth4
            ax4.hlines(
                y=0.0,
                xmin=(vr - 0.5),
                xmax=(vr + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax4.vlines(
                x=vr,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax4.hlines(
                y=1.0,
                xmin=(vr - 1e-2),
                xmax=(vr + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax4.plot(
                chvspace,
                ch4value,
                color="tab:red",
                alpha=0.75,
            )
            ax4.scatter(
                powerflow.point[casekeymin]["c"]["voltage"][busidx],
                smooth4,
                color="tab:red",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax4.set_title("Chave 4 - Volt mínimo", fontsize=8)

            fig.savefig(powerflow.dirsmoothsys + "smooth-" + busname + ".png", dpi=400)
            plt.close(fig)


def svcstorage(
    powerflow,
):
    """armazenamento e geração de imagens referente a comutação das chaves

    Parâmetros:
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Criação automática de diretório
    smoothfolder(
        powerflow,
    )

    # Condição de método
    if powerflow.method == "CPF":
        # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
        for key, value in powerflow.point.items():
            if key == 0:
                casekeymin = key
                casevalmin = mn(abs(value["eigenvalues-QV"]))

            elif (
                (key > 0)
                and (mn(value["c"]["eigenvalues-QV"]) < casevalmin)
                and (mn(value["c"]["eigenvalues-QV"] > 0))
            ):
                casekeymin = key
                casevalmin = mn(abs(value["c"]["eigenvalues-QV"]))

        powerflow.pointkeymin = deepcopy(casekeymin)

        # Loop
        for busname, _ in powerflow.svckeys.items():
            # Variáveis
            busidx = powerflow.dbarraDF.index[
                powerflow.dbarraDF["nome"] == busname
            ].tolist()[0]
            busidxcer = powerflow.dcerDF.index[
                powerflow.dcerDF["barra"] == powerflow.dbarraDF["numero"].iloc[busidx]
            ].tolist()[0]
            ctrlbusidxcer = powerflow.dbarraDF.index[
                powerflow.dbarraDF["numero"]
                == powerflow.dcerDF["barra_controlada"].iloc[busidxcer]
            ].tolist()[0]

            bmax = powerflow.dcerDF["potencia_reativa_maxima"].iloc[busidxcer]
            bmin = powerflow.dcerDF["potencia_reativa_minima"].iloc[busidxcer]
            vk = powerflow.solution["voltage"][busidx]
            vmref = powerflow.dbarraDF["tensao"].iloc[ctrlbusidxcer] * 1e-3
            droop = (
                powerflow.dcerDF["droop"].iloc[busidxcer] / powerflow.options["BASE"]
            )

            vmmax = vmref + (droop * bmin * (vk**2))
            vmmin = vmref + (droop * bmax * (vk**2))

            ch1space = linspace(
                start=(vmmax - (powerflow.options["SIGV"] * 1e1)),
                stop=(vmmax + (powerflow.options["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch1value = 1 / (
                1
                + npexp(
                    -powerflow.options["SIGK"]
                    * (ch1space - vmmax + powerflow.options["SIGV"])
                )
            )

            ch2space = linspace(
                start=(vmmin - (powerflow.options["SIGV"] * 1e1)),
                stop=(vmmin + (powerflow.options["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch2value = 1 / (
                1
                + npexp(
                    powerflow.options["SIGK"]
                    * (ch2space - vmmin - powerflow.options["SIGV"])
                )
            )

            caseitems = powerflow.svckeys[busname][casekeymin - 1]
            smooth1 = [item[0] for item in caseitems][-1]
            smooth2 = [item[1] for item in caseitems][-1]

            fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)
            fig.suptitle(f"Caso {casekeymin}")

            # smooth1
            ax1.hlines(
                y=0.0,
                xmin=(vmmax - 0.5),
                xmax=(vmmax + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.vlines(
                x=vmmax,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.hlines(
                y=1.0,
                xmin=(vmmax - 1e-2),
                xmax=(vmmax + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.plot(
                ch1space,
                ch1value,
                color="tab:blue",
                alpha=0.75,
            )
            ax1.scatter(
                powerflow.point[casekeymin]["c"]["voltage"][ctrlbusidxcer],
                smooth1,
                color="tab:blue",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax1.set_title("Chave 1 - V máximo", fontsize=8)

            # smooth2
            ax2.hlines(
                y=1.0,
                xmin=(vmmin - 0.5),
                xmax=(vmmin + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.vlines(
                x=vmmin,
                ymin=0.0,
                ymax=1.0,
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.hlines(
                y=0.0,
                xmin=(vmmin - 1e-2),
                xmax=(vmmin + 0.5),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.plot(
                ch2space,
                ch2value,
                color="tab:orange",
                alpha=0.75,
            )
            ax2.scatter(
                powerflow.point[casekeymin]["c"]["voltage"][ctrlbusidxcer],
                smooth2,
                color="tab:orange",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax2.set_title("Chave 2 - V mínimo", fontsize=8)

            fig.savefig(powerflow.dirsmoothsys + "smooth-" + busname + ".png", dpi=400)
            plt.close(fig)
