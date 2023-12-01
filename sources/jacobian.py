# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, cos, savetxt, sin, zeros
from os.path import exists
from os import remove
from scipy.sparse import csc_matrix

from calc import PQCalc
from ctrl import Control
from folder import Folder

class Jacobi:
    """classe para construção da matriz Jacobiana"""

    def jacobi(
        self,
        powerflow,
    ):
        """cálculo das submatrizes da matriz Jacobiana
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        nnz = int(powerflow.setup.apont[-1])
        data = zeros([4 * nnz], dtype=float)
        indx = zeros([4 * nnz], dtype=int)
        indp = concatenate((deepcopy(powerflow.setup.apont), zeros(powerflow.setup.nbus, dtype=int)))
        
        for idx, value in powerflow.setup.dlinhaDF.iterrows():
            if value['estado']:
                de = value['de'] - 1
                para = value['para'] - 1

                # elementos de,para
                h1 = powerflow.sol['voltage'][de] * powerflow.sol['voltage'][para] * (- powerflow.setup.admitancia[idx].real * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                n1 = - powerflow.sol['voltage'][de] * (powerflow.setup.admitancia[idx].real * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                m1 = powerflow.sol['voltage'][de] * powerflow.sol['voltage'][para] * (powerflow.setup.admitancia[idx].real * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                l1 = powerflow.sol['voltage'][de] * (- powerflow.setup.admitancia[idx].real * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))

                # elementos para,de
                h2 = powerflow.sol['voltage'][para] * powerflow.sol['voltage'][de] * (powerflow.setup.admitancia[idx].real * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                n2 = powerflow.sol['voltage'][para] * (- powerflow.setup.admitancia[idx].real * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                m2 = powerflow.sol['voltage'][para] * powerflow.sol['voltage'][de] * (powerflow.setup.admitancia[idx].real * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) - powerflow.setup.admitancia[idx].imag * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))
                l2 = powerflow.sol['voltage'][para] * (powerflow.setup.admitancia[idx].real * sin(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]) + powerflow.setup.admitancia[idx].imag * cos(powerflow.sol['theta'][de] - powerflow.sol['theta'][para]))

                # preenchimento vetores de,para
                if para == 0:
                    aux_h1 = int(indp[para] - 1)
                    aux_n1 = int(indp[para] - 1) + 2 * nnz
                    aux_m1 = int(indp[para] - 1) + int(powerflow.setup.apont[para])
                    aux_l1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.setup.apont[para])
                else:
                    aux_h1 = int(indp[para] - 1) + int(powerflow.setup.apont[para - 1])
                    aux_n1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.setup.apont[para - 1])
                    aux_m1 = int(indp[para] - 1) + int(powerflow.setup.apont[para])
                    aux_l1 = int(indp[para] - 1) + 2 * nnz + int(powerflow.setup.apont[para])
                data[aux_h1]  = h1                         # Submatriz H
                data[aux_n1]  = n1                         # Submatriz N
                data[aux_m1]  = m1                         # Submatriz M
                data[aux_l1]  = l1                         # Submatriz L
                indx[aux_h1]  = de                         # Submatriz H
                indx[aux_n1]  = de                         # Submatriz N
                indx[aux_m1]  = de + powerflow.setup.nbus  # Submatriz M
                indx[aux_l1]  = de + powerflow.setup.nbus  # Submatriz L
                indp[para]   += -1

                # Preencher vetores de construção com elementos da posição [para, de]
                if de == 0:
                    aux_h2 = int(indp[de] - 1)
                    aux_n2 = int(indp[de] - 1) + 2 * nnz
                    aux_m2 = int(indp[de] - 1) + int(powerflow.setup.apont[de])
                    aux_l2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.setup.apont[de])
                else:
                    aux_h2 = int(indp[de] - 1) + int(powerflow.setup.apont[de - 1])
                    aux_n2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.setup.apont[de - 1])
                    aux_m2 = int(indp[de] - 1) + int(powerflow.setup.apont[de])
                    aux_l2 = int(indp[de] - 1) + 2 * nnz + int(powerflow.setup.apont[de])
                data[aux_h2]  = h2                           # Submatriz H
                data[aux_n2]  = n2                           # Submatriz N
                data[aux_m2]  = m2                           # Submatriz M
                data[aux_l2]  = l2                           # Submatriz L
                indx[aux_h2]  = para                         # Submatriz H
                indx[aux_n2]  = para                         # Submatriz N
                indx[aux_m2]  = para + powerflow.setup.nbus  # Submatriz M
                indx[aux_l2]  = para + powerflow.setup.nbus  # Submatriz L
                indp[de]     += -1

        # Elementos da diagonal principal da matriz jacobiana
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Submatriz H
            if (powerflow.setup.maskP[idx] == False): # A presença do módulo se deve ao tratamento de limites (QLIM), que pode converter barra tipo 2 em -2
                hk = 1E20
                # if 'FREQ' in comandos.exec and k not in freq.nrefrp:
                #     hk = - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.bdiag[idx] - PQCalc().qcalc(powerflow=powerflow, idx=idx)
                                                        
            else:
                hk = - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.bdiag[idx] - PQCalc().qcalc(powerflow=powerflow, idx=idx)

            # Submatriz N
            nk = (PQCalc().pcalc(powerflow=powerflow, idx=idx) + (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.gdiag[idx]) / powerflow.sol['voltage'][idx]

            # Submatriz M
            mk = - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.gdiag[idx] + PQCalc().qcalc(powerflow=powerflow, idx=idx)

            # Submatriz L
            if (powerflow.setup.maskQ[idx] == False) and (('QLIM' not in powerflow.setup.control) or ('QLIMs' not in powerflow.setup.control) or ('QLIMn' not in powerflow.setup.control)):
                lk = 1E20
            else:
                lk = (PQCalc().qcalc(powerflow=powerflow, idx=idx) - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.bdiag[idx]) / powerflow.sol['voltage'][idx]

            # # Verificar se o controle remoto de tensão está ativo
            # if 'CREM' in comandos.exec:
            #     # if barra.ntype[k] == 1 and gerador.busgr[k] in gerador.icb:
            #     if barra.ntype[k] > 0 and gerador.busgr[k] in gerador.icb:
            #         lk = (qcalc[k] - (powerflow.sol['voltage'][idx] ** 2) * powerflow.setup.bdiag[k]) / powerflow.sol['voltage'][idx]

            # Preencher vetor  de construção com elementos da posição [k, k]
            if idx == 0:
                aux_h = int(indp[idx] - 1)
                aux_n = int(indp[idx] - 1) + 2 * nnz
                aux_m = int(indp[idx] - 1) + int(powerflow.setup.apont[idx])
                aux_l = int(indp[idx] - 1) + 2 * nnz + int(powerflow.setup.apont[idx])
            else:
                aux_h = int(indp[idx] - 1) + int(powerflow.setup.apont[idx - 1])
                aux_n = int(indp[idx] - 1) + 2 * nnz + int(powerflow.setup.apont[idx - 1])
                aux_m = int(indp[idx] - 1) + int(powerflow.setup.apont[idx])
                aux_l = int(indp[idx] - 1) + 2 * nnz + int(powerflow.setup.apont[idx])
            data[aux_h]  = hk              # Submatriz H
            data[aux_n]  = nk              # Submatriz N
            data[aux_m]  = mk              # Submatriz M
            data[aux_l]  = lk              # Submatriz L
            indx[aux_h]  = idx               # Submatriz H
            indx[aux_n]  = idx               # Submatriz N
            indx[aux_m]  = idx + powerflow.setup.nbus  # Submatriz M
            indx[aux_l]  = idx + powerflow.setup.nbus  # Submatriz L
            indp[idx]   += -1

            # Atualizar vetor "indprt" para estrutura final
            indp[idx]      = 2 * indp[idx]
            indp[idx + powerflow.setup.nbus] = 2 * nnz + indp[idx]

        # Adicionar comprimento do vetor "incices" como último elemento do vetor "indprt"
        indp = append(indp, len(indx))

        # Criação da jacobiana como matriz CSC
        powerflow.setup.jacob = csc_matrix((data, indx, indp), shape=(2 * powerflow.setup.nbus, 2 * powerflow.setup.nbus))

        
        # # Montagem da Matriz Jacobiana
        # self.assembly(powerflow,)
        
        # Submatrizes de controles ativos
        if (powerflow.setup.controlcount > 0):
            Control(powerflow, powerflow.setup,).controljac(powerflow,)

        # # Condição
        # if (powerflow.method != 'CPF'):
        #     # Armazenamento da Matriz Jacobiana
        #     Folder(powerflow.setup,).jacobi(powerflow.setup,)
        #     self.savejacobi(powerflow,)


    
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
            
            if (powerflow.setup.maskQ[idx] == False) and (('QLIM' not in powerflow.setup.control) or ('QLIMs' not in powerflow.setup.control) or ('QLIMn' not in powerflow.setup.control)):
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