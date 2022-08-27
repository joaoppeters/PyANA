# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import abs, append, array, cos, genfromtxt, max, radians, sin, sum, zeros
from numpy.linalg import solve

from ctrl import Control
from jacobian import Jacobi

class Method():
    """classe para aplicação do método selecionado para análise de fluxo de potência"""

    def __init__(
        self,
        powerflow,
        ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        if not hasattr(powerflow, 'sol'):
            # Variáveis de barra
            powerflow.setup.npv = sum(powerflow.setup.dbarraDF.tipo.values == 1)
            powerflow.setup.nger = powerflow.setup.npv + 1
            powerflow.setup.npq = powerflow.setup.nbus - powerflow.setup.nger

            # Variáveis de linha
            powerflow.setup.nlin = len(powerflow.setup.dlinhaDF.de.values)

            # Chamada automática do método de solução selecionado
            self.method(powerflow,)



    def method(
        self,
        powerflow,
    ):
        """chamada automática do método de solução selecionado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Chamada específica método de Newton-Raphson Não-Linear
        if powerflow.method == 'NEWTON':
            self.newtonraphson(powerflow,)

        # Chamada específica método de Gauss-Seidel
        elif powerflow.method == 'GAUSS':
            self.gaussseidel(powerflow,)

        # Chamada específica método de Newton-Raphson Linearizado
        elif powerflow.method == 'LINEAR':
            self.linearpowerflow(powerflow,)

        # Chamada específica método Desacoplado
        elif powerflow.method == 'DECOUP':
            self.decoupledpowerflow(powerflow,)

        # Chamada específica método Desacoplado Rápido
        elif powerflow.method == 'fDECOUP':
            self.fastdecoupledpowerflow(powerflow,)

        # Chamada específica método Continuado
        elif powerflow.method == 'CPF':
            self.continuationpowerflow(powerflow,)

    

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
            'convP': array([]),
            'convQ': array([]),
            'convY': array([]),
            'active_flow_F2': zeros(powerflow.setup.nlin),
            'reactive_flow_F2': zeros(powerflow.setup.nlin),
            'active_flow_2F': zeros(powerflow.setup.nlin),
            'reactive_flow_2F': zeros(powerflow.setup.nlin),
        }

        # Variáveis Especificadas
        self.scheduled(powerflow,)

        # Resíduos
        self.residue(powerflow,)

        # Controles
        self.checkcontrol(powerflow,)

        while ((max(abs(self.deltaP)) > powerflow.setup.options['tolP']) or (max(abs(self.deltaQ)) > powerflow.setup.options['tolQ']) or (max(abs(self.deltaY)) > powerflow.setup.options['tolY'])):
            # Armazenamento da trajetória de convergência
            self.convergence(powerflow.sol,)

            # Atualização da Matriz Jacobiana
            Jacobi(powerflow,)


    

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
        self.vsch = {
            'potencia_ativa_especificada': zeros(powerflow.setup.nbus),
            'potencia_reativa_especificada': zeros(powerflow.setup.nbus),
        }

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Potência ativa especificada
            self.vsch['potencia_ativa_especificada'][idx] += float(value['potencia_ativa'])
            self.vsch['potencia_ativa_especificada'][idx] -= float(value['demanda_ativa'])

            # Potência reativa especificada
            self.vsch['potencia_reativa_especificada'][idx] += float(value['potencia_reativa'])
            self.vsch['potencia_reativa_especificada'][idx] -= float(value['demanda_reativa'])

        # Tratamento
        self.vsch['potencia_ativa_especificada'] /= powerflow.setup.options['sbase']
        self.vsch['potencia_reativa_especificada'] /= powerflow.setup.options['sbase']



    def residue(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações diferenciáveis"""

        ## Inicialização
        # Vetores de resíduo
        self.deltaP = zeros(powerflow.setup.nbus)
        self.deltaQ = zeros(powerflow.setup.nbus)

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            # Tipo PV ou PQ - Resíduo Potência Ativa
            if value['tipo'] == 1 or value['tipo'] == 0:
                self.deltaP[idx] += self.vsch['potencia_ativa_especificada'][idx]
                self.deltaP[idx] -= self.pcalc(powerflow, idx,)

                # Tipo PQ - Resíduo Potência Reativa
                if value['tipo'] == 0:
                    self.deltaQ[idx] += self.vsch['potencia_reativa_especificada'][idx]
                    self.deltaQ[idx] -= self.qcalc(powerflow, idx,)



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



    def checkcontrol(
        self,
        powerflow,
    ):
        """checagem automática de controles ativados
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Resíduo de equação de controle adicional
        self.deltaY = array([])

        for key, _ in powerflow.setup.control.items():
            # Controle Remoto de Tensão
            if (key == 'CREM') and (powerflow.setup.control[key]):
                Control(powerflow, powerflow.setup).ctrlcrem(powerflow,)

            # Controle Secundário de Tensão
            elif (key == 'CST') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlcst(powerflow,)

            # Controle de Tap Variável de Transformadores
            elif (key == 'CTAP') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlctap(powerflow,)

            # Controle de Ângulo de Transformadores Defasadores
            elif (key == 'CTAPd') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlctapd(powerflow,)

            # Controle de Regulação Primária de Frequência
            elif (key == 'FREQ') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlfreq(powerflow,)

            # Controle de Limite de Potência Reativa
            elif (key == 'QLIM') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlqlim(powerflow,)

            # Controle de Compensadores Estáticos de Potência Reativa
            elif (key == 'SVC') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlsvc(powerflow,)

            # Controle de Tensão de Barramentos
            elif (key == 'VCTRL') and (powerflow.setup.control[key]):
                Control(powerflow,).ctrlvctrl(powerflow,)

        if not self.deltaY:
            self.deltaY = 0



    def convergence(
        self,
        sol,
    ):
        """armazenamento da trajetória de convergência do processo de solução do fluxo de potência
        
        Parâmetros
            sol: variável de armazenamento de soluções do self do arquivo powerflow.py
        """

        ## Inicialização
        # Trajetória de convergência da potência ativa
        sol['convP'] = append(sol['convP'], max(abs(self.deltaP)))

        # Trajetória de convergência da potência reativa
        sol['convQ'] = append(sol['convQ'], max(abs(self.deltaQ)))

        # Trajetória de convergência referente a cada equação de controle adicional
        sol['convY'] = append(sol['convY'], max(abs(self.deltaY)))