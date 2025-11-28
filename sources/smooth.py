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
    anarede,
    idx,
    value,
):
    """_summary_

    Args:
        anarede:
    """
    ## Inicialização
    seterr(all="ignore")

    anarede.qlimkeys[value["nome"]] = dict()
    anarede.qlimkeys[value["nome"]][0] = list()

    anarede.qlimsch[idx] = dict()
    anarede.qlimsch[idx]["ch1"] = list()
    anarede.qlimsch[idx]["ch2"] = list()
    anarede.qlimsch[idx]["ch3"] = list()
    anarede.qlimsch[idx]["ch4"] = list()

    # Variáveis Simbólicas
    qg = Symbol("qg%s" % idx)
    v = Symbol("v%s" % idx)
    vr = Symbol("vr%s" % idx)
    qgx = Symbol("qgx%s" % idx)
    qgn = Symbol("qgn%s" % idx)

    # Associação das variáveis
    anarede.qlimvar.update(
        {
            qg: anarede.solution["qlim_reactive_generation"][idx] / anarede.cte["BASE"],
            v: anarede.solution["voltage"][idx],
            vr: value["tensao"] * 1e-3,
            qgx: value["potencia_reativa_maxima"] / anarede.cte["BASE"],
            qgn: value["potencia_reativa_minima"] / anarede.cte["BASE"],
        }
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vr + anarede.cte["SIGV"]
    vliminf = vr - anarede.cte["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - anarede.cte["SIGQ"]
    qliminf = qgn + anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    anarede.qlimsch[idx]["ch1"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (qg - qlimsup)))

    # Chave Inferior de Potência Reativa
    anarede.qlimsch[idx]["ch2"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (qg - qliminf)))

    # Chave Superior de Tensão
    anarede.qlimsch[idx]["ch3"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (v - vlimsup)))

    # Chave Inferior de Tensão
    anarede.qlimsch[idx]["ch4"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (v - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (v - vr)
    )

    # Superior
    Ysuperior = (
        (anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgx)
    )

    # Inferior
    Yinferior = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgn)
    )

    anarede.Y[idx] = [Ynormal, Ysuperior, Yinferior]

    ## Derivadas
    # Derivada Parcial de Y por Qg
    anarede.diffyqg[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(qg)

    # Derivada Parcial de Y por V
    anarede.diffyv[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(v)

    if anarede.method == "EXPC":
        anarede.diffyvv[idx] = anarede.diffyv[idx].diff(v)
        anarede.diffyqgv[idx] = anarede.diffyqg[idx].diff(v)
        anarede.diffyvqg[idx] = anarede.diffyv[idx].diff(qg)
        anarede.diffyqgqg[idx] = anarede.diffyqg[idx].diff(qg)


def qlimssmooth(
    idx,
    anarede,
    nger,
    case,
):
    """aplicação da função suave sigmoide para tratamento de limite de geração de potência reativa

    Args
        idx: índice da da barra geradora
        anarede:
        nger: índice de geradores
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    if case not in anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]]:
        anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]][case] = list()

    # Variáveis Simbólicas
    qg = Symbol("qg%s" % idx)
    v = Symbol("v%s" % idx)

    # Associação das variáveis
    anarede.qlimvar.update(
        {
            qg: anarede.solution["qlim_reactive_generation"][idx] / anarede.cte["BASE"],
            v: anarede.solution["voltage"][idx],
        }
    )

    # Expressão Geral
    if anarede.solution["method"] != "EXPC":
        anarede.qlimdiff[idx] = array(
            [
                anarede.diffyv[idx].subs(anarede.qlimvar),
                anarede.diffyqg[idx].subs(anarede.qlimvar),
            ],
            dtype="float64",
        )
    else:
        anarede.qlimdiff[idx] = array(
            [
                anarede.diffyv[idx].subs(anarede.qlimvar),
                anarede.diffyqg[idx].subs(anarede.qlimvar),
                anarede.diffyvv[idx].subs(anarede.qlimvar),
                anarede.diffyvqg[idx].subs(anarede.qlimvar),
                anarede.diffyqgv[idx].subs(anarede.qlimvar),
                anarede.diffyqgqg[idx].subs(anarede.qlimvar),
            ],
            dtype="float64",
        )

    ## Resíduo
    anarede.deltaQLIM[nger] = (
        -anarede.Y[idx][0].subs(anarede.qlimvar)
        - anarede.Y[idx][1].subs(anarede.qlimvar)
        - anarede.Y[idx][2].subs(anarede.qlimvar)
    )

    ## Armazenamento de valores das chaves
    anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]][case].append(
        array(
            [
                anarede.qlimsch[idx]["ch1"].subs(anarede.qlimvar),
                anarede.qlimsch[idx]["ch2"].subs(anarede.qlimvar),
                anarede.qlimsch[idx]["ch3"].subs(anarede.qlimvar),
                anarede.qlimsch[idx]["ch4"].subs(anarede.qlimvar),
            ]
        )
    )


def qlimnsmooth(
    idx,
    anarede,
    nger,
    case,
):
    """aplicação da função suave sigmoide para tratamento de limite de geração de potência reativa

    Args
        idx: índice da da barra geradora
        anarede:
        nger: índice de geradores
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    if case not in anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]]:
        anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]][case] = list()

    # Variáveis Simbólicas
    qg = anarede.solution["qlim_reactive_generation"][idx] / anarede.cte["BASE"]
    v = anarede.solution["voltage"][idx]
    vr = anarede.dbarDF.loc[idx, "tensao"] * 1e-3
    qgx = anarede.dbarDF.loc[idx, "potencia_reativa_maxima"] / anarede.cte["BASE"]
    qgn = anarede.dbarDF.loc[idx, "potencia_reativa_minima"] / anarede.cte["BASE"]

    ## Limites
    # Limites de Tensão
    vlimsup = vr + anarede.cte["SIGV"]
    vliminf = vr - anarede.cte["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - anarede.cte["SIGQ"]
    qliminf = qgn + anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    ch1 = 1 / (1 + npexp(-anarede.cte["SIGK"] * (qg - qlimsup)))

    # Chave Inferior de Poência Reativa
    ch2 = 1 / (1 + npexp(anarede.cte["SIGK"] * (qg - qliminf)))

    # Chave Superior de Tensão
    ch3 = 1 / (1 + npexp(anarede.cte["SIGK"] * (v - vlimsup)))

    # Chave Inferior de Tensão
    ch4 = 1 / (1 + npexp(-anarede.cte["SIGK"] * (v - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (v - vr)

    # Superior
    Ysuperior = (ch1 * ch3) * (1 - ch2 * ch4) * (qg - qgx)

    # Inferior
    Yinferior = (1 - ch1 * ch3) * (ch2 * ch4) * (qg - qgn)

    ## Derivadas
    # Expressão Geral
    anarede.qlimdiff[idx] = array(
        [
            (1 - ch1 * ch3) * (1 - ch2 * ch4),  # Derivada Parcial de Y por V
            (ch1 * ch3) * (1 - ch2 * ch4)
            + (ch2 * ch4) * (1 - ch1 * ch3),  # Derivada Parcial de Y por Qg
        ],
        dtype="float64",
    )

    ## Resíduo
    anarede.deltaQLIM[nger] = -Ynormal - Ysuperior - Yinferior

    ## Armazenamento de valores das chaves
    anarede.qlimkeys[anarede.dbarDF.loc[idx, "nome"]][case].append(
        array([ch1, ch2, ch3, ch4])
    )


def svcsQ(
    anarede,
    ncer,
    idxcer,
    idxctrl,
    value,
    case: int = 0,
):
    """_summary_

    Args:
        anarede:
    """
    ## Inicialização
    seterr(all="ignore")

    # Variáveis Simbólicas
    vk = Symbol("vk%s" % idxcer)
    vm = Symbol("vm%s" % idxcer)
    qgk = Symbol("qgk%s" % idxcer)
    r = Symbol("r%s" % idxcer)
    bmin = Symbol("bmn%s" % idxcer)
    bmax = Symbol("bmx%s" % idxcer)

    vmsch = anarede.dbarDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (r * bmin * (vk**2))
    vmmin = vmsch + (r * bmax * (vk**2))

    # Associação das variáveis
    anarede.svcvar.update(
        {
            vk: anarede.solution["voltage"][idxcer],
            vm: anarede.solution["voltage"][idxctrl],
            r: value["droop"],
            bmin: value["potencia_reativa_minima"]
            / (
                anarede.cte["BASE"]
                * (anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
            ),
            bmax: value["potencia_reativa_maxima"]
            / (
                anarede.cte["BASE"]
                * (anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
            ),
            qgk: anarede.solution["svc_generation"][ncer] / anarede.cte["BASE"],
        }
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vmmax + anarede.cte["SIGV"]
    vliminf = vmmin - anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa - Região Indutiva
    anarede.svcsch[idxcer]["ch1"] = 1 / (
        1 + spexp(-anarede.cte["SIGK"] * (vm - vlimsup))
    )

    # Chave Inferior de Poência Reativa - Região Capacitiva
    anarede.svcsch[idxcer]["ch2"] = 1 / (
        1 + spexp(anarede.cte["SIGK"] * (vm - vliminf))
    )

    ## Equações de Controle
    # Região Indutiva
    Yindutiva = (anarede.svcsch[idxcer]["ch1"]) * (-(vk**2) * bmin + qgk)

    # Região Linear
    Ylinear = (
        (1 - anarede.svcsch[idxcer]["ch1"])
        * (1 - anarede.svcsch[idxcer]["ch2"])
        * (-vmsch - (r * qgk) + vm)
    )

    # Região Capacitiva
    Ycapacitiva = (anarede.svcsch[idxcer]["ch2"]) * (-(vk**2) * bmax + qgk)

    anarede.Y[idxcer] = [
        Yindutiva,
        Ylinear,
        Ycapacitiva,
    ]

    ## Derivadas
    # Derivada Parcial de Y por Vk
    anarede.diffyvk[idxcer] = (
        anarede.Y[idxcer][0] + anarede.Y[idxcer][1] + anarede.Y[idxcer][2]
    ).diff(vk)

    # Derivada Parcial de Y por Vm
    anarede.diffyvm[idxcer] = (
        anarede.Y[idxcer][0] + anarede.Y[idxcer][1] + anarede.Y[idxcer][2]
    ).diff(vm)

    # Derivada Parcial de Y por Qgk
    anarede.diffyqgk[idxcer] = (
        anarede.Y[idxcer][0] + anarede.Y[idxcer][1] + anarede.Y[idxcer][2]
    ).diff(qgk)


def svcsQsmooth(
    idxcer,
    idxctrl,
    anarede,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por potência reativa injetada

    Args
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        anarede:
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    if case not in anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]]:
        anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("vk%s" % idxcer)
    vm = Symbol("vm%s" % idxcer)
    qgk = Symbol("qgk%s" % idxcer)
    r = Symbol("r%s" % idxcer)
    bmin = Symbol("bmn%s" % idxcer)
    bmax = Symbol("bmx%s" % idxcer)
    # Associação das variáveis
    anarede.svcvar.update(
        {
            vk: anarede.solution["voltage"][idxcer],
            vm: anarede.solution["voltage"][idxctrl],
            r: anarede.dcerDF.loc[ncer, "droop"],
            bmin: anarede.dcerDF.loc[ncer, "potencia_reativa_minima"]
            / (
                anarede.cte["BASE"]
                * (anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
            ),
            bmax: anarede.dcerDF.loc[ncer, "potencia_reativa_maxima"]
            / (
                anarede.cte["BASE"]
                * (anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3) ** 2
            ),
            qgk: anarede.solution["svc_generation"][ncer] / anarede.cte["BASE"],
        }
    )

    # Expressão Geral
    anarede.svcdiff[idxcer] = array(
        [
            anarede.diffyvk[idxcer].subs(anarede.svcvar),
            anarede.diffyvm[idxcer].subs(anarede.svcvar),
            anarede.diffyqgk[idxcer].subs(anarede.svcvar),
        ],
        dtype="float64",
    )

    ## Resíduo
    anarede.deltaSVC[ncer] = (
        -anarede.Y[idxcer][0].subs(anarede.svcvar)
        - anarede.Y[idxcer][1].subs(anarede.svcvar)
        - anarede.Y[idxcer][2].subs(anarede.svcvar)
    )

    ## Armazenamento de valores das chaves
    anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case].append(
        array(
            [
                anarede.svcsch[idxcer]["ch1"].subs(anarede.svcvar),
                anarede.svcsch[idxcer]["ch2"].subs(anarede.svcvar),
            ],
            dtype="float",
        )
    )


def svcsI(
    anarede,
    idx,
    value,
):
    """_summary_

    Args:
        anarede:
    """
    ## Inicialização
    seterr(all="ignore")

    anarede.qlimkeys[value["nome"]] = dict()
    anarede.qlimkeys[value["nome"]][0] = list()

    anarede.qlimsch[idx] = dict()
    anarede.qlimsch[idx]["ch1"] = list()
    anarede.qlimsch[idx]["ch2"] = list()
    anarede.qlimsch[idx]["ch3"] = list()
    anarede.qlimsch[idx]["ch4"] = list()

    # Variáveis Simbólicas
    qg = Symbol("qg%s" % idx)
    v = Symbol("v%s" % idx)
    vr = Symbol("vr%s" % idx)
    qgx = Symbol("qgx%s" % idx)
    qgn = Symbol("qgn%s" % idx)

    # Associação das variáveis
    anarede.qlimvar.update(
        {
            qg: anarede.solution["qlim_reactive_generation"][idx] / anarede.cte["BASE"],
            v: anarede.solution["voltage"][idx],
            vr: value["tensao"] * 1e-3,
            qgx: value["potencia_reativa_maxima"] / anarede.cte["BASE"],
            qgn: value["potencia_reativa_minima"] / anarede.cte["BASE"],
        }
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vr + anarede.cte["SIGV"]
    vliminf = vr - anarede.cte["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - anarede.cte["SIGQ"]
    qliminf = qgn + anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    anarede.qlimsch[idx]["ch1"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (qg - qlimsup)))

    # Chave Inferior de Potência Reativa
    anarede.qlimsch[idx]["ch2"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (qg - qliminf)))

    # Chave Superior de Tensão
    anarede.qlimsch[idx]["ch3"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (v - vlimsup)))

    # Chave Inferior de Tensão
    anarede.qlimsch[idx]["ch4"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (v - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (v - vr)
    )

    # Superior
    Ysuperior = (
        (anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgx)
    )

    # Inferior
    Yinferior = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgn)
    )

    anarede.Y[idx] = [Ynormal, Ysuperior, Yinferior]

    ## Derivadas
    # Derivada Parcial de Y por Qg
    anarede.diffyqg[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(qg)

    # Derivada Parcial de Y por V
    anarede.diffyv[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(v)

    if anarede.method == "EXPC":
        anarede.diffyvv[idx] = anarede.diffyv[idx].diff(v)
        anarede.diffyqgv[idx] = anarede.diffyqg[idx].diff(v)
        anarede.diffyvqg[idx] = anarede.diffyv[idx].diff(qg)
        anarede.diffyqgqg[idx] = anarede.diffyqg[idx].diff(qg)


def svcsIsmooth(
    idxcer,
    idxctrl,
    anarede,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por corrente injetada

    Args
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        anarede:
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    seterr(all="ignore")

    # Variáveis
    if case not in anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]]:
        anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("Vk")
    vm = Symbol("Vm")

    ik = Symbol("Ik")
    r = Symbol("r")

    bmin = Symbol("Bmin")
    bmax = Symbol("Bmax")

    vmsch = anarede.dbarDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (r * bmin * vk)
    vmmin = vmsch + (r * bmax * vk)

    # Associação das variáveis
    anarede.svcivarkey = {
        vk: anarede.solution["voltage"][idxcer],
        vm: anarede.solution["voltage"][idxctrl],
        r: anarede.dcerDF.loc[ncer, "droop"],
        bmin: anarede.dcerDF.loc[ncer, "potencia_reativa_minima"]
        / (anarede.cte["BASE"] * anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3),
        bmax: anarede.dcerDF.loc[ncer, "potencia_reativa_maxima"]
        / (anarede.cte["BASE"] * anarede.dbarDF.loc[idxcer, "tensao_base"] * 1e-3),
    }

    anarede.svcivar = deepcopy(anarede.svcivarkey)
    anarede.svcivar[ik] = (anarede.solution["svc_generation"][ncer]) / (
        anarede.cte["BASE"]
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vmmax + anarede.cte["SIGV"]
    vliminf = vmmin - anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa - Região Indutiva
    ch1 = 1 / (1 + spexp(-anarede.cte["SIGK"] * (vm - vlimsup)))

    # Chave Inferior de Poência Reativa - Região Capacitiva
    ch2 = 1 / (1 + spexp(anarede.cte["SIGK"] * (vm - vliminf)))

    ## Equações de Controle
    # Região Indutiva
    Yindutiva = (ch1) * (-vk * bmin + ik)

    # Região Linear
    Ylinear = (1 - ch1) * (1 - ch2) * (-vmsch - (r * ik) + vm)

    # Região Capacitiva
    Ycapacitiva = (ch2) * (-vk * bmax + ik)

    ## Derivadas
    # Derivada Parcial de Y por Vk
    anarede.diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

    # Derivada Parcial de Y por Vm
    anarede.diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

    # Derivada Parcial de Y por Ik
    anarede.diffyik = (Yindutiva + Ylinear + Ycapacitiva).diff(ik)

    # Expressão Geral
    anarede.svcdiff[idxcer] = array(
        [
            anarede.diffyvk.subs(anarede.svcivar),
            anarede.diffyvm.subs(anarede.svcivar),
            anarede.diffyik.subs(anarede.svcivar),
        ],
        dtype="float64",
    )

    ## Resíduo
    anarede.deltaSVC[ncer] = (
        -Yindutiva.subs(anarede.svcivar)
        - Ylinear.subs(anarede.svcivar)
        - Ycapacitiva.subs(anarede.svcivar)
    )

    ## Armazenamento de valores das chaves
    anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case].append(
        array(
            [
                ch1.subs(anarede.svcivarkey),
                ch2.subs(anarede.svcivarkey),
            ],
            dtype="float",
        )
    )


def svcsA(
    anarede,
    idx,
    value,
):
    """_summary_

    Args:
        anarede:
    """
    ## Inicialização
    seterr(all="ignore")

    anarede.qlimkeys[value["nome"]] = dict()
    anarede.qlimkeys[value["nome"]][0] = list()

    anarede.qlimsch[idx] = dict()
    anarede.qlimsch[idx]["ch1"] = list()
    anarede.qlimsch[idx]["ch2"] = list()
    anarede.qlimsch[idx]["ch3"] = list()
    anarede.qlimsch[idx]["ch4"] = list()

    # Variáveis Simbólicas
    qg = Symbol("qg%s" % idx)
    v = Symbol("v%s" % idx)
    vr = Symbol("vr%s" % idx)
    qgx = Symbol("qgx%s" % idx)
    qgn = Symbol("qgn%s" % idx)

    # Associação das variáveis
    anarede.qlimvar.update(
        {
            qg: anarede.solution["qlim_reactive_generation"][idx] / anarede.cte["BASE"],
            v: anarede.solution["voltage"][idx],
            vr: value["tensao"] * 1e-3,
            qgx: value["potencia_reativa_maxima"] / anarede.cte["BASE"],
            qgn: value["potencia_reativa_minima"] / anarede.cte["BASE"],
        }
    )

    ## Limites
    # Limites de Tensão
    vlimsup = vr + anarede.cte["SIGV"]
    vliminf = vr - anarede.cte["SIGV"]

    # Limites de Potência Reativa
    qlimsup = qgx - anarede.cte["SIGQ"]
    qliminf = qgn + anarede.cte["SIGV"]

    ## Chaves
    # Chave Superior de Potência Reativa
    anarede.qlimsch[idx]["ch1"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (qg - qlimsup)))

    # Chave Inferior de Potência Reativa
    anarede.qlimsch[idx]["ch2"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (qg - qliminf)))

    # Chave Superior de Tensão
    anarede.qlimsch[idx]["ch3"] = 1 / (1 + spexp(anarede.cte["SIGK"] * (v - vlimsup)))

    # Chave Inferior de Tensão
    anarede.qlimsch[idx]["ch4"] = 1 / (1 + spexp(-anarede.cte["SIGK"] * (v - vliminf)))

    ## Equações de Controle
    # Normal
    Ynormal = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (v - vr)
    )

    # Superior
    Ysuperior = (
        (anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (1 - anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgx)
    )

    # Inferior
    Yinferior = (
        (1 - anarede.qlimsch[idx]["ch1"] * anarede.qlimsch[idx]["ch3"])
        * (anarede.qlimsch[idx]["ch2"] * anarede.qlimsch[idx]["ch4"])
        * (qg - qgn)
    )

    anarede.Y[idx] = [Ynormal, Ysuperior, Yinferior]

    ## Derivadas
    # Derivada Parcial de Y por Qg
    anarede.diffyqg[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(qg)

    # Derivada Parcial de Y por V
    anarede.diffyv[idx] = (
        anarede.Y[idx][0] + anarede.Y[idx][1] + anarede.Y[idx][2]
    ).diff(v)

    if anarede.method == "EXPC":
        anarede.diffyvv[idx] = anarede.diffyv[idx].diff(v)
        anarede.diffyqgv[idx] = anarede.diffyqg[idx].diff(v)
        anarede.diffyvqg[idx] = anarede.diffyv[idx].diff(qg)
        anarede.diffyqgqg[idx] = anarede.diffyqg[idx].diff(qg)


def svcsAsmooth(
    idxcer,
    idxctrl,
    anarede,
    ncer,
    case,
):
    """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
        metodologia por ângulo de disparo

    Args
        idxcer: índice da barra do compensador estático de potência reativa
        idxctrl: índice da barra controlada pelo compensador estático de potência reativa
        anarede:
        ncer: índice do compensador estático de potência reativa
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    seterr(all="ignore")

    # Variáveis
    if case not in anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]]:
        anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case] = list()

    # Variáveis Simbólicas
    vk = Symbol("Vk")
    vm = Symbol("Vm")

    r = Symbol("r")
    alpha = Symbol("alpha")

    vmsch = anarede.dbarDF.loc[idxctrl, "tensao"] * 1e-3
    vmmax = vmsch + (
        anarede.dcerDF.loc[ncer, "droop"]
        * anarede.alphabeq.subs(alpha, pi / 2)
        * (anarede.solution["voltage"][idxcer] ** 2)
    )
    vmmin = vmsch + (
        anarede.dcerDF.loc[ncer, "droop"]
        * anarede.alphabeq.subs(alpha, pi)
        * (anarede.solution["voltage"][idxcer] ** 2)
    )

    # Associação das variáveis
    anarede.svcavar = {
        vk: anarede.solution["voltage"][idxcer],
        vm: anarede.solution["voltage"][idxctrl],
        r: anarede.dcerDF.loc[ncer, "droop"],
        alpha: anarede.solution["alpha"],
    }

    ## Limites
    # Limites de Ângulo de disparo
    alphalimsup = pi - anarede.cte["SIGA"]
    alphaliminf = pi / 2 + anarede.cte["SIGA"]

    # Limites de Tensão
    vlimsup = vmmax + anarede.cte["SIGV"]
    vliminf = vmmin - anarede.cte["SIGV"]

    ## Chaves
    # Chave Inferior de Ângulo de disparo
    ch1 = 1 / (
        1 + npexp(anarede.cte["SIGK"] * (anarede.solution["alpha"] - alphaliminf))
    )

    # Chave Superior de Ângulo de disparo
    ch2 = 1 / (
        1 + npexp(-anarede.cte["SIGK"] * (anarede.solution["alpha"] - alphalimsup))
    )

    # Chave Inferior de Tensão
    ch3 = 1 / (
        1
        + npexp(
            anarede.cte["SIGK"] * float(anarede.solution["voltage"][idxctrl] - vliminf)
        )
    )

    # Chave Superior de Tensao
    ch4 = 1 / (
        1
        + npexp(
            -anarede.cte["SIGK"] * float(anarede.solution["voltage"][idxctrl] - vlimsup)
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
    ) * (-vmsch - (r * (vk**2) * anarede.alphabeq) + vm)

    # Região Capacitiva
    Ycapacitiva = ch2 * (1 - ch4) * (alpha - pi)

    ## Derivadas
    # Derivada Parcial de Y por Vk
    anarede.diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

    # Derivada Parcial de Y por Vm
    anarede.diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

    # Derivada Parcial de Y por alpha
    anarede.diffyalpha = (Yindutiva + Ylinear + Ycapacitiva).diff(alpha)

    if anarede.solution["alpha"] <= pi / 2 + anarede.cte["SIGA"]:
        # anarede.solution['alpha'] = pi/2
        if anarede.solution["voltage"][idxctrl] <= vmmin:
            anarede.solution["voltage"][idxctrl] = deepcopy(vmsch)
            anarede.solution["alpha"] = deepcopy(anarede.solution["alpha0"])

    elif anarede.solution["alpha"] >= pi - anarede.cte["SIGA"]:
        # anarede.solution['alpha'] = pi
        if anarede.solution["voltage"][idxctrl] >= vmmax:
            anarede.solution["voltage"][idxctrl] = deepcopy(vmsch)
            anarede.solution["alpha"] = deepcopy(anarede.solution["alpha0"])

    anarede.svcavar = {
        vk: anarede.solution["voltage"][idxcer],
        vm: anarede.solution["voltage"][idxctrl],
        r: anarede.dcerDF["droop"][0],
        alpha: anarede.solution["alpha"],
    }

    anarede.solution["svc_generation"][ncer] = (
        (anarede.solution["voltage"][idxcer] ** 2)
        * anarede.alphabeq.subs(alpha, anarede.solution["alpha"])
        * anarede.cte["BASE"]
    )

    # Expressão Geral
    anarede.svcdiff[idxcer] = array(
        [
            anarede.diffyvk.subs(anarede.svcavar),
            anarede.diffyvm.subs(anarede.svcavar),
            anarede.diffyalpha.subs(anarede.svcavar),
        ],
        dtype="float64",
    )

    ## Resíduo
    anarede.deltaSVC[ncer] = (
        -Yindutiva.subs(
            {
                vm: anarede.solution["voltage"][idxctrl],
                alpha: anarede.solution["alpha"],
            }
        )
        - Ylinear.subs(anarede.svcavar)
        - Ycapacitiva.subs(
            {
                vm: anarede.solution["voltage"][idxctrl],
                alpha: anarede.solution["alpha"],
            }
        )
    )

    ## Armazenamento de valores das chaves
    anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][case].append(
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
    anarede,
    pop: int = 1,
):
    """deleta última instância salva em variável anarede.qlimskeys

    Args
        anarede:
        pop: quantidade de ações necessárias
    """
    ## Inicialização
    for _, value in anarede.dbarDF.iterrows():
        popped = 0
        if value["tipo"] != 0:
            while popped < pop:
                anarede.qlimkeys[value["nome"]].popitem()
                popped += 1


def qlimstorage(
    anarede,
):
    """armazenamento e geração de imagens referente a comutação das chaves

    Args:
        anarede:
    """
    ## Inicialização
    # Criação automática de diretório
    smoothfolder(
        anarede,
    )

    # Condição de método
    if anarede.method == "EXIC":
        # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
        for key, value in anarede.operationpoint.items():
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
        for busname, _ in anarede.qlimkeys.items():
            # Variáveis
            busidx = anarede.dbarDF.index[anarede.dbarDF["nome"] == busname].tolist()[0]

            qgx = anarede.dbarDF.loc[
                anarede.dbarDF["nome"] == busname,
                "potencia_reativa_maxima",
            ].values[0]
            qgn = anarede.dbarDF.loc[
                anarede.dbarDF["nome"] == busname,
                "potencia_reativa_minima",
            ].values[0]
            vr = (
                anarede.dbarDF.loc[anarede.dbarDF["nome"] == busname, "tensao"].values[
                    0
                ]
                * 1e-3
            )

            ch1space = linspace(
                start=(qgx - (anarede.cte["SIGQ"] * 1e1)),
                stop=(qgx + (anarede.cte["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch1value = 1 / (
                1 + npexp(-anarede.cte["SIGK"] * (ch1space - qgx + anarede.cte["SIGQ"]))
            )

            ch2space = linspace(
                start=(qgn - (anarede.cte["SIGQ"] * 1e1)),
                stop=(qgn + (anarede.cte["SIGQ"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch2value = 1 / (
                1 + npexp(anarede.cte["SIGK"] * (ch2space - qgn - anarede.cte["SIGQ"]))
            )

            chvspace = linspace(
                start=(vr - (anarede.cte["SIGV"] * 1e1)),
                stop=(vr + (anarede.cte["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch3value = 1 / (
                1 + npexp(anarede.cte["SIGK"] * (chvspace - vr - anarede.cte["SIGV"]))
            )
            ch4value = 1 / (
                1 + npexp(-anarede.cte["SIGK"] * (chvspace - vr + anarede.cte["SIGV"]))
            )

            caseitems = anarede.qlimkeys[busname][casekeymin - 1]
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
                anarede.operationpoint[casekeymin]["c"]["reactive"][busidx],
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
                anarede.operationpoint[casekeymin]["c"]["reactive"][busidx],
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
                anarede.operationpoint[casekeymin]["c"]["voltage"][busidx],
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
                anarede.operationpoint[casekeymin]["c"]["voltage"][busidx],
                smooth4,
                color="tab:red",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax4.set_title("Chave 4 - Volt mínimo", fontsize=8)

            fig.savefig(anarede.dirsmoothsys + "smooth-" + busname + ".png", dpi=400)
            plt.close(fig)


def svcstorage(
    anarede,
):
    """armazenamento e geração de imagens referente a comutação das chaves

    Args:
        anarede:
    """
    ## Inicialização
    # Criação automática de diretório
    smoothfolder(
        anarede,
    )

    # Condição de método
    if anarede.method == "EXIC":
        # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
        for key, value in anarede.operationpoint.items():
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

        anarede.pointkeymin = deepcopy(casekeymin)

        # Loop
        for busname, _ in anarede.svckeys.items():
            # Variáveis
            busidx = anarede.dbarDF.index[anarede.dbarDF["nome"] == busname].tolist()[0]
            busidxcer = anarede.dcerDF.index[
                anarede.dcerDF["barra"] == anarede.dbarDF["numero"].iloc[busidx]
            ].tolist()[0]
            ctrlbusidxcer = anarede.dbarDF.index[
                anarede.dbarDF["numero"]
                == anarede.dcerDF["barra_controlada"].iloc[busidxcer]
            ].tolist()[0]

            bmax = anarede.dcerDF["potencia_reativa_maxima"].iloc[busidxcer]
            bmin = anarede.dcerDF["potencia_reativa_minima"].iloc[busidxcer]
            vk = anarede.solution["voltage"][busidx]
            vmref = anarede.dbarDF["tensao"].iloc[ctrlbusidxcer] * 1e-3
            droop = anarede.dcerDF["droop"].iloc[busidxcer] / anarede.cte["BASE"]

            vmmax = vmref + (droop * bmin * (vk**2))
            vmmin = vmref + (droop * bmax * (vk**2))

            ch1space = linspace(
                start=(vmmax - (anarede.cte["SIGV"] * 1e1)),
                stop=(vmmax + (anarede.cte["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch1value = 1 / (
                1
                + npexp(-anarede.cte["SIGK"] * (ch1space - vmmax + anarede.cte["SIGV"]))
            )

            ch2space = linspace(
                start=(vmmin - (anarede.cte["SIGV"] * 1e1)),
                stop=(vmmin + (anarede.cte["SIGV"] * 1e1)),
                num=10000,
                endpoint=True,
            )
            ch2value = 1 / (
                1
                + npexp(anarede.cte["SIGK"] * (ch2space - vmmin - anarede.cte["SIGV"]))
            )

            caseitems = anarede.svckeys[busname][casekeymin - 1]
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
                anarede.operationpoint[casekeymin]["c"]["voltage"][ctrlbusidxcer],
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
                anarede.operationpoint[casekeymin]["c"]["voltage"][ctrlbusidxcer],
                smooth2,
                color="tab:orange",
                marker="o",
                s=50,
                alpha=0.75,
            )
            ax2.set_title("Chave 2 - V mínimo", fontsize=8)

            fig.savefig(anarede.dirsmoothsys + "smooth-" + busname + ".png", dpi=400)
            plt.close(fig)
