# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import absolute, zeros
from numpy.linalg import det, eig, inv

from ctrl import controlpop


def eigensens(
    case,
    powerflow,
    stage: str = None,
):
    """análise de autovalores e autovetores

    Args
        powerflow:
        stage: string de identificação da etapa do fluxo de potência continuado
    """

    ## Inicialização
    # Reorganização da Matriz Jacobiana Expandida
    jacobian = deepcopy(powerflow.jacobian)

    if case > 0:
        jacobian = jacobian[:-1, :-1]

    # Submatrizes Jacobianas
    pt = deepcopy(jacobian[: (powerflow.Tval), :][:, : (powerflow.Tval)])
    pv = deepcopy(
        jacobian[: (powerflow.Tval), :][
            :,
            (powerflow.Tval) : (powerflow.Tval + powerflow.Vval + powerflow.controldim),
        ]
    )
    qt = deepcopy(
        jacobian[
            (powerflow.Tval) : (powerflow.Tval + powerflow.Vval + powerflow.controldim),
            :,
        ][:, : (powerflow.Tval)]
    )
    qv = deepcopy(
        jacobian[
            (powerflow.Tval) : (powerflow.Tval + powerflow.Vval + powerflow.controldim),
            :,
        ][
            :,
            (powerflow.Tval) : (powerflow.Tval + powerflow.Vval + powerflow.controldim),
        ]
    )

    try:
        # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
        rightvalues, rightvector = eig(powerflow.jacobian)
        powerflow.jacpfactor = zeros(powerflow.jacobian.shape)

        # Jacobiana reduzida - sensibilidade QV
        powerflow.jacQV = qv - qt @ inv(pt) @ pv
        rightvaluesQV, rightvectorQV = eig(powerflow.jacQV)
        rightvaluesQV = absolute(rightvaluesQV)
        powerflow.jacQVpfactor = zeros(qv.shape)
        for row in range(0, qv.shape[0]):
            for col in range(0, qv.shape[1]):
                powerflow.jacQVpfactor[col, row] = (
                    rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                )

        # Condição
        if stage == None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.operationpoint[case]["jacobian"] = powerflow.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.operationpoint[case]["determinant"] = det(powerflow.jacobian)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            powerflow.operationpoint[case]["eigenvalues"] = rightvalues
            powerflow.operationpoint[case]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.operationpoint[case][
                "participation_factor"
            ] = powerflow.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            powerflow.operationpoint[case]["jacobian-QV"] = powerflow.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.operationpoint[case]["determinant-QV"] = det(powerflow.jacQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            powerflow.operationpoint[case]["eigenvalues-QV"] = rightvaluesQV
            powerflow.operationpoint[case]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.operationpoint[case][
                "participationfactor-QV"
            ] = powerflow.jacQVpfactor

        elif stage != None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            powerflow.operationpoint[case][stage]["jacobian"] = powerflow.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            powerflow.operationpoint[case][stage]["determinant"] = det(
                powerflow.jacobian
            )

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            powerflow.operationpoint[case][stage]["eigenvalues"] = rightvalues
            powerflow.operationpoint[case][stage]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            powerflow.operationpoint[case][stage][
                "participationfactor"
            ] = powerflow.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            powerflow.operationpoint[case][stage]["jacobian-QV"] = powerflow.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            powerflow.operationpoint[case][stage]["determinant-QV"] = det(
                powerflow.jacQV
            )

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            powerflow.operationpoint[case][stage]["eigenvalues-QV"] = rightvaluesQV
            powerflow.operationpoint[case][stage]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            powerflow.operationpoint[case][stage][
                "participationfactor-QV"
            ] = powerflow.jacQVpfactor

    # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
    # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
    except:
        # self.active_heuristic = True

        # Reconfiguração do caso
        auxdiv = deepcopy(powerflow.solution["ndiv"]) + 1
        case -= 1
        controlpop(
            powerflow,
        )

        # Reconfiguração das variáveis de passo
        cpfkeys = {
            "system",
            "pmc",
            "v2l",
            "div",
            "beta",
            "step",
            "stepsch",
            "vsch",
            "varstep",
            "potencia_ativa",
            "demanda_ativa",
            "demanda_reativa",
            "stepmax",
        }
        powerflow.solution = {
            key: deepcopy(powerflow.operationpoint[case]["c"][key])
            for key in powerflow.solution.keys() & cpfkeys
        }
        powerflow.solution["ndiv"] = auxdiv

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        powerflow.solution["voltage"] = deepcopy(
            powerflow.operationpoint[case]["c"]["voltage"]
        )
        powerflow.solution["theta"] = deepcopy(
            powerflow.operationpoint[case]["c"]["theta"]
        )
