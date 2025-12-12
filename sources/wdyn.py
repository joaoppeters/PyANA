# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import exp


def wdsm(
    anarede,
    anatem,
    organon,
):
    """escrita de dados de máquina síncrona no formato ORGANON (.stb -> .dyn)
    
    Args:
        anatem:
        organon:        
    """
    ## Inicialização
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
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip():
                        if anatem.drgv[anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()]['modelo'] == "MD01":
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
                    else:
                        gov = 5*" "
                    organon.file.write(f"{dmdg} {nome}\n")
                    organon.file.write("! (--Bus--) (--ID--) (--Gov--) (--Bus Name--)\n")
                    organon.file.write(f"  {numero:>9} {id:>8} {gov:>9} {' ':>14}\n")
                    organon.file.write("!SM01  (-Xld-) (-Ra-) (-Sb-) (-Xt-)   (-H-) (-D-)\n")
                    organon.file.write(f"       {xld:>7.3f} {ra:>6.3f} {sb:>6.2f} {xt:>6.3f} {h:>5.3f} {d:>5.3f} /\n")
                    if gov.strip():
                        if gov == "GOV04":
                            organon.file.write("!GOV04 (-Rp-) (-Kp-) (-Ki-) (-Kd-) (-Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n")
                        elif gov == "GOV09":
                            organon.file.write("!GOV09 (-R-) (-T1-) (-Pmax-) (-Pmin-) (-T2-) (-T3-)\n")
                else:
                    dmdg = "SM0" + str(int(dmdg) + 2)
                    cs = anatem.dmdg[modelo_gerador]['curva_saturacao'].strip()
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_tensao'].strip():
                        avr = "AVR04"
                    else:
                        avr = 5*" "
                    if anatem.dmaq[value][ndmaq]['modelo_estabilizador'].strip():
                        pss = "PSS01"
                    else:
                        pss = 5*" "
                    if anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip():
                        if anatem.drgv[anatem.dmaq[value][ndmaq]['modelo_regulador_velocidade'].strip()]['modelo'] == "MD01":
                            gov = "GOV04"
                        else:
                            gov = "GOV09"
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
                    if gov.strip():
                        if gov == "GOV04":
                            organon.file.write("!GOV04 (-Rp-) (-Kp-) (-Ki-) (-Kd-) (-Td-) (-Tp1-) (-Tp2>0-) (-G1min-) (-G1max-) (-Tv>0-) (-G2min-) (-G2max-) (-Tq>0-) (-G3min-) (-G3max-) (-Tw-) (-At-) (-qnl-)\n")
                        elif gov == "GOV09":
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
    