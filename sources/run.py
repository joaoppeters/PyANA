# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from powerflow import PowerFlow

# system = "1Q2017_R1_C6.pwf"  # JAN-APR 2017
# system = "2Q2017_R1_C6.pwf"  # MAY-AUG 2017
# system = "3Q2017_R2_C6.pwf"  # SEP-DEC 2017
# system = "1Q2018_R2_C6.pwf"  # JAN-APR 2018
# system = "2Q2018_R2_C6.pwf"  # MAY-AUG 2018
# system = "3Q2018_R2_C6.pwf"  # SEP-DEC 2018
# system = "1Q2019_R1_C6.pwf"  # JAN-APR 2019
# system = "2Q2019_R2_C6.pwf"  # MAY-AUG 2019
# system = "3Q2019_R1_C6.pwf"  # SEP-DEC 2019
# system = "1Q2020_R1_C6.pwf"  # JAN-APR 2020
# system = "2Q2020_R1_C6.pwf"  # MAY-AUG 2020
# system = "3Q2020_R2_C6.pwf"  # SEP-DEC 2020
# system = "1Q2021_R2_C6.pwf"  # JAN-APR 2021
# system = "2Q2021_R3_C6.pwf"  # MAY-AUG 2021
# system = "3Q2021_R1_C6.pwf"  # SEP-DEC 2021
# system = "1Q2022_R2_C6.pwf"  # JAN-APR 2022
# system = "2Q2022_R1_C6.pwf"  # MAY-AUG 2022
# system = "3Q2022_R1_C6.pwf"  # SEP-DEC 2022
# system = "1Q2023_R1_C3.pwf"  # JAN-APR 2023
# system = "2Q2023_R2_C9.pwf"  # MAY-AUG 2023
# system = "3Q2023_R2_C9.pwf"  # SEP-DEC 2023
# system = "1Q2024_R2_C11.pwf" # JAN-APR 2024
system = "2Q2024_R2_C1.pwf"  # MAY-AUG 2024
# system = "3Q2024_R2_C11.pwf" # SEP-DEC 2024
# system = "1Q2025_R1_C11.pwf" # JAN-APR 2025
# system = "2Q2025_R0_C11.pwf" # MAY-AUG 2025
# system = "NE224-C1.pwf"
system = "107BARRAS_DCTG.pwf"

# method =  "EXLF"  # NEWTON-RAPHSON
# method =  "EXIC"  # CONTINUATION POWER FLOW
# method =  "EXPC"  # POINT OF COLLAPSE
# method =  "EXSI"  # DYNAMIC SIMULATION
# method =  "BXLF"  # NEWTON-RAPHSON (ANAREDE BATCH RUNNING)
# method =  "BXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING)
# method =  "BXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING)
method = "SXLF"  # STOCHASTIC (ANAREDE BATCH RUNNING)
# method =  "SXIC"  # CONTINUATION POWER FLOW (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "SXCT"  # CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "SPVCT" # CONTINUATION POWER FLOW + CONTINGENCY ANALYSIS (ANAREDE BATCH RUNNING OF STOCHASTIC CASES)
# method =  "PSSe"  # PSS/E EXCEL FILE FORMATTING
# method =  "RELR"  # READING ANAREDE REL FILES
# method =  "DATA"  # DATA MANIPULATION
# method =  "EXCE"  # CROSS-ENTROPY
# method = "AREA"
# method =  "RTOT"
# method =  "RINT"
# method =  "RINT"
# method =  "RPVCT"
# method =  "VSM"
method = "CXLF"
# method =  "CXIC"
# method =  "CXCT"
method = "SNTS"


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
