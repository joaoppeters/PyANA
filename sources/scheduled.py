# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import cos, sin, zeros
from ctrl import ctrlsch


def scheduled(
    anarede,
):
    """metodo para armazenamento dos Args especificados

    Args
        anarede:
    """
    # Potências ativa e reativa especificadas
    if anarede.solution["method"] == "LFDC":
        anarede.psch = zeros(anarede.nbus)
        anarede.qsch = zeros(anarede.nbus)
        anarede.psch += anarede.dbarDF["potencia_ativa"].to_numpy()
        anarede.psch -= anarede.dbarDF["demanda_ativa"].to_numpy()

    elif anarede.solution["method"] == "EXPC":
        anarede.psch = zeros(anarede.nbus)
        anarede.psch += anarede.solution["potencia_ativa"]
        anarede.psch -= anarede.dbarDF["demanda_ativa"].to_numpy()
        anarede.qsch = zeros(anarede.nbus)
        anarede.qsch += anarede.solution["potencia_reativa"]
        anarede.qsch -= anarede.dbarDF["demanda_reativa"].to_numpy()

    elif (anarede.solution["method"] != "EXPC") and (
        anarede.solution["method"] != "LFDC"
    ):
        anarede.psch = zeros(anarede.nbus)
        anarede.psch += anarede.dbarDF["potencia_ativa"].to_numpy()
        anarede.psch -= anarede.dbarDF["demanda_ativa"].to_numpy()
        anarede.qsch = zeros(anarede.nbus)
        anarede.qsch += anarede.dbarDF["potencia_reativa"].to_numpy()
        anarede.qsch -= anarede.dbarDF["demanda_reativa"].to_numpy()

    anarede.psch /= anarede.cte["BMVA"]
    anarede.qsch /= anarede.cte["BMVA"]

    # Variaveis especificadas de controle ativos
    if anarede.ctrlcount > 0 and anarede.solution["method"] != "LFDC":
        ctrlsch(
            anarede,
        )
