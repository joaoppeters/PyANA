# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, ones, zeros
from scipy.sparse import csc_matrix, hstack, vstack

class Qlim:
    """classe para tratamento de limites de geração de potência reativa"""

    def qlimsol(
        self,
        powerflow,
    ):
        """variável de estado adicional para o problema de fluxo de potência
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variáveis
        if ('reactive_generation' not in powerflow.sol):
            powerflow.sol['reactive_generation'] = zeros([powerflow.setup.nbus])
            powerflow.setup.maskQ = ones(powerflow.setup.nbus, dtype=bool)
            powerflow.setup.slackqlim = False
                

    
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
            if (value['tipo'] != 0):
                # Tratamento de limites em barras PV
                if (value['tipo'] == 1):
                    if (powerflow.sol['reactive_generation'][idx] < value['potencia_reativa_maxima']) and (powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_minima']):
                        # Tratamento de limite de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['BASE']
                
                    elif (powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = -1
                    
                    elif (powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = -1

                # Tratamento de backoff em barras PQV
                elif (value['tipo'] == -1):
                    if ((powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']) and (powerflow.sol['voltage'][idx] > value['tensao'] * (1E-3))) or ((powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']) and (powerflow.sol['voltage'][idx] < value['tensao'] * (1E-3))):
                        # Tratamento de backoff de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['BASE']
                        powerflow.setup.dbarraDF.loc[idx, 'tipo'] = 1
                    
                    elif (powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']) and (powerflow.sol['voltage'][idx] <= value['tensao'] * (1E-3)):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                    
                    elif (powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']) and (powerflow.sol['voltage'][idx] >= value['tensao'] * (1E-3)):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]

                # Tratamento de limites de barra SLACK
                elif (value['tipo'] == 2) and (not powerflow.setup.slackqlim):
                    if (powerflow.sol['reactive_generation'][idx] < value['potencia_reativa_maxima']) and (powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_minima']):
                        # Tratamento de limite de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['BASE']
                
                    elif (powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                        powerflow.setup.slackqlim = True
                    
                    elif (powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                        powerflow.setup.slackqlim = True
                    
                # Tratamento de backoff de barra SLACK
                elif (value['tipo'] == 2) and (powerflow.setup.slackqlim):
                    if ((powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']) and (powerflow.sol['voltage'][idx] > value['tensao'] * (1E-3))) or ((powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']) and (powerflow.sol['voltage'][idx] < value['tensao'] * (1E-3))):
                        # Tratamento de backoff de magnitude de tensão
                        powerflow.setup.deltaQlim[nger] += value['tensao'] * (1E-3)
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['voltage'][idx]
                        powerflow.setup.deltaQlim[nger] *= powerflow.setup.options['BASE']
                        powerflow.setup.slackqlim = False
                    
                    elif (powerflow.sol['reactive_generation'][idx] >= value['potencia_reativa_maxima']) and (powerflow.sol['voltage'][idx] <= value['tensao'] * (1E-3)):
                        # Tratamento de limite de potência reativa gerada máxima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_maxima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]
                    
                    elif (powerflow.sol['reactive_generation'][idx] <= value['potencia_reativa_minima']) and (powerflow.sol['voltage'][idx] >= value['tensao'] * (1E-3)):
                        # Tratamento de limite de potência reativa gerada mínima
                        powerflow.setup.deltaQlim[nger] += value['potencia_reativa_minima']
                        powerflow.setup.deltaQlim[nger] -= powerflow.sol['reactive_generation'][idx]

                
                # Incrementa contador
                nger += 1
        
        # Resíduo de equação de controle
        powerflow.setup.deltaQlim /= powerflow.setup.options['BASE']
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaQlim)



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
        #   H     N   px   
        #   M     L   qx   
        #  yt    yv   yx   
        # 

        # Dimensão da matriz Jacobiana
        powerflow.setup.dimpreqlim = deepcopy(powerflow.setup.jacob.shape[0])
            
        # Submatrizes
        powerflow.setup.px = zeros([powerflow.setup.nbus, powerflow.setup.nger])        
        powerflow.setup.qx = zeros([powerflow.setup.nbus, powerflow.setup.nger])
        powerflow.setup.yx = zeros([powerflow.setup.nger, powerflow.setup.nger])
        powerflow.setup.yt = zeros([powerflow.setup.nger, powerflow.setup.nbus])
        powerflow.setup.yv = zeros([powerflow.setup.nger, powerflow.setup.nbus])

        # Contador
        nger = 0

        # Submatrizes QX YV YX
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if (value['tipo'] != 0):
                # dQg/dx
                powerflow.setup.qx[idx, nger] = -1

                powerflow.setup.yx[nger, nger] = 1E-10

                # Barras PV
                if (value['tipo'] == 1) or ((value['tipo'] == 2) and (not powerflow.setup.slackqlim)):
                    powerflow.setup.yv[nger, idx] = 1

                # Barras PQV
                elif (value['tipo'] == -1) or ((value['tipo'] == 2) and (powerflow.setup.slackqlim)):
                    powerflow.setup.yx[nger, nger] = 1

                # Incrementa contador
                nger += 1

        ## Montagem Jacobiana
        # Condição
        if (powerflow.setup.controldim != 0):
            powerflow.setup.extrarow = zeros([powerflow.setup.nger, powerflow.setup.controldim])
            powerflow.setup.extracol = zeros([powerflow.setup.controldim, powerflow.setup.nger])

            ytv = csc_matrix(concatenate((powerflow.setup.yt, powerflow.setup.yv, powerflow.setup.extrarow), axis=1))
            pqyx = csc_matrix(concatenate((powerflow.setup.px, powerflow.setup.qx, powerflow.setup.extracol, powerflow.setup.yx), axis=0))

        elif (powerflow.setup.controldim == 0):
            ytv = csc_matrix(concatenate((powerflow.setup.yt, powerflow.setup.yv), axis=1))
            pqyx = csc_matrix(concatenate((powerflow.setup.px, powerflow.setup.qx, powerflow.setup.yx), axis=0))

        powerflow.setup.jacob = vstack([powerflow.setup.jacob, ytv], format='csc')
        powerflow.setup.jacob = hstack([powerflow.setup.jacob, pqyx], format='csc')



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
            if (value['tipo'] != 0):
                powerflow.sol['reactive_generation'][idx] += powerflow.setup.statevar[(powerflow.setup.dimpreqlim + nger)] * powerflow.setup.options['BASE']

                if (value['tipo'] == 1) and ((powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_maxima']) or (powerflow.sol['reactive_generation'][idx] < value['potencia_reativa_minima'])):
                    powerflow.setup.dbarraDF.loc[idx, 'tipo'] = -1

                if (value['tipo'] == 2) and ((powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_maxima']) or (powerflow.sol['reactive_generation'][idx] < value['potencia_reativa_minima'])):
                    powerflow.setup.slackqlim = True

                # Incrementa contador
                nger += 1
        
        self.qlimsch(powerflow,)


    
    def qlimsch(
        self,
        powerflow,
    ):
        """atualização do valor de potência reativa especificada
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variável
        powerflow.setup.pqsch['potencia_reativa_especificada'] = zeros([powerflow.setup.nbus])

        # Atualização da potência reativa especificada
        powerflow.setup.pqsch['potencia_reativa_especificada'] += powerflow.sol['reactive_generation']
        powerflow.setup.pqsch['potencia_reativa_especificada'] -= powerflow.setup.dbarraDF['demanda_reativa'].to_numpy()
        powerflow.setup.pqsch['potencia_reativa_especificada'] /= powerflow.setup.options['BASE']



    def qlimcorr(
        self,
        powerflow,
        case,
    ):
        """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        powerflow.sol['reactive_generation'] = deepcopy(powerflow.case[case]['prev']['reactive_generation'])



    def qlimheur(
        self,
        powerflow,
    ):
        """
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização 
        # Condição de geração de potência reativa ser superior ao valor máximo
        if any((powerflow.sol['reactive_generation'] > powerflow.setup.dbarraDF['potencia_reativa_maxima'].to_numpy()), where=~powerflow.setup.mask[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]):
            powerflow.setup.controlheur = True

        # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB 
        if (not powerflow.cpfsol['pmc']) and (powerflow.cpfsol['varstep'] == 'lambda') and ((powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])) <= powerflow.setup.options['ICMN']):
            powerflow.setup.bifurcation = True
            # Condição de curva completa do fluxo de potência continuado
            if (powerflow.setup.options['FULL']):
                powerflow.setup.dbarraDF['true_potencia_reativa_minima'] = powerflow.setup.dbarraDF.loc[:, 'potencia_reativa_minima']
                for idx, value in powerflow.setup.dbarraDF.iterrows():
                    if (powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_maxima']):
                        powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa_minima'] = deepcopy(value['potencia_reativa_maxima'])