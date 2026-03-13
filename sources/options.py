# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros
from copy import deepcopy


def optionspwf(
    anarede,
):
    """configuração de variáveis para processos de convergência em análise estática de fluxos de potência
    determinação dos valores padrão das constantes, variáveis de controle, variáveis de execução, variáveis de monitoramento e variáveis de relatórios

    Args
        anarede:
    """
    ## Inicialização
    anarede.cte = dict(
        {
            "BASE": 100.0,  # base de potência para o sistema CA
            "DASE": 100.0,  # base de potência default para o sistema CC
            "TEPA": 1e-3,  # tolerancia de convergencia de potencia ativa
            "TEPR": 1e-3,  # tolerancia de convergencia de potencia reativa
            "TLPR": 1e-3,  # tolerância para limite de geração de potência reativa
            "TLVC": 5e-3,  # tolerância para tensões controladas
            "TLTC": 1e-4,  # tolerância para limite de tap de transformador
            "TETP": 5e-2,  # tolerância para erro de intercâmbio de potência ativa entre áreas
            "TBPA": 5e-2,  # tolerância para erro de redistribuição de potência ativa em contingências de geração/carga
            "TSFR": 1e-4,  # tolerância para detecção de separação física da rede elétrica
            "TUDC": 1e-5,  # tolerância de convergência do erro de tensão em barra CC
            "TADC": 1e-4,  # tolerância para limite de ângulo de disparo/extinção de conversor
            "TPST": 2e-3,  # tolerância de erro de potência reativa para aplicação de variação automática de tap de transformador
            "QLST": 4e-3,  # tolerância de erro de potência reativa para aplicação de controle de limite de geração de potência reativa
            "EXST": 4e-3,  # tolerância de erro de potência ativa para aplicação de controle de intercâmbio de potência ativa entre áreas
            "TLPP": 1e-2,  # tolerância para a capacidade de carregamento de circuitos
            "TSBZ": 1e-4,  # tolerância para detecção de variação nula de fluxo de potência ativa nos circuitos do sistema externo
            "TSBA": 5e-2,  # tolerância para detecção de pequenas variações de fluxo de potência ativa nos circuitos do sistema externo
            "PGER": 0.3,  # percentagem de geração de potência ativa a ser removida dos geradores do sistema interno para o cálculo das variações de fluxo de potência ativa nos circuitos do sistema externo
            "VFLD": 0.7,  # valor de tensão abaixo do qual a parcela de potência constante das cargas funcionais passa a ser modelada como uma impedância constante
            "VART": 5e-2,  # variação da tensão (em relação ao caso base) a partir da qual uma barra passa a ser automaticamente monitorada no problema de fluxo de potência continuado
            "TSTP": 33,  # número de steps do transformador com tap discreto
            "NDIR": 20,  # número de direções utilizado no processo de construção da região de segurança
            "STIR": 1,  # fator de divisão do passo atual de transferência de geração de potência ativa quando ocorre alguma violação no processo de construção da região de segurança
            "STTR": 5e-2,  # passo de transferência de geração de potência ativa utilizado no processo de construção da região de segurança
            "TRPT": 1,  #  percentagem de geração de potência ativa utilizado no processo de construção da região de segurança
            "ZMIN": 1e-5,  # valor mínimo do módulo de impedância dos circuitos CA
            "VDVN": 0.4,  # tensão mínima para teste de divergência automática do caso
            "ICMN": 5e-4,  # valor mínimo do incremento automático de carga (utilizado como critério de parada do método de fluxo de potência continuado)
            "BFPO": 1e-2,  # valor mínimo de injeção de potência reativa de um banco shunt alocado pelo programa flupot
            "ZMAX": 5e2,  # tensão mínima para teste de divergência do caso
            "VDVM": 2.0,  # tensão máxima para teste de divergência do caso
            "ASTP": 0.05,  # valor máximo de correção de ângulo de fase da tensão durante o processo de solução
            "VSTP": 5e-2,  # valor máximo de correção de magnitude da tensão durante o processo de solução
            "CSTP": 5e-2,  # valor máximo de correção de susceptância do CSC durante o processo de solução
            "DMAX": 5,  # número máximo de vezes consecutivas que o fator de divisão FDIV pode ser aplicado (utilizado como critério de parada do método de fluxo de potência continuado)
            "TSDC": 0.02,  # valor máximo de correção do tap do conversor do elo CC durante o processo de solução
            "ASDC": 1,  # valor máximo de correção do ângulo de disparo do conversor do elo CC durante o processo de solução
            "ACIT": 30,  # número máximo de iterações na solução do fluxo de potência CA
            "ICIT": 30,  # número máximo de soluções do fluxo de potência a serem calculadas durante a execução do problema de fluxo de potência continuado
            "LPIT": 50,  # número máximo de iterações do problema de programação linear
            "LFLP": 10,  # número máximo de iterações do problema de redespacho de potência ativa
            "LFIT": 10,  # número máximo de iterações na solução da interface CA-CC
            "DCIT": 10,  # número máximo de iterações na solução do fluxo de potência CC
            "VSIT": 10,  # número máximo de iterações no ajuste da tensão em barra CC
            "LFCV": 1,  # número de iterações do método desacoplado rápido antes do início do processo de solução pelo método de newton raphson
            "PDIT": 10,  # número de iterações na estimação das perdas no modelo de fluxo de potência linearizado
            "FDIV": 2,  # fator de redução do incremento automático de carga quando o problema de fluxo de potência não apresenta solução durante a execução do programa de fluxo de potência continuado
            "ICMV": 5e-3,  # tamanho do passo inicial quando o parâmetro de continuação muda de carregamento para o módulo de tensão
            "APAS": 0.9,  # determina o ponto a partir do qual o tamanho do passo do fluxo de potência continuado parametrizado será acelerado (% do carregamento máximo)
            "CPAR": 0.7,  # especifica o ponto de para do fluxo de potência continuado parametrizado (% do carregamento máximo)
            "VAVT": 2e-2,  # critério de variação de tensão para a determinação da rede complementar
            "VAVF": 5e-2,  # critério de variação de fluxo em função do carregamento nominal para a determinação da rede complementar
            "VMVF": 15e-2,  # critério de variação de fluxo para a determinação da rede complementar
            "VPVT": 2e-2,  # critério de variação de tensão para a terminação da rede de simulação - primeiro critério
            "VPVF": 5e-2,  # critério de variação de fluxo em função do carregamento nominal para a determinação da rede de simulação - primeiro critério
            "VPMF": 10e-2,  # critério de variação de fluxo para a determinação da rede de simulação - primeiro critério
            # novas constantes adicionadas por JP
            "FBSE": 60.0,  # frequencia base do sep (criado por JP)
            "SIGA": 1e-6,  # tolerância da chave sigmóide SVC-A (criado por JP)
            "SIGQ": 1e-6,  # tolerância da chave sigmóide SVC-Q e QLIM (criado por JP)
            "SIGI": 1e-6,  # tolerância da chave sigmóide SVC-I (criado por JP)
            "SIGV": 1e-6,  # tolerância da chave sigmóide referente à variável de tensão (criado por JP)
            "SIGK": 1e8,  # variável de inclinação da chave sigmóide (criado por JP)
            "FULL": 0,  # Curva completa do fluxo de potência continuado (criado por JP)
            "VVAR": 1e-6,  # (criado por JP)
            "CTOL": 1e-7,  # tolerância para as variáveis de estado do método direto (canizares) (criado por JP)
        }
    )

    for idx, value in anarede.dcteDF.iterrows():
        anarede.cte[value.constante] = value.valor_constante

    if anarede.pwfblock["DINC"]:
        anarede.cte["LMBD"] = anarede.dincDF.loc[0, "passo_incremento_potencia_ativa"]
        anarede.cte["cpfBeta"] = zeros(anarede.nbus)
        if anarede.pwfblock["DGER"]:
            for idx, value in anarede.dgerDF.iterrows():
                # idx = value["numero"] - 1
                anarede.cte["cpfBeta"][idx] = value.fator_participacao

    anarede.control = dict(
        {
            "CPHS": False,
            "CREM": False,
            "CSCA": False,
            "CTAP": False,
            "CTAF": False,
            "FREQ": False,
            "QLIM": False,
            "VLIM": False,
        }
    )
    anarede.maskctrlcount = 0
    print("\033[96mOpções de controle escolhidas: ", end="")
    for idx, value in anarede.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anarede.control):
            anarede.control[value.opcao] = True
            anarede.maskctrlcount += 1
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anarede.control):
        print("\033[96mNenhuma opção de controle foi escolhida.\033[0m")

    anarede.excc = dict(
        {
            "80CO": False,  # relatórios impressos em formato de 80 colunas
            "A0GI": False,  # gravação automática do arquivo de saída DGEI.dat durante etapa 1 de utilização do software ANAT0
            "ACCC": False,  # força a reinicialização do controle de tensão de dois ou mais elos de corrente contínua do tipo ccc qie controlam a tensão da mesma barra CA pelo modo de tensão definido no código de execução DCCV
            "ACFP": False,  # executa a análise de casos de fluxo de potência através da impressão de relatórios que contêm dados de transformadores que podem causar problemas à convergência dos casos
            "ACLS": False,  # utilizada em conjunto com o código de execução DANC, permite a especificação da alteração do carregamento através da linguagem de seleção
            "ADRE": False,  # indica que as restrições lineares adicionais definidas no código de execução DRES serão consideradas durante a solução do problema de redespacho de potência ativa
            "AGRE": False,  # utilizada com o código de execução RELA, em conjunto com as opções para relatórios de equipamentos (RBAR, DADB, RLIN, DADL, RGER, RTRA, RLTC, RCSC, DADC, RSHB, RSHL, RBSH, RBSL, RFCR, RFQL), imprime o relatório apenas dos agregadores e grupos selecionados de acordo com os campo de número de agregador e número de grupo do código de execução DAGR
            "AGRF": False,  # utilizada com o código de execução EXMT e com a opção de execução IDSA, atua nas etapas de agrupamento e incremento de geração da ferramenta de identificação de subáreas e áreas de modo a garantir que os elementos selecionados reduzam a folga do circuito de maior fator
            "ALPR": False,  # permite a alteração da prioridade máxima de ativação das variáveis de controle
            "AMOT": False,  # após a execução do processo de otimização pelo código de execução EXOT, adiciona as modificações sugeridas pelo processo de otimização (FPO) ao caso em memória
            "AREA": False,  # utilizada com o código de execução RELA, permite selecionar a área ou as áreas que serão impressas, de acordo com o campo número do código de execução DARE
            "AREG": False,  # utilizada com o código de execução ARQV, habilita o acréscimo automático de registros ao arquivo histórico
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
    print("\033[96mOpções de execução escolhidas: ", end="")
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
        print("\033[96mNenhuma opção de execução foi escolhida.\033[0m")

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
    print("\033[96mOpções de monitoramento escolhidas: ", end="")
    for idx, value in anarede.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anarede.monitor):
            anarede.monitor[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anarede.monitor):
        print("\033[96mNenhuma opção de monitoramento foi escolhida.\033[0m")

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
    for idx, value in anarede.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anarede.report):
            anarede.report[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anarede.report):
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")


def optionsstb(
    anatem,
):
    """configuração de variáveis para processos de convergência em análise dinâmica do sistema elétrico de potência
    determinação dos valores padrão das constantes, variáveis de controle, variáveis de execução, variáveis de monitoramento e variáveis de relatórios

    Args
        anatem:
    """
    ## Inicialização
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
            "BASE": False,
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
    print("\033[96mOpções de execução escolhidas: ", end="")
    for idx, value in anatem.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anatem.excc):
            anatem.excc[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anatem.excc):
        print("\033[96mNenhuma opção de execução foi escolhida.\033[0m")

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
    print("\033[96mOpções de relatorio escolhidas: ", end="")
    for idx, value in anatem.dopcDF.iterrows():
        if (value.padrao == "L") and (value.opcao in anatem.report):
            anatem.report[value.opcao] = True
            print(f"{value.opcao}", end=" ")
    print("\033[0m")
    if not any(anatem.report):
        print("\033[96mNenhuma opcao de relatorio foi escolhida.\033[0m")
