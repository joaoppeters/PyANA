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
    powerflow.pqsch = {
        "potencia_ativa_especificada": zeros(powerflow.nbus),
        "potencia_reativa_especificada": zeros(powerflow.nbus),
    }

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Potência ativa especificada
        powerflow.pqsch["potencia_ativa_especificada"][idx] += value["potencia_ativa"]
        powerflow.pqsch["potencia_ativa_especificada"][idx] -= value["demanda_ativa"]

        # Potência reativa especificada
        powerflow.pqsch["potencia_reativa_especificada"][idx] += value[
            "potencia_reativa"
        ]
        powerflow.pqsch["potencia_reativa_especificada"][idx] -= value[
            "demanda_reativa"
        ]

    # Tratamento
    powerflow.pqsch["potencia_ativa_especificada"] /= powerflow.options["BASE"]
    powerflow.pqsch["potencia_reativa_especificada"] /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0:
        controlsch(
            powerflow,
        )