# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import append, concatenate, cos, infty, radians, sin, zeros

class Freq:
    """classe para regulação primária de frequência"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        if not hasattr(powerflow.setup, 'freqjcount'):
            powerflow.setup.freqjcount = 0
        pass


    
    def freqsol(
        self,
        powerflow,
    ):
        """adiciona variáveis narea solução para caso controle de regulação primária de frequência esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        
        ## Inicialização
        # Variável
        powerflow.setup.nare = 1

        # Condição
        if powerflow.setup.control['FREQ']:
            # DGER contém dados de todos os geradores 
            if powerflow.setup.dgeraDF.numero.shape[0] == powerflow.setup.nger:
                # Variáveis
                powerflow.sol['active_generation'] = zeros(powerflow.setup.nger)
                powerflow.sol['reactive_generation'] = zeros(powerflow.setup.nger)        
                powerflow.setup.fesp = 1

                # Loop
                nger = 0
                for idx, value in powerflow.setup.dbarraDF.iterrows():
                    # Barra tipo VT ou PV
                    if value['tipo'] != 0:
                        powerflow.sol['active_generation'][nger] = value['potencia_ativa'] / powerflow.setup.options['sbase']
                        powerflow.sol['reactive_generation'][nger] = value['potencia_reativa'] / powerflow.setup.options['sbase']
                        nger += 1
                # Frequências máxima e mínima por gerador
                self.freqgerlim(powerflow,)
                
            # DGER não contém dados de todos os geradores
            else:
                powerflow.setup.control['FREQ'] = False
                print('\033[93mERROR: Controle `FREQ` não será ativado por insuficiência de dados de barras geradoras!\nAtualize o campo `DGER` do arquivo {}!\033[0m'.format(powerflow.system))



    def freqgerlim(
        self,
        powerflow,
        ):
        """cálculo das frequências máximas e mínimas de operação de cada gerador
        
        Parâmetros
            powerflow: self do arquivo powerflowl.py
        """

        ## Inicialização
        # Variáveis
        powerflow.setup.freqger = {
            'max': zeros(powerflow.setup.nger),
            'min': zeros(powerflow.setup.nger)
        }
        powerflow.setup.dgerorder = dict()

        # Loop
        for idx, value in powerflow.setup.dgeraDF.iterrows():
            # Armazenamento da barra por ordem de entrada de dados dos geradores
            powerflow.setup.dgerorder[idx] = powerflow.setup.dbarraDF['nome'][value['numero'] - 1]
            # Frequência máxima gerador `idx`
            powerflow.setup.freqger['max'][idx] = powerflow.setup.fesp + value['estatismo'] * 1E-2 * (powerflow.setup.dbarraDF['potencia_ativa'][value['numero'] - 1] - value['potencia_ativa_minima']) / powerflow.setup.options['sbase']
            # Frequência mínima gerador `idx`
            powerflow.setup.freqger['min'][idx] = powerflow.setup.fesp + value['estatismo'] * 1E-2 * (powerflow.setup.dbarraDF['potencia_ativa'][value['numero'] - 1] - value['potencia_ativa_maxima']) / powerflow.setup.options['sbase']



    def freqsch(
        self,
        powerflow,
    ):
        """armazenamento de parâmetros especificados das equações de controle adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis adicionais
        powerflow.setup.vsch['potencia_ativa_gerada_especificada'] = zeros(powerflow.setup.nger)
        powerflow.setup.vsch['potencia_reativa_gerada_especificada'] = zeros(powerflow.setup.nger)
        powerflow.setup.vsch['magnitude_tensao_especificada'] = zeros(powerflow.setup.nbus)
        powerflow.setup.vsch['defasagem_angular_especificada'] = zeros(powerflow.setup.nbus)
        
        # Contador de geradores
        nger = 0

        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0.:
                # Potência ativa gerada
                powerflow.setup.vsch['potencia_ativa_gerada_especificada'][nger] = value['potencia_ativa']
                # Potência reativa gerada
                powerflow.setup.vsch['potencia_reativa_gerada_especificada'][nger] = value['potencia_reativa']
                # Magnitude de tensão
                powerflow.setup.vsch['magnitude_tensao_especificada'][idx] = value['tensao'] * 1E-3
                # Condição - slack
                if value['tipo'] == 2:
                    # Defasagem angular
                    powerflow.setup.vsch['defasagem_angular_especificada'][idx] = radians(value['angulo'])
                # Incrementa contador
                nger += 1

        # Tratamento
        powerflow.setup.vsch['potencia_ativa_gerada_especificada'] /= powerflow.setup.options['sbase']
        powerflow.setup.vsch['potencia_reativa_gerada_especificada'] /= powerflow.setup.options['sbase']


    
    def freqres(
        self,
        powerflow,
    ):
        """cálculo de resíduos das equações de controle adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Vetor de resíduos
        powerflow.setup.deltaPger = zeros([powerflow.setup.nger])
        powerflow.setup.deltaQger = zeros([powerflow.setup.nger])
        powerflow.setup.deltaTger = zeros([powerflow.setup.nare])

        # Contador
        nger = 0

        # Loop
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
            #     # Cálculo do resíduo DeltaP
            #     powerflow.setup.deltaPQY[idx] = powerflow.setup.vsch['potencia_ativa_especificada'][idx]
            #     powerflow.setup.deltaPQY[idx] -= self.pcalc(powerflow, idx,)

            #     # Cálculo do resíduo DeltaQ
            #     powerflow.setup.deltaPQY[idx + powerflow.setup.nbus] = powerflow.setup.vsch['potencia_reativa_especificada'][idx]
            #     powerflow.setup.deltaPQY[idx + powerflow.setup.nbus] -= self.qcalc(powerflow, idx,)

            # else:
                # Cálculo do resíduo DeltaP
                powerflow.setup.deltaP[idx] = powerflow.sol['active_generation'][nger]
                powerflow.setup.deltaP[idx] -= value['demanda_ativa'] / powerflow.setup.options['sbase']
                powerflow.setup.deltaP[idx] -= self.pcalc(powerflow, idx,)

                # Cálculo do resíduo DeltaQ
                powerflow.setup.deltaQ[idx] = powerflow.sol['reactive_generation'][nger]
                powerflow.setup.deltaQ[idx] -= value['demanda_reativa'] / powerflow.setup.options['sbase']
                powerflow.setup.deltaQ[idx] -= self.qcalc(powerflow, idx,)

                # Tratamento de limite de potência ativa
                if powerflow.sol['freq'] >= powerflow.setup.freqger['max'][nger] or powerflow.sol['freq'] <= powerflow.setup.freqger['min'][nger]:
                    powerflow.setup.deltaPger[nger] = 0.
                else:
                    powerflow.setup.deltaPger[nger] += powerflow.setup.vsch['potencia_ativa_gerada_especificada'][nger]
                    powerflow.setup.deltaPger[nger] -= powerflow.sol['active_generation'][nger]
                    powerflow.setup.deltaPger[nger] -= (1 / (powerflow.setup.dgeraDF['estatismo'][nger] * 1E-2)) * (powerflow.sol['freq'] - powerflow.setup.fesp)

                # Tratamento de limite de magnitude de tensão
                powerflow.setup.deltaQger[nger] += powerflow.setup.vsch['magnitude_tensao_especificada'][idx]
                powerflow.setup.deltaQger[nger] -= powerflow.sol['voltage'][idx]
                
                # Condição - slack
                if value['tipo'] == 2:
                    # Tratamento de limite de 
                    powerflow.setup.deltaTger += powerflow.setup.vsch['defasagem_angular_especificada'][idx]
                    powerflow.setup.deltaTger -= powerflow.sol['theta'][idx]
                
                # Incrementa contador
                nger += 1
        
        # Resíduo de equação de controle
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaPger)
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaQger)
        powerflow.setup.deltaY = append(powerflow.setup.deltaY, powerflow.setup.deltaTger)



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



    def freqsubjac(
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
        #   H     N   pxp   pxq   pxx
        #   M     L   qxp   qxq   qxx
        # ypt   ypv   ypp   ypq   ypx
        # yqt   yqv   yqp   yqq   yqx
        # yxt   yxv   yxp   yxq   yxx
        # 
        
        # Condição
        if powerflow.setup.freqjcount == 0:
            # Variável
            powerflow.setup.freqjcount += 1
            
            # Submatrizes
            powerflow.setup.pxp = zeros([powerflow.setup.nbus, powerflow.setup.nger]) # -> APG
            powerflow.setup.pxq = zeros([powerflow.setup.nbus, powerflow.setup.nger])
            powerflow.setup.pxx = zeros([powerflow.setup.nbus, powerflow.setup.nare])        

            powerflow.setup.qxp = zeros([powerflow.setup.nbus, powerflow.setup.nger])
            powerflow.setup.qxq = zeros([powerflow.setup.nbus, powerflow.setup.nger]) # -> BQG
            powerflow.setup.qxx = zeros([powerflow.setup.nbus, powerflow.setup.nare])
            
            powerflow.setup.ypt = zeros([powerflow.setup.nger, powerflow.setup.nbus])
            powerflow.setup.ypv = zeros([powerflow.setup.nger, powerflow.setup.nbus])
            powerflow.setup.ypp = zeros([powerflow.setup.nger, powerflow.setup.nger]) # -> CPG
            powerflow.setup.ypq = zeros([powerflow.setup.nger, powerflow.setup.nger])
            powerflow.setup.ypx = zeros([powerflow.setup.nger, powerflow.setup.nare]) # -> CF        

            powerflow.setup.yqt = zeros([powerflow.setup.nger, powerflow.setup.nbus])
            powerflow.setup.yqv = zeros([powerflow.setup.nger, powerflow.setup.nbus]) # -> EQG
            powerflow.setup.yqp = zeros([powerflow.setup.nger, powerflow.setup.nger])
            powerflow.setup.yqq = zeros([powerflow.setup.nger, powerflow.setup.nger])
            powerflow.setup.yqx = zeros([powerflow.setup.nger, powerflow.setup.nare])

            powerflow.setup.yxt = zeros([powerflow.setup.nare, powerflow.setup.nbus]) # -> FT
            powerflow.setup.yxv = zeros([powerflow.setup.nare, powerflow.setup.nbus])
            powerflow.setup.yxp = zeros([powerflow.setup.nare, powerflow.setup.nger])
            powerflow.setup.yxq = zeros([powerflow.setup.nare, powerflow.setup.nger])
            powerflow.setup.yxx = zeros([powerflow.setup.nare, powerflow.setup.nare])

            # Contadores
            nger = 0
            nare = 0

            # Submatrizes PXP QXP YQV YXT
            for idx, value in powerflow.setup.dbarraDF.iterrows():
                if value['tipo'] != 0:
                    powerflow.setup.pxp[idx, nger] = -1.
                    powerflow.setup.qxq[idx, nger] = -1.
                    powerflow.setup.yqv[nger, idx] = 1.
                    nger += 1

                    if value['tipo'] == 2:
                        powerflow.setup.yxt[nare, idx] = 1.

            # Submatrizes YPP YPX
            for idx, value in powerflow.setup.dgeraDF.iterrows():
                powerflow.setup.ypp[idx, idx] = 1.
                powerflow.setup.ypx[idx, nare] = 1. / (value['estatismo'] * 1E-2)

        ## Montagem Jacobiana
        # H-N M-L + ypt-ypv + yqt-yqv + yxt-yxv
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((concatenate((powerflow.setup.ypt, powerflow.setup.ypv), axis=1), concatenate((powerflow.setup.yqt, powerflow.setup.yqv), axis=1), concatenate((powerflow.setup.yxt, powerflow.setup.yxv), axis=1)), axis=0)), axis=0)

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxp, powerflow.setup.qxp, powerflow.setup.ypp, powerflow.setup.yqp, powerflow.setup.yxp), axis=0)), axis=1)

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp + pxq-qxq-ypq-yqq-yxq
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxq, powerflow.setup.qxq, powerflow.setup.ypq, powerflow.setup.yqq, powerflow.setup.yxq), axis=0)), axis=1)

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp pxq-qxq-ypq-yqq-yxq + pxx-qxx-ypx-yqx-yxx
        powerflow.setup.jacob = concatenate((powerflow.setup.jacob, concatenate((powerflow.setup.pxx, powerflow.setup.qxx, powerflow.setup.ypx, powerflow.setup.yqx, powerflow.setup.yxx), axis=0)), axis=1)



    def frequpdt(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Atualização da potência ativa gerada
        powerflow.sol['active_generation'] += powerflow.setup.statevar[(2 * powerflow.setup.nbus):(2 * powerflow.setup.nbus + powerflow.setup.nger)]
        # Atualização da potência reativa gerada
        powerflow.sol['reactive_generation'] += powerflow.setup.statevar[(2 * powerflow.setup.nbus + powerflow.setup.nger):(2 * powerflow.setup.nbus + 2 * powerflow.setup.nger)]
        # Atualização da defasagem angular
        powerflow.sol['freq'] += powerflow.setup.statevar[(2 * powerflow.setup.nbus + 2 * powerflow.setup.nger)]

        # Tratamento de limite de potência ativa
        for idx, value in powerflow.setup.dgeraDF.iterrows():
            if powerflow.sol['freq'] >= powerflow.setup.freqger['max'][idx]:
                powerflow.sol['active_generation'][idx] = value['potencia_ativa_minima'] / powerflow.setup.options['sbase']
                powerflow.setup.ypp[idx][idx] = infty
            elif powerflow.sol['freq'] <= powerflow.setup.freqger['min'][idx]:
                powerflow.sol['active_generation'][idx] = value['potencia_ativa_maxima'] / powerflow.setup.options['sbase']
                powerflow.setup.ypp[idx][idx] = infty
            else:
                powerflow.setup.ypp[idx][idx] = 1