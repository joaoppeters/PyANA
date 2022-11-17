# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, array, zeros

from ctrlfreq import Freq
from ctrlqlim import Qlim

from ctrlqlims import Qlims

class Control:
    """classe para determinar a realização das opções de controle escolhidas"""

    def __init__(
        self,
        powerflow,
        setup,
    ):
        """inicialização

        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        if not hasattr(powerflow, 'setup'):
            if powerflow.control:
                setup.maskctrlcount = 0
                setup.control = dict()
                # if not setup.control:
                self.control = {
                    'CREM': False, 
                    'CST': False,
                    'CTAP': False,
                    'CTAPd': False,
                    'FREQ': False,
                    'QLIM': False,
                    'QLIMs': False,
                    'SVC' : False,
                    'VCTRL': False,
                    }
                
                self.checkcontrol(powerflow, setup,)

            else:
                setup.control = dict()
                print('\033[96mNenhuma opção de controle foi escolhida.\033[0m')



    def checkcontrol(
        self,
        powerflow,
        setup,
    ):
        """verificação das opções de controle escolhidas
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """
        
        ## Inicialização
        print('\033[96mOpções de controle escolhidas: ', end='')
        for k, _ in self.control.items():
            if k in powerflow.control:
                setup.control[k] = True
                print(f'{k}', end=' ')
        print('\033[0m')


    
    def controlsol(
        self, 
        powerflow,
    ):
        """altera variável de armazenamento de solução do fluxo de potência em função do controle ativo

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        if not hasattr(powerflow.setup, 'ctrlcount'):
            powerflow.setup.controlcount = 0
            powerflow.setup.controlorder = dict()

        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'CREM'
                pass
            # controle secundário de tensão
            elif key == 'CST':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'CST'
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'CTAP'
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'CTAPd'
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'FREQ'
                Freq(powerflow,).freqsol(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'QLIM'
                Qlim().qlimsol(powerflow,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'QLIMs'
                Qlims().qlimssol(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'SVC'
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                powerflow.setup.controlcount += 1
                powerflow.setup.controlorder[powerflow.setup.controlcount] = 'VCTRL'
                pass


    
    def controlsch(
        self,
        powerflow,
    ):
        """adiciona variáveis especificadas de controles ativos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                pass
            # controle secundário de tensão
            elif key == 'CST':
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq(powerflow,).freqsch(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                Qlim().qlimsch(powerflow,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                Qlims().qlimssch(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                pass

    

    def controlres(
        self,
        powerflow,
    ):
        """adiciona resíduos de equações de controle de controles ativos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        powerflow.setup.deltaY = array([])

        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                pass
            # controle secundário de tensão
            elif key == 'CST':
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq(powerflow,).freqres(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                Qlim().qlimres(powerflow,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                Qlims().qlimsres(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                pass

        if powerflow.setup.deltaY.size == 0:
            powerflow.setup.deltaY = array([0]) 


    
    def controljac(
        self,
        powerflow,
    ):
        """submatrizes referentes aos controles ativos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        powerflow.setup.truedim = deepcopy(powerflow.setup.jacob.shape[0])

        # Loop
        for key,_ in powerflow.setup.control.items():
            # Dimensão
            powerflow.setup.controldim = powerflow.setup.jacob.shape[0] - powerflow.setup.truedim

            # controle remoto de tensão
            if key == 'CREM':
                pass
            # controle secundário de tensão
            elif key == 'CST':
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq(powerflow,).freqsubjac(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                Qlim().qlimsubjac(powerflow,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                Qlims().qlimssubjac(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                pass

        # Dimensão
        powerflow.setup.controldim = powerflow.setup.jacob.shape[0] - powerflow.setup.truedim
        
        # Atualização da Máscara da Jacobiana
        if powerflow.setup.maskctrlcount == 0:
            powerflow.setup.mask = append(powerflow.setup.mask, zeros(powerflow.setup.controldim, dtype=bool))
            powerflow.setup.maskctrlcount += 1

    

    def controlupdt(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado adicionais por controle ativo
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                pass
            # controle secundário de tensão
            elif key == 'CST':
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq(powerflow,).frequpdt(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                Qlim().qlimupdt(powerflow,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                Qlims().qlimsupdt(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                pass



    def controlcorrsol(
        self,
        powerflow,
        case,
    ):
        """atualização das variáveis de controle para a etapa de correção do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                pass
            # controle secundário de tensão
            elif key == 'CST':
                pass
            # controle de tap variável de transformador
            elif key == 'CTAP':
                pass
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                pass
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq(powerflow,).freqcorr(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                Qlim().qlimcorr(powerflow, case,)
            # controle suave de limite de geração de potência reativa
            elif key == 'QLIMs':
                Qlims().qlimscorr(powerflow, case,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                pass
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                pass



    def controlheuristics(
        self,
        powerflow,
    ):
        """aplicação de heurísticas das variáveis de controle para a etapa de correção do fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        powerflow.setup.controlheur = False
        if not hasattr(powerflow.setup, 'bifurcation'):
            powerflow.setup.bifurcation = False
        
        # Loop
        for key,_ in powerflow.setup.control.items():
            if (powerflow.setup.controlheur) or ((powerflow.setup.bifurcation) and (not powerflow.setup.options['full'])):
                break
            
            elif (not powerflow.setup.controlheur) and (not powerflow.cpfsol['pmc']):
                # controle remoto de tensão
                if key == 'CREM':
                    pass
                # controle secundário de tensão
                elif key == 'CST':
                    pass
                # controle de tap variável de transformador
                elif key == 'CTAP':
                    pass
                # controle de ângulo de transformador defasador
                elif key == 'CTAPd':
                    pass
                # controle de regulação primária de frequência
                elif key == 'FREQ':
                    pass
                # controle de limite de geração de potência reativa
                elif key == 'QLIM':
                    Qlim().qlimheur(powerflow,)
                # controle suave de limite de geração de potência reativa
                elif key == 'QLIMs':
                    Qlims().qlimheur(powerflow,)
                # controle de compensadores estáticos de potência reativa
                elif key == 'SVC':
                    pass
                # controle de magnitude de tensão de barramentos
                elif key == 'VCTRL':
                    pass