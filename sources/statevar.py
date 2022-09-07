# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import arange, degrees, linspace, max, min, ones, pi

from folder import Folder

class StateVarProfile:
    """classe para geração dos resultados finais de convergência das variáveis de estado"""

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
        Folder(setup,).statevar(setup,)

        # Resultado final de convergência das magnitudes e ângulos de tensão
        self.stateVT(powerflow,)

        # # Resultado final de convergência dos ângulos de tensão
        # self.stateT(powerflow,)
        
        # Condição
        if powerflow.setup.control:
            # Resultado final de convergência das variáveis de estado adicionais
            self.stateY(powerflow,)



    def stateVT(
        self,
        powerflow,
    ):
        """resultado final de convergência das magnitudes e ângulos de tensão
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': 'polar'}, figsize=(8,9))

        # Referência
        self.thetaref = powerflow.sol['theta'][powerflow.setup.dbarraDF.loc[powerflow.setup.dbarraDF['tipo'] == 2].index[0]]
        
        # Plots 
        colors = plt.cm.viridis(arange(powerflow.setup.nbus)/powerflow.setup.nbus)
        bars = ax.bar(powerflow.sol['theta'], powerflow.sol['voltage'], width=0.005, bottom=0., color=colors, alpha=0.5, zorder=3,)
        ax.plot(linspace(0, 2 * pi, 360, endpoint=False,), ones(360), linestyle='--', color=(0., 0., 0.), alpha=1., zorder=2,)
        for theta, rotation, label in zip(powerflow.sol['theta'], degrees(powerflow.sol['theta']), powerflow.setup.dbarraDF['nome'].values):
            ax.text(theta, ax.get_ylim()[1] + 0.075, label, ha='left', va='center', rotation=rotation-degrees(self.thetaref), rotation_mode='anchor', fontsize=5)

        # Label
        ax.set_title('Magnitude e Ângulo de Tensão dos Barramentos')
        ax.set_thetamax(max(degrees(powerflow.sol['theta'])) + 5)
        ax.set_thetamin(min(degrees(powerflow.sol['theta'])) - 5)
        ax.set_rticks([1.,])
        ax.set_yticklabels({'1 p.u.'})
        ax.legend(bars, powerflow.setup.dbarraDF['nome'].values.tolist(), frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=int(5), prop={'size': 7})
        ax.set_theta_offset(-self.thetaref)
        

        
        # Save
        fig.savefig(powerflow.setup.dirRstatevar + powerflow.setup.name + '-stateVT.png')


    # def stateT(
    #     self,
    #     powerflow,
    # ):
    #     """resultado final de convergência dos ângulos de tensão
        
    #     Parâmetros
    #         powerflow: self do arquivo powerflow.py
    #     """

    #     ## Inicialização
    #     fig, ax = plt.subplots(nrows=1, ncols=1)
        
    #     # Plots 
    #     line, = ax.plot(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color='C0', linewidth=2, alpha=0.85, zorder=2)
    #     mark = ax.scatter(arange(0, powerflow.sol['iter'] + 1), (powerflow.sol['convQ'] * powerflow.setup.options['sbase']), color='C5', marker='*', alpha=0.85, s=75, zorder=3)

    #     # Label
    #     ax.set_title('Trajetória de Convergência de Potência Reativa')
    #     ax.set_xlabel('Iterações')
    #     ax.set_xticks(arange(0, powerflow.sol['iter'] + 1))
    #     ax.set_ylabel('Resíduo de Potência Reativa [Mvar]')
    #     ax.legend([(line, mark,)], [f'abs(max($\Delta$Q))'])
    #     ax.grid()

    #     # Save
    #     fig.savefig(powerflow.setup.dirRconvergence + powerflow.setup.name + '-trajconv-deltaQ.png')



    def stateY(
        self,
        powerflow,
    ):
        """resultado final de convergência das variáveis de estado adicionais
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        pass