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
    powerflow,
    case: int = 0,
    stage: str = None,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    if stage == None:
        powerflow.statevar = powerflow.statevar.reshape(
            powerflow.statevar.size,
        )

        # configuração reduzida
        powerflow.solution["theta"][powerflow.maskP] += (
            powerflow.solution["sign"] * powerflow.statevar[0 : (powerflow.Tval)]
        )
        powerflow.solution["voltage"][powerflow.maskQ] += (
            powerflow.solution["sign"]
            * powerflow.statevar[(powerflow.Tval) : (powerflow.Tval + powerflow.Vval)]
        )

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.controlcount > 0:
            controlupdt(
                powerflow,
            )

        if powerflow.solution["method"] == "EXPC":
            powerflow.solution["lambda"] += (
                powerflow.solution["sign"]
                * powerflow.statevar[
                    (powerflow.Tval + powerflow.Vval + powerflow.controldim)
                ]
            )
            powerflow.solution["eigen"][powerflow.mask] += (
                powerflow.solution["sign"]
                * powerflow.statevar[
                    (powerflow.Tval + powerflow.Vval + powerflow.controldim + 1) :
                ]
            )

    # Condição de previsão
    elif stage == "p":
        powerflow.solution["theta"][powerflow.maskP] += (
            powerflow.solution["sign"] * powerflow.statevar[0 : (powerflow.Tval)]
        )
        # Condição de variável de passo
        if powerflow.solution["varstep"] == "lambda":
            powerflow.solution["voltage"][powerflow.maskQ] += (
                powerflow.solution["sign"]
                * powerflow.statevar[
                    (powerflow.Tval) : (powerflow.Tval + powerflow.Vval)
                ]
            )
            powerflow.solution["stepsch"] += powerflow.statevar[-1]

        elif powerflow.solution["varstep"] == "volt":
            powerflow.solution["step"] += powerflow.statevar[-1]
            powerflow.solution["stepsch"] += powerflow.statevar[-1]
            powerflow.solution["vsch"] = (
                powerflow.solution["voltage"][powerflow.nodevarvolt]
                + powerflow.statevar[(powerflow.nbus + powerflow.nodevarvolt)]
            )

        # Verificação do Ponto de Máximo Carregamento
        if case > 0:
            if case == 1:
                powerflow.solution["stepmax"] = deepcopy(powerflow.solution["stepsch"])

            elif case != 1:
                if (
                    powerflow.solution["stepsch"]
                    > powerflow.operationpoint[case - 1]["c"]["step"]
                ) and (not powerflow.solution["pmc"]):
                    powerflow.solution["stepmax"] = deepcopy(
                        powerflow.solution["stepsch"]
                    )

                elif (
                    powerflow.solution["stepsch"]
                    < powerflow.operationpoint[case - 1]["c"]["step"]
                ) and (not powerflow.solution["pmc"]):
                    powerflow.solution["pmc"] = True
                    powerflow.pmcidx = deepcopy(case)

    # Condição de correção
    elif stage == "c":
        powerflow.solution["theta"][powerflow.maskP] += (
            powerflow.solution["sign"] * powerflow.statevar[0 : (powerflow.Tval)]
        )
        powerflow.solution["voltage"][powerflow.maskQ] += (
            powerflow.solution["sign"]
            * powerflow.statevar[(powerflow.Tval) : (powerflow.Tval + powerflow.Vval)]
        )
        powerflow.solution["step"] += powerflow.statevar[-1]

        if powerflow.solution["varstep"] == "volt":
            powerflow.solution["stepsch"] += powerflow.statevar[-1]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0 and stage != None:
        controlupdt(
            powerflow,
        )


def updtpwr(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])
    I = powerflow.Ybus @ V
    S = diag(V) @ conj(I)

    powerflow.solution["active"] = (
        S.real * powerflow.options["BASE"] + powerflow.dbarDF["demanda_ativa"].tolist()
    )
    powerflow.solution["reactive"] = (
        S.imag * powerflow.options["BASE"]
        + powerflow.dbarDF["demanda_reativa"].tolist()
    )


def updtlinear(
    powerflow,
):
    """
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização    
    # Atualização dos ângulos dos barramentos
    powerflow.solution["theta"] = deepcopy(powerflow.statevar)