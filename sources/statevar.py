# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from ctrl import controlupdt

def update(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.solution["theta"] += powerflow.statevar[0 : (powerflow.nbus)]
    powerflow.solution["voltage"] += powerflow.statevar[
        (powerflow.nbus) : (2 * powerflow.nbus)
    ]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )


