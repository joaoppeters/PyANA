# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import column_stack, zeros
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
        # Configuração de variáveis para processos de convergência de fluxos de potência tradicionais
        self.pf(powerflow, setup,)
                
        # # Nenhuma opção de método de solução para análise de fluxo de potência foi selecionado
        # else:
        #     raise ValueError('\033[91mERROR: A opção de método de solução selecionada para análise de fluxo de potência não é válida!\nRode novamente o programa e selecione uma das alternativas informadas!\033[0m')


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
            'BASE': 100., 'DASE': 100., 'FBASE': 60.,
            'TEPA': 1E-3, 'TEPR': 1E-3, 'TLPR': 1E-3,  'TLVC': 5E-3, 'TLTC': 1E-4, 'TETP': 5E-2, 'TBPA': 5E-2, 'TSFR': 1E-4,
            'TUDC': 1E-5, 'TADC': 1E-4, 'TPST': 2E-3,  'QLST': 4E-3, 'EXST': 4E-3, 'TLPP': 1E-2, 'TSBZ': 1E-4, 'TSBA': 5E-2,
            'PGER': 0.3,  'VFLD': 0.7,  'VART': 5E-2,  'TSTP': 33,   'NDIR': 20,   'STIR': 1,    'STTR': 5E-2, 'TRPT': 1,
            'ZMIN': 1E-5, 'VDVN': 0.4,  'ICMN': 5E-4,  'BFPO': 1E-2,
            'ZMAX': 5E2,  'VDVM': 2.,   'ASTP': 0.05,  'VSTP': 5E-2, 'CSTP': 5E-2, 'DMAX': 5,    'TSDC': 0.02, 'ASDC': 1,
            'ACIT': 30,   'ICIT': 30,   'LPIT': 50,    'LFLP': 10,   'LFIT': 10,   'DCIT': 10,   'VSIT': 10,   'LFCV': 1,    'PDIT': 10,
            'FDIV': 2,    'ICMV': 5E-3, 'APAS': .9,    'CPAR': .7,
            'VAVT': 2E-2, 'VAVF': 5E-2, 'VMVF': 15E-2, 'VPVT': 2E-2, 'VPVF': 5E-2, 'VPMF': 10E-2, 
        }

# 'BASE': 100.,
# 'ACIT': 15,
# 'TEPA': 1E-8, #10
# 'TEPR': 1E-8, #10
# 'tolY': 1E-8, #10
# 'vmax': 1.05,
# 'vmin': 0.95,
# 'vvar': 1E-8,
# 'qvar': 1E-8,
# 'cpfBeta': 0.,
# 'cpfLambda': 1E-1,
# 'cpfV2L': 0.95,
# 'cpfVolt': 1E-4,
# 'icmn': 1E-10,
# 'full': False,

        setup.options = dict()

        for k, v in self.stdpf.items():
            if (k not in setup.dcteDF['constante']):
                setup.options[k] = v
            else:
                setup.options[k] = deepcopy(setup.dcteDF.loc[setup.dcteDF['constante'] == k]['valor_constante'][0])



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
        self.stdcpf = {
            'cpfBeta': 0., 
            'cpfLambda': 1E-1,
            'cpfVolt': 5E-4,
            'cpfV2L': 0.85,
            'icmn': 5E-4,
            'full': False,
        }
        
        for k, v in self.stdcpf.items():
            if (k not in powerflow.options):
                setup.options[k] = v
            else:
                setup.options[k] = deepcopy(powerflow.options[k])

        if (not setup.dincDF.empty):
            setup.options['cpfLambda'] = setup.dincDF.loc[0, 'passo_incremento_potencia_ativa']

        
        setup.options['cpfBeta'] = zeros(setup.nbus)
        if (hasattr(setup, 'dgeraDF')) and (not setup.dgeraDF.empty):
            for idx, value in setup.dgeraDF.iterrows():
                idx = value['numero'] - 1
                setup.options['cpfBeta'][idx] = value['fator_participacao']