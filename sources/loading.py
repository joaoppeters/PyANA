# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import append, around, array, degrees, sum

from folder import Folder

class Loading:
    """classe para geração e armazenamento automático de gráficos da solução do fluxo de potência continuado"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Criação automática de diretório
        Folder(powerflow.setup,).continuation(powerflow.setup,)

        # Variáveis para geração dos gráficos de fluxo de potência continuado
        self.var(powerflow,)

        # Gráficos de variáveis de estado e controle em função do carregamento
        self.pqvt(powerflow,)

        # Gráfico de rootlocus
        self.ruthe(powerflow,)



    def var(
        self,
        powerflow,
    ):
        """variáveis para geração dos gráficos de fluxo de potência continuado
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variável
        powerflow.setup.pqtv = {}
        powerflow.setup.mw = array([])
        powerflow.setup.eigenvalues = array([])
        # powerflow.setup.det = array([])
        
        # Loop de Inicialização da Variável
        for _, value in powerflow.setup.dbarraDF.iterrows():
            if value['tipo'] != 0:
                # Variável de Armazenamento de Potência Ativa
                powerflow.setup.pqtv['P-' + value['nome']] = array([])
                
                # Variável de Armazenamento de Potência Reativa
                powerflow.setup.pqtv['Q-' + value['nome']] = array([])
                
            # Variável de Armazenamento de Magnitude de Tensão Corrigida
            powerflow.setup.pqtv['Vcorr-' + value['nome']] = array([])

            # Variável de Armazenamento de Defasagem Angular Corrigida
            powerflow.setup.pqtv['Tcorr-' + value['nome']] = array([])

        # Loop de Armazenamento
        for key, item in powerflow.case.items():
            # Condição
            if key == 0:
                self.aux = powerflow.setup.dbarraDF['nome'][0] # usado no loop seguinte
                for value in range(0, item['voltage'].shape[0]):
                    if powerflow.setup.dbarraDF['tipo'][value] != 0:
                        # Armazenamento de Potência Ativa
                        powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]], around(item['active'][value], decimals=4))

                        # Armazenamento de Potência Reativa
                        powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]], around(item['reactive'][value], decimals=4))
                    
                    # Armazenamento de Magnitude de Tensão
                    powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]], around(item['voltage'][value], decimals=4))

                    # Variável de Armazenamento de Defasagem Angular
                    powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]], around(degrees(item['theta'][value]), decimals=4))

                # Demanda
                powerflow.setup.mw = append(powerflow.setup.mw, around(sum(powerflow.cpfsol['demanda_ativa']), decimals=4))
                
                # Determinante e Autovalores
                powerflow.setup.eigenvalues = append(powerflow.setup.eigenvalues, item['eigenvalues'])
                # powerflow.setup.det = append(powerflow.setup.det, item['determinant'])

            elif key != 0 and key != list(powerflow.case.keys())[-1]:
                for value in range(0, item['corr']['voltage'].shape[0]):
                    if powerflow.setup.dbarraDF['tipo'][value] != 0:
                        # Armazenamento de Potência Ativa
                        powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]], around(item['corr']['active'][value], decimals=4))

                        # Armazenamento de Potência Reativa
                        powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]], around(item['corr']['reactive'][value], decimals=4))
                    
                    # Armazenamento de Magnitude de Tensão Corrigida
                    powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]], around(item['corr']['voltage'][value], decimals=4))

                    # Variável de Armazenamento de Defasagem Angular Corrigida
                    powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]], around(degrees(item['corr']['theta'][value]), decimals=4))

                # Demanda
                powerflow.setup.mw = append(powerflow.setup.mw, around(((1 + item['corr']['step']) * sum(powerflow.cpfsol['demanda_ativa'])), decimals=4))

                # Determinante e Autovalores
                powerflow.setup.eigenvalues = append(powerflow.setup.eigenvalues, item['corr']['eigenvalues'])
                # powerflow.setup.det = append(powerflow.setup.det, item['corr']['determinant'])



    def pqvt(
        self,
        powerflow,
    ):
        """geração e armazenamento de gráficos de variáveis de estado e controle em função do carregamento
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Geração de Gráfico
        color = 0
        for key, item in powerflow.setup.pqtv.items():
            if key[0] != 'V' and key[0] != 'T':
                fig, ax = plt.subplots(nrows=1, ncols=1)
                
                # Variáveis
                busname = key[2:]
                if busname != self.aux:
                    self.aux = key[2:]
                    color += 1
                
                # Plot
                line, = ax.plot(powerflow.setup.mw, item, color=f'C{color}', linewidth=2, alpha=0.85, zorder=2)
                
                # Labels
                # Condição de Potência Ativa
                if key[0] == 'P':
                    ax.set_title('Variação da Geração de Potência Ativa')
                    ax.set_ylabel('Geração de Potência Ativa [MW]')
                    ax.legend([line], [busname])
                
                # Condição de Potência Reativa
                elif key[0] == 'Q':
                    ax.set_title('Variação da Geração de Potência Reativa')
                    ax.set_ylabel('Geração de Potência Reativa [Mvar]')
                    ax.legend([line], [busname])

                ax.set_xlabel('Carregamento [MW]')
                ax.grid()

                
            elif (key[0] == 'V' and key[:5] != 'Vprev') or (key[0] == 'T' and key[:5] != 'Tprev'):
                fig, ax = plt.subplots(nrows=1, ncols=1)

                # Variáveis
                busname = key[6:]
                if busname != self.aux:
                    self.aux = key[6:]
                    color += 1
                
                # Plots
                line, = ax.plot(powerflow.setup.mw[:powerflow.setup.pmcidx], item[:powerflow.setup.pmcidx], color=f'C{color}', linestyle='solid', linewidth=2, alpha=0.85, label=busname, zorder=2)
                
                if powerflow.setup.options['full']:
                    dashed, = ax.plot(powerflow.setup.mw[(powerflow.setup.pmcidx):(powerflow.setup.v2lidx)], item[(powerflow.setup.pmcidx):(powerflow.setup.v2lidx)], color=f'C{color}', linestyle='dashed', linewidth=2, alpha=0.85, label=busname, zorder=2)
                    dotted, = ax.plot(powerflow.setup.mw[powerflow.setup.v2lidx:], item[powerflow.setup.v2lidx:], color=f'C{color}', linestyle='dotted', linewidth=2, alpha=0.85, label=busname, zorder=2)
                    ax.legend([(line, dashed, dotted)], [busname])
                
                elif not powerflow.setup.options['full']:
                    ax.legend([(line,   )], [busname])
                        
                # Labels
                if key[0] == 'V':
                    ax.set_title('Variação da Magnitude de Tensão do Barramento')
                    ax.set_ylabel('Magnitude de Tensão do Barramento [p.u.]')

                elif key[0] == 'T':
                    ax.set_title('Variação da Defasagem Angular do Barramento')
                    ax.set_ylabel('Defasagem Angular do Barramento [graus]')

                ax.set_xlabel('Carregamento [MW]')
                ax.grid()

            # Save
            fig.savefig(powerflow.setup.dircpfsysimag + key[0] + '-' + busname + '.png', dpi=400)
            plt.close(fig)



    def ruthe(
        self,
        powerflow,
    ):
        """geração e armazenamento de gráfico rootlocus
        
        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis
        rows = list(powerflow.case.keys())[-1]
        cols = len(powerflow.case[0]['eigenvalues'])

        # Reconfiguração
        powerflow.setup.eigenvalues = powerflow.setup.eigenvalues.reshape(rows, cols).T.astype(dtype=complex)

        # Geração de Gráfico
        fig, ax = plt.subplots(nrows=1, ncols=1)
        color = 0
        for eigen in range(0, cols):
            ax.scatter(-powerflow.setup.eigenvalues.real[eigen, 0], powerflow.setup.eigenvalues.imag[eigen, 0], color=f'C{color}', marker='x', alpha=1, zorder=3)
            ax.plot(-powerflow.setup.eigenvalues.real[eigen, :], powerflow.setup.eigenvalues.imag[eigen, :], color=f'C{color}', linewidth=2, alpha=0.85, zorder=2)
            color += 1
        
        ax.axhline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)
        ax.axvline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)

        ax.set_title('Autovalores no Fluxo de Potência Continuado')
        ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
        ax.set_xlabel(f'Eixo Real ($\sigma$)')

        # Save
        fig.savefig(powerflow.setup.dircpfsys + powerflow.setup.name + '-rootlocus.png', dpi=400)
        plt.close(fig)