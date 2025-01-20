# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "2Q2024_R2_C6.pwf"
# system = "01 - ONS - MENSAL - JANEIRO 2020 - LEVE - R1.pwf"
# system = "01 - ONS - MENSAL - JANEIRO 2020 - LEVE.pwf"
# system = "NE224_CASO1_MA.pwf"
# system = "NE224-C1.pwf"

method = "EXLF"  # NEWTON-RAPHSON
# method = "EXIC" # CONTINUATION POWER FLOW
# method = "EXPC" # POINT OF COLLAPSE
# method = "EXSI"  # DYNAMIC SIMULATION
# method = "BXLF" # NEWTON-RAPHSON (ANAREDE BATCH RUNNING)
# method = "BXIC" # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING)
# method = "BXCT" # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING)
method = "SXLF"  # STOCHASTIC (ANAREDE BATCH RUNNING)
method = "SXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method = "SXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method = "SPVCT" # CONTINUATION POWER FLOW + CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method = "PSSe" # PSS/E EXCEL FILE FORMATTING
# method = "RELR"  # READING ANAREDE REL FILES
# method = "DATA" # DATA MANIPULATION
# method = "EXCE" # CROSS-ENTROPY
# method = "AREA"
# method = "RREL"
# method = "RINT"
# method = "RPVCT"


control = [
    # "CREM",
    # "CTAP",
    # "CTAPd",
    # "FREQ",
    # "QLIM",
    # "QLIMs",
    # "SVCs",
]

monitor = [
    # "PFLOW",
    # "PGMON",
    # "QGMON",
    # "VMON",
]

report = [
    "RBAR",
    # "RLIN",
    # "RGER",
    # "RCER",
]

PowerFlow(
    system=system,
    method=method,
    control=control,
    monitor=monitor,
    report=report,
)
