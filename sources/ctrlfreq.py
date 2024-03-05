# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import append, concatenate, infty, radians, zeros

from calc import pcalc, qcalc


def freqsol(
    self,
    powerflow,
):
    """adiciona variáveis narea solução para caso controle de regulação primária de frequência esteja ativado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.nare = 1

    # Condição
    if (powerflow.control["FREQ"]) and (powerflow.codes["DGER"]):
        # Variáveis
        powerflow.solution["active_generation"] = zeros(powerflow.nger)
        powerflow.solution["qlim_reactive_generation"] = zeros(powerflow.nger)
        powerflow.fesp = 1

        # Loop
        nger = 0
        for idx, value in powerflow.dbarraDF.iterrows():
            # Barra tipo VT ou PV
            if value["tipo"] != 0:
                powerflow.solution["active_generation"][nger] = (
                    value["potencia_ativa"] / powerflow.options["BASE"]
                )
                powerflow.solution["qlim_reactive_generation"][nger] = (
                    value["potencia_reativa"] / powerflow.options["BASE"]
                )
                nger += 1
        # Frequências máxima e mínima por gerador
        freqgerlim(
            powerflow,
        )

    # DGER não ativado
    else:
        powerflow.control["FREQ"] = False
        print(
            "\033[93mERROR: Controle `FREQ` não será ativado por ausência de dados de barras geradoras! Atualize o campo `DGER` do arquivo `{}`!\033[0m".format(
                powerflow.system
            )
        )


def freqgerlim(
    powerflow,
):
    """cálculo das frequências máximas e mínimas de operação de cada gerador

    Parâmetros
        powerflow: self do arquivo powerflowl.py
    """

    ## Inicialização
    # Variáveis
    powerflow.freqger = {
        "max": zeros(powerflow.nger),
        "min": zeros(powerflow.nger),
    }
    powerflow.dgerorder = dict()

    # Loop
    for idx, value in powerflow.dgeraDF.iterrows():
        # Armazenamento da barra por ordem de entrada de dados dos geradores
        powerflow.dgerorder[idx] = powerflow.dbarraDF["nome"][value["numero"] - 1]
        # Frequência máxima gerador `idx`
        powerflow.freqger["max"][idx] = (
            powerflow.fesp
            + value["estatismo"]
            * 1e-2
            * (
                powerflow.dbarraDF["potencia_ativa"][value["numero"] - 1]
                - value["potencia_ativa_minima"]
            )
            / powerflow.options["BASE"]
        )
        # Frequência mínima gerador `idx`
        powerflow.freqger["min"][idx] = (
            powerflow.fesp
            + value["estatismo"]
            * 1e-2
            * (
                powerflow.dbarraDF["potencia_ativa"][value["numero"] - 1]
                - value["potencia_ativa_maxima"]
            )
            / powerflow.options["BASE"]
        )


def freqsch(
    powerflow,
):
    """armazenamento de parâmetros especificados das equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variáveis adicionais
    powerflow.pqsch["potencia_ativa_gerada_especificada"] = zeros(powerflow.nger)
    powerflow.pqsch["potencia_reativa_gerada_especificada"] = zeros(powerflow.nger)
    powerflow.pqsch["magnitude_tensao_especificada"] = zeros(powerflow.nbus)
    powerflow.pqsch["defasagem_angular_especificada"] = zeros(powerflow.nbus)

    # Contador de geradores
    nger = 0

    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 0:
            # Potência ativa gerada
            powerflow.pqsch["potencia_ativa_gerada_especificada"][nger] = value[
                "potencia_ativa"
            ]
            # Potência reativa gerada
            powerflow.pqsch["potencia_reativa_gerada_especificada"][nger] = value[
                "potencia_reativa"
            ]
            # Magnitude de tensão
            powerflow.pqsch["magnitude_tensao_especificada"][idx] = (
                value["tensao"] * 1e-3
            )
            # Condição - slack
            if value["tipo"] == 2:
                # Defasagem angular
                powerflow.pqsch["defasagem_angular_especificada"][idx] = radians(
                    value["angulo"]
                )
            # Incrementa contador
            nger += 1

    # Tratamento
    powerflow.pqsch["potencia_ativa_gerada_especificada"] /= powerflow.options["BASE"]
    powerflow.pqsch["potencia_reativa_gerada_especificada"] /= powerflow.options["BASE"]


def freqres(
    powerflow,
):
    """cálculo de resíduos das equações de controle adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetor de resíduos
    powerflow.deltaPger = zeros([powerflow.nger])
    powerflow.deltaQger = zeros([powerflow.nger])
    powerflow.deltaTger = zeros([powerflow.nare])

    # Contador
    nger = 0

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 0:
            # Cálculo do resíduo DeltaP
            powerflow.deltaP[idx] = powerflow.solution["active_generation"][nger]
            powerflow.deltaP[idx] -= value["demanda_ativa"] / powerflow.options["BASE"]
            powerflow.deltaP[idx] -= pcalc(
                powerflow,
                idx,
            )

            # Cálculo do resíduo DeltaQ
            powerflow.deltaQ[idx] = powerflow.solution["qlim_reactive_generation"][nger]
            powerflow.deltaQ[idx] -= (
                value["demanda_reativa"] / powerflow.options["BASE"]
            )
            powerflow.deltaQ[idx] -= qcalc(
                powerflow,
                idx,
            )

            # Tratamento de limite de potência ativa
            if (powerflow.solution["freq"] >= powerflow.freqger["max"][nger]) or (
                powerflow.solution["freq"] <= powerflow.freqger["min"][nger]
            ):
                powerflow.deltaPger[nger] = 0.0
            else:
                powerflow.deltaPger[nger] += powerflow.pqsch[
                    "potencia_ativa_gerada_especificada"
                ][nger]
                powerflow.deltaPger[nger] -= powerflow.solution["active_generation"][
                    nger
                ]
                powerflow.deltaPger[nger] -= (
                    1 / (powerflow.dgeraDF["estatismo"][nger] * 1e-2)
                ) * (powerflow.solution["freq"] - powerflow.fesp)

            # Tratamento de limite de magnitude de tensão
            powerflow.deltaQger[nger] += powerflow.pqsch[
                "magnitude_tensao_especificada"
            ][idx]
            powerflow.deltaQger[nger] -= powerflow.solution["voltage"][idx]

            # Condição - slack
            if value["tipo"] == 2:
                # Tratamento de limite de
                powerflow.deltaTger += powerflow.pqsch[
                    "defasagem_angular_especificada"
                ][idx]
                powerflow.deltaTger -= powerflow.solution["theta"][idx]

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaPger)
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaQger)
    powerflow.deltaY = append(powerflow.deltaY, powerflow.deltaTger)


def freqsubjac(
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
    #   H     N   pxp   pxq   pxx
    #   M     L   qxp   qxq   qxx
    # ypt   ypv   ypp   ypq   ypx
    # yqt   yqv   yqp   yqq   yqx
    # yxt   yxv   yxp   yxq   yxx
    #

    # Variável
    powerflow.dimprefreq = deepcopy(powerflow.jacobian.shape[0])

    # Condição
    if powerflow.freqjcount == 0:
        # Variável
        powerflow.freqjcount += 1

        # Submatrizes
        powerflow.pxp = zeros([powerflow.nbus, powerflow.nger])  # -> APG
        powerflow.pxq = zeros([powerflow.nbus, powerflow.nger])
        powerflow.pxx = zeros([powerflow.nbus, powerflow.nare])

        powerflow.qxp = zeros([powerflow.nbus, powerflow.nger])
        powerflow.qxq = zeros([powerflow.nbus, powerflow.nger])  # -> BQG
        powerflow.qxx = zeros([powerflow.nbus, powerflow.nare])

        powerflow.ypt = zeros([powerflow.nger, powerflow.nbus])
        powerflow.ypv = zeros([powerflow.nger, powerflow.nbus])
        powerflow.ypp = zeros([powerflow.nger, powerflow.nger])  # -> CPG
        powerflow.ypq = zeros([powerflow.nger, powerflow.nger])
        powerflow.ypx = zeros([powerflow.nger, powerflow.nare])  # -> CF

        powerflow.yqt = zeros([powerflow.nger, powerflow.nbus])
        powerflow.yqv = zeros([powerflow.nger, powerflow.nbus])  # -> EQG
        powerflow.yqp = zeros([powerflow.nger, powerflow.nger])
        powerflow.yqq = zeros([powerflow.nger, powerflow.nger])
        powerflow.yqx = zeros([powerflow.nger, powerflow.nare])

        powerflow.yxt = zeros([powerflow.nare, powerflow.nbus])  # -> FT
        powerflow.yxv = zeros([powerflow.nare, powerflow.nbus])
        powerflow.yxp = zeros([powerflow.nare, powerflow.nger])
        powerflow.yxq = zeros([powerflow.nare, powerflow.nger])
        powerflow.yxx = zeros([powerflow.nare, powerflow.nare])

        # Contadores
        nger = 0
        nare = 0

        # Submatrizes PXP QXP YQV YXT
        for idx, value in powerflow.dbarraDF.iterrows():
            if value["tipo"] != 0:
                powerflow.pxp[idx, nger] = -1.0
                powerflow.qxq[idx, nger] = -1.0
                powerflow.yqv[nger, idx] = 1.0
                nger += 1

                if value["tipo"] == 2:
                    powerflow.yxt[nare, idx] = 1.0

        # Submatrizes YPP YPX
        for idx, value in powerflow.dgeraDF.iterrows():
            powerflow.ypp[idx, idx] = 1.0
            powerflow.ypx[idx, nare] = 1.0 / (value["estatismo"] * 1e-2)

    ## Montagem Jacobiana
    # Condição
    if powerflow.controldim != 0:
        powerflow.extrarowp = zeros([powerflow.nger, powerflow.controldim])
        powerflow.extrarowq = zeros([powerflow.nger, powerflow.controldim])
        powerflow.extrarowy = zeros([powerflow.nger, powerflow.controldim])

        powerflow.extracolp = zeros([powerflow.controldim, powerflow.nger])
        powerflow.extracolq = zeros([powerflow.controldim, powerflow.nger])
        powerflow.extracoly = zeros([powerflow.controldim, powerflow.nger])

        # H-N M-L + ypt-ypv + yqt-yqv + yxt-yxv
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        concatenate(
                            (
                                powerflow.ypt,
                                powerflow.ypv,
                                powerflow.extrarowp,
                            ),
                            axis=1,
                        ),
                        concatenate(
                            (
                                powerflow.yqt,
                                powerflow.yqv,
                                powerflow.extrarowq,
                            ),
                            axis=1,
                        ),
                        concatenate(
                            (
                                powerflow.yxt,
                                powerflow.yxv,
                                powerflow.extrarowy,
                            ),
                            axis=1,
                        ),
                    ),
                    axis=0,
                ),
            ),
            axis=0,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxp,
                        powerflow.qxp,
                        powerflow.extracolp,
                        powerflow.ypp,
                        powerflow.yqp,
                        powerflow.yxp,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp + pxq-qxq-ypq-yqq-yxq
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxq,
                        powerflow.qxq,
                        powerflow.extracolq,
                        powerflow.ypq,
                        powerflow.yqq,
                        powerflow.yxq,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp pxq-qxq-ypq-yqq-yxq + pxx-qxx-ypx-yqx-yxx
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxx,
                        powerflow.qxx,
                        powerflow.extracoly,
                        powerflow.ypx,
                        powerflow.yqx,
                        powerflow.yxx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif powerflow.controldim == 0:
        # H-N M-L + ypt-ypv + yqt-yqv + yxt-yxv
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        concatenate((powerflow.ypt, powerflow.ypv), axis=1),
                        concatenate((powerflow.yqt, powerflow.yqv), axis=1),
                        concatenate((powerflow.yxt, powerflow.yxv), axis=1),
                    ),
                    axis=0,
                ),
            ),
            axis=0,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxp,
                        powerflow.qxp,
                        powerflow.ypp,
                        powerflow.yqp,
                        powerflow.yxp,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp + pxq-qxq-ypq-yqq-yxq
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxq,
                        powerflow.qxq,
                        powerflow.ypq,
                        powerflow.yqq,
                        powerflow.yxq,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp pxq-qxq-ypq-yqq-yxq + pxx-qxx-ypx-yqx-yxx
        powerflow.jacobian = concatenate(
            (
                powerflow.jacobian,
                concatenate(
                    (
                        powerflow.pxx,
                        powerflow.qxx,
                        powerflow.ypx,
                        powerflow.yqx,
                        powerflow.yxx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def frequpdt(
    powerflow,
):
    """atualização das variáveis de estado adicionais

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Atualização da potência ativa gerada
    powerflow.solution["active_generation"] += powerflow.statevar[
        (powerflow.dimprefreq) : (powerflow.dimprefreq + powerflow.nger)
    ]
    # Atualização da potência reativa gerada
    powerflow.solution["qlim_reactive_generation"] += powerflow.statevar[
        (powerflow.dimprefreq + powerflow.nger) : (
            powerflow.dimprefreq + 2 * powerflow.nger
        )
    ]
    # Atualização da defasagem angular
    powerflow.solution["freq"] += powerflow.statevar[
        (powerflow.dimprefreq + 2 * powerflow.nger)
    ]

    # Tratamento de limite de potência ativa
    for idx, value in powerflow.dgeraDF.iterrows():
        if powerflow.solution["freq"] >= powerflow.freqger["max"][idx]:
            powerflow.solution["active_generation"][idx] = (
                value["potencia_ativa_minima"] / powerflow.options["BASE"]
            )
            powerflow.ypp[idx][idx] = infty
        elif powerflow.solution["freq"] <= powerflow.freqger["min"][idx]:
            powerflow.solution["active_generation"][idx] = (
                value["potencia_ativa_maxima"] / powerflow.options["BASE"]
            )
            powerflow.ypp[idx][idx] = infty
        else:
            powerflow.ypp[idx][idx] = 1


def freqcorr(
    powerflow,
    case,
):
    """atualização dos valores de frequência para a etapa de correção do fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    powerflow.solution["freq"] = deepcopy(powerflow.point[case]["p"]["freq"])
    powerflow.solution["active_generation"] = deepcopy(
        powerflow.point[case]["p"]["active_generation"]
    )
    powerflow.solution["qlim_reactive_generation"] = deepcopy(
        powerflow.point[case]["p"]["qlim_reactive_generation"]
    )


def freqsubhess(
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
    #   H     N   pxp   pxq   pxx
    #   M     L   qxp   qxq   qxx
    # ypt   ypv   ypp   ypq   ypx
    # yqt   yqv   yqp   yqq   yqx
    # yxt   yxv   yxp   yxq   yxx
    #

    pass


def freqsubjacsym(
    powerflow,
):
    """

    Parametros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicializacao
    pass
