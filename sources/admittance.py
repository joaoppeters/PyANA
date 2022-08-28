# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import complex, ndarray, zeros
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
        # Número de barras do sistema
        powerflow.setup.nbus = len(powerflow.setup.dbarraDF.tipo.values)

        # Matriz Admitância
        powerflow.setup.ybus: ndarray = zeros(shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype='complex_')
        self.admit(powerflow,)



    def admit(
        self,
        powerflow,
        ):
        """Método para cálculo dos parâmetros da matriz Admitância
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Linhas de transmissão e transformadores
        for _, value in powerflow.setup.dlinhaDF.iterrows():
            # Elementos fora da diagonal (elemento série)
            if value['tap'] == 0.:
                powerflow.setup.ybus[int(value['de']) - 1, int(value['para']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.setup.options['sbase']
                powerflow.setup.ybus[int(value['para']) - 1, int(value['de']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.setup.options['sbase']
            else:
                powerflow.setup.ybus[int(value['de']) - 1, int(value['para']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.setup.options['sbase']) / float(value['tap'])
                powerflow.setup.ybus[int(value['para']) - 1, int(value['de']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * powerflow.setup.options['sbase']) / float(value['tap'])

        # Bancos de capacitores e reatores
        for _, value in powerflow.setup.dbarraDF.iterrows():
            powerflow.setup.ybus[int(value['numero']) - 1, int(value['numero']) - 1] = sum(-powerflow.setup.ybus[:, int(value['numero']) - 1])
            # Elementos na diagonal (elemento shunt de barra)
            if value['shunt_barra'] != 0.:
                powerflow.setup.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=float(value['shunt_barra'])) / powerflow.setup.options['sbase']

            for _, v in powerflow.setup.dlinhaDF.iterrows():
                ## Elementos na diagonal 
                # (shunt de linha)
                if v['de'] == value['numero'] or v['para'] == value['numero']:
                    if v['susceptancia'] != 0.:
                        powerflow.setup.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=v['susceptancia']) / (2 * powerflow.setup.options['sbase'])
                # (transformador)   
                if v['tap'] != 0:
                    if value['numero'] == v['de']:
                        powerflow.setup.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += (((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.setup.options['sbase']) / float(v['tap'])) * (1 / float(v['tap']) - 1)

                    elif value['numero'] == v['para']:
                        powerflow.setup.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += ((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * powerflow.setup.options['sbase']) * (1 - 1 / float(v['tap']))


        # Salva matriz admitância em arquivo formato `.csv`
        Folder(powerflow.setup,).admittance(powerflow.setup,)
        DF(powerflow.setup.ybus).to_csv(f'{powerflow.setup.dirRadmittance + powerflow.setup.name + "-"}ybus.csv', header=None, index=None, sep=',')