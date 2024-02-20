# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros
from ctrl import controlsch


def scheduled(
    powerflow,
):
    """método para armazenamento dos parâmetros especificados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento das potências ativa e reativa especificadas
    powerflow.psch = zeros(powerflow.nbus)
    powerflow.qsch = zeros(powerflow.nbus)

    # Potências ativa e reativa especificadas
    for idx, value in powerflow.dbarraDF.iterrows():
        powerflow.psch[idx] += value["potencia_ativa"]
        powerflow.psch[idx] -= value["demanda_ativa"]

        powerflow.qsch[idx] += value["potencia_reativa"]
        powerflow.qsch[idx] -= value["demanda_reativa"]

    # Tratamento
    powerflow.psch /= powerflow.options["BASE"]
    powerflow.qsch /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0:
        controlsch(
            powerflow,
        )
