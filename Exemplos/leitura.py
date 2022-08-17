# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

'''
licenciado e adaptado de amandapavila: https://github.com/amandapavila/GovernorPowerFlow
'''

import numpy as np
import pandas as pd
import sys


class LeituraPWF:
    """classe para leitura do arquivo de dados eletricos
    """

    def __init__(self):
        """__init__ method

        Parametros
        ----------
        arqv: str, obrigatorio
            Diretório onde está localizado arquivo .pwf contendo os dados do sistema elétrico em estudo
        """
        self.count = 0
        self._keywords()
        self._dbar()
        self._dlin()
        

    def _keywords(self):
        """Classificacao das palavras-chave contidas em arquivo .pwf
        """
        self.end_archive = 'FIM'
        self.end_block = ('9999', '99999')
        self.comment = '('


    def _dbar(self):
        """Inicializacao de leitura de dados de barra
        """
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


    def _dlin(self):
        """Inicializacao de leitura de dados de linha
        """
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


    def _readfile(self, arqv: str):
        """Inicializacao da leitura do arquivo .pwf

        Parametros
        ----------
        arqv: str, obrigatorio
            Diretório onde está localizado arquivo .pwf contendo os dados do sistema elétrico em estudo
        
        Retorno
        -------
        dbar_df: DataFrame, obj
            Retorna a leitura completa dos dados de barra do sistema encontrados no arquivo .pwf

        dlin_df: DataFrame, obj
            Retorna a leitura completa dos dados de linha do sistema encontrados no arquivo .pwf
        """
        if arqv:
            f = open(f'{arqv}', 'r', encoding='latin-1')
            self.lines = f.readlines()
            f.close()
            self.pwf2py = {}
            qtd_barra = 0
        
        else:
            raise ValueError(
                "class LeituraPWF() should receive arqv=str as argument"
            )

        while self.lines[self.count].strip() != self.end_archive:

            if self.lines[self.count].strip() == 'DBAR':
                self.count += 1
                while self.lines[self.count].strip() not in self.end_block:
                    if self.lines[self.count][0] == self.comment:
                        pass

                    else:
                        qtd_barra += 1
                        self.pwf2py[self.lines[self.count][:5]] = qtd_barra
                        self.dbar['numero'].append(qtd_barra)
                        self.dbar['operacao'].append(self.lines[self.count][5])
                        self.dbar['estado'].append(self.lines[self.count][6])
                        self.dbar['tipo'].append(self.lines[self.count][7])
                        self.dbar['grupo_base_tensao'].append(self.lines[self.count][8:10])
                        if not any(c.isalpha() for c in self.lines[self.count][10:22]) or \
                            sum(i.isalpha() for i in self.lines[self.count][10:22]) < 5:
                            self.dbar['nome'].append("BARRA-{}".format(self.lines[self.count][:5].strip(" ")))
                        else:
                            self.dbar['nome'].append(self.lines[self.count][10:22].strip(" "))
                        self.dbar['grupo_limite_tensao'].append(self.lines[self.count][22:24])
                        self.dbar['tensao'].append(self.lines[self.count][24:28])
                        self.dbar['angulo'].append(self.lines[self.count][28:32])
                        self.dbar['potencia_ativa'].append(self.lines[self.count][32:37])
                        self.dbar['potencia_reativa'].append(self.lines[self.count][37:42])
                        self.dbar['potencia_reativa_min'].append(self.lines[self.count][42:47])
                        self.dbar['potencia_reativa_max'].append(self.lines[self.count][47:52])
                        self.dbar['barra_controlada'].append(self.lines[self.count][52:58])
                        self.dbar['demanda_ativa'].append(self.lines[self.count][58:63])
                        self.dbar['demanda_reativa'].append(self.lines[self.count][63:68])
                        self.dbar['capacitor_reator'].append(self.lines[self.count][68:73])
                        self.dbar['area'].append(self.lines[self.count][73:76])
                        self.dbar['demanda_tensao_base'].append(self.lines[self.count][76:80])
                        self.dbar['modo'].append(self.lines[self.count][80])
                        # self.dbar['agreg1'].append(self.lines[self.count][81:84])
                        # self.dbar['agreg2'].append(self.lines[self.count][84:87])
                        # self.dbar['agreg3'].append(self.lines[self.count][87:90])
                        # self.dbar['agreg4'].append(self.lines[self.count][90:93])
                        # self.dbar['agreg5'].append(self.lines[self.count][93:96])
                        # self.dbar['agreg6'].append(self.lines[self.count][96:99])
                        # self.dbar['agreg7'].append(self.lines[self.count][99:102])
                        # self.dbar['agreg8'].append(self.lines[self.count][102:105])
                        # self.dbar['agreg9'].append(self.lines[self.count][105:108])
                        # self.dbar['agreg10'].append(self.lines[self.count][108:111])

                    self.count += 1

            elif self.lines[self.count].strip() == 'DLIN':
                self.count += 1
                while self.lines[self.count].strip() not in self.end_block:
                    if self.lines[self.count][0] == self.comment:
                        pass

                    else:
                        self.dlin['from'].append(self.pwf2py[self.lines[self.count][:5]])
                        self.dlin['abertura_from'].append(self.lines[self.count][5])
                        self.dlin['operacao'].append(self.lines[self.count][7])
                        self.dlin['abertura_to'].append(self.lines[self.count][9])
                        self.dlin['to'].append(self.pwf2py[self.lines[self.count][10:15]])
                        self.dlin['circuito'].append(self.lines[self.count][15:17])
                        self.dlin['estado'].append(self.lines[self.count][17])
                        self.dlin['proprietario'].append(self.lines[self.count][18])
                        self.dlin['resistencia'].append(self.lines[self.count][20:26])
                        self.dlin['reatancia'].append(self.lines[self.count][26:32])
                        self.dlin['susceptancia'].append(self.lines[self.count][32:38])
                        self.dlin['tap'].append(self.lines[self.count][38:43])
                        self.dlin['tap_min'].append(self.lines[self.count][43:48])
                        self.dlin['tap_max'].append(self.lines[self.count][48:53])
                        self.dlin['defasagem'].append(self.lines[self.count][53:58])
                        self.dlin['barra_controlada'].append(self.lines[self.count][58:64])
                        self.dlin['capacidade_normal'].append(self.lines[self.count][64:68])
                        self.dlin['capacidade_emergencia'].append(self.lines[self.count][68:72])
                        self.dlin['numero_taps'].append(self.lines[self.count][72:74])
                        self.dlin['capacidade_equipamento'].append(self.lines[self.count][74:78])
                        # self.dlin['agreg1'].append(self.lines[self.count][78:81])
                        # self.dlin['agreg2'].append(self.lines[self.count][81:84])
                        # self.dlin['agreg3'].append(self.lines[self.count][84:87])
                        # self.dlin['agreg4'].append(self.lines[self.count][87:90])
                        # self.dlin['agreg5'].append(self.lines[self.count][90:93])
                        # self.dlin['agreg6'].append(self.lines[self.count][93:96])
                        # self.dlin['agreg7'].append(self.lines[self.count][96:99])
                        # self.dlin['agreg8'].append(self.lines[self.count][99:102])
                        # self.dlin['agreg9'].append(self.lines[self.count][102:105])
                        # self.dlin['agreg10'].append(self.lines[self.count][105:108])

                    self.count += 1


            self.count += 1

        self.dbar_df = self._treatment(pd.DataFrame(data=self.dbar), data='DBARRA')
        self.dlin_df = self._treatment(pd.DataFrame(data=self.dlin), data='DLINHA')

        if self.dbar_df.empty or self.dlin_df.empty:
            print('\033[91m404: file reading has failed!\033[0m')
            sys.exit()

        else:
            print('\033[93mFile read successfully!\033[0m')
            return self.dbar_df, self.dlin_df


    def _treatment(self, df: pd.DataFrame, data: str = None):
        """Tratamento dos valores padrao adotados na leitura do arquivo .pwf

        Parametros
        ----------
        df: DataFrame, obj
            Arquivo para tratamento dos valores padrao

        data: str, opicional


        Retorno
        -------
        df: DataFrame, obj
            Arquivo com valores padrao tratados
        """

        df = df.replace(r"^\s*$", '0', regex=True)

        if data == 'DBARRA':
            df = df.astype(
                {
                    'numero': 'int',
                    'operacao': 'int',
                    'estado': 'object',
                    'tipo': 'int',
                    'grupo_base_tensao': 'int',
                    'nome': 'str',
                    'grupo_limite_tensao': 'object',
                    'tensao': 'float',
                    'angulo': 'float',
                    'potencia_ativa': 'float',
                    'potencia_reativa': 'float',
                    'potencia_reativa_min': 'float',
                    'potencia_reativa_max': 'float',
                    'barra_controlada': 'int',
                    'demanda_ativa': 'float',
                    'demanda_reativa': 'float',
                    'capacitor_reator': 'float',
                    'area': 'int',
                    'demanda_tensao_base': 'int',
                    'modo': 'int',
                }
            )

        elif data == 'DLINHA':
            df = df.astype(
                {
                    'from': 'int',
                    'abertura_from': 'int',
                    'operacao': 'int',
                    'abertura_to': 'int',
                    'to': 'int',
                    'circuito': 'int',
                    'estado': 'int',
                    'proprietario': 'int',
                    'resistencia': 'float',
                    'reatancia': 'float',
                    'susceptancia': 'float',
                    'tap': 'float',
                    'tap_min': 'float',
                    'tap_max': 'float',
                    'defasagem': 'float',
                    'barra_controlada': 'int',
                    'capacidade_normal': 'float',
                    'capacidade_emergencia': 'float',
                    'numero_taps': 'int',
                    'capacidade_equipamento': 'float',
                }
            )

        return df



