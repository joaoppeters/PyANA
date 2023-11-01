# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import ndarray, ones, vectorize, zeros
from pandas import DataFrame as DF

from folder import Folder

class Ybus:
    """classe para construção da matriz admitância"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Checa alteração no nível de carregamento
        self.checkdanc(powerflow,)

        # Matriz Admitância
        powerflow.setup.ybus: ndarray = zeros(shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype='complex_')
        self.admit(powerflow,)



    def checkdanc(
        self,
        powerflow,
    ):
        """checa alteração no nível de carregamento
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variável
        if (powerflow.setup.codes['DANC']):
            for area in powerflow.setup.dancDF['area'].values:
                for idx, value in powerflow.setup.dbarraDF.iterrows():
                    if (value['area'] == area):
                        powerflow.setup.dbarraDF.loc[idx, 'demanda_ativa'] *= (1 + powerflow.setup.dancDF['fator_carga_ativa'][0] / powerflow.setup.options['BASE'])
                        powerflow.setup.dbarraDF.loc[idx, 'demanda_reativa'] *= (1 + powerflow.setup.dancDF['fator_carga_reativa'][0] / powerflow.setup.options['BASE'])
                        powerflow.setup.dbarraDF.loc[idx, 'shunt_barra'] *= (1 + powerflow.setup.dancDF['fator_shunt_barra'][0] / powerflow.setup.options['BASE'])



    def admit(
        self,
        powerflow,
        ):
        """Método para cálculo dos parâmetros da matriz Admitância
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        powerflow.setup.gdiag = zeros(powerflow.setup.nbus)
        powerflow.setup.bdiag = zeros(powerflow.setup.nbus)
        powerflow.setup.apont = ones(powerflow.setup.nbus, dtype=int)
        powerflow.setup.admitancia = 1/vectorize(complex)(real=powerflow.setup.dlinhaDF['resistencia'], imag=powerflow.setup.dlinhaDF['reatancia'])
        
        # Linhas de transmissão e transformadores
        for _, value in powerflow.setup.dlinhaDF.iterrows():
            if (value['estado']):
                if (value['transf']):
                    value['tap'] = 1 / value['tap']

                    # Elementos da diagonal (elemento série)
                    powerflow.setup.admitancia[_] *= value['tap']

                    powerflow.setup.gdiag[value['de'] - 1] += (value['tap'] - 1.) * powerflow.setup.admitancia[_].real
                    powerflow.setup.bdiag[value['de'] - 1] += (value['tap'] - 1.) * powerflow.setup.admitancia[_].imag
                    powerflow.setup.gdiag[value['para'] - 1] += (1/value['tap'] - 1.) * powerflow.setup.admitancia[_].real
                    powerflow.setup.bdiag[value['para'] - 1] += (1/value['tap'] - 1.) * powerflow.setup.admitancia[_].imag

            
                # Elementos da diagonal (elemento série)
                powerflow.setup.gdiag[value['de'] - 1] += powerflow.setup.admitancia[_].real
                powerflow.setup.gdiag[value['para'] - 1] += powerflow.setup.admitancia[_].real
                powerflow.setup.bdiag[value['de'] - 1] += powerflow.setup.admitancia[_].imag + value['susceptancia']
                powerflow.setup.bdiag[value['para'] - 1] += powerflow.setup.admitancia[_].imag + value['susceptancia']

                # apontador auxiliar de conexões
                powerflow.setup.apont[value['de'] - 1] += 1
                powerflow.setup.apont[value['para'] - 1] += 1

        
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if (value['shunt_barra'] != 0.):
                powerflow.setup.bdiag[value['numero'] - 1] += value['shunt_barra'] / powerflow.setup.dcteDF.loc[powerflow.setup.dcteDF.constante == 'BASE'].valor_constante[0]

            if (idx != 0):
                powerflow.setup.apont[value['numero'] - 1] += powerflow.setup.apont[value['numero'] - 2]


        #     # Elementos fora da diagonal (elemento série)
        #     if (value['tap'] == 0.):
        #         powerflow.setup.ybus[powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['de']][0], powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['para']][0]] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * 1E2
        #         powerflow.setup.ybus[powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['para']][0], powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['de']][0]] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * 1E2
        #     else:
        #         powerflow.setup.ybus[powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['de']][0], powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['para']][0]] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * 1E2 / float(value['tap'])
        #         powerflow.setup.ybus[powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['para']][0], powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['de']][0]] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * 1E2 / float(value['tap'])

        # # Bancos de capacitores e reatores
        # for idx, value in powerflow.setup.dbarraDF.iterrows():
        #     powerflow.setup.ybus[idx, idx] = sum(-powerflow.setup.ybus[:, idx])
        #     # Elementos na diagonal (elemento shunt de barra)
        #     if (value['shunt_barra'] != 0.):
        #         powerflow.setup.ybus[idx, idx] += complex(real=0., imag=float(value['shunt_barra'])) / powerflow.setup.options['BASE']

        #     for _, v in powerflow.setup.dlinhaDF.iterrows():
        #         ## Elementos na diagonal 
        #         # (shunt de linha)
        #         if (v['de'] == value['numero']) or (v['para'] == value['numero']):
        #             if (v['susceptancia'] != 0.):
        #                 powerflow.setup.ybus[idx, idx] += complex(real=0., imag=v['susceptancia']) / (2 * powerflow.setup.options['BASE'])
        #         # (transformador)   
        #         if (v['tap'] != 0):
        #             if (value['numero'] == v['de']):
        #                 powerflow.setup.ybus[idx, idx] += (((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.setup.options['BASE']) / float(v['tap'])) * (1 / float(v['tap']) - 1)

        #             elif (value['numero'] == v['para']):
        #                 powerflow.setup.ybus[idx, idx] += ((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.setup.options['BASE']) * (1 - 1 / float(v['tap']))

        # Condição
        if (powerflow.method != 'CPF'):
            # Salva matriz admitância em arquivo formato `.csv`
            Folder(powerflow.setup,).admittance(powerflow.setup,)
            DF(powerflow.setup.ybus).to_csv(f'{powerflow.setup.dirRadmittance + powerflow.setup.name + "-"}admittance.csv', header=None, index=None, sep=',')