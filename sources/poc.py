# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import array, concatenate, vstack, zeros
from numpy.linalg import LinAlgError, lstsq, norm

from ctrl import controlsol
from increment import increment
from matrices import matrices
from residue import residue
from scheduled import scheduled
from update import updtstt, updtpwr


def poc(
    anarede,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Args
        anarede:
    """
    ## Inicialização
    # Variável para armazenamento de solução
    anarede.solution.update(
        {
            "method": "EXPC",
            "iter": 0,
            "freq": 1.0,
            "lambda": 0.0,
            "potencia_ativa": deepcopy(anarede.solution["active"]),
            "potencia_reativa": deepcopy(anarede.solution["reactive"]),
            "demanda_ativa": deepcopy(anarede.dbarDF["demanda_ativa"]),
            "demanda_reativa": deepcopy(anarede.dbarDF["demanda_reativa"]),
            "eigen": 1.0 * (anarede.mask),
            "sign": -1.0,
            "cvgprint": False,
        }
    )

    # Controles
    controlsol(
        anarede,
    )

    while True:
        # Incremento do Nível de Carregamento e Geração
        increment(
            anarede,
        )

        # Variáveis Especificadas
        scheduled(
            anarede,
        )

        # Resíduos
        residue(
            anarede,
        )

        # Matrizes
        matrices(
            anarede,
        )

        # expansao total
        expansion(
            anarede,
        )

        anarede.deltapoc = concatenate(
            (
                -anarede.deltaPQY.reshape((sum(anarede.mask), 1)),
                anarede.G,
                array([[anarede.H @ anarede.H - 1]]),
            ),
            axis=0,
        )

        try:
            # Your sparse matrix computation using spsolve here
            anarede.statevar, residuals, rank, singular = lstsq(
                anarede.jacobianpoc,
                anarede.deltapoc,
                rcond=None,
            )
        except LinAlgError:
            raise ValueError(
                "\033[91mERROR: Falha ao inverter a Matriz (singularidade)!\033[0m"
            )

        # Atualização das Variáveis de estado
        updtstt(
            anarede,
        )

        # Incremento de iteração
        anarede.solution["iter"] += 1

        if anarede.solution["cvgprint"]:
            print(norm(anarede.statevar), anarede.solution["lambda"])

        # Condição de Divergência por iterações
        if anarede.solution["iter"] > anarede.cte["ACIT"]:
            anarede.solution["convergence"] = (
                "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            )
            break

        elif (norm(anarede.statevar) <= anarede.cte["CTOL"]) and (
            anarede.solution["iter"] <= anarede.cte["ACIT"]
        ):
            anarede.solution["convergence"] = "SISTEMA CONVERGENTE"
            break

    updtpwr(
        anarede,
    )


def expansion(
    anarede,
):
    """expansão da matriz jacobiana para o método direto (Canizares, 1993)

    Args
        anarede:
    """
    ## Inicialização
    anarede.dtf = vstack(
        (anarede.solution["demanda_ativa"], anarede.solution["demanda_reativa"])
    )
    anarede.dtf = anarede.dtf.reshape((2 * anarede.nbus, 1)) / anarede.cte["BASE"]
    anarede.dtf = concatenate((anarede.dtf, zeros((anarede.controldim, 1))), axis=0)

    # Reducao Total
    anarede.dtf = anarede.dtf[anarede.mask]
    anarede.dwf = zeros((anarede.mask.shape[0], anarede.mask.shape[0]))[
        anarede.mask, :
    ][:, anarede.mask]

    anarede.dtg = zeros(anarede.dtf.shape)

    anarede.dxh = zeros((1, anarede.mask.shape[0]))[0, anarede.mask]
    anarede.dwh = 2 * anarede.solution["eigen"][anarede.mask]

    anarede.jacobianpoc = concatenate(
        (anarede.jacobian, anarede.dtf, anarede.dwf),
        axis=1,
    )

    anarede.jacobianpoc = concatenate(
        (
            anarede.jacobianpoc,
            concatenate(
                (anarede.hessian, anarede.dtg, anarede.jacobian.T),
                axis=1,
            ),
        ),
        axis=0,
    )

    anarede.jacobianpoc = concatenate(
        (
            anarede.jacobianpoc,
            concatenate(
                (anarede.dxh, array([0]), anarede.dwh),
                axis=0,
            ).reshape((1, anarede.jacobianpoc.shape[1])),
        ),
        axis=0,
    )
