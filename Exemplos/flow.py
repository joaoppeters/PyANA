import pandas as pd
import sys
from os import path
from numpy import abs, array, concatenate, cos, linalg, max, ndarray, radians, savetxt, sin, zeros

class PowerFlow:
    """Classe para cálculo do fluxo de potência newton-raphson
    """

    def __init__(
        self, 
        dbarra: pd.DataFrame = None,
        dlinha: pd.DataFrame = None,
        dir: str = '',
        sistema: str = '',
        ):
        """Método __init__
        
        Parametros
        ----------
        dbarra: pd.DataFrame, obrigatorio
        dlinha: pd.DataFrame, obrigatorio
        dir: str, 
        """

        self.dbarra = dbarra
        self.dlinha = dlinha
        self.dir = dir
        self.sistema = sistema.split(".")[0]

        if len(self.dbarra.index) == 0:
            raise ValueError(
                "DBARRA DataFrame vazio"
            )

        if len(self.dlinha.index) == 0:
            raise ValueError(
                "DLINHA DataFrame vazio"
            )

        # Número de barras do sistema
        self.nbus = len(dbarra.tipo.values)
        self.npv = (dbarra.tipo.values == 1).sum()
        self.nger = self.npv + 1
        self.npq = self.nbus - self.nger
        self.dim = 2 * self.nbus

        # Número de linhas do sistema
        self.nlin = len(dlinha.to.values)

        # Potência base do sistema (em MVA)
        self.sbase = 100

        self.ybus: ndarray = zeros(shape=[self.nbus, self.nbus], dtype='complex_')
        self.calc_ybus()

        # Iteration counter
        self.iter = 0
        self.iter_max = 10

        # Tolerance
        self.e = 1E-6

        self.sol = {
            'dir': self.dir,
            'sistema': self.sistema,   
            'dbarra': self.dbarra,
            'dlinha': self.dlinha,
            'sbase': self.sbase,
            'nbus': self.nbus,
            'nlin': self.nlin,
            'voltage': array(self.dbarra['tensao'] * 1e-3),
            'theta': array(radians(self.dbarra['angulo'])),
            'active': zeros(self.nbus),
            'reactive': zeros(self.nbus),
            'active_flow_F2': zeros(len(self.dlinha['from'])),
            'reactive_flow_F2': zeros(len(self.dlinha['from'])),
            'active_flow_2F': zeros(len(self.dlinha['from'])),
            'reactive_flow_2F': zeros(len(self.dlinha['from'])),
        }



    def calc_ybus(self):
        """Método para cálculo dos parâmetros da matriz Ybus
        """

        # Linhas de transmissão e transformadores
        for idx, value in self.dlinha.iterrows():

            # Elementos fora da diagonal (elemento série)
            if value['tap'] == 0.:
                self.ybus[int(value['from']) - 1, int(value['to']) - 1] -= (1 / complex(real=value['resistencia'],
                                                                              imag=value['reatancia'])) * self.sbase
                self.ybus[int(value['to']) - 1, int(value['from']) - 1] -= (1 / complex(real=value['resistencia'],
                                                                              imag=value['reatancia'])) * self.sbase
            else:
                self.ybus[int(value['from']) - 1, int(value['to']) - 1] -= (1 / complex(real=value['resistencia'],
                                                                              imag=value['reatancia'])) * self.sbase \
                                                                 / float(value['tap'])
                self.ybus[int(value['to']) - 1, int(value['from']) - 1] -= (1 / complex(real=value['resistencia'],
                                                                              imag=value['reatancia'])) * self.sbase \
                                                                 / float(value['tap'])

            # Elementos na diagonal (elemento série)
            if value['tap'] == 0.:
                self.ybus[int(value['from']) - 1, int(value['from']) - 1] += (1 / complex(real=value['resistencia'], imag=value['reatancia'])) \
                                                               * self.sbase
            else:
                self.ybus[int(value['from']) - 1, int(value['from']) - 1] += (1 / complex(real=value['resistencia'], imag=value['reatancia'])) \
                                                               * self.sbase / float(value['tap']) ** 2

            self.ybus[int(value['to']) - 1, int(value['to']) - 1] += (1 / complex(real=value['resistencia'], imag=value['reatancia'])) \
                                                               * self.sbase

            # Elementos na diagonal (elemento shunt)
            if value['susceptancia'] == 0.:
                pass
            else:
                self.ybus[int(value['from']) - 1, int(value['from']) - 1] += complex(real=0., imag=float(value['susceptancia'])
                                                                                     / (2 * self.sbase))

                self.ybus[int(value['to']) - 1, int(value['to']) - 1] += complex(real=0., imag=float(value['susceptancia'])
                                                                                         / (2 * self.sbase))

        # Bancos de capacitores e reatores
        for idx, value in self.dbarra.iterrows():
            # Elementos na diagonal (elemento shunt)
            if value['capacitor_reator'] == 0.:
                pass
            else:
                self.ybus[int(value['numero']) - 1, int(value['numero']) - 1] += complex(real=0., imag=float(value['capacitor_reator'])
                                                                                       / self.sbase)

        if self.dir:
            pd.DataFrame(self.ybus).to_csv(f'{self.dir + "/Resultados/MatrizAdmitancia/" + self.sistema + "-"}ybus.csv', header=None, index=None, sep=',')



    def value_sche(self):
        """Método para armazenamento de parâmetros especificados
        """

        self.value_esp = {
            'potencia_ativa_especificada': zeros(self.nbus),
            'potencia_reativa_especificada': zeros(self.nbus),
        }

        for idx, value in self.dbarra.iterrows():

            # Potência ativa
            self.value_esp['potencia_ativa_especificada'][idx] += float(value['potencia_ativa'])
            self.value_esp['potencia_ativa_especificada'][idx] -= float(value['demanda_ativa'])

            # Potência reativa
            self.value_esp['potencia_reativa_especificada'][idx] += float(value['potencia_reativa'])
            self.value_esp['potencia_reativa_especificada'][idx] -= float(value['demanda_reativa'])


        self.value_esp['potencia_ativa_especificada'] /= self.sbase
        self.value_esp['potencia_reativa_especificada'] /= self.sbase



    def calc_p(self, bar):
        """Método para cálculo da potência ativa na barra bar
        """

        p = 0.

        for idx in range(self.nbus):
            p += self.sol['voltage'][idx] * \
                (self.ybus[bar][idx].real * cos(self.sol['theta'][bar] - self.sol['theta'][idx]) +
                self.ybus[bar][idx].imag * sin(self.sol['theta'][bar] - self.sol['theta'][idx]))

        p *= self.sol['voltage'][bar]

        self.sol['active'][bar] = (p * self.sbase) + self.dbarra['demanda_ativa'][bar]

        return p



    def calc_q(self, bar):
        """Método para cálculo da potência reativa na barra bar
        """

        q = 0.

        for idx in range(self.nbus):
            q += self.sol['voltage'][idx] * \
                (self.ybus[bar][idx].real * sin(self.sol['theta'][bar] - self.sol['theta'][idx]) -
                self.ybus[bar][idx].imag * cos(self.sol['theta'][bar] - self.sol['theta'][idx]))


        q *= self.sol['voltage'][bar]

        self.sol['reactive'][bar] = (q * self.sbase) + self.dbarra['demanda_reativa'][bar]

        return q



    def jacobiana(self):
        """Método para cálculo da matriz Jacobiana Expandida
        """

        # Submatrizes da matriz jacobiana
        self.h = zeros([self.nbus, self.nbus])
        self.n = zeros([self.nbus, self.nbus])
        self.m = zeros([self.nbus, self.nbus])
        self.l = zeros([self.nbus, self.nbus])

        for idx in range(self.nbus):
            for idy in range(self.nbus):
                if idx is idy:
                    # Elemento Hkk
                    self.h[idx, idy] += (-self.sol['voltage'][idx] ** 2) * self.ybus[idx][idy].imag - self.calc_q(idx)

                    # Elemento Nkk
                    self.n[idx, idy] += (self.calc_p(idx) + self.sol['voltage'][idx] ** 2 * self.ybus[idx][idy].real) \
                                        / self.sol['voltage'][idx]

                    # Elemento Mkk
                    self.m[idx, idy] += self.calc_p(idx) - (self.sol['voltage'][idx] ** 2) * self.ybus[idx][idy].real

                    # Elemento Lkk
                    self.l[idx, idy] += (self.calc_q(idx) - self.sol['voltage'][idx] ** 2 * self.ybus[idx][idy].imag) \
                                        / self.sol['voltage'][idx]
                else:
                    # Elemento Hkm
                    self.h[idx, idy] += self.sol['voltage'][idx] * self.sol['voltage'][idy] * (
                            self.ybus[idx][idy].real * sin(self.sol['theta'][idx] - self.sol['theta'][idy]) -
                            self.ybus[idx][idy].imag * cos(self.sol['theta'][idx] - self.sol['theta'][idy]))

                    # Elemento Nkm
                    self.n[idx, idy] += self.sol['voltage'][idx] * (
                            self.ybus[idx][idy].real * cos(self.sol['theta'][idx] - self.sol['theta'][idy]) +
                            self.ybus[idx][idy].imag * sin(self.sol['theta'][idx] - self.sol['theta'][idy]))

                    # Elemento Mkm
                    self.m[idx, idy] -= self.sol['voltage'][idx] * self.sol['voltage'][idy] * (
                            self.ybus[idx][idy].real * cos(self.sol['theta'][idx] - self.sol['theta'][idy]) +
                            self.ybus[idx][idy].imag * sin(self.sol['theta'][idx] - self.sol['theta'][idy]))

                    # Elemento Lkm
                    self.l[idx, idy] += self.sol['voltage'][idx] * (
                            self.ybus[idx][idy].real * sin(self.sol['theta'][idx] - self.sol['theta'][idy]) -
                            self.ybus[idx][idy].imag * cos(self.sol['theta'][idx] - self.sol['theta'][idy]))

        
        self.jacob = concatenate((concatenate((self.h, self.m), axis=0),
                                    concatenate((self.n, self.l), axis=0)),
                                    axis=1)

        for idx in range(self.nbus):
            if self.dbarra.tipo[idx] == 2:
                self.jacob[idx, :] = 0
                self.jacob[:, idx] = 0
                self.jacob[idx, idx] = 1

                self.jacob[idx + self.nbus, :] = 0
                self.jacob[:, idx + self.nbus] = 0
                self.jacob[idx + self.nbus, idx + self.nbus] = 1

            elif self.dbarra.tipo[idx] == 1:
                self.jacob[idx + self.nbus, :] = 0
                self.jacob[:, idx + self.nbus] = 0
                self.jacob[idx + self.nbus, idx + self.nbus] = 1



    def calc_res(self):
        """Método para cálculo dos resíduos
        """

        # Vetor de residuos
        self.deltaP = zeros(self.nbus)
        self.deltaQ = zeros(self.nbus)

        for idx, value in self.dbarra.iterrows():
            # Barra PQ
            if value['tipo'] == 0.:
                # Cálculo do resíduo DeltaP e DeltaQ
                self.deltaP[idx] += self.value_esp['potencia_ativa_especificada'][idx]
                self.deltaP[idx] -= self.calc_p(idx)

                self.deltaQ[idx] += self.value_esp['potencia_reativa_especificada'][idx]
                self.deltaQ[idx] -= self.calc_q(idx)

            # Barra PV
            elif value['tipo'] == 1:
                # Cálculo do resíduo DeltaP
                self.deltaP[idx] += self.value_esp['potencia_ativa_especificada'][idx]
                self.deltaP[idx] -= self.calc_p(idx)

        self.res = concatenate((self.deltaP, self.deltaQ), axis=0)



    def update_state_variables(self):
        """Método para atualização das variáveis de estado
        """
        
        self.sol['theta'] += self.state_variables[0:self.nbus]
        self.sol['voltage'] += self.state_variables[self.nbus:(2 * self.nbus)]

        if self.sol['voltage'].any() < 0.7 or self.sol['voltage'].any() > 1.5:
            print('\n')
            print(f"Solução Divergente (tensao)")
            print('\n')
            self.sol['solucao'] = 'Divergente (tensao)'
            self.sol['iteracoes'] = self.iter
            sys.exit(0)


    
    def line_flow(self):
        """Método para cálculo do fluxo de potência nas linhas de transmissão
        """

        for idx, value in self.dlinha.iterrows():
            k = int(value['from']) - 1
            m = int(value['to']) - 1
            yline = 1 / ((value['resistencia'] / 100) + 1j * (value['reatancia'] / 100))
            if value['tap'] != 0:
                yline /= value['tap']
            
            self.sol['active_flow_F2'][idx] = yline.real * (self.sol['voltage'][k] ** 2) - \
                self.sol['voltage'][k] * self.sol['voltage'][m] * (\
                    yline.real * cos(self.sol['theta'][k] - self.sol['theta'][m])\
                    + yline.imag * sin(self.sol['theta'][k] - self.sol['theta'][m])
            )

            self.sol['reactive_flow_F2'][idx] = -((value['susceptancia'] / (2*self.sbase)) + yline.imag) * (self.sol['voltage'][k] ** 2) + self.sol['voltage'][k] * self.sol['voltage'][m] * (
                yline.imag * cos(self.sol['theta'][k] - self.sol['theta'][m])
                - yline.real * sin(self.sol['theta'][k] - self.sol['theta'][m])
            )

            self.sol['active_flow_2F'][idx] = yline.real * (self.sol['voltage'][m] ** 2) - self.sol['voltage'][k] * self.sol['voltage'][m] * (
                yline.real * cos(self.sol['theta'][k] - self.sol['theta'][m])
                - yline.imag * sin(self.sol['theta'][k] - self.sol['theta'][m])
            )

            self.sol['reactive_flow_2F'][idx] = -((value['susceptancia'] / (2*self.sbase)) + yline.imag) * (self.sol['voltage'][m] ** 2) + self.sol['voltage'][k] * self.sol['voltage'][m] * (
                yline.imag * cos(self.sol['theta'][k] - self.sol['theta'][m])
                + yline.real * sin(self.sol['theta'][k] - self.sol['theta'][m])
            )

        self.sol['active_flow_F2'] *= self.sbase
        self.sol['active_flow_2F'] *= self.sbase

        self.sol['reactive_flow_F2'] *= self.sbase
        self.sol['reactive_flow_2F'] *= self.sbase



    def NewtonRaphson(self):
        """Método de Newton-Raphson
        """

        # Método de valores especificados
        self.value_sche()

        # Cálculo de resíduos para primeira iteração
        self.calc_res()

        while max(abs(self.res)) > self.e:
            # Atualiza matriz jacobiana
            self.jacobiana()

            # Resolve problema de programacao linear
            self.state_variables = linalg.solve(self.jacob, self.res)

            # Atualiza variaveis de estado
            self.update_state_variables()

            # Calcula residuos
            self.calc_res()
            
            # Se não convergiu
            # Incrementa contador de iteracoes
            self.iter += 1

            if self.iter > self.iter_max:
                break

        if self.iter > self.iter_max:
            print('\n')
            print(f"Solução Divergente (iter > iter_max)")
            print('\n')
            self.sol['solucao'] = 'Divergente (iter > iter_max)'
            self.sol['iteracoes'] = self.iter

        else:
            print('\n')
            print(f"Solução Convergente")
            print('\n')
            self.sol['solucao'] = 'Convergente'
            self.sol['iteracoes'] = self.iter
        
        savetxt(path.expanduser(self.dir + "/Resultados/MatrizJacobiana/" + self.sistema + "-matjacob.csv"), self.jacob, delimiter=',')
        self.line_flow()

        return self.sol