# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import concatenate, cos, ndarray, ones, savetxt, sin, zeros
from os.path import exists
from os import remove

from calc import PQCalc
from ctrl import Control
from folder import Folder

class Jacobi:
    """classe para construção da matriz Jacobiana"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Chamada da função para cálculo da matriz Jacobiana
        self.jacobi(powerflow,)


    
    def jacobi(
        self,
        powerflow,
    ):
        """cálculo das submatrizes da matriz Jacobiana
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Submatrizes da matriz jacobiana
        powerflow.setup.pt = zeros([powerflow.setup.nbus, powerflow.setup.nbus])
        powerflow.setup.pv = zeros([powerflow.setup.nbus, powerflow.setup.nbus])
        powerflow.setup.qt = zeros([powerflow.setup.nbus, powerflow.setup.nbus])
        powerflow.setup.qv = zeros([powerflow.setup.nbus, powerflow.setup.nbus])

        for idx in range(0, powerflow.setup.nbus):
            for idy in range(0, powerflow.setup.nbus):
                if (idx is idy):
                    # Elemento Hkk
                    powerflow.setup.pt[idx, idy] += (-powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.ybus[idx][idy].imag - PQCalc().qcalc(powerflow, idx,)

                    # Elemento Nkk
                    powerflow.setup.pv[idx, idy] += (PQCalc().pcalc(powerflow, idx,) + powerflow.sol['voltage'][idx] ** 2 * powerflow.setup.ybus[idx][idy].real) / powerflow.sol['voltage'][idx]

                    # Elemento Mkk
                    powerflow.setup.qt[idx, idy] += PQCalc().pcalc(powerflow, idx,) - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.ybus[idx][idy].real

                    # Elemento Lkk
                    powerflow.setup.qv[idx, idy] += (PQCalc().qcalc(powerflow, idx,) - powerflow.sol['voltage'][idx] ** 2 * powerflow.setup.ybus[idx][idy].imag) / powerflow.sol['voltage'][idx]
                
                else:
                    # Elemento Hkm
                    powerflow.setup.pt[idx, idy] += powerflow.sol['voltage'][idx] * powerflow.sol['voltage'][idy] * (powerflow.setup.ybus[idx][idy].real * sin(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]) - powerflow.setup.ybus[idx][idy].imag * cos(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]))

                    # Elemento Nkm
                    powerflow.setup.pv[idx, idy] += powerflow.sol['voltage'][idx] * (powerflow.setup.ybus[idx][idy].real * cos(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]) + powerflow.setup.ybus[idx][idy].imag * sin(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]))

                    # Elemento Mkm
                    powerflow.setup.qt[idx, idy] -= powerflow.sol['voltage'][idx] * powerflow.sol['voltage'][idy] * (powerflow.setup.ybus[idx][idy].real * cos(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]) + powerflow.setup.ybus[idx][idy].imag * sin(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]))

                    # Elemento Lkm
                    powerflow.setup.qv[idx, idy] += powerflow.sol['voltage'][idx] * (powerflow.setup.ybus[idx][idy].real * sin(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]) - powerflow.setup.ybus[idx][idy].imag * cos(powerflow.sol['theta'][idx] - powerflow.sol['theta'][idy]))

        # Montagem da Matriz Jacobiana
        self.assembly(powerflow,)
        
        # Submatrizes de controles ativos
        if (powerflow.setup.controlcount > 0):
            Control(powerflow, powerflow.setup,).controljac(powerflow,)

        # Condição
        if (powerflow.method != 'CPF'):
            # Armazenamento da Matriz Jacobiana
            Folder(powerflow.setup,).jacobi(powerflow.setup,)
            self.savejacobi(powerflow,)


    
    def assembly(
        self,
        powerflow,
    ):
        """montagem da matriz Jacobiana
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Tratamento de big-number
        if ('FREQ' not in powerflow.setup.control) or (not powerflow.setup.control['FREQ']):
            self.bignumber(powerflow,)

        # Montagem da matriz Jacobiana
        # configuração completa
        powerflow.setup.jacob = concatenate((concatenate((powerflow.setup.pt, powerflow.setup.qt), axis=0), concatenate((powerflow.setup.pv, powerflow.setup.qv), axis=0)), axis=1)



    def bignumber(
        self,
        powerflow,
    ):
        """
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização Método Big-Number
        for idx in range(0, powerflow.setup.nbus):
            if (powerflow.setup.maskP[idx] == False):
                powerflow.setup.pt[idx, :] = 0
                powerflow.setup.pv[idx, :] = 0
                powerflow.setup.pt[:, idx] = 0
                powerflow.setup.qt[:, idx] = 0
                powerflow.setup.pt[idx, idx] = 1
            
            if (powerflow.setup.maskQ[idx] == False) and (('QLIM' not in powerflow.setup.control) or ('QLIMs' not in powerflow.setup.control)):
                powerflow.setup.qv[idx, :] = 0
                powerflow.setup.qt[idx, :] = 0
                powerflow.setup.qv[:, idx] = 0
                powerflow.setup.pv[:, idx] = 0
                powerflow.setup.qv[idx, idx] = 1



    def savejacobi(
        self,
        powerflow,
    ):
        """armazena a matriz jacobiana a cada iteração
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Cabeçalho
        header = 'vv Sistema ' + powerflow.setup.name + ' vv Matriz Jacobiana vv Formulação Completa vv Iteração ' + str(powerflow.sol['iter']) + ' vv'

        # Arquivo
        file = powerflow.setup.dirRjacobi + powerflow.setup.name + '-jacobi.csv'

        # Check
        if (exists(file) is False):
            open(file, 'a').close()
        elif (True and powerflow.sol['iter'] == 0):
            remove(file)
            open(file, 'a').close()
        
        # Atualização
        with open(file, 'a') as of:
            savetxt(of, powerflow.setup.jacob, delimiter=',', header=header)
            of.close()