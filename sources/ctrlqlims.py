# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, ones, zeros

from smooth import Smooth

class Qlims:
    """classe para tratamento de limites de geração de potência reativa"""

    def qlimssol(
        self,
        powerflow,
    ):
        """variável de estado adicional para o problema de fluxo de potência
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variáveis
        if 'reactive_generation' not in powerflow.sol:
            powerflow.sol['reactive_generation'] = zeros([powerflow.setup.nbus])
            powerflow.setup.maskQ = ones(powerflow.setup.nbus, dtype=bool)
                

    
    def qlimsres(
        self,
        powerflow,
        case,
    ):
        """cálculo de resíduos das equações de controle adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        # Vetor de resíduos
        powerflow.setup.deltaQlim = zeros([powerflow.setup.nger])

        # Contador
        nger = 0

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
                Smooth(powerflow,).qlimssmooth(idx, powerflow, nger, case,)
                
                # Incrementa contador
                nger += 1
        
        # Resíduo de equação de controle
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaQlim)



    def qlimssubjac(
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
            if (value['tipo'] != 0):
                # dQg/dx
                powerflow.setup.qxx[idx, nger] = -1

                # Barras PV
                powerflow.setup.yxv[nger, idx] = powerflow.setup.diffqlim[idx][0]
                # powerflow.setup.yxx[nger, nger] = 1E-10

                # Barras PQV
                if (powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_maxima'] - powerflow.setup.tolqlimq) or \
                    (powerflow.sol['reactive_generation'][idx] < value['potencia_reativa_minima'] + powerflow.setup.tolqlimq):
                    powerflow.setup.yxx[nger, nger] = powerflow.setup.diffqlim[idx][1]

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



    def qlimsupdt(
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
                powerflow.sol['reactive_generation'][idx] += powerflow.setup.statevar[(powerflow.setup.dimpreqlim + nger)] * powerflow.setup.options['sbase']

                # Incrementa contador
                nger += 1

        self.qlimssch(powerflow,)


    
    def qlimssch(
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
        powerflow.setup.pqsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']



    def qlimscorr(
        self,
        powerflow,
        case,
    ):
        """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: etapa do fluxo de potência continuado analisada
        """

        ## Inicialização
        # Variável
        powerflow.sol['reactive_generation'] = deepcopy(powerflow.case[case]['prev']['reactive_generation'])



    def qlimsheur(
        self,
        powerflow,
    ):
        """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização 
        # Condição de geração de potência reativa ser superior ao valor máximo - analisa apenas para as barras de geração
        # powerflow.setup.dbarraDF['potencia_reativa_maxima'].to_numpy()
        if any((powerflow.sol['reactive_generation'] > powerflow.setup.dbarraDF['potencia_reativa_maxima'].to_numpy() - powerflow.setup.tolqlimq), where=~powerflow.setup.mask[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]):
            powerflow.setup.controlheur = True

        # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB 
        if (not powerflow.cpfsol['pmc']) and (powerflow.cpfsol['varstep'] == 'lambda') and ((powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])) <= powerflow.setup.options['icmn']):
            powerflow.setup.bifurcation = True
            # Condição de curva completa do fluxo de potência continuado
            if (powerflow.setup.options['full']):
                powerflow.setup.dbarraDF['true_potencia_reativa_minima'] = powerflow.setup.dbarraDF.loc[:, 'potencia_reativa_minima']
                for idx, value in powerflow.setup.dbarraDF.iterrows():
                    if (powerflow.sol['reactive_generation'][idx] > value['potencia_reativa_maxima']) and (value['tipo'] != 0):
                        powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa_minima'] = deepcopy(value['potencia_reativa_maxima'])

    

    def qlimspop(
        self,
        powerflow,
        pop: int=1,
    ):
        """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
                atua diretamente na variável de controle associada à opção de controle QLIMs

        Parâmetros
            powerflow: self do arquivo powerflow.py
            pop: quantidade de ações necessárias
        """

        ## Inicialização
        Smooth(powerflow,).qlimspop(powerflow, pop=pop,)