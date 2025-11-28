# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import conj, diag, exp

from ctrl import controlupdt


def updtstt(
    anarede,
    case: int = 0,
    stage: str = None,
):
    """atualização das variáveis de estado

    Args
        anarede:
    """
    ## Inicialização
    if stage == None:
        anarede.statevar = anarede.statevar.reshape(
            anarede.statevar.size,
        )

        # configuração reduzida
        anarede.solution["theta"][anarede.maskP] += (
            anarede.solution["sign"] * anarede.statevar[0 : (anarede.Tval)]
        )
        anarede.solution["voltage"][anarede.maskQ] += (
            anarede.solution["sign"]
            * anarede.statevar[(anarede.Tval) : (anarede.Tval + anarede.Vval)]
        )

        # Atualização das variáveis de estado adicionais para controles ativos
        if anarede.controlcount > 0:
            controlupdt(
                anarede,
            )

        if anarede.solution["method"] == "EXPC":
            anarede.solution["lambda"] += (
                anarede.solution["sign"]
                * anarede.statevar[(anarede.Tval + anarede.Vval + anarede.controldim)]
            )
            anarede.solution["eigen"][anarede.mask] += (
                anarede.solution["sign"]
                * anarede.statevar[
                    (anarede.Tval + anarede.Vval + anarede.controldim + 1) :
                ]
            )

    # Condição de previsão
    elif stage == "p":
        anarede.solution["theta"][anarede.maskP] += (
            anarede.solution["sign"] * anarede.statevar[0 : (anarede.Tval)]
        )
        # Condição de variável de passo
        if anarede.solution["varstep"] == "lambda":
            anarede.solution["voltage"][anarede.maskQ] += (
                anarede.solution["sign"]
                * anarede.statevar[(anarede.Tval) : (anarede.Tval + anarede.Vval)]
            )
            anarede.solution["stepsch"] += anarede.statevar[-1]

        elif anarede.solution["varstep"] == "volt":
            anarede.solution["step"] += anarede.statevar[-1]
            anarede.solution["stepsch"] += anarede.statevar[-1]
            anarede.solution["vsch"] = (
                anarede.solution["voltage"][anarede.nodevarvolt]
                + anarede.statevar[(anarede.nbus + anarede.nodevarvolt)]
            )

        # Verificação do Ponto de Máximo Carregamento
        if case > 0:
            if case == 1:
                anarede.solution["stepmax"] = deepcopy(anarede.solution["stepsch"])

            elif case != 1:
                if (
                    anarede.solution["stepsch"]
                    > anarede.operationpoint[case - 1]["c"]["step"]
                ) and (not anarede.solution["pmc"]):
                    anarede.solution["stepmax"] = deepcopy(anarede.solution["stepsch"])

                elif (
                    anarede.solution["stepsch"]
                    < anarede.operationpoint[case - 1]["c"]["step"]
                ) and (not anarede.solution["pmc"]):
                    anarede.solution["pmc"] = True
                    anarede.pmcidx = deepcopy(case)

    # Condição de correção
    elif stage == "c":
        anarede.solution["theta"][anarede.maskP] += (
            anarede.solution["sign"] * anarede.statevar[0 : (anarede.Tval)]
        )
        anarede.solution["voltage"][anarede.maskQ] += (
            anarede.solution["sign"]
            * anarede.statevar[(anarede.Tval) : (anarede.Tval + anarede.Vval)]
        )
        anarede.solution["step"] += anarede.statevar[-1]

        if anarede.solution["varstep"] == "volt":
            anarede.solution["stepsch"] += anarede.statevar[-1]

    # Atualização das variáveis de estado adicionais para controles ativos
    if anarede.controlcount > 0 and stage != None:
        controlupdt(
            anarede,
        )


def updtpwr(
    anarede,
):
    """atualização das variáveis de estado

    Args
        anarede:
    """
    ## Inicialização
    V = anarede.solution["voltage"] * exp(1j * anarede.solution["theta"])
    I = anarede.Yb @ V
    S = diag(V) @ conj(I)

    anarede.solution["active"] = (
        S.real * anarede.cte["BASE"] + anarede.dbarDF["demanda_ativa"].tolist()
    )
    anarede.solution["reactive"] = (
        S.imag * anarede.cte["BASE"] + anarede.dbarDF["demanda_reativa"].tolist()
    )


def updtlinear(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    # Atualização dos ângulos dos barramentos
    anarede.solution["theta"] = deepcopy(anarede.statevar)


def updttm(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    # Atualização das variaveis dinamicas tempo
    anarede.solution["delta"] += anarede.timestatevar[0 : 2 * anarede.nger : 2]
    anarede.solution["omega"] += anarede.timestatevar[1 : 2 * anarede.nger : 2]
    anarede.solution["theta"] += anarede.timestatevar[
        3 * anarede.nger : 3 * anarede.nger + anarede.nbus
    ]
    anarede.solution["voltage"] += anarede.timestatevar[
        4 * anarede.nger + anarede.nbus :
    ]
