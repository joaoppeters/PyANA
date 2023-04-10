# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import arange

from folder import Folder

class Convergence:
    """classe para geração das trajetórias de convergência das variáveis de estado do fluxo de potência"""

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
        # Criação de pasta
        Folder(setup,).convergence(setup,)

        # Convergência de Potência Ativa
        self.convP(powerflow,)

        # Convergência de Potência Reativa
        self.convQ(powerflow,)
        
        # Condição
        if (powerflow.setup.control):
            # Convergência de Equações de Controle Adicionais
            self.convY(powerflow,)



    def convP(
        self,
        powerflow,
    ):
        """trajetória de convergência de equação de potência ativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        fig, ax = plt.subplots(nrows=1, ncols=1)
        
        # Plots 
        if (powerflow.sol['convergence'] == 'SISTEMA CONVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convP'] * powerflow.setup.options['sbase']), color='C0', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convP'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        elif (powerflow.sol['convergence'] == 'SISTEMA DIVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter']), (powerflow.sol['convP'] * powerflow.setup.options['sbase']), color='C0', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter']), (powerflow.sol['convP'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        # Label
        ax.set_title('Trajetória de Convergência de Potência Ativa')
        ax.set_xlabel('Iterações')
        ax.set_xticks(arange(0, powerflow.sol['iter'] + 1))
        ax.set_ylabel('Resíduo de Potência Ativa [MW]')
        ax.legend([(line, mark,)], [f'abs(max($\Delta$P))'])
        ax.grid()

        # Save
        fig.savefig(powerflow.setup.dirRconvergence + powerflow.setup.name + '-trajconv-deltaP.png', dpi=400)


    def convQ(
        self,
        powerflow,
    ):
        """trajetória de convergência de equação de potência reativa
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        fig, ax = plt.subplots(nrows=1, ncols=1)
        
        # Plots 
        if (powerflow.sol['convergence'] == 'SISTEMA CONVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color='C1', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        elif (powerflow.sol['convergence'] == 'SISTEMA DIVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter']), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color='C1', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter']), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        # Label
        ax.set_title('Trajetória de Convergência de Potência Reativa')
        ax.set_xlabel('Iterações')
        ax.set_xticks(arange(0, powerflow.sol['iter'] + 1))
        ax.set_ylabel('Resíduo de Potência Reativa [Mvar]')
        ax.legend([(line, mark,)], [f'abs(max($\Delta$Q))'])
        ax.grid()

        # Save
        fig.savefig(powerflow.setup.dirRconvergence + powerflow.setup.name + '-trajconv-deltaQ.png', dpi=400)



    def convY(
        self,
        powerflow,
    ):
        """trajetória de convergência de equações de controle adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        fig, ax = plt.subplots(nrows=1, ncols=1)
        
        # Plots 
        if (powerflow.sol['convergence'] == 'SISTEMA CONVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convY'] * powerflow.setup.options['sbase']), color='C1', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convY'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        elif (powerflow.sol['convergence'] == 'SISTEMA DIVERGENTE'):
            line, = ax.plot(arange(0, powerflow.sol['iter']), (powerflow.sol['convY'] * powerflow.setup.options['sbase']), color='C1', linewidth=2, alpha=0.85, zorder=2)
            mark = ax.scatter(arange(0, powerflow.sol['iter']), (powerflow.sol['convY'] * powerflow.setup.options['sbase']), color=(1., 1., 1.), marker='*', edgecolor=(0., 0., 0.), alpha=1., s=100, zorder=3)

        # Label
        ax.set_title('Trajetória de Convergência de Potência Reativa')
        ax.set_xlabel('Iterações')
        ax.set_xticks(arange(0, powerflow.sol['iter'] + 1))
        ax.set_ylabel('Resíduo de Variável de Controle')
        ax.legend([(line, mark,)], [f'abs(max($\Delta$Y))'])
        ax.grid()

        # Save
        fig.savefig(powerflow.setup.dirRconvergence + powerflow.setup.name + '-trajconv-deltaY.png', dpi=400)