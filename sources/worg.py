# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import cdufolder
from os.path import realpath
import re
from numpy import exp


def worg(
    anarede,
    anatem,
    organon,
):
    """Inicialização

    Args
        anatem:
    """
    ## Inicialização    
    anatemfiles = list()
    organonfiles = list()
    cdupath = cdufolder(anarede,)

    for key in anatem.dcdu.keys():
        if key in [
            "dctg",
            "ncdu_ruler",
            "defpar_ruler",
            "bloco_ruler",
            "defval_ruler",
        ]:
            continue

        if "AVR" in anatem.dcdu[key]["nome"].strip():
            nome = "AVR" + key
        elif "PSS" in anatem.dcdu[key]["nome"].strip():
            nome = "PSS" + str(900 + int(key))
        elif "WT3" in anatem.dcdu[key]["nome"].strip():
            nome = "WT3" + key
        elif "PV" in anatem.dcdu[key]["nome"].strip():
            nome = "PV" + key
        else:
            break      

        # ======================================================
        # OPEN CDU FILE (LOSSLESS WRITE)
        # ======================================================
        cdufile = realpath(cdupath + nome + ".cdu")
        udcfile = realpath(cdupath + nome + ".udc")
        anatem.file = open(cdufile, "w", encoding="latin-1")
        anatem.file.write("DCDU\n")
        anatem.file.write("(ncdu) ( nome cdu )\n")

        # ======================================================
        # UDC / ORGANON GENERATION (UNCHANGED LOGIC)
        # ======================================================

        if "AVR" in nome:
            organon.file = open(udcfile, "w", encoding="latin-1")
            organon.file.write(f"UDC AVR {key} 1 {nome} '@joaoppeters'\n")
            organon.file.write("OUT EFD\n")

        elif "PSS" in nome:
            number = int(key) + 900
            nome = "PSS" + str(number)
            udcfile = realpath(cdupath + nome + ".udc")
            organon.file = open(udcfile, "w", encoding="latin-1")
            organon.file.write(f"UDC PSS {number} 1 {nome} '@joaoppeters'\n")
            organon.file.write("OUT VPSS\n")

        elif "WT3" in nome or "PV" in nome:
            organon.file = open(udcfile, "w", encoding="latin-1")
            organon.file.write(f"UDC RNG {key} 2 {nome} '@joaoppeters'\n")
            organon.file.write("OUT ITRFNT ITIFNT\n")

        # semantic counters
        i_defpar, i_defval, ia_bloco, io_bloco = 0, 0, 0, 0
        # flag block 
        b = 0
        # terms counter for multi-input blocks
        terms = 1

        # ------------------------------------------------------
        # LOSSLESS WRITE FROM RAW TABLE
        # ------------------------------------------------------
        for entry in anatem.dcdu_raw:
            print(entry)
            if entry["ncdu"] not in (None, key):
                continue

            kind = entry["kind"]

            # comments and blanks
            if kind in ("comment", "blank") and entry["ncdu"] == key:
                anatem.file.write(entry["raw"] + "\n")
                organon.file.write("!" + entry["raw"] + "\n")
                continue

            # ncdu header
            if kind == "ncdu" and entry["ncdu"] == key:
                anatem.file.write(entry["raw"] + "\n")
                organon.file.write("!" + entry["raw"] + "\n")
                continue

            # DEFPAR
            if kind == "defpar":
                anatem.file.write(
                    f"{anatem.dcdu[key]['defpar'][i_defpar]:>6} "
                    f"{anatem.dcdu[key]['defpar_nome'][i_defpar]:>6} "
                    f"{anatem.dcdu[key]['defpar_valor'][i_defpar]:>18}\n"
                )
                organon.file.write(
                    f"{anatem.dcdu[key]['defpar_nome'][i_defpar].strip():<6} = "
                    f"PARAM({anatem.dcdu[key]['defpar_valor'][i_defpar]:>18})\n",
                )
                i_defpar += 1
                continue

            # DEFVAL
            if kind == "defval":
                anatem.file.write(
                    f"{anatem.dcdu[key]['defval'][i_defval]:>6} "
                    f"{anatem.dcdu[key]['defval_subtipo'][i_defval]:>6} "
                    f"{anatem.dcdu[key]['defval_variavel'][i_defval]:>6} "
                    f"{anatem.dcdu[key]['defval_parametro_d1'][i_defval]:>6}"
                    f"{anatem.dcdu[key]['defval_exclusao'][i_defval]:1}"
                    f"{anatem.dcdu[key]['defval_parametro_d2'][i_defval]:>6}\n"
                )
                
                try:
                    float(anatem.dcdu[key]['defval_parametro_d1'][i_defval])
                    organon.file.write(
                        f"{anatem.dcdu[key]['defval_variavel'][i_defval].strip():<6} = "
                        f"CONST({anatem.dcdu[key]['defval_parametro_d1'][i_defval]:>18})\n",
                    )
                except:
                    if "#" in anatem.dcdu[key]['defval_parametro_d1'][i_defval]:
                        defval_variable = anatem.dcdu[key]['defval_parametro_d1'][i_defval]
                        for j, defpar_nome in enumerate(anatem.dcdu[key]['defpar_nome']):
                            if defpar_nome.strip() == defval_variable: 
                                defval_value = anatem.dcdu[key]['defpar_valor'][j]

                        organon.file.write(
                            f"{anatem.dcdu[key]['defval_variavel'][i_defval].strip():<6} = "
                            f"CONST({defval_value:>18})\n",
                        )
                    else:
                        organon.file.write(
                            f"{anatem.dcdu[key]['defval_variavel'][i_defval].strip():<6} = "
                            f"INIT({anatem.dcdu[key]['defval_parametro_d1'][i_defval]:>18})\n",
                        )

                i_defval += 1
                continue

            # BLOCO
            if kind == "bloco":
                if not b:
                    dtdelay = 'TMSTP'
                    organon.file.write(f"{dtdelay:<6} =INPSTEP()\n")
                    b = 1
                anatem.file.write(
                    f"{anatem.dcdu[key]['bloco_numero'][ia_bloco]:>4}"
                    f"{anatem.dcdu[key]['bloco_inicializacao'][ia_bloco]:1}"
                    f"{anatem.dcdu[key]['bloco_tipo'][ia_bloco]:>6}"
                    f"{anatem.dcdu[key]['bloco_omitir'][ia_bloco]:1}"
                    f"{anatem.dcdu[key]['bloco_subtipo'][ia_bloco]:>6}"
                    f"{anatem.dcdu[key]['bloco_sinal'][ia_bloco]:1}"
                    f"{anatem.dcdu[key]['bloco_entrada'][ia_bloco]:>6} "
                    f"{anatem.dcdu[key]['bloco_saida'][ia_bloco]:>6} "
                    f"{anatem.dcdu[key]['bloco_parametro1'][ia_bloco]:>6}"
                    f"{anatem.dcdu[key]['bloco_parametro2'][ia_bloco]:>6}"
                    f"{anatem.dcdu[key]['bloco_parametro3'][ia_bloco]:>6}"
                    f"{anatem.dcdu[key]['bloco_parametro4'][ia_bloco]:>6} "
                    f"{anatem.dcdu[key]['bloco_limite_minimo'][ia_bloco]:>6} "
                    f"{anatem.dcdu[key]['bloco_limite_maximo'][ia_bloco]:>6}\n"
                )
                # if io_bloco >= len(anatem.dcdu[key]['bloco_numero']):
                if terms > 1:
                    terms -= 1
                    ia_bloco += 1
                    continue

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'ENTRAD' and \
                    anatem.dcdu[key]['bloco_saida'][io_bloco] not in anatem.dcdu[key]['defpar_nome'] and \
                        anatem.dcdu[key]['bloco_saida'][io_bloco] not in anatem.dcdu[key]['defval_variavel']:
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =REF(0.0)\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'VTR':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}    =INPGVC()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'VSAD':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INPPSS()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'WMAQ':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}    =INPGW()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'PTFNT':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INPWMW()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'QTFNT':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INPWMVAR()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'VOLT':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INPGVT()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'ANGL':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INPVANG()\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'PBSIS':
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}  =INIT(100.)\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'IMPORT' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'DT':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida}    =CONST({dtdelay})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.GT.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =GT({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.LT.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =LT({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.GE.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =GE({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.LE.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =LE({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.EQ.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =EQ({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'COMPAR' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NE.':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NE({entrada[0]}, {entrada[1]})\n")
                    terms += 1

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'DIVSAO':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    if terms == 2:
                        entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                        saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                        organon.file.write(f"{saida:<6} =DIVIDE({entrada[0]}, {entrada[1]})\n")
                        io_bloco += 1
                    else:
                        saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                        organon.file.write(f"{saida:<6} =DIVIDEM(0.0, 1.0, ")
                        for j in range(terms):
                            entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                            if j < terms - 1:
                                organon.file.write(f"{entrada}, ")
                            else:
                                organon.file.write(f"{entrada})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FRACAO':
                    num = anatem.dcdu[key]['bloco_parametro1'][io_bloco] or anatem.dcdu[key]['bloco_parametro2'][io_bloco]
                    den = anatem.dcdu[key]['bloco_parametro3'][io_bloco] or anatem.dcdu[key]['bloco_parametro4'][io_bloco]
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =FRAC({entrada}, {num}, {den})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'COS':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =COS({entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'SIN':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =SIN({entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'DEADB1':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    abcd = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco], anatem.dcdu[key]['bloco_parametro4'][io_bloco]]
                    organon.file.write(f"{saida:<6} =DDBND3({entrada}, {abcd[0]}, {abcd[1]})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'DEADB2':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    abcd = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco], anatem.dcdu[key]['bloco_parametro4'][io_bloco]]
                    organon.file.write(f"{saida:<6} =DDBND4({entrada}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'PONTOS':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    organon.file.write(f"{saida:<6} =LFPP({entrada}, ")
                    for j in range(terms):
                        ponto_x = anatem.dcdu[key]['bloco_parametro1'][io_bloco + j]
                        ponto_y = anatem.dcdu[key]['bloco_parametro2'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{ponto_x}, {ponto_y}, ")
                        else:
                            organon.file.write(f"{ponto_x}, {ponto_y})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'X**2':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =SQR({entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'SQRT':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =SQRT({entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'MENOS':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =GAIN(0.0, {entrada}, -1.0)\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'FUNCAO' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == 'RAMPA':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    abcd = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco], anatem.dcdu[key]['bloco_parametro4'][io_bloco]]
                    organon.file.write(f"{saida:<6} =RAMP({saida}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'GANHO':
                    a = anatem.dcdu[key]['bloco_parametro1'][io_bloco]
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =GAIN(0.0, {entrada}, {a})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LEDLAG':
                    abcd = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco], anatem.dcdu[key]['bloco_parametro4'][io_bloco]]
                    abcd = ['0' if item == '' else item for item in abcd]
                    xn = [anatem.dcdu[key]['bloco_limite_maximo'][io_bloco], anatem.dcdu[key]['bloco_limite_minimo'][io_bloco]]
                    xn = ['99.99', '-99.99'] if xn == ['', ''] else xn
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =COMP6(0.0, {entrada}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]}, {xn[0]}, {xn[1]})\n")
                
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LIMITA':
                    xn = [anatem.dcdu[key]['bloco_limite_maximo'][io_bloco], anatem.dcdu[key]['bloco_limite_minimo'][io_bloco]]
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =LIMIT(0.0, {entrada}, #{xn[0]}, #{xn[1]})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.AND.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =AND( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.OR.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =OR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.XOR.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =XOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NOT.':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NOT({entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NAND.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NAND( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NOR.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NXOR.':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NXOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'LOGIC' and anatem.dcdu[key]['bloco_subtipo'][io_bloco] == '.NOT.':
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =NOT({entrada})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'MAX':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =MAX({entrada[0]}, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1                   
                
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'MIN':                    
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =MIN({entrada[0]}, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1                   
                                
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'MULTPL':
                    try:
                        while anatem.dcdu[key]['bloco_tipo'][io_bloco + terms] == '':
                            terms += 1
                    except:
                        pass
                    if terms == 2:
                        entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                        saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                        organon.file.write(f"{saida:<6} =MULT({entrada[0]}, {entrada[1]})\n")
                        io_bloco += 1
                    else:
                        saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                        organon.file.write(f"{saida:<6} =MULTM(0.0, 1.0, ")
                        for j in range(terms):
                            entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco + j]
                            if j < terms - 1:
                                organon.file.write(f"{entrada}, ")
                            else:
                                organon.file.write(f"{entrada})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'PROINT':
                    abc = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco]]
                    abc = ['0' if item == '' else item for item in abc]
                    xn = [anatem.dcdu[key]['bloco_limite_maximo'][io_bloco], anatem.dcdu[key]['bloco_limite_minimo'][io_bloco]]
                    xn = ['99.99', '-99.99'] if xn == ['', ''] else xn
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =COMP6(0.0, {entrada}, {abc[0]}, {abc[1]}, {abc[2]}, {0.0}, {xn[0]}, {xn[1]})\n")

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'SELET2':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1], anatem.dcdu[key]['bloco_entrada'][io_bloco+2]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =SEL({entrada[0]}, {entrada[1]}, {entrada[2]}, 0.0)\n")
                    terms = 3
                    io_bloco += 2

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'SOMA' and anatem.dcdu[key]['bloco_tipo'][io_bloco+2] == '':
                    sinal = [anatem.dcdu[key]['bloco_sinal'][io_bloco], anatem.dcdu[key]['bloco_sinal'][io_bloco+1], anatem.dcdu[key]['bloco_sinal'][io_bloco+2]]
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1], anatem.dcdu[key]['bloco_entrada'][io_bloco+2]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =ADD({sinal[0]}1.0, {entrada[0]}, {sinal[1]}1.0, {entrada[1]}, {sinal[2]}1.0, {entrada[2]})\n")
                    terms = 3
                    io_bloco += 2
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'SOMA' and anatem.dcdu[key]['bloco_tipo'][io_bloco+1] == '':
                    sinal = [anatem.dcdu[key]['bloco_sinal'][io_bloco], anatem.dcdu[key]['bloco_sinal'][io_bloco+1]]
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =ADD({sinal[0]}1.0, {entrada[0]}, {sinal[1]}1.0, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1
                
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'T/HOLD':
                    entrada = [anatem.dcdu[key]['bloco_entrada'][io_bloco], anatem.dcdu[key]['bloco_entrada'][io_bloco+1]]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =THOLD({entrada[0]}, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1

                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'WSHOUT':
                    abc = [anatem.dcdu[key]['bloco_parametro1'][io_bloco], anatem.dcdu[key]['bloco_parametro2'][io_bloco], anatem.dcdu[key]['bloco_parametro3'][io_bloco]]
                    xn = [anatem.dcdu[key]['bloco_limite_maximo'][io_bloco], anatem.dcdu[key]['bloco_limite_minimo'][io_bloco]]
                    xn = ['99.99', '-99.99'] if xn == ['', ''] else xn
                    entrada = anatem.dcdu[key]['bloco_entrada'][io_bloco]
                    saida = anatem.dcdu[key]['bloco_saida'][io_bloco]
                    organon.file.write(f"{saida:<6} =COMP6(0.0, {entrada}, {0.0}, {abc[0]}, {abc[1]}, {abc[2]}, {xn[0]}, {xn[1]})\n")
        
                if anatem.dcdu[key]['bloco_tipo'][io_bloco] == 'EXPORT':
                    pass

                ia_bloco += 1
                io_bloco += 1
                continue

            # FIMCDU
            if kind == "fimcdu":
                anatem.file.write("FIMCDU\n")
                anatem.file.write("999999\n")
                anatem.file.close()
                organon.file.write("!\n")
                organon.file.write("END\n")
                organon.file.close()
                break

        anatemfiles.append(cdufile)
        organonfiles.append(udcfile)
    
    # Arquivo
    organon.filedir = realpath(
        anarede.maindir + "\\sistemas\\" + anarede.name + ".dyn",
    )

    # Manipulacao
    organon.file = open(organon.filedir, "w")
    wdsm(
        anarede=anarede,
        anatem=anatem,
        organon=organon,
        anatemfiles=anatemfiles,
        organonfiles=organonfiles,
    )
    organon.file.close()


def wdsm(
    anarede,
    anatem,
    organon,
    anatemfiles,
    organonfiles,
):
    """escrita de dados de máquina síncrona no formato ORGANON (.stb -> .dyn)
    
    Args:
        anatem:
        organon:        
    """
    ## Inicialização
    organon.file.write("!\n")
    for file in organonfiles:
        f = file.split('\\')[-1]
        organon.file.write(f"MDF {f}\n")
    organon.file.write("!\n")

    for idx, value in enumerate(anatem.dmaq):
        if value != 'dmaq' and value != 'ruler':
            ndmaq = 0
            while ndmaq < len(anatem.dmaq[value]):
                numero = value.strip()
                nome = anarede.dbarDF[anarede.dbarDF.numero == int(value)].nome.values[0]
                id = anatem.dmaq[value][ndmaq]['grupo']
                modelo_gerador = anatem.dmaq[value][ndmaq]['modelo_gerador'].split()[0]
                dmdg = anatem.dmdg[modelo_gerador]['modelo'][2:]
                if dmdg == "01":
                    dmdg = "SM01"
                    xld = float(anatem.dmdg[modelo_gerador]['l_d']) * 1e-2
                    ra = float(anatem.dmdg[modelo_gerador]['resistencia_armadura']) * 1e-2 if not anatem.dmdg[modelo_gerador]['resistencia_armadura'].strip() == "" else 0.
                    sb = float(anatem.dmdg[modelo_gerador]['potencia_nominal']) if anatem.dmdg[modelo_gerador]['potencia_nominal'].strip() != "" else 100.
                    xt = 0
                    h = float(anatem.dmdg[modelo_gerador]['inercia']) if anatem.dmdg[modelo_gerador]['inercia'].strip() != "" else 100.
                    d = float(anatem.dmdg[modelo_gerador]['amortecimento']) if anatem.dmdg[modelo_gerador]['amortecimento'].strip() != "" else 0.
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip() and anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade_u'].strip() != 'u':
                        if anatem.drgv[anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()]['modelo'] == "MD01":
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
                    else:
                        gov = "GOV" + anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()
                    organon.file.write(f"{dmdg} {nome}\n")
                    organon.file.write("! (--Bus--) (--ID--) (--Gov--) (--Bus Name--)\n")
                    organon.file.write(f"  {numero:>9} {id:>8} {gov:>9} {' ':>14}\n")
                    organon.file.write("!SM01  (-Xld-) (-Ra-) (-Sb-) (-Xt-)   (-H-) (-D-)\n")
                    organon.file.write(f"       {xld:>7.3f} {ra:>6.3f} {sb:>6.2f} {xt:>6.3f} {h:>5.3f} {d:>5.3f} /\n")
                    if gov.strip() == "GOV04":
                        organon.file.write("!GOV04 (-Rp-) (-Kp-) (-Ki-) (-Kd-) (-Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n")
                    elif gov.strip() == "GOV09":
                        organon.file.write("!GOV09 (-R-) (-T1-) (-Pmax-) (-Pmin-) (-T2-) (-T3-)\n")
                else:
                    dmdg = "SM0" + str(int(dmdg) + 2)
                    cs = anatem.dmdg[modelo_gerador]['curva_saturacao'].strip()
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_tensao'].strip() and anatem.dmaq[value][ndmaq]['modelo_regulador_tensao_u'].strip() != 'u':
                        avr = "AVR04"
                    else:
                        avr = "AVR" + anatem.dmaq[value][ndmaq]['modelo_regulador_tensao'].strip()
                    if anatem.dmaq[value][ndmaq]['modelo_estabilizador'].strip() and anatem.dmaq[value][ndmaq]['modelo_estabilizador_u'].strip() != 'u':
                        pss = "PSS01"
                    elif anatem.dmaq[value][ndmaq]['modelo_estabilizador'].strip() and anatem.dmaq[value][ndmaq]['modelo_estabilizador_u'].strip() == 'u':
                        pss = "PSS" + str(900 + int(anatem.dmaq[value][ndmaq]['modelo_estabilizador'].strip()))
                    else:
                        pss = 5*" "
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip() and anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade_u'].strip() != 'u':
                        if anatem.drgv[anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()]['modelo'] == "MD01":
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
                    elif anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip() and anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade_u'].strip() == 'u':
                        gov = "GOV" + anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()
                    else:
                        gov = 5*" "
                    uel = 5*" "
                    oel = 5*" "
                    scl = 5*" "
                    organon.file.write(f"{dmdg} {nome}\n")
                    organon.file.write("! (--Bus--) (--ID--) (--AVR--) (--PSS--) (--UEL--) (--OEL--) (--SCL--) (--Gov--) (--Ctrl Bus--) (--Rc(pu)--) (--Xc(pu)--) (--Tr(s)--) (--Bus Name--) (--CtrBus-Name--)\n")
                    organon.file.write(f"  {numero:>9} {id:>8} {avr:>9} {pss:>9} {uel:>9} {oel:>9} {scl:>9} {gov:>9} {numero:>14} {0.:>12.2f} {0.:>12.2f} {0.:>11.2f} {' ':>14} {' ':>17} /\n")                
                    if dmdg == 'SM04':
                        xd = float(anatem.dmdg[modelo_gerador]['l_d']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d'].strip() != "" else 0.
                        xld = float(anatem.dmdg[modelo_gerador]['l_d_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_prime'].strip() != "" else 0.
                        xlld = float(anatem.dmdg[modelo_gerador]['l_d_double_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_double_prime'].strip() != "" else 0.
                        xq = float(anatem.dmdg[modelo_gerador]['l_q']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_q'].strip() != "" else 0.
                        xlq = 0.
                        xllq = float(anatem.dmdg[modelo_gerador]['l_d_double_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_double_prime'].strip() != "" else 0.
                        ra = float(anatem.dmdg[modelo_gerador]['resistencia_armadura']) * 1e-2 if not anatem.dmdg[modelo_gerador]['resistencia_armadura'].strip() == "" else 0. 
                        sb = float(anatem.dmdg[modelo_gerador]['potencia_nominal']) if anatem.dmdg[modelo_gerador]['potencia_nominal'].strip() != "" else 100.
                        xl = float(anatem.dmdg[modelo_gerador]['l_l']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_l'].strip() != "" else 0.
                        xt = 0.
                        tld = float(anatem.dmdg[modelo_gerador]['tau_d0_prime']) if anatem.dmdg[modelo_gerador]['tau_d0_prime'].strip() != "" else 0.
                        tlld = float(anatem.dmdg[modelo_gerador]['tau_d0_double_prime']) if anatem.dmdg[modelo_gerador]['tau_d0_double_prime'].strip() != "" else 0.
                        tlq = 0.
                        h = float(anatem.dmdg[modelo_gerador]['inercia']) if anatem.dmdg[modelo_gerador]['inercia'].strip() != "" else 100.
                        d = float(anatem.dmdg[modelo_gerador]['amortecimento']) if anatem.dmdg[modelo_gerador]['amortecimento'].strip() != "" else 1.
                        tllq = float(anatem.dmdg[modelo_gerador]['tau_q0_double_prime']) if anatem.dmdg[modelo_gerador]['tau_q0_double_prime'].strip() != "" else 0.
                        ag = float(anatem.dcst[modelo_gerador]['parametro_1']) if (cs != "" and anatem.dcst[modelo_gerador]['parametro_1'].strip() != "") else 0.
                        bg = float(anatem.dcst[modelo_gerador]['parametro_2']) if (cs != "" and anatem.dcst[modelo_gerador]['parametro_2'].strip() != "") else 0.
                        cg = float(anatem.dcst[modelo_gerador]['parametro_3']) if (cs != "" and anatem.dcst[modelo_gerador]['parametro_3'].strip() != "") else 0.
                        organon.file.write("!SM04  (--Xd-) (-Xld-) (-Xlld-) (--Xq-) (-Xlq-) (-Xllq-) (--Ra-) (-Sbase-) (--Xl-) (-Xt-) (-Tld-) (-Tlld-) (-Tlq-) (-H-) (-D-) (-Tllq-) (---Ag-) (---Bg-) (---Cg-)\n")
                        organon.file.write(f"       {xd:>7.5f} {xld:>7.5f} {xlld:>8.5f} {xq:>7.5f} {xlq:>7.5f} {xllq:>8.5f} {ra:>7.5f} {sb:>9.2f} {xl:>7.5f} {xt:>6.1f} {tld:>7.4f} {tlld:>8.4f} {tlq:>7.4f} {h:>5.4f} {d:>5.4f} {tllq:>8.4f} {ag:>8.7f} {bg:>8.7f} {cg:>8.7f} /\n")
                    elif dmdg == 'SM05':
                        xd = float(anatem.dmdg[modelo_gerador]['l_d']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d'].strip() != "" else 0.
                        xld = float(anatem.dmdg[modelo_gerador]['l_d_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_prime'].strip() != "" else 0.
                        xlld = float(anatem.dmdg[modelo_gerador]['l_d_double_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_double_prime'].strip() != "" else 0.
                        xq = float(anatem.dmdg[modelo_gerador]['l_q']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_q'].strip() != "" else 0.
                        xlq = float(anatem.dmdg[modelo_gerador]['l_q_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_q_prime'].strip() != "" else 0.
                        xllq = float(anatem.dmdg[modelo_gerador]['l_d_double_prime']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_d_double_prime'].strip() != "" else 0.
                        ra = float(anatem.dmdg[modelo_gerador]['resistencia_armadura']) * 1e-2 if not anatem.dmdg[modelo_gerador]['resistencia_armadura'].strip() == "" else 0. 
                        sb = float(anatem.dmdg[modelo_gerador]['potencia_nominal']) if anatem.dmdg[modelo_gerador]['potencia_nominal'].strip() != "" else 100.
                        xl = float(anatem.dmdg[modelo_gerador]['l_l']) * 1e-2 if anatem.dmdg[modelo_gerador]['l_l'].strip() != "" else 0.
                        xt = 0.
                        tld = float(anatem.dmdg[modelo_gerador]['tau_d0_prime']) if anatem.dmdg[modelo_gerador]['tau_d0_prime'].strip() != "" else 0.
                        tlld = float(anatem.dmdg[modelo_gerador]['tau_d0_double_prime']) if anatem.dmdg[modelo_gerador]['tau_d0_double_prime'].strip() != "" else 0.
                        tlq = float(anatem.dmdg[modelo_gerador]['tau_q0_prime']) if anatem.dmdg[modelo_gerador]['tau_q0_prime'].strip() != "" else 0.
                        h = float(anatem.dmdg[modelo_gerador]['inercia']) if anatem.dmdg[modelo_gerador]['inercia'].strip() != "" else 100.
                        d = float(anatem.dmdg[modelo_gerador]['amortecimento']) if anatem.dmdg[modelo_gerador]['amortecimento'].strip() != "" else 1.
                        tllq = float(anatem.dmdg[modelo_gerador]['tau_q0_double_prime']) if anatem.dmdg[modelo_gerador]['tau_q0_double_prime'].strip() != "" else 0.
                        p1 = float(anatem.dcst[cs]['parametro_1']) if(cs != "" and anatem.dcst[cs]['parametro_1'].strip() != "") else 0.
                        p2 = float(anatem.dcst[modelo_gerador]['parametro_2']) if(cs != "" and anatem.dcst[modelo_gerador]['parametro_2'].strip() != "") else 0.
                        p3 = float(anatem.dcst[modelo_gerador]['parametro_3']) if(cs != "" and anatem.dcst[modelo_gerador]['parametro_3'].strip() != "") else 0.
                        sm1 = float(p1 * exp(p2-p2*p3)) 
                        sm2 = float(p1 * exp(p2*1.2-p2*p3)) 
                        organon.file.write("!SM05  (--Xd-) (-Xld-) (-Xlld-) (--Xq-) (-Xlq-) (-Xllq-) (--Ra-) (-Sbase-) (--Xl-) (-Xt-) (-Tld-) (-Tlld-) (-Tlq-) (-H-) (-D-) (-Tllq-) (-S1.0-) (-S1.2-)\n")
                        organon.file.write(f"       {xd:>7.5f} {xld:>7.5f} {xlld:>8.5f} {xq:>7.5f} {xlq:>7.5f} {xllq:>8.5f} {ra:>7.5f} {sb:>9.2f} {xl:>7.5f} {xt:>6.1f} {tld:>7.4f} {tlld:>8.4f} {tlq:>7.4f} {h:>5.4f} {d:>5.4f} {tllq:>8.4f} {sm1:>8.7f} {sm2:>8.7f} /\n")
                    if avr == "AVR04":
                        avr = anatem.dmaq[value][ndmaq]['modelo_regulador_tensao']
                        ka = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#KA")]
                        ta = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#TA")]
                        kf = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#KF")]
                        tf = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#TF")]
                        te = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#TE")]
                        ke = anatem.dcdu[avr]['defpar_valor'][anatem.dcdu[avr]['defpar_nome'].index("#KE")]
                        min = anatem.dcdu[avr]['defval_parametro_d1'][anatem.dcdu[avr]['defval_variavel'].index('Lmin')]
                        max = anatem.dcdu[avr]['defval_parametro_d1'][anatem.dcdu[avr]['defval_variavel'].index('Lmax')]
                        organon.file.write("!AVR04 (-Ka-) (-Ta>0-) (-Ke-) (-Te-) (-Tc-) (-Tb>0-) (-Kf-) (-Tf-) (-Vmin-) (-Vmax-) (-E1-) (-S[E1]-) (-E2-) (-S[E2]-) (-Tc1-) (-Tb1-)\n")
                        organon.file.write(f"       {ka:>6} {ta:>8} {ke:>6} {te:>6} {6*' ':>6} {8*' ':>8} {kf:>6} {tf:>6} {min:>8} {max:>8} {6*' ':>6} {9*' ':>9} {6*' ':>6} {9*' ':>9} {7*' ':>7} {7*' ':>7} /\n")
                    if pss == "PSS01": 
                        pss = anatem.dmaq[value][ndmaq]['modelo_estabilizador']
                        tw = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#TW1")]
                        t1 = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#TN1")]
                        t2 = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#TN1")]
                        t3 = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#TD1")]
                        t4 = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#TD1")]
                        k1 = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#KP1")]
                        min = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#LMIN")]
                        max = anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index("#LMAX")]
                        organon.file.write("!PSS01 (-T1-) (-T2-) (-T3-) (-T4-) (-T5-) (-T6-) (-Tw-) (-K1-) (-Vmin-) (-Vmax-) (-Type-)\n")
                        organon.file.write(f"       {t1} {t2} {t3} {t4} {' '} {' '} {tw} {k1} {min} {max} {' '} /\n")
                    if gov.strip() == "GOV04":
                        gov = anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade']
                        rp = anatem.drgv[gov]['estatismo']
                        at = anatem.drgv[gov]['ganho_turbina']
                        qnl = anatem.drgv[gov]['vazao_noload']
                        tw = float(anatem.drgv[gov]['cte_tempo_agua'])
                        tg = anatem.drgv[gov]['cte_tempo_servomotor']
                        tv = '0.001'
                        tp1 = anatem.drgv[gov]['cte_tempo_filtragem']
                        tp2 = '0.001'
                        td = "0."
                        g1x = '99.'
                        g1n = '-99.'
                        g2x = '99.'
                        g2n = '-99.'
                        g3x = anatem.drgv[gov]['limite_maximo']
                        g3n = anatem.drgv[gov]['limite_minimo']
                        kd = '1.'
                        h = float(anatem.dmdg[modelo_gerador]['inercia'])
                        kp = (h * tw) / (2.3 - (tw - 1) * 0.15)
                        ki = (h) / ((2.3 - (tw - 1) * 0.15) * (5 - (tw - 1) * 0.5) * tw * tw)
                        organon.file.write("!GOV04 (-Rp-) (--Kp-) (--Ki-) (--Kd-) (--Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n")
                        organon.file.write(f"       {rp:>6} {kp:>7.5f} {ki:>7.5f} {kd:>7} {td:>7} {tp1:>7} {tp2:>9} {g1n:>9} {g1x:>9} {tv:>8} {g2n:>9} {g2x:>9} {tg:>8} {g3n:>9} {g3x:>9} {tw:>6.4f} {at:>6} {qnl:>7} /\n")
                    elif gov.strip() == "GOV09":
                        gov = anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade']
                        r = anatem.drgv[gov]['estatismo']
                        t1 = anatem.drgv[gov]['cte_tempo_regulador']
                        pmax = anatem.drgv[gov]['limite_maximo']
                        pmin = anatem.drgv[gov]['limite_minimo']
                        t2 = anatem.drgv[gov]['cte_tempo_1']
                        t3 = anatem.drgv[gov]['cte_tempo_reaquecimento']
                        organon.file.write("!GOV09 (-R-) (-T1-) (-Pmax-) (-Pmin-) (-T2-) (-T3-)\n")
                        organon.file.write(f"       {r:>4} {t1:>6} {pmax:>8} {pmin:>8} {t2:>6} {t3:>6} /\n")
                organon.file.write("!\n")
                organon.file.write("!\n")
                ndmaq += 1
                
    pass
    