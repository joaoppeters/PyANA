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
    anarede,
):
    """adiciona variáveis narea solução para caso controle de regulação primária de frequência esteja ativado

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.nare = 1

    # Condição
    if (anarede.control["FREQ"]) and (anarede.pwfblock["DGER"]):
        # Variáveis
        anarede.solution["active_generation"] = zeros(anarede.nger)
        anarede.solution["qlim_reactive_generation"] = zeros(anarede.nger)
        anarede.fesp = 1

        # Loop
        nger = 0
        for idx, value in anarede.dbarDF.iterrows():
            # Barra tipo VT ou PV
            if value["tipo"] != 0:
                anarede.solution["active_generation"][nger] = (
                    value["potencia_ativa"] / anarede.cte["BASE"]
                )
                anarede.solution["qlim_reactive_generation"][nger] = (
                    value["potencia_reativa"] / anarede.cte["BASE"]
                )
                nger += 1
        # Frequências máxima e mínima por gerador
        freqgerlim(
            anarede,
        )

    # DGER não ativado
    else:
        anarede.control["FREQ"] = False
        print(
            f"\033[93mERROR: Controle `FREQ` não será ativado por ausência de dados de barras geradoras! Atualize o campo `DGER` do arquivo `{anarede.system}`!\033[0m"
        )


def freqgerlim(
    anarede,
):
    """cálculo das frequências máximas e mínimas de operação de cada gerador

    Args
        anarede:  self do arquivo powerflowl.py
    """
    ## Inicialização
    # Variáveis
    anarede.freqger = {
        "max": zeros(anarede.nger),
        "min": zeros(anarede.nger),
    }
    anarede.dgerorder = dict()

    # Loop
    for idx, value in anarede.dgerDF.iterrows():
        # Armazenamento da barra por ordem de entrada de dados dos geradores
        anarede.dgerorder[idx] = anarede.dbarDF["nome"][value["numero"] - 1]
        # Frequência máxima gerador `idx`
        anarede.freqger["max"][idx] = (
            anarede.fesp
            + value["estatismo"]
            * 1e-2
            * (
                anarede.dbarDF["potencia_ativa"][value["numero"] - 1]
                - value["potencia_ativa_minima"]
            )
            / anarede.cte["BASE"]
        )
        # Frequência mínima gerador `idx`
        anarede.freqger["min"][idx] = (
            anarede.fesp
            + value["estatismo"]
            * 1e-2
            * (
                anarede.dbarDF["potencia_ativa"][value["numero"] - 1]
                - value["potencia_ativa_maxima"]
            )
            / anarede.cte["BASE"]
        )


def freqsch(
    anarede,
):
    """armazenamento de Args especificados das equações de controle adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Variáveis adicionais
    anarede.pqsch["potencia_ativa_gerada_especificada"] = zeros(anarede.nger)
    anarede.pqsch["potencia_reativa_gerada_especificada"] = zeros(anarede.nger)
    anarede.pqsch["magnitude_tensao_especificada"] = zeros(anarede.nbus)
    anarede.pqsch["defasagem_angular_especificada"] = zeros(anarede.nbus)

    # Contador de geradores
    nger = 0

    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Potência ativa gerada
            anarede.pqsch["potencia_ativa_gerada_especificada"][nger] = value[
                "potencia_ativa"
            ]
            # Potência reativa gerada
            anarede.pqsch["potencia_reativa_gerada_especificada"][nger] = value[
                "potencia_reativa"
            ]
            # Magnitude de tensão
            anarede.pqsch["magnitude_tensao_especificada"][idx] = value["tensao"] * 1e-3
            # Condição - slack
            if value["tipo"] == 2:
                # Defasagem angular
                anarede.pqsch["defasagem_angular_especificada"][idx] = radians(
                    value["angulo"]
                )
            # Incrementa contador
            nger += 1

    # Tratamento
    anarede.pqsch["potencia_ativa_gerada_especificada"] /= anarede.cte["BASE"]
    anarede.pqsch["potencia_reativa_gerada_especificada"] /= anarede.cte["BASE"]


def freqres(
    anarede,
):
    """cálculo de resíduos das equações de controle adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Vetor de resíduos
    anarede.deltaPger = zeros([anarede.nger])
    anarede.deltaQger = zeros([anarede.nger])
    anarede.deltaTger = zeros([anarede.nare])

    # Contador
    nger = 0

    # Loop
    for idx, value in anarede.dbarDF.iterrows():
        if value["tipo"] != 0:
            # Cálculo do resíduo DeltaP
            anarede.deltaP[idx] = anarede.solution["active_generation"][nger]
            anarede.deltaP[idx] -= value["demanda_ativa"] / anarede.cte["BASE"]
            anarede.deltaP[idx] -= pcalc(
                anarede,
                idx,
            )

            # Cálculo do resíduo DeltaQ
            anarede.deltaQ[idx] = anarede.solution["qlim_reactive_generation"][nger]
            anarede.deltaQ[idx] -= value["demanda_reativa"] / anarede.cte["BASE"]
            anarede.deltaQ[idx] -= qcalc(
                anarede,
                idx,
            )

            # Tratamento de limite de potência ativa
            if (anarede.solution["freq"] >= anarede.freqger["max"][nger]) or (
                anarede.solution["freq"] <= anarede.freqger["min"][nger]
            ):
                anarede.deltaPger[nger] = 0.0
            else:
                anarede.deltaPger[nger] += anarede.pqsch[
                    "potencia_ativa_gerada_especificada"
                ][nger]
                anarede.deltaPger[nger] -= anarede.solution["active_generation"][nger]
                anarede.deltaPger[nger] -= (
                    1 / (anarede.dgerDF["estatismo"][nger] * 1e-2)
                ) * (anarede.solution["freq"] - anarede.fesp)

            # Tratamento de limite de magnitude de tensão
            anarede.deltaQger[nger] += anarede.pqsch["magnitude_tensao_especificada"][
                idx
            ]
            anarede.deltaQger[nger] -= anarede.solution["voltage"][idx]

            # Condição - slack
            if value["tipo"] == 2:
                # Tratamento de limite de
                anarede.deltaTger += anarede.pqsch["defasagem_angular_especificada"][
                    idx
                ]
                anarede.deltaTger -= anarede.solution["theta"][idx]

            # Incrementa contador
            nger += 1

    # Resíduo de equação de controle
    anarede.deltaY = append(anarede.deltaY, anarede.deltaPger)
    anarede.deltaY = append(anarede.deltaY, anarede.deltaQger)
    anarede.deltaY = append(anarede.deltaY, anarede.deltaTger)


def freqsubjac(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
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
    anarede.dimprefreq = deepcopy(anarede.jacobian.shape[0])

    # Condição
    if anarede.freqjcount == 0:
        # Variável
        anarede.freqjcount += 1

        # Submatrizes
        anarede.pxp = zeros([anarede.nbus, anarede.nger])  # -> APG
        anarede.pxq = zeros([anarede.nbus, anarede.nger])
        anarede.pxx = zeros([anarede.nbus, anarede.nare])

        anarede.qxp = zeros([anarede.nbus, anarede.nger])
        anarede.qxq = zeros([anarede.nbus, anarede.nger])  # -> BQG
        anarede.qxx = zeros([anarede.nbus, anarede.nare])

        anarede.ypt = zeros([anarede.nger, anarede.nbus])
        anarede.ypv = zeros([anarede.nger, anarede.nbus])
        anarede.ypp = zeros([anarede.nger, anarede.nger])  # -> CPG
        anarede.ypq = zeros([anarede.nger, anarede.nger])
        anarede.ypx = zeros([anarede.nger, anarede.nare])  # -> CF

        anarede.yqt = zeros([anarede.nger, anarede.nbus])
        anarede.yqv = zeros([anarede.nger, anarede.nbus])  # -> EQG
        anarede.yqp = zeros([anarede.nger, anarede.nger])
        anarede.yqq = zeros([anarede.nger, anarede.nger])
        anarede.yqx = zeros([anarede.nger, anarede.nare])

        anarede.yxt = zeros([anarede.nare, anarede.nbus])  # -> FT
        anarede.yxv = zeros([anarede.nare, anarede.nbus])
        anarede.yxp = zeros([anarede.nare, anarede.nger])
        anarede.yxq = zeros([anarede.nare, anarede.nger])
        anarede.yxx = zeros([anarede.nare, anarede.nare])

        # Contadores
        nger = 0
        nare = 0

        # Submatrizes PXP QXP YQV YXT
        for idx, value in anarede.dbarDF.iterrows():
            if value["tipo"] != 0:
                anarede.pxp[idx, nger] = -1.0
                anarede.qxq[idx, nger] = -1.0
                anarede.yqv[nger, idx] = 1.0
                nger += 1

                if value["tipo"] == 2:
                    anarede.yxt[nare, idx] = 1.0

        # Submatrizes YPP YPX
        for idx, value in anarede.dgerDF.iterrows():
            anarede.ypp[idx, idx] = 1.0
            anarede.ypx[idx, nare] = 1.0 / (value["estatismo"] * 1e-2)

    ## Montagem Jacobiana
    # Condição
    if anarede.controldim != 0:
        anarede.extrarowp = zeros([anarede.nger, anarede.controldim])
        anarede.extrarowq = zeros([anarede.nger, anarede.controldim])
        anarede.extrarowy = zeros([anarede.nger, anarede.controldim])

        anarede.extracolp = zeros([anarede.controldim, anarede.nger])
        anarede.extracolq = zeros([anarede.controldim, anarede.nger])
        anarede.extracoly = zeros([anarede.controldim, anarede.nger])

        # H-N M-L + ypt-ypv + yqt-yqv + yxt-yxv
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        concatenate(
                            (
                                anarede.ypt,
                                anarede.ypv,
                                anarede.extrarowp,
                            ),
                            axis=1,
                        ),
                        concatenate(
                            (
                                anarede.yqt,
                                anarede.yqv,
                                anarede.extrarowq,
                            ),
                            axis=1,
                        ),
                        concatenate(
                            (
                                anarede.yxt,
                                anarede.yxv,
                                anarede.extrarowy,
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
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxp,
                        anarede.qxp,
                        anarede.extracolp,
                        anarede.ypp,
                        anarede.yqp,
                        anarede.yxp,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp + pxq-qxq-ypq-yqq-yxq
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxq,
                        anarede.qxq,
                        anarede.extracolq,
                        anarede.ypq,
                        anarede.yqq,
                        anarede.yxq,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp pxq-qxq-ypq-yqq-yxq + pxx-qxx-ypx-yqx-yxx
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxx,
                        anarede.qxx,
                        anarede.extracoly,
                        anarede.ypx,
                        anarede.yqx,
                        anarede.yxx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

    elif anarede.controldim == 0:
        # H-N M-L + ypt-ypv + yqt-yqv + yxt-yxv
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        concatenate((anarede.ypt, anarede.ypv), axis=1),
                        concatenate((anarede.yqt, anarede.yqv), axis=1),
                        concatenate((anarede.yxt, anarede.yxv), axis=1),
                    ),
                    axis=0,
                ),
            ),
            axis=0,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv + pxp-qxp-ypp-yqp-yxp
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxp,
                        anarede.qxp,
                        anarede.ypp,
                        anarede.yqp,
                        anarede.yxp,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp + pxq-qxq-ypq-yqq-yxq
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxq,
                        anarede.qxq,
                        anarede.ypq,
                        anarede.yqq,
                        anarede.yxq,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        # H-M-ypt-yqt-yxt N-L-ypv-yqv-yxv pxp-qxp-ypp-yqp-yxp pxq-qxq-ypq-yqq-yxq + pxx-qxx-ypx-yqx-yxx
        anarede.jacobian = concatenate(
            (
                anarede.jacobian,
                concatenate(
                    (
                        anarede.pxx,
                        anarede.qxx,
                        anarede.ypx,
                        anarede.yqx,
                        anarede.yxx,
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )


def frequpdt(
    anarede,
):
    """atualização das variáveis de estado adicionais

    Args
        anarede:
    """
    ## Inicialização
    # Atualização da potência ativa gerada
    anarede.solution["active_generation"] += anarede.statevar[
        (anarede.dimprefreq) : (anarede.dimprefreq + anarede.nger)
    ]
    # Atualização da potência reativa gerada
    anarede.solution["qlim_reactive_generation"] += anarede.statevar[
        (anarede.dimprefreq + anarede.nger) : (anarede.dimprefreq + 2 * anarede.nger)
    ]
    # Atualização da defasagem angular
    anarede.solution["freq"] += anarede.statevar[
        (anarede.dimprefreq + 2 * anarede.nger)
    ]

    # Tratamento de limite de potência ativa
    for idx, value in anarede.dgerDF.iterrows():
        if anarede.solution["freq"] >= anarede.freqger["max"][idx]:
            anarede.solution["active_generation"][idx] = (
                value["potencia_ativa_minima"] / anarede.cte["BASE"]
            )
            anarede.ypp[idx][idx] = infty
        elif anarede.solution["freq"] <= anarede.freqger["min"][idx]:
            anarede.solution["active_generation"][idx] = (
                value["potencia_ativa_maxima"] / anarede.cte["BASE"]
            )
            anarede.ypp[idx][idx] = infty
        else:
            anarede.ypp[idx][idx] = 1


def freqcorr(
    anarede,
    case,
):
    """atualização dos valores de frequência para a etapa de correção do fluxo de potência continuado

    Args
        anarede:
    """
    ## Inicialização
    # Variável
    anarede.solution["freq"] = deepcopy(anarede.operationpoint[case]["p"]["freq"])
    anarede.solution["active_generation"] = deepcopy(
        anarede.operationpoint[case]["p"]["active_generation"]
    )
    anarede.solution["qlim_reactive_generation"] = deepcopy(
        anarede.operationpoint[case]["p"]["qlim_reactive_generation"]
    )


def freqsubhess(
    anarede,
):
    """submatrizes da matriz jacobiana

    Args
        anarede:
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
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    pass
