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
            powerflow.maranhao,
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
        ],
        axis=0,
        ignore_index=True,
    )

    ## CODIGO PARA FILTRAGEM DE LINHAS DE INTERCONEXAO ENTRE REGIOES GEOELETRICAS DO SISTEMA ELETRICO BRASILEIRO
    # seco = concat([sudeste, centro,], axis=0, ignore_index=True)
    # seco_de = seco.rename(columns={"numero": "de"})
    # seco_para = seco.rename(columns={"numero": "para"})

    # sudeste_de = sudeste.rename(columns={"numero": "de"})
    # sudeste_para = sudeste.rename(columns={"numero": "para"})

    # nordeste_de = nordeste.rename(columns={"numero": "de"})
    # nordeste_para = nordeste.rename(columns={"numero": "para"})

    # fsene = merge(powerflow.dlinDF, sudeste_de, on="de")
    # fsene = merge(fsene, nordeste_para, on="para")

    # fnese = merge(powerflow.dlinDF, nordeste_de, on="de")
    # fnese = merge(fnese, sudeste_para, on="para")

    # fsecone = merge(powerflow.dlinDF, seco_de, on="de")
    # fsecone = merge(fsecone, nordeste_para, on="para")

    # fneseco = merge(powerflow.dlinDF, nordeste_de, on="de")
    # fneseco = merge(fneseco, seco_para, on="para")

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
        powerflow.dbarDF.nome.str.contains("UNE")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.uhe = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UHE")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.ute = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UTE")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.eol = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("EOL")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.ufv = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("UFV")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.pch = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("PCH")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.bio = powerflow.dbarDF.loc[
        powerflow.dbarDF.nome.str.contains("BIO")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]
    powerflow.gd = powerflow.dbarDF.loc[
        ~powerflow.dbarDF.nome.str.contains("UNE|UHE|UTE|EOL|UFV|PCH|BIO")
        & (powerflow.dbarDF.potencia_ativa > 0.0)
    ]

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
                        item.nome.str.contains("UNE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UNE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UHE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UHE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UHE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UTE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UTE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UTE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- EOL: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("EOL") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("EOL") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UFV: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UFV") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UFV") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- PCH: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("PCH") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("PCH") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- BIO: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("BIO") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("BIO") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- OTHER: {} unidades, {} MW".format(
                    item.loc[
                        ~item.nome.str.contains("UNE|UHE|UTE|EOL|UFV|PCH|BIO")
                        & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        ~item.nome.str.contains("UNE|UHE|UTE|EOL|UFV|PCH|BIO")
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
                        item.nome.str.contains("UNE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UNE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UHE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UHE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UHE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UTE: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UTE") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UTE") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- EOL: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("EOL") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("EOL") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- UFV: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("UFV") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("UFV") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- PCH: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("PCH") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("PCH") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- BIO: {} unidades, {} MW".format(
                    item.loc[
                        item.nome.str.contains("BIO") & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        item.nome.str.contains("BIO") & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")
            file.write(
                "        --- OTHER: {} unidades, {} MW".format(
                    item.loc[
                        ~item.nome.str.contains("UNE|UHE|UTE|EOL|UFV|PCH|BIO")
                        & (item.potencia_ativa > 0.0)
                    ].shape[0],
                    item.loc[
                        ~item.nome.str.contains("UNE|UHE|UTE|EOL|UFV|PCH|BIO")
                        & (item.potencia_ativa > 0.0)
                    ].potencia_ativa.sum(),
                )
            )
            file.write("\n\n")


def ne224(
    powerflow,
):
    """

    Args
        powerflow (_type_): _description_
    """
    ## Inicialização
    fronteira = powerflow.dbarDF.loc[
        (powerflow.dbarDF.potencia_reativa_minima == -9999)
        & (powerflow.dbarDF.potencia_reativa_maxima == 99999)
    ]

    alagoas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  2"]
    maceio = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 259]

    bahia = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  5"]
    camacari = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 284]

    ceara = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == "  6"]
    fortaleza = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 325]

    maranhao = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 10"]
    saoluis = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 332]

    paraiba = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 15"]
    joaopessoa = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 12999]

    pernambuco = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 16"]
    recife = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 241]

    piaui = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 17"]
    teresina = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 228]

    rio_grande_do_norte = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 20"]
    natal = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 346]

    sergipe = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == " 25"]
    aracaju = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 273]

    eolicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  2"]
    hidreletricas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  5"]
    termicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == "  7"]

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
        file.write(hidreletricas.to_string(index=False))
        file.write("\n\n")
        file.write("        --- UTE")
        file.write("\n")
        file.write(termicas.to_string(index=False))
        file.write("\n\n")
        file.write("        --- EOL")
        file.write("\n")
        file.write(eolicas.to_string(index=False))
        file.write("\n\n")
        file.write("    -- BARRAS")
        file.write("\n")
        file.write(str(powerflow.nbus))
        file.write("\n\n")
        file.write("    -- FRONTEIRA")
        file.write("\n")
        file.write(fronteira.to_string(index=False))
        file.write("\n\n")
        file.write("    -- LINHAS")
        file.write("\n")
        file.write(str(powerflow.nlin))
        file.write("\n\n")
        file.write("    -- ESTADOS")
        file.write("\n")
        file.write("        --- AL")
        file.write("\n")
        file.write(alagoas.to_string(index=False))
        file.write("\n")
        file.write("            ---- Maceio")
        file.write("\n")
        file.write(maceio.to_string(index=False))
        file.write("\n\n")
        file.write("        --- BA")
        file.write("\n")
        file.write(bahia.to_string(index=False))
        file.write("\n")
        file.write("            ---- Camacari")
        file.write("\n")
        file.write(camacari.to_string(index=False))
        file.write("\n\n")
        file.write("        --- CE")
        file.write("\n")
        file.write(ceara.to_string(index=False))
        file.write("\n")
        file.write("            ---- Fortaleza")
        file.write("\n")
        file.write(fortaleza.to_string(index=False))
        file.write("\n\n")
        file.write("        --- MA")
        file.write("\n")
        file.write(maranhao.to_string(index=False))
        file.write("\n")
        file.write("            ---- Sao Luis")
        file.write("\n")
        file.write(saoluis.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PB")
        file.write("\n")
        file.write(paraiba.to_string(index=False))
        file.write("\n")
        file.write("            ---- Joao Pessoa")
        file.write("\n")
        file.write(joaopessoa.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PE")
        file.write("\n")
        file.write(pernambuco.to_string(index=False))
        file.write("\n")
        file.write("            ---- Recife")
        file.write("\n")
        file.write(recife.to_string(index=False))
        file.write("\n\n")
        file.write("        --- PI")
        file.write("\n")
        file.write(piaui.to_string(index=False))
        file.write("\n")
        file.write("            ---- Teresina")
        file.write("\n")
        file.write(teresina.to_string(index=False))
        file.write("\n\n")
        file.write("        --- RN")
        file.write("\n")
        file.write(rio_grande_do_norte.to_string(index=False))
        file.write("\n")
        file.write("            ---- Natal")
        file.write("\n")
        file.write(natal.to_string(index=False))
        file.write("\n\n")
        file.write("        --- SE")
        file.write("\n")
        file.write(sergipe.to_string(index=False))
        file.write("\n")
        file.write("            ---- Aracaju")
        file.write("\n")
        file.write(aracaju.to_string(index=False))
