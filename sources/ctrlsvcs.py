# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, isreal, ones, pi, roots, zeros
from scipy.sparse import csc_matrix, hstack, vstack
from sympy import Symbol
from sympy.functions import sin

from calc import qcalc
from smooth import svcsA, svcsAsmooth, svcsI, svcsIsmooth, svcsQ, svcsQsmooth


def svcssol(
    anarede,
):
    """variável de estado adicional para o problema de fluxo de potência

    Args
        anarede:
    """
    ## Inicialização
    # Variáveis
    if "svc_generation" not in anarede.solution:
        anarede.solution["svc_generation"] = zeros([anarede.ncer])

        anarede.Y = dict()
        anarede.svcsch = dict()
        anarede.svckeys = dict()
        anarede.svcdiff = dict()
        anarede.svcvar = dict()
        anarede.diffyqgk = dict()
        anarede.diffyvk = dict()
        anarede.diffyvm = dict()
        anarede.diffyalpha = dict()

        for idx, value in anarede.dcerDF.iterrows():
            idxcer = anarede.dbarDF.index[
                anarede.dbarDF["numero"] == value["barra"]
            ].tolist()[0]
            idxctrl = anarede.dbarDF.index[
                anarede.dbarDF["numero"] == value["barra_controlada"]
            ].tolist()[0]

            anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]] = dict()
            anarede.svckeys[anarede.dbarDF.loc[idxcer, "nome"]][0] = list()

            anarede.svcsch[idxcer] = dict()
            anarede.svcsch[idxcer]["ch1"] = list()
            anarede.svcsch[idxcer]["ch2"] = list()

            if value["controle"] == "A":
                anarede.svcsch[idxcer]["ch3"] = list()
                anarede.svcsch[idxcer]["ch4"] = list()
                anarede.solution["svc_generation"][idx] = value["potencia_reativa"]
                alphavar(
                    anarede,
                )
                svcsA(
                    anarede,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

            elif value["controle"] == "I":
                anarede.solution["svc_generation"][idx] = value["potencia_reativa"]
                svcsI(
                    anarede,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

            elif value["controle"] == "P":
                anarede.solution["svc_generation"][idx] = value["potencia_reativa"]
                svcsQ(
                    anarede,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

    anarede.mask = concatenate((anarede.mask, ones(anarede.ncer, dtype=bool)), axis=0)


def alphavar(
    anarede,
):
    """calculo dos Args para metodologia alpha do compensador estatico de potencia reativa

    Args
        anarede:
    """
    ## Inicialização
    anarede.alphaxc = (anarede.cte["BASE"]) / (
        anarede.dcerDF["potencia_reativa_maxima"][0]
    )
    anarede.alphaxl = (
        (anarede.cte["BASE"]) / (anarede.dcerDF["potencia_reativa_maxima"][0])
    ) / (
        1
        - (anarede.dcerDF["potencia_reativa_minima"][0])
        / (anarede.dcerDF["potencia_reativa_maxima"][0])
    )
    anarede.solution["alpha"] = roots(
        [
            (8 / 1856156927625),
            0,
            (-4 / 10854718875),
            0,
            (16 / 638512875),
            0,
            (-8 / 6081075),
            0,
            (8 / 155925),
            0,
            (-4 / 2835),
            0,
            (8 / 315),
            0,
            (-4 / 15),
            0,
            (4 / 3),
            0,
            0,
            -(2 * pi) + ((anarede.alphaxl * pi) / anarede.alphaxc),
        ]
    )
    anarede.solution["alpha"] = anarede.solution["alpha"][
        isreal(anarede.solution["alpha"])
    ][0].real
    anarede.solution["alpha0"] = deepcopy(anarede.solution["alpha"])

    # Variáveis Simbólicas
    global alpha
    alpha = Symbol("alpha")
    anarede.alphabeq = -(
        (anarede.alphaxc / pi) * (2 * (pi - alpha) + sin(2 * alpha)) - anarede.alphaxl
    ) / (anarede.alphaxc * anarede.alphaxl)

    # Potência Reativa
    idxcer = anarede.dbarDF.index[
        anarede.dbarDF["numero"] == anarede.dcerDF["barra"][0]
    ].tolist()[0]
    anarede.solution["svc_generation"][0] = (
        anarede.solution["voltage"][idxcer] ** 2
    ) * anarede.alphabeq.subs(alpha, anarede.solution["alpha"])


def svcres(
    anarede,
    case,
):
    """cálculo de resíduos das equações de controle adicionais

    Args
        anarede:
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    # Vetor de resíduos
    anarede.deltaSVC = zeros([anarede.ncer])

    # Contador
    ncer = 0

    # Loop
    for _, value in anarede.dcerDF.iterrows():
        idxcer = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == value["barra_controlada"]
        ].tolist()[0]

        if value["controle"] == "A":
            svcsAsmooth(
                idxcer,
                idxctrl,
                anarede,
                ncer,
                case,
            )
            anarede.deltaQ[idxcer] = (
                deepcopy(anarede.solution["svc_generation"][ncer]) / anarede.cte["BASE"]
            )

        elif value["controle"] == "I":
            svcsIsmooth(
                idxcer,
                idxctrl,
                anarede,
                ncer,
                case,
            )
            anarede.deltaQ[idxcer] = (
                deepcopy(anarede.solution["svc_generation"][ncer])
                * anarede.solution["voltage"][idxcer]
                / anarede.cte["BASE"]
            )

        elif value["controle"] == "P":
            svcsQsmooth(
                idxcer,
                idxctrl,
                anarede,
                ncer,
                case,
            )
            anarede.deltaQ[idxcer] = (
                deepcopy(anarede.solution["svc_generation"][ncer]) / anarede.cte["BASE"]
            )

        anarede.deltaQ[idxcer] -= (
            anarede.dbarDF["demanda_reativa"][idxcer] / anarede.cte["BASE"]
        )
        # anarede.deltaQ[idxcer] -= qcalc(
        #     anarede,
        #     idxcer,
        # )

        # Incrementa contador
        ncer += 1

    # Resíduo de equação de controle
    anarede.deltaY = append(anarede.deltaY, anarede.deltaSVC)


def svcsubjac(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
    """
    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    # Dimensão da matriz Jacobiana
    anarede.dimpresvc = deepcopy(anarede.jacobian.shape[0])

    # Submatrizes
    px = zeros([anarede.nbus, anarede.ncer])
    qx = zeros([anarede.nbus, anarede.ncer])
    yx = zeros([anarede.ncer, anarede.ncer])
    yt = zeros([anarede.ncer, anarede.nbus])
    yv = zeros([anarede.ncer, anarede.nbus])

    # Contador
    ncer = 0

    # Submatrizes PXP QXP YQV YXT
    for idx, value in anarede.dcerDF.iterrows():
        idxcer = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == value["barra_controlada"]
        ].tolist()[0]

        if value["barra"] != value["barra_controlada"]:
            # Derivada Vk
            yv[ncer, idxcer] = anarede.svcdiff[idxcer][0]

            # Derivada Vm
            yv[ncer, idxctrl] = anarede.svcdiff[idxcer][1]

        elif value["barra"] == value["barra_controlada"]:
            # Derivada Vk + Vm
            yv[ncer, idxcer] = anarede.svcdiff[idxcer][0] + anarede.svcdiff[idxcer][1]

        # Derivada Equação de Controle Adicional por Variável de Estado Adicional
        yx[ncer, ncer] = anarede.svcdiff[idxcer][2]

        # Derivada Qk
        if value["controle"] == "A":
            anarede.jacobian[anarede.nbus + idxcer, anarede.nbus + idxcer] -= (
                2
                * anarede.solution["voltage"][idxcer]
                * float(anarede.alphabeq.subs(alpha, anarede.solution["alpha"]))
            )
            qx[idxcer, ncer] = -(anarede.solution["voltage"][idxcer] ** 2) * float(
                anarede.alphabeq.diff(alpha).subs(alpha, anarede.solution["alpha"])
            )

        elif value["controle"] == "I":
            anarede.jacobian[anarede.nbus + idxcer, anarede.nbus + idxcer] -= (
                anarede.solution["svc_generation"][ncer]
            ) / anarede.cte["BASE"]
            qx[idxcer, ncer] = -anarede.solution["voltage"][idxcer]

        elif value["controle"] == "P":
            qx[idxcer, ncer] = -1

        # Incrementa contador
        ncer += 1

    ## Montagem Jacobiana
    # Condição
    if anarede.controldim != 0:
        extrarow = zeros([anarede.nger, anarede.controldim])
        extracol = zeros([anarede.controldim, anarede.nger])

        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        yt[:, anarede.maskP],
                        yv[:, anarede.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        px[anarede.maskP, :],
                        qx[anarede.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif anarede.controldim == 0:
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        yt[:, anarede.maskP],
                        yv[:, anarede.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        px[anarede.maskP, :],
                        qx[anarede.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def svcupdt(
    anarede,
):
    """atualização das variáveis de estado adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Contador
    ncer = 0

    # Atualização da potência reativa gerada
    for _, value in anarede.dcerDF.iterrows():
        if value["controle"] == "A":
            anarede.solution["alpha"] += anarede.statevar[(anarede.dimpresvc + ncer)]

        elif value["controle"] == "I":
            anarede.solution["svc_generation"][ncer] += (
                anarede.statevar[(anarede.dimpresvc + ncer)] * anarede.cte["BASE"]
            )

        elif value["controle"] == "P":
            anarede.solution["svc_generation"][ncer] += (
                anarede.statevar[(anarede.dimpresvc + ncer)] * anarede.cte["BASE"]
            )

        # Incrementa contador
        ncer += 1


def svcsch(
    anarede,
):
    """atualização do valor de potência reativa especificada

    Args
        anarede:
    """
    ## Inicialização
    # Atualização da potência reativa especificada
    ncer = 0
    for _, value in anarede.dcerDF.iterrows():
        idxcer = anarede.dbarDF.index[
            anarede.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        if (anarede.dcerDF["controle"][0] == "A") or (
            anarede.dcerDF["controle"][0] == "P"
        ):
            anarede.qsch[idxcer] += (
                anarede.solution["svc_generation"][ncer] / anarede.cte["BASE"]
            )

        elif anarede.dcerDF["controle"][0] == "I":
            anarede.qsch[idxcer] += (
                anarede.solution["svc_generation"][ncer]
                * anarede.solution["voltage"][idxcer]
            ) / anarede.cte["BASE"]

        # Incrementa contador
        ncer += 1


def svccorr(
    anarede,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
        case: etapa do fluxo de potência continuado analisada
    """
    ## Inicialização
    # Variável
    anarede.solution["svc_generation"] = deepcopy(
        anarede.operationpoint[case]["p"]["svc_generation"]
    )


def svcheur(
    anarede,
):
    """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
    if (
        (not anarede.solution["pmc"])
        and (anarede.solution["varstep"] == "lambda")
        and (
            (anarede.cte["LMBD"] * (5e-1 ** anarede.solution["ndiv"]))
            <= anarede.cte["icmn"]
        )
    ):
        anarede.nbusbifurcation = True


def svccpf(
    anarede,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    anarede.solution["svc_generation"] = deepcopy(anarede.solution["svc_generation"])


def svcsolcpf(
    anarede,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
        case: etapa do fluxo de potência continuado analisada
    """
    ## Inicialização
    # Condição
    precase = case - 1
    if case == 1:
        anarede.solution["svc_generation"] = deepcopy(
            anarede.operationpoint[precase]["svc_generation"]
        )

    elif case > 1:
        anarede.solution["svc_generation"] = deepcopy(
            anarede.operationpoint[precase]["p"]["svc_generation"]
        )


def svcsubhess(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
    """
    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    pass


def svcsubjacsym(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
    """
    ## Inicialização
    #
    # jacobiana:
    #
    #   H     N   px
    #   M     L   qx
    #  yt    yv   yx
    #

    pass
