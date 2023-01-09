# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@engenharia.ufjf.br #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import append, array, degrees, sum

from folder import Folder
from smooth import Smooth

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

        # # Gráfico de rootlocus
        # self.ruthe(powerflow,)



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
        powerflow.setup.mvar = array([])
        powerflow.setup.eigenvalues = array([])
        powerflow.setup.eigenvaluesPT = array([])
        powerflow.setup.eigenvaluesQV = array([])
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
                        powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]], item['active'][value])

                        # Armazenamento de Potência Reativa
                        powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]], item['reactive'][value])
                    
                    # Armazenamento de Magnitude de Tensão
                    powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]], item['voltage'][value])

                    # Variável de Armazenamento de Defasagem Angular
                    powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]], degrees(item['theta'][value]))

                # Demanda
                powerflow.setup.mw = append(powerflow.setup.mw, sum(powerflow.cpfsol['demanda_ativa']))
                powerflow.setup.mvar = append(powerflow.setup.mvar, sum(powerflow.cpfsol['demanda_reativa']))
                
                # Determinante e Autovalores
                powerflow.setup.eigenvalues = append(powerflow.setup.eigenvalues, item['eigenvalues'])
                powerflow.setup.eigenvaluesPT = append(powerflow.setup.eigenvaluesPT, item['eigenvalues-PT'])
                powerflow.setup.eigenvaluesQV = append(powerflow.setup.eigenvaluesQV, item['eigenvalues-QV'])
                # powerflow.setup.det = append(powerflow.setup.det, item['determinant'])

            elif key > 0:
                for value in range(0, item['corr']['voltage'].shape[0]):
                    if powerflow.setup.dbarraDF['tipo'][value] != 0:
                        # Armazenamento de Potência Ativa
                        powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['P-' + powerflow.setup.dbarraDF['nome'][value]], item['corr']['active'][value])

                        # Armazenamento de Potência Reativa
                        powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Q-' + powerflow.setup.dbarraDF['nome'][value]], item['corr']['reactive'][value])
                    
                    # Armazenamento de Magnitude de Tensão Corrigida
                    powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Vcorr-' + powerflow.setup.dbarraDF['nome'][value]], item['corr']['voltage'][value])

                    # Variável de Armazenamento de Defasagem Angular Corrigida
                    powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]] = append(powerflow.setup.pqtv['Tcorr-' + powerflow.setup.dbarraDF['nome'][value]], degrees(item['corr']['theta'][value]))

                # Demanda
                totalmw = sum(powerflow.cpfsol['demanda_ativa'])
                totalmvar = sum(powerflow.cpfsol['demanda_reativa'])
                for _, valueinc in powerflow.setup.dincDF.iterrows():
                    if valueinc['tipo_incremento_1'] == 'AREA':
                        # MW
                        areamw = (1 + item['corr']['step']) * sum(array([powerflow.cpfsol['demanda_ativa'][idxarea] for idxarea, valuearea in powerflow.setup.dbarraDF.iterrows() if valuearea['area'] == valueinc['identificacao_incremento_1']]))
                        totalmw += areamw - sum(array([powerflow.cpfsol['demanda_ativa'][idxarea] for idxarea, valuearea in powerflow.setup.dbarraDF.iterrows() if valuearea['area'] == valueinc['identificacao_incremento_1']]))

                        # Mvar
                        areamvar = (1 + item['corr']['step']) * sum(array([powerflow.cpfsol['demanda_reativa'][idxarea] for idxarea, valuearea in powerflow.setup.dbarraDF.iterrows() if valuearea['area'] == valueinc['identificacao_incremento_1']]))
                        totalmvar += areamvar - sum(array([powerflow.cpfsol['demanda_reativa'][idxarea] for idxarea, valuearea in powerflow.setup.dbarraDF.iterrows() if valuearea['area'] == valueinc['identificacao_incremento_1']]))

                    elif powerflow.setup.dincDF.loc[0, 'tipo_incremento_1'] == 'BARR':
                        # MW
                        barramw = (1 + item['corr']['step']) * powerflow.cpfsol['demanda_ativa'][powerflow.setup.dincDF.loc[0, 'identificacao_incremento_1'] - 1]
                        totalmw += barramw - powerflow.cpfsol['demanda_ativa'][powerflow.setup.dincDF.loc[0, 'identificacao_incremento_1'] - 1]

                        # Mvar
                        barramvar = (1 + item['corr']['step']) * powerflow.cpfsol['demanda_reativa'][powerflow.setup.dincDF.loc[0, 'identificacao_incremento_1'] - 1]
                        totalmvar += barramvar - powerflow.cpfsol['demanda_reativa'][powerflow.setup.dincDF.loc[0, 'identificacao_incremento_1'] - 1]
                    
                powerflow.setup.mw = append(powerflow.setup.mw, totalmw)
                powerflow.setup.mvar = append(powerflow.setup.mvar, totalmvar)

                # Determinante e Autovalores
                powerflow.setup.eigenvalues = append(powerflow.setup.eigenvalues, item['corr']['eigenvalues'])
                powerflow.setup.eigenvaluesPT = append(powerflow.setup.eigenvaluesPT, item['corr']['eigenvalues-PT'])
                powerflow.setup.eigenvaluesQV = append(powerflow.setup.eigenvaluesQV, item['corr']['eigenvalues-QV'])
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
            if key[:5] != 'Vprev' and key[:5] != 'Tprev':
                fig, ax = plt.subplots(nrows=1, ncols=1)
                
                # Variáveis
                if key[1:5] == 'corr':
                    busname = key[6:]
                else:
                    busname = key[2:]
                if busname != self.aux:
                    if key[1:5] == 'corr':
                        self.aux = key[6:]
                    else:
                        self.aux = key[2:]
                    color += 1
                
                # Plot
                line, = ax.plot(powerflow.setup.mw[:powerflow.setup.pmcidx+1], item[:powerflow.setup.pmcidx+1], color=f'C{color}', linestyle='solid', linewidth=2, alpha=0.85, label=busname, zorder=2)
                
                if powerflow.setup.options['full']:
                    dashed, = ax.plot(powerflow.setup.mw[(powerflow.setup.pmcidx+1):(powerflow.setup.v2lidx)], item[(powerflow.setup.pmcidx+1):(powerflow.setup.v2lidx)], color=f'C{color}', linestyle='dashed', linewidth=2, alpha=0.85, label=busname, zorder=2)
                    dotted, = ax.plot(powerflow.setup.mw[powerflow.setup.v2lidx:], item[powerflow.setup.v2lidx:], color=f'C{color}', linestyle='dotted', linewidth=2, alpha=0.85, label=busname, zorder=2)
                    ax.legend([(line, dashed, dotted)], [busname])
                
                elif not powerflow.setup.options['full']:
                    ax.legend([(line,   )], [busname])
                
                # Labels
                # Condição de Potência Ativa
                if key[0] == 'P':
                    ax.set_title('Variação da Geração de Potência Ativa')
                    ax.set_ylabel('Geração de Potência Ativa [MW]')
                
                # Condição de Potência Reativa
                elif key[0] == 'Q':
                    ax.set_title('Variação da Geração de Potência Reativa')
                    ax.set_ylabel('Geração de Potência Reativa [Mvar]')

                # Magnitude de Tensão Nodal
                if key[0] == 'V':
                    ax.set_title('Variação da Magnitude de Tensão do Barramento')
                    ax.set_ylabel('Magnitude de Tensão do Barramento [p.u.]')

                # Defasagem Angular de Tensão Nodal
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
        cols = sum(powerflow.setup.mask)
        colsP = sum(powerflow.setup.maskP)
        colsQ = sum(powerflow.setup.maskQ)

        # Reconfiguração
        powerflow.setup.eigenvalues = powerflow.setup.eigenvalues.reshape(rows, cols).T.astype(dtype=complex)
        powerflow.setup.eigenvaluesPT = powerflow.setup.eigenvaluesPT.reshape(rows, colsP).T.astype(dtype=complex)
        powerflow.setup.eigenvaluesQV = powerflow.setup.eigenvaluesQV.reshape(rows, colsQ).T.astype(dtype=complex)

        # Geração de Gráfico - Autovalores da matriz Jacobiana Reduzida
        fig, ax = plt.subplots(nrows=1, ncols=1)
        color = 0
        for eigen in range(0, cols):
            ax.scatter(-powerflow.setup.eigenvalues.real[eigen, 0], powerflow.setup.eigenvalues.imag[eigen, 0], marker='x', color=f'C{color}', alpha=1, zorder=3)
            ax.plot(-powerflow.setup.eigenvalues.real[eigen, :], powerflow.setup.eigenvalues.imag[eigen, :], color=f'C{color}', linewidth=2, alpha=0.85, zorder=2)
            color += 1
        
        ax.axhline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)
        ax.axvline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)

        ax.set_title('Autovalores da Matriz Jacobiana Reduzida')
        ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
        ax.set_xlabel(f'Eixo Real ($\sigma$)')

        # Save
        fig.savefig(powerflow.setup.dircpfsys + powerflow.setup.name + '-rootlocus-Jacobian.png', dpi=400)
        plt.close(fig)

        # Geração de Gráfico - Autovalores da matriz de sensisbilidade PT
        fig, ax = plt.subplots(nrows=1, ncols=1)
        color = 0
        for eigen in range(0, colsP):
            ax.scatter(-powerflow.setup.eigenvaluesPT.real[eigen, 0], powerflow.setup.eigenvaluesPT.imag[eigen, 0], marker='x', color=f'C{color}', alpha=1, zorder=3)
            ax.plot(-powerflow.setup.eigenvaluesPT.real[eigen, :], powerflow.setup.eigenvaluesPT.imag[eigen, :], color=f'C{color}', linewidth=2, alpha=0.85, zorder=2)
            color += 1
        
        ax.axhline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)
        ax.axvline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)

        ax.set_title(f'Autovalores da Matriz de Sensibilidade $P\\theta$')
        ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
        ax.set_xlabel(f'Eixo Real ($\sigma$)')

        # Save
        fig.savefig(powerflow.setup.dircpfsys + powerflow.setup.name + '-rootlocus-PTsens.png', dpi=400)
        plt.close(fig)

        # Geração de Gráfico - Autovalores da matriz de sensibilidade QV
        fig, ax = plt.subplots(nrows=1, ncols=1)
        color = 0
        for eigen in range(0, colsQ):
            ax.scatter(-powerflow.setup.eigenvaluesQV.real[eigen, 0], powerflow.setup.eigenvaluesQV.imag[eigen, 0], marker='x', color=f'C{color}', alpha=1, zorder=3)
            ax.plot(-powerflow.setup.eigenvaluesQV.real[eigen, :], powerflow.setup.eigenvaluesQV.imag[eigen, :], color=f'C{color}', linewidth=2, alpha=0.85, zorder=2)
            color += 1
        
        ax.axhline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)
        ax.axvline(0., linestyle=':', color='k', linewidth=.75, zorder=-20)

        ax.set_title(f'Autovalores da Matriz de Sensibilidade $QV$')
        ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
        ax.set_xlabel(f'Eixo Real ($\sigma$)')

        # Save
        fig.savefig(powerflow.setup.dircpfsys + powerflow.setup.name + '-rootlocus-QVsens.png', dpi=400)
        plt.close(fig)