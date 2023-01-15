# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import any, append, concatenate, isreal, pi, roots, zeros
from sympy import Symbol
from sympy.functions import sin

from calc import PQCalc
from smooth import Smooth

class SVC:
    """classe para tratamento de compensadores estáticos de potência reativa"""

    def svcsol(
        self,
        powerflow,
    ):
        """variável de estado adicional para o problema de fluxo de potência
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variáveis
        if 'svc_reactive_generation' not in powerflow.sol:
            powerflow.sol['svc_reactive_generation'] = powerflow.setup.dcerDF['potencia_reativa'].to_numpy()
            if powerflow.setup.dcerDF['controle'][0] == 'A':
                self.alpha(powerflow,)



    def alpha(
        self,
        powerflow,
    ):
        """calculo dos parametros para metodologia alpha do compensador estatico de potencia reativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        powerflow.setup.alphaxc = (powerflow.setup.options['sbase']) / (powerflow.setup.dcerDF['potencia_reativa_maxima'][0])
        powerflow.setup.alphaxl = ((powerflow.setup.options['sbase']) / (powerflow.setup.dcerDF['potencia_reativa_maxima'][0])) / (1 - (powerflow.setup.dcerDF['potencia_reativa_minima'][0]) / (powerflow.setup.dcerDF['potencia_reativa_maxima'][0]))
        powerflow.setup.alpha = roots([(8 / 1856156927625), 0, (-4 / 10854718875), 0, (16 / 638512875), 0, (-8 / 6081075), 0, (8 / 155925), 0, (-4 / 2835), 0, (8 / 315), 0, (-4 / 15), 0, (4 / 3), 0, 0, -(2 * pi) + ((powerflow.setup.alphaxl * pi) / powerflow.setup.alphaxc),])
        powerflow.setup.alpha = powerflow.setup.alpha[isreal(powerflow.setup.alpha)][0].real

        # Variáveis Simbólicas
        powerflow.setup.alphasym = Symbol('alpha')
        powerflow.setup.alphabeq = -(((powerflow.setup.alphaxc) / (pi)) * (2 * (pi - powerflow.setup.alphasym) + sin(2 * powerflow.setup.alphasym)) - powerflow.setup.alphaxl) / (powerflow.setup.alphaxc * powerflow.setup.alphaxl)

        # Potência Reativa
        idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == powerflow.setup.dcerDF['barra']].tolist()[0]
        powerflow.sol['svc_reactive_generation']

                

    
    def svcres(
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
        powerflow.setup.deltaSVC = zeros([powerflow.setup.ncer])

        # Contador
        ncer = 0

        # Loop
        for _, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra']].tolist()[0]
            idxctrl = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra_controlada']].tolist()[0]

            powerflow.setup.deltaQ[idxcer] = deepcopy(powerflow.sol['svc_reactive_generation'][ncer]) / powerflow.setup.options['sbase']
            powerflow.setup.deltaQ[idxcer] -= PQCalc().qcalc(powerflow, idxcer,)
            
            Smooth(powerflow,).svcsmooth(idxcer, idxctrl, powerflow, ncer, case,)
            
            # Incrementa contador
            ncer += 1
        
        # Resíduo de equação de controle
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaSVC)



    def svcsubjac(
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
        powerflow.setup.pxx = zeros([powerflow.setup.nbus, powerflow.setup.ncer])        
        powerflow.setup.qxx = zeros([powerflow.setup.nbus, powerflow.setup.ncer])
        powerflow.setup.yxx = zeros([powerflow.setup.ncer, powerflow.setup.ncer])
        powerflow.setup.yxt = zeros([powerflow.setup.ncer, powerflow.setup.nbus])
        powerflow.setup.yxv = zeros([powerflow.setup.ncer, powerflow.setup.nbus])

        # Contador
        ncer = 0

        # Submatrizes PXP QXP YQV YXT
        for idx, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra']].tolist()[0]
            idxctrl = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra_controlada']].tolist()[0]
            
            # Derivada Vk
            powerflow.setup.yxv[ncer, idxcer] = powerflow.setup.diffy[idxcer][0]

            # Derivada Vm
            powerflow.setup.yxv[ncer, idxctrl] = powerflow.setup.diffy[idxcer][1]

            # Derivada Qk
            powerflow.setup.qxx[idxcer, ncer] = -1

            # Derivada Qgk - Variável de Estado Adicional
            powerflow.setup.yxx[ncer, ncer] = powerflow.setup.diffy[idxcer][2]

            # Incrementa contador
            ncer += 1


        ## Montagem Jacobiana
        # Condição
        if powerflow.setup.controldim != 0:
            powerflow.setup.extrarow = zeros([powerflow.setup.ncer, powerflow.setup.controldim])
            powerflow.setup.extracol = zeros([powerflow.setup.controldim, powerflow.setup.ncer])

            # H-N M-L + yxt-yxv
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.yxt, powerflow.setup.yxv, powerflow.setup.extrarow), axis=1)), axis=0)

            # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.extracol, powerflow.setup.yxx), axis=0)), axis=1)

        elif powerflow.setup.controldim == 0:
            # H-N M-L + yxt-yxv
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.yxt, powerflow.setup.yxv), axis=1)), axis=0)

            # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.yxx), axis=0)), axis=1)



    def svcupdt(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Contador
        ncer = 0

        # Atualização da potência reativa gerada
        for idx, value in powerflow.setup.dcerDF.iterrows():
            powerflow.sol['svc_reactive_generation'][ncer] += powerflow.setup.statevar[(powerflow.setup.dimpreqlim + ncer)] * powerflow.setup.options['sbase']

            # Incrementa contador
            ncer += 1

        # self.svcsch(powerflow,)


    
    def svcsch(
        self,
        powerflow,
    ):
        """atualização do valor de potência reativa especificada
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Atualização da potência reativa especificada
        ncer = 0
        for idx, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra']].tolist()[0]
            powerflow.setup.pqsch['potencia_reativa_especificada'][idxcer] += powerflow.sol['svc_reactive_generation'][ncer] / powerflow.setup.options['sbase']
            
            # Incrementa contador
            ncer += 1



    def svccorr(
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
        powerflow.sol['reactive_generation'] = deepcopy(powerflow.case[case]['prev']['svc_reactive_generation'])



    def svcheur(
        self,
        powerflow,
    ):
        """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização 
        # Condição de geração de potência reativa ser superior ao valor máximo - analisa apenas para as barras de geração
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

    

    def svcpop(
        self,
        powerflow,
        pop: int=1,
    ):
        """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
                atua diretamente na variável de controle associada à opção de controle svc

        Parâmetros
            powerflow: self do arquivo powerflow.py
            pop: quantidade de ações necessárias
        """

        ## Inicialização
        Smooth(powerflow,).svcpop(powerflow, pop=pop,)