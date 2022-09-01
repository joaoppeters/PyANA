# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from numpy import array

from freq import Freq

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
                setup.control = dict()
                # if not setup.control:
                self.control = {
                    'CREM': False, 
                    'CST': False,
                    'CTAP': False,
                    'CTAPd': False,
                    'FREQ': False,
                    'QLIM': False,
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
        powerflow.setup.ctrlcount = 0
        powerflow.setup.ctrlorder = dict()
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'CREM'
                self.solcrem(powerflow,)
            # controle secundário de tensão
            elif key == 'CST':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'CST'
                self.solcst(powerflow,)
            # controle de tap variável de transformador
            elif key == 'CTAP':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'CTAP'
                self.solctap(powerflow,)
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'CTAPd'
                self.solctapd(powerflow,)
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'FREQ'
                Freq().freqsol(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'QLIM'
                self.solqlim(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'SVC'
                self.solsvc(powerflow,)
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                powerflow.setup.ctrlcount += 1
                powerflow.setup.ctrlorder[powerflow.setup.ctrlcount] = 'VCTRL'
                self.solvctrl(powerflow,)


    
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
                self.solcrem(powerflow,)
            # controle secundário de tensão
            elif key == 'CST':
                self.solcst(powerflow,)
            # controle de tap variável de transformador
            elif key == 'CTAP':
                self.solctap(powerflow,)
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                self.solctapd(powerflow,)
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq().freqsch(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                self.solqlim(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                self.solsvc(powerflow,)
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                self.solvctrl(powerflow,)

    

    def controlres(
        self,
        powerflow,
    ):
        """adiciona resíduos de equações de controle de controles ativos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                self.solcrem(powerflow,)
            # controle secundário de tensão
            elif key == 'CST':
                self.solcst(powerflow,)
            # controle de tap variável de transformador
            elif key == 'CTAP':
                self.solctap(powerflow,)
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                self.solctapd(powerflow,)
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq().freqres(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                self.solqlim(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                self.solsvc(powerflow,)
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                self.solvctrl(powerflow,)

        if powerflow.setup.deltaY.size == 0:
            powerflow.setup.deltaY = array([]) 


    
    def controljac(
        self,
        powerflow,
    ):
        """submatrizes referentes aos controles ativos
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Loop
        for key,_ in powerflow.setup.control.items():
            # controle remoto de tensão
            if key == 'CREM':
                self.solcrem(powerflow,)
            # controle secundário de tensão
            elif key == 'CST':
                self.solcst(powerflow,)
            # controle de tap variável de transformador
            elif key == 'CTAP':
                self.solctap(powerflow,)
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                self.solctapd(powerflow,)
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq().freqsubjac(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                self.solqlim(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                self.solsvc(powerflow,)
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                self.solvctrl(powerflow,)

    

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
                self.solcrem(powerflow,)
            # controle secundário de tensão
            elif key == 'CST':
                self.solcst(powerflow,)
            # controle de tap variável de transformador
            elif key == 'CTAP':
                self.solctap(powerflow,)
            # controle de ângulo de transformador defasador
            elif key == 'CTAPd':
                self.solctapd(powerflow,)
            # controle de regulação primária de frequência
            elif key == 'FREQ':
                Freq().frequpdt(powerflow,)
            # controle de limite de geração de potência reativa
            elif key == 'QLIM':
                self.solqlim(powerflow,)
            # controle de compensadores estáticos de potência reativa
            elif key == 'SVC':
                self.solsvc(powerflow,)
            # controle de magnitude de tensão de barramentos
            elif key == 'VCTRL':
                self.solvctrl(powerflow,)



    def solcrem(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle remoto de tensão esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solcst(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle secundário de tensão esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solctap(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle de tap variável de transformador esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solctapd(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle de ângulo de transformador defasador esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solqlim(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle de limite de geração de potência reativa esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solsvc(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle de compensadores estáticos de potência reativa esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass



    def solvctrl(
        self,
        powerflow,
    ):
        """adiciona variáveis na solução para caso controle de magnitude de tensão de barramentos esteja ativado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py"""

        ## Inicialização
        pass