# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #



class Options:
    """classe para configuração dos valores padrão de variáveis de tolerância para o processo de convergência do fluxo de potência"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """
        ## Inicialização
        self.stdmethods = ['NEWTON', 'GAUSS', 'LINEAR', 'DECOUP', 'fDECOUP']
        # Configuração de variáveis para processos de convergência de fluxos de potência tradicionais
        if powerflow.method in self.stdmethods:
            self.pf(powerflow,)
        # Configuração de variáveis para processo de convergência do fluxo de potência continuado
        elif powerflow.method == 'CPF':
            self.cpf(powerflow,)

        # else:
        #     ## ERROR - VERMELHO
        #     raise ValueError('\033[91mNenhum sistema foi selecionado.\033[0m')



    def pf(
        self,
        powerflow,
    ):
        """configuração de variáveis para processos de convergência de fluxos de potência tradicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis padrão
        self.stdpf = {
            'itermx': 15,
            'tolP': 1E-6,
            'tolQ': 1E-6,
            'tolY': 1E-6,
            'vmax': 1.05,
            'vmin': 0.95,
        }
        
        for k, v in self.stdpf.items():
            if k not in powerflow.options:
                powerflow.options[k] = v



    def cpf(
        self,
        powerflow,
    ):
        """configuração de variáveis para processos de convergência de fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis padrão
        self.pf(self, powerflow,)
        self.stdcpf = {
            'cpfL': 1E-1,
            'cpfV': 1E-3,
            'cpfV2L': 0.85,
        }
        
        for k, v in self.stdcpf.items():
            if k not in powerflow.options:
                powerflow.options[k] = v