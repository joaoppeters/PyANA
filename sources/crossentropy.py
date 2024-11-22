# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from fastcontinuation import FastContinuation
from newton import newton

from numpy import array, random, sqrt, zeros


class CrossEntropy:
    """classe para aplicação de estocasticidade cross-entropy"""

    def __init__(
        self,
        powerflow,
    ):
        """inicialização

        Args
            powerflow:
        """

        ## Inicialização
        # Newton-Raphson
        newton(
            powerflow,
        )

        # CrossEntropy
        self.cent(
            powerflow,
        )

    def cent(
        self,
        powerflow,
    ):
        """
        Args
            powerflow:
        """

        ## Inicialização
        # População Inicial
        self.PA = zeros(powerflow.setting.narea)
        self.mean = zeros(powerflow.setting.narea)
        self.stdd = zeros(powerflow.setting.narea)
        a = 0
        for area in powerflow.setting.areas:
            self.PA[a] = powerflow.setting.dbarDF.loc[
                powerflow.setting.dbarDF["area"] == area, "demanda_ativa"
            ].sum()
            self.mean[a] = powerflow.setting.dbarDF.loc[
                powerflow.setting.dbarDF["area"] == area, "demanda_ativa"
            ].mean()
            self.stdd[a] = powerflow.setting.dbarDF.loc[
                powerflow.setting.dbarDF["area"] == area, "demanda_ativa"
            ].std()
            a += 1

        self.population(
            powerflow,
        )

    def population(
        self,
        powerflow,
    ):
        """

        Args
            powerflow:
        """

        ## Inicialização
        random.random()
        self.amostras = 50
        self.elite = 10
        self.smootht = 0.8
        self.smoothv = 0.2
        self.metlimit = 4
        self.objective = 0

        n = -1
        while self.objective < (0.8 * self.elite):
            n += 1

            # PASSO 1:  NÃO É NECESSÁRIO NA DISTRIBUIÇÃO NORMAL
            self.a = (((1 - self.mean) * (self.mean**2)) / (self.stdd**2)) - self.mean
            self.b = ((1 - self.mean) / self.mean) * self.a

            # PASSO 2: CRIAÇÃO DO VETOR DE AMOSTRAS
            self.x = zeros(shape=[powerflow.setting.narea, self.amostras])
            for j in range(0, powerflow.setting.narea):
                self.x[j, :] = self.mean[j] + sqrt(self.stdd[j]) * (
                    random.randn(self.amostras)
                )

            # PASSO 3: COMPUTAR O VALOR DE Sx PARA CADA AMOSTRA
            self.s = array([])
            for k in range(powerflow.setting.narea):
                self.s[k] = FastContinuation(
                    powerflow, (self.x[:][k] - self.PA) / self.PA
                )
