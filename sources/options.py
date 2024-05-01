# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import zeros
from copy import deepcopy


def options(
    powerflow,
):
    """inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Configuração de variáveis para processos de convergência de fluxos de potência tradicionais
    powerflow.stdcte = {
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
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        "FBASE": 60.0,  # frequencia base do sep (criado por JP)
        "SIGA": 1e-6,  # tolerância da chave sigmóide SVC-A (criado por JP)
        "SIGQ": 1e-6,  # tolerância da chave sigmóide SVC-Q e SVC-I, QLIM (criado por JP)
        "SIGV": 1e-6,  # tolerância da chave sigmóide referente à variável de tensão (criado por JP)
        "SIGK": 1e8,  # variável de inclinação da chave sigmóide (criado por JP)
        "FULL": 0,  # Curva completa do fluxo de potência continuado (criado por JP)
        "VVAR": 1e-6,  # (criado por JP)
        "CTOL": 1e-7,  # tolerância para as variáveis de estado do método direto (canizares) (criado por JP)
    }

    powerflow.options = dict()

    for k, v in powerflow.stdcte.items():
        if k not in powerflow.dcteDF["constante"].unique():
            powerflow.options[k] = v
        else:
            powerflow.options[k] = deepcopy(
                powerflow.dcteDF.loc[powerflow.dcteDF["constante"] == k][
                    "valor_constante"
                ].values[0]
            )

    if powerflow.codes["DINC"]:
        powerflow.options["LMBD"] = powerflow.dincDF.loc[
            0, "passo_incremento_potencia_ativa"
        ]
        powerflow.options["cpfBeta"] = zeros(powerflow.nbus)
        if powerflow.codes["DGER"]:
            for idx, value in powerflow.dgerDF.iterrows():
                # idx = value["numero"] - 1
                powerflow.options["cpfBeta"][idx] = value["fator_participacao"]
