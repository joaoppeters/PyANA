# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import re
import pandas as pd
import numpy as np
from os.path import dirname

BUS_COLS = [
    "bus_i",
    "type",
    "Pd",
    "Qd",
    "Gs",
    "Bs",
    "area",
    "Vm",
    "Va",
    "baseKV",
    "zone",
    "Vmax",
    "Vmin",
]

GEN_COLS = [
    "bus",
    "Pg",
    "Qg",
    "Qmax",
    "Qmin",
    "Vg",
    "mBase",
    "status",
    "Pmax",
    "Pmin",
    "Pc1",
    "Pc2",
    "Qc1min",
    "Qc1max",
    "Qc2min",
    "Qc2max",
    "ramp_agc",
    "ramp_10",
    "ramp_30",
    "ramp_q",
    "apf",
]

BRANCH_COLS = [
    "fbus",
    "tbus",
    "r",
    "x",
    "b",
    "rateA",
    "rateB",
    "rateC",
    "ratio",
    "angle",
    "status",
    "angmin",
    "angmax",
]


def rmatpower(anarede, matpower):
    """read matpower .m file and populate PowerFlowContainer with bus, gen, branch data

    Args
        anarede: PowerFlowContainer to populate with data from .m file
        matpower: PowerFlowContainer to populate with matpower data
    """
    ## Inicializacao
    mpfile = dirname(dirname(__file__)) + "\\sistemas\\" + anarede.system
    with open(mpfile, "r", encoding="utf-8") as f:
        text = f.read()

    version_match = re.search(r"mpc\.version\s*=\s*'(\d+)'", text)
    version = version_match.group(1) if version_match else "unknown"
    baseMVA = _scalar(text, "baseMVA")

    bus_data = _extract_matrix(text, "bus")
    bus_df = pd.DataFrame(bus_data, columns=BUS_COLS)
    bus_df["bus_i"] = bus_df["bus_i"].astype(int)
    bus_df["type"] = bus_df["type"].astype(int)
    bus_df["area"] = bus_df["area"].astype(int)
    bus_df["zone"] = bus_df["zone"].astype(int)

    gen_data = _extract_matrix(text, "gen")
    gen_df = pd.DataFrame(gen_data, columns=GEN_COLS)
    gen_df["bus"] = gen_df["bus"].astype(int)
    gen_df["status"] = gen_df["status"].astype(int)

    branch_data = _extract_matrix(text, "branch")
    branch_df = pd.DataFrame(branch_data, columns=BRANCH_COLS)
    branch_df["fbus"] = branch_df["fbus"].astype(int)
    branch_df["tbus"] = branch_df["tbus"].astype(int)
    branch_df["status"] = branch_df["status"].astype(int)

    return bus_df, gen_df, branch_df, baseMVA


def _extract_matrix(text: str, name: str) -> list[list[float]]:
    """
    Pull the numeric rows from  mpc.<name> = [ ... ];
    Returns a list of rows (each row is a list of floats).
    """
    pattern = rf"mpc\.{name}\s*=\s*\[(.*?)\];"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        raise ValueError(f"Section 'mpc.{name}' not found in file.")

    rows = []
    for line in match.group(1).splitlines():
        line = (
            line.split("%")[0].strip().rstrip(";").strip()
        )  # strip comments & semicolons
        if not line:
            continue
        try:
            rows.append([float(v) for v in line.split()])
        except ValueError:
            continue  # skip malformed lines
    return rows


def _scalar(text: str, name: str) -> float:
    """Extract  mpc.<name> = <value>;"""
    match = re.search(rf"mpc\.{name}\s*=\s*([^\s;]+)\s*;", text)
    if not match:
        raise ValueError(f"Scalar 'mpc.{name}' not found.")
    return float(match.group(1).strip("'\""))
