# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from copy import deepcopy

class Options:
    """classe para configuração dos valores padrão de variáveis de tolerância para o processo de convergência do fluxo de potência"""

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
        self.standard()
        # Configuração de variáveis para processos de convergência de fluxos de potência tradicionais
        if powerflow.method in self.stdmethods:
            self.pf(powerflow, setup,)
        # Configuração de variáveis para processo de convergência do fluxo de potência continuado
        elif powerflow.method == 'CPF':
            self.cpf(powerflow, setup,)
        # Nenhuma opção de método de solução para análise de fluxo de potência foi selecionado
        else:
            raise ValueError('\033[91mERROR: A opção de método de solução selecionada para análise de fluxo de potência não é válida!\nRode novamente o programa e selecione uma das alternativas informadas!\033[0m')



    def standard(
        self,
    ):
        """configuração padrão"""

        ## Inicialização
        self.stdmethods = ['NEWTON', 'GAUSS', 'LINEAR', 'DECOUP', 'fDECOUP']
    
    
    
    def pf(
        self,
        powerflow,
        setup,
    ):
        """configuração de variáveis para processos de convergência de fluxos de potência tradicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            setup: self do arquivo setup.py
        """

        ## Inicialização
        # Variáveis padrão
        self.stdpf = {
            'sbase': 100.,
            'fbase': 60.,
            'itermx': 15,
            'tolP': 1E-6,
            'tolQ': 1E-6,
            'tolY': 1E-6,
            'vmax': 1.05,
            'vmin': 0.95,
            'vvar': 1E-6,
            'qvar': 1E-6,
        }
        
        setup.options = dict()

        # if powerflow.options:
        for k, v in self.stdpf.items():
            if k not in powerflow.options:
                setup.options[k] = v
            else:
                setup.options[k] = deepcopy(powerflow.options[k])



    def cpf(
        self,
        powerflow,
        setup,
    ):
        """configuração de variáveis para processos de convergência de fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis padrão
        self.pf(powerflow, setup,)
        self.stdcpf = {
            'cpfBeta': 0., 
            'cpfLambda': 1E-1,
            'cpfVolt': 5E-4,
            'cpfV2L': 0.85,
            'icmn': 5E-4,
            'full': True,
        }
        
        for k, v in self.stdcpf.items():
            if k not in powerflow.options:
                setup.options[k] = v
            else:
                setup.options[k] = deepcopy(powerflow.options[k])