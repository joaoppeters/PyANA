# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, array, ones, zeros
from numpy.linalg import norm

from ctrlfreq import *
from ctrlqlim import *
from ctrlqlims import *
from ctrlqlimn import *
from ctrlsvcs import *


def control(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    if powerflow.control:
        powerflow.maskctrlcount = 0
        print("\033[96mOpções de controle escolhidas: ", end="")
        for k in powerflow.control:
            if (k == "SVCs") and (not powerflow.codes["DCER"]):
                continue
            if k == "FREQ":
                powerflow.freqjcount = 0
            else:
                print(f"{k}", end=" ")
        print("\033[0m")

    else:
        powerflow.control = dict()
        print("\033[96mNenhuma opção de controle foi escolhida.\033[0m")


def controlsol(
    powerflow,
):
    """altera variável de armazenamento de solução do fluxo de potência em função do controle ativo

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    if not hasattr(powerflow, "ctrlcount"):
        powerflow.controlcount = 0
        powerflow.totaldevicescontrol = 0
        powerflow.controlorder = dict()

    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "CREM"
            pass
        # controle secundário de tensão
        elif value == "CST":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "CST"
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "CTAP"
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "CTAPd"
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "FREQ"
            freqsol(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            powerflow.controlcount += 1
            powerflow.totaldevicescontrol += powerflow.nger
            powerflow.controlorder[powerflow.controlcount] = "QLIM"
            qlimsol(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            powerflow.controlcount += 1
            powerflow.totaldevicescontrol += powerflow.nger
            powerflow.controlorder[powerflow.controlcount] = "QLIMs"
            qlimssol(
                powerflow,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            powerflow.controlcount += 1
            powerflow.totaldevicescontrol += powerflow.nger
            powerflow.controlorder[powerflow.controlcount] = "QLIMn"
            qlimnsol(
                powerflow,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            powerflow.controlcount += 1
            powerflow.totaldevicescontrol += powerflow.ncer
            powerflow.controlorder[powerflow.controlcount] = "SVCs"
            svcsol(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            powerflow.controlcount += 1
            powerflow.controlorder[powerflow.controlcount] = "VCTRL"
            pass

    powerflow.Tval = sum(powerflow.maskP)
    powerflow.Vval = sum(powerflow.maskQ)

    if not powerflow.controlcount:
        powerflow.controldim = 0


def controlsch(
    powerflow,
):
    """adiciona variáveis especificadas de controles ativos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            freqsch(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsch(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssch(
                powerflow,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsch(
                powerflow,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsch(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controlres(
    powerflow,
    case: int = 0,
):
    """adiciona resíduos de equações de controle de controles ativos

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: caso analisado do fluxo de potência continuado (prev + corr)
            valor padrão igual a zero -> Newton-Raphson
    """

    ## Inicialização
    # Variável
    powerflow.deltaY = array([])

    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            freqres(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimres(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimsres(
                powerflow,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnres(
                powerflow,
                case,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcres(
                powerflow,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    if powerflow.deltaY.size == 0:
        powerflow.deltaY = array([])


def controljac(
    powerflow,
):
    """submatrizes referentes aos controles ativos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.truedim = deepcopy(powerflow.jacobian.shape[0])

    # Loop
    for value in powerflow.control:
        # Dimensão
        powerflow.controldim = powerflow.jacobian.shape[0] - powerflow.truedim

        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            freqsubjac(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsubjac(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssubjac(
                powerflow,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsubjac(
                powerflow,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsubjac(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    # Dimensão
    powerflow.controldim = powerflow.jacobian.shape[0] - powerflow.truedim

    # Atualização da Máscara da Jacobiana
    if (powerflow.maskctrlcount == 0) and (powerflow.solution["method"] != "CANI"):
        powerflow.maskctrlcount += 1

    elif (powerflow.maskctrlcount == 0) and (powerflow.solution["method"] == "CANI"):
        powerflow.maskctrlcount += 1


def controlupdt(
    powerflow,
):
    """atualização das variáveis de estado adicionais por controle ativo

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            frequpdt(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimupdt(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimsupdt(
                powerflow,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnupdt(
                powerflow,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcupdt(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controlcorrsol(
    case,
    powerflow,
):
    """atualização das variáveis de controle para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            freqcorr(
                powerflow,
                case,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimcorr(
                powerflow,
                case,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimscorr(
                powerflow,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimncorr(
                powerflow,
                case,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svccorr(
                powerflow,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controlheuristics(
    powerflow,
):
    """aplicação de heurísticas das variáveis de controle para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.controlheur = False
    if not hasattr(powerflow, "bifurcation"):
        powerflow.bifurcation = False

    # Loop
    for value in powerflow.control:
        if (powerflow.controlheur) or (
            (powerflow.bifurcation) and (not powerflow.options["FULL"])
        ):
            break

        elif (not powerflow.controlheur) and (not powerflow.solution["pmc"]):
            # controle remoto de tensão
            if value == "CREM":
                pass
            # controle secundário de tensão
            elif value == "CST":
                pass
            # controle de tap variável de transformador
            elif value == "CTAP":
                pass
            # controle de ângulo de transformador defasador
            elif value == "CTAPd":
                pass
            # controle de regulação primária de frequência
            elif value == "FREQ":
                pass
            # controle de limite de geração de potência reativa
            elif value == "QLIM":
                qlimheur(
                    powerflow,
                )
            # controle suave de limite de geração de potência reativa
            elif value == "QLIMs":
                qlimsheur(
                    powerflow,
                )
            # controle suave de limite de geração de potência reativa
            elif value == "QLIMn":
                qlimnheur(
                    powerflow,
                )
            # controle de compensadores estáticos de potência reativa
            elif value == "SVCs":
                svcheur(
                    powerflow,
                )
            # controle de magnitude de tensão de barramentos
            elif value == "VCTRL":
                pass


def controlpop(
    powerflow,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas

    Parâmetros
        powerflow: self do arquivo powerflow.py
        pop: quantidade de ações necessárias
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            pass
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            pass
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimspop(powerflow, pop=pop)
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnpop(powerflow, pop=pop)
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            pass
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controlcpf(
    powerflow,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            pass
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            pass
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            pass
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            pass
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svccpf(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controlsolcpf(
    powerflow,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
        case: etapa do fluxo de potência continuado analisada
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            pass
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            pass
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssolcpf(
                powerflow,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            pass
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsolcpf(
                powerflow,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def controldelta(
    powerflow,
):
    """checagem da variação dos resíduos durante método iterativo de newton-raphson

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    boollist = list()
    ctrl = 0

    # Loop
    for value in powerflow.control:
        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["TEPA"]
            )
            ctrl += powerflow.nger
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["TEPR"]
            )
            ctrl += powerflow.nger
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["ASTP"]
            )
            ctrl += powerflow.nger
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["QLST"]
            )
            ctrl += powerflow.nger
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["QLST"]
            )
            ctrl += powerflow.nger
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.nger])
                > powerflow.options["QLST"]
            )
            ctrl += powerflow.nger
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            boollist.append(
                norm(powerflow.deltaY[ctrl : ctrl + powerflow.ncer])
                > powerflow.options["QLST"]
            )
            ctrl += powerflow.ncer
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    return any(boollist)


def controlhess(
    powerflow,
):
    """submatrizes referentes aos controles ativos

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Loop
    for value in powerflow.control:
        # Dimensão
        powerflow.controldim = powerflow.hessian.shape[0] - powerflow.truedim

        # controle remoto de tensão
        if value == "CREM":
            pass
        # controle secundário de tensão
        elif value == "CST":
            pass
        # controle de tap variável de transformador
        elif value == "CTAP":
            pass
        # controle de ângulo de transformador defasador
        elif value == "CTAPd":
            pass
        # controle de regulação primária de frequência
        elif value == "FREQ":
            freqsubhess(
                powerflow,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsubhess(
                powerflow,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssubhess(
                powerflow,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsubhess(
                powerflow,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsubhess(
                powerflow,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    # Dimensão
    powerflow.controldim = powerflow.hessian.shape[0] - powerflow.truedim
