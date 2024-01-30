# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import concatenate, count_nonzero, nan, nonzero, ones
from pandas import DataFrame as DF

def pwf(
    powerflow,
):
    '''inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variáveis
    powerflow.linecount = 0

    # Funções
    keywords(
        powerflow,
    )

    # Códigos
    codes(
        powerflow,
    )

    # Leitura
    readfile(
        powerflow,
    )

def keywords(
    powerflow,
):
    '''palavras-chave de arquivo .pwf
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.end_archive = 'FIM'
    powerflow.end_block = ('9999', '99999')
    powerflow.comment = '('

def codes(
    powerflow,
):
    '''códigos de dados de execução implementados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variável
    powerflow.codes = {
        'DANC': False,
        'DBAR': False,
        'DCER': False,
        'DCTE': False,
        'DGER': False,
        'DINC': False,
        'DLIN': False,
    }

def danc(
    powerflow,
):
    '''inicialização para leitura de dados de alteração do nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.danc = dict()
    powerflow.danc['area'] = list()
    powerflow.danc['fator_carga_ativa'] = list()
    powerflow.danc['fator_carga_reativa'] = list()
    powerflow.danc['fator_shunt_barra'] = list()

def dbar(
    powerflow,
):
    '''inicialização para leitura de dados de barra

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dbar = dict()
    powerflow.dbar['numero'] = list()
    powerflow.dbar['operacao'] = list()
    powerflow.dbar['estado'] = list()
    powerflow.dbar['tipo'] = list()
    powerflow.dbar['grupo_base_tensao'] = list()
    powerflow.dbar['nome'] = list()
    powerflow.dbar['grupo_limite_tensao'] = list()
    powerflow.dbar['tensao'] = list()
    powerflow.dbar['angulo'] = list()
    powerflow.dbar['potencia_ativa'] = list()
    powerflow.dbar['potencia_reativa'] = list()
    powerflow.dbar['potencia_reativa_minima'] = list()
    powerflow.dbar['potencia_reativa_maxima'] = list()
    powerflow.dbar['barra_controlada'] = list()
    powerflow.dbar['demanda_ativa'] = list()
    powerflow.dbar['demanda_reativa'] = list()
    powerflow.dbar['shunt_barra'] = list()
    powerflow.dbar['area'] = list()
    powerflow.dbar['tensao_base'] = list()
    powerflow.dbar['modo'] = list()
    powerflow.dbar['agreg1'] = list()
    powerflow.dbar['agreg2'] = list()
    powerflow.dbar['agreg3'] = list()
    powerflow.dbar['agreg4'] = list()
    powerflow.dbar['agreg5'] = list()
    powerflow.dbar['agreg6'] = list()
    powerflow.dbar['agreg7'] = list()
    powerflow.dbar['agreg8'] = list()
    powerflow.dbar['agreg9'] = list()
    powerflow.dbar['agreg10'] = list()

def dcer(
    powerflow,
):
    '''inicialização para leitura de dados de compensadores estáticos de potência reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dcer = dict()
    powerflow.dcer['barra'] = list()
    powerflow.dcer['operacao'] = list()
    powerflow.dcer['grupo_base'] = list()
    powerflow.dcer['unidades'] = list()
    powerflow.dcer['barra_controlada'] = list()
    powerflow.dcer['droop'] = list()
    powerflow.dcer['potencia_reativa'] = list()
    powerflow.dcer['potencia_reativa_minima'] = list()
    powerflow.dcer['potencia_reativa_maxima'] = list()
    powerflow.dcer['controle'] = list()
    powerflow.dcer['estado'] = list()

def dcte(
    powerflow,
):
    '''inicialização para leitura de dados de constantes

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dcte = dict()
    powerflow.dcte['constante'] = list()
    powerflow.dcte['valor_constante'] = list()

def dger(
    powerflow,
):
    '''inicialização para leitura de dados de geradores

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dger = dict()
    powerflow.dger['numero'] = list()
    powerflow.dger['operacao'] = list()
    powerflow.dger['potencia_ativa_minima'] = list()
    powerflow.dger['potencia_ativa_maxima'] = list()
    powerflow.dger['fator_participacao'] = list()
    powerflow.dger['fator_participacao_controle_remoto'] = list()
    powerflow.dger['fator_potencia_nominal'] = list()
    powerflow.dger['fator_servico_armadura'] = list()
    powerflow.dger['fator_servico_rotor'] = list()
    powerflow.dger['angulo_maximo_carga'] = list()
    powerflow.dger['reatancia_maquina'] = list()
    powerflow.dger['potencia_aparente_nominal'] = list()
    powerflow.dger['estatismo'] = list()

def dinc(
    powerflow,
):
    '''inicialização para leitura de dados de incremento do nível de carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dinc = dict()
    powerflow.dinc['tipo_incremento_1'] = list()
    powerflow.dinc['identificacao_incremento_1'] = list()
    powerflow.dinc['condicao_incremento_1'] = list()
    powerflow.dinc['tipo_incremento_2'] = list()
    powerflow.dinc['identificacao_incremento_2'] = list()
    powerflow.dinc['condicao_incremento_2'] = list()
    powerflow.dinc['tipo_incremento_3'] = list()
    powerflow.dinc['identificacao_incremento_3'] = list()
    powerflow.dinc['condicao_incremento_3'] = list()
    powerflow.dinc['tipo_incremento_4'] = list()
    powerflow.dinc['identificacao_incremento_4'] = list()
    powerflow.dinc['condicao_incremento_4'] = list()
    powerflow.dinc['passo_incremento_potencia_ativa'] = list()
    powerflow.dinc['passo_incremento_potencia_reativa'] = list()
    powerflow.dinc['maximo_incremento_potencia_ativa'] = list()
    powerflow.dinc['maximo_incremento_potencia_reativa'] = list()
    powerflow.dinc['tratamento_incremento_potencia_ativa'] = list()
    powerflow.dinc['tratamento_incremento_potencia_reativa'] = list()

def dlin(
    powerflow,
):
    '''inicialização para leitura de dados de linha

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    powerflow.dlin = dict()
    powerflow.dlin['de'] = list()
    powerflow.dlin['abertura_de'] = list()
    powerflow.dlin['operacao'] = list()
    powerflow.dlin['abertura_para'] = list()
    powerflow.dlin['para'] = list()
    powerflow.dlin['circuito'] = list()
    powerflow.dlin['estado'] = list()
    powerflow.dlin['proprietario'] = list()
    powerflow.dlin['resistencia'] = list()
    powerflow.dlin['reatancia'] = list()
    powerflow.dlin['susceptancia'] = list()
    powerflow.dlin['tap'] = list()
    powerflow.dlin['tap_minimo'] = list()
    powerflow.dlin['tap_maximo'] = list()
    powerflow.dlin['tap_defasagem'] = list()
    powerflow.dlin['barra_controlada'] = list()
    powerflow.dlin['capacidade_normal'] = list()
    powerflow.dlin['capacidade_emergencial'] = list()
    powerflow.dlin['numero_taps'] = list()
    powerflow.dlin['capacidade_equipamento'] = list()
    powerflow.dlin['agreg1'] = list()
    powerflow.dlin['agreg2'] = list()
    powerflow.dlin['agreg3'] = list()
    powerflow.dlin['agreg4'] = list()
    powerflow.dlin['agreg5'] = list()
    powerflow.dlin['agreg6'] = list()
    powerflow.dlin['agreg7'] = list()
    powerflow.dlin['agreg8'] = list()
    powerflow.dlin['agreg9'] = list()
    powerflow.dlin['agreg10'] = list()

def readfile(
    powerflow,
):
    '''leitura do arquivo .pwf

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    f = open(f'{powerflow.dirSEP}', 'r', encoding='latin-1')
    powerflow.lines = f.readlines()
    f.close()
    powerflow.pwf2py = {}

    # Loop de leitura de linhas do `.pwf`
    while powerflow.lines[powerflow.linecount].strip() != powerflow.end_archive:
        # Dados de Alteração do Nível de Carregamento
        if powerflow.lines[powerflow.linecount].strip() == 'DANC':
            danc(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.danc['area'].append(powerflow.lines[powerflow.linecount][:5])
                    powerflow.danc['fator_carga_ativa'].append(
                        powerflow.lines[powerflow.linecount][5:12]
                    )
                    powerflow.danc['fator_carga_reativa'].append(
                        powerflow.lines[powerflow.linecount][12:19]
                    )
                    powerflow.danc['fator_shunt_barra'].append(
                        powerflow.lines[powerflow.linecount][19:24]
                    )
                powerflow.linecount += 1

            # DataFrame dos Dados de Alteração do Nível de Carregamento
            powerflow.dancDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.danc),
                data='DANC',
            )
            if powerflow.dancDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m'
                )
            else:
                powerflow.codes['DANC'] = True

        # Dados de Barra
        elif powerflow.lines[powerflow.linecount].strip() == 'DBAR':
            dbar(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dbar['numero'].append(powerflow.lines[powerflow.linecount][:5])
                    powerflow.dbar['operacao'].append(powerflow.lines[powerflow.linecount][5])
                    powerflow.dbar['estado'].append(powerflow.lines[powerflow.linecount][6])
                    powerflow.dbar['tipo'].append(powerflow.lines[powerflow.linecount][7])
                    powerflow.dbar['grupo_base_tensao'].append(
                        powerflow.lines[powerflow.linecount][8:10]
                    )
                    powerflow.dbar['nome'].append(
                        powerflow.lines[powerflow.linecount][10:22].split(' ')[0]
                    )
                    powerflow.dbar['grupo_limite_tensao'].append(
                        powerflow.lines[powerflow.linecount][22:24]
                    )
                    powerflow.dbar['tensao'].append(powerflow.lines[powerflow.linecount][24:28])
                    powerflow.dbar['angulo'].append(powerflow.lines[powerflow.linecount][28:32])
                    powerflow.dbar['potencia_ativa'].append(
                        powerflow.lines[powerflow.linecount][32:37]
                    )
                    powerflow.dbar['potencia_reativa'].append(
                        powerflow.lines[powerflow.linecount][37:42]
                    )
                    powerflow.dbar['potencia_reativa_minima'].append(
                        powerflow.lines[powerflow.linecount][42:47]
                    )
                    powerflow.dbar['potencia_reativa_maxima'].append(
                        powerflow.lines[powerflow.linecount][47:52]
                    )
                    powerflow.dbar['barra_controlada'].append(
                        powerflow.lines[powerflow.linecount][52:58]
                    )
                    powerflow.dbar['demanda_ativa'].append(
                        powerflow.lines[powerflow.linecount][58:63]
                    )
                    powerflow.dbar['demanda_reativa'].append(
                        powerflow.lines[powerflow.linecount][63:68]
                    )
                    powerflow.dbar['shunt_barra'].append(
                        powerflow.lines[powerflow.linecount][68:73]
                    )
                    powerflow.dbar['area'].append(powerflow.lines[powerflow.linecount][73:76])
                    powerflow.dbar['tensao_base'].append(
                        powerflow.lines[powerflow.linecount][76:80]
                    )
                    powerflow.dbar['modo'].append(powerflow.lines[powerflow.linecount][80])
                    powerflow.dbar['agreg1'].append(powerflow.lines[powerflow.linecount][81:84])
                    powerflow.dbar['agreg2'].append(powerflow.lines[powerflow.linecount][84:87])
                    powerflow.dbar['agreg3'].append(powerflow.lines[powerflow.linecount][87:90])
                    powerflow.dbar['agreg4'].append(powerflow.lines[powerflow.linecount][90:93])
                    powerflow.dbar['agreg5'].append(powerflow.lines[powerflow.linecount][93:96])
                    powerflow.dbar['agreg6'].append(powerflow.lines[powerflow.linecount][96:99])
                    powerflow.dbar['agreg7'].append(powerflow.lines[powerflow.linecount][99:102])
                    powerflow.dbar['agreg8'].append(powerflow.lines[powerflow.linecount][102:105])
                    powerflow.dbar['agreg9'].append(powerflow.lines[powerflow.linecount][105:108])
                    powerflow.dbar['agreg10'].append(powerflow.lines[powerflow.linecount][108:111])
                powerflow.linecount += 1

            # DataFrame dos Dados de Barra
            powerflow.dbarraDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dbar),
                data='DBAR',
            )
            if powerflow.dbarraDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DBAR`!\033[0m'
                )
            else:
                powerflow.codes['DBAR'] = True

        # Dados de Compensadores Estáticos de Potência Reativa
        elif powerflow.lines[powerflow.linecount].strip() == 'DCER':
            dcer(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dcer['barra'].append(powerflow.lines[powerflow.linecount][:5])
                    powerflow.dcer['operacao'].append(powerflow.lines[powerflow.linecount][6])
                    powerflow.dcer['grupo_base'].append(powerflow.lines[powerflow.linecount][8:10])
                    powerflow.dcer['unidades'].append(powerflow.lines[powerflow.linecount][11:13])
                    powerflow.dcer['barra_controlada'].append(
                        powerflow.lines[powerflow.linecount][14:19]
                    )
                    powerflow.dcer['droop'].append(powerflow.lines[powerflow.linecount][20:26])
                    powerflow.dcer['potencia_reativa'].append(
                        powerflow.lines[powerflow.linecount][27:32]
                    )
                    powerflow.dcer['potencia_reativa_minima'].append(
                        powerflow.lines[powerflow.linecount][32:37]
                    )
                    powerflow.dcer['potencia_reativa_maxima'].append(
                        powerflow.lines[powerflow.linecount][37:42]
                    )
                    powerflow.dcer['controle'].append(powerflow.lines[powerflow.linecount][43])
                    powerflow.dcer['estado'].append(powerflow.lines[powerflow.linecount][45])
                powerflow.linecount += 1

            # DataFrame dos Dados dos Compensadores Estáticos de Potência Reativa
            powerflow.dcerDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dcer),
                data='DCER',
            )
            if powerflow.dcerDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código e execução `DCER`!\033[0m'
                )
            else:
                powerflow.codes['DCER'] = True

        # Dados de Constantes
        elif powerflow.lines[powerflow.linecount].strip() == 'DCTE':
            dcte(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][:4])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][5:11]
                    )
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][12:16])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][17:23]
                    )
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][24:28])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][29:35]
                    )
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][36:40])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][41:47]
                    )
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][48:52])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][53:59]
                    )
                    powerflow.dcte['constante'].append(powerflow.lines[powerflow.linecount][60:64])
                    powerflow.dcte['valor_constante'].append(
                        powerflow.lines[powerflow.linecount][65:71]
                    )
                powerflow.linecount += 1

            # DataFrame dos Dados de Constantes
            powerflow.dcteDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dcte),
                data='DCTE',
            )
            if powerflow.dcteDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DCTE`!\033[0m'
                )
            else:
                powerflow.codes['DCTE'] = True

        # Dados de Geradores
        elif powerflow.lines[powerflow.linecount].strip() == 'DGER':
            dger(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dger['numero'].append(powerflow.lines[powerflow.linecount][:5])
                    powerflow.dger['operacao'].append(powerflow.lines[powerflow.linecount][6])
                    powerflow.dger['potencia_ativa_minima'].append(
                        powerflow.lines[powerflow.linecount][8:14]
                    )
                    powerflow.dger['potencia_ativa_maxima'].append(
                        powerflow.lines[powerflow.linecount][15:21]
                    )
                    powerflow.dger['fator_participacao'].append(
                        powerflow.lines[powerflow.linecount][22:27]
                    )
                    powerflow.dger['fator_participacao_controle_remoto'].append(
                        powerflow.lines[powerflow.linecount][28:33]
                    )
                    powerflow.dger['fator_potencia_nominal'].append(
                        powerflow.lines[powerflow.linecount][34:39]
                    )
                    powerflow.dger['fator_servico_armadura'].append(
                        powerflow.lines[powerflow.linecount][40:44]
                    )
                    powerflow.dger['fator_servico_rotor'].append(
                        powerflow.lines[powerflow.linecount][45:49]
                    )
                    powerflow.dger['angulo_maximo_carga'].append(
                        powerflow.lines[powerflow.linecount][50:54]
                    )
                    powerflow.dger['reatancia_maquina'].append(
                        powerflow.lines[powerflow.linecount][55:60]
                    )
                    powerflow.dger['potencia_aparente_nominal'].append(
                        powerflow.lines[powerflow.linecount][61:66]
                    )
                    powerflow.dger['estatismo'].append(powerflow.lines[powerflow.linecount][66:72])
                powerflow.linecount += 1

            # DataFrame dos Dados de Geradores
            powerflow.dgeraDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dger),
                data='DGER',
            )
            if powerflow.dgeraDF.empty:  # or (powerflow.dgeraDF.shape[0] != powerflow.nger):
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DGER`!\033[0m'
                )
            else:
                powerflow.codes['DGER'] = True

        # Dados de Incremento do Nível de Carregamento
        elif powerflow.lines[powerflow.linecount].strip() == 'DINC':
            dinc(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dinc['tipo_incremento_1'].append(
                        powerflow.lines[powerflow.linecount][:4]
                    )
                    powerflow.dinc['identificacao_incremento_1'].append(
                        powerflow.lines[powerflow.linecount][5:10]
                    )
                    powerflow.dinc['condicao_incremento_1'].append(
                        powerflow.lines[powerflow.linecount][11]
                    )
                    powerflow.dinc['tipo_incremento_2'].append(
                        powerflow.lines[powerflow.linecount][13:17]
                    )
                    powerflow.dinc['identificacao_incremento_2'].append(
                        powerflow.lines[powerflow.linecount][18:23]
                    )
                    powerflow.dinc['condicao_incremento_2'].append(
                        powerflow.lines[powerflow.linecount][24]
                    )
                    powerflow.dinc['tipo_incremento_3'].append(
                        powerflow.lines[powerflow.linecount][26:30]
                    )
                    powerflow.dinc['identificacao_incremento_3'].append(
                        powerflow.lines[powerflow.linecount][31:36]
                    )
                    powerflow.dinc['condicao_incremento_3'].append(
                        powerflow.lines[powerflow.linecount][37]
                    )
                    powerflow.dinc['tipo_incremento_4'].append(
                        powerflow.lines[powerflow.linecount][39:43]
                    )
                    powerflow.dinc['identificacao_incremento_4'].append(
                        powerflow.lines[powerflow.linecount][44:49]
                    )
                    powerflow.dinc['condicao_incremento_4'].append(
                        powerflow.lines[powerflow.linecount][50]
                    )
                    powerflow.dinc['passo_incremento_potencia_ativa'].append(
                        powerflow.lines[powerflow.linecount][52:57]
                    )
                    powerflow.dinc['passo_incremento_potencia_reativa'].append(
                        powerflow.lines[powerflow.linecount][58:63]
                    )
                    powerflow.dinc['maximo_incremento_potencia_ativa'].append(
                        powerflow.lines[powerflow.linecount][64:69]
                    )
                    powerflow.dinc['maximo_incremento_potencia_reativa'].append(
                        powerflow.lines[powerflow.linecount][70:75]
                    )
                    powerflow.dinc['tratamento_incremento_potencia_ativa'].append(
                        False if powerflow.lines[powerflow.linecount][64:69] != '' else True
                    )
                    powerflow.dinc['tratamento_incremento_potencia_reativa'].append(
                        False if powerflow.lines[powerflow.linecount][70:75] != '' else True
                    )
                powerflow.linecount += 1

            # DataFrame dos dados de Incremento do Nível de Carregamento
            powerflow.dincDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dinc),
                data='DINC',
            )
            if powerflow.dincDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DINC`!\033[0m'
                )
            else:
                powerflow.codes['DINC'] = True

        # Dados de Linha
        elif powerflow.lines[powerflow.linecount].strip() == 'DLIN':
            dlin(powerflow,)
            powerflow.linecount += 1
            while powerflow.lines[powerflow.linecount].strip() not in powerflow.end_block:
                if powerflow.lines[powerflow.linecount][0] == powerflow.comment:
                    pass
                else:
                    powerflow.dlin['de'].append(powerflow.lines[powerflow.linecount][:5])
                    powerflow.dlin['abertura_de'].append(powerflow.lines[powerflow.linecount][5])
                    powerflow.dlin['operacao'].append(powerflow.lines[powerflow.linecount][7])
                    powerflow.dlin['abertura_para'].append(powerflow.lines[powerflow.linecount][9])
                    powerflow.dlin['para'].append(powerflow.lines[powerflow.linecount][10:15])
                    powerflow.dlin['circuito'].append(powerflow.lines[powerflow.linecount][15:17])
                    powerflow.dlin['estado'].append(powerflow.lines[powerflow.linecount][17])
                    powerflow.dlin['proprietario'].append(powerflow.lines[powerflow.linecount][18])
                    powerflow.dlin['resistencia'].append(
                        powerflow.lines[powerflow.linecount][20:26]
                    )
                    powerflow.dlin['reatancia'].append(powerflow.lines[powerflow.linecount][26:32])
                    powerflow.dlin['susceptancia'].append(
                        powerflow.lines[powerflow.linecount][32:38]
                    )
                    powerflow.dlin['tap'].append(powerflow.lines[powerflow.linecount][38:43])
                    powerflow.dlin['tap_minimo'].append(
                        powerflow.lines[powerflow.linecount][43:48]
                    )
                    powerflow.dlin['tap_maximo'].append(
                        powerflow.lines[powerflow.linecount][48:53]
                    )
                    powerflow.dlin['tap_defasagem'].append(
                        powerflow.lines[powerflow.linecount][53:58]
                    )
                    powerflow.dlin['barra_controlada'].append(
                        powerflow.lines[powerflow.linecount][58:64]
                    )
                    powerflow.dlin['capacidade_normal'].append(
                        powerflow.lines[powerflow.linecount][64:68]
                    )
                    powerflow.dlin['capacidade_emergencial'].append(
                        powerflow.lines[powerflow.linecount][68:72]
                    )
                    powerflow.dlin['numero_taps'].append(
                        powerflow.lines[powerflow.linecount][72:74]
                    )
                    powerflow.dlin['capacidade_equipamento'].append(
                        powerflow.lines[powerflow.linecount][74:78]
                    )
                    powerflow.dlin['agreg1'].append(powerflow.lines[powerflow.linecount][78:81])
                    powerflow.dlin['agreg2'].append(powerflow.lines[powerflow.linecount][81:84])
                    powerflow.dlin['agreg3'].append(powerflow.lines[powerflow.linecount][84:87])
                    powerflow.dlin['agreg4'].append(powerflow.lines[powerflow.linecount][87:90])
                    powerflow.dlin['agreg5'].append(powerflow.lines[powerflow.linecount][90:93])
                    powerflow.dlin['agreg6'].append(powerflow.lines[powerflow.linecount][93:96])
                    powerflow.dlin['agreg7'].append(powerflow.lines[powerflow.linecount][96:99])
                    powerflow.dlin['agreg8'].append(powerflow.lines[powerflow.linecount][99:102])
                    powerflow.dlin['agreg9'].append(powerflow.lines[powerflow.linecount][102:105])
                    powerflow.dlin['agreg10'].append(powerflow.lines[powerflow.linecount][105:108])
                powerflow.linecount += 1

            # DataFrame dos Dados de Linha
            powerflow.dlinhaDF = treatment(
                powerflow,
                pandas=DF(data=powerflow.dlin),
                data='DLIN',
            )
            if powerflow.dlinhaDF.empty:
                ## ERROR - VERMELHO
                raise ValueError(
                    '\033[91mERROR: Falha na leitura de código de execução `DLIN`!\033[0m'
                )
            else:
                powerflow.codes['DLIN'] = True

        powerflow.linecount += 1

    ## SUCESSO NA LEITURA
    print(f'\033[32mSucesso na leitura de arquivo `{powerflow.system}`!\033[0m')

def treatment(
    powerflow,
    pandas: DF = DF.empty,
    data: str = '',
):
    '''tratamento dos valores padrão adotadas nas leituras de códigos de execução

    Parâmetros
        powerflow: self do arquivo powerflow.py
        pandas: DataFrame, obrigatório, valor padrão DataFrame.empty
            Arquivo que contém a leitura e armazenamento de dados de um respectivo código de execução
        data: str, obrigatório, valor padrão 'None'
            String que indica o código de execução lido para que haja o tratamento de dados das variáveis armazenadas no DataFrame

    Retorno
        pandas: DataFrame
            Arquivo com os valores tratados
    '''

    ## Inicialização
    # Tratamento inicial
    pandas = pandas.replace(r'^\s*$', '0', regex=True)

    ## Tratamentos
    # Tratamento específico 'DANC'
    if data == 'DANC':
        pandas = pandas.astype(
            {
                'area': 'int',
                'fator_carga_ativa': 'float',
                'fator_carga_reativa': 'float',
                'fator_shunt_barra': 'float',
            }
        )

    # Tratamento específico 'DBAR'
    elif data == 'DBAR':
        pandas = pandas.astype(
            {
                'numero': 'int',
                'operacao': 'object',
                'estado': 'object',
                'tipo': 'int',
                'grupo_base_tensao': 'object',
                'nome': 'str',
                'grupo_limite_tensao': 'object',
                'tensao': 'float',
                'angulo': 'float',
                'potencia_ativa': 'float',
                'potencia_reativa': 'float',
                'potencia_reativa_minima': 'float',
                'potencia_reativa_maxima': 'float',
                'barra_controlada': 'int',
                'demanda_ativa': 'float',
                'demanda_reativa': 'float',
                'shunt_barra': 'float',
                'area': 'int',
                'tensao_base': 'float',
                'modo': 'object',
                'agreg1': 'object',
                'agreg2': 'object',
                'agreg3': 'object',
                'agreg4': 'object',
                'agreg5': 'object',
                'agreg6': 'object',
                'agreg7': 'object',
                'agreg8': 'object',
                'agreg9': 'object',
                'agreg10': 'object',
            }
        )

        # Número de barras do sistema
        powerflow.nbus = len(pandas.tipo.values)

        # Barras geradoras: número & máscara
        powerflow.nger = 0
        powerflow.maskP = ones(powerflow.nbus, dtype=bool)
        powerflow.maskQ = ones(powerflow.nbus, dtype=bool)
        for idx, value in pandas.iterrows():
            if (value['tipo'] == 2) or (value['tipo'] == 1):
                powerflow.nger += 1
                powerflow.maskQ[idx] = False

                if value['tipo'] == 2:
                    powerflow.maskP[idx] = False
                    powerflow.slackidx = idx

                elif value['tipo'] == 1:
                    pandas.at[idx, 'angulo'] = 0.0

                if value['potencia_reativa'] > value['potencia_reativa_maxima']:
                    pandas.at[idx, 'potencia_reativa'] = value[
                        'potencia_reativa_maxima'
                    ]

                elif value['potencia_reativa'] < value['potencia_reativa_minima']:
                    pandas.at[idx, 'potencia_reativa'] = value[
                        'potencia_reativa_minima'
                    ]

            elif value['tipo'] == 0:
                pandas.at[idx, 'angulo'] = 0.0

        powerflow.mask = concatenate((powerflow.maskP, powerflow.maskQ), axis=0)

        # Número de barras PV
        powerflow.npv = powerflow.nger - 1

        # Número de barras PQ
        powerflow.npq = powerflow.nbus - powerflow.nger

        # Tensao Base
        pandas.loc[pandas['tensao_base'] == 0.0, 'tensao_base'] = 1000.0

        # Numero de Areas
        powerflow.narea = pandas['area'].nunique()
        powerflow.areas = sorted(pandas['area'].unique())

    # Tratamento específico 'DBTB'
    elif data == 'DBTB':
        pandas = pandas.astype(
            {
                'numero': 'int',
                'tensao_minima': 'float',
                'tensao_maxima': 'float',
            }
        )

    # Tratamento específico 'DCER'
    elif data == 'DCER':
        pandas = pandas.astype(
            {
                'barra': 'int',
                'operacao': 'object',
                'grupo_base': 'int',
                'unidades': 'int',
                'barra_controlada': 'int',
                'droop': 'float',
                'potencia_reativa': 'float',
                'potencia_reativa_minima': 'float',
                'potencia_reativa_maxima': 'float',
                'controle': 'object',
                'estado': 'object',
            }
        )

        powerflow.ncer = 0
        for idx, value in pandas.iterrows():
            if value['estado'] == 'D':
                pandas = pandas.drop(
                    labels=idx,
                    axis=0,
                )

            elif ((value['estado'] == '0') or (value['estado'] == 'L')) and (
                (value['controle'] == '0')
                or (value['controle'] == 'P')
                or (value['controle'] == 'I')
            ):
                powerflow.ncer += 1
                pandas.at[idx, 'droop'] = -value['droop'] / (
                    1e2 * value['unidades']
                )

                if value['barra_controlada'] == 0:
                    pandas.at[idx, 'barra_controlada'] = value['barra']

                if value['potencia_reativa'] > value['potencia_reativa_maxima']:
                    pandas.at[idx, 'potencia_reativa'] = value[
                        'potencia_reativa_maxima'
                    ]

                elif value['potencia_reativa'] < value['potencia_reativa_minima']:
                    pandas.at[idx, 'potencia_reativa'] = value[
                        'potencia_reativa_minima'
                    ]

                if value['controle'] == '0':
                    pandas.at[idx, 'controle'] = 'P'

            elif ((value['estado'] == '0') or (value['estado'] == 'L')) and (
                value['controle'] == 'A'
            ):
                powerflow.ncer += 1
                pandas.at[idx, 'droop'] = -value['droop'] / (
                    1e2 * value['unidades']
                )

                if value['barra_controlada'] == 0:
                    pandas.at[idx, 'barra_controlada'] = value['barra']

    # Tratamento específico 'DCTE'
    elif data == 'DCTE':
        pandas = pandas.astype(
            {
                'valor_constante': 'float',
            }
        )
        pandas['constante'] = pandas['constante'].replace('0', nan)
        pandas = pandas.dropna(axis=0, subset=['constante'])
        pandas = pandas.drop_duplicates(
            subset=['constante'], keep='last'
        ).reset_index(drop=True)

    # Tratamento específico 'DGER'
    elif data == 'DGER':
        pandas = pandas.astype(
            {
                'numero': 'int',
                'operacao': 'object',
                'potencia_ativa_minima': 'float',
                'potencia_ativa_maxima': 'float',
                'fator_participacao': 'float',
                'fator_participacao_controle_remoto': 'float',
                'fator_potencia_nominal': 'float',
                'fator_servico_armadura': 'float',
                'fator_servico_rotor': 'float',
                'angulo_maximo_carga': 'float',
                'reatancia_maquina': 'float',
                'potencia_aparente_nominal': 'float',
                'estatismo': 'float',
            }
        )

        pandas['fator_participacao'] = pandas['fator_participacao'].apply(
            lambda x: x * 1e-2
        )

    # Tratamento específico 'DGLT'
    elif data == 'DGLT':
        pandas = pandas.astype(
            {
                'grupo_limite_tensao': 'object',
                'tensao_minima': 'float',
                'tensao_maxima': 'float',
                'tensao_minima_emergencial': 'float',
                'tensao_maxima_emergencial': 'float',
            }
        )

    # Tratamento específico 'DINC'
    elif data == 'DINC':
        pandas = pandas.astype(
            {
                'tipo_incremento_1': 'object',
                'identificacao_incremento_1': 'int',
                'condicao_incremento_1': 'object',
                'tipo_incremento_2': 'object',
                'identificacao_incremento_2': 'int',
                'condicao_incremento_2': 'object',
                'tipo_incremento_3': 'object',
                'identificacao_incremento_3': 'int',
                'condicao_incremento_3': 'object',
                'tipo_incremento_4': 'object',
                'identificacao_incremento_4': 'int',
                'condicao_incremento_4': 'object',
                'passo_incremento_potencia_ativa': 'float',
                'passo_incremento_potencia_reativa': 'float',
                'maximo_incremento_potencia_ativa': 'float',
                'maximo_incremento_potencia_reativa': 'float',
            }
        )

        for idx, value in pandas.iterrows():
            pandas.at[idx, 'passo_incremento_potencia_ativa'] *= 1e-2
            if value['tratamento_incremento_potencia_ativa']:
                pandas.at[idx, 'maximo_incremento_potencia_ativa'] = 99.99
            else:
                pandas.at[idx, 'maximo_incremento_potencia_ativa'] *= 1e-2

            pandas.at[idx, 'passo_incremento_potencia_reativa'] *= 1e-2
            if value['tratamento_incremento_potencia_reativa']:
                pandas.at[idx, 'maximo_incremento_potencia_reativa'] = 99.99
            else:
                pandas.at[idx, 'maximo_incremento_potencia_reativa'] *= 1e-2

    # Tratamento específico 'DLIN'
    elif data == 'DLIN':
        pandas = pandas.astype(
            {
                'de': 'int',
                'abertura_de': 'object',
                'operacao': 'object',
                'abertura_para': 'object',
                'para': 'int',
                'circuito': 'int',
                'estado': 'object',
                'proprietario': 'object',
                'resistencia': 'float',
                'reatancia': 'float',
                'susceptancia': 'float',
                'tap': 'float',
                'tap_minimo': 'float',
                'tap_maximo': 'float',
                'tap_defasagem': 'float',
                'barra_controlada': 'int',
                'capacidade_normal': 'float',
                'capacidade_emergencial': 'float',
                'numero_taps': 'int',
                'capacidade_equipamento': 'float',
                'agreg1': 'float',
                'agreg2': 'object',
                'agreg3': 'object',
                'agreg4': 'object',
                'agreg5': 'object',
                'agreg6': 'object',
                'agreg7': 'object',
                'agreg8': 'object',
                'agreg9': 'object',
                'agreg10': 'object',
            }
        )

        pandas['resistencia'] *= 1e-2
        pandas['reatancia'] *= 1e-2
        pandas['susceptancia'] /= (
            2
            * powerflow.dcteDF.loc[powerflow.dcteDF.constante == 'BASE'].valor_constante[0]
        )

        pandas['estado'] = (pandas['estado'] == '0') | (pandas['estado'] == 'L')
        pandas['transf'] = (pandas['tap'] != 0.0) & pandas['estado']

        # Número de barras do sistema
        powerflow.nlin = len(pandas.de.values)

        # Número de plim
        powerflow.plim = count_nonzero(pandas.agreg1)
        powerflow.plimline = nonzero(pandas.agreg1.shape[0])

    return pandas
