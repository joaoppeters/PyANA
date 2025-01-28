# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "2Q2024_R2_C11.pwf"
# system = "01 - ONS - MENSAL - JANEIRO 2020 - LEVE - R1.pwf"
# system = "01 - ONS - MENSAL - JANEIRO 2020 - LEVE.pwf"
# system = "NE224_CASO1_MA.pwf"
# system = "NE224-C1.pwf"

sim = "EXLF"  # NEWTON-RAPHSON
# sim = "EXIC" # CONTINUATION POWER FLOW
# sim = "EXPC" # POINT OF COLLAPSE
# sim = "EXSI"  # DYNAMIC SIMULATION
# sim = "BXLF" # NEWTON-RAPHSON (ANAREDE BATCH RUNNING)
# sim = "BXIC" # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING)
# sim = "BXCT" # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING)
sim = "SXLF"  # STOCHASTIC (ANAREDE BATCH RUNNING)
sim = "SXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# sim = "SXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# sim = "SPVCT" # CONTINUATION POWER FLOW + CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# sim = "PSSe" # PSS/E EXCEL FILE FORMATTING
# sim = "RELR" # READING ANAREDE REL FILES
# sim = "DATA" # DATA MANIPULATION
# sim = "EXCE" # CROSS-ENTROPY
# sim = "AREA"
# sim = "RREL"
# sim = "RINT"
# sim = "RPVCT"
sim = "Q2024"
# sim = "VSM"
sim = "CXLF"
# sim = "CXIC"
# sim = "CXCT"


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
    sim=sim,
    control=control,
    monitor=monitor,
    report=report,
)
