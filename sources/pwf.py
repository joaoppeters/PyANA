# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import ones
from pandas import DataFrame as DF

class PWF:
    """classe para leitura de dados PWF"""

    def __init__(
        self,
        powerflow,
        setup,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        # Variáveis
        self.linecount = 0

        # Funções
        self.keywords()

        # Códigos
        self.codes(setup,)
        
        # Leitura
        self.readfile(powerflow, setup,)



    def keywords(
        self,
    ):
        """palavras-chave de arquivo .pwf"""

        ## Inicialização
        self.end_archive = 'FIM'
        self.end_block = ('9999', '99999')
        self.comment = '('

    
    def codes(
        self,
        setup,
    ):
        """códigos de dados de execução implementados
        
        Parâmetros
            setup: self do arquivo setup.py
        """

        ## Inicialização
        # Variável
        setup.codes = {
            'DANC': False,
            'DBAR': False,
            'DGER': False,
            'DLIN': False,
        }



    def danc(
        self,
    ):
        """inicialização para leitura de dados de alteração do nível de carregamento"""

        ## Inicialização
        self.danc = dict()
        self.danc['area'] = list()
        self.danc['fator_carga_ativa'] = list()
        self.danc['fator_carga_reativa'] = list()
        self.danc['fator_shunt_barra'] = list()



    def dbar(
        self,
        ):
        """inicialização para leitura de dados de barra"""

        ## Inicialização
        self.dbar = dict()
        self.dbar['numero'] = list()
        self.dbar['operacao'] = list()
        self.dbar['estado'] = list()
        self.dbar['tipo'] = list()
        self.dbar['grupo_base_tensao'] = list()
        self.dbar['nome'] = list()
        self.dbar['grupo_limite_tensao'] = list()
        self.dbar['tensao'] = list()
        self.dbar['angulo'] = list()
        self.dbar['potencia_ativa'] = list()
        self.dbar['potencia_reativa'] = list()
        self.dbar['potencia_reativa_minima'] = list()
        self.dbar['potencia_reativa_maxima'] = list()
        self.dbar['barra_controlada'] = list()
        self.dbar['demanda_ativa'] = list()
        self.dbar['demanda_reativa'] = list()
        self.dbar['shunt_barra'] = list()
        self.dbar['area'] = list()
        self.dbar['demanda_tensao_base'] = list()
        self.dbar['modo'] = list()
        self.dbar['agreg1'] = list()
        self.dbar['agreg2'] = list()
        self.dbar['agreg3'] = list()
        self.dbar['agreg4'] = list()
        self.dbar['agreg5'] = list()
        self.dbar['agreg6'] = list()
        self.dbar['agreg7'] = list()
        self.dbar['agreg8'] = list()
        self.dbar['agreg9'] = list()
        self.dbar['agreg10'] = list()



    def dger(
        self,
    ):
        """inicialização para leitura de dados de geradores"""
        
        ## Inicialização
        self.dger = dict()
        self.dger['numero'] = list()
        self.dger['operacao'] = list()
        self.dger['potencia_ativa_minima'] = list()
        self.dger['potencia_ativa_maxima'] = list()
        self.dger['fator_participacao'] = list()
        self.dger['fator_participacao_controle_remoto'] = list()
        self.dger['fator_potencia_nominal'] = list()
        self.dger['fator_servico_armadura'] = list()
        self.dger['fator_servico_rotor'] = list()
        self.dger['angulo_maximo_carga'] = list()
        self.dger['reatancia_maquina'] = list()
        self.dger['potencia_aparente_nominal'] = list()
        self.dger['estatismo'] = list()



    def dlin(
        self,
        ):
        """inicialização para leitura de dados de linha"""

        ## Inicialização
        self.dlin = dict()
        self.dlin['de'] = list()
        self.dlin['abertura_de'] = list()
        self.dlin['operacao'] = list()
        self.dlin['abertura_para'] = list()
        self.dlin['para'] = list()
        self.dlin['circuito'] = list()
        self.dlin['estado'] = list()
        self.dlin['proprietario'] = list()
        self.dlin['resistencia'] = list()
        self.dlin['reatancia'] = list()
        self.dlin['susceptancia'] = list()
        self.dlin['tap'] = list()
        self.dlin['tap_minimo'] = list()
        self.dlin['tap_maximo'] = list()
        self.dlin['tap_defasagem'] = list()
        self.dlin['barra_controlada'] = list()
        self.dlin['capacidade_normal'] = list()
        self.dlin['capacidade_emergencial'] = list()
        self.dlin['numero_taps'] = list()
        self.dlin['capacidade_equipamento'] = list()
        self.dlin['agreg1'] = list()
        self.dlin['agreg2'] = list()
        self.dlin['agreg3'] = list()
        self.dlin['agreg4'] = list()
        self.dlin['agreg5'] = list()
        self.dlin['agreg6'] = list()
        self.dlin['agreg7'] = list()
        self.dlin['agreg8'] = list()
        self.dlin['agreg9'] = list()
        self.dlin['agreg10'] = list()



    def readfile(
        self,
        powerflow,
        setup,
        ):
        """leitura do arquivo .pwf
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        f = open(f'{setup.dirSEP}', 'r', encoding='latin-1')
        self.lines = f.readlines()
        f.close()
        self.pwf2py = {}

        # Loop de leitura de linhas do `.pwf`
        while self.lines[self.linecount].strip() != self.end_archive:
            # Dados de Alteração do Nível de Carregamento
            if self.lines[self.linecount].strip() == 'DANC':
                self.danc()
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass
                    else:
                        self.danc['area'].append(self.lines[self.linecount][:5])
                        self.danc['fator_carga_ativa'].append(self.lines[self.linecount][5:12])
                        self.danc['fator_carga_reativa'].append(self.lines[self.linecount][12:19])
                        self.danc['fator_shunt_barra'].append(self.lines[self.linecount][19:24])
                    self.linecount += 1
                
                # DataFrame dos Dados de Alteração do Nível de Carregamento
                setup.dancDF = self.treatment(setup, pandas=DF(data=self.danc), data='DANC')
                if setup.dancDF.empty:
                    ## ERROR - VERMELHO
                    raise ValueError('\033[91mERROR: Falha na leitura de código de execução `DANC`!\033[0m')
                else:
                    setup.codes['DANC'] = True
                
            # Dados de Barra
            elif self.lines[self.linecount].strip() == 'DBAR':
                setup.codes['DBAR'] = False
                self.dbar()
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass
                    else:
                        self.dbar['numero'].append(self.lines[self.linecount][:5])
                        self.dbar['operacao'].append(self.lines[self.linecount][5])
                        self.dbar['estado'].append(self.lines[self.linecount][6])
                        self.dbar['tipo'].append(self.lines[self.linecount][7])
                        self.dbar['grupo_base_tensao'].append(self.lines[self.linecount][8:10])
                        self.dbar['nome'].append(self.lines[self.linecount][10:22].split(' ')[0])
                        self.dbar['grupo_limite_tensao'].append(self.lines[self.linecount][22:24])
                        self.dbar['tensao'].append(self.lines[self.linecount][24:28])
                        self.dbar['angulo'].append(self.lines[self.linecount][28:32])
                        self.dbar['potencia_ativa'].append(self.lines[self.linecount][32:37])
                        self.dbar['potencia_reativa'].append(self.lines[self.linecount][37:42])
                        self.dbar['potencia_reativa_minima'].append(self.lines[self.linecount][42:47])
                        self.dbar['potencia_reativa_maxima'].append(self.lines[self.linecount][47:52])
                        self.dbar['barra_controlada'].append(self.lines[self.linecount][52:58])
                        self.dbar['demanda_ativa'].append(self.lines[self.linecount][58:63])
                        self.dbar['demanda_reativa'].append(self.lines[self.linecount][63:68])
                        self.dbar['shunt_barra'].append(self.lines[self.linecount][68:73])
                        self.dbar['area'].append(self.lines[self.linecount][73:76])
                        self.dbar['demanda_tensao_base'].append(self.lines[self.linecount][76:80])
                        self.dbar['modo'].append(self.lines[self.linecount][80])
                        self.dbar['agreg1'].append(self.lines[self.linecount][81:84])
                        self.dbar['agreg2'].append(self.lines[self.linecount][84:87])
                        self.dbar['agreg3'].append(self.lines[self.linecount][87:90])
                        self.dbar['agreg4'].append(self.lines[self.linecount][90:93])
                        self.dbar['agreg5'].append(self.lines[self.linecount][93:96])
                        self.dbar['agreg6'].append(self.lines[self.linecount][96:99])
                        self.dbar['agreg7'].append(self.lines[self.linecount][99:102])
                        self.dbar['agreg8'].append(self.lines[self.linecount][102:105])
                        self.dbar['agreg9'].append(self.lines[self.linecount][105:108])
                        self.dbar['agreg10'].append(self.lines[self.linecount][108:111])
                    self.linecount += 1
                
                # DataFrame dos Dados de Barra
                setup.dbarraDF = self.treatment(setup, pandas=DF(data=self.dbar), data='DBAR')
                if setup.dbarraDF.empty:
                    ## ERROR - VERMELHO
                    raise ValueError('\033[91mERROR: Falha na leitura de código de execução `DBAR`!\033[0m')
                else:
                    setup.codes['DBAR'] = True
                
            # Dados de Geradores
            elif self.lines[self.linecount].strip() == 'DGER':
                setup.codes['DGER'] = False
                self.dger()
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass
                    else:
                        self.dger['numero'].append(self.lines[self.linecount][:5])
                        self.dger['operacao'].append(self.lines[self.linecount][6])
                        self.dger['potencia_ativa_minima'].append(self.lines[self.linecount][8:14])
                        self.dger['potencia_ativa_maxima'].append(self.lines[self.linecount][15:21])
                        self.dger['fator_participacao'].append(self.lines[self.linecount][22:27])
                        self.dger['fator_participacao_controle_remoto'].append(self.lines[self.linecount][28:33])
                        self.dger['fator_potencia_nominal'].append(self.lines[self.linecount][34:39])
                        self.dger['fator_servico_armadura'].append(self.lines[self.linecount][40:44])
                        self.dger['fator_servico_rotor'].append(self.lines[self.linecount][45:49])
                        self.dger['angulo_maximo_carga'].append(self.lines[self.linecount][50:54])
                        self.dger['reatancia_maquina'].append(self.lines[self.linecount][55:60])
                        self.dger['potencia_aparente_nominal'].append(self.lines[self.linecount][61:66])
                        self.dger['estatismo'].append(self.lines[self.linecount][66:72])
                    self.linecount += 1

                # DataFrame dos Dados de Linha
                setup.dgeraDF = self.treatment(setup, pandas=DF(data=self.dger), data='DGER')
                if setup.dgeraDF.empty:
                    ## ERROR - VERMELHO
                    raise ValueError('\033[91mERROR: Falha na leitura de código de execução `DGER`!\033[0m')
                else:
                    setup.codes['DGER'] = True

            # Dados de Linha
            elif self.lines[self.linecount].strip() == 'DLIN':
                setup.codes['DLIN'] = False
                self.dlin()
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass
                    else:
                        self.dlin['de'].append(self.lines[self.linecount][:5])
                        self.dlin['abertura_de'].append(self.lines[self.linecount][5])
                        self.dlin['operacao'].append(self.lines[self.linecount][7])
                        self.dlin['abertura_para'].append(self.lines[self.linecount][9])
                        self.dlin['para'].append(self.lines[self.linecount][10:15])
                        self.dlin['circuito'].append(self.lines[self.linecount][15:17])
                        self.dlin['estado'].append(self.lines[self.linecount][17])
                        self.dlin['proprietario'].append(self.lines[self.linecount][18])
                        self.dlin['resistencia'].append(self.lines[self.linecount][20:26])
                        self.dlin['reatancia'].append(self.lines[self.linecount][26:32])
                        self.dlin['susceptancia'].append(self.lines[self.linecount][32:38])
                        self.dlin['tap'].append(self.lines[self.linecount][38:43])
                        self.dlin['tap_minimo'].append(self.lines[self.linecount][43:48])
                        self.dlin['tap_maximo'].append(self.lines[self.linecount][48:53])
                        self.dlin['tap_defasagem'].append(self.lines[self.linecount][53:58])
                        self.dlin['barra_controlada'].append(self.lines[self.linecount][58:64])
                        self.dlin['capacidade_normal'].append(self.lines[self.linecount][64:68])
                        self.dlin['capacidade_emergencial'].append(self.lines[self.linecount][68:72])
                        self.dlin['numero_taps'].append(self.lines[self.linecount][72:74])
                        self.dlin['capacidade_equipamento'].append(self.lines[self.linecount][74:78])
                        self.dlin['agreg1'].append(self.lines[self.linecount][78:81])
                        self.dlin['agreg2'].append(self.lines[self.linecount][81:84])
                        self.dlin['agreg3'].append(self.lines[self.linecount][84:87])
                        self.dlin['agreg4'].append(self.lines[self.linecount][87:90])
                        self.dlin['agreg5'].append(self.lines[self.linecount][90:93])
                        self.dlin['agreg6'].append(self.lines[self.linecount][93:96])
                        self.dlin['agreg7'].append(self.lines[self.linecount][96:99])
                        self.dlin['agreg8'].append(self.lines[self.linecount][99:102])
                        self.dlin['agreg9'].append(self.lines[self.linecount][102:105])
                        self.dlin['agreg10'].append(self.lines[self.linecount][105:108])
                    self.linecount += 1

                # DataFrame dos Dados de Linha
                setup.dlinhaDF = self.treatment(setup, pandas=DF(data=self.dlin), data='DLIN')
                if setup.dlinhaDF.empty:
                    ## ERROR - VERMELHO
                    raise ValueError('\033[91mERROR: Falha na leitura de código de execução `DLIN`!\033[0m')
                else:
                    setup.codes['DLIN'] = True

            self.linecount += 1

        ## SUCESSO NA LEITURA
        print(f'\033[32mSucesso na leitura de arquivo `{powerflow.system}`!\033[0m')



    def treatment(
        self,
        setup,
        pandas: DF=DF.empty,
        data: str='',
    ):
        """tratamento dos valores padrão adotadas nas leituras de códigos de execução
        
        Parâmetros
            setup: self do arquivo setup.py

            pandas: DataFrame, obrigatório, valor padrão DataFrame.empty
                Arquivo que contém a leitura e armazenamento de dados de um respectivo código de execução

            data: str, obrigatório, valor padrão 'None'
                String que indica o código de execução lido para que haja o tratamento de dados das variáveis armazenadas no DataFrame

        Retorno
            pandas: DataFrame
                Arquivo com os valores tratados
        """

        ## Inicialização
        # Tratamento inicial
        pandas = pandas.replace(r"^\s*$", '0', regex=True)

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
                    'demanda_tensao_base': 'float',
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
            setup.nbus = len(pandas.tipo.values)

            # Barras geradoras: número & máscara
            setup.nger = 0
            setup.mask = ones(2 * setup.nbus, bool)
            for idx, value in pandas.iterrows():
                if (value['tipo'] == 2) or (value['tipo'] == 1):
                    setup.nger += 1
                    setup.mask[setup.nbus+idx] = False
                    if (value['tipo'] == 2):
                        setup.mask[idx] = False
            
            # Número de barras PV
            setup.npv = setup.nger - 1

            # Número de barras PQ
            setup.npq = setup.nbus - setup.nger
        
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
                    'numero': 'int',
                    'operacao': 'object',
                    'grupo_base_svc': 'int',
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
            setup.nlin = len(pandas.de.values)

        return pandas