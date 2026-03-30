# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from folder import organonfolder, pssefolder
from os.path import realpath
from numpy import exp
from datetime import datetime as dt
import sys


def orgntw(
    anarede,
    organon,
):
    """escrita de dados de rede no formato ORGANON (.pwf -> .ntw)

    Args
        anarede:
        organon
    """
    ## Inicialização
    ntwpath = organonfolder(
        anarede,
    )

    # ======================================================
    # OPEN NTW FILE (LOSSLESS WRITE)
    # ======================================================

    fOrg = r"C:\\Program Files\\HPPA\\Organon\\bin"
    vPyt = "3.8"
    fMod = fOrg + "\\Python\\" + vPyt
    sys.path.append(fMod)

    import organon

    app = organon.GetApp()
    ret = app.OpenFile(anarede.dirPWF)
    print("\nOpen Return Code: {}".format(ret))
    if not ret == 0:
        print("File not loaded. Exiting...")
        exit()

    app.RunScriptCommand("PARAM PFBLKTAP T")

    for i in range(2):
        print("\n--- POWER FLOW #{} ---".format(i + 1))
        app.RunScriptCommand("NEWTON")

    ntwfile = realpath(ntwpath + anarede.system[:-4] + ".ntw")
    organon.file = open(ntwfile, "w", encoding="latin-1")
    organon.file.write("           7           0\n")
    organon.file.write(
        f" {dt.now().strftime('%Y%m%d %H:%M:%S')}  {anarede.cte['SBSE']}\n"
    )
    organon.file.write(f"{anarede.titu['ruler']}\n")
    loaddata = ""
    gendata = ""
    shuntdata = ""
    organon.file.write(
        f"(BUS_ID), '  BUS_NAME  ', (VBASEKV), TP, S, (GSHT_MW), (BSHMVAR), ARE, ZON, (MODV_PU), (ANGV_DEG), (VMXN_PU), (VMNN_PU), (VMXE_PU), (VMNE_PU), OWN SUB ARG\n"
    )
    for idx, value in anarede.dbarDF.iterrows():
        tipo = 0 if value.tipo == 0 else 2 if value.tipo == 1 else 3
        dgbt = (
            anarede.dgbtDF.loc[
                anarede.dgbtDF.grupo == value.grupo_base_tensao, "tensao"
            ].values[0]
            if anarede.pwfblock["DGBT"]
            else 500.0
        )
        shunt = 1 if value.shunt_barra != 0.0 else 0
        if anarede.pwfblock["DGLT"]:
            vmax = anarede.dgltDF.loc[
                anarede.dgltDF.grupo_limite_tensao == value.grupo_limite_tensao,
                "limite_maximo",
            ].values[0]
            vmin = anarede.dgltDF.loc[
                anarede.dgltDF.grupo_limite_tensao == value.grupo_limite_tensao,
                "limite_minimo",
            ].values[0]
            vmaxE = anarede.dgltDF.loc[
                anarede.dgltDF.grupo_limite_tensao == value.grupo_limite_tensao,
                "limite_maximo_E",
            ].values[0]
            vminE = anarede.dgltDF.loc[
                anarede.dgltDF.grupo_limite_tensao == value.grupo_limite_tensao,
                "limite_minimo_E",
            ].values[0]
        else:
            vmax = 1.05
            vmin = 0.95
            vmaxE = 1.1
            vminE = 0.9
        bctrl = (
            value.numero if value.barra_controlada == "0" else value.barra_controlada
        )
        if anarede.pwfblock["DGER"]:
            genst = 1 if value.numero in anarede.dgerDF.numero.values else 0
            fpercent = (
                anarede.dgerDF.loc[
                    anarede.dgerDF.numero == value.numero,
                    "fator_participacao_controle_remoto",
                ].values[0]
                if genst
                else 100.0
            )
            pmax = (
                anarede.dgerDF.loc[
                    anarede.dgerDF.numero == value.numero, "potencia_ativa_maxima"
                ].values[0]
                if genst
                else 0.0
            )
            pmin = (
                anarede.dgerDF.loc[
                    anarede.dgerDF.numero == value.numero, "potencia_ativa_minima"
                ].values[0]
                if genst
                else 0.0
            )
            grupo = 10
        else:
            genst = 0
            fpercent = 100.0
            pmax = 99999.0
            pmin = 0.0
            grupo = 10
        organon.file.write(
            f"{int(value.numero):>8},'{value.nome:>12s}',{dgbt:>10},{tipo:>3},{shunt:>2},{0.0:>10},{value.shunt_barra:>10.3f},{value.area:>4},{1:>4},{value.tensao:>10.5f},{value.angulo:>11.4f},{vmax:>10.5f},{vmin:10.5f},{vmaxE:10.5f},{vminE:10.5f},{0:>2} /\n"
        )
        loaddata += (
            f"{int(value.numero):>8},' 1', 1,{value.demanda_ativa:>11.3f},{value.demanda_reativa:>12.3f},{0.0:>12},{0.0:>12},{0.0:>12},{1:>6},{0.1e8:>12E},{0.1e8:>12E},'Unnamed' /\n"
            if value.demanda_ativa != 0.0 and value.demanda_reativa != 0.0
            else ""
        )
        gendata += (
            f"{int(value.numero):>8},' 1',{value.potencia_ativa:>10.3f},{value.potencia_reativa:>11.3f},{value.potencia_reativa_maxima:>11.3f},{value.potencia_reativa_minima:>11.3f},{value.tensao:>10.5f},{bctrl:>10},{anarede.cte['SBSE']:>11.3f},{0.0:>10},{0.0:>10},{1.0:>10},{genst:>2},{fpercent:>8.1f},{pmax:>12.3f},{pmin:>12.3f},{grupo:>5},{0:>10},{1:>6},{2:>11},{0.0:>13.3f}"
            if tipo >= 2
            else ""
        )
    organon.file.write(f" 0  / END OF BUS DATA, BEGIN LOAD DATA\n")
    organon.file.write(
        f"(BUS_ID) ,'ID',ST,    (PL_MW),   (QL_MVAR),    (IPL_MW),  (IQL_MVAR),    (ZPL_MW),  (ZQL_MVAR), (OWN), (R0), (X0), (Name)\n"
    )
    organon.file.write(f"0  / END OF LOAD DATA, BEGIN GENERATOR DATA\n")
    organon.file.write(
        f"(BUS_ID) ,'ID',   (PG_MW),  (QG_MVAR), (QMX_MVAR), (QMN_MVAR), (VSPECPU),  (BCO_ID), (BASE_MVA), (RTRF_PU), (XTRF_PU),  (TAP_PU),ST,   (FP%),   (PMAX_MW),  (PMIN_MW),(GRP), (BLOCKED), OWNER, CONNECTION, R1, X1, R2, X2, R0, X0, RGRD, XGRD, XQ, SF, MAXANG, TYPE, NAME, NMAX, NON, COMP. BUS\n"
    )
    organon.file.write(f"0  / END OF GENERATOR DATA, BEGIN SHUNT DATA\n")
    organon.file.write(
        f"! BUS_ID, TC, VMAX_PU, VMIN_PU, BCO_ID, B0_MVAR, ST, ST1, N1, B1_Mvar, XZ1_PU, ST2, N2, B2_Mvar, XZ2_PU, ...\n"
    )

    transformerdata = ""
    capacitordata = ""
    mutualimpedancedata = ""
    organon.file.write(
        f"0 / END OF SWITCHED SHUNT DATA, BEGIN TRANSMISSION LINE DATA\n"
    )
    organon.file.write(
        f"! BFR_ID, BTO_ID,'CI', RL_PU , XL_PU, B_MVAR, L1_MVA, L2_MVA, L3_MVA, F, T, LEN_KM, ARE, OWN, R0_PU, X0_PU, BSH0_PU, NAME, BCSHTF_ID, CSHTF_ST, BCSHTT_ID, CSHTT_ST, SHTF1_ST, GSHTF1_PU, BSHTF1_PU, SHTT1_ST, GSHTT1_PU, BSHTT1_PU, SHTF2_ST, GSHTF2_PU, BSHTF2_PU, SHTT2_ST, GSHTT2_PU, BSHTT2_PU, SHTF3_ST, GSHTF3_PU, BSHTF3_PU, SHTT3_ST, GSHTT3_PU, BSHTT3_PU\n"
    )
    organon.file.write(f"0  / END OF TRANSMISSION LINE DATA, BEGIN TRANSFORMER DATA\n")
    organon.file.write(f"0  / END OF TRANSFORMER DATA, BEGIN SERIES CAPACITOR DATA\n")
    organon.file.write(
        f"! BFROM_ID, BTO_ID, 'CRC', R_PU, X_PU, RATEA_MVA, RATEB_MVA, RATEC_MVA, SHTF_ST, GSHTF, BSHTF, SHTT_ST, GSHTT, BSHTT, BRKERF_ST, BRKERT_ST, OWNER, NAME\n"
    )

    dclinkdata = ""
    organon.file.write(f"0  / END OF SERIES CAPACITOR DATA, BEGIN DCLINK DATA\n")
    organon.file.write(
        f"! BIP, ARE, ZON, TC, RL_OHM, VALCONT, VSPEC_KV, VCCMIN_KV, DELTI_A, STATUS, VNOM_KV, PNOM_MW, NAME\n"
    )
    organon.file.write(
        f"! RET_ID, NC, ALFA, ALFMN, RTRFC_PU, XTRFC_PU, BASE_KV, TRR, TAPC_PU, TMXC_PU, TMNC_PU, TSTC_PU, XCCC_OHM\n"
    )
    organon.file.write(
        f"! INV_ID, NC, GAMA, GAMMN, ITRFC_PU, XTRFC_PU, BASE_KV, TRI, TAPC_PU, TMXC_PU, TMNC_PU, TSTC_PU, XCCC_OHM\n"
    )
    organon.file.write(f"0  / END OF DCLINK DATA, BEGIN VSC DATA\n")  # nada v
    organon.file.write(f"(NUM) (NAME) (STATUS) (TYPE)\n")
    organon.file.write(
        f"(CONV_NUM), (BUS), (PSTATUS), (NSTATUS), (PTYPE), (PSET1), (PSET2), (QTYPE), (QSET), (A), (B), (C), (SMAX), (IMAX), (QMAX), (QMIN), (VMAX), (VMIN), (RC), (XC), (BF), (RT), (XT), (VBASE), (LPWF), (GND), (NS), (TYPE)\n"
    )
    organon.file.write(f"(FROM_NODE), (TO_NODE), (STATUS), (PRDC) (NRDC) (GRDC)\n")

    areadata = ""
    organon.file.write(f"0  / END OF VSC DATA, BEGIN AREA DATA\n")
    organon.file.write(f"(#AR), (ASW_ID),  (INT_MW),'(          AREA_NAME         )'\n")
    organon.file.write(f"0  / END OF AREA DATA, BEGIN OF ZONE DATA\n")  # nada v
    organon.file.write(f"! ZONE ID, ZONE NAME\n")
    organon.file.write(f"0 / END OF ZONE DATA, BEGIN OWNER DATA\n")  # nada v
    organon.file.write(f"! OWNER ID, OWNER NAME\n")
    organon.file.write(f"0 / END OF OWNER DATA, BEGIN OF SUBSTATION DATA\n")
    organon.file.write(f"! SUBSTATION ID, SUB NAME, LATITUDE, LONGITUDE\n")
    organon.file.write(
        f" 0  / END OF SUBSTATION DATA, BEGIN OF TRANSFORMER IMPEDANCE CORRECTION DATA\n"
    )  # nada v
    organon.file.write(f"! TABLE ID, TAP1, CORR1, TAP2, CORR2, TAP3, CORR3, ...\n")
    organon.file.write(
        f" 0 / END OF IMPEDANCE CORRECTION DATA, BEGIN OF LINE MUTUAL IMPEDANCE DATA\n"
    )
    organon.file.write(
        f"! BFR1, BTO1, CRC1, INI1(%), FIN1(%), BFR2, BTO2, CRC2, INI2(%), FIN2(%), R_PU, X_PU\n"
    )
    organon.file.write(
        f" 0 / END OF LINE MUTUAL IMPEDANCE DATA, BEGIN OF INDUCTION MOTOR DATA\n"
    )  # nada v
    organon.file.write(
        f"! BUS,  ID,  STATUS, COUNT  MVA,  PE,  QE,  RS, XS, XM, R1, X1, R0, X0, OWNER, TYPE NAME\n"
    )
    organon.file.write(
        f"0  / END OF INDUCTION MOTOR DATA, BEGIN OF BREAKER CONFIGURATION DATA\n"
    )  # nada v
    organon.file.write(f"! BUS No.,  Node 1, Node 2, ...\n")
    organon.file.write(
        f"0  / END OF BREAKER CONFIGURATION DATA, BEGIN OF FACTS DATA\n"
    )  # nada v
    organon.file.write(
        f"! NAME, SEND-BUS, TERMINAL-BUS, CRC, TYPE, PREF(MW), QREF(MVAR), VSET(PU), ISHTMAX(MVA), PTRXMAX(MW), VTMIN(PU), VTMAX(PU), VCMAX(PU), VCMIN(PU) ICMAX(MVA), ICEMR(MVA), ICMIN(MVA), XC(PU), DROOP, CUROVR, IINI, IINC, IOFFI, IOFFC, STATUS, OWNER\n"
    )
    organon.file.write(f"0  / END OF FACTS DATA")
    organon.file.write(f"")
    organon.file.write(f"")
    organon.file.write(f"")


def orwudc(
    anarede,
    anatem,
    organon,
):
    """escrita de controladores definidos pelo usuário no formato ORGANON (.cdu -> .udc)

    Args
        anarede:
        anatem:
        organon:
    """
    ## Inicialização
    anatemfiles = list()
    organonfiles = list()
    cdupath = organonfolder(
        anarede,
    )

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
            # print(entry)
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
                    float(anatem.dcdu[key]["defval_parametro_d1"][i_defval])
                    organon.file.write(
                        f"{anatem.dcdu[key]['defval_variavel'][i_defval].strip():<6} = "
                        f"CONST({anatem.dcdu[key]['defval_parametro_d1'][i_defval]:>18})\n",
                    )
                except:
                    if "#" in anatem.dcdu[key]["defval_parametro_d1"][i_defval]:
                        defval_variable = anatem.dcdu[key]["defval_parametro_d1"][
                            i_defval
                        ]
                        for j, defpar_nome in enumerate(
                            anatem.dcdu[key]["defpar_nome"]
                        ):
                            if defpar_nome.strip() == defval_variable:
                                defval_value = anatem.dcdu[key]["defpar_valor"][j]

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
                    dtdelay = "TMSTP"
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

                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "ENTRAD"
                    and anatem.dcdu[key]["bloco_saida"][io_bloco]
                    not in anatem.dcdu[key]["defpar_nome"]
                    and anatem.dcdu[key]["bloco_saida"][io_bloco]
                    not in anatem.dcdu[key]["defval_variavel"]
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =REF(0.0)\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "VTR"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}    =INPGVC()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "VSAD"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INPPSS()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "WMAQ"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}    =INPGW()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "PTFNT"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INPWMW()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "QTFNT"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INPWMVAR()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "VOLT"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INPGVT()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "ANGL"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INPVANG()\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "PBSIS"
                ):
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}  =INIT(100.)\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "IMPORT"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "DT"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida}    =CONST({dtdelay})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".GT."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =GT({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".LT."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =LT({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".GE."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =GE({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".LE."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =LE({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".EQ."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =EQ({entrada[0]}, {entrada[1]})\n")
                    terms += 1
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "COMPAR"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NE."
                ):
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NE({entrada[0]}, {entrada[1]})\n")
                    terms += 1

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "DIVSAO":
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    if terms == 2:
                        entrada = [
                            anatem.dcdu[key]["bloco_entrada"][io_bloco],
                            anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                        ]
                        saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                        organon.file.write(
                            f"{saida:<6} =DIVIDE({entrada[0]}, {entrada[1]})\n"
                        )
                        io_bloco += 1
                    else:
                        saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                        organon.file.write(f"{saida:<6} =DIVIDEM(0.0, 1.0, ")
                        for j in range(terms):
                            entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                            if j < terms - 1:
                                organon.file.write(f"{entrada}, ")
                            else:
                                organon.file.write(f"{entrada})\n")

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FRACAO":
                    num = (
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco]
                        or anatem.dcdu[key]["bloco_parametro2"][io_bloco]
                    )
                    den = (
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco]
                        or anatem.dcdu[key]["bloco_parametro4"][io_bloco]
                    )
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =FRAC({entrada}, {num}, {den})\n")

                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "COS"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =COS({entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "SIN"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =SIN({entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "DEADB1"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    abcd = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro4"][io_bloco],
                    ]
                    organon.file.write(
                        f"{saida:<6} =DDBND3({entrada}, {abcd[0]}, {abcd[1]})\n"
                    )
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "DEADB2"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    abcd = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro4"][io_bloco],
                    ]
                    organon.file.write(
                        f"{saida:<6} =DDBND4({entrada}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]})\n"
                    )
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "PONTOS"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    organon.file.write(f"{saida:<6} =LFPP({entrada}, ")
                    for j in range(terms):
                        ponto_x = anatem.dcdu[key]["bloco_parametro1"][io_bloco + j]
                        ponto_y = anatem.dcdu[key]["bloco_parametro2"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{ponto_x}, {ponto_y}, ")
                        else:
                            organon.file.write(f"{ponto_x}, {ponto_y})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "X**2"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =SQR({entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "SQRT"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =SQRT({entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "MENOS"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =GAIN(0.0, {entrada}, -1.0)\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "FUNCAO"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == "RAMPA"
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    abcd = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro4"][io_bloco],
                    ]
                    organon.file.write(
                        f"{saida:<6} =RAMP({saida}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]})\n"
                    )

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "GANHO":
                    a = anatem.dcdu[key]["bloco_parametro1"][io_bloco]
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =GAIN(0.0, {entrada}, {a})\n")

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LEDLAG":
                    abcd = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro4"][io_bloco],
                    ]
                    abcd = ["0" if item == "" else item for item in abcd]
                    xn = [
                        anatem.dcdu[key]["bloco_limite_maximo"][io_bloco],
                        anatem.dcdu[key]["bloco_limite_minimo"][io_bloco],
                    ]
                    xn = ["99.99", "-99.99"] if xn == ["", ""] else xn
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =COMP6(0.0, {entrada}, {abcd[0]}, {abcd[1]}, {abcd[2]}, {abcd[3]}, {xn[0]}, {xn[1]})\n"
                    )

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LIMITA":
                    xn = [
                        anatem.dcdu[key]["bloco_limite_maximo"][io_bloco],
                        anatem.dcdu[key]["bloco_limite_minimo"][io_bloco],
                    ]
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =LIMIT(0.0, {entrada}, #{xn[0]}, #{xn[1]})\n"
                    )

                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".AND."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =AND( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".OR."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =OR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".XOR."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =XOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NOT."
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NOT({entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NAND."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NAND( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NOR."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NXOR."
                ):
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NXOR( ")
                    for j in range(terms):
                        entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                        if j < terms - 1:
                            organon.file.write(f"{entrada}, ")
                        else:
                            organon.file.write(f"{entrada})\n")
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "LOGIC"
                    and anatem.dcdu[key]["bloco_subtipo"][io_bloco] == ".NOT."
                ):
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =NOT({entrada})\n")

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "MAX":
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =MAX({entrada[0]}, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "MIN":
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(f"{saida:<6} =MIN({entrada[0]}, {entrada[1]})\n")
                    terms = 2
                    io_bloco += 1

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "MULTPL":
                    try:
                        while anatem.dcdu[key]["bloco_tipo"][io_bloco + terms] == "":
                            terms += 1
                    except:
                        pass
                    if terms == 2:
                        entrada = [
                            anatem.dcdu[key]["bloco_entrada"][io_bloco],
                            anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                        ]
                        saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                        organon.file.write(
                            f"{saida:<6} =MULT({entrada[0]}, {entrada[1]})\n"
                        )
                        io_bloco += 1
                    else:
                        saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                        organon.file.write(f"{saida:<6} =MULTM(0.0, 1.0, ")
                        for j in range(terms):
                            entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco + j]
                            if j < terms - 1:
                                organon.file.write(f"{entrada}, ")
                            else:
                                organon.file.write(f"{entrada})\n")

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "PROINT":
                    abc = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                    ]
                    abc = ["0" if item == "" else item for item in abc]
                    xn = [
                        anatem.dcdu[key]["bloco_limite_maximo"][io_bloco],
                        anatem.dcdu[key]["bloco_limite_minimo"][io_bloco],
                    ]
                    xn = ["99.99", "-99.99"] if xn == ["", ""] else xn
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =COMP6(0.0, {entrada}, {abc[0]}, {abc[1]}, {abc[2]}, {0.0}, {xn[0]}, {xn[1]})\n"
                    )

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "SELET2":
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 2],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =SEL({entrada[0]}, {entrada[1]}, {entrada[2]}, 0.0)\n"
                    )
                    terms = 3
                    io_bloco += 2

                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "SOMA"
                    and anatem.dcdu[key]["bloco_tipo"][io_bloco + 2] == ""
                ):
                    sinal = [
                        anatem.dcdu[key]["bloco_sinal"][io_bloco],
                        anatem.dcdu[key]["bloco_sinal"][io_bloco + 1],
                        anatem.dcdu[key]["bloco_sinal"][io_bloco + 2],
                    ]
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 2],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =ADD({sinal[0]}1.0, {entrada[0]}, {sinal[1]}1.0, {entrada[1]}, {sinal[2]}1.0, {entrada[2]})\n"
                    )
                    terms = 3
                    io_bloco += 2
                if (
                    anatem.dcdu[key]["bloco_tipo"][io_bloco] == "SOMA"
                    and anatem.dcdu[key]["bloco_tipo"][io_bloco + 1] == ""
                ):
                    sinal = [
                        anatem.dcdu[key]["bloco_sinal"][io_bloco],
                        anatem.dcdu[key]["bloco_sinal"][io_bloco + 1],
                    ]
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =ADD({sinal[0]}1.0, {entrada[0]}, {sinal[1]}1.0, {entrada[1]})\n"
                    )
                    terms = 2
                    io_bloco += 1

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "T/HOLD":
                    entrada = [
                        anatem.dcdu[key]["bloco_entrada"][io_bloco],
                        anatem.dcdu[key]["bloco_entrada"][io_bloco + 1],
                    ]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =THOLD({entrada[0]}, {entrada[1]})\n"
                    )
                    terms = 2
                    io_bloco += 1

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "WSHOUT":
                    abc = [
                        anatem.dcdu[key]["bloco_parametro1"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro2"][io_bloco],
                        anatem.dcdu[key]["bloco_parametro3"][io_bloco],
                    ]
                    xn = [
                        anatem.dcdu[key]["bloco_limite_maximo"][io_bloco],
                        anatem.dcdu[key]["bloco_limite_minimo"][io_bloco],
                    ]
                    xn = ["99.99", "-99.99"] if xn == ["", ""] else xn
                    entrada = anatem.dcdu[key]["bloco_entrada"][io_bloco]
                    saida = anatem.dcdu[key]["bloco_saida"][io_bloco]
                    organon.file.write(
                        f"{saida:<6} =COMP6(0.0, {entrada}, {0.0}, {abc[0]}, {abc[1]}, {abc[2]}, {xn[0]}, {xn[1]})\n"
                    )

                if anatem.dcdu[key]["bloco_tipo"][io_bloco] == "EXPORT":
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

    return anatemfiles, organonfiles


def orwdyn(
    anarede,
    anatem,
    organon,
    organonfiles,
):
    """escrita de dados de máquina síncrona no formato ORGANON (.stb -> .dyn)

    Args:
        anatem:
        anatem:
        organon:
        organonfiles:
    """
    ## Inicialização
    # Arquivo
    folder = organonfolder(
        anarede,
    )
    organon.filedir = realpath(
        folder + "\\" + anarede.name + ".dyn",
    )
    organon.file = open(organon.filedir, "w")
    organon.file.write("!\n")
    for file in organonfiles:
        f = file.split("\\")[-1]
        organon.file.write(f"MDF {f}\n")
    organon.file.write("!\n")

    for idx, value in enumerate(anatem.dmaq):
        if value != "dmaq" and value != "ruler":
            ndmaq = 0
            while ndmaq < len(anatem.dmaq[value]):
                numero = value.strip()
                nome = anarede.dbarDF[anarede.dbarDF.numero == int(value)].nome.values[
                    0
                ]
                id = anatem.dmaq[value][ndmaq]["grupo"]
                modelo_gerador = anatem.dmaq[value][ndmaq]["modelo_gerador"].split()[0]
                dmdg = anatem.dmdg[modelo_gerador]["modelo"][2:]
                if dmdg == "01":
                    dmdg = "SM01"
                    xld = float(anatem.dmdg[modelo_gerador]["l_d"]) * 1e-2
                    ra = (
                        float(anatem.dmdg[modelo_gerador]["resistencia_armadura"])
                        * 1e-2
                        if not anatem.dmdg[modelo_gerador][
                            "resistencia_armadura"
                        ].strip()
                        == ""
                        else 0.0
                    )
                    sb = (
                        float(anatem.dmdg[modelo_gerador]["potencia_nominal"])
                        if anatem.dmdg[modelo_gerador]["potencia_nominal"].strip() != ""
                        else 100.0
                    )
                    xt = 0
                    h = (
                        float(anatem.dmdg[modelo_gerador]["inercia"])
                        if anatem.dmdg[modelo_gerador]["inercia"].strip() != ""
                        else 100.0
                    )
                    d = (
                        float(anatem.dmdg[modelo_gerador]["amortecimento"])
                        if anatem.dmdg[modelo_gerador]["amortecimento"].strip() != ""
                        else 0.0
                    )
                    if (
                        anatem.dmaq[value][ndmaq]["modelo_regulador_velocidade"].strip()
                        and anatem.dmaq[value][ndmaq][
                            "modelo_regulador_velocidade_u"
                        ].strip()
                        != "u"
                    ):
                        if (
                            anatem.drgv[
                                anatem.dmaq[value][ndmaq][
                                    "modelo_regulador_velocidade"
                                ].strip()
                            ]["modelo"]
                            == "MD01"
                        ):
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
                    else:
                        gov = (
                            "GOV"
                            + anatem.dmaq[value][ndmaq][
                                "modelo_regulador_velocidade"
                            ].strip()
                        )
                    organon.file.write(f"{dmdg} {nome}\n")
                    organon.file.write(
                        "! (--Bus--) (--ID--) (--Gov--) (--Bus Name--)\n"
                    )
                    organon.file.write(f"  {numero:>9} {id:>8} {gov:>9} {' ':>14}\n")
                    organon.file.write(
                        "!SM01  (-Xld-) (-Ra-) (-Sb-) (-Xt-)   (-H-) (-D-)\n"
                    )
                    organon.file.write(
                        f"       {xld:>7.3f} {ra:>6.3f} {sb:>6.2f} {xt:>6.3f} {h:>5.3f} {d:>5.3f} /\n"
                    )
                    if gov.strip() == "GOV04":
                        organon.file.write(
                            "!GOV04 (-Rp-) (-Kp-) (-Ki-) (-Kd-) (-Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n"
                        )
                    elif gov.strip() == "GOV09":
                        organon.file.write(
                            "!GOV09 (-R-) (-T1-) (-Pmax-) (-Pmin-) (-T2-) (-T3-)\n"
                        )
                else:
                    dmdg = "SM0" + str(int(dmdg) + 2)
                    cs = anatem.dmdg[modelo_gerador]["curva_saturacao"].strip()
                    if (
                        anatem.dmaq[value][ndmaq]["modelo_regulador_tensao"].strip()
                        and anatem.dmaq[value][ndmaq][
                            "modelo_regulador_tensao_u"
                        ].strip()
                        != "u"
                    ):
                        avr = "AVR04"
                    else:
                        avr = (
                            "AVR"
                            + anatem.dmaq[value][ndmaq][
                                "modelo_regulador_tensao"
                            ].strip()
                        )
                    if (
                        anatem.dmaq[value][ndmaq]["modelo_estabilizador"].strip()
                        and anatem.dmaq[value][ndmaq]["modelo_estabilizador_u"].strip()
                        != "u"
                    ):
                        pss = "PSS01"
                    elif (
                        anatem.dmaq[value][ndmaq]["modelo_estabilizador"].strip()
                        and anatem.dmaq[value][ndmaq]["modelo_estabilizador_u"].strip()
                        == "u"
                    ):
                        pss = "PSS" + str(
                            900
                            + int(
                                anatem.dmaq[value][ndmaq][
                                    "modelo_estabilizador"
                                ].strip()
                            )
                        )
                    else:
                        pss = 5 * " "
                    if (
                        anatem.dmaq[value][ndmaq]["modelo_regulador_velocidade"].strip()
                        and anatem.dmaq[value][ndmaq][
                            "modelo_regulador_velocidade_u"
                        ].strip()
                        != "u"
                    ):
                        if (
                            anatem.drgv[
                                anatem.dmaq[value][ndmaq][
                                    "modelo_regulador_velocidade"
                                ].strip()
                            ]["modelo"]
                            == "MD01"
                        ):
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
                    elif (
                        anatem.dmaq[value][ndmaq]["modelo_regulador_velocidade"].strip()
                        and anatem.dmaq[value][ndmaq][
                            "modelo_regulador_velocidade_u"
                        ].strip()
                        == "u"
                    ):
                        gov = (
                            "GOV"
                            + anatem.dmaq[value][ndmaq][
                                "modelo_regulador_velocidade"
                            ].strip()
                        )
                    else:
                        gov = 5 * " "
                    uel = 5 * " "
                    oel = 5 * " "
                    scl = 5 * " "
                    organon.file.write(f"{dmdg} {nome}\n")
                    organon.file.write(
                        "! (--Bus--) (--ID--) (--AVR--) (--PSS--) (--UEL--) (--OEL--) (--SCL--) (--Gov--) (--Ctrl Bus--) (--Rc(pu)--) (--Xc(pu)--) (--Tr(s)--) (--Bus Name--) (--CtrBus-Name--)\n"
                    )
                    organon.file.write(
                        f"  {numero:>9} {id:>8} {avr:>9} {pss:>9} {uel:>9} {oel:>9} {scl:>9} {gov:>9} {numero:>14} {0.:>12.2f} {0.:>12.2f} {0.:>11.2f} {' ':>14} {' ':>17} /\n"
                    )
                    if dmdg == "SM04":
                        xd = (
                            float(anatem.dmdg[modelo_gerador]["l_d"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d"].strip() != ""
                            else 0.0
                        )
                        xld = (
                            float(anatem.dmdg[modelo_gerador]["l_d_prime"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_prime"].strip() != ""
                            else 0.0
                        )
                        xlld = (
                            float(anatem.dmdg[modelo_gerador]["l_d_double_prime"])
                            * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_double_prime"].strip()
                            != ""
                            else 0.0
                        )
                        xq = (
                            float(anatem.dmdg[modelo_gerador]["l_q"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_q"].strip() != ""
                            else 0.0
                        )
                        xlq = 0.0
                        xllq = (
                            float(anatem.dmdg[modelo_gerador]["l_d_double_prime"])
                            * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_double_prime"].strip()
                            != ""
                            else 0.0
                        )
                        ra = (
                            float(anatem.dmdg[modelo_gerador]["resistencia_armadura"])
                            * 1e-2
                            if not anatem.dmdg[modelo_gerador][
                                "resistencia_armadura"
                            ].strip()
                            == ""
                            else 0.0
                        )
                        sb = (
                            float(anatem.dmdg[modelo_gerador]["potencia_nominal"])
                            if anatem.dmdg[modelo_gerador]["potencia_nominal"].strip()
                            != ""
                            else 100.0
                        )
                        xl = (
                            float(anatem.dmdg[modelo_gerador]["l_l"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_l"].strip() != ""
                            else 0.0
                        )
                        xt = 0.0
                        tld = (
                            float(anatem.dmdg[modelo_gerador]["tau_d0_prime"])
                            if anatem.dmdg[modelo_gerador]["tau_d0_prime"].strip() != ""
                            else 0.0
                        )
                        tlld = (
                            float(anatem.dmdg[modelo_gerador]["tau_d0_double_prime"])
                            if anatem.dmdg[modelo_gerador][
                                "tau_d0_double_prime"
                            ].strip()
                            != ""
                            else 0.0
                        )
                        tlq = 0.0
                        h = (
                            float(anatem.dmdg[modelo_gerador]["inercia"])
                            if anatem.dmdg[modelo_gerador]["inercia"].strip() != ""
                            else 100.0
                        )
                        d = (
                            float(anatem.dmdg[modelo_gerador]["amortecimento"])
                            if anatem.dmdg[modelo_gerador]["amortecimento"].strip()
                            != ""
                            else 1.0
                        )
                        tllq = (
                            float(anatem.dmdg[modelo_gerador]["tau_q0_double_prime"])
                            if anatem.dmdg[modelo_gerador][
                                "tau_q0_double_prime"
                            ].strip()
                            != ""
                            else 0.0
                        )
                        ag = (
                            float(anatem.dcst[modelo_gerador]["parametro_1"])
                            if (
                                cs != ""
                                and anatem.dcst[modelo_gerador]["parametro_1"].strip()
                                != ""
                            )
                            else 0.0
                        )
                        bg = (
                            float(anatem.dcst[modelo_gerador]["parametro_2"])
                            if (
                                cs != ""
                                and anatem.dcst[modelo_gerador]["parametro_2"].strip()
                                != ""
                            )
                            else 0.0
                        )
                        cg = (
                            float(anatem.dcst[modelo_gerador]["parametro_3"])
                            if (
                                cs != ""
                                and anatem.dcst[modelo_gerador]["parametro_3"].strip()
                                != ""
                            )
                            else 0.0
                        )
                        organon.file.write(
                            "!SM04  (--Xd-) (-Xld-) (-Xlld-) (--Xq-) (-Xlq-) (-Xllq-) (--Ra-) (-Sbase-) (--Xl-) (-Xt-) (-Tld-) (-Tlld-) (-Tlq-) (-H-) (-D-) (-Tllq-) (---Ag-) (---Bg-) (---Cg-)\n"
                        )
                        organon.file.write(
                            f"       {xd:>7.5f} {xld:>7.5f} {xlld:>8.5f} {xq:>7.5f} {xlq:>7.5f} {xllq:>8.5f} {ra:>7.5f} {sb:>9.2f} {xl:>7.5f} {xt:>6.1f} {tld:>7.4f} {tlld:>8.4f} {tlq:>7.4f} {h:>5.4f} {d:>5.4f} {tllq:>8.4f} {ag:>8.7f} {bg:>8.7f} {cg:>8.7f} /\n"
                        )
                    elif dmdg == "SM05":
                        xd = (
                            float(anatem.dmdg[modelo_gerador]["l_d"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d"].strip() != ""
                            else 0.0
                        )
                        xld = (
                            float(anatem.dmdg[modelo_gerador]["l_d_prime"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_prime"].strip() != ""
                            else 0.0
                        )
                        xlld = (
                            float(anatem.dmdg[modelo_gerador]["l_d_double_prime"])
                            * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_double_prime"].strip()
                            != ""
                            else 0.0
                        )
                        xq = (
                            float(anatem.dmdg[modelo_gerador]["l_q"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_q"].strip() != ""
                            else 0.0
                        )
                        xlq = (
                            float(anatem.dmdg[modelo_gerador]["l_q_prime"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_q_prime"].strip() != ""
                            else 0.0
                        )
                        xllq = (
                            float(anatem.dmdg[modelo_gerador]["l_d_double_prime"])
                            * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_d_double_prime"].strip()
                            != ""
                            else 0.0
                        )
                        ra = (
                            float(anatem.dmdg[modelo_gerador]["resistencia_armadura"])
                            * 1e-2
                            if not anatem.dmdg[modelo_gerador][
                                "resistencia_armadura"
                            ].strip()
                            == ""
                            else 0.0
                        )
                        sb = (
                            float(anatem.dmdg[modelo_gerador]["potencia_nominal"])
                            if anatem.dmdg[modelo_gerador]["potencia_nominal"].strip()
                            != ""
                            else 100.0
                        )
                        xl = (
                            float(anatem.dmdg[modelo_gerador]["l_l"]) * 1e-2
                            if anatem.dmdg[modelo_gerador]["l_l"].strip() != ""
                            else 0.0
                        )
                        xt = 0.0
                        tld = (
                            float(anatem.dmdg[modelo_gerador]["tau_d0_prime"])
                            if anatem.dmdg[modelo_gerador]["tau_d0_prime"].strip() != ""
                            else 0.0
                        )
                        tlld = (
                            float(anatem.dmdg[modelo_gerador]["tau_d0_double_prime"])
                            if anatem.dmdg[modelo_gerador][
                                "tau_d0_double_prime"
                            ].strip()
                            != ""
                            else 0.0
                        )
                        tlq = (
                            float(anatem.dmdg[modelo_gerador]["tau_q0_prime"])
                            if anatem.dmdg[modelo_gerador]["tau_q0_prime"].strip() != ""
                            else 0.0
                        )
                        h = (
                            float(anatem.dmdg[modelo_gerador]["inercia"])
                            if anatem.dmdg[modelo_gerador]["inercia"].strip() != ""
                            else 100.0
                        )
                        d = (
                            float(anatem.dmdg[modelo_gerador]["amortecimento"])
                            if anatem.dmdg[modelo_gerador]["amortecimento"].strip()
                            != ""
                            else 1.0
                        )
                        tllq = (
                            float(anatem.dmdg[modelo_gerador]["tau_q0_double_prime"])
                            if anatem.dmdg[modelo_gerador][
                                "tau_q0_double_prime"
                            ].strip()
                            != ""
                            else 0.0
                        )
                        p1 = (
                            float(anatem.dcst[cs]["parametro_1"])
                            if (
                                cs != ""
                                and anatem.dcst[cs]["parametro_1"].strip() != ""
                            )
                            else 0.0
                        )
                        p2 = (
                            float(anatem.dcst[modelo_gerador]["parametro_2"])
                            if (
                                cs != ""
                                and anatem.dcst[modelo_gerador]["parametro_2"].strip()
                                != ""
                            )
                            else 0.0
                        )
                        p3 = (
                            float(anatem.dcst[modelo_gerador]["parametro_3"])
                            if (
                                cs != ""
                                and anatem.dcst[modelo_gerador]["parametro_3"].strip()
                                != ""
                            )
                            else 0.0
                        )
                        sm1 = float(p1 * exp(p2 - p2 * p3))
                        sm2 = float(p1 * exp(p2 * 1.2 - p2 * p3))
                        organon.file.write(
                            "!SM05  (--Xd-) (-Xld-) (-Xlld-) (--Xq-) (-Xlq-) (-Xllq-) (--Ra-) (-Sbase-) (--Xl-) (-Xt-) (-Tld-) (-Tlld-) (-Tlq-) (-H-) (-D-) (-Tllq-) (-S1.0-) (-S1.2-)\n"
                        )
                        organon.file.write(
                            f"       {xd:>7.5f} {xld:>7.5f} {xlld:>8.5f} {xq:>7.5f} {xlq:>7.5f} {xllq:>8.5f} {ra:>7.5f} {sb:>9.2f} {xl:>7.5f} {xt:>6.1f} {tld:>7.4f} {tlld:>8.4f} {tlq:>7.4f} {h:>5.4f} {d:>5.4f} {tllq:>8.4f} {sm1:>8.7f} {sm2:>8.7f} /\n"
                        )
                    if avr == "AVR04":
                        avr = anatem.dmaq[value][ndmaq]["modelo_regulador_tensao"]
                        ka = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#KA")
                        ]
                        ta = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#TA")
                        ]
                        kf = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#KF")
                        ]
                        tf = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#TF")
                        ]
                        te = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#TE")
                        ]
                        ke = anatem.dcdu[avr]["defpar_valor"][
                            anatem.dcdu[avr]["defpar_nome"].index("#KE")
                        ]
                        min = anatem.dcdu[avr]["defval_parametro_d1"][
                            anatem.dcdu[avr]["defval_variavel"].index("Lmin")
                        ]
                        max = anatem.dcdu[avr]["defval_parametro_d1"][
                            anatem.dcdu[avr]["defval_variavel"].index("Lmax")
                        ]
                        organon.file.write(
                            "!AVR04 (-Ka-) (-Ta>0-) (-Ke-) (-Te-) (-Tc-) (-Tb>0-) (-Kf-) (-Tf-) (-Vmin-) (-Vmax-) (-E1-) (-S[E1]-) (-E2-) (-S[E2]-) (-Tc1-) (-Tb1-)\n"
                        )
                        organon.file.write(
                            f"       {ka:>6} {ta:>8} {ke:>6} {te:>6} {6*' ':>6} {8*' ':>8} {kf:>6} {tf:>6} {min:>8} {max:>8} {6*' ':>6} {9*' ':>9} {6*' ':>6} {9*' ':>9} {7*' ':>7} {7*' ':>7} /\n"
                        )
                    if pss == "PSS01":
                        pss = anatem.dmaq[value][ndmaq]["modelo_estabilizador"]
                        tw = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#TW1")
                        ]
                        t1 = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#TN1")
                        ]
                        t2 = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#TN1")
                        ]
                        t3 = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#TD1")
                        ]
                        t4 = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#TD1")
                        ]
                        k1 = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#KP1")
                        ]
                        min = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#LMIN")
                        ]
                        max = anatem.dcdu[pss]["defpar_valor"][
                            anatem.dcdu[pss]["defpar_nome"].index("#LMAX")
                        ]
                        organon.file.write(
                            "!PSS01 (-T1-) (-T2-) (-T3-) (-T4-) (-T5-) (-T6-) (-Tw-) (-K1-) (-Vmin-) (-Vmax-) (-Type-)\n"
                        )
                        organon.file.write(
                            f"       {t1} {t2} {t3} {t4} {' '} {' '} {tw} {k1} {min} {max} {' '} /\n"
                        )
                    if gov.strip() == "GOV04":
                        gov = anatem.dmaq[value][ndmaq]["modelo_regulador_velocidade"]
                        rp = anatem.drgv[gov]["estatismo"]
                        at = anatem.drgv[gov]["ganho_turbina"]
                        qnl = anatem.drgv[gov]["vazao_noload"]
                        tw = float(anatem.drgv[gov]["cte_tempo_agua"])
                        tg = anatem.drgv[gov]["cte_tempo_servomotor"]
                        tv = "0.001"
                        tp1 = anatem.drgv[gov]["cte_tempo_filtragem"]
                        tp2 = "0.001"
                        td = "0."
                        g1x = "99."
                        g1n = "-99."
                        g2x = "99."
                        g2n = "-99."
                        g3x = anatem.drgv[gov]["limite_maximo"]
                        g3n = anatem.drgv[gov]["limite_minimo"]
                        kd = "1."
                        h = float(anatem.dmdg[modelo_gerador]["inercia"])
                        kp = (h * tw) / (2.3 - (tw - 1) * 0.15)
                        ki = (h) / (
                            (2.3 - (tw - 1) * 0.15) * (5 - (tw - 1) * 0.5) * tw * tw
                        )
                        organon.file.write(
                            "!GOV04 (-Rp-) (--Kp-) (--Ki-) (--Kd-) (--Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n"
                        )
                        organon.file.write(
                            f"       {rp:>6} {kp:>7.5f} {ki:>7.5f} {kd:>7} {td:>7} {tp1:>7} {tp2:>9} {g1n:>9} {g1x:>9} {tv:>8} {g2n:>9} {g2x:>9} {tg:>8} {g3n:>9} {g3x:>9} {tw:>6.4f} {at:>6} {qnl:>7} /\n"
                        )
                    elif gov.strip() == "GOV09":
                        gov = anatem.dmaq[value][ndmaq]["modelo_regulador_velocidade"]
                        r = anatem.drgv[gov]["estatismo"]
                        t1 = anatem.drgv[gov]["cte_tempo_regulador"]
                        pmax = anatem.drgv[gov]["limite_maximo"]
                        pmin = anatem.drgv[gov]["limite_minimo"]
                        t2 = anatem.drgv[gov]["cte_tempo_1"]
                        t3 = anatem.drgv[gov]["cte_tempo_reaquecimento"]
                        organon.file.write(
                            "!GOV09 (-R-) (-T1-) (-Pmax-) (-Pmin-) (-T2-) (-T3-)\n"
                        )
                        organon.file.write(
                            f"       {r:>4} {t1:>6} {pmax:>8} {pmin:>8} {t2:>6} {t3:>6} /\n"
                        )
                organon.file.write("!\n")
                organon.file.write("!\n")
                ndmaq += 1


def prwraw(
    anarede,
    psse,
):
    """escrita de dados de máquina síncrona no formato PSS/E (.pwf -> .raw)

    Args:
        anarede:
    """
    pssepath = pssefolder(
        anarede,
    )
    rawfile = realpath(pssepath + anarede.system[:-4] + ".raw")
    psse.file = open(rawfile, "w", encoding="latin-1")
    psse.file.write(
        f"{0:>6d},{anarede.cte['SBSE']:>8.1f},{32:>6d},{0:>6d},{0:>6d},{anarede.cte['FBSE']:>8.2f} / PSS(R)E 32\n"
    )
    (
        psse.file.write(f" {anarede.titu['ruler'].strip():>60}")
        if len(anarede.titu["ruler"].strip()) <= 60
        else psse.file.write(
            f" {anarede.titu['ruler'].strip()[:60]}\n {anarede.titu['ruler'].strip()[60:120]}\n"
        )
    )

    loaddata = ""
    fixedshuntdata = ""
    generatorsdata = ""
    for idx, value in anarede.dbarDF.iterrows():
        dgbt = anarede.dgbtDF[
            anarede.dgbtDF.grupo == value.grupo_base_tensao
        ].tensao.values[0]
        code = (
            1
            if value.tipo == 0 and value.estado == "L"
            else (
                2
                if value.tipo == 1 and value.estado == "L"
                else (
                    3
                    if value.tipo == 2 and value.estado == "L"
                    else 4 if value.estado == "D" else None
                )
            )
        )
        psse.file.write(
            f"{value.numero:>6d},'{value.nome:<12}',{dgbt:>9.4f},{code:>3d},{value.area:>5d},{1:>5d},{1:>5d},{value.tensao*1e-3:>11.6f},{value.angulo:>11.4f}\n"
        )
        loaddata += (
            f"{value.numero:>6d},'1 ',{1:2d},{value.area:>4d},{1:>5d},{value.demanda_ativa:>11.3f},{value.demanda_reativa:>11.3f},{0:>10.3f},{0:>12.3f},{0:>12.3f},{0:>10.3f},{1:>4d},{1:>2d}\n"
            if value.demanda_ativa != 0 or value.demanda_reativa != 0
            else ""
        )
        fixedshuntdata += (
            f"{value.numero:>6d},' 1 ',{1:3d},{0:>11.3f},{value.shunt_barra:>11.3f}\n"
            if value.shunt_barra != 0
            else ""
        )
        generatorsdata += (
            f"{value.numero:>6d},'1 ',{value.potencia_ativa:>10.3f},{value.potencia_reativa:>11.3f},{value.potencia_reativa_maxima:>11.3f},{value.potencia_reativa_minima:>11.3f},{value.tensao*1e-3:>10.4f},{value.barra_controlada:>7},{anarede.cte['SBSE']:>11.3f},{0:>11.4f},{1:>11.4f},{0:>10.4f},{0:>10.4f},{1:>10.4f},{1:>3d},{100:>8.1f},{value.potencia_ativa:>12.3f},{value.potencia_ativa:>12.3f},{1:>5d},{1:>9.3f},{0:>6d},{0:>9.3f},{0:>6d},{0:>9.3f},{0:>6d},{0:>9.3f},{0:>3d},{0:>11.3f}/\n"
            if code != 1
            else ""
        )
    psse.file.write(" 0  / END OF BUS DATA, BEGIN LOAD DATA\n")
    psse.file.write(loaddata)
    psse.file.write(" 0  / END OF LOAD DATA, BEGIN FIXED SHUNT DATA\n")
    psse.file.write(fixedshuntdata)
    psse.file.write(" 0  / END OF FIXED SHUNT DATA, BEGIN GENERATOR DATA\n")
    psse.file.write(generatorsdata)
    psse.file.write(" 0  / END OF GENERATOR DATA, BEGIN BRANCH DATA\n")
    transformersdata = ""
    for idx, value in anarede.dlinDF.iterrows():
        st = 1 if value.estado == "L" else 0
        if value.barra_controlada < 0 and abs(value.barra_controlada) == value.de:
            bc = value.para
        elif value.barra_controlada < 0 and abs(value.barra_controlada) == value.para:
            bc = value.de
        elif value.barra_controlada > 0:
            bc = value.barra_controlada
        else:
            bc = 0
        tn = value.tap_minimo if value.tap_minimo != 0 else value.tap.real
        tx = value.tap_maximo if value.tap_maximo != 0 else value.tap.real
        td = value.tap_defasagem if value.tap_defasagem != 0 else 0
        cod1 = 1 if bc != 0 else 0
        cont1 = bc if bc != 0 else 0
        vx = (
            anarede.dbarDF[anarede.dbarDF.numero == bc].tensao.values[0]
            if bc != 0
            else 0
        )
        vn = (
            anarede.dbarDF[anarede.dbarDF.numero == bc].tensao.values[0]
            if bc != 0
            else 0
        )
        nome_de = anarede.dbarDF[anarede.dbarDF.numero == value.de].nome.values[0]
        (
            psse.file.write(
                f"{value.de:>6d},{value.para:>6d},'{value.circuito:02d}',{value.resistencia:>12.4E},{value.reatancia:>13.4E},{value.susceptancia*2:>10.4f},{value.capacidade_normal:>12.2f},{value.capacidade_emergencial:>12.2f},{value.capacidade_equipamento:>12.2f},{0:>10.5f},{0:>10.5f},{0:>10.5f},{0:>10.5f},{1:>3d},{1:>3d},{0:>9.2f},{1:>4d},{1:>9.4f}\n"
            )
            if value.estado and value.tap.real == 0
            else ""
        )
        transformersdata += (
            f"{value.de:>6d},{value.para:>7d},{0:>7d},'{value.circuito:02d}',{1:>2d},{1:>2d},{1:>2d},{0:>11.3f},{0:>11.3f},{1:>2d}, '{nome_de:12}',{1:>2d},{1:>5d},{1:>10.5f}\n {value.resistencia:>11.5E},{value.reatancia:>13.5E},{anarede.cte['SBSE']:>11.3E}\n {value.tap.real:>8.4f},{0:>10.4f},{td:>10.4f},{value.capacidade_normal:>10.2f},{value.capacidade_emergencial:>10.2f},{value.capacidade_equipamento:>10.2f},{cod1:>3d},{cont1:>8d},{tx:>13.5f},{tn:>13.5f},{vx:>13.5f},{vn:>13.5f},{value.numero_taps:>3d},{0:>3d},{0:>10.5f},{0:>10.5f}\n {1:>8.5f},{0:>10.5f}\n"
            if value.estado and value.tap.real != 0
            else ""
        )
    psse.file.write(" 0  / END OF BRANCH DATA, BEGIN TRANSFORMER DATA\n")
    psse.file.write(transformersdata)
    psse.file.write(" 0  / END OF TRANSFORMER DATA, BEGIN AREA DATA\n")
    for idx, value in anarede.dareDF.iterrows():
        psse.file.write(
            f"{value.numero:>6d},{0:>6d},{0:>10.3f},{10:>10.3f}, '{value.nome[:10]:10}'\n"
        )
    psse.file.write(" 0  / END OF AREA DATA, BEGIN TWO-TERMINAL DC DATA\n")
    psse.file.write(" 0  / END OF TWO-TERMINAL DC DATA, BEGIN VSC DATA\n")
    psse.file.write(" 0  / END OF VSC DATA, BEGIN IMPEDANCE CORRECTION DATA\n")
    psse.file.write(
        " 0 / END OF IMPEDANCE CORRECTION DATA, BEGIN MULTI-TERMINAL DC DATA\n"
    )
    psse.file.write(
        " 0 / END OF MULTI-TERMINAL DC DATA, BEGIN MULTI-SECTION LINE DATA\n"
    )
    psse.file.write(" 0 / END OF MULTI-SECTION LINE DATA, BEGIN ZONE DATA\n")
    psse.file.write(" 0 / END OF ZONE DATA, BEGIN INTER-AREA TRANSFER DATA\n")
    psse.file.write(" 0 / END OF INTER-AREA TRANSFER DATA, BEGIN OWNER DATA\n")
    psse.file.write(" 0 / END OF OWNER DATA, BEGIN FACTS CONTROL DEVICE DATA\n")
    psse.file.write(
        " 0 / END OF FACTS CONTROL DEVICE DATA, BEGIN SWITCHED SHUNT DATA\n"
    )
    psse.file.write(" 0 / END OF SWITCHED SHUNT DATA\n")
    psse.file.write("Q / END OF DATA\n")
    psse.file.close()


def prwdyr(
    anarede,
    anatem,
    psse,
):
    """escrita de dados de máquina síncrona no formato PSS/E (.stb -> .dyr)

    Args:
        anarede:
        anatem
        psse
    """
    pssepath = pssefolder(
        anarede,
    )
    rawfile = realpath(pssepath + anarede.system[:-4] + ".dyr")
    psse.file = open(rawfile, "w", encoding="latin-1")
    psse.file.write("@! PSSE Generator Models\n")
    psse.file.write("@!\n")
    gencls = ""
    gensae = ""
    genroe = ""
    excitation = ""
    governor = ""
    stabilizer = ""
    for key in anatem.dmaq.keys():
        try:
            barra = int(key)
            i = 0
            while i < len(anatem.dmaq[key]):
                gerador = anatem.dmaq[key][i]["modelo_gerador"]
                gendata = anatem.dmdg[gerador]
                genmodel = anatem.dmdg[gerador]["modelo"]
                amortecimento = (
                    0
                    if gendata["amortecimento"].strip() == ""
                    else float(gendata["amortecimento"])
                )
                saturacao = (
                    gendata["curva_saturacao"]
                    if "curva_saturacao" in gendata.keys()
                    else ""
                )
                if saturacao.strip():
                    sat1 = float(anatem.dcst[saturacao]["parametro_1"]) * exp(
                        float(anatem.dcst[saturacao]["parametro_2"])
                        - float(anatem.dcst[saturacao]["parametro_2"])
                        * float(anatem.dcst[saturacao]["parametro_3"])
                    )
                    sat12 = float(anatem.dcst[saturacao]["parametro_1"]) * exp(
                        float(anatem.dcst[saturacao]["parametro_2"]) * 1.2
                        - float(anatem.dcst[saturacao]["parametro_2"])
                        * float(anatem.dcst[saturacao]["parametro_3"])
                    )
                else:
                    sat1 = 0.105
                    sat12 = 0.318
                if genmodel == "MD01":
                    gencls += f"{barra:>7d} 'GENCLS' '{anatem.dmaq[key][i]['grupo']}' {float(gendata['inercia'])}  {amortecimento} /\n"
                elif genmodel == "MD02":
                    gensae += f"{barra:>7d} 'GENSAE' '{anatem.dmaq[key][i]['grupo']}' {float(gendata['tau_d0_prime'])}  {float(gendata['tau_d0_double_prime'])}  {float(gendata['tau_q0_double_prime'])}  {float(gendata['inercia'])}  {amortecimento}  {float(gendata['l_d'])*1e-2}  {float(gendata['l_q'])*1e-2}  {float(gendata['l_d_prime'])*1e-2}  {float(gendata['l_d_double_prime'])*1e-2}  {float(gendata['l_l'])*1e-2}  {sat1}  {sat12} /\n"
                elif genmodel == "MD03":
                    genroe += f"{barra:>7d} 'GENROE' '{anatem.dmaq[key][i]['grupo']}' {float(gendata['tau_d0_prime'])}  {float(gendata['tau_d0_double_prime'])}  {float(gendata['tau_q0_prime'])}  {float(gendata['tau_q0_double_prime'])}  {float(gendata['inercia'])}  {amortecimento}  {float(gendata['l_d'])*1e-2}  {float(gendata['l_q'])*1e-2}  {float(gendata['l_d_prime'])*1e-2}  {float(gendata['l_q_prime'])*1e-2}  {float(gendata['l_d_double_prime'])*1e-2}  {float(gendata['l_l'])*1e-2}  {sat1}  {sat12} /\n"
                avr = anatem.dmaq[key][i]["modelo_regulador_tensao"]
                gov = anatem.dmaq[key][i]["modelo_regulador_velocidade"]
                if (
                    gov.strip()
                    and anatem.dmaq[key][i]["modelo_regulador_velocidade_u"] != "u"
                ):
                    govdata = anatem.drgv[gov]
                    if anatem.drgv[gov]["modelo"].strip() == "MD01":
                        governor += f"{barra:>7d} 'HYGOV' '{anatem.dmaq[key][i]['grupo']}' {float(govdata['estatismo'])}  {float(govdata['estatismo_transitorio'])}  {float(govdata['cte_tempo_regulador'])}  {float(govdata['cte_tempo_filtragem'])}  {float(govdata['cte_tempo_servomotor'])}  {0.}  {float(govdata['limite_maximo'])}  {float(govdata['limite_minimo'])}  {float(govdata['cte_tempo_agua'])}  {float(govdata['ganho_turbina'])}  {float(govdata['amortecimento_turbina'])}  {float(govdata['vazao_noload'])} /\n"
                    elif anatem.drgv[gov]["modelo"].strip() == "MD02":
                        governor += f"{barra:>7d} 'TGOV1' '{anatem.dmaq[key][i]['grupo']}' {float(govdata['estatismo'])}  {float(govdata['cte_tempo_regulador'])}  {float(govdata['limite_maximo'])}  {float(govdata['limite_minimo'])}  {float(govdata['cte_tempo_1'])}  {float(govdata['cte_tempo_reaquecimento'])}  {float(govdata['amortecimento_turbina'])} /\n"
                else:
                    pass
                pss = anatem.dmaq[key][i]["modelo_estabilizador"]
                if pss.strip() and anatem.dmaq[key][i]["modelo_estabilizador_u"] != "u":
                    pass
                elif (
                    pss.strip() and anatem.dmaq[key][i]["modelo_estabilizador_u"] == "u"
                ):
                    stabilizer += f"{barra:>7d} 'IEEEST' '{anatem.dmaq[key][i]['grupo']}' {1}  {0}  {0}  {0}  {0}  {0}  {0}  {0}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TN1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TD1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TN1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TD1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TW1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#TW1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#KP1')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#LMAX')])}  {float(anatem.dcdu[pss]['defpar_valor'][anatem.dcdu[pss]['defpar_nome'].index('#LMIN')])}  {0}  {0} /\n"

                if (
                    anarede.dbarDF.loc[anarede.dbarDF.numero == barra, "tipo"].values[0]
                    == 1
                ):
                    excitation += f"{barra:>7d} 'IEEET1' '{anatem.dmaq[key][i]['grupo']}' 0.00  100  0.05  8.00  -4.00  1.00  1.50  0.30  3.00  0  0.5  0.35  0.8  0.35 /\n"
                elif (
                    anarede.dbarDF.loc[anarede.dbarDF.numero == barra, "tipo"].values[0]
                    == 2
                ):
                    excitation += f"{barra:>7d} 'IEEET1' '{anatem.dmaq[key][i]['grupo']}' 0.00  100  0.05  20  -20  1.00  1.50  0.30  3.00  0  0.5  0.35  0.8  0.35 /\n"
                i += 1
        except:
            pass
    if gencls != "":
        psse.file.write("@! GENCLS\n")
        psse.file.write(gencls)
    if gensae != "":
        psse.file.write("@! GENSAE\n")
        psse.file.write(gensae)
    if genroe != "":
        psse.file.write("@! GENROE\n")
        psse.file.write(genroe)
    psse.file.write("@! PSSE Excitation System Models\n")
    psse.file.write(excitation)
    psse.file.write("@! PSSE Governor Models\n")
    psse.file.write(governor)
    psse.file.write("@! PSSE PSSModels\n")
    psse.file.write(stabilizer)
    regc = ""
    reec = ""
    repc = ""
    torque = ""
    pitch = ""
    aerodynamic = ""
    drivetrain = ""
    for key in anatem.dfnt.keys():
        try:
            barra = int(key)
            if anatem.dfnt[key]["modelo_fonte_u"]:
                # gendata = anatem.dcdu[anatem.dfnt[key]['modelo_fonte'].strip()]
                regc += f"{barra:>7d} 'REGCA1' '{anatem.dfnt[key]['grupo']}' 1  0.02  99  0.90  0.50  1.20  1.20  0.2  0.05  -1.30  0.02  1.50  99  -99  1 /\n"
                reec += f"{barra:>7d} 'REECA1' '{anatem.dfnt[key]['grupo']}' 0  0  1  1  0  1  0.85  1.2  0.01  -0.05  0.05  0.8  0.75  -0.75  0  0  0  0  0.05  0.436  -0.436  1.2  0.8  1  10  1  10  0  8  99  -99  1.2  0.04  1.11  0.02  0  0.75  0.2  0.750001  0.5  0.750002  1  0.750003  0.2  1.11  0.5  1.110001  0.75  1.110002  1  1.110003 /\n"
                repc += f"{barra:>7d} 'REPCA1' '{anatem.dfnt[key]['grupo']}' {barra:>7d}{barra:>7d}  55412  '01'  0  0 0  0.02  18.0  5.00  0.00  0.05  0.70  0.00  0.00  0.00  0.10  -0.10  -0.00333  0.00333  0.436  -0.436  0.00  0.00  0.02  -0.0006  0.0006  999  -999  1  0  0.00  0.00  0.00 /\n"
                torque += (
                    f"{barra:>7d} 'WTTQA1' '{anatem.dfnt[key]['grupo']}' 1  3.00  0.60  0.05  30  1.20  0.08  0.20  0.69  0.40  0.78  0.60  0.98  0.74  1.20  0 /\n"
                    if "WT3"
                    in anatem.dcdu[anatem.dfnt[key]["modelo_fonte"].strip()]["nome"]
                    else ""
                )
                pitch += (
                    f"{barra:>7d} 'WTPTA1' '{anatem.dfnt[key]['grupo']}' 5.00  150  30.0  3.00  0.00  0.30  27.0  0.00  10.0  -10.0 /\n"
                    if "WT3"
                    in anatem.dcdu[anatem.dfnt[key]["modelo_fonte"].strip()]["nome"]
                    else ""
                )
                aerodynamic += (
                    f"{barra:>7d} 'WTARA1' '{anatem.dfnt[key]['grupo']}' 0.007  0.00 /\n"
                    if "WT3"
                    in anatem.dcdu[anatem.dfnt[key]["modelo_fonte"].strip()]["nome"]
                    else ""
                )
                drivetrain += (
                    f"{barra:>7d} 'WTDTA1' '{anatem.dfnt[key]['grupo']}' 4.754  0  0.869  37.35  1.5 /\n"
                    if "WT3"
                    in anatem.dcdu[anatem.dfnt[key]["modelo_fonte"].strip()]["nome"]
                    else ""
                )
        except:
            pass
    psse.file.write("@! PSSE RE Generator Models\n")
    psse.file.write(regc)
    psse.file.write("@! PSSE RE Electrical Control Models\n")
    psse.file.write(reec)
    psse.file.write("@! PSSE RE PPC Models\n")
    psse.file.write(repc)
    psse.file.write(
        "@! PSSE Generic Torque controller for Type 3 wind machines Models\n"
    )
    psse.file.write(torque)
    psse.file.write(
        "@! PSSE Generic Pitch Control Model for Type 3 Wind Generator Models\n"
    )
    psse.file.write(pitch)
    psse.file.write(
        "@! PSSE Generic Aerodynamic Model for Type 3 wind machine Models\n"
    )
    psse.file.write(aerodynamic)
    psse.file.write(
        "@! PSSE Generic Drive Train Model for Type 3 and Type 4 Wind Machines Models\n"
    )
    psse.file.write(drivetrain)
    psse.file.close()
