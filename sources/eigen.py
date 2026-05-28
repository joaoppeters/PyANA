# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import absolute, zeros
from numpy.linalg import det, eig, inv

from ctrl import ctrlpop


def eigensens(
    case,
    anarede,
    stage: str = "",
):
    """analise de autovalores e autovetores

    Args
        anarede:
        stage: string de identificacao da etapa do fluxo de potencia continuado
    """
    # Reorganização da Matriz Jacobiana Expandida
    jacobian = deepcopy(anarede.jacobian)

    if case > 0:
        jacobian = jacobian[:-1, :-1]

    # Submatrizes Jacobianas
    pt = deepcopy(jacobian[: (anarede.Tval), :][:, : (anarede.Tval)])
    pv = deepcopy(
        jacobian[: (anarede.Tval), :][
            :,
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.ctrldim),
        ]
    )
    qt = deepcopy(
        jacobian[
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.ctrldim),
            :,
        ][:, : (anarede.Tval)]
    )
    qv = deepcopy(
        jacobian[
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.ctrldim),
            :,
        ][
            :,
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.ctrldim),
        ]
    )

    try:
        # Calculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
        rightvalues, rightvector = eig(anarede.jacobian)
        anarede.jacpfactor = zeros(anarede.jacobian.shape)

        # Jacobiana reduzida - sensibilidade QV
        anarede.jacQV = qv - qt @ inv(pt) @ pv
        rightvaluesQV, rightvectorQV = eig(anarede.jacQV)
        rightvaluesQV = absolute(rightvaluesQV)
        anarede.jacQVpfactor = zeros(qv.shape)
        for row in range(0, qv.shape[0]):
            for col in range(0, qv.shape[1]):
                anarede.jacQVpfactor[col, row] = (
                    rightvectorQV[col, row] * inv(rightvectorQV)[row, col]
                )

        # Condicao
        if stage == None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansao)
            anarede.operationpoint[case]["jacobian"] = anarede.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            anarede.operationpoint[case]["determinant"] = det(anarede.jacobian)

            # Calculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            anarede.operationpoint[case]["eigenvalues"] = rightvalues
            anarede.operationpoint[case]["eigenvectors"] = rightvector

            # Calculo e armazenamento do fator de participacao da matriz Jacobiana reduzida
            anarede.operationpoint[case]["participation_factor"] = anarede.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            anarede.operationpoint[case]["jacobian-QV"] = anarede.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            anarede.operationpoint[case]["determinant-QV"] = det(anarede.jacQV)

            # Calculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            anarede.operationpoint[case]["eigenvalues-QV"] = rightvaluesQV
            anarede.operationpoint[case]["eigenvectors-QV"] = rightvectorQV

            # Calculo e armazenamento do fator de participacao da matriz de sensibilidade QV
            anarede.operationpoint[case][
                "participationfactor-QV"
            ] = anarede.jacQVpfactor

        elif stage != None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansao)
            anarede.operationpoint[case][stage]["jacobian"] = anarede.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage]["determinant"] = det(anarede.jacobian)

            # Calculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage]["eigenvalues"] = rightvalues
            anarede.operationpoint[case][stage]["eigenvectors"] = rightvector

            # Calculo e armazenamento do fator de participacao da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage][
                "participationfactor"
            ] = anarede.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["jacobian-QV"] = anarede.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["determinant-QV"] = det(anarede.jacQV)

            # Calculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["eigenvalues-QV"] = rightvaluesQV
            anarede.operationpoint[case][stage]["eigenvectors-QV"] = rightvectorQV

            # Calculo e armazenamento do fator de participacao da matriz de sensibilidade QV
            anarede.operationpoint[case][stage][
                "participationfactor-QV"
            ] = anarede.jacQVpfactor

    # Caso nao seja possivel realizar a inversao da matriz PT pelo fato da geracao de potencia reativa
    # ter sido superior ao limite maximo durante a analise de tratamento de limites de geracao de potencia reativa
    except:
        # self.active_heuristic = True

        # Reconfiguracao do caso
        auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
        case -= 1
        controlpop(
            anarede,
        )

        # Reconfiguracao das variaveis de passo
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
        anarede.solution = {
            key: deepcopy(anarede.operationpoint[case]["c"][key])
            for key in anarede.solution.keys() & cpfkeys
        }
        anarede.solution["ndiv"] = auxdiv

        # Reconfiguracao dos valores de magnitude de tensao e defasagem angular de barramento
        anarede.solution["voltage"] = deepcopy(
            anarede.operationpoint[case]["c"]["voltage"]
        )
        anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["c"]["theta"])
