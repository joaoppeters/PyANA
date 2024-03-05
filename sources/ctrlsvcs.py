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


def svcsol(
    powerflow,
):
    """variável de estado adicional para o problema de fluxo de potência

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis
    if "svc_reactive_generation" not in powerflow.solution:
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
            idxcer = powerflow.dbarraDF.index[
                powerflow.dbarraDF["numero"] == value["barra"]
            ].tolist()[0]
            idxctrl = powerflow.dbarraDF.index[
                powerflow.dbarraDF["numero"] == value["barra_controlada"]
            ].tolist()[0]

            powerflow.svckeys[value["nome"]] = dict()
            powerflow.svckeys[value["nome"]][0] = list()

            powerflow.svcsch[idxcer] = dict()
            powerflow.svcsch[idxcer]["ch1"] = list()
            powerflow.svcsch[idxcer]["ch2"] = list()

            if value["controle"] == "A":
                powerflow.svcsch[idxcer]["ch3"] = list()
                powerflow.svcsch[idxcer]["ch4"] = list()
                powerflow.solution["svc_reactive_generation"] = value[
                    "potencia_reativa"
                ].to_numpy()
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
                powerflow.solution["svc_current_injection"] = value[
                    "potencia_reativa"
                ].to_numpy()
                svcsI(
                    powerflow,
                    idx,
                    idxcer,
                    idxctrl,
                    value,
                )

            elif value["controle"] == "P":
                powerflow.solution["svc_reactive_generation"] = value[
                    "potencia_reativa"
                ].to_numpy()
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
    powerflow.nbusalphaxc = (powerflow.options["BASE"]) / (
        powerflow.dcerDF["potencia_reativa_maxima"][0]
    )
    powerflow.nbusalphaxl = (
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
            -(2 * pi) + ((powerflow.nbusalphaxl * pi) / powerflow.nbusalphaxc),
        ]
    )
    powerflow.solution["alpha"] = powerflow.solution["alpha"][
        isreal(powerflow.solution["alpha"])
    ][0].real
    powerflow.solution["alpha0"] = deepcopy(powerflow.solution["alpha"])

    # Variáveis Simbólicas
    global alpha
    alpha = Symbol("alpha")
    powerflow.nbusalphabeq = -(
        (powerflow.nbusalphaxc / pi) * (2 * (pi - alpha) + sin(2 * alpha))
        - powerflow.nbusalphaxl
    ) / (powerflow.nbusalphaxc * powerflow.nbusalphaxl)

    # Potência Reativa
    idxcer = powerflow.dbarraDF.index[
        powerflow.dbarraDF["numero"] == powerflow.dcerDF["barra"][0]
    ].tolist()[0]
    powerflow.solution["svc_reactive_generation"][0] = (
        powerflow.solution["voltage"][idxcer] ** 2
    ) * powerflow.nbusalphabeq.subs(alpha, powerflow.solution["alpha"])


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
    powerflow.nbusdeltaSVC = zeros([powerflow.ncer])

    # Contador
    ncer = 0

    # Loop
    for _, value in powerflow.dcerDF.iterrows():
        idxcer = powerflow.dbarraDF.index[
            powerflow.dbarraDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = powerflow.dbarraDF.index[
            powerflow.dbarraDF["numero"] == value["barra_controlada"]
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
                deepcopy(powerflow.solution["svc_reactive_generation"][ncer])
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
                deepcopy(powerflow.solution["svc_current_injection"][ncer])
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
                deepcopy(powerflow.solution["svc_reactive_generation"][ncer])
                / powerflow.options["BASE"]
            )

        powerflow.deltaQ[idxcer] -= (
            powerflow.dbarraDF["demanda_reativa"][idxcer] / powerflow.options["BASE"]
        )
        powerflow.deltaQ[idxcer] -= qcalc(
            powerflow,
            idxcer,
        )

        # Incrementa contador
        ncer += 1

    # Resíduo de equação de controle
    powerflow.deltaY = append(powerflow.deltaY, powerflow.nbusdeltaSVC)


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
    powerflow.nbusdimpresvc = deepcopy(powerflow.jacobian.shape[0])

    # Submatrizes
    powerflow.nbuspx = zeros([powerflow.nbus, powerflow.ncer])
    powerflow.nbusqx = zeros([powerflow.nbus, powerflow.ncer])
    powerflow.nbusyx = zeros([powerflow.ncer, powerflow.ncer])
    powerflow.nbusyt = zeros([powerflow.ncer, powerflow.nbus])
    powerflow.nbusyv = zeros([powerflow.ncer, powerflow.nbus])

    # Contador
    ncer = 0

    # Submatrizes PXP QXP YQV YXT
    for idx, value in powerflow.dcerDF.iterrows():
        idxcer = powerflow.dbarraDF.index[
            powerflow.dbarraDF["numero"] == value["barra"]
        ].tolist()[0]
        idxctrl = powerflow.dbarraDF.index[
            powerflow.dbarraDF["numero"] == value["barra_controlada"]
        ].tolist()[0]

        if value["barra"] != value["barra_controlada"]:
            # Derivada Vk
            powerflow.nbusyv[ncer, idxcer] = powerflow.nbusdiffsvc[idxcer][0]

            # Derivada Vm
            powerflow.nbusyv[ncer, idxctrl] = powerflow.nbusdiffsvc[idxcer][1]

        elif value["barra"] == value["barra_controlada"]:
            # Derivada Vk + Vm
            powerflow.nbusyv[ncer, idxcer] = (
                powerflow.nbusdiffsvc[idxcer][0] + powerflow.nbusdiffsvc[idxcer][1]
            )

        # Derivada Equação de Controle Adicional por Variável de Estado Adicional
        powerflow.nbusyx[ncer, ncer] = powerflow.nbusdiffsvc[idxcer][2]

        # Derivada Qk
        if value["controle"] == "A":
            powerflow.jacobian[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
                2
                * powerflow.solution["voltage"][idxcer]
                * float(powerflow.nbusalphabeq.subs(alpha, powerflow.solution["alpha"]))
            )
            powerflow.nbusqx[idxcer, ncer] = -(
                powerflow.solution["voltage"][idxcer] ** 2
            ) * float(
                powerflow.nbusalphabeq.diff(alpha).subs(
                    alpha, powerflow.solution["alpha"]
                )
            )

        elif value["controle"] == "I":
            powerflow.jacobian[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
                powerflow.solution["svc_current_injection"][ncer]
            ) / powerflow.options["BASE"]
            powerflow.nbusqx[idxcer, ncer] = -powerflow.solution["voltage"][idxcer]

        elif value["controle"] == "P":
            powerflow.nbusqx[idxcer, ncer] = -1

        # Incrementa contador
        ncer += 1

    ## Montagem Jacobiana
    # Condição
    if powerflow.nbuscontroldim != 0:
        powerflow.nbusextrarow = zeros([powerflow.nbusnger, powerflow.nbuscontroldim])
        powerflow.nbusextracol = zeros([powerflow.nbuscontroldim, powerflow.nbusnger])

        ytv = csc_matrix(
            concatenate(
                (powerflow.nbusyt, powerflow.nbusyv, powerflow.nbusextrarow),
                axis=1,
            )
        )
        pqyx = csc_matrix(
            concatenate(
                (
                    powerflow.nbuspx,
                    powerflow.nbusqx,
                    powerflow.nbusextracol,
                    powerflow.nbusyx,
                ),
                axis=0,
            )
        )

    elif powerflow.nbuscontroldim == 0:
        ytv = csc_matrix(concatenate((powerflow.nbusyt, powerflow.nbusyv), axis=1))
        pqyx = csc_matrix(
            concatenate((powerflow.nbuspx, powerflow.nbusqx, powerflow.nbusyx), axis=0)
        )

    powerflow.jacobian = vstack([powerflow.jacobian, ytv], format="csc")
    powerflow.jacobian = hstack([powerflow.jacobian, pqyx], format="csc")


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
                (powerflow.nbusdimpresvc + ncer)
            ]

        elif value["controle"] == "I":
            powerflow.solution["svc_current_injection"][ncer] += (
                powerflow.statevar[(powerflow.nbusdimpresvc + ncer)]
                * powerflow.options["BASE"]
            )

        elif value["controle"] == "P":
            powerflow.solution["svc_reactive_generation"][ncer] += (
                powerflow.statevar[(powerflow.nbusdimpresvc + ncer)]
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
        idxcer = powerflow.dbarraDF.index[
            powerflow.dbarraDF["numero"] == value["barra"]
        ].tolist()[0]
        if (powerflow.dcerDF["controle"][0] == "A") or (
            powerflow.dcerDF["controle"][0] == "P"
        ):
            powerflow.qsch[idxcer] += (
                powerflow.solution["svc_reactive_generation"][ncer]
                / powerflow.options["BASE"]
            )

        elif powerflow.dcerDF["controle"][0] == "I":
            powerflow.qsch[idxcer] += (
                powerflow.solution["svc_current_injection"][ncer]
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
    powerflow.solution["svc_reactive_generation"] = deepcopy(
        powerflow.point[case]["p"]["svc_reactive_generation"]
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
            (powerflow.options["LMBD"] * (5e-1 ** powerflow.solution["div"]))
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
    powerflow.solution["svc_reactive_generation"] = deepcopy(
        powerflow.solution["svc_reactive_generation"]
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
        powerflow.solution["svc_reactive_generation"] = deepcopy(
            powerflow.point[precase]["svc_reactive_generation"]
        )

    elif case > 1:
        powerflow.solution["svc_reactive_generation"] = deepcopy(
            powerflow.point[precase]["p"]["svc_reactive_generation"]
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
