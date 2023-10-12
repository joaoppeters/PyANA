# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from matplotlib import pyplot as plt
from numpy import abs, arange, array, exp as npexp, linspace, min as mn, pi, seterr
from sympy import Symbol
from sympy.functions import exp as spexp

from folder import Folder

class Smooth:
    """classe para aplicação da função suave sigmoide"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis
        if ('QLIMs' in powerflow.setup.control) and (not hasattr(powerflow.setup, 'TEPRlimq')):
            powerflow.setup.TEPRlimq = 1E-8
            powerflow.setup.TEPRlimv = 1E-8
            powerflow.setup.qliminc = 1E10

        if ('SVCs' in powerflow.setup.control) and (not hasattr(powerflow.setup, 'tolsvcq')):
            powerflow.setup.tolsvcv = 1E-8
            powerflow.setup.tolalpha = 1E-8
            powerflow.setup.svcinc = 1E10



    def qlimssmooth(
        self,
        idx,
        powerflow,
        nger,
        case,
    ):
        """aplicação da função suave sigmoide para tratamento de limite de geração de potência reativa
        
        Parâmetros
            idx: índice da da barra geradora
            powerflow: self do arquivo powerflow.py
            nger: índice de geradores
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        seterr(all="ignore")

        # Variáveis
        if not hasattr(powerflow.setup, 'qlimkeys'):
            powerflow.setup.qlimkeys = dict()
            powerflow.setup.diffqlim = dict()

        if powerflow.setup.qlimkeys.get(powerflow.setup.dbarraDF.loc[idx, 'nome']) is None:
            powerflow.setup.qlimkeys[powerflow.setup.dbarraDF.loc[idx, 'nome']] = dict()

        if case not in powerflow.setup.qlimkeys[powerflow.setup.dbarraDF.loc[idx, 'nome']]:
            powerflow.setup.qlimkeys[powerflow.setup.dbarraDF.loc[idx, 'nome']][case] = list()

        # Variáveis Simbólicas
        qger = Symbol('Qg')
        vger = Symbol('V')
        vesp = Symbol('Vesp')
        qmax = Symbol('Qmax')
        qmin = Symbol('Qmin')

        # Associação das variáveis
        var = {
           qger: powerflow.sol['reactive_generation'][idx] * 1E-2,
           vger: powerflow.sol['voltage'][idx],
           vesp: powerflow.setup.dbarraDF.loc[idx, 'tensao'] * 1E-3,
           qmax: powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa_maxima'] / powerflow.setup.options['BASE'],
           qmin: powerflow.setup.dbarraDF.loc[idx, 'potencia_reativa_minima'] / powerflow.setup.options['BASE'],
        }


        ## Limites
        # Limites de Tensão
        vlimsup = vesp + powerflow.setup.TEPRlimv
        vliminf = vesp - powerflow.setup.TEPRlimv

        # Limites de Potência Reativa
        qlimsup = qmax - powerflow.setup.TEPRlimq
        qliminf = qmin + powerflow.setup.TEPRlimq


        ## Chaves
        # Chave Superior de Potência Reativa
        ch1 = 1 / (1 + spexp(-powerflow.setup.qliminc * (qger - qlimsup)))

        # Chave Inferior de Poência Reativa
        ch2 = 1 / (1 + spexp(powerflow.setup.qliminc * (qger - qliminf)))

        # Chave Superior de Tensão
        ch3 = 1 / (1 + spexp(powerflow.setup.qliminc * (vger - vlimsup)))

        # Chave Inferior de Tensão
        ch4 = 1 / (1 + spexp(-powerflow.setup.qliminc * (vger - vliminf)))


        ## Equações de Controle
        # Normal
        Ynormal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (vger - vesp)
        
        # Superior
        Ysuperior = (ch1 * ch3) * (1 - ch2 * ch4) * (qger - qmax)
        
        # Inferior 
        Yinferior = (1 - ch1 * ch3) * (ch2 * ch4) * (qger - qmin)


        ## Derivadas
        # Derivada Parcial de Y por Qg
        diffyqg = (Ynormal + Ysuperior + Yinferior).diff(qger)

        # Derivada Parcial de Y por V
        diffyv = (Ynormal + Ysuperior + Yinferior).diff(vger)

        # Expressão Geral
        powerflow.setup.diffqlim[idx] = array([diffyv.subs(var), diffyqg.subs(var)], dtype='float64')

        
        ## Resíduo
        powerflow.setup.deltaQlim[nger] = - Ynormal.subs(var) - Ysuperior.subs(var) - Yinferior.subs(var)
                    

        ## Armazenamento de valores das chaves
        powerflow.setup.qlimkeys[powerflow.setup.dbarraDF.loc[idx, 'nome']][case].append(array([ch1.subs(var), ch2.subs(var), ch3.subs(var), ch4.subs(var)]))


    
    def svcreactivesmooth(
        self,
        idxcer,
        idxctrl,
        powerflow,
        ncer,
        case,
    ):
        """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
            metodologia por potência reativa injetada
        
        Parâmetros
            idxcer: índice da barra do compensador estático de potência reativa
            idxctrl: índice da barra controlada pelo compensador estático de potência reativa
            powerflow: self do arquivo powerflow.py
            ncer: índice do compensador estático de potência reativa
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        seterr(all="ignore")

        # Variáveis
        if not hasattr(powerflow.setup, 'svckeys'):
            powerflow.setup.svckeys = dict()
            powerflow.setup.diffsvc = dict()

        if powerflow.setup.svckeys.get(powerflow.setup.dbarraDF.loc[idxcer, 'nome']) is None:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']] = dict()

        if case not in powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']]:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case] = list()

        # Variáveis Simbólicas
        vk = Symbol("Vk")
        vm = Symbol("Vm")

        qgk = Symbol("Qgk")
        r = Symbol("r")
        
        bmin = Symbol("Bmin")
        bmax = Symbol("Bmax")

        vmsch = powerflow.setup.dbarraDF.loc[idxctrl, 'tensao'] * 1E-3
        vmmax = vmsch + (r * bmin * (vk ** 2))
        vmmin = vmsch + (r * bmax * (vk ** 2))

        # Associação das variáveis
        varkey = {
            vk: powerflow.sol['voltage'][idxcer],
            vm: powerflow.sol['voltage'][idxctrl],
            r: powerflow.setup.dcerDF.loc[ncer, 'droop'],
            bmin: powerflow.setup.dcerDF.loc[ncer, 'potencia_reativa_minima'] / (powerflow.setup.options['BASE'] * (powerflow.setup.dbarraDF.loc[idxcer, 'tensao_base'] * 1E-3) ** 2),
            bmax: powerflow.setup.dcerDF.loc[ncer, 'potencia_reativa_maxima'] / (powerflow.setup.options['BASE'] * (powerflow.setup.dbarraDF.loc[idxcer, 'tensao_base'] * 1E-3) ** 2),
        }

        var = deepcopy(varkey)
        var[qgk] = (powerflow.sol['svc_reactive_generation'][ncer]) / (powerflow.setup.options['BASE'])
            

        ## Limites
        # Limites de Tensão
        vlimsup = vmmax + powerflow.setup.tolsvcv
        vliminf = vmmin - powerflow.setup.tolsvcv


        ## Chaves
        # Chave Superior de Potência Reativa - Região Indutiva
        ch1 = 1 / (1 + spexp(-powerflow.setup.svcinc * (vm - vlimsup)))

        # Chave Inferior de Poência Reativa - Região Capacitiva
        ch2 = 1 / (1 + spexp(powerflow.setup.svcinc * (vm - vliminf)))


        ## Equações de Controle
        # Região Indutiva
        Yindutiva = (ch1) * (-(vk ** 2) * bmin + qgk)

        # Região Linear
        Ylinear = (1 - ch1) * (1 - ch2) * (-vmsch -(r * qgk) + vm)

        # Região Capacitiva
        Ycapacitiva = (ch2) * (-(vk ** 2) * bmax + qgk)


        ## Derivadas
        # Derivada Parcial de Y por Vk
        diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

        # Derivada Parcial de Y por Vm
        diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

        # Derivada Parcial de Y por Qgk
        diffyqgk = (Yindutiva + Ylinear + Ycapacitiva).diff(qgk)

        # Expressão Geral
        powerflow.setup.diffsvc[idxcer] = array([diffyvk.subs(var), diffyvm.subs(var), diffyqgk.subs(var),], dtype='float64')


        ## Resíduo
        powerflow.setup.deltaSVC[ncer] = - Yindutiva.subs(var) - Ylinear.subs(var) - Ycapacitiva.subs(var)

                    
        ## Armazenamento de valores das chaves
        powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case].append(array([ch1.subs(varkey), ch2.subs(varkey),], dtype='float',))


    
    def svccurrentsmooth(
        self,
        idxcer,
        idxctrl,
        powerflow,
        ncer,
        case,
    ):
        """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
            metodologia por corrente injetada
        
        Parâmetros
            idxcer: índice da barra do compensador estático de potência reativa
            idxctrl: índice da barra controlada pelo compensador estático de potência reativa
            powerflow: self do arquivo powerflow.py
            ncer: índice do compensador estático de potência reativa
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        seterr(all="ignore")

        # Variáveis
        if not hasattr(powerflow.setup, 'svckeys'):
            powerflow.setup.svckeys = dict()
            powerflow.setup.diffsvc = dict()

        if powerflow.setup.svckeys.get(powerflow.setup.dbarraDF.loc[idxcer, 'nome']) is None:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']] = dict()

        if case not in powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']]:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case] = list()

        # Variáveis Simbólicas
        vk = Symbol("Vk")
        vm = Symbol("Vm")

        ik = Symbol("Ik")
        r = Symbol("r")
        
        bmin = Symbol("Bmin")
        bmax = Symbol("Bmax")

        vmsch = powerflow.setup.dbarraDF.loc[idxctrl, 'tensao'] * 1E-3
        vmmax = vmsch + (r * bmin * vk)
        vmmin = vmsch + (r * bmax * vk)

        # Associação das variáveis
        varkey = {
            vk: powerflow.sol['voltage'][idxcer],
            vm: powerflow.sol['voltage'][idxctrl],
            r: powerflow.setup.dcerDF.loc[ncer, 'droop'],
            bmin: powerflow.setup.dcerDF.loc[ncer, 'potencia_reativa_minima'] / (powerflow.setup.options['BASE'] * powerflow.setup.dbarraDF.loc[idxcer, 'tensao_base'] * 1E-3),
            bmax: powerflow.setup.dcerDF.loc[ncer, 'potencia_reativa_maxima'] / (powerflow.setup.options['BASE'] * powerflow.setup.dbarraDF.loc[idxcer, 'tensao_base'] * 1E-3),
        }

        var = deepcopy(varkey)
        var[ik] = (powerflow.sol['svc_current_injection'][ncer]) / (powerflow.setup.options['BASE'])
            

        ## Limites
        # Limites de Tensão
        vlimsup = vmmax + powerflow.setup.tolsvcv
        vliminf = vmmin - powerflow.setup.tolsvcv


        ## Chaves
        # Chave Superior de Potência Reativa - Região Indutiva
        ch1 = 1 / (1 + spexp(-powerflow.setup.svcinc * (vm - vlimsup)))

        # Chave Inferior de Poência Reativa - Região Capacitiva
        ch2 = 1 / (1 + spexp(powerflow.setup.svcinc * (vm - vliminf)))


        ## Equações de Controle
        # Região Indutiva
        Yindutiva = (ch1) * (-vk * bmin + ik)

        # Região Linear
        Ylinear = (1 - ch1) * (1 - ch2) * (-vmsch -(r * ik) + vm)

        # Região Capacitiva
        Ycapacitiva = (ch2) * (-vk * bmax + ik)


        ## Derivadas
        # Derivada Parcial de Y por Vk
        diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

        # Derivada Parcial de Y por Vm
        diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

        # Derivada Parcial de Y por Ik
        diffyik = (Yindutiva + Ylinear + Ycapacitiva).diff(ik)

        # Expressão Geral
        powerflow.setup.diffsvc[idxcer] = array([diffyvk.subs(var), diffyvm.subs(var), diffyik.subs(var),], dtype='float64')

        
        ## Resíduo
        powerflow.setup.deltaSVC[ncer] = - Yindutiva.subs(var) - Ylinear.subs(var) - Ycapacitiva.subs(var)
                    

        ## Armazenamento de valores das chaves
        powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case].append(array([ch1.subs(varkey), ch2.subs(varkey),], dtype='float',))


    
    def svcalphasmooth(
        self,
        idxcer,
        idxctrl,
        powerflow,
        ncer,
        case,
    ):
        """aplicação da função suave sigmoide para modelagem de compensadores estáticos de potência reativa
            metodologia por ângulo de disparo
        
        Parâmetros
            idxcer: índice da barra do compensador estático de potência reativa
            idxctrl: índice da barra controlada pelo compensador estático de potência reativa
            powerflow: self do arquivo powerflow.py
            ncer: índice do compensador estático de potência reativa
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        flagv0 = False
        seterr(all="ignore")

        # Variáveis
        if not hasattr(powerflow.setup, 'svckeys'):
            powerflow.setup.svckeys = dict()
            powerflow.setup.diffsvc = dict()

        if powerflow.setup.svckeys.get(powerflow.setup.dbarraDF.loc[idxcer, 'nome']) is None:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']] = dict()

        if case not in powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']]:
            powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case] = list()

        # Variáveis Simbólicas
        vk = Symbol("Vk")
        vm = Symbol("Vm")

        r = Symbol("r")
        alpha = Symbol("alpha")

        vmsch = powerflow.setup.dbarraDF.loc[idxctrl, 'tensao'] * 1E-3
        vmmax = vmsch + (powerflow.setup.dcerDF.loc[ncer, 'droop'] * powerflow.setup.alphabeq.subs(alpha, pi/2) * (powerflow.sol['voltage'][idxcer] ** 2))
        vmmin = vmsch + (powerflow.setup.dcerDF.loc[ncer, 'droop'] * powerflow.setup.alphabeq.subs(alpha, pi) * (powerflow.sol['voltage'][idxcer] ** 2))

        # Associação das variáveis
        var = {
            vk: powerflow.sol['voltage'][idxcer],
            vm: powerflow.sol['voltage'][idxctrl],
            r: powerflow.setup.dcerDF.loc[ncer, 'droop'],
            alpha: powerflow.sol['alpha'],
        }
            

        ## Limites
        # Limites de Ângulo de disparo
        alphalimsup = pi - powerflow.setup.tolalpha
        alphaliminf = pi/2 + powerflow.setup.tolalpha

        # Limites de Tensão
        vlimsup = vmmax + powerflow.setup.tolsvcv
        vliminf = vmmin - powerflow.setup.tolsvcv


        ## Chaves
        # Chave Inferior de Ângulo de disparo
        ch1 = 1 / (1 + npexp(powerflow.setup.svcinc * (powerflow.sol['alpha'] - alphaliminf)))

        # Chave Superior de Ângulo de disparo
        ch2 = 1 / (1 + npexp(-powerflow.setup.svcinc * (powerflow.sol['alpha'] - alphalimsup)))

        # Chave Inferior de Tensão
        ch3 = 1 / (1 + npexp(powerflow.setup.svcinc * float(powerflow.sol['voltage'][idxctrl] - vliminf)))

        # Chave Superior de Tensao
        ch4 = 1 / (1 + npexp(-powerflow.setup.svcinc * float(powerflow.sol['voltage'][idxctrl] - vlimsup)))


        # Equações de Controle
        
        # ch1 = sw10
        # ch2 = sw9
        # ch3 = sw12
        # ch4 = sw11
        
        # Região Indutiva
        Yindutiva = ch1 * (1 - ch3) * (alpha - pi/2)

        # Região Linear
        Ylinear = ((1 - ch1)*(1 - ch3)*ch4 + (1 - ch2)*(1 - ch4)*ch3 + (1 - ch1) * (1 - ch2) * (1 - ch3) * (1 - ch4)) * (-vmsch - (r * (vk ** 2) * powerflow.setup.alphabeq) + vm)

        # Região Capacitiva
        Ycapacitiva = ch2 * (1 - ch4) * (alpha - pi)


        ## Derivadas
        # Derivada Parcial de Y por Vk
        diffyvk = (Yindutiva + Ylinear + Ycapacitiva).diff(vk)

        # Derivada Parcial de Y por Vm
        diffyvm = (Yindutiva + Ylinear + Ycapacitiva).diff(vm)

        # Derivada Parcial de Y por alpha
        diffyalpha = (Yindutiva + Ylinear + Ycapacitiva).diff(alpha)

        

        if powerflow.sol['alpha'] <= pi/2 + powerflow.setup.tolalpha:
            # powerflow.sol['alpha'] = pi/2
            if powerflow.sol['voltage'][idxctrl] <= vmmin:
                powerflow.sol['voltage'][idxctrl] = deepcopy(vmsch)
                powerflow.sol['alpha'] = deepcopy(powerflow.sol['alpha0'])
                
                # flagv0 = True

        elif powerflow.sol['alpha'] >= pi - powerflow.setup.tolalpha:
            # powerflow.sol['alpha'] = pi
            if powerflow.sol['voltage'][idxctrl] >= vmmax:
                powerflow.sol['voltage'][idxctrl] = deepcopy(vmsch)
                powerflow.sol['alpha'] = deepcopy(powerflow.sol['alpha0'])
                
                # flagv0 = True

        # if powerflow.sol['voltage'][idxctrl] >= vmmax:
        #     powerflow.sol['alpha'] = pi/2
        #     powerflow.sol.alpha_[-1] = alpha

        # elif powerflow.sol['voltage'][idxctrl] <= vmmin:
        #     powerflow.sol['alpha'] = pi
        #     powerflow.sol.alpha_[-1] = alpha

        # if (powerflow.sol.alpha_[-2] == pi/2 and powerflow.sol.alpha_[-1] == pi) or \
        #     (powerflow.sol.alpha_[-1] == pi/2 and powerflow.sol.alpha_[-2] == pi):
        #     powerflow.sol.alpha_[-1] = powerflow.sol['alpha0']
        #     powerflow.sol['alpha'] = deepcopy(powerflow.sol['alpha0'])
        #     powerflow.sol['voltage'][idxctrl] = deepcopy(vmsch)

        var = {
            vk: powerflow.sol['voltage'][idxcer],
            vm: powerflow.sol['voltage'][idxctrl],
            r: powerflow.setup.dcerDF['droop'][0],
            alpha: powerflow.sol['alpha'],
        }

        
        powerflow.sol['svc_reactive_generation'][ncer] = (powerflow.sol['voltage'][idxcer] ** 2) * powerflow.setup.alphabeq.subs(alpha, powerflow.sol['alpha']) * powerflow.setup.options['BASE']

        # Expressão Geral
        powerflow.setup.diffsvc[idxcer] = array([diffyvk.subs(var), diffyvm.subs(var), diffyalpha.subs(var),], dtype='float64')

        
        ## Resíduo
        powerflow.setup.deltaSVC[ncer] = - Yindutiva.subs({vm:powerflow.sol['voltage'][idxctrl], alpha:powerflow.sol['alpha']}) - Ylinear.subs(var) - Ycapacitiva.subs({vm:powerflow.sol['voltage'][idxctrl], alpha:powerflow.sol['alpha']})


        # if flagv0:
        #     powerflow.sol['voltage'][idxctrl] = deepcopy(vmsch)
                    

        ## Armazenamento de valores das chaves
        powerflow.setup.svckeys[powerflow.setup.dbarraDF.loc[idxcer, 'nome']][case].append(array([ch1, ch2, ch3, ch4,], dtype='float',))


    
    def qlimspop(
        self,
        powerflow,
        pop: int=1,
    ):
        """deleta última instância salva em variável powerflow.setup.qlimskeys
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
            pop: quantidade de ações necessárias
        """

        ## Inicialização
        for idx, value in powerflow.setup.dbarraDF.iterrows():
            popped = 0
            if value['tipo'] != 0:
                while popped < pop:
                    powerflow.setup.qlimkeys[value['nome']].popitem()
                    popped += 1
        
    
    
    def qlimstorage(
        self,
        powerflow,
    ):
        """armazenamento e geração de imagens referente a comutação das chaves

        Parâmetros:
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Criação automática de diretório
        Folder(powerflow.setup,).smooth(powerflow, powerflow.setup,)

        # Condição de método
        if powerflow.method == 'CPF':
            # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
            for key, value in powerflow.case.items():
                if key == 0:
                    casekeymin = key
                    casevalmin = mn(abs(value['eigenvalues-QV']))
                
                elif (key > 0) and (mn(value['corr']['eigenvalues-QV']) < casevalmin) and (mn(value['corr']['eigenvalues-QV'] > 0)):
                    casekeymin = key
                    casevalmin = mn(abs(value['corr']['eigenvalues-QV']))
            
            # Loop
            for busname,_ in powerflow.setup.qlimkeys.items():
                # Variáveis
                busidx = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['nome'] == busname].tolist()[0]

                qmax = powerflow.setup.dbarraDF.loc[powerflow.setup.dbarraDF['nome'] == busname, 'potencia_reativa_maxima'].values[0]
                qmin = powerflow.setup.dbarraDF.loc[powerflow.setup.dbarraDF['nome'] == busname, 'potencia_reativa_minima'].values[0]
                vesp = powerflow.setup.dbarraDF.loc[powerflow.setup.dbarraDF['nome'] == busname, 'tensao'].values[0] * 1E-3
                
                ch1space = linspace(start=(qmax - (powerflow.setup.TEPRlimq * 1E1)), stop=(qmax + (powerflow.setup.TEPRlimq * 1E1)), num=10000, endpoint=True)
                ch1value = 1 / (1 + npexp(-powerflow.setup.qliminc * (ch1space - qmax + powerflow.setup.TEPRlimq)))

                ch2space = linspace(start=(qmin - (powerflow.setup.TEPRlimq * 1E1)), stop=(qmin + (powerflow.setup.TEPRlimq * 1E1)), num=10000, endpoint=True)
                ch2value = 1 / (1 + npexp(powerflow.setup.qliminc * (ch2space - qmin - powerflow.setup.TEPRlimq)))

                chvspace = linspace(start=(vesp - (powerflow.setup.TEPRlimv * 1E1)), stop=(vesp + (powerflow.setup.TEPRlimv * 1E1)), num=10000, endpoint=True)
                ch3value = 1 / (1 + npexp(powerflow.setup.qliminc * (chvspace - vesp - powerflow.setup.TEPRlimv)))
                ch4value = 1 / (1 + npexp(-powerflow.setup.qliminc * (chvspace - vesp + powerflow.setup.TEPRlimv)))

                caseitems = powerflow.setup.qlimkeys[busname][casekeymin - 1]
                smooth1 = [item[0] for item in caseitems][-1]
                smooth2 = [item[1] for item in caseitems][-1]
                smooth3 = [item[2] for item in caseitems][-1]
                smooth4 = [item[3] for item in caseitems][-1]

                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
                # fig.tight_layout()
                fig.suptitle(f"Caso {casekeymin}")

                # smooth1
                ax1.hlines(y=0., xmin=(qmax - 0.5), xmax=(qmax + 1E-2), color=(0., 0., 0.,))
                ax1.vlines(x=qmax, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax1.hlines(y=1., xmin=(qmax - 1E-2), xmax=(qmax + 0.5), color=(0., 0., 0.,))
                ax1.plot(ch1space, ch1value, color='tab:blue', alpha=0.75,)
                ax1.scatter(powerflow.case[casekeymin]['corr']['reactive'][busidx], smooth1, color='tab:blue', marker='o', s=50, alpha=0.75,)
                ax1.set_title('Chave 1 - Mvar máximo', fontsize=8)

                # smooth2
                ax2.hlines(y=1., xmin=(qmin - 0.5), xmax=(qmin + 1E-2), color=(0., 0., 0.,))
                ax2.vlines(x=qmin, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax2.hlines(y=0., xmin=(qmin - 1E-2), xmax=(qmin + 0.5), color=(0., 0., 0.,))
                ax2.plot(ch2space, ch2value, color='tab:orange', alpha=0.75,)
                ax2.scatter(powerflow.case[casekeymin]['corr']['reactive'][busidx], smooth2, color='tab:orange', marker='o', s=50, alpha=0.75,)
                ax2.set_title('Chave 2 - Mvar mínimo', fontsize=8)

                # smooth3
                ax3.hlines(y=1., xmin=(vesp - 0.5), xmax=(vesp + 1E-2), color=(0., 0., 0.,))
                ax3.vlines(x=vesp, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax3.hlines(y=0., xmin=(vesp - 1E-2), xmax=(vesp + 0.5), color=(0., 0., 0.,))
                ax3.plot(chvspace, ch3value, color='tab:green', alpha=0.75,)
                ax3.scatter(powerflow.case[casekeymin]['corr']['voltage'][busidx], smooth3, color='tab:green', marker='o', s=50, alpha=0.75,)
                ax3.set_title('Chave 3 - Volt máximo', fontsize=8)

                # smooth4
                ax4.hlines(y=0., xmin=(vesp - 0.5), xmax=(vesp + 1E-2), color=(0., 0., 0.,))
                ax4.vlines(x=vesp, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax4.hlines(y=1., xmin=(vesp - 1E-2), xmax=(vesp + 0.5), color=(0., 0., 0.,))
                ax4.plot(chvspace, ch4value, color='tab:red', alpha=0.75,)
                ax4.scatter(powerflow.case[casekeymin]['corr']['voltage'][busidx], smooth4, color='tab:red', marker='o', s=50, alpha=0.75,)
                ax4.set_title('Chave 4 - Volt mínimo', fontsize=8)

                fig.savefig(powerflow.setup.dirsmoothsys + 'smooth-' + busname + '.png', dpi=400)
                plt.close(fig)



    def svcstorage(
        self,
        powerflow,
    ):
        """armazenamento e geração de imagens referente a comutação das chaves

        Parâmetros:
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Criação automática de diretório
        Folder(powerflow.setup,).smooth(powerflow, powerflow.setup,)

        # Condição de método
        if (powerflow.method == 'CPF'):
            # índice para o caso do fluxo de potência continuado para o mínimo valor de determinante da matriz de sensibilidade
            for key, value in powerflow.case.items():
                if key == 0:
                    casekeymin = key
                    casevalmin = mn(abs(value['eigenvalues-QV']))
                
                elif (key > 0) and (mn(value['corr']['eigenvalues-QV']) < casevalmin) and (mn(value['corr']['eigenvalues-QV'] > 0)):
                    casekeymin = key
                    casevalmin = mn(abs(value['corr']['eigenvalues-QV']))
            
            powerflow.setup.casekeymin = deepcopy(casekeymin)

            # Loop
            for busname,_ in powerflow.setup.svckeys.items():
                # Variáveis
                busidx = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['nome'] == busname].tolist()[0]
                busidxcer = powerflow.setup.dcerDF.index[powerflow.setup.dcerDF['barra'] == powerflow.setup.dbarraDF['numero'].iloc[busidx]].tolist()[0]
                ctrlbusidxcer = powerflow.setup.dbarraDF.index[powerflow.setup.dbarraDF['numero'] == powerflow.setup.dcerDF['barra_controlada'].iloc[busidxcer]].tolist()[0]
                
                bmax = powerflow.setup.dcerDF['potencia_reativa_maxima'].iloc[busidxcer]
                bmin = powerflow.setup.dcerDF['potencia_reativa_minima'].iloc[busidxcer]
                vk = powerflow.sol['voltage'][busidx]
                vmref = powerflow.setup.dbarraDF['tensao'].iloc[ctrlbusidxcer] * 1E-3
                droop = powerflow.setup.dcerDF['droop'].iloc[busidxcer] * 1E-2
                
                vmmax = vmref + (droop * bmin * (vk ** 2))
                vmmin = vmref + (droop * bmax * (vk ** 2))
                
                ch1space = linspace(start=(vmmax - (powerflow.setup.tolsvcv * 1E1)), stop=(vmmax + (powerflow.setup.tolsvcv * 1E1)), num=10000, endpoint=True)
                ch1value = 1 / (1 + npexp(-powerflow.setup.svcinc * (ch1space - vmmax + powerflow.setup.tolsvcv)))

                ch2space = linspace(start=(vmmin - (powerflow.setup.tolsvcv * 1E1)), stop=(vmmin + (powerflow.setup.tolsvcv * 1E1)), num=10000, endpoint=True)
                ch2value = 1 / (1 + npexp(powerflow.setup.svcinc * (ch2space - vmmin - powerflow.setup.tolsvcv)))

                caseitems = powerflow.setup.svckeys[busname][casekeymin - 1]
                smooth1 = [item[0] for item in caseitems][-1]
                smooth2 = [item[1] for item in caseitems][-1]
                
                fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)
                fig.suptitle(f"Caso {casekeymin}")

                # smooth1
                ax1.hlines(y=0., xmin=(vmmax - 0.5), xmax=(vmmax + 1E-2), color=(0., 0., 0.,))
                ax1.vlines(x=vmmax, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax1.hlines(y=1., xmin=(vmmax - 1E-2), xmax=(vmmax + 0.5), color=(0., 0., 0.,))
                ax1.plot(ch1space, ch1value, color='tab:blue', alpha=0.75,)
                ax1.scatter(powerflow.case[casekeymin]['corr']['voltage'][ctrlbusidxcer], smooth1, color='tab:blue', marker='o', s=50, alpha=0.75,)
                ax1.set_title('Chave 1 - V máximo', fontsize=8)

                # smooth2
                ax2.hlines(y=1., xmin=(vmmin - 0.5), xmax=(vmmin + 1E-2), color=(0., 0., 0.,))
                ax2.vlines(x=vmmin, ymin=0., ymax=1., color=(0., 0., 0.,))
                ax2.hlines(y=0., xmin=(vmmin - 1E-2), xmax=(vmmin + 0.5), color=(0., 0., 0.,))
                ax2.plot(ch2space, ch2value, color='tab:orange', alpha=0.75,)
                ax2.scatter(powerflow.case[casekeymin]['corr']['voltage'][ctrlbusidxcer], smooth2, color='tab:orange', marker='o', s=50, alpha=0.75,)
                ax2.set_title('Chave 2 - V mínimo', fontsize=8)

                fig.savefig(powerflow.setup.dirsmoothsys + 'smooth-' + busname + '.png', dpi=400)
                plt.close(fig)