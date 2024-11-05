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

    ## Inicialização
    # Areas
    allareas = powerflow.dbarDF.area.unique().sort_values()
    generation_types = ["UNE", "UHE", "UTE", "EOL", "UFV", "PCH", "BIO", "OTHER", "TOTAL",]

    generation = {area: 0 for area in allareas}
    demand = {area: 0 for area in allareas}
    buses = {area: 0 for area in allareas}

    stateareas_number = {area: {generation_type: 0 for generation_type in generation_types} for area in allareas}
    stateareas_generation = {area: {generation_type: 0 for generation_type in generation_types} for area in allareas}
    stateareas_demand = {area: 0 for area in allareas}
    stateareas_buses = {area: 0 for area in allareas}

    # State Areas
    stateareas = {
    'rsareas': [1, 2, 3, 4, 5, 6,],
    'scareas': [51, 52, 53, 54,],
    'prareas': [7, 101, 102, 103, 104, 105, 240, 241,],
    'spareas': [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217,],
    'rjareas': [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262,],
    'esareas': [301, 302, 303, 304, 305, 306, 307,],
    'mgareas': [351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363,],
    'msareas': [401, 402, 403, 404, 405,],
    'acareas': [431, 432, 433,],
    'roareas': [451, 452, 453, 454, 455, 456, 457, 458, 459, 460,],
    'mtareas': [471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482,],
    'goareas': [511, 512, 513, 514, 515, 516, 517, 518, 519, 520,],
    'dfareas': [561, 562, 563, 564,],
    'toareas': [581, 881, 882, 883,],
    'baareas': [701, 702, 703, 704,],
    'baseareas': [711, 712, 713, 714, 715, 716,],
    'alpeareas': [721, 722, 723, 724,],
    'pbrnareas': [741, 742, 743, 744,],
    'ceareas': [761, 762, 763, 764,],
    'piareas': [771, 772, 773,],
    'amareas': [801, 802, 803, 804, 805, 806,],
    'apareas': [821, 822,],
    'paareas': [841, 842, 843, 844, 845, 846, 847, 848,],
    'maareas': [222, 861, 862, 863, 864, 865, 866,],
    }

    # DBAR DATA
    dbar_other = list() 

    for idx, value in powerflow.dbarDF.iterrows():
        generation[value.area] += value.potencia_ativa
        demand[value.area] += value.demanda_ativa
        buses[value.area] += 1
        if "UNE" in value.nome:
           stateareas_number[value.area]["UNE"] += 1
           stateareas_generation[value.area]["UNE"] += value.potencia_ativa
           stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "UHE" in value.nome:
            stateareas_number[value.area]["UHE"] += 1
            stateareas_generation[value.area]["UHE"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "UTE" in value.nome:
            stateareas_number[value.area]["UTE"] += 1
            stateareas_generation[value.area]["UTE"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "EOL" in value.nome:
            stateareas_number[value.area]["EOL"] += 1
            stateareas_generation[value.area]["EOL"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "UFV" in value.nome:
            stateareas_number[value.area]["UFV"] += 1
            stateareas_generation[value.area]["UFV"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "PCH" in value.nome:
            stateareas_number[value.area]["PCH"] += 1
            stateareas_generation[value.area]["PCH"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif "BIO" in value.nome:
            stateareas_number[value.area]["BIO"] += 1
            stateareas_generation[value.area]["BIO"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa
        elif value.potencia_ativa > 0. and any(gt not in value.nome for gt in generation_types):
            dbar_other.append(value.nome)
            stateareas_number[value.area]["OTHER"] += 1
            stateareas_generation[value.area]["OTHER"] += value.potencia_ativa
            stateareas_generation[value.area]["TOTAL"] += value.potencia_ativa

    # DGER DATA
    dger = 0
    dger_UNE = 0
    dger_UHE = 0
    dger_UTE = 0
    dger_EOL = 0
    dger_UFV = 0
    dger_PCH = 0
    dger_BIO = 0
    dger_OTHER = 0
    dger_other = list()

    for idx, value in powerflow.dgerDF.iterrows():
        [nome, area] = powerflow.dbarDF.loc[powerflow.dbarDF.numero == value.numero, ["nome", "area"]].values.tolist()[0]
        if "UNE" in nome:
            dger_UNE += 1
        elif "UHE" in nome:
            dger_UHE += 1
        elif "UTE" in nome:
            dger_UTE += 1
        elif "EOL" in nome:
            dger_EOL += 1
        elif "UFV" in nome:
            dger_UFV += 1
        elif "PCH" in nome:
            dger_PCH += 1
        elif "BIO" in nome:
            dger_BIO += 1
        else:
            dger_other.append(nome)
            dger_OTHER += 1

        dger += 1
        
    # AREA REPORT
    filename = powerflow.infofolder + powerflow.name + "-areas.txt"
    with open(filename, "w") as file:
        file.write("AREA REPORT\n")
        file.write("\n")
        file.write("GERACAO\n")
        file.write("AREA;GERACAO;DEMANDA;BARRAS\n")
        for area in allareas:
            file.write(f"{area};{generation[area]};{demand[area]};{buses[area]}\n")
        file.write("\n")
        file.write("GERACAO POR TIPO\n")
        file.write("AREA;UNE;UHE;UTE;EOL;UFV;PCH;BIO;OTHER;TOTAL\n")
        for area in allareas:
            file.write(f"{area};{stateareas_generation[area]['UNE']};{stateareas_generation[area]['UHE']};{stateareas_generation[area]['UTE']};{stateareas_generation[area]['EOL']};{stateareas_generation[area]['UFV']};{stateareas_generation[area]['PCH']};{stateareas_generation[area]['BIO']};{stateareas_generation[area]['OTHER']};{stateareas_generation[area]['TOTAL']}\n")
        file.write("\n")
        file.write("GERACAO POR NUMERO DE USINAS\n")
        file.write("AREA;UNE;UHE;UTE;EOL;UFV;PCH;BIO;OTHER;TOTAL\n")
        for area in allareas:
            file.write(f"{area};{stateareas_number[area]['UNE']};{stateareas_number[area]['UHE']};{stateareas_number[area]['UTE']};{stateareas_number[area]['EOL']};{stateareas_number[area]['UFV']};{stateareas_number[area]['PCH']};{stateareas_number[area]['BIO']};{stateareas_number[area]['OTHER']};{stateareas_buses[area]}\n")
        file.write("\n")
        file.write("GERACAO POR TIPO DE USINA\n")
        file.write("AREA;UNE;UHE;UTE;EOL;UFV;PCH;BIO;OTHER;TOTAL\n")
        # for area in allareas:
        #     file.write(f"{area};{stateareas_number[area]['UNE']};{stateareas_number[area]['UHE']};{stateareas_number


    
def ne224(
    powerflow,
):
    """	

    Args
        powerflow (_type_): _description_
    """

    ## Inicialização
    fronteira = powerflow.dbarDF.loc[(powerflow.dbarDF.potencia_reativa_minima == -9999) & (powerflow.dbarDF.potencia_reativa_maxima == 99999)]

    alagoas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == '  2']
    maceio = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 259]

    bahia = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == '  5']
    camacari = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 284]

    ceara = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == '  6']
    fortaleza = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 325]

    maranhao = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 10']
    saoluis = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 332]

    paraiba = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 15']
    joaopessoa = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 12999]

    pernambuco = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 16']
    recife = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 241]

    piaui = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 17']
    teresina = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 228]

    rio_grande_do_norte = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 20']
    natal = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 346]

    sergipe = powerflow.dbarDF.loc[powerflow.dbarDF.agreg1 == ' 25']
    aracaju = powerflow.dbarDF.loc[powerflow.dbarDF.numero == 273]

    eolicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == '  2']
    hidreletricas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == '  5']
    termicas = powerflow.dbarDF.loc[powerflow.dbarDF.agreg4 == '  7']


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

        


    print()