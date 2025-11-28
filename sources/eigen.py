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
        anarede:
        stage: string de identificação da etapa do fluxo de potência continuado
    """
    ## Inicialização
    # Reorganização da Matriz Jacobiana Expandida
    jacobian = deepcopy(anarede.jacobian)

    if case > 0:
        jacobian = jacobian[:-1, :-1]

    # Submatrizes Jacobianas
    pt = deepcopy(jacobian[: (anarede.Tval), :][:, : (anarede.Tval)])
    pv = deepcopy(
        jacobian[: (anarede.Tval), :][
            :,
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.controldim),
        ]
    )
    qt = deepcopy(
        jacobian[
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.controldim),
            :,
        ][:, : (anarede.Tval)]
    )
    qv = deepcopy(
        jacobian[
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.controldim),
            :,
        ][
            :,
            (anarede.Tval) : (anarede.Tval + anarede.Vval + anarede.controldim),
        ]
    )

    try:
        # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
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

        # Condição
        if stage == None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            anarede.operationpoint[case]["jacobian"] = anarede.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            anarede.operationpoint[case]["determinant"] = det(anarede.jacobian)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            anarede.operationpoint[case]["eigenvalues"] = rightvalues
            anarede.operationpoint[case]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            anarede.operationpoint[case]["participation_factor"] = anarede.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            anarede.operationpoint[case]["jacobian-QV"] = anarede.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            anarede.operationpoint[case]["determinant-QV"] = det(anarede.jacQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            anarede.operationpoint[case]["eigenvalues-QV"] = rightvaluesQV
            anarede.operationpoint[case]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            anarede.operationpoint[case][
                "participationfactor-QV"
            ] = anarede.jacQVpfactor

        elif stage != None:
            # Armazenamento da matriz Jacobiana reduzida (sem bignumber e sem expansão)
            anarede.operationpoint[case][stage]["jacobian"] = anarede.jacobian

            # Armazenamento do determinante da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage]["determinant"] = det(anarede.jacobian)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage]["eigenvalues"] = rightvalues
            anarede.operationpoint[case][stage]["eigenvectors"] = rightvector

            # Cálculo e armazenamento do fator de participação da matriz Jacobiana reduzida
            anarede.operationpoint[case][stage][
                "participationfactor"
            ] = anarede.jacpfactor

            # Armazenamento da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["jacobian-QV"] = anarede.jacQV

            # Armazenamento do determinante da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["determinant-QV"] = det(anarede.jacQV)

            # Cálculo e armazenamento dos autovalores e autovetores da matriz de sensibilidade QV
            anarede.operationpoint[case][stage]["eigenvalues-QV"] = rightvaluesQV
            anarede.operationpoint[case][stage]["eigenvectors-QV"] = rightvectorQV

            # Cálculo e armazenamento do fator de participação da matriz de sensibilidade QV
            anarede.operationpoint[case][stage][
                "participationfactor-QV"
            ] = anarede.jacQVpfactor

    # Caso não seja possível realizar a inversão da matriz PT pelo fato da geração de potência reativa
    # ter sido superior ao limite máximo durante a análise de tratamento de limites de geração de potência reativa
    except:
        # self.active_heuristic = True

        # Reconfiguração do caso
        auxdiv = deepcopy(anarede.solution["ndiv"]) + 1
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
        anarede.solution = {
            key: deepcopy(anarede.operationpoint[case]["c"][key])
            for key in anarede.solution.keys() & cpfkeys
        }
        anarede.solution["ndiv"] = auxdiv

        # Reconfiguração dos valores de magnitude de tensão e defasagem angular de barramento
        anarede.solution["voltage"] = deepcopy(
            anarede.operationpoint[case]["c"]["voltage"]
        )
        anarede.solution["theta"] = deepcopy(anarede.operationpoint[case]["c"]["theta"])
