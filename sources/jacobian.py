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

        for idx in range(powerflow.setup.nbus):
            for idy in range(powerflow.setup.nbus):
                if idx is idy:
                    # Elemento Hkk
                    powerflow.setup.pt[idx, idy] += (-powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.ybus[idx][idy].imag - self.qcalc(powerflow, idx,)

                    # Elemento Nkk
                    powerflow.setup.pv[idx, idy] += (self.pcalc(powerflow, idx,) + powerflow.sol['voltage'][idx] ** 2 * powerflow.setup.ybus[idx][idy].real) / powerflow.sol['voltage'][idx]

                    # Elemento Mkk
                    powerflow.setup.qt[idx, idy] += self.pcalc(powerflow, idx,) - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.ybus[idx][idy].real

                    # Elemento Lkk
                    powerflow.setup.qv[idx, idy] += (self.qcalc(powerflow, idx,) - powerflow.sol['voltage'][idx] ** 2 * powerflow.setup.ybus[idx][idy].imag) / powerflow.sol['voltage'][idx]
                
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
        if powerflow.setup.ctrlcount > 0:
            Control(powerflow, powerflow.setup,).controljac(powerflow,)

        # Armazenamento da Matriz Jacobiana
        Folder(powerflow.setup,).jacobi(powerflow.setup,)
        self.savejacobi(powerflow,)
        


    def pcalc(
        self,
        powerflow,
        idx: int=None,
    ):
        """cálculo da potência ativa de cada barra
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            idx: int, obrigatório, valor padrão None
                referencia o índice da barra a qual vai ser calculada a potência ativa

        Retorno
            p: float
                potência ativa calculada para o barramento `idx`
        """
        
        ## Inicialização
        # Variável de potência ativa calculada para o barramento `idx`
        p = 0

        for bus in range(0, powerflow.setup.nbus):
            p += powerflow.sol['voltage'][bus] * (powerflow.setup.ybus[idx][bus].real * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) + powerflow.setup.ybus[idx][bus].imag * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        p *= powerflow.sol['voltage'][idx]

        # Armazenamento da potência ativa gerada equivalente do barramento
        powerflow.sol['active'][idx] = (p * powerflow.setup.options['sbase']) + powerflow.setup.dbarraDF['demanda_ativa'][idx]

        return p



    def qcalc(
        self,
        powerflow,
        idx: int=None,
    ):
        """cálculo da potência reativa de cada barra
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            idx: int, obrigatório, valor padrão None
                referencia o índice da barra a qual vai ser calculada a potência reativa

        Retorno
            q: float
                potência reativa calculada para o barramento `idx`
        """
        
        ## Inicialização
        # Variável de potência reativa calculada para o barramento `idx`
        q = 0

        for bus in range(0, powerflow.setup.nbus):
            q += powerflow.sol['voltage'][bus] * (powerflow.setup.ybus[idx][bus].real * sin(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]) - powerflow.setup.ybus[idx][bus].imag * cos(powerflow.sol['theta'][idx]-powerflow.sol['theta'][bus]))

        q *= powerflow.sol['voltage'][idx]

        # Armazenamento da potência ativa gerada equivalente do barramento
        powerflow.sol['reactive'][idx] = (q * powerflow.setup.options['sbase']) + powerflow.setup.dbarraDF['demanda_reativa'][idx]

        return q


    
    def assembly(
        self,
        powerflow,
    ):
        """montagem da matriz Jacobiana
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Tratamento de limite de geração de potência reativa & big-number
        if not powerflow.control:
            self.bignumber(powerflow,)

        # Montagem da matriz Jacobiana
        # configuração completa
        if powerflow.jacobi == 'COMPLETA':
            powerflow.setup.jacob = concatenate((concatenate((powerflow.setup.pt, powerflow.setup.qt), axis=0), concatenate((powerflow.setup.pv, powerflow.setup.qv), axis=0)), axis=1)
        # configuração alternada
        elif powerflow.jacobi == 'ALTERNADA':
            powerflow.setup.jacob: ndarray = zeros(shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype='float')
            for row in range(0, powerflow.setup.nbus):
                ptpv = -1
                qtqv = -1
                for col in range(0, powerflow.setup.nbus):
                    if row % 2 == 0:
                        if col % 2 == 0:
                            ptpv += 1
                            powerflow.setup.jacob[row, col] = deepcopy(powerflow.setup.pt[row, ptpv])
                        else:
                            powerflow.setup.jacob[row, col] = deepcopy(powerflow.setup.pv[row, ptpv])
                    else:
                        if col % 2 == 0:
                            qtqv += 1
                            powerflow.setup.jacob[row, col] = deepcopy(powerflow.setup.qt[row, qtqv])
                        else:
                            powerflow.setup.jacob[row, col] = deepcopy(powerflow.setup.qv[row, qtqv])
        # configuração reduzida
        elif powerflow.jacobi == 'REDUZIDA':
            powerflow.setup.jacob = concatenate((concatenate((powerflow.setup.pt, powerflow.setup.qt), axis=0), concatenate((powerflow.setup.pv, powerflow.setup.qv), axis=0)), axis=1)
            powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask]
            


    def bignumber(
        self,
        powerflow,
    ):
        """
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização Método Big-Number
        # Mask H & M
        powerflow.setup.BNP = ones(powerflow.setup.nbus) 
        # Mask N & L
        powerflow.setup.BNQ = ones(powerflow.setup.nbus)
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if (value['tipo'] == 2) or (value['tipo'] == 1):
                powerflow.setup.BNQ[idx] = 0
                if (value['tipo'] == 2):
                    powerflow.setup.BNP[idx] = 0 

        for v in range(0, powerflow.setup.nbus):
            if powerflow.setup.BNP[v] == 0:
                powerflow.setup.pt[v, :] = 0
                powerflow.setup.pv[v, :] = 0
                powerflow.setup.pt[:, v] = 0
                powerflow.setup.qt[:, v] = 0
                powerflow.setup.pt[v, v] = 1
            
            if powerflow.setup.BNQ[v] == 0:
                powerflow.setup.qv[v, :] = 0
                powerflow.setup.qt[v, :] = 0
                powerflow.setup.qv[:, v] = 0
                powerflow.setup.pv[:, v] = 0
                powerflow.setup.qv[v, v] = 1



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
        header = 'vv Sistema ' + powerflow.setup.name + ' vv Matriz Jacobiana vv Formulação ' + powerflow.jacobi + ' vv Iteração ' + str(powerflow.sol['iter']) + ' vv'

        # Arquivo
        file = powerflow.setup.dirRjacobi + powerflow.setup.name + '-jacobi.csv'

        # Check
        if exists(file) is False:
            open(file, 'a').close()
        elif True and powerflow.sol['iter'] == 0:
            remove(file)
            open(file, 'a').close()
        
        # Atualização
        with open(file, 'a') as of:
            savetxt(of, powerflow.setup.jacob, delimiter=',', header=header)
            of.close()