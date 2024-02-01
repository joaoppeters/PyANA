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
    seterr(all="ignore")

    # Variáveis
    if not hasattr(powerflow, "qlimkeys"):
        powerflow.qlimkeys = dict()
        powerflow.diffqlim = dict()

    if powerflow.qlimkeys.get(powerflow.dbarraDF.loc[idx, "nome"]) is None:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]] = dict()

    if case not in powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]]:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case] = list()

    # Variáveis Simbólicas
    qger = Symbol("Qg")
    vger = Symbol("V")
    vesp = Symbol("Vesp")
    qmax = Symbol("Qmax")
    qmin = Symbol("Qmin")

    # Associação das variáveis
    powerflow.qlimsvar =  {
        qger: powerflow.solution["qlim_reactive_generation"][idx]
        / powerflow.options["BASE"],
        vger: powerflow.solution["voltage"][idx],
        vesp: powerflow.dbarraDF.loc[idx, "tensao"] * 1e-3,
        qmax: powerflow.dbarraDF.loc[idx, "potencia_reativa_maxima"]
        / powerflow.options["BASE"],
        qmin: powerflow.dbarraDF.loc[idx, "potencia_reativa_minima"]
        / powerflow.options["BASE"],
    }

    ## Limites
    # Limites de Tensão
    vlimsup = vesp + powerflow.options["SIGV"]
    vliminf = vesp - powerflow.options["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qmax - powerflow.options["SIGQ"]
    qliminf = qmin + powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    ch1 = 1 / (1 + spexp(-powerflow.options["SIGK"] * (qger - qlimsup)))

    # Chave Inferior de Potência Reativa
    ch2 = 1 / (1 + spexp(powerflow.options["SIGK"] * (qger - qliminf)))

    # Chave Superior de Tensão
    ch3 = 1 / (1 + spexp(powerflow.options["SIGK"] * (vger - vlimsup)))

    # Chave Inferior de Tensão
    ch4 = 1 / (1 + spexp(-powerflow.options["SIGK"] * (vger - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (vger - vesp)

    # Superior
    Ysuperior = (ch1 * ch3) * (1 - ch2 * ch4) * (qger - qmax)

    # Inferior
    Yinferior = (1 - ch1 * ch3) * (ch2 * ch4) * (qger - qmin)

    ## Derivadas
    # Derivada Parcial de Y por Qg
    powerflow.diffyqg = (Ynormal + Ysuperior + Yinferior).diff(qger)

    # Derivada Parcial de Y por V
    powerflow.diffyv = (Ynormal + Ysuperior + Yinferior).diff(vger)

    # Expressão Geral
    powerflow.diffqlim[idx] = array(
        [powerflow.diffyv.subs(powerflow.qlimsvar), powerflow.diffyqg.subs(powerflow.qlimsvar)], dtype="float64"
    )

    ## Resíduo
    powerflow.deltaQlim[nger] = (
        -Ynormal.subs(powerflow.qlimsvar) - Ysuperior.subs(powerflow.qlimsvar) - Yinferior.subs(powerflow.qlimsvar)
    )

    ## Armazenamento de valores das chaves
    powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case].append(
        array([ch1.subs(powerflow.qlimsvar), ch2.subs(powerflow.qlimsvar), ch3.subs(powerflow.qlimsvar), ch4.subs(powerflow.qlimsvar)])
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
    seterr(all="ignore")

    # Variáveis
    if not hasattr(powerflow, "qlimkeys"):
        powerflow.qlimkeys = dict()
        powerflow.diffqlim = dict()

    if powerflow.qlimkeys.get(powerflow.dbarraDF.loc[idx, "nome"]) is None:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]] = dict()

    if case not in powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]]:
        powerflow.qlimkeys[powerflow.dbarraDF.loc[idx, "nome"]][case] = list()

    # Variáveis Simbólicas
    qger = (
        powerflow.solution["qlim_reactive_generation"][idx] / powerflow.options["BASE"]
    )
    vger = powerflow.solution["voltage"][idx]
    vesp = powerflow.dbarraDF.loc[idx, "tensao"] * 1e-3
    qmax = (
        powerflow.dbarraDF.loc[idx, "potencia_reativa_maxima"]
        / powerflow.options["BASE"]
    )
    qmin = (
        powerflow.dbarraDF.loc[idx, "potencia_reativa_minima"]
        / powerflow.options["BASE"]
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vesp + powerflow.options["SIGV"]
    vliminf = vesp - powerflow.options["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qmax - powerflow.options["SIGQ"]
    qliminf = qmin + powerflow.options["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    ch1 = 1 / (1 + npexp(-powerflow.options["SIGK"] * (qger - qlimsup)))

    # Chave Inferior de Poência Reativa
    ch2 = 1 / (1 + npexp(powerflow.options["SIGK"] * (qger - qliminf)))

    # Chave Superior de Tensão
    ch3 = 1 / (1 + npexp(powerflow.options["SIGK"] * (vger - vlimsup)))

    # Chave Inferior de Tensão
    ch4 = 1 / (1 + npexp(-powerflow.options["SIGK"] * (vger - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (vger - vesp)

    # Superior
    Ysuperior = (ch1 * ch3) * (1 - ch2 * ch4) * (qger - qmax)

    # Inferior
    Yinferior = (1 - ch1 * ch3) * (ch2 * ch4) * (qger - qmin)

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

    powerflow.svcqvar =  deepcopy(powerflow.svcqvarkey)
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
        -Yindutiva.subs(powerflow.svcqvar) - Ylinear.subs(powerflow.svcqvar) - Ycapacitiva.subs(powerflow.svcqvar)
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

    powerflow.svcivar =  deepcopy(powerflow.svcivarkey)
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
        -Yindutiva.subs(powerflow.svcivar) - Ylinear.subs(powerflow.svcivar) - Ycapacitiva.subs(powerflow.svcivar)
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
    powerflow.svcavar =  {
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

    powerflow.svcavar =  {
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

            qmax = powerflow.dbarraDF.loc[
                powerflow.dbarraDF["nome"] == busname,
                "potencia_reativa_maxima",
            ].values[0]
            qmin = powerflow.dbarraDF.loc[
                powerflow.dbarraDF["nome"] == busname,
                "potencia_reativa_minima",
            ].values[0]
            vesp = (
                powerflow.dbarraDF.loc[
                    powerflow.dbarraDF["nome"] == busname, "tensao"
                ].values[0]
                * 1e-3
            )

            ch1space = linspace(
                start=(qmax - (powerflow.options["SIGQ"] * 1e1)),
                stop=(qmax + (powerflow.options["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch1value = 1 / (
                1
                + npexp(
                    -powerflow.options["SIGK"]
                    * (ch1space - qmax + powerflow.options["SIGQ"])
                )
            )

            ch2space = linspace(
                start=(qmin - (powerflow.options["SIGQ"] * 1e1)),
                stop=(qmin + (powerflow.options["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch2value = 1 / (
                1
                + npexp(
                    powerflow.options["SIGK"]
                    * (ch2space - qmin - powerflow.options["SIGQ"])
                )
            )

            chvspace = linspace(
                start=(vesp - (powerflow.options["SIGV"] * 1e1)),
                stop=(vesp + (powerflow.options["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch3value = 1 / (
                1
                + npexp(
                    powerflow.options["SIGK"]
                    * (chvspace - vesp - powerflow.options["SIGV"])
                )
            )
            ch4value = 1 / (
                1
                + npexp(
                    -powerflow.options["SIGK"]
                    * (chvspace - vesp + powerflow.options["SIGV"])
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
                xmin=(qmax - 0.5),
                xmax=(qmax + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax1.vlines(
                x=qmax,
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
                xmin=(qmax - 1e-2),
                xmax=(qmax + 0.5),
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
                xmin=(qmin - 0.5),
                xmax=(qmin + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax2.vlines(
                x=qmin,
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
                xmin=(qmin - 1e-2),
                xmax=(qmin + 0.5),
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
                xmin=(vesp - 0.5),
                xmax=(vesp + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax3.vlines(
                x=vesp,
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
                xmin=(vesp - 1e-2),
                xmax=(vesp + 0.5),
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
                xmin=(vesp - 0.5),
                xmax=(vesp + 1e-2),
                color=(
                    0.0,
                    0.0,
                    0.0,
                ),
            )
            ax4.vlines(
                x=vesp,
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
                xmin=(vesp - 1e-2),
                xmax=(vesp + 0.5),
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
