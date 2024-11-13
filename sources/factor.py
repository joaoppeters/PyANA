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
):
    """

    Args
        powerflow: self do arquivo powerflow.py
    """

    from pandas import concat
    from numpy import random

    ## Inicialização
    if "2Q2024" in name:
        # Load Power Factor IN SP State
        sao_paulo = dbarDF.loc[
            dbarDF.area.isin(
                [
                    201,
                    202,
                    203,
                    204,
                    205,
                    206,
                    207,
                    208,
                    209,
                    210,
                    211,
                    212,
                    213,
                    214,
                    215,
                    216,
                    217,
                ]
            )
        ]
        sao_paulo["fator_demanda_ativa"] = sao_paulo.demanda_ativa / lpmean
        sao_paulo["fator_potencia"] = (
            sao_paulo.demanda_reativa / sao_paulo.demanda_ativa
        )

        # Wind Generation Power Factor in NE Region
        bahia = dbarDF.loc[dbarDF.area.isin([701, 702, 703, 704])]
        bahia_sergipe = dbarDF.loc[dbarDF.area.isin([711, 712, 713, 714, 715, 716])]
        alagoas_pernambuco = dbarDF.loc[dbarDF.area.isin([721, 722, 723, 724])]
        paraiba_rio_grande_norte = dbarDF.loc[dbarDF.area.isin([741, 742, 743, 744])]
        ceara = dbarDF.loc[dbarDF.area.isin([761, 762, 763, 764])]
        piaui = dbarDF.loc[dbarDF.area.isin([771, 772, 773])]
        maranhao = dbarDF.loc[dbarDF.area.isin([222, 861, 862, 863, 864, 865, 866])]
        nordeste = concat(
            [
                bahia,
                bahia_sergipe,
                alagoas_pernambuco,
                paraiba_rio_grande_norte,
                ceara,
                piaui,
                maranhao,
            ],
            axis=0,
            ignore_index=True,
        )
        nordeste["fator_eol"] = [
            value.potencia_ativa / wpmean if "EOL" in value.nome else 0
            for idx, value in nordeste.iterrows()
        ]
        # Update on DGER DataFrame For Wind Generation in NE region
        ruler = dger[["ruler"]].copy()
        blockname = dger[["dger"]].copy()
        wind = nordeste[nordeste.fator_eol != 0]
        dger = wind[["numero", "fator_eol"]]
        dger["ruler"] = (
            ruler.ruler.reindex(range(len(dger))).fillna(method="ffill").values
        )
        dger["dger"] = (
            blockname.dger.reindex(range(len(dger))).fillna(method="ffill").values
        )
        dger["fator_eol"] = (dger["fator_eol"] * 1e2).round(2)
        difference = 100 - dger["fator_eol"].sum()
        if difference > 0:
            increment_indices = random.choice(
                dger.index, int(difference * 100), replace=True
            )
            dger.loc[increment_indices, "fator_eol"] += 0.01
        dger = dger.sort_values(by="fator_eol", ascending=False)
        dger["fator_eol"] = (dger["fator_eol"]).round(2)
        dger = dger.rename(columns={"fator_eol": "fator_participacao"})
        dger = dger.assign(
            **{
                col: None
                for col in [
                    "operacao",
                    "potencia_ativa_minima",
                    "potencia_ativa_maxima",
                    "fator_participacao_controle_remoto",
                    "fator_potencia_nominal",
                    "fator_servico_armadura",
                    "fator_servico_rotor",
                    "angulo_maximo_carga",
                    "reatancia_maquina",
                    "potencia_aparente_nominal",
                    "estatismo",
                ]
            }
        )

        # Merging Data Variables
        dbar = dbar.astype({"numero": int})
        dbar = dbar.merge(
            sao_paulo[["numero", "fator_demanda_ativa", "fator_potencia"]],
            on="numero",
            how="left",
        )
        dbar = dbar.merge(nordeste[["numero", "fator_eol"]], on="numero", how="left")
        # dbar[['fator_demanda_ativa', 'fator_potencia', 'fator_eol']] = dbar[['fator_demanda_ativa', 'fator_potencia', 'fator_eol']].fillna(0)

    else:
        # Load Power Factor
        dbar["fator_demanda_ativa"] = dbarDF.demanda_ativa / lpmean
        dbar["fator_potencia"] = dbarDF.demanda_reativa / dbarDF.demanda_ativa

        # Wind Generation Power Factor
        dbar["fator_eol"] = [
            value["potencia_ativa"] / wpmean if "EOL" in value["nome"] else 0
            for idx, value in dbarDF.iterrows()
        ]

    return dbar, dger


def loadf(
    dbar,
    dbarDF,
    psamples,
    s,
):
    """fator de potência aplicado à estocasticidade das cargas

    Args
        dbar: DataFrame com as barras
        dbarDF: DataFrame com as barras
        psamples: amostras da demanda ativa
        s: amostra
    """

    import pandas as pd

    ## Inicialização
    for idx, value in dbarDF.iterrows():
        if not pd.isna(dbar.loc[idx, "fator_demanda_ativa"]):
            dbar.loc[idx, "demanda_ativa"] = str(
                psamples[s] * dbar.loc[idx, "fator_demanda_ativa"]
            )
        if (
            (not pd.isna(dbar.loc[idx, "fator_potencia"]))
            and (not pd.isna(dbar.loc[idx, "fator_demanda_ativa"]))
            and value["demanda_reativa"] != 0
            and value["demanda_ativa"] != 0
        ):
            dbar.loc[idx, "demanda_reativa"] = str(
                psamples[s]
                * dbar.loc[idx, "fator_demanda_ativa"]
                * dbar.loc[idx, "fator_potencia"]
            )


def windf(
    dbar,
    dbarDF,
    wsamples,
    s,
):
    """fator de potência aplicado à estocasticidade da geração eólica

    Args
        dbar: DataFrame com as barras
        dbarDF: DataFrame com as barras
        wsamples: amostras da geração eólica
        s: amostra
    """

    import pandas as pd

    ## Inicialização
    for idx, value in dbarDF.iterrows():
        if (not pd.isna(dbar.loc[idx, "fator_eol"])) and "EOL" in value["nome"]:
            dbar.loc[idx, "potencia_ativa"] = str(
                round(wsamples[s] * dbar.loc[idx, "fator_eol"], 0)
            )
