# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, cos, sin, zeros

class Qlim:
    """classe para tratamento de limites de geração de potência reativa"""
    
    def qlimres(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações de controle adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Vetor de resíduos
        powerflow.setup.deltaQlim = zeros([powerflow.setup.nger])

        # Contador
        nger = 0

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
                # Modificação do resíduo de potência reativa
                powerflow.setup.deltaQ[idx] = powerflow.setup.pqsch['potencia_reativa_especificada'][idx]
                powerflow.setup.deltaQ[idx] -= self.qcalc(powerflow, idx,)

                # Tratamento de limites em barras PV
                if (value['tipo'] == 1):
                    if (value['potencia_reativa'] < value['potencia_reativa_maxima']) and (value['potencia_reativa'] > value['potencia_reativa_minima']):
                        # Tratamento de limite de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['sbase']
                
                    elif (value['potencia_reativa'] >= value['potencia_reativa_maxima']):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= value['potencia_reativa']
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = -1
                    
                    elif (value['potencia_reativa'] <= value['potencia_reativa_minima']):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= value['potencia_reativa']
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = -1

                # Tratamento de limites em barras PQV
                elif (value['tipo'] == -1):
                    # Modificação do resíduo de potência ativa
                    powerflow.setup.deltaP[idx] = powerflow.setup.pqsch['potencia_ativa_especificada'][idx]
                    powerflow.setup.deltaP[idx] -= self.pcalc(powerflow, idx,)

                    if ((value['potencia_reativa'] >= value['potencia_reativa_maxima']) and (powerflow.sol['voltage'][idx] > value['tensao'] * (1E-3)))\
                        or ((value['potencia_reativa'] <= value['potencia_reativa_minima']) and (powerflow.sol['voltage'][idx] < value['tensao'] * (1E-3))):
                        # Tratamento de limite de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['sbase']
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = 1
                
                    elif (value['potencia_reativa'] >= value['potencia_reativa_maxima']):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= value['potencia_reativa']
                    
                    elif (value['potencia_reativa'] <= value['potencia_reativa_minima']):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= value['potencia_reativa']
                
                # Incrementa contador
                nger += 1
        
        # Resíduo de equação de controle
        powerflow.setup.deltaQlim /= powerflow.setup.options['sbase']
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaQlim)



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



    def qlimsubjac(
        self,
        powerflow,
    ):
        """submatrizes da matriz jacobiana
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # 
        # jacobiana:
        # 
        #   H     N   pxx   
        #   M     L   qxx   
        # yxt   yxv   yxx   
        # 

        # Dimensão da matriz Jacobiana
        powerflow.setup.dimpreqlim = deepcopy(powerflow.setup.jacob.shape[0])
            
        # Submatrizes
        powerflow.setup.pxx = zeros([powerflow.setup.nbus, powerflow.setup.nger])        
        powerflow.setup.qxx = zeros([powerflow.setup.nbus, powerflow.setup.nger])
        powerflow.setup.yxx = zeros([powerflow.setup.nger, powerflow.setup.nger])
        powerflow.setup.yxt = zeros([powerflow.setup.nger, powerflow.setup.nbus])
        powerflow.setup.yxv = zeros([powerflow.setup.nger, powerflow.setup.nbus])

        # Contador
        nger = 0

        # Submatrizes PXP QXP YQV YXT
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
                # dQg/dx
                powerflow.setup.qxx[idx, nger] = -1

                # Barras PV
                if value['tipo'] != -1:
                    powerflow.setup.yxv[nger, idx] = 1

                # Barras PQV
                elif value['tipo'] == -1:
                    powerflow.setup.yxx[nger, nger] = 1

                # Incrementa contador
                nger += 1


        ## Montagem Jacobiana
        # Condição
        if powerflow.setup.controldim != 0:
            powerflow.setup.extrarow = zeros([powerflow.setup.nger, powerflow.setup.controldim])
            powerflow.setup.extracol = zeros([powerflow.setup.controldim, powerflow.setup.nger])

            # H-N M-L + yxt-yxv
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.yxt, powerflow.setup.yxv, powerflow.setup.extrarow), axis=1)), axis=0)

            # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.extracol, powerflow.setup.yxx), axis=0)), axis=1)

        elif powerflow.setup.controldim == 0:
            # H-N M-L + yxt-yxv
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.yxt, powerflow.setup.yxv), axis=1)), axis=0)

            # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.yxx), axis=0)), axis=1)



    def qlimupdt(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Contador
        nger = 0

        # Atualização da potência reativa gerada
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
                powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa'] = value['potencia_reativa'] + powerflow.setup.statevar[(powerflow.setup.dimpreqlim + nger)] * powerflow.setup.options['sbase']

                # Atualização da potência reativa especificada
                powerflow.setup.pqsch['potencia_reativa_especificada'][idx] = powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa']
                powerflow.setup.pqsch['potencia_reativa_especificada'][idx] -= value['demanda_reativa']

                # Incrementa contador
                nger += 1
        
        powerflow.setup.pqsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']