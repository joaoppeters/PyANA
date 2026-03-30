# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, array
from numpy.linalg import norm

from ctrlfreq import *
from ctrlqlim import *
from ctrlqlims import *
from ctrlqlimn import *
from ctrlsvcs import *


def ctrlsol(
    anarede,
):
    """altera variável de armazenamento de solução do fluxo de potência em função do controle ativo

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    if not hasattr(anarede, "ctrlcount"):
        anarede.ctrlcount = 0
        anarede.totaldevicesctrl = 0
        anarede.ctrlorder = dict()

    # controle remoto de tensão
    if anarede.ctrl["CREM"]:
        anarede.ctrlcount += 1
        anarede.ctrlorder[anarede.ctrlcount] = "CREM"
        pass
    # # controle secundário de tensão
    # if anarede.ctrl['CST']:
    #     anarede.ctrlcount += 1
    #     anarede.ctrlorder[anarede.ctrlcount] = "CST"
    #     pass
    # controle de tap variável de transformador
    if anarede.ctrl["CTAP"]:
        anarede.ctrlcount += 1
        anarede.ctrlorder[anarede.ctrlcount] = "CTAP"
        pass
    # controle de ângulo de transformador defasador
    if anarede.ctrl["CPHS"]:
        anarede.ctrlcount += 1
        anarede.ctrlorder[anarede.ctrlcount] = "CPHS"
        pass
    # controle de regulação primária de frequência
    if anarede.ctrl["FREQ"]:
        anarede.ctrlcount += 1
        anarede.ctrlorder[anarede.ctrlcount] = "FREQ"
        freqsol(
            anarede,
        )
    # controle de limite de geração de potência reativa
    if anarede.ctrl["QLIM"]:
        anarede.ctrlcount += 1
        anarede.totaldevicesctrl += anarede.nger
        anarede.ctrlorder[anarede.ctrlcount] = "QLIM"
        qlimsol(
            anarede,
        )
    # controle suave simbolico de limite de geração de potência reativa
    # if anarede.ctrl['QLIMs']:
    #     anarede.ctrlcount += 1
    #     anarede.totaldevicesctrl += anarede.nger
    #     anarede.ctrlorder[anarede.ctrlcount] = "QLIMs"
    #     qlimssol(
    #         anarede,
    #     )
    # # controle suave numerico de limite de geração de potência reativa
    # if anarede.ctrl['QLIMn']:
    #     anarede.ctrlcount += 1
    #     anarede.totaldevicesctrl += anarede.nger
    #     anarede.ctrlorder[anarede.ctrlcount] = "QLIMn"
    #     qlimnsol(
    #         anarede,
    #     )
    # # controle de compensadores estáticos de potência reativa
    # if anarede.ctrl['SVCs']:
    #     anarede.ctrlcount += 1
    #     anarede.totaldevicesctrl += anarede.ncer
    #     anarede.ctrlorder[anarede.ctrlcount] = "SVCs"
    #     svcssol(
    #         anarede,
    #     )
    # controle de magnitude de tensão de barramentos
    if anarede.ctrl["VLIM"]:
        anarede.ctrlcount += 1
        anarede.ctrlorder[anarede.ctrlcount] = "VLIM"
        pass

    anarede.Tval = sum(anarede.maskP)
    anarede.Vval = sum(anarede.maskQ)

    if not anarede.ctrlcount:
        anarede.ctrldim = 0


def ctrlsch(
    anarede,
):
    """adiciona variáveis especificadas de controles ativos

    Args
        anarede:
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
                anarede,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsch(
                anarede,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssch(
                anarede,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsch(
                anarede,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsch(
                anarede,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrlres(
    anarede,
    case: int = 0,
):
    """adiciona resíduos de equações de controle de controles ativos

    Args
        anarede:
        case: caso analisado do fluxo de potência continuado (prev + corr)
            valor padrão igual a zero -> Newton-Raphson
    """
    ## Inicialização
    # Variável
    anarede.deltaY = array([])

    # Loop
    for value in anarede.ctrl:
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
                anarede,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimres(
                anarede,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimsres(
                anarede,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnres(
                anarede,
                case,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcres(
                anarede,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    if anarede.deltaY.size == 0:
        anarede.deltaY = array([])


def ctrljac(
    anarede,
):
    """submatrizes referentes aos controles ativos

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.truedim = deepcopy(anarede.jacobian.shape[0])

    # Loop
    for value in anarede.ctrl:
        # Dimensão
        anarede.ctrldim = anarede.jacobian.shape[0] - anarede.truedim

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
                anarede,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsubjac(
                anarede,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssubjac(
                anarede,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsubjac(
                anarede,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsubjac(
                anarede,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    # Dimensão
    anarede.ctrldim = anarede.jacobian.shape[0] - anarede.truedim

    # Atualização da Máscara da Jacobiana
    if (anarede.maskctrlcount == 0) and (anarede.solution["method"] != "EXPC"):
        anarede.maskctrlcount += 1

    elif (anarede.maskctrlcount == 0) and (anarede.solution["method"] == "EXPC"):
        anarede.maskctrlcount += 1


def ctrlupdt(
    anarede,
):
    """atualização das variáveis de estado adicionais por controle ativo

    Args
        anarede:
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
                anarede,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimupdt(
                anarede,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimsupdt(
                anarede,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnupdt(
                anarede,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcupdt(
                anarede,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrlcorrsol(
    anarede,
    case,
):
    """atualização das variáveis de controle para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
        case: caso analisado do fluxo de potência continuado (prev + corr)
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
                anarede,
                case,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimcorr(
                anarede,
                case,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimscorr(
                anarede,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimncorr(
                anarede,
                case,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svccorr(
                anarede,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrlheuristics(
    anarede,
):
    """aplicação de heurísticas das variáveis de controle para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.ctrlheur = False
    if not hasattr(anarede, "bifurcation"):
        anarede.bifurcation = False

    # Loop
    for value in anarede.ctrl:
        if (anarede.ctrlheur) or ((anarede.bifurcation) and (not anarede.cte["FULL"])):
            break

        elif (not anarede.ctrlheur) and (not anarede.solution["pmc"]):
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
                    anarede,
                )
            # controle suave de limite de geração de potência reativa
            elif value == "QLIMs":
                qlimsheur(
                    anarede,
                )
            # controle suave de limite de geração de potência reativa
            elif value == "QLIMn":
                qlimnheur(
                    anarede,
                )
            # controle de compensadores estáticos de potência reativa
            elif value == "SVCs":
                svcheur(
                    anarede,
                )
            # controle de magnitude de tensão de barramentos
            elif value == "VCTRL":
                pass


def ctrlpop(
    anarede,
    pop: int = 1,
):
    """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas

    Args
        anarede:
        pop: quantidade de ações necessárias
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
            qlimspop(anarede, pop=pop)
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnpop(anarede, pop=pop)
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            pass
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrlcpf(
    anarede,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
                anarede,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrlsolcpf(
    anarede,
    case,
):
    """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

    Args
        anarede:
        case: etapa do fluxo de potência continuado analisada
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
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
                anarede,
                case,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            pass
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsolcpf(
                anarede,
                case,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass


def ctrldelta(
    anarede,
):
    """checagem da variação dos resíduos durante método iterativo de newton-raphson

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    boollist = list()
    ctrl = 0

    # Loop
    for value in anarede.ctrl:
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
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["TEPA"]
            )
            ctrl += anarede.nger
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["TEPR"]
            )
            ctrl += anarede.nger
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["ASTP"]
            )
            ctrl += anarede.nger
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["QLST"]
            )
            ctrl += anarede.nger
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["QLST"]
            )
            ctrl += anarede.nger
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.nger]) > anarede.cte["QLST"]
            )
            ctrl += anarede.nger
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            boollist.append(
                norm(anarede.deltaY[ctrl : ctrl + anarede.ncer]) > anarede.cte["QLST"]
            )
            ctrl += anarede.ncer
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    return any(boollist)


def ctrlhess(
    anarede,
):
    """submatrizes referentes aos controles ativos

    Args
        anarede:
    """
    ## Inicialização
    # Loop
    for value in anarede.ctrl:
        # Dimensão
        anarede.ctrldim = anarede.hessian.shape[0] - anarede.truedim

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
                anarede,
            )
        # controle de limite de geração de potência reativa
        elif value == "QLIM":
            qlimsubhess(
                anarede,
            )
        # controle suave simbolico de limite de geração de potência reativa
        elif value == "QLIMs":
            qlimssubhess(
                anarede,
            )
        # controle suave numerico de limite de geração de potência reativa
        elif value == "QLIMn":
            qlimnsubhess(
                anarede,
            )
        # controle de compensadores estáticos de potência reativa
        elif value == "SVCs":
            svcsubhess(
                anarede,
            )
        # controle de magnitude de tensão de barramentos
        elif value == "VCTRL":
            pass

    # Dimensão
    anarede.ctrldim = anarede.hessian.shape[0] - anarede.truedim
