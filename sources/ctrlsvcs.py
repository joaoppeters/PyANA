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
    powerflow,
):
    """variável de estado adicional para o problema de fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    if "svc_generation" not in powerflow.solution:
        powerflow.solution["svc_generation"] = zeros([powerflow.ncer])

        powerflow.Y = dict()
        powerflow.svcsch = dict()
        powerflow.svckeys = dict()
        powerflow.svcdiff = dict()
        powerflow.svcvar = dict()
        powerflow.diffyqgk = dict()
        powerflow.diffyvk = dict()
        powerflow.diffyvm = dict()
        powerflow.diffyalpha = dict()

        for idx, value in powerflow.dcerDF.iterrows():
            idxcer = powerflow.dbarDF.index[
                powerflow.dbarDF["numero"] == value["barra"]
            ].tolist()[0]
            idxctrl = powerflow.dbarDF.index[
                powerflow.dbarDF["numero"] == value["barra_controlada"]
            ].tolist()[0]

            powerflow.svckeys[powerflow.dbarDF.loc[idxcer, "nome"]] = dict()
            powerflow.svckeys[powerflow.dbarDF.loc[idxcer, "nome"]][0] = list()

            powerflow.svcsch[idxcer] = dict()
            powerflow.svcsch[idxcer]["ch1"] = list()
            powerflow.svcsch[idxcer]["ch2"] = list()

            if value["controle"] == "A":
                powerflow.svcsch[idxcer]["ch3"] = list()
                powerflow.svcsch[idxcer]["ch4"] = list()
                powerflow.solution["svc_generation"][idx] = value["potencia_reativa"]
                alphavar(
                    powerflow,
                )
                svcsA(
                    powerflow,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

            elif value["controle"] == "I":
                powerflow.solution["svc_generation"][idx] = value["potencia_reativa"]
                svcsI(
                    powerflow,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

            elif value["controle"] == "P":
                powerflow.solution["svc_generation"][idx] = value["potencia_reativa"]
                svcsQ(
                    powerflow,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

    powerflow.mask = concatenate(
        (powerflow.mask, ones(powerflow.ncer, dtype=bool)), axis=0
    )


def alphavar(
    powerflow,
):
    """calculo dos parametros para metodologia alpha do compensador estatico de potencia reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.alphaxc = (powerflow.options["BASE"]) / (
        powerflow.dcerDF["potencia_reativa_maxima"][0]
    )
    powerflow.alphaxl = (
        (powerflow.options["BASE"]) / (powerflow.dcerDF["potencia_reativa_maxima"][0])
    ) / (
        1
        - (powerflow.dcerDF["potencia_reativa_minima"][0])
        / (powerflow.dcerDF["potencia_reativa_maxima"][0])
    )
    powerflow.solution["alpha"] = roots(
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
            -(2 * pi) + ((powerflow.alphaxl * pi) / powerflow.alphaxc),
        ]
    )
    powerflow.solution["alpha"] = powerflow.solution["alpha"][
        isreal(powerflow.solution["alpha"])
    ][0].real
    powerflow.solution["alpha0"] = deepcopy(powerflow.solution["alpha"])

    # Variáveis Simbólicas
    global alpha
    alpha = Symbol("alpha")
    powerflow.alphabeq = -(
        (powerflow.alphaxc / pi) * (2 * (pi - alpha) + sin(2 * alpha))
        - powerflow.alphaxl
    ) / (powerflow.alphaxc * powerflow.alphaxl)

    # Potência Reativa
    idxcer = powerflow.dbarDF.index[
        powerflow.dbarDF["numero"] == powerflow.dcerDF["barra"][0]
    ].tolist()[0]
    powerflow.solution["svc_generation"][0] = (
        powerflow.solution["voltage"][idxcer] ** 2
    ) * powerflow.alphabeq.subs(alpha, powerflow.solution["alpha"])


def svcres(
    powerflow,
    case,
):
    """cálculo de resíduos das equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    # Vetor de resíduos
    powerflow.deltaSVC = zeros([powerflow.ncer])

    # Contador
    ncer = 0

    # Loop
    for _, value in powerflow.dcerDF.iterrows():
        idxcer = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == value["barra_controlada"]
        ].tolist()[0]

        if value["controle"] == "A":
            svcsAsmooth(
                idxcer,
                idxctrl,
                powerflow,
                ncer,
                case,
            )
            powerflow.deltaQ[idxcer] = (
                deepcopy(powerflow.solution["svc_generation"][ncer])
                / powerflow.options["BASE"]
            )

        elif value["controle"] == "I":
            svcsIsmooth(
                idxcer,
                idxctrl,
                powerflow,
                ncer,
                case,
            )
            powerflow.deltaQ[idxcer] = (
                deepcopy(powerflow.solution["svc_generation"][ncer])
                * powerflow.solution["voltage"][idxcer]
                / powerflow.options["BASE"]
            )

        elif value["controle"] == "P":
            svcsQsmooth(
                idxcer,
                idxctrl,
                powerflow,
                ncer,
                case,
            )
            powerflow.deltaQ[idxcer] = (
                deepcopy(powerflow.solution["svc_generation"][ncer])
                / powerflow.options["BASE"]
            )

        powerflow.deltaQ[idxcer] -= (
            powerflow.dbarDF["demanda_reativa"][idxcer] / powerflow.options["BASE"]
        )
        # powerflow.deltaQ[idxcer] -= qcalc(
        #     powerflow,
        #     idxcer,
        # )

        # Incrementa contador
        ncer += 1

    # Resíduo de equação de controle
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaSVC)


def svcsubjac(
    powerflow,
):
    """submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
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
    powerflow.dimpresvc = deepcopy(powerflow.jacobian.shape[0])

    # Submatrizes
    px = zeros([powerflow.nbus, powerflow.ncer])
    qx = zeros([powerflow.nbus, powerflow.ncer])
    yx = zeros([powerflow.ncer, powerflow.ncer])
    yt = zeros([powerflow.ncer, powerflow.nbus])
    yv = zeros([powerflow.ncer, powerflow.nbus])

    # Contador
    ncer = 0

    # Submatrizes PXP QXP YQV YXT
    for idx, value in powerflow.dcerDF.iterrows():
        idxcer = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == value["barra_controlada"]
        ].tolist()[0]

        if value["barra"] != value["barra_controlada"]:
            # Derivada Vk
            yv[ncer, idxcer] = powerflow.svcdiff[idxcer][0]

            # Derivada Vm
            yv[ncer, idxctrl] = powerflow.svcdiff[idxcer][1]

        elif value["barra"] == value["barra_controlada"]:
            # Derivada Vk + Vm
            yv[ncer, idxcer] = (
                powerflow.svcdiff[idxcer][0] + powerflow.svcdiff[idxcer][1]
            )

        # Derivada Equação de Controle Adicional por Variável de Estado Adicional
        yx[ncer, ncer] = powerflow.svcdiff[idxcer][2]

        # Derivada Qk
        if value["controle"] == "A":
            powerflow.jacobian[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
                2
                * powerflow.solution["voltage"][idxcer]
                * float(powerflow.alphabeq.subs(alpha, powerflow.solution["alpha"]))
            )
            qx[idxcer, ncer] = -(
                powerflow.solution["voltage"][idxcer] ** 2
            ) * float(
                powerflow.alphabeq.diff(alpha).subs(alpha, powerflow.solution["alpha"])
            )

        elif value["controle"] == "I":
            powerflow.jacobian[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
                powerflow.solution["svc_generation"][ncer]
            ) / powerflow.options["BASE"]
            qx[idxcer, ncer] = -powerflow.solution["voltage"][idxcer]

        elif value["controle"] == "P":
            qx[idxcer, ncer] = -1

        # Incrementa contador
        ncer += 1

    ## Montagem Jacobiana
    # Condição
    if powerflow.controldim != 0:
        extrarow = zeros([powerflow.nger, powerflow.controldim])
        extracol = zeros([powerflow.controldim, powerflow.nger])

        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        yt[:, powerflow.maskP],
                        yv[:, powerflow.maskQ],
                        extrarow,
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        px[powerflow.maskP, :],
                        qx[powerflow.maskQ, :],
                        extracol,
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif powerflow.controldim == 0:
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        yt[:, powerflow.maskP],
                        yv[:, powerflow.maskQ],
                    ),
                    axis=1,
                ),
            ),
            axis=0,
        )
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        px[powerflow.maskP, :],
                        qx[powerflow.maskQ, :],
                        yx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def svcupdt(
    powerflow,
):
    """atualização das variáveis de estado adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Contador
    ncer = 0

    # Atualização da potência reativa gerada
    for _, value in powerflow.dcerDF.iterrows():
        if value["controle"] == "A":
            powerflow.solution["alpha"] += powerflow.statevar[
                (powerflow.dimpresvc + ncer)
            ]

        elif value["controle"] == "I":
            powerflow.solution["svc_generation"][ncer] += (
                powerflow.statevar[(powerflow.dimpresvc + ncer)]
                * powerflow.options["BASE"]
            )

        elif value["controle"] == "P":
            powerflow.solution["svc_generation"][ncer] += (
                powerflow.statevar[(powerflow.dimpresvc + ncer)]
                * powerflow.options["BASE"]
            )

        # Incrementa contador
        ncer += 1


def svcsch(
    powerflow,
):
    """atualização do valor de potência reativa especificada

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Atualização da potência reativa especificada
    ncer = 0
    for _, value in powerflow.dcerDF.iterrows():
        idxcer = powerflow.dbarDF.index[
            powerflow.dbarDF["numero"] == value["barra"]
        ].tolist()[0]
        if (powerflow.dcerDF["controle"][0] == "A") or (
            powerflow.dcerDF["controle"][0] == "P"
        ):
            powerflow.qsch[idxcer] += (
                powerflow.solution["svc_generation"][ncer] / powerflow.options["BASE"]
            )

        elif powerflow.dcerDF["controle"][0] == "I":
            powerflow.qsch[idxcer] += (
                powerflow.solution["svc_generation"][ncer]
                * powerflow.solution["voltage"][idxcer]
            ) / powerflow.options["BASE"]

        # Incrementa contador
        ncer += 1


def svccorr(
    powerflow,
    case,
):
    """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: etapa do fluxo de potência continuado analisada
    """

    ## Inicialização
    # Variável
    powerflow.solution["svc_generation"] = deepcopy(
        powerflow.operationpoint[case]["p"]["svc_generation"]
    )


def svcheur(
    powerflow,
):
    """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
    if (
        (not powerflow.solution["pmc"])
        and (powerflow.solution["varstep"] == "lambda")
        and (
            (powerflow.options["LMBD"] * (5e-1 ** powerflow.solution["ndiv"]))
            <= powerflow.options["icmn"]
        )
    ):
        powerflow.nbusbifurcation = True


def svccpf(
    powerflow,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.solution["svc_generation"] = deepcopy(
        powerflow.solution["svc_generation"]
    )


def svcsolcpf(
    powerflow,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: etapa do fluxo de potência continuado analisada
    """

    ## Inicialização
    # Condição
    precase = case - 1
    if case == 1:
        powerflow.solution["svc_generation"] = deepcopy(
            powerflow.operationpoint[precase]["svc_generation"]
        )

    elif case > 1:
        powerflow.solution["svc_generation"] = deepcopy(
            powerflow.operationpoint[precase]["p"]["svc_generation"]
        )


def svcsubhess(
    powerflow,
):
    """submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
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
    powerflow,
):
    """submatrizes da matriz jacobiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
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
