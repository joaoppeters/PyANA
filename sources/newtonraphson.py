# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import abs, append, argmax, array, concatenate, cos, max, ndarray, ones, radians, sin, zeros
from numpy.linalg import solve

from ctrl import Control
from jacobian import Jacobi

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

        while ((max(abs(powerflow.setup.deltaP)) > powerflow.setup.options['tolP']) or (max(abs(powerflow.setup.deltaQ)) > powerflow.setup.options['tolQ']) or (max(abs(powerflow.setup.deltaY)) > powerflow.setup.options['tolY'])):
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
                powerflow.sol['convergence'] = 'SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)'
                break

        # Iteração Adicional
        if powerflow.sol['iter'] < powerflow.setup.options['itermx']:
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
        powerflow.setup.vsch = {
            'potencia_ativa_especificada': zeros(powerflow.setup.nbus),
            'potencia_reativa_especificada': zeros(powerflow.setup.nbus),
        }

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Potência ativa especificada
            powerflow.setup.vsch['potencia_ativa_especificada'][idx] += value['potencia_ativa']
            powerflow.setup.vsch['potencia_ativa_especificada'][idx] -= value['demanda_ativa']

            # Potência reativa especificada
            powerflow.setup.vsch['potencia_reativa_especificada'][idx] += value['potencia_reativa']
            powerflow.setup.vsch['potencia_reativa_especificada'][idx] -= value['demanda_reativa']

        # Tratamento
        powerflow.setup.vsch['potencia_ativa_especificada'] /= powerflow.setup.options['sbase']
        powerflow.setup.vsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']

        # Variáveis especificadas de controle ativos
        if powerflow.setup.ctrlcount > 0:
            Control(powerflow, powerflow.setup).controlsch(powerflow,)



    def residue(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações diferenciáveis"""

        ## Inicialização
        # Vetores de resíduo
        powerflow.setup.deltaP = zeros(powerflow.setup.nbus)
        powerflow.setup.deltaQ = zeros(powerflow.setup.nbus)

        # Resíduo de equação de controle adicional
        powerflow.setup.deltaY = array([])

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if value['tipo'] == 1 or value['tipo'] == 0:
                powerflow.setup.deltaP[idx] += powerflow.setup.vsch['potencia_ativa_especificada'][idx]
                powerflow.setup.deltaP[idx] -= self.pcalc(powerflow, idx,)

                # Tipo PQ - Resíduo Potência Reativa
                if value['tipo'] == 0:
                    powerflow.setup.deltaQ[idx] += powerflow.setup.vsch['potencia_reativa_especificada'][idx]
                    powerflow.setup.deltaQ[idx] -= self.qcalc(powerflow, idx,)

        # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
        self.checkresidue(powerflow,)

        # Resíduos de variáveis de estado de controle
        if powerflow.setup.ctrlcount > 0:
            Control(powerflow, powerflow.setup).controlres(powerflow,)
            self.checkresidue(powerflow,)
            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaPQY, powerflow.setup.deltaY), axis=0)
        else:
            powerflow.setup.deltaY = array([0])



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
        

    
    def checkresidue(
        self,
        powerflow,
    ):
        """
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # configuração completa
        if powerflow.jacobi == 'COMPLETA':
            powerflow.setup.deltaPQY  = concatenate((powerflow.setup.deltaP, powerflow.setup.deltaQ), axis=0)
        # configuração alternada
        elif powerflow.jacobi == 'ALTERNADA':
            powerflow.setup.deltaPQY: ndarray = zeros(shape=[powerflow.setup.nbus, powerflow.setup.nbus], dtype='float')
            pq = -1
            for row in range(0, powerflow.setup.nbus):
                if row % 2 == 0:
                    pq += 1
                    powerflow.setup.deltaPQY[row] = deepcopy(powerflow.setup.deltaP[pq])
                else:
                    powerflow.setup.deltaPQY[row] = deepcopy(powerflow.setup.deltaQ[pq])
        # configuração reduzida
        elif powerflow.jacobi == 'REDUZIDA':
            powerflow.setup.deltaPQY = concatenate((powerflow.setup.deltaP, powerflow.setup.deltaQ), axis=0)
            powerflow.setup.mask = ones(2*powerflow.setup.nbus, bool)
            for idx, value in powerflow.setup.dbarraDF.iterrows():
                if (value['tipo'] == 2) or (value['tipo'] == 1):
                    powerflow.setup.mask[powerflow.setup.nbus+idx] = False
                    if (value['tipo'] == 2):
                        powerflow.setup.mask[idx] = False
            powerflow.setup.deltaPQY[powerflow.setup.mask]
        ## ERROR
        else:
            raise ValueError('\033[91mERROR: Falha na escolha da formulação para montagem da matriz Jacobiana.\nRevise as opções disponíveis e rode novamente o programa!\033[0m')



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
        if powerflow.jacobi == 'COMPLETA':
            powerflow.sol['theta'] += powerflow.setup.statevar[0:(powerflow.setup.nbus)]
            powerflow.sol['voltage'] += powerflow.setup.statevar[(powerflow.setup.nbus):(2 * powerflow.setup.nbus)]
        # configuração alternada
        elif powerflow.jacobi == 'ALTERNADA':
            for idx in range(0, powerflow.setup.nbus):
                powerflow.sol['theta'][idx] += powerflow.setup.statevar[idx]
                powerflow.sol['voltage'][idx] += powerflow.setup.statevar[idx+1]
        # configuração reduzida
        elif powerflow.jacobi == 'REDUZIDA':
            for idx, value in powerflow.setup.dbarraDF.iterrows():
                if (value['tipo'] == 1) or (value['tipo'] == 0):
                    powerflow.sol['theta'][idx] += powerflow.setup.statevar[idx]
                    if value['tipo'] == 0:
                        powerflow.sol['voltage'][idx] += powerflow.setup.statevar[idx + powerflow.setup.nbus]
        
        # Atualização das variáveis de estado adicionais para controles ativos
        if powerflow.setup.ctrlcount > 0:
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
            k = int(value['de']) - 1
            m = int(value['para']) - 1
            yline = 1 / ((value['resistencia'] / 100) + 1j * (value['reatancia'] / 100))
            
            # Verifica presença de transformadores com tap != 1.
            if value['tap'] != 0:
                yline /= value['tap']
            
            # Potência ativa k -> m
            powerflow.sol['active_flow_F2'][idx] = yline.real * (powerflow.sol['voltage'][k] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa k -> m
            powerflow.sol['reactive_flow_F2'][idx] = -((value['susceptancia'] / (2*powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][k] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência ativa m -> k
            powerflow.sol['active_flow_2F'][idx] = yline.real * (powerflow.sol['voltage'][m] ** 2) - powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.real * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) - yline.imag * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

            # Potência reativa m -> k
            powerflow.sol['reactive_flow_2F'][idx] = -((value['susceptancia'] / (2*powerflow.setup.options['sbase'])) + yline.imag) * (powerflow.sol['voltage'][m] ** 2) + powerflow.sol['voltage'][k] * powerflow.sol['voltage'][m] * (yline.imag * cos(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]) + yline.real * sin(powerflow.sol['theta'][k] - powerflow.sol['theta'][m]))

        powerflow.sol['active_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['active_flow_2F'] *= powerflow.setup.options['sbase']

        powerflow.sol['reactive_flow_F2'] *= powerflow.setup.options['sbase']
        powerflow.sol['reactive_flow_2F'] *= powerflow.setup.options['sbase']