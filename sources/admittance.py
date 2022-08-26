# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import ndarray, zeros
from pandas import DataFrame as DF


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
        self.nbus = len(powerflow.dbarraDF.tipo.values)

        # Matriz Admitância
        self.ybus: ndarray = zeros(shape=[self.nbus, self.nbus], dtype='complex_')
        self.calc_ybus()



        def calc_ybus(self):
            """Método para cálculo dos parâmetros da matriz Admitância"""

            # Linhas de transmissão e transformadores
            for idx, value in powerflow.dlinhaDF.iterrows():

                # Elementos fora da diagonal (elemento série)
                if value['tap'].strip() == '':
                    self.ybus[int(value['from']) - 1, int(value['to']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * self.sbase
                    self.ybus[int(value['to']) - 1, int(value['from']) - 1] -= (1 / complex(real=value['resistencia'], imag=value['reatancia'])) * self.sbase
                else:
                    self.ybus[int(value['from']) - 1, int(value['to']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * self.sbase) / float(value['tap'])
                    self.ybus[int(value['to']) - 1, int(value['from']) - 1] -= ((1 / complex(real=value['resistencia'], imag=value['reatancia'])) * self.sbase) / float(value['tap'])

            # Bancos de capacitores e reatores
            for idx, value in self.dbarraDF.iterrows():
                self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] = sum(-self.ybus[:, int(value['numero']) - 1])
                # Elementos na diagonal (elemento shunt de barra)
                if value['capacitor_reator'] != 0.:
                    self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=float(value['shunt_barra'])) / self.sbase

                for i, v in self.dlinhaDF.iterrows():
                    ## Elementos na diagonal 
                    # (shunt de linha)
                    if v['from'] == value['numero'] or v['to'] == value['numero']:
                        if v['susceptancia'].strip() != '':
                            self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=v['susceptancia']) / (2 * self.sbase)
                    # (transformador)   
                    if v['tap'] != 0:
                        if value['numero'] == v['from']:
                            self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += (((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * self.sbase) / float(v['tap'])) * (1 / float(v['tap']) - 1)

                        elif value['numero'] == v['to']:
                            self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += ((1 / complex(real=v['resistencia'], imag=v['reatancia'])) * self.sbase) * (1 - 1 / float(v['tap']))


            # Salva matriz admitância em arquivo .csv
            if self.dir:
                DF(self.ybus).to_csv(f'{self.dir + "/Resultados/MatrizAdmitancia/" + self.sistema + "-"}ybus.csv', header=None, index=None, sep=',')



                # Linhas de transmissão e transformadores
                for idx, value in self.dlin.iterrows():

                    # Elementos fora da diagonal (elemento série)
                    if value['tap'].strip() == '':
                        self.ybus[value['de'] - 1, value['para'] - 1] -= (1 / complex(real=value['resist'],
                                                                                    imag=value['reat'])) * self.sbase
                        self.ybus[value['para'] - 1, value['de'] - 1] -= (1 / complex(real=value['resist'],
                                                                                    imag=value['reat'])) * self.sbase
                    else:
                        self.ybus[value['de'] - 1, value['para'] - 1] -= (1 / complex(real=value['resist'],
                                                                                    imag=value['reat'])) * self.sbase \
                                                                        / float(value['tap'])
                        self.ybus[value['para'] - 1, value['de'] - 1] -= (1 / complex(real=value['resist'],
                                                                                    imag=value['reat'])) * self.sbase \
                                                                        / float(value['tap'])

                    # Elementos na diagonal (elemento série)
                    if value['tap'].strip() == '':
                        self.ybus[value['de'] - 1, value['de'] - 1] += (1 / complex(real=value['resist'], imag=value['reat'])) \
                                                                    * self.sbase
                    else:
                        self.ybus[value['de'] - 1, value['de'] - 1] += (1 / complex(real=value['resist'], imag=value['reat'])) \
                                                                    * self.sbase / float(value['tap']) ** 2

                    self.ybus[value['para'] - 1, value['para'] - 1] += (1 / complex(real=value['resist'], imag=value['reat'])) \
                                                                    * self.sbase

                    # Elementos na diagonal (elemento shunt)
                    if value['suscep'].strip() == '':
                        pass
                    else:
                        self.ybus[value['de'] - 1, value['de'] - 1] += complex(real=0., imag=float(value['suscep'])
                                                                                            / (2 * self.sbase))

                        self.ybus[value['para'] - 1, value['para'] - 1] += complex(real=0., imag=float(value['suscep'])
                                                                                                / (2 * self.sbase))
                # Bancos de capacitores e reatores
                for idx, value in self.dbar.iterrows():
                    # Elementos na diagonal (elemento shunt)
                    if value['capac_reat'].strip() == '':
                        pass
                    else:
                        self.ybus[value['num'] - 1, value['num'] - 1] += complex(real=0., imag=float(value['capac_reat'])
                                                                                            / self.sbase)

                if file_out:
                    DF(self.ybus).to_csv(f'{file_out}ybus.csv', header=None, index=None, sep=',')

                return self.ybus