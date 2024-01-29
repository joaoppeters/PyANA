# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, isreal, pi, roots, zeros
from scipy.sparse import csc_matrix, hstack, vstack
from sympy import Symbol
from sympy.functions import sin

from calc import PQCalc
from smooth import Smooth


class SVCs:
    """classe para tratamento de compensadores estáticos de potência reativa"""

    def svcsol(
        self,
        powerflow,
    ):
        """variável de estado adicional para o problema de fluxo de potência

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Variáveis
        if 'svc_reactive_generation' not in powerflow.solution:
            if powerflow.setup.dcerDF['controle'][0] == 'A':
                powerflow.solution['svc_reactive_generation'] = powerflow.setup.dcerDF[
                    "potencia_reativa"
                ].to_numpy()
                self.alphavar(
                    powerflow,
                )

            elif powerflow.setup.dcerDF['controle'][0] == 'I':
                powerflow.solution['svc_current_injection'] = powerflow.setup.dcerDF[
                    "potencia_reativa"
                ].to_numpy()

            elif powerflow.setup.dcerDF['controle'][0] == 'P':
                powerflow.solution['svc_reactive_generation'] = powerflow.setup.dcerDF[
                    "potencia_reativa"
                ].to_numpy()

    def alphavar(
        self,
        powerflow,
    ):
        """calculo dos parametros para metodologia alpha do compensador estatico de potencia reativa

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        powerflow.setup.alphaxc = (powerflow.setup.options['BASE']) / (
            powerflow.setup.dcerDF['potencia_reativa_maxima'][0]
        )
        powerflow.setup.alphaxl = (
            (powerflow.setup.options['BASE'])
            / (powerflow.setup.dcerDF['potencia_reativa_maxima'][0])
        ) / (
            1
            - (powerflow.setup.dcerDF['potencia_reativa_minima'][0])
            / (powerflow.setup.dcerDF['potencia_reativa_maxima'][0])
        )
        powerflow.solution['alpha'] = roots(
            [
                (8 / 1856156927625),
                0,
                (-4 / 10854718875),
                0,
                (16 / 638512875),
                0,
                (-8 / 6081075),
                0,
                (8 / 155925),
                0,
                (-4 / 2835),
                0,
                (8 / 315),
                0,
                (-4 / 15),
                0,
                (4 / 3),
                0,
                0,
                -(2 * pi) + ((powerflow.setup.alphaxl * pi) / powerflow.setup.alphaxc),
            ]
        )
        powerflow.solution['alpha'] = powerflow.solution['alpha'][
            isreal(powerflow.solution['alpha'])
        ][0].real
        powerflow.solution['alpha0'] = deepcopy(powerflow.solution['alpha'])

        # Variáveis Simbólicas
        global alpha
        alpha = Symbol("alpha")
        powerflow.setup.alphabeq = -(
            (powerflow.setup.alphaxc / pi) * (2 * (pi - alpha) + sin(2 * alpha))
            - powerflow.setup.alphaxl
        ) / (powerflow.setup.alphaxc * powerflow.setup.alphaxl)

        # Potência Reativa
        idxcer = powerflow.setup.dbarraDF.index[
            powerflow.setup.dbarraDF['numero'] == powerflow.setup.dcerDF['barra'][0]
        ].tolist()[0]
        powerflow.solution['svc_reactive_generation'][0] = (
            powerflow.solution['voltage'][idxcer] ** 2
        ) * powerflow.setup.alphabeq.subs(alpha, powerflow.solution['alpha'])

    def svcres(
        self,
        powerflow,
        case,
    ):
        """cálculo de resíduos das equações de controle adicionais

        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: caso analisado do fluxo de potência continuado (prev + corr)
        """

        ## Inicialização
        # Vetor de resíduos
        powerflow.setup.deltaSVC = zeros([powerflow.setup.ncer])

        # Contador
        ncer = 0

        # Loop
        for _, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra']
            ].tolist()[0]
            idxctrl = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra_controlada']
            ].tolist()[0]

            if value['controle'] == 'A':
                Smooth().svcalphasmooth(
                    idxcer,
                    idxctrl,
                    powerflow,
                    ncer,
                    case,
                )
                powerflow.deltaQ[idxcer] = (
                    deepcopy(powerflow.solution['svc_reactive_generation'][ncer])
                    / powerflow.setup.options['BASE']
                )

            elif value['controle'] == 'I':
                Smooth().svccurrentsmooth(
                    idxcer,
                    idxctrl,
                    powerflow,
                    ncer,
                    case,
                )
                powerflow.deltaQ[idxcer] = (
                    deepcopy(powerflow.solution['svc_current_injection'][ncer])
                    * powerflow.solution['voltage'][idxcer]
                    / powerflow.setup.options['BASE']
                )

            elif value['controle'] == 'P':
                Smooth().svcreactivesmooth(
                    idxcer,
                    idxctrl,
                    powerflow,
                    ncer,
                    case,
                )
                powerflow.deltaQ[idxcer] = (
                    deepcopy(powerflow.solution['svc_reactive_generation'][ncer])
                    / powerflow.setup.options['BASE']
                )

            powerflow.deltaQ[idxcer] -= (
                powerflow.setup.dbarraDF['demanda_reativa'][idxcer]
                / powerflow.setup.options['BASE']
            )
            powerflow.deltaQ[idxcer] -= PQCalc().qcalc(
                powerflow,
                idxcer,
            )

            # Incrementa contador
            ncer += 1

        # Resíduo de equação de controle
        powerflow.deltaY = append(
            powerflow.deltaY, powerflow.setup.deltaSVC
        )

    def svcsubjac(
        self,
        powerflow,
    ):
        """submatrizes da matriz jacobiana

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        #
        # jacobiana:
        #
        #   H     N   px
        #   M     L   qx
        #  yt    yv   yx
        #

        # Dimensão da matriz Jacobiana
        powerflow.setup.dimpresvc = deepcopy(powerflow.jacob.shape[0])

        # Submatrizes
        powerflow.setup.px = zeros([powerflow.setup.nbus, powerflow.setup.ncer])
        powerflow.setup.qx = zeros([powerflow.setup.nbus, powerflow.setup.ncer])
        powerflow.setup.yx = zeros([powerflow.setup.ncer, powerflow.setup.ncer])
        powerflow.setup.yt = zeros([powerflow.setup.ncer, powerflow.setup.nbus])
        powerflow.setup.yv = zeros([powerflow.setup.ncer, powerflow.setup.nbus])

        # Contador
        ncer = 0

        # Submatrizes PXP QXP YQV YXT
        for idx, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra']
            ].tolist()[0]
            idxctrl = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra_controlada']
            ].tolist()[0]

            if value['barra'] != value['barra_controlada']:
                # Derivada Vk
                powerflow.setup.yv[ncer, idxcer] = powerflow.setup.diffsvc[idxcer][0]

                # Derivada Vm
                powerflow.setup.yv[ncer, idxctrl] = powerflow.setup.diffsvc[idxcer][1]

            elif value['barra'] == value['barra_controlada']:
                # Derivada Vk + Vm
                powerflow.setup.yv[ncer, idxcer] = (
                    powerflow.setup.diffsvc[idxcer][0]
                    + powerflow.setup.diffsvc[idxcer][1]
                )

            # Derivada Equação de Controle Adicional por Variável de Estado Adicional
            powerflow.setup.yx[ncer, ncer] = powerflow.setup.diffsvc[idxcer][2]

            # Derivada Qk
            if value['controle'] == 'A':
                powerflow.jacob[
                    powerflow.setup.nbus + idxcer, powerflow.setup.nbus + idxcer
                ] -= (
                    2
                    * powerflow.solution['voltage'][idxcer]
                    * float(
                        powerflow.setup.alphabeq.subs(
                            alpha, powerflow.solution['alpha']
                        )
                    )
                )
                powerflow.setup.qx[idxcer, ncer] = -(
                    powerflow.solution['voltage'][idxcer] ** 2
                ) * float(
                    powerflow.setup.alphabeq.diff(alpha).subs(
                        alpha, powerflow.solution['alpha']
                    )
                )

            elif value['controle'] == 'I':
                powerflow.jacob[
                    powerflow.setup.nbus + idxcer, powerflow.setup.nbus + idxcer
                ] -= (
                    powerflow.solution['svc_current_injection'][ncer]
                ) / powerflow.setup.options[
                    "BASE"
                ]
                powerflow.setup.qx[idxcer, ncer] = -powerflow.solution['voltage'][
                    idxcer
                ]

            elif value['controle'] == 'P':
                powerflow.setup.qx[idxcer, ncer] = -1

            # Incrementa contador
            ncer += 1

        ## Montagem Jacobiana
        # Condição
        if powerflow.setup.controldim != 0:
            powerflow.setup.extrarow = zeros(
                [powerflow.setup.nger, powerflow.setup.controldim]
            )
            powerflow.setup.extracol = zeros(
                [powerflow.setup.controldim, powerflow.setup.nger]
            )

            ytv = csc_matrix(
                concatenate(
                    (powerflow.setup.yt, powerflow.setup.yv, powerflow.setup.extrarow),
                    axis=1,
                )
            )
            pqyx = csc_matrix(
                concatenate(
                    (
                        powerflow.setup.px,
                        powerflow.setup.qx,
                        powerflow.setup.extracol,
                        powerflow.setup.yx,
                    ),
                    axis=0,
                )
            )

        elif powerflow.setup.controldim == 0:
            ytv = csc_matrix(
                concatenate((powerflow.setup.yt, powerflow.setup.yv), axis=1)
            )
            pqyx = csc_matrix(
                concatenate(
                    (powerflow.setup.px, powerflow.setup.qx, powerflow.setup.yx), axis=0
                )
            )

        powerflow.jacob = vstack([powerflow.jacob, ytv], format="csc")
        powerflow.jacob = hstack([powerflow.jacob, pqyx], format="csc")

    def svcupdt(
        self,
        powerflow,
    ):
        """atualização das variáveis de estado adicionais

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Contador
        ncer = 0

        # Atualização da potência reativa gerada
        for idx, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra']
            ].tolist()[0]

            if value['controle'] == 'A':
                powerflow.solution['alpha'] += powerflow.setup.statevar[
                    (powerflow.setup.dimpresvc + ncer)
                ]

            elif value['controle'] == 'I':
                powerflow.solution['svc_current_injection'][ncer] += (
                    powerflow.setup.statevar[(powerflow.setup.dimpresvc + ncer)]
                    * powerflow.setup.options['BASE']
                )

            elif value['controle'] == 'P':
                powerflow.solution['svc_reactive_generation'][ncer] += (
                    powerflow.setup.statevar[(powerflow.setup.dimpresvc + ncer)]
                    * powerflow.setup.options['BASE']
                )

            # Incrementa contador
            ncer += 1

        # self.svcsch(powerflow,)

    def svcsch(
        self,
        powerflow,
    ):
        """atualização do valor de potência reativa especificada

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Atualização da potência reativa especificada
        ncer = 0
        for idx, value in powerflow.setup.dcerDF.iterrows():
            idxcer = powerflow.setup.dbarraDF.index[
                powerflow.setup.dbarraDF['numero'] == value['barra']
            ].tolist()[0]
            if (powerflow.setup.dcerDF['controle'][0] == 'A') or (
                powerflow.setup.dcerDF['controle'][0] == 'P'
            ):
                powerflow.pqsch['potencia_reativa_especificada'][idxcer] += (
                    powerflow.solution['svc_reactive_generation'][ncer]
                    / powerflow.setup.options['BASE']
                )

            elif powerflow.setup.dcerDF['controle'][0] == 'I':
                powerflow.pqsch['potencia_reativa_especificada'][idxcer] += (
                    powerflow.solution['svc_current_injection'][ncer]
                    * powerflow.solution['voltage'][idxcer]
                ) / powerflow.setup.options['BASE']

            # Incrementa contador
            ncer += 1

    def svccorr(
        self,
        powerflow,
        case,
    ):
        """atualização dos valores de potência reativa gerada para a etapa de correção do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: etapa do fluxo de potência continuado analisada
        """

        ## Inicialização
        # Variável
        powerflow.solution['svc_reactive_generation'] = deepcopy(
            powerflow.case[case]['p']['svc_reactive_generation']
        )

    def svcheur(
        self,
        powerflow,
    ):
        """heurísticas aplicadas ao tratamento de limites de geração de potência reativa no problema do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        # Condição de atingimento do ponto de máximo carregamento ou bifurcação LIB
        if (
            (not powerflow.cpfsolution['pmc'])
            and (powerflow.cpfsolution['varstep'] == "lambda")
            and (
                (
                    powerflow.setup.options['LMBD']
                    * (5e-1 ** powerflow.cpfsolution['div'])
                )
                <= powerflow.setup.options['icmn']
            )
        ):
            powerflow.setup.bifurcation = True

    def svcpop(
        self,
        powerflow,
        pop: int = 1,
    ):
        """deleta última instância salva em variável de controle caso sistema divergente ou atuação de heurísticas
                atua diretamente na variável de controle associada à opção de controle SVCs

        Parâmetros
            powerflow: self do arquivo powerflow.py
            pop: quantidade de ações necessárias
        """

        ## Inicialização
        Smooth().svcpop(
            powerflow,
            pop=pop,
        )

    def svccpf(
        self,
        powerflow,
    ):
        """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
        """

        ## Inicialização
        powerflow.cpfsolution['svc_reactive_generation'] = deepcopy(
            powerflow.solution['svc_reactive_generation']
        )

    def svcsolcpf(
        self,
        powerflow,
        case,
    ):
        """armazenamento das variáveis de controle presentes na solução do fluxo de potência continuado

        Parâmetros
            powerflow: self do arquivo powerflow.py
            case: etapa do fluxo de potência continuado analisada
        """

        ## Inicialização
        # Condição
        precase = case - 1
        if case == 1:
            powerflow.solution['svc_reactive_generation'] = deepcopy(
                powerflow.case[precase]['svc_reactive_generation']
            )

        elif case > 1:
            powerflow.solution['svc_reactive_generation'] = deepcopy(
                powerflow.case[precase]['p']['svc_reactive_generation']
            )
