# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def q2024(
    powerflow,
):
    """

    Args:
        powerflow (_type_): _description_
    """
    from pandas import concat, merge

    ## Inicialização
    # Areas
    powerflow.rio_grande_sul = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([1, 2, 3, 4, 5, 6])
    ]
    powerflow.santa_catarina = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([51, 52, 53, 54])
    ]
    powerflow.parana = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([7, 101, 102, 103, 104, 105, 240, 241])
    ]
    powerflow.sul = concat(
        [powerflow.rio_grande_sul, powerflow.santa_catarina, powerflow.parana],
        axis=0,
        ignore_index=True,
    )

    powerflow.sao_paulo = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin(
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

    powerflow.rio_janeiro = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin(
            [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262]
        )
    ]
    powerflow.espirito_santo = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([301, 302, 303, 304, 305, 306, 307])
    ]
    powerflow.minas_gerais = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin(
            [351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363]
        )
    ]
    powerflow.sudeste = concat(
        [
            powerflow.sao_paulo,
            powerflow.rio_janeiro,
            powerflow.espirito_santo,
            powerflow.minas_gerais,
        ],
        axis=0,
        ignore_index=True,
    )

    powerflow.mato_grosso_sul = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([401, 402, 403, 404, 405])
    ]
    powerflow.mato_grosso = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin(
            [471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]
        )
    ]
    powerflow.goias = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([511, 512, 513, 514, 515, 516, 517, 518, 519, 520])
    ]
    powerflow.distrito_federal = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([561, 562, 563, 564])
    ]
    powerflow.centro = concat(
        [
            powerflow.mato_grosso_sul,
            powerflow.mato_grosso,
            powerflow.goias,
            powerflow.distrito_federal,
        ],
        axis=0,
        ignore_index=True,
    )
    powerflow.seco = concat(
        [
            powerflow.sudeste,
            powerflow.centro,
        ],
        axis=0,
        ignore_index=True,
    )

    powerflow.bahia = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([701, 702, 703, 704])
    ]
    powerflow.bahia_sergipe = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([711, 712, 713, 714, 715, 716])
    ]
    powerflow.alagoas_pernambuco = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([721, 722, 723, 724])
    ]
    powerflow.paraiba_rio_grande_norte = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([741, 742, 743, 744])
    ]
    powerflow.ceara = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([761, 762, 763, 764])
    ]
    powerflow.piaui = powerflow.dbarDF.loc[powerflow.dbarDF.area.isin([771, 772, 773])]
    powerflow.maranhao = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([222, 861, 862, 863, 864, 865, 866])
    ]
    powerflow.nordeste = concat(
        [
            powerflow.bahia,
            powerflow.bahia_sergipe,
            powerflow.alagoas_pernambuco,
            powerflow.paraiba_rio_grande_norte,
            powerflow.ceara,
            powerflow.piaui,
        ],
        axis=0,
        ignore_index=True,
    )

    powerflow.acre = powerflow.dbarDF.loc[powerflow.dbarDF.area.isin([431, 432, 433])]
    powerflow.amazonas = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([801, 802, 803, 804, 805, 806])
    ]
    powerflow.rondonia = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([451, 452, 453, 454, 455, 456, 457, 458, 459, 460])
    ]
    powerflow.roraima = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin(
            [471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482]
        )
    ]
    powerflow.amapa = powerflow.dbarDF.loc[powerflow.dbarDF.area.isin([821, 822])]
    powerflow.para = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([841, 842, 843, 844, 845, 846, 847, 848])
    ]
    powerflow.tocantins = powerflow.dbarDF.loc[
        powerflow.dbarDF.area.isin([581, 881, 882, 883])
    ]
    powerflow.norte = concat(
        [
            powerflow.acre,
            powerflow.amazonas,
            powerflow.rondonia,
            powerflow.roraima,
            powerflow.amapa,
            powerflow.para,
            powerflow.tocantins,
            powerflow.maranhao,
        ],
        axis=0,
        ignore_index=True,
    )

    # # CODIGO PARA FILTRAGEM DE LINHAS DE INTERCONEXAO ENTRE REGIOES GEOELETRICAS DO SISTEMA ELETRICO BRASILEIRO
    # seco = concat([powerflow.sudeste, powerflow.centro,], axis=0, ignore_index=True)
    # seco_de = seco.rename(columns={"numero": "de"})
    # seco_para = seco.rename(columns={"numero": "para"})

    # nordeste_de = powerflow.nordeste.rename(columns={"numero": "de"})
    # nordeste_para = powerflow.nordeste.rename(columns={"numero": "para"})

    # norte_de = powerflow.norte.rename(columns={"numero": "de"})
    # norte_para = powerflow.norte.rename(columns={"numero": "para"})

    # # SECO <-> NORDESTE
    # secone = merge(powerflow.dlinDF, seco_de, on="de")
    # secone = merge(secone, nordeste_para, on="para")
    # neseco = merge(powerflow.dlinDF, nordeste_de, on="de")
    # neseco = merge(neseco, seco_para, on="para")
    # print("INTERLIGACAO SECO-NORDESTE")
    # print(secone[["de", "para", "circuito", "area_x", "area_y",]])
    # print(neseco[["de", "para", "circuito", "area_x", "area_y",]])

    # # NORTE <-> NORDESTE
    # nne = merge(powerflow.dlinDF, norte_de, on="de")
    # nne = merge(nne, nordeste_para, on="para")
    # nen = merge(powerflow.dlinDF, nordeste_de, on="de")
    # nen = merge(nen, norte_para, on="para")
    # print("INTERLIGACAO NORTE-NORDESTE")
    # print(nne[["de", "para", "circuito", "area_x", "area_y",]])
    # print(nen[["de", "para", "circuito", "area_x", "area_y",]])

    powerflow.estados = {
        "RS": powerflow.rio_grande_sul,
        "SC": powerflow.santa_catarina,
        "PR": powerflow.parana,
        "SP": powerflow.sao_paulo,
        "RJ": powerflow.rio_janeiro,
        "ES": powerflow.espirito_santo,
        "MG": powerflow.minas_gerais,
        "MS": powerflow.mato_grosso_sul,
        "MT": powerflow.mato_grosso,
        "GO": powerflow.goias,
        "DF": powerflow.distrito_federal,
        "BA": powerflow.bahia,
        "BA/SE": powerflow.bahia_sergipe,
        "AL/PE": powerflow.alagoas_pernambuco,
        "PB/RN": powerflow.paraiba_rio_grande_norte,
        "CE": powerflow.ceara,
        "PI": powerflow.piaui,
        "MA": powerflow.maranhao,
        "PA": powerflow.para,
        "AP": powerflow.amapa,
        "AM": powerflow.amazonas,
        "RR": powerflow.roraima,
        "RO": powerflow.rondonia,
        "AC": powerflow.acre,
        "TO": powerflow.tocantins,
    }

    powerflow.regioes = {
        "S": powerflow.sul,
        "SECO": powerflow.seco,
        "NE": powerflow.nordeste,
        "N": powerflow.norte,
    }

    powerflow.geracao_total = powerflow.dbarDF.potencia_ativa.sum()
    powerflow.une = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UNE|UN-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
        & (powerflow.dbarDF.tipo != 0)
    ]
    powerflow.uhe = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UHE|UH-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
        & (powerflow.dbarDF.tipo != 0)
    ]
    powerflow.ute = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UTE|UT-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
        & (powerflow.dbarDF.tipo != 0)
    ]
    powerflow.eol = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("EOL|EO-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.ufv = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UFV|UF-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.pch = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("PCH|PC-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.bio = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("BIO|BI-")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.gd = powerflow.dbarDF.loc[
        ~powerflow.dbarDF.nome.str.contains(
            "UNE|UHE|UTE|EOL|UFV|PCH|BIO|UN-|UH-|UT-|EO-|UF-|PC-|BI-"
        )
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.carga_total = powerflow.dbarDF.demanda_ativa.sum()
    powerflow.cargas = powerflow.dbarDF.loc[powerflow.dbarDF.tipo == 0]

    # AREA REPORT
    filename = powerflow.infofolder + powerflow.name + ".txt"
    with open(filename, "w") as file:
        file.write("- FULL SYSTEM REPORT")
        file.write("\n\n")
        file.write(
            "    -- GERADORES: {} unidades, {} MW".format(
                (powerflow.dbarDF.potencia_ativa > 0).sum(), powerflow.geracao_total
            )
        )
        file.write("\n\n")
        file.write(
            "        --- UNE: {} unidades, {} MW".format(
                powerflow.une.shape[0], powerflow.une.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.une.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- UHE: {} unidades, {} MW".format(
                powerflow.uhe.shape[0], powerflow.uhe.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.uhe.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- UTE: {} unidades, {} MW".format(
                powerflow.ute.shape[0], powerflow.ute.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.ute.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- EOL: {} unidades, {} MW".format(
                powerflow.eol.shape[0], powerflow.eol.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.eol.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- UFV: {} unidades, {} MW".format(
                powerflow.ufv.shape[0], powerflow.ufv.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.ufv.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- PCH: {} unidades, {} MW".format(
                powerflow.pch.shape[0], powerflow.pch.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.pch.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- BIO: {} unidades, {} MW".format(
                powerflow.bio.shape[0], powerflow.bio.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.bio.to_string(index=False))
        file.write("\n\n")
        file.write(
            "        --- OTHER: {} unidades, {} MW".format(
                powerflow.gd.shape[0], powerflow.gd.potencia_ativa.sum()
            )
        )
        file.write("\n")
        file.write(powerflow.gd.to_string(index=False))
        file.write("\n\n")

        file.write("\n\n")
        file.write("- STATE REPORT")
        for key, item in powerflow.estados.items():
            geradores = item.loc[item.potencia_ativa > 0.0]
            file.write("\n")
            file.write("    -- {}".format(key))
            file.write("\n")
            file.write(
                "        --- GERADORES: {} unidades, {} MW".format(
                    geradores.shape[0], geradores.potencia_ativa.sum()
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UNE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UNE|UN-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UNE|UN-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UHE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UHE|UH-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UHE|UH-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UTE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UTE|UT-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UTE|UT-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- EOL: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("EOL|EO-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("EOL|EO-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UFV: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UFV|UF-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UFV|UF-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- PCH: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("PCH|PC-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("PCH|PC-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- BIO: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("BIO|BI-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("BIO|BI-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- OTHER: {} unidades, {} MW".format(
                    item.loc[
                        ~item.nome.str.contains(
                            "UNE|UHE|UTE|EOL|UFV|PCH|BIO|UN-|UH-|UT-|EO-|UF-|PC-|BI-"
                        )
                        & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        ~item.nome.str.contains(
                            "UNE|UHE|UTE|EOL|UFV|PCH|BIO|UN-|UH-|UT-|EO-|UF-|PC-|BI-"
                        )
                        & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")

        file.write("\n\n")
        file.write("- SUBREGION REPORT")
        for key, item in powerflow.regioes.items():
            geradores = item.loc[item.potencia_ativa > 0.0]
            file.write("\n")
            file.write("    -- {}".format(key))
            file.write("\n")
            file.write(
                "        --- GERADORES: {} unidades, {} MW".format(
                    geradores.shape[0], geradores.potencia_ativa.sum()
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UNE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UNE|UN-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UNE|UN-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UHE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UHE|UH-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UHE|UH-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UTE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UTE|UT-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UTE|UT-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- EOL: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("EOL|EO-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("EOL|EO-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UFV: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UFV|UF-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UFV|UF-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- PCH: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("PCH|PC-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("PCH|PC-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- BIO: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("BIO|BI-") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("BIO|BI-") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- OTHER: {} unidades, {} MW".format(
                    item.loc[
                        ~item.nome.str.contains(
                            "UNE|UHE|UTE|EOL|UFV|PCH|BIO|UN-|UH-|UT-|EO-|UF-|PC-|BI-"
                        )
                        & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        ~item.nome.str.contains(
                            "UNE|UHE|UTE|EOL|UFV|PCH|BIO|UN-|UH-|UT-|EO-|UF-|PC-|BI-"
                        )
                        & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")

    powerflow.cargas = powerflow.sao_paulo.copy()
    powerflow.eolicas = powerflow.nordeste[
        powerflow.nordeste.nome.str.contains("EOL|EO-")
    ].copy()


def ne224(
    powerflow,
):
    """

    Args
        powerflow (_type_): _description_
    """
    ## Inicialização
    powerflow.fronteira = powerflow.dbarDF.loc[
        (powerflow.dbarDF.potencia_reativa_minima == -9999)
        & (powerflow.dbarDF.potencia_reativa_maxima == 99999)
    ]

    powerflow.alagoas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  2"]
    powerflow.maceio = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 259]

    powerflow.bahia = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  5"]
    powerflow.camacari = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 284]

    powerflow.ceara = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  6"]
    powerflow.fortaleza = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 325]

    powerflow.maranhao = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 10"]
    powerflow.saoluis = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 332]

    powerflow.paraiba = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 15"]
    powerflow.joaopessoa = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 12999]

    powerflow.pernambuco = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 16"]
    powerflow.recife = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 241]

    powerflow.piaui = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 17"]
    powerflow.teresina = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 228]

    powerflow.rio_grande_do_norte = powerflow.dbarDF.loc[
        powerflow.dbarDF.agreg1 == " 20"
    ]
    powerflow.natal = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 346]

    powerflow.sergipe = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 25"]
    powerflow.aracaju = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 273]

    powerflow.eolicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  2"]
    powerflow.hidreletricas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  5"]
    powerflow.termicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  7"]
    powerflow.cargas = powerflow.dbarDF.loc[powerflow.dbarDF.tipo == 0]

    # AREA REPORT
    filename = powerflow.infofolder + powerflow.name + ".txt"
    with open(filename, "w") as file:
        file.write("- AREA REPORT")
        file.write("\n\n")
        file.write("    -- GERADORES")
        file.write("\n")
        file.write(str(powerflow.nger))
        file.write("\n\n")
        file.write("        --- UHE")
        file.write("\n")
        file.write(powerflow.hidreletricas.to_string(index=False))
        file.write("\n\n")
        file.write("        --- UTE")
        file.write("\n")
        file.write(powerflow.termicas.to_string(index=False))
        file.write("\n\n")
        file.write("        --- EOL")
        file.write("\n")
        file.write(powerflow.eolicas.to_string(index=False))
        file.write("\n\n")
        file.write("    -- BARRAS")
        file.write("\n")
        file.write(str(powerflow.nbus))
        file.write("\n\n")
        file.write("    -- FRONTEIRA")
        file.write("\n")
        file.write(powerflow.fronteira.to_string(index=False))
        file.write("\n\n")
        file.write("    -- LINHAS")
        file.write("\n")
        file.write(str(powerflow.nlin))
        file.write("\n\n")
        file.write("    -- ESTADOS")
        file.write("\n")
        file.write("        --- AL")
        file.write("\n")
        file.write(powerflow.alagoas.to_string(index=False))
        file.write("\n")
        file.write("            ---- Maceio")
        file.write("\n")
        file.write(powerflow.maceio.to_string(index=False))
        file.write("\n\n")
        file.write("        --- BA")
        file.write("\n")
        file.write(powerflow.bahia.to_string(index=False))
        file.write("\n")
        file.write("            ---- Camacari")
        file.write("\n")
        file.write(powerflow.camacari.to_string(index=False))
        file.write("\n\n")
        file.write("        --- CE")
        file.write("\n")
        file.write(powerflow.ceara.to_string(index=False))
        file.write("\n")
        file.write("            ---- Fortaleza")
        file.write("\n")
        file.write(powerflow.fortaleza.to_string(index=False))
        file.write("\n\n")
        file.write("        --- MA")
        file.write("\n")
        file.write(powerflow.maranhao.to_string(index=False))
        file.write("\n")
        file.write("            ---- Sao Luis")
        file.write("\n")
        file.write(powerflow.saoluis.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PB")
        file.write("\n")
        file.write(powerflow.paraiba.to_string(index=False))
        file.write("\n")
        file.write("            ---- Joao Pessoa")
        file.write("\n")
        file.write(powerflow.joaopessoa.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PE")
        file.write("\n")
        file.write(powerflow.pernambuco.to_string(index=False))
        file.write("\n")
        file.write("            ---- Recife")
        file.write("\n")
        file.write(powerflow.recife.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PI")
        file.write("\n")
        file.write(powerflow.piaui.to_string(index=False))
        file.write("\n")
        file.write("            ---- Teresina")
        file.write("\n")
        file.write(powerflow.teresina.to_string(index=False))
        file.write("\n\n")
        file.write("        --- RN")
        file.write("\n")
        file.write(powerflow.rio_grande_do_norte.to_string(index=False))
        file.write("\n")
        file.write("            ---- Natal")
        file.write("\n")
        file.write(powerflow.natal.to_string(index=False))
        file.write("\n\n")
        file.write("        --- SE")
        file.write("\n")
        file.write(powerflow.sergipe.to_string(index=False))
        file.write("\n")
        file.write("            ---- Aracaju")
        file.write("\n")
        file.write(powerflow.aracaju.to_string(index=False))
