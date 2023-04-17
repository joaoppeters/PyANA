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

class SVCs:
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
        if ('svc_reactive_generation' not in powerflow.sol):
            if (powerflow.setup.dcerDF['controle'][0] == 'A'):
                powerflow.sol['svc_reactive_generation'] = powerflow.setup.dcerDF['potencia_reativa'].to_numpy()
                self.alphavar(powerflow,)

            elif (powerflow.setup.dcerDF['controle'][0] == 'I'):
                powerflow.sol['svc_current_injection'] = powerflow.setup.dcerDF['potencia_reativa'].to_numpy()

            elif (powerflow.setup.dcerDF['controle'][0] == 'P'):
                powerflow.sol['svc_reactive_generation'] = powerflow.setup.dcerDF['potencia_reativa'].to_numpy()



    def alphavar(
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
        powerflow.sol['alpha'] = roots([(8 / 1856156927625), 0, (-4 / 10854718875), 0, (16 / 638512875), 0, (-8 / 6081075), 0, (8 / 155925), 0, (-4 / 2835), 0, (8 / 315), 0, (-4 / 15), 0, (4 / 3), 0, 0, -(2 * pi) + ((powerflow.setup.alphaxl * pi) / powerflow.setup.alphaxc),])
        powerflow.sol['alpha'] = powerflow.sol['alpha'][isreal(powerflow.sol['alpha'])][0].real

        # Variáveis Simbólicas
        global alpha
        alpha = Symbol('alpha')
        powerflow.setup.alphabeq = -((powerflow.setup.alphaxc / pi) * (2 * (pi - alpha) + sin(2 * alpha)) - powerflow.setup.alphaxl) / (powerflow.setup.alphaxc * powerflow.setup.alphaxl)

        # Potência Reativa
        idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == powerflow.setup.dcerDF['barra'][0]].tolist()[0]
        powerflow.sol['svc_reactive_generation'][0] = (powerflow.sol['voltage'][idxcer] ** 2) * powerflow.setup.alphabeq.subs(alpha, powerflow.sol['alpha'])

                

    
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
            
            if (value['controle'] == 'A'):
                Smooth(powerflow,).svcalphasmooth(idxcer, idxctrl, powerflow, ncer, case,)
                powerflow.setup.deltaQ[idxcer] = deepcopy(powerflow.sol['svc_reactive_generation'][ncer]) / powerflow.setup.options['sbase']

            elif (value['controle'] == 'I'):
                Smooth(powerflow,).svccurrentsmooth(idxcer, idxctrl, powerflow, ncer, case,)
                powerflow.setup.deltaQ[idxcer] = deepcopy(powerflow.sol['svc_current_injection'][ncer]) * powerflow.sol['voltage'][idxcer] / powerflow.setup.options['sbase']
            
            elif (value['controle'] == 'P'):
                Smooth(powerflow,).svcreactivesmooth(idxcer, idxctrl, powerflow, ncer, case,)
                powerflow.setup.deltaQ[idxcer] = deepcopy(powerflow.sol['svc_reactive_generation'][ncer]) / powerflow.setup.options['sbase']

            powerflow.setup.deltaQ[idxcer] -= powerflow.setup.dbarraDF['demanda_reativa'][idxcer] / powerflow.setup.options['sbase']
            powerflow.setup.deltaQ[idxcer] -= PQCalc().qcalc(powerflow, idxcer,)
                
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
        powerflow.setup.dimpresvc = deepcopy(powerflow.setup.jacob.shape[0])
            
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

            if (value['barra'] != value['barra_controlada']):
                # Derivada Vk
                powerflow.setup.yxv[ncer, idxcer] = powerflow.setup.diffsvc[idxcer][0]

                # Derivada Vm
                powerflow.setup.yxv[ncer, idxctrl] = powerflow.setup.diffsvc[idxcer][1]

            elif (value['barra'] == value['barra_controlada']):
                # Derivada Vk + Vm
                powerflow.setup.yxv[ncer, idxcer] = powerflow.setup.diffsvc[idxcer][0] + powerflow.setup.diffsvc[idxcer][1]

            # Derivada Equação de Controle Adicional por Variável de Estado Adicional
            powerflow.setup.yxx[ncer, ncer] = powerflow.setup.diffsvc[idxcer][2]

            # Derivada Qk
            if (value['controle'] == 'A'):
                powerflow.setup.jacob[powerflow.setup.nbus + idxcer, powerflow.setup.nbus + idxcer] -= (2 * powerflow.sol['voltage'][idxcer] * float(powerflow.setup.alphabeq.subs(alpha, powerflow.sol['alpha'])))
                powerflow.setup.qxx[idxcer, ncer] = -(powerflow.sol['voltage'][idxcer] ** 2) * float(powerflow.setup.alphabeq.diff(alpha).subs(alpha, powerflow.sol['alpha']))

            elif (value['controle'] == 'I'):
                powerflow.setup.jacob[powerflow.setup.nbus + idxcer, powerflow.setup.nbus + idxcer] -= (powerflow.sol['svc_current_injection'][ncer]) / powerflow.setup.options['sbase']
                powerflow.setup.qxx[idxcer, ncer] = -powerflow.sol['voltage'][idxcer]

            elif (value['controle'] == 'P'):
                powerflow.setup.qxx[idxcer, ncer] = -1
        
            # Incrementa contador
            ncer += 1


        ## Montagem Jacobiana
        # Condição
        if (powerflow.setup.controldim != 0):
            powerflow.setup.extrarow = zeros([powerflow.setup.ncer, powerflow.setup.controldim])
            powerflow.setup.extracol = zeros([powerflow.setup.controldim, powerflow.setup.ncer])

            # H-N M-L + yxt-yxv
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.yxt, powerflow.setup.yxv, powerflow.setup.extrarow), axis=1)), axis=0)

            # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
            powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.extracol, powerflow.setup.yxx), axis=0)), axis=1)

        elif (powerflow.setup.controldim == 0):
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
            idxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['barra']].tolist()[0]
            
            if (value['controle'] == 'A'):
                powerflow.sol['alpha'] += powerflow.setup.statevar[(powerflow.setup.dimpresvc + ncer)]
            
            elif (value['controle'] == 'I'):
                powerflow.sol['svc_current_injection'][ncer] += powerflow.setup.statevar[(powerflow.setup.dimpresvc + ncer)] * powerflow.setup.options['sbase']
            
            elif (value['controle'] == 'P'):
                powerflow.sol['svc_reactive_generation'][ncer] += powerflow.setup.statevar[(powerflow.setup.dimpresvc + ncer)] * powerflow.setup.options['sbase']

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
            if (powerflow.setup.dcerDF['controle'][0] == 'A') or (powerflow.setup.dcerDF['controle'][0] == 'P'):
                powerflow.setup.pqsch['potencia_reativa_especificada'][idxcer] += powerflow.sol['svc_reactive_generation'][ncer] / powerflow.setup.options['sbase']
            
            elif (powerflow.setup.dcerDF['controle'][0] == 'I'):
                powerflow.setup.pqsch['potencia_reativa_especificada'][idxcer] += (powerflow.sol['svc_current_injection'][ncer] * powerflow.sol['voltage'][idxcer]) / powerflow.setup.options['sbase']

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
        powerflow.sol['svc_reactive_generation'] = deepcopy(powerflow.case[case]['prev']['svc_reactive_generation'])



    def svcheur(
        self,
        powerflow,
    ):
        """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização 
        # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB 
        if (not powerflow.cpfsol['pmc']) and (powerflow.cpfsol['varstep'] == 'lambda') and ((powerflow.setup.options['cpfLambda'] * (5E-1 ** powerflow.cpfsol['div'])) <= powerflow.setup.options['icmn']):
            powerflow.setup.bifurcation = True

    

    def svcpop(
        self,
        powerflow,
        pop: int=1,
    ):
        """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
                atua diretamente na variável de controle associada à opção de controle SVCs

        Parâmetros
            powerflow: self do arquivo powerflow.py
            pop: quantidade de ações necessárias
        """

        ## Inicialização
        Smooth(powerflow,).svcpop(powerflow, pop=pop,)



    def svccpf(
        self,
        powerflow,
    ):
        """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        powerflow.cpfsol['svc_reactive_generation'] = deepcopy(powerflow.sol['svc_reactive_generation'])



    def svcsolcpf(
        self,
        powerflow,
        case,
    ):
        """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: etapa do fluxo de potência continuado analisada
        """

        ## Inicialização
        # Condição
        precase = case - 1
        if (case == 1):
            powerflow.sol['svc_reactive_generation'] = deepcopy(powerflow.case[precase]['svc_reactive_generation'])
        
        elif (case > 1):
            powerflow.sol['svc_reactive_generation'] = deepcopy(powerflow.case[precase]['prev']['svc_reactive_generation'])