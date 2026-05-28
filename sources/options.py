# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros
from pandas import DataFrame


def optionspwf(
    anarede,
):
    """configuracao de variaveis para processos de convergencia em analise estatica de fluxos de potencia
    determinacao dos valores padrao das constantes, variaveis de controle, variaveis de execucao, variaveis de monitoramento e variaveis de relatorios

    Args
        anarede:
    """
    anarede.cte = dict(
        {
            "BMVA": 100.0,  # base de potencia para o sistema CA
            "DASE": 100.0,  # base de potencia default para o sistema CC
            "TEPA": 1e-3,  # tolerancia de convergencia de potencia ativa
            "TEPR": 1e-3,  # tolerancia de convergencia de potencia reativa
            "TLPR": 1e-3,  # tolerância para limite de geracao de potencia reativa
            "TLVC": 5e-3,  # tolerância para tensoes controladas
            "TLTC": 1e-4,  # tolerância para limite de tap de transformador
            "TETP": 5e-2,  # tolerância para erro de intercâmbio de potencia ativa entre areas
            "TBPA": 5e-2,  # tolerância para erro de redistribuicao de potencia ativa em contingencias de geracao/carga
            "TSFR": 1e-4,  # tolerância para deteccao de separacao fisica da rede eletrica
            "TUDC": 1e-5,  # tolerância de convergencia do erro de tensao em barra CC
            "TADC": 1e-4,  # tolerância para limite de ângulo de disparo/extincao de conversor
            "TPST": 2e-3,  # tolerância de erro de potencia reativa para aplicacao de variacao automatica de tap de transformador
            "QLST": 4e-3,  # tolerância de erro de potencia reativa para aplicacao de controle de limite de geracao de potencia reativa
            "EXST": 4e-3,  # tolerância de erro de potencia ativa para aplicacao de controle de intercâmbio de potencia ativa entre areas
            "TLPP": 1e-2,  # tolerância para a capacidade de carregamento de circuitos
            "TSBZ": 1e-4,  # tolerância para deteccao de variacao nula de fluxo de potencia ativa nos circuitos do sistema externo
            "TSBA": 5e-2,  # tolerância para deteccao de pequenas variacoes de fluxo de potencia ativa nos circuitos do sistema externo
            "PGER": 0.3,  # percentagem de geracao de potencia ativa a ser removida dos geradores do sistema interno para o calculo das variacoes de fluxo de potencia ativa nos circuitos do sistema externo
            "VFLD": 0.7,  # valor de tensao abaixo do qual a parcela de potencia constante das cargas funcionais passa a ser modelada como uma impedância constante
            "VART": 5e-2,  # variacao da tensao (em relacao ao caso base) a partir da qual uma barra passa a ser automaticamente monitorada no problema de fluxo de potencia continuado
            "TSTP": 33,  # número de steps do transformador com tap discreto
            "NDIR": 20,  # número de direcoes utilizado no processo de construcao da regiao de seguranca
            "STIR": 1,  # fator de divisao do passo atual de transferencia de geracao de potencia ativa quando ocorre alguma violacao no processo de construcao da regiao de seguranca
            "STTR": 5e-2,  # passo de transferencia de geracao de potencia ativa utilizado no processo de construcao da regiao de seguranca
            "TRPT": 1,  #  percentagem de geracao de potencia ativa utilizado no processo de construcao da regiao de seguranca
            "ZMIN": 1e-5,  # valor minimo do modulo de impedância dos circuitos CA
            "VDVN": 0.4,  # tensao minima para teste de divergencia automatica do caso
            "ICMN": 5e-4,  # valor minimo do incremento automatico de carga (utilizado como criterio de parada do metodo de fluxo de potencia continuado)
            "BFPO": 1e-2,  # valor minimo de injecao de potencia reativa de um banco shunt alocado pelo programa flupot
            "ZMAX": 5e2,  # tensao minima para teste de divergencia do caso
            "VDVM": 2.0,  # tensao maxima para teste de divergencia do caso
            "ASTP": 0.05,  # valor maximo de correcao de ângulo de fase da tensao durante o processo de solucao
            "VSTP": 5e-2,  # valor maximo de correcao de magnitude da tensao durante o processo de solucao
            "CSTP": 5e-2,  # valor maximo de correcao de susceptância do CSC durante o processo de solucao
            "DMAX": 5,  # numero maximo de vezes consecutivas que o fator de divisao FDIV pode ser aplicado (utilizado como criterio de parada do metodo de fluxo de potencia continuado)
            "TSDC": 0.02,  # valor maximo de correcao do tap do conversor do elo CC durante o processo de solucao
            "ASDC": 1,  # valor maximo de correcao do ângulo de disparo do conversor do elo CC durante o processo de solucao
            "ACIT": 30,  # numero maximo de iteracoes na solucao do fluxo de potencia CA
            "ICIT": 30,  # numero maximo de solucoes do fluxo de potencia a serem calculadas durante a execucao do problema de fluxo de potencia continuado
            "LPIT": 50,  # numero maximo de iteracoes do problema de programacao linear
            "LFLP": 10,  # numero maximo de iteracoes do problema de redespacho de potencia ativa
            "LFIT": 10,  # numero maximo de iteracoes na solucao da interface CA-CC
            "DCIT": 10,  # numero maximo de iteracoes na solucao do fluxo de potencia CC
            "VSIT": 10,  # numero maximo de iteracoes no ajuste da tensao em barra CC
            "LFCV": 1,  # número de iteracoes do metodo desacoplado rapido antes do inicio do processo de solucao pelo metodo de newton raphson
            "PDIT": 10,  # número de iteracoes na estimacao das perdas no modelo de fluxo de potencia linearizado
            "FDIV": 2,  # fator de reducao do incremento automatico de carga quando o problema de fluxo de potencia nao apresenta solucao durante a execucao do programa de fluxo de potencia continuado
            "ICMV": 5e-3,  # tamanho do passo inicial quando o parâmetro de continuacao muda de carregamento para o modulo de tensao
            "APAS": 0.9,  # determina o ponto a partir do qual o tamanho do passo do fluxo de potencia continuado parametrizado sera acelerado (% do carregamento maximo)
            "CPAR": 0.7,  # especifica o ponto de para do fluxo de potencia continuado parametrizado (% do carregamento maximo)
            "VAVT": 2e-2,  # criterio de variacao de tensao para a determinacao da rede complementar
            "VAVF": 5e-2,  # criterio de variacao de fluxo em funcao do carregamento nominal para a determinacao da rede complementar
            "VMVF": 15e-2,  # criterio de variacao de fluxo para a determinacao da rede complementar
            "VPVT": 2e-2,  # criterio de variacao de tensao para a terminacao da rede de simulacao - primeiro criterio
            "VPVF": 5e-2,  # criterio de variacao de fluxo em funcao do carregamento nominal para a determinacao da rede de simulacao - primeiro criterio
            "VPMF": 10e-2,  # criterio de variacao de fluxo para a determinacao da rede de simulacao - primeiro criterio
            # novas constantes adicionadas por JP
            "FBSE": 60.0,  # frequencia base do sep (criado por JP)
            "SIGA": 1e-6,  # tolerância da chave sigmoide SVC-A (criado por JP)
            "SIGQ": 1e-6,  # tolerância da chave sigmoide SVC-Q e QLIM (criado por JP)
            "SIGI": 1e-6,  # tolerância da chave sigmoide SVC-I (criado por JP)
            "SIGV": 1e-6,  # tolerância da chave sigmoide referente à variavel de tensao (criado por JP)
            "SIGK": 1e8,  # variavel de inclinacao da chave sigmoide (criado por JP)
            "FULL": 0,  # Curva completa do fluxo de potencia continuado (criado por JP)
            "VVAR": 1e-6,  # (criado por JP)
            "CTOL": 1e-7,  # tolerância para as variaveis de estado do metodo direto (canizares) (criado por JP)
        }
    )
    try:
        for idx, value in anarede.dcteDF.iterrows():
            anarede.cte[value.constante] = value.valor_constante
    except:
        anarede.dcteDF = DataFrame(
            {
                "constante": list(anarede.cte.keys()),
                "valor_constante": list(anarede.cte.values()),
            }
        )

    if anarede.pwfblock["DINC"]:
        anarede.cte["LMBD"] = anarede.dincDF.loc[0, "passo_incremento_potencia_ativa"]
        anarede.cte["cpfBeta"] = zeros(anarede.nbus)
        if anarede.pwfblock["DGER"]:
            for idx, value in anarede.dgerDF.iterrows():
                # idx = value["numero"] - 1
                anarede.cte["cpfBeta"][idx] = value.fator_participacao

    anarede.ctrl = dict(
        {
            "CPHS": False,
            "CREM": False,
            "CSCA": False,
            "CTAP": False,
            "FREQ": False,
            "QLIM": False,
            "VLIM": False,
        }
    )
    anarede.maskctrlcount = 0
    print("\033[96mOpcoes de controle escolhidas: ", end="")
    try:
        for idx, value in anarede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in anarede.ctrl):
                anarede.ctrl[value.opcao] = True
                anarede.maskctrlcount += 1
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(anarede.ctrl):
            print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")

    anarede.excc = dict(
        {
            "80CO": False,  # relatorios impressos em formato de 80 colunas
            "A0GI": False,  # gravacao automatica do arquivo de saida DGEI.dat durante etapa 1 de utilizacao do software ANAT0
            "ACCC": False,  # forca a reInicializacao do controle de tensao de dois ou mais elos de corrente continua do tipo ccc qie controlam a tensao da mesma barra CA pelo modo de tensao definido no codigo de execucao DCCV
            "ACFP": False,  # executa a analise de casos de fluxo de potencia atraves da impressao de relatorios que contem dados de transformadores que podem causar problemas à convergencia dos casos
            "ACLS": False,  # utilizada em conjunto com o codigo de execucao DANC, permite a especificacao da alteracao do carregamento atraves da linguagem de selecao
            "ADRE": False,  # indica que as restricoes lineares adicionais definidas no codigo de execucao DRES serao consideradas durante a solucao do problema de redespacho de potencia ativa
            "AGRE": False,  # utilizada com o codigo de execucao RELA, em conjunto com as opcoes para relatorios de equipamentos (RBAR, DADB, RLIN, DADL, RGER, RTRA, RLTC, RCSC, DADC, RSHB, RSHL, RBSH, RBSL, RFCR, RFQL), imprime o relatorio apenas dos agregadores e grupos selecionados de acordo com os campo de número de agregador e número de grupo do codigo de execucao DAGR
            "AGRF": False,  # utilizada com o codigo de execucao EXMT e com a opcao de execucao IDSA, atua nas etapas de agrupamento e incremento de geracao da ferramenta de identificacao de subareas e areas de modo a garantir que os elementos selecionados reduzam a folga do circuito de maior fator
            "ALPR": False,  # permite a alteracao da prioridade maxima de ativacao das variaveis de controle
            "AMOT": False,  # apos a execucao do processo de otimizacao pelo codigo de execucao EXOT, adiciona as modificacoes sugeridas pelo processo de otimizacao (FPO) ao caso em memoria
            "AREA": False,  # utilizada com o codigo de execucao RELA, permite selecionar a area ou as areas que serao impressas, de acordo com o campo número do codigo de execucao DARE
            "AREG": False,  # utilizada com o codigo de execucao ARQV, habilita o acrescimo automatico de registros ao arquivo historico
            "ASLK": False,
            "ATCR": False,
            "AUTO": False,
            "BPAR": False,
            "BPSI": False,
            "CBAS": False,
            "CCMT": False,
            "CELO": False,
            "CHAV": False,
            "CILH": False,
            "CINT": False,
            "CIRC": False,
            "CNF1": False,
            "CNF2": False,
            "CNF3": False,
            "CNF4": False,
            "CONT": False,
            "CONV": False,
            "CPB1": False,
            "CPB2": False,
            "CPER": False,
            "CPRI": False,
            "CTGS": False,
            "DIRB": False,
            "DIRT": False,
            "DMAB": False,
            "DMQA": False,
            "DMQR": False,
            "DMRE": False,
            "DPER": False,
            "ELIM": False,
            "EMOF": False,
            "EMRG": False,
            "EQPM": False,
            "ERRC": False,
            "ERRS": False,
            "ETP1": False,
            "ETP2": False,
            "EXPO": False,
            "EXSA": False,
            "FCTE": False,
            "FILE": False,
            "FINT": False,
            "FJAC": False,
            "FLAT": False,
            "FLEX": False,
            "FMCC": False,
            "FMCS": False,
            "FOBJ": False,
            "GICC": False,
            "GRAF": False,
            "GRAV": False,
            "GSAV": False,
            "HIST": False,
            "IANG": False,
            "ICMB": False,
            "ICRV": False,
            "IDSA": False,
            "IERR": False,
            "ILHA": False,
            "IMPO": False,
            "IMPR": False,
            "INDC": False,
            "INDV": False,
            "INIC": False,
            "INJF": False,
            "INMN": False,
            "JUMP": False,
            "LFDC": False,
            "LIST": False,
            "MANU": False,
            "MDEF": False,
            "NEWT": False,
            "NCAP": False,
            "NOVO": False,
            "OPEN": False,
            "ORDP": False,
            "ORDQ": False,
            "PARM": False,
            "PART": False,
            "PCTE": False,
            "PECO": False,
            "PERC": False,
            "PERD": False,
            "PESC": False,
            "PLEL": False,
            "PLTF": False,
            "PLTT": False,
            "PMIN": False,
            "PMVA": False,
            "POPE": False,
            "PVCT": False,
            "PVQV": False,
            "SIMU": False,
            "SNEW": False,
            "SPLI": False,
            "SQLI": False,
            "SQPR": False,
            "STEP": False,
            "STPO": False,
            "SUBS": False,
            "TABE": False,
            "TAPC": False,
            "TAPD": False,
            "TCIR": False,
            "TPER": False,
            "TRB1": False,
            "TRB2": False,
            "TRUN": False,
            "ULG2": False,
            "UNPG": False,
            "VABS": False,
            "VIRG": False,
            "VLCR": False,
            "VLDC": False,
            "VNUL": False,
        }
    )
    print("\033[96mOpcoes de execucao escolhidas: ", end="")
    try:
        for idx, value in anarede.dopcDF.iterrows():
            if (value.opcao == "RCER") and (~anarede.pwfblock["DCER"]):
                continue
            if (value.opcao == "FREQ") and (value.padrao == "L"):
                anarede.freqjcount = 0
            if (value.padrao == "L") and (value.opcao in anarede.excc):
                anarede.excc[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(anarede.excc):
            print("\033[96mNenhuma opcao de execucao foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de controle foi escolhida.\033[0m")

    anarede.monitor = dict(
        {
            "MFCT": False,
            "MOCF": False,
            "MOSF": False,
            "MOCG": False,
            "MOSG": False,
            "MOCT": False,
            "MOST": False,
            "MOCV": False,
        }
    )
    print("\033[96mOpcoes de monitoramento escolhidas: ", end="")
    try:
        for idx, value in anarede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in anarede.monitor):
                anarede.monitor[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(anarede.monitor):
            print("\033[96mNenhuma opcao de monitoramento foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de monitoramento foi escolhida.\033[0m")

    anarede.report = dict(
        {
            "DADB": False,
            "DADC": False,
            "DADL": False,
            "RAGR": False,
            "RARE": False,
            "RARI": False,
            "RBAR": False,
            "RBEL": False,
            "RBEQ": False,
            "RBRC": False,
            "RBRS": False,
            "RBSH": False,
            "RBSI": False,
            "RBSL": False,
            "RCAI": False,
            "RCAR": False,
            "RCER": False,
            "RCMT": False,
            "RCON": False,
            "RCSC": False,
            "RCTE": False,
            "RCTG": False,
            "RCTR": False,
            "RCUR": False,
            "RCUS": False,
            "RCVC": False,
            "RCVG": False,
            "RDMS": False,
            "RDMT": False,
            "REMT": False,
            "REQV": False,
            "REST": False,
            "RETC": False,
            "RFCR": False,
            "RFQL": False,
            "RFRP": False,
            "RFXC": False,
            "RFXS": False,
            "RGBT": False,
            "RGER": False,
            "RGLT": False,
            "RILH": False,
            "RINT": False,
            "RLDC": False,
            "RLTP": False,
            "RLEQ": False,
            "RLIL": False,
            "RLIN": False,
            "RLTC": False,
            "RMAC": False,
            "RMIS": False,
            "RMON": False,
            "RMOT": False,
            "ROUT": False,
            "ROPC": False,
            "RPRL": False,
            "RREF": False,
            "RREM": False,
            "RRES": False,
            "RROP": False,
            "RRSI": False,
            "RRSU": False,
            "RSEL": False,
            "RSHB": False,
            "RSHL": False,
            "RSIS": False,
            "RSLP": False,
            "RTAB": False,
            "RTGR": False,
            "RTIE": False,
            "RTOT": False,
            "RTPF": False,
            "RTPL": False,
            "RTR3": False,
            "RTRA": False,
            "RTRP": False,
            "RTRU": False,
            "RVCO": False,
            "RVIO": False,
            "RVSA": False,
        }
    )
    print("\033[96mOpcoes de relatorio escolhidas: ", end="")
    try:
        for idx, value in anarede.dopcDF.iterrows():
            if (value.padrao == "L") and (value.opcao in anarede.report):
                anarede.report[value.opcao] = True
                print(f"{value.opcao}", end=" ")
        print("\033[0m")
        if not any(anarede.report):
            print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")
    except:
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")


def optionsstb(
    anatem,
):
    """configuracao de variaveis para processos de convergencia em analise dinâmica do sistema eletrico de potencia
    determinacao dos valores padrao das constantes, variaveis de controle, variaveis de execucao, variaveis de monitoramento e variaveis de relatorios

    Args
        anatem:
    """
    anatem.cte = dict(
        {
            "TETE": 1e-6,
            "TEMD": 1e-6,
            "TABS": 1e-7,
            "TEPQ": 1e-2,
            "LCRT": 30,
            "LPRT": 60,
            "IMDS": 10,
            "IACS": 10,
            "IACE": 300,
            "ITMI": 100,
            "MRAC": 30,
            "MRDC": 100,
            "ITMR": 20,
            "PFFB": 2e-2,
            "PRDA": 10,
            "AMX1": 360,
            "AMX2": 1000,
            "TBID": 1e-9,
            "TSAD": 1e-2,
        }
    )
    for idx, value in anatem.dcteDF.iterrows():
        anatem.cte[value.constante] = value.valor_constante

    anatem.excc = dict(
        {
            "80CO": False,
            "ASYN": False,
            "BMVA": False,
            "CCCO": False,
            "CILH": False,
            "CONV": False,
            "CONT": False,
            "DCNI": False,
            "DESV": False,
            "DLCC": False,
            "DLCA": False,
            "DNWT": False,
            "ECHO": False,
            "IEPS": False,
            "IERR": False,
            "ILHA": False,
            "FILE": False,
            "FLXT": False,
            "FLX2": False,
            "FREQ": False,
            "FULL": False,
            "GRAV": False,
            "IMPR": False,
            "INIC": False,
            "IRMX": False,
            "LGCY": False,
            "LIBS": False,
            "LIST": False,
            "MCDU": False,
            "MD01": False,
            "MD02": False,
            "MD03": False,
            "MD04": False,
            "MD05": False,
            "MD06": False,
            "MD07": False,
            "MD08": False,
            "MD09": False,
            "MD10": False,
            "MD11": False,
            "MD12": False,
            "MD13": False,
            "MD14": False,
            "MD15": False,
            "MD16": False,
            "MD17": False,
            "MD18": False,
            "MD19": False,
            "MD20": False,
            "MO21": False,
            "MO22": False,
            "MO23": False,
            "MO24": False,
            "NEWT": False,
            "NULL": False,
            "OTM1": False,
            "OTM2": False,
            "OTM3": False,
            "OTM4": False,
            "OTM5": False,
            "OTMX": False,
            "P2D2": False,
            "RE2S": False,
            "REST": False,
            "SADD": False,
            "SAD2": False,
            "SAD3": False,
            "TELE": False,
            "TMEC": False,
            "WARN": False,
        }
    )
    print("\033[96mOpcoes de execucao escolhidas: ", end="")
    for idx, value in anatem.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anatem.excc):
            anatem.excc[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anatem.excc):
        print("\033[96mNenhuma opcao de execucao foi escolhida.\033[0m")

    anatem.report = dict(
        {
            "RBAR": False,
            "RBCN": False,
            "RBLI": False,
            "RCAR": False,
            "RCDU": False,
            "RCEN": False,
            "RCMT": False,
            "RCSC": False,
            "RCTE": False,
            "RCVP": False,
            "RCVT": False,
            "RDIM": False,
            "RERA": False,
            "RGER": False,
            "RILH": False,
            "RLDC": False,
            "RLIN": False,
            "RLOG": False,
            "RMOT": False,
            "RMXG": False,
            "RMXU": False,
            "ROPC": False,
            "ROPG": False,
            "RSEG": False,
        }
    )
    print("\033[96mOpcoes de relatorio escolhidas: ", end="")
    for idx, value in anatem.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anatem.report):
            anatem.report[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anatem.report):
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")
