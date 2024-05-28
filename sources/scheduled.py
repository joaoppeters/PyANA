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
    # Potências ativa e reativa especificadas
    if powerflow.solution["method"] == "LFDC":
        powerflow.psch = zeros(powerflow.nbus)
        powerflow.qsch = zeros(powerflow.nbus)
        powerflow.psch += powerflow.dbarDF["potencia_ativa"].to_numpy()
        powerflow.psch -= powerflow.dbarDF["demanda_ativa"].to_numpy()

    elif powerflow.solution["method"] == "EXPC":
        powerflow.psch = zeros(powerflow.nbus)
        powerflow.psch += powerflow.solution["potencia_ativa"]
        powerflow.psch -= powerflow.dbarDF["demanda_ativa"].to_numpy()
        powerflow.qsch = zeros(powerflow.nbus)
        powerflow.qsch += powerflow.solution["potencia_reativa"]
        powerflow.qsch -= powerflow.dbarDF["demanda_reativa"].to_numpy()

    elif (powerflow.solution["method"] != "EXPC") and (
        powerflow.solution["method"] != "LFDC"
    ):
        powerflow.psch = zeros(powerflow.nbus)
        powerflow.psch += powerflow.dbarDF["potencia_ativa"].to_numpy()
        powerflow.psch -= powerflow.dbarDF["demanda_ativa"].to_numpy()
        powerflow.qsch = zeros(powerflow.nbus)
        powerflow.qsch += powerflow.dbarDF["potencia_reativa"].to_numpy()
        powerflow.qsch -= powerflow.dbarDF["demanda_reativa"].to_numpy()

    powerflow.psch /= powerflow.options["BASE"]
    powerflow.qsch /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0 and powerflow.solution["method"] != "LFDC":
        controlsch(
            powerflow,
        )