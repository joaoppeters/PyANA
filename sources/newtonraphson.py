# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import abs, append, arange, argmax, array, concatenate, cos, dot, insert, max, radians, sin, zeros
from numpy.linalg import det, eig, solve, inv

from calc import PQCalc
from ctrl import Control
from jacobian import Jacobi
from smooth import Smooth

class NewtonRaphson:
    """classe para cálculo do fluxo de potência não-linear via método newton-raphson"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        self.newtonraphson(powerflow,)

        # Smooth
        if ('QLIMs' in powerflow.setup.control) and (powerflow.method == 'NEWTON'):
            Smooth(powerflow,).qlimstorage(powerflow,)



    def newtonraphson(
        self,
        powerflow,
    ):
        """análise do fluxo de potência não-linear em regime permanente de SEP via método Newton-Raphson
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento de solução
        powerflow.sol = {
            'system': powerflow.setup.name,
            'iter': 0,
            'voltage': array(powerflow.setup.dbarraDF['tensao'] * 1E-3),
            'theta': array(radians(powerflow.setup.dbarraDF['angulo'])),
            'active': zeros(powerflow.setup.nbus),
            'reactive': zeros(powerflow.setup.nbus),
            'freq': 1.,
            'freqiter': array([]),
            'convP': array([]),
            'busP': array([]),
            'convQ': array([]),
            'busQ': array([]),
            'convY': array([]),
            'busY': array([]),
            'active_flow_F2': zeros(powerflow.setup.nlin),
            'reactive_flow_F2': zeros(powerflow.setup.nlin),
            'active_flow_2F': zeros(powerflow.setup.nlin),
            'reactive_flow_2F': zeros(powerflow.setup.nlin),
        }

        # Controles
        Control(powerflow, powerflow.setup).controlsol(powerflow,)

        # Variáveis Especificadas
        self.scheduled(powerflow,)

        # Resíduos
        self.residue(powerflow,)

        while ((max(abs(powerflow.setup.deltaP)) > powerflow.setup.options['tolP']) or \
            (max(abs(powerflow.setup.deltaQ)) > powerflow.setup.options['tolQ']) or \
                (max(abs(powerflow.setup.deltaY)) > powerflow.setup.options['tolY'])):

            # Armazenamento da trajetória de convergência
            self.convergence(powerflow,)

            # Atualização da Matriz Jacobiana
            Jacobi(powerflow,)

            # Variáveis de estado
            powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)
            
            # Atualização das Variáveis de estado
            self.update_statevar(powerflow,)

            # Atualização dos resíduos
            self.residue(powerflow,)
            
            # Incremento de iteração
            powerflow.sol['iter'] += 1

            # Condição
            if powerflow.sol['iter'] > powerflow.setup.options['itermx']:
                # Divergência
                powerflow.sol['convergence'] = 'SISTEMA DIVERGENTE'
                break

        # Iteração Adicional
        if powerflow.sol['iter'] <= powerflow.setup.options['itermx']:
            # Armazenamento da trajetória de convergência
            self.convergence(powerflow,)

            # Atualização da Matriz Jacobiana
            Jacobi(powerflow,)

            # Variáveis de estado
            powerflow.setup.statevar = solve(powerflow.setup.jacob, powerflow.setup.deltaPQY)

            # Atualização das Variáveis de estado
            self.update_statevar(powerflow,)

            # Atualização dos resíduos
            self.residue(powerflow,)

            # Fluxo em linhas de transmissão
            self.line_flow(powerflow,)

            # Análise de autovalores & sensibilidade
            self.eigensens(powerflow,)
            
            # Convergência
            powerflow.sol['convergence'] = 'SISTEMA CONVERGENTE'

    

    def scheduled(
        self,
        powerflow,
    ):
        """método para armazenamento dos parâmetros especificados
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável para armazenamento das potências ativa e reativa especificadas
        powerflow.setup.pqsch = {
            'potencia_ativa_especificada': zeros(powerflow.setup.nbus),
            'potencia_reativa_especificada': zeros(powerflow.setup.nbus),
        }

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.setup.pqsch['potencia_ativa_especificada'][idx] += value['potencia_ativa']
            powerflow.setup.pqsch['potencia_ativa_especificada'][idx] -= value['demanda_ativa']

            # Potência reativa especificada
            powerflow.setup.pqsch['potencia_reativa_especificada'][idx] += value['potencia_reativa']
            powerflow.setup.pqsch['potencia_reativa_especificada'][idx] -= value['demanda_reativa']

        # Tratamento
        powerflow.setup.pqsch['potencia_ativa_especificada'] /= powerflow.setup.options['sbase']
        powerflow.setup.pqsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']

        # Variáveis especificadas de controle ativos
        if powerflow.setup.controlcount > 0:
            Control(powerflow, powerflow.setup).controlsch(powerflow,)



    def residue(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações diferenciáveis
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Vetores de resíduo
        powerflow.setup.deltaP = zeros(powerflow.setup.nbus)
        powerflow.setup.deltaQ = zeros(powerflow.setup.nbus)

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if (value['tipo'] != 2):
                powerflow.setup.deltaP[idx] += powerflow.setup.pqsch['potencia_ativa_especificada'][idx]
                powerflow.setup.deltaP[idx] -= PQCalc().pcalc(powerflow, idx,)

            # Tipo PQ - Resíduo Potência Reativa
            if ('QLIM' in powerflow.setup.control) or ('QLIMs' in powerflow.setup.control) or (value['tipo'] == 0):
                powerflow.setup.deltaQ[idx] += powerflow.setup.pqsch['potencia_reativa_especificada'][idx]
                powerflow.setup.deltaQ[idx] -= PQCalc().qcalc(powerflow, idx,)

        # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
        self.concatresidue(powerflow,)

        # Resíduos de variáveis de estado de controle
        if powerflow.setup.controlcount > 0:
            Control(powerflow, powerflow.setup).controlres(powerflow,)
            self.concatresidue(powerflow,)
            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaPQY, powerflow.setup.deltaY), axis=0)
        else:
            powerflow.setup.deltaY = array([0])
        

    
    def concatresidue(
        self,
        powerflow,
    ):
        """concatenação de resíduos de potências ativa e reativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # configuração completa
        powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaP, powerflow.setup.deltaQ), axis=0)



    def convergence(
        self,
        powerflow,
    ):
        """armazenamento da trajetória de convergência do processo de solução do fluxo de potência
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Trajetória de convergência da frequência
        powerflow.sol['freqiter'] = append(powerflow.sol['freqiter'], powerflow.sol['freq'] * powerflow.setup.options['fbase'])

        # Trajetória de convergência da potência ativa
        powerflow.sol['convP'] = append(powerflow.sol['convP'], max(abs(powerflow.setup.deltaP)))
        powerflow.sol['busP'] = append(powerflow.sol['busP'], argmax(abs(powerflow.setup.deltaP)))

        # Trajetória de convergência da potência reativa
        powerflow.sol['convQ'] = append(powerflow.sol['convQ'], max(abs(powerflow.setup.deltaQ)))
        powerflow.sol['busQ'] = append(powerflow.sol['busQ'], argmax(abs(powerflow.setup.deltaQ)))

        # Trajetória de convergência referente a cada equação de controle adicional
        if powerflow.setup.deltaY.size != 0:
            powerflow.sol['convY'] = append(powerflow.sol['convY'], max(abs(powerflow.setup.deltaY)))
            powerflow.sol['busY'] = append(powerflow.sol['busY'], argmax(abs(powerflow.setup.deltaY)))
        else:
            powerflow.sol['convY'] = append(powerflow.sol['convY'], 0.)
            powerflow.sol['busY'] = append(powerflow.sol['busY'], 0.)

    

    def update_statevar(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # configuração completa
        powerflow.sol['theta'] += powerflow.setup.statevar[0:(powerflow.setup.nbus)]
        powerflow.sol['voltage'] += powerflow.setup.statevar[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]

        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.setup.controlcount > 0:
            Control(powerflow, powerflow.setup).controlupdt(powerflow,)



    def line_flow(
        self,
        powerflow,
        ):
        """cálculo do fluxo de potência nas linhas de transmissão
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        ## Inicialização 
        for idx, value in powerflow.setup.dlinhaDF.iterrows():
            k = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['de']][0]
            m = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == value['para']][0]
            yline = 1 / ((value['resistencia'] / 100) + 1j * (value['reatancia'] / 100))
            
            # Verifica presença de transformadores com tap != 1.
            if value['tap'] != 0:
                yline /= value['tap']
            
            # Potência ativa k -> m
            powerflow.sol['active_flow_F2'][idx] = yline.real * (powerflow.sol['voltage'][k] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa k -> m
            powerflow.sol['reactive_flow_F2'][idx] = -((value['susceptancia'] / (2 * powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][k] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência ativa m -> k
            powerflow.sol['active_flow_2F'][idx] = yline.real * (powerflow.sol['voltage'][m] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa m -> k
            powerflow.sol['reactive_flow_2F'][idx] = -((value['susceptancia'] / (2 * powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][m] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

        powerflow.sol['active_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['active_flow_2F'] *= powerflow.setup.options['sbase']

        powerflow.sol['reactive_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['reactive_flow_2F'] *= powerflow.setup.options['sbase']



    def eigensens(
        self,
        powerflow,
    ):
        """análise de autovalores e autovetores

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Reorganização da Matriz Jacobiana Expandida
        self.jacob = deepcopy(powerflow.setup.jacob)
        
        if (('QLIM' in powerflow.setup.control) or ('QLIMs' in powerflow.setup.control)):
            self.reidx = insert(arange(0, ((2 * powerflow.setup.nbus))), (powerflow.setup.nbus), (-1 * arange(1, powerflow.setup.nger + 1)))

            self.jacob = self.jacob[self.reidx, :][:, self.reidx]

            # Submatrizes Jacobianas
            self.pt = deepcopy(self.jacob[:(powerflow.setup.nbus + powerflow.setup.nger), :][:, :(powerflow.setup.nbus + powerflow.setup.nger)])
            self.pv = deepcopy(self.jacob[:(powerflow.setup.nbus + powerflow.setup.nger), :][:, (powerflow.setup.nbus + powerflow.setup.nger):(2 * powerflow.setup.nbus + powerflow.setup.nger)])
            self.qt = deepcopy(self.jacob[(powerflow.setup.nbus + powerflow.setup.nger):(2 * powerflow.setup.nbus + powerflow.setup.nger), :][:, :(powerflow.setup.nbus + powerflow.setup.nger)])
            self.qv = deepcopy(self.jacob[(powerflow.setup.nbus + powerflow.setup.nger):(2 * powerflow.setup.nbus + powerflow.setup.nger), :][:, (powerflow.setup.nbus + powerflow.setup.nger):(2 * powerflow.setup.nbus + powerflow.setup.nger)])

        elif not (('QLIM' in powerflow.setup.control) or ('QLIMs' in powerflow.setup.control)):
            # Submatrizes Jacobianas
            self.pt = deepcopy(self.jacob[:(powerflow.setup.nbus), :][:, :(powerflow.setup.nbus)])
            self.pv = deepcopy(self.jacob[:(powerflow.setup.nbus), :][:, (powerflow.setup.nbus):(2 * powerflow.setup.nbus)])
            self.qt = deepcopy(self.jacob[(powerflow.setup.nbus):(2 * powerflow.setup.nbus), :][:, :(powerflow.setup.nbus)])
            self.qv = deepcopy(self.jacob[(powerflow.setup.nbus):(2 * powerflow.setup.nbus), :][:, (powerflow.setup.nbus):(2 * powerflow.setup.nbus)])

        try:
            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida 
            rightvalues, rightvector = eig(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])
            powerflow.setup.PF = zeros([powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask].shape[0], powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask].shape[1]])

            # Jacobiana reduzida - sensibilidade PT
            powerflow.setup.jacobPT = self.pt - dot(dot(self.pv, inv(self.qv)), self.qt)
            rightvaluesPT, rightvectorPT = eig(powerflow.setup.jacobPT)
            powerflow.setup.PFPT = zeros([powerflow.setup.jacobPT.shape[0], powerflow.setup.jacobPT.shape[1]])

            # Jacobiana reduzida - sensibilidade QV
            powerflow.setup.jacobQV = self.qv - dot(dot(self.qt, inv(self.pt)), self.pv)
            # powerflow.setup.jacobQV = deepcopy(powerflow.setup.jacob)
            rightvaluesQV, rightvectorQV = eig(powerflow.setup.jacobQV)
            powerflow.setup.PFQV = zeros([powerflow.setup.jacobQV.shape[0], powerflow.setup.jacobQV.shape[1]])
            for row in range(0, powerflow.setup.jacobQV.shape[0]):
                for col in range(0, powerflow.setup.jacobQV.shape[1]):
                    powerflow.setup.PFQV[col, row] = rightvectorQV[col, row] * inv(rightvectorQV)[row, col]

            # Condição
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.case[self.case]['jacobian'] = powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask]

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.case[self.case]['determinant'] = det(powerflow.setup.jacob[powerflow.setup.mask, :][:, powerflow.setup.mask])

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            powerflow.case[self.case]['eigenvalues'] = rightvalues
            powerflow.case[self.case]['eigenvectors'] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.case[self.case]['participation_factor'] = powerflow.setup.PF

            # Armazenamento da matriz de sensibilidade QV
            powerflow.case[self.case]['jacobian-QV'] = powerflow.setup.jacobQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.case[self.case]['determinant-QV'] = det(powerflow.setup.jacobQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            powerflow.case[self.case]['eigenvalues-QV'] = rightvaluesQV
            powerflow.case[self.case]['eigenvectors-QV'] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.case[self.case]['participationfactor-QV'] = powerflow.setup.PFQV

        # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa 
        # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
        except:
            # Loop
            pass