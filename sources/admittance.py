# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import complex, ndarray, zeros
from os.path import dirname
from pandas import DataFrame as DF

from folder import Folder

class Ybus:
    """classe para construção da matriz admitância"""

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
        # Número de barras do sistema
        self.nbus = len(powerflow.dbarraDF.tipo.values)

        # Matriz Admitância
        powerflow.ybus: ndarray = zeros(shape=[self.nbus, self.nbus], dtype='complex_')
        self.admit(powerflow, setup, )



    def admit(
        self,
        powerflow,
        setup,
        ):
        """Método para cálculo dos parâmetros da matriz Admitância
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        # Linhas de transmissão e transformadores
        for _, value in powerflow.dlinhaDF.iterrows():
            # Elementos fora da diagonal (elemento série)
            if value['tap'] == 0.:
                powerflow.ybus[int(value['de']) - 1, int(value['para']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.options['sbase']
                powerflow.ybus[int(value['para']) - 1, int(value['de']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.options['sbase']
            else:
                powerflow.ybus[int(value['de']) - 1, int(value['para']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.options['sbase']) / float(value['tap'])
                powerflow.ybus[int(value['para']) - 1, int(value['de']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.options['sbase']) / float(value['tap'])

        # Bancos de capacitores e reatores
        for _, value in powerflow.dbarraDF.iterrows():
            powerflow.ybus[int(value['numero']) - 1, int(value['numero']) - 1] = sum(-powerflow.ybus[:, int(value['numero']) - 1])
            # Elementos na diagonal (elemento shunt de barra)
            if value['shunt_barra'] != 0.:
                powerflow.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=float(value['shunt_barra'])) / powerflow.options['sbase']

            for _, v in powerflow.dlinhaDF.iterrows():
                ## Elementos na diagonal 
                # (shunt de linha)
                if v['de'] == value['numero'] or v['para'] == value['numero']:
                    if v['susceptancia'] != 0.:
                        powerflow.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=v['susceptancia']) / (2 * powerflow.options['sbase'])
                # (transformador)   
                if v['tap'] != 0:
                    if value['numero'] == v['de']:
                        powerflow.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += (((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.options['sbase']) / float(v['tap'])) * (1 / float(v['tap']) - 1)

                    elif value['numero'] == v['para']:
                        powerflow.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += ((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.options['sbase']) * (1 - 1 / float(v['tap']))


        # Salva matriz admitância em arquivo formato `.csv`
        Folder(setup,).admittance(setup,)
        DF(powerflow.ybus).to_csv(f'{setup.dirRadmittance + setup.name + "-"}ybus.csv', header=None, index=None, sep=',')