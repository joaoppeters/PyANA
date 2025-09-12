# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

system = "2Q2024_R2_C8.pwf"  # MAY-AUG 2024
# system = "NE224-C1.pwf"
system = "107BARRAS_DCTG.pwf"
# system = "ieee14.pwf"
# system = "EXIC-JUN25C3MOD-FULL.PWF"

method = "EXLF"  # NEWTON-RAPHSON
# method =  "EXIC"  # CONTINUATION POWER FLOW
# method =  "EXPC"  # POINT OF COLLAPSE
# method =  "EXSI"  # DYNAMIC SIMULATION

# method =  "BXLF"  # NEWTON-RAPHSON (ANAREDE BATCH RUNNING)
# method =  "BXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING)
# method =  "BXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING)
# method =  "SXLF"  # STOCHASTIC (ANAREDE BATCH RUNNING)l
# method =  "SXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "SXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "SPVCT" # CONTINUATION POWER FLOW + CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "PSSe"  # PSS/E EXCEL FILE FORMATTING
# method =  "RELR"  # READING ANAREDE REL FILES
# method =  "DATA"  # DATA MANIPULATION
# method =  "EXCE"  # CROSS-ENTROPY
# method =  "AREA"
# method =  "RTOT"
# method =  "RINT"
# method =  "RINT"
# method =  "RPVCT"
# method =  "VSM"
# method =  "CXLF"
# method =  "CXIC"
# method =  "CXCT"
method = "UFES"
# method = "SAGE"
# method = "READ"


control = [
    # "CREM",
    # "CTAP",
    # "CTAPd",
    # "FREQ",
    # "QLIM",
    # "QLIMs",
    # "SVCs",
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
    report=report,
)
