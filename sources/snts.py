# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def snts(
    powerflow,
):
    """
    
    Args
    ----
    powerflow : 
    """

    from os import listdir
    import pandas as pd

    from rela import bint, rbar, vsm
    from ulog import basexlf, basexic, basexct

    ## Inicialização
    basexlf(powerflow,)
    powerflow.dbar_base = rbar(powerflow, where="EXLF",)
    powerflow.intercambio_base = bint(powerflow, where="EXLF",)

    basexic(powerflow,)
    powerflow.dbar_mlp = rbar(powerflow, where="EXIC",)
    vsm(powerflow, base=True,)
    powerflow.intercambio_vsm = bint(powerflow, where="EXIC",)

    basexct(powerflow, where="EXIC",)
    powerflow.dbar_premlp = rbar(powerflow, where="EXCT",)
    powerflow.intercambio_premlp = bint(powerflow, where="EXCT",)
    rfiles = [
        f
        for f in listdir(powerflow.bxctfolder)
        if f.startswith("EXCT_" + powerflow.name) and f.endswith(".REL")
    ]
    for rfile in rfiles:
        powerflow.dbar_premlp = pd.concat([powerflow.dbar_premlp, rbar(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True)
        powerflow.intercambio_premlp = pd.concat([powerflow.intercambio_premlp, bint(powerflow, where="EXCT", rfile=rfile,)], ignore_index=True)




    print()