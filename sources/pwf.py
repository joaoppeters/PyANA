# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from os.path import exists
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

        if exists(setup.arqv) is True:
            ## Inicialização
            # Variáveis
            self.linecount = 0

            # Funções
            self.keywords()
            self.dbarra()
            self.dlinha()
            # self.dsvc()
            
            # Leitura
            self.readfile(powerflow, setup,)

        else:
            ## ERROR - AMARELO
            raise ValueError('\033[93mEsse sistema não está presente na pasta de `sistemas/`.\033[0m')



    def keywords(
        self,
        ):
        """Palavras-chave de arquivo .pwf"""

        self.end_archive = 'FIM'
        self.end_block = ('9999', '99999')
        self.comment = '('



    def dbarra(
        self,
        ):
        """Inicialização das colunas de dados de barra"""

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
        self.dbar['potencia_reativa_min'] = list()
        self.dbar['potencia_reativa_max'] = list()
        self.dbar['barra_controlada'] = list()
        self.dbar['demanda_ativa'] = list()
        self.dbar['demanda_reativa'] = list()
        self.dbar['capacitor_reator'] = list()
        self.dbar['area'] = list()
        self.dbar['demanda_tensao_base'] = list()
        self.dbar['modo'] = list()
        # self.dbar['agreg1'] = list()
        # self.dbar['agreg2'] = list()
        # self.dbar['agreg3'] = list()
        # self.dbar['agreg4'] = list()
        # self.dbar['agreg5'] = list()
        # self.dbar['agreg6'] = list()
        # self.dbar['agreg7'] = list()
        # self.dbar['agreg8'] = list()
        # self.dbar['agreg9'] = list()
        # self.dbar['agreg10'] = list()



    def dlinha(
        self,
        ):
        """Inicialização das colunas de dados de linha"""

        self.dlin = dict()
        self.dlin['from'] = list()
        self.dlin['abertura_from'] = list()
        self.dlin['operacao'] = list()
        self.dlin['abertura_to'] = list()
        self.dlin['to'] = list()
        self.dlin['circuito'] = list()
        self.dlin['estado'] = list()
        self.dlin['proprietario'] = list()
        self.dlin['resistencia'] = list()
        self.dlin['reatancia'] = list()
        self.dlin['susceptancia'] = list()
        self.dlin['tap'] = list()
        self.dlin['tap_min'] = list()
        self.dlin['tap_max'] = list()
        self.dlin['defasagem'] = list()
        self.dlin['barra_controlada'] = list()
        self.dlin['capacidade_normal'] = list()
        self.dlin['capacidade_emergencia'] = list()
        self.dlin['numero_taps'] = list()
        self.dlin['capacidade_equipamento'] = list()
        # self.dlin['agreg1'] = list()
        # self.dlin['agreg2'] = list()
        # self.dlin['agreg3'] = list()
        # self.dlin['agreg4'] = list()
        # self.dlin['agreg5'] = list()
        # self.dlin['agreg6'] = list()
        # self.dlin['agreg7'] = list()
        # self.dlin['agreg8'] = list()
        # self.dlin['agreg9'] = list()
        # self.dlin['agreg10'] = list()



    def readfile(
        self,
        powerflow,
        setup,
        ):
        """Leitura do arquivo .pwf
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        f = open(f'{setup.arqv}', 'r', encoding='latin-1')
        self.lines = f.readlines()
        f.close()
        self.pwf2py = {}
        qtd_barra = 0

        while self.lines[self.linecount].strip() != self.end_archive:

            if self.lines[self.linecount].strip() == 'DBAR':
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass

                    else:
                        qtd_barra += 1
                        self.pwf2py[self.lines[self.linecount][:5]] = qtd_barra
                        self.dbar['numero'].append(qtd_barra)
                        self.dbar['operacao'].append(self.lines[self.linecount][5])
                        self.dbar['estado'].append(self.lines[self.linecount][6])
                        self.dbar['tipo'].append(self.lines[self.linecount][7])
                        self.dbar['grupo_base_tensao'].append(self.lines[self.linecount][8:10])
                        if not any(c.isalpha() for c in self.lines[self.linecount][10:22]) or \
                            sum(i.isalpha() for i in self.lines[self.linecount][10:22]) < 5:
                            self.dbar['nome'].append("BARRA-{}".format(self.lines[self.linecount][:5].strip(" ")))
                        else:
                            self.dbar['nome'].append(self.lines[self.linecount][10:22].strip(" "))
                        self.dbar['grupo_limite_tensao'].append(self.lines[self.linecount][22:24])
                        self.dbar['tensao'].append(self.lines[self.linecount][24:28])
                        self.dbar['angulo'].append(self.lines[self.linecount][28:32])
                        self.dbar['potencia_ativa'].append(self.lines[self.linecount][32:37])
                        self.dbar['potencia_reativa'].append(self.lines[self.linecount][37:42])
                        self.dbar['potencia_reativa_min'].append(self.lines[self.linecount][42:47])
                        self.dbar['potencia_reativa_max'].append(self.lines[self.linecount][47:52])
                        self.dbar['barra_controlada'].append(self.lines[self.linecount][52:58])
                        self.dbar['demanda_ativa'].append(self.lines[self.linecount][58:63])
                        self.dbar['demanda_reativa'].append(self.lines[self.linecount][63:68])
                        self.dbar['capacitor_reator'].append(self.lines[self.linecount][68:73])
                        self.dbar['area'].append(self.lines[self.linecount][73:76])
                        self.dbar['demanda_tensao_base'].append(self.lines[self.linecount][76:80])
                        self.dbar['modo'].append(self.lines[self.linecount][80])
                        # self.dbar['agreg1'].append(self.lines[self.linecount][81:84])
                        # self.dbar['agreg2'].append(self.lines[self.linecount][84:87])
                        # self.dbar['agreg3'].append(self.lines[self.linecount][87:90])
                        # self.dbar['agreg4'].append(self.lines[self.linecount][90:93])
                        # self.dbar['agreg5'].append(self.lines[self.linecount][93:96])
                        # self.dbar['agreg6'].append(self.lines[self.linecount][96:99])
                        # self.dbar['agreg7'].append(self.lines[self.linecount][99:102])
                        # self.dbar['agreg8'].append(self.lines[self.linecount][102:105])
                        # self.dbar['agreg9'].append(self.lines[self.linecount][105:108])
                        # self.dbar['agreg10'].append(self.lines[self.linecount][108:111])

                    self.linecount += 1

            elif self.lines[self.linecount].strip() == 'DLIN':
                self.linecount += 1
                while self.lines[self.linecount].strip() not in self.end_block:
                    if self.lines[self.linecount][0] == self.comment:
                        pass

                    else:
                        self.dlin['from'].append(self.pwf2py[self.lines[self.linecount][:5]])
                        self.dlin['abertura_from'].append(self.lines[self.linecount][5])
                        self.dlin['operacao'].append(self.lines[self.linecount][7])
                        self.dlin['abertura_to'].append(self.lines[self.linecount][9])
                        self.dlin['to'].append(self.pwf2py[self.lines[self.linecount][10:15]])
                        self.dlin['circuito'].append(self.lines[self.linecount][15:17])
                        self.dlin['estado'].append(self.lines[self.linecount][17])
                        self.dlin['proprietario'].append(self.lines[self.linecount][18])
                        self.dlin['resistencia'].append(self.lines[self.linecount][20:26])
                        self.dlin['reatancia'].append(self.lines[self.linecount][26:32])
                        self.dlin['susceptancia'].append(self.lines[self.linecount][32:38])
                        self.dlin['tap'].append(self.lines[self.linecount][38:43])
                        self.dlin['tap_min'].append(self.lines[self.linecount][43:48])
                        self.dlin['tap_max'].append(self.lines[self.linecount][48:53])
                        self.dlin['defasagem'].append(self.lines[self.linecount][53:58])
                        self.dlin['barra_controlada'].append(self.lines[self.linecount][58:64])
                        self.dlin['capacidade_normal'].append(self.lines[self.linecount][64:68])
                        self.dlin['capacidade_emergencia'].append(self.lines[self.linecount][68:72])
                        self.dlin['numero_taps'].append(self.lines[self.linecount][72:74])
                        self.dlin['capacidade_equipamento'].append(self.lines[self.linecount][74:78])
                        # self.dlin['agreg1'].append(self.lines[self.linecount][78:81])
                        # self.dlin['agreg2'].append(self.lines[self.linecount][81:84])
                        # self.dlin['agreg3'].append(self.lines[self.linecount][84:87])
                        # self.dlin['agreg4'].append(self.lines[self.linecount][87:90])
                        # self.dlin['agreg5'].append(self.lines[self.linecount][90:93])
                        # self.dlin['agreg6'].append(self.lines[self.linecount][93:96])
                        # self.dlin['agreg7'].append(self.lines[self.linecount][96:99])
                        # self.dlin['agreg8'].append(self.lines[self.linecount][99:102])
                        # self.dlin['agreg9'].append(self.lines[self.linecount][102:105])
                        # self.dlin['agreg10'].append(self.lines[self.linecount][105:108])

                    self.linecount += 1

            self.linecount += 1

        # DataFrame dos Dados de Barra
        powerflow.dbarraDF = DF(data=self.dbar)

        # DataFrame dos Dados de Linha
        powerflow.dlinhaDF = DF(data=self.dlin)

        if powerflow.dbarraDF.empty or powerflow.dlinhaDF.empty:
            ## ERROR - VERMELHO
            raise ValueError('\033[91mERROR: Falha na leitura de arquivo!\033[0m')

        else:
            ## SUCESSO
            print('\033[32mSucesso na leitura de arquivo!\033[0m')