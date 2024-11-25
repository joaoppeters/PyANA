# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def factor(
    name,
    lpmean,
    wpmean,
    dbarDF,
    dbar,
    dger,
    stateload,
    stategeneration,
):
    """

    Args
        powerflow:
    """

    from pandas import concat, merge
    from numpy import nan

    ## Inicialização
    if "2Q2024" in name:
        # Load Power Factor IN SP State
        dbar[
            [
                "numero",
                "potencia_ativa",
                "potencia_reativa",
                "demanda_ativa",
                "demanda_reativa",
                "shunt_barra",
            ]
        ] = dbar[
            [
                "numero",
                "potencia_ativa",
                "potencia_reativa",
                "demanda_ativa",
                "demanda_reativa",
                "shunt_barra",
            ]
        ].replace(
            r"^\s*$", nan, regex=True
        )
        dbar = dbar.astype(
            {
                "numero": int,
                "potencia_ativa": float,
                "potencia_reativa": float,
                "demanda_ativa": float,
                "demanda_reativa": float,
                "shunt_barra": float,
            }
        )
        # Mark rows for common bars
        mdbar = dbar.copy()
        commondbar = mdbar.numero.isin(stateload.numero)
        mdbar["operacao"] = "M"

        # Update `fator_demanda_ativa` and `fator_demanda_reativa` directly in `mdbar`
        mdbar.loc[commondbar, "fator_demanda_ativa"] = (
            mdbar.loc[commondbar, "demanda_ativa"] / lpmean
        )
        mdbar.loc[commondbar, "fator_demanda_reativa"] = (
            mdbar.loc[commondbar, "demanda_reativa"]
            / mdbar.loc[commondbar, "demanda_ativa"]
        ).where(mdbar.loc[commondbar, "demanda_ativa"] != 0, 0)

        # Filter rows corresponding to wind generation
        eolNE = mdbar.numero.isin(
            stategeneration.loc[stategeneration.nome.str.contains("EOL")].numero
        )
        mdbar.loc[eolNE, "fator_geracao_eolica"] = (
            mdbar.loc[eolNE, "potencia_ativa"] / wpmean
        )
        mdbar = mdbar.fillna(0)
        # mdbar = merge(
        #     mdbar,
        #     eol[["numero", "nome", "potencia_ativa", "fator_geracao_eolica"]],
        #     on="numero",
        #     how="outer",
        #     suffixes=("", "_eol"),
        # )
        # mdbar["nome"] = mdbar.nome.combine_first(mdbar.nome_eol)
        # mdbar["potencia_ativa"] = mdbar.potencia_ativa.combine_first(
        #     mdbar.potencia_ativa_eol
        # )
        # mdbar.drop(columns=["nome_eol", "potencia_ativa_eol"], inplace=True)
        # mdbar = mdbar.fillna(0)

        # UHE & UTE Generation Power Factor in NE Region
        uheute = dbarDF[dbarDF.nome.str.contains("UHE|UTE") & dbarDF.tipo == 1].copy()
        dger = dger.astype({"numero": int})
        commondger = merge(dger, uheute, on="numero").numero
        dger["operacao"] = dger.numero.apply(
            lambda x: "M" if x in commondger.values else None
        )
        dger = merge(
            dger, dbarDF[["numero", "potencia_ativa"]], on="numero", how="left"
        )
        newdger = uheute[~uheute.numero.isin(dger.numero)].copy()
        newdger["operacao"] = "A"
        mdger = concat([dger, newdger], ignore_index=True)
        mdger = mdger[mdger.numero.isin(uheute.numero)].reset_index(drop=True)
        mdger["fator_participacao"] = (
            mdger.potencia_ativa * 100 / mdger.potencia_ativa.sum()
        )
        mdger = mdger.fillna(0)

    else:
        # Load Power Factor
        dbar["fator_demanda_ativa"] = stateload.demanda_ativa / lpmean
        dbar["fator_potencia"] = stateload.demanda_reativa / stateload.demanda_ativa

        # # Wind Generation Power Factor
        # dbar["fator_geracao_eolica"] = [
        #     value["potencia_ativa"] / wpmean if "EOL" in value["nome"] else 0
        #     for idx, value in stategeneration.iterrows()
        # ]

    return mdbar, mdger


def loadf(
    mdbar,
    psamples,
    s,
):
    """fator de potência aplicado à estocasticidade das cargas

    Args
        mdbar:
        dbarDF:
        psamples:
        s:
    """

    import pandas as pd

    ## Inicialização
    for idx, value in mdbar.iterrows():
        if not pd.isna(value.fator_demanda_ativa) and value.demanda_ativa != 0:
            mdbar.loc[idx, "demanda_ativa"] = (
                psamples[s] * mdbar.loc[idx, "fator_demanda_ativa"]
            )
        if (
            (not pd.isna(value.fator_demanda_reativa))
            and (not pd.isna(value.fator_demanda_ativa))
            and value.demanda_reativa != 0
            and value.demanda_ativa != 0
        ):
            mdbar.loc[idx, "demanda_reativa"] = (
                psamples[s]
                * mdbar.loc[idx, "fator_demanda_ativa"]
                * mdbar.loc[idx, "fator_demanda_reativa"]
            )

    return mdbar


def windf(
    mdbar,
    wsamples,
    s,
):
    """fator de potência aplicado à estocasticidade da geração eólica

    Args
        dbar:
        dbarDF:
        wsamples:
        s:
    """

    import pandas as pd

    ## Inicialização
    for idx, value in mdbar.iterrows():
        if (not pd.isna(value.fator_geracao_eolica)) and "EOL" in value.nome:
            mdbar.loc[idx, "potencia_ativa"] = round(
                wsamples[s] * mdbar.loc[idx, "fator_geracao_eolica"], 0
            )

    return mdbar
