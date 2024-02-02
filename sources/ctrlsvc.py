# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, isreal, pi, roots, zeros
from scipy.sparse import csc_matrix, hstack, vstack
from sympy import Symbol
from sympy.functions import sin

from calc import qcalc
from smooth import svcalphasmooth, svccurrentsmooth, svcreactivesmooth


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
        if powerflow.dcerDF["controle"][0] == "A":
            powerflow.solution["svc_reactive_generation"] = powerflow.dcerDF[
                "potencia_reativa"
            ].to_numpy()
            alphavar(
                powerflow,
            )

        elif powerflow.dcerDF["controle"][0] == "I":
            powerflow.solution["svc_current_injection"] = powerflow.dcerDF[
                "potencia_reativa"
            ].to_numpy()

        elif powerflow.dcerDF["controle"][0] == "P":
            powerflow.solution["svc_reactive_generation"] = powerflow.dcerDF[
                "potencia_reativa"
            ].to_numpy()


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
    powerflow.nbusdeltaSVC = zeros([powerflow.nbusncer])

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
            svcalphasmooth(
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
            svccurrentsmooth(
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
            svcreactivesmooth(
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
    powerflow.nbusdimpresvc = deepcopy(powerflow.jacob.shape[0])

    # Submatrizes
    powerflow.nbuspx = zeros([powerflow.nbus, powerflow.nbusncer])
    powerflow.nbusqx = zeros([powerflow.nbus, powerflow.nbusncer])
    powerflow.nbusyx = zeros([powerflow.nbusncer, powerflow.nbusncer])
    powerflow.nbusyt = zeros([powerflow.nbusncer, powerflow.nbus])
    powerflow.nbusyv = zeros([powerflow.nbusncer, powerflow.nbus])

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
            powerflow.jacob[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
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
            powerflow.jacob[powerflow.nbus + idxcer, powerflow.nbus + idxcer] -= (
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

    powerflow.jacob = vstack([powerflow.jacob, ytv], format="csc")
    powerflow.jacob = hstack([powerflow.jacob, pqyx], format="csc")


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
            powerflow.pqsch["potencia_reativa_especificada"][idxcer] += (
                powerflow.solution["svc_reactive_generation"][ncer]
                / powerflow.options["BASE"]
            )

        elif powerflow.dcerDF["controle"][0] == "I":
            powerflow.pqsch["potencia_reativa_especificada"][idxcer] += (
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
        (not powerflow.cpfsolution["pmc"])
        and (powerflow.cpfsolution["varstep"] == "lambda")
        and (
            (powerflow.options["LMBD"] * (5e-1 ** powerflow.cpfsolution["div"]))
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
    powerflow.cpfsolution["svc_reactive_generation"] = deepcopy(
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