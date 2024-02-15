# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from numpy import (
    arange,
    array,
    asarray,
    asmatrix,
    concatenate,
    conj,
    diag,
    exp,
    ones,
    radians,
    sqrt,
    sum,
    zeros,
)
from numpy.linalg import norm, solve
from scipy.sparse import issparse, csr_matrix as sparse

from calc import pcalc, qcalc
from ctrl import controlupdt, controlres, controlsol, controlsch
from hessian import hessian
from jacobian import jacobi


def cani(
    powerflow,
):
    """análise do fluxo de potência não-linear em regime permanente de SEP via método direto (Canizares, 1993)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento de solução
    powerflow.solution = {
        "system": powerflow.name,
        "iter": 0,
        "voltage": array(powerflow.dbarraDF["tensao"] * 1e-3),
        "theta": array(radians(powerflow.dbarraDF["angulo"])),
        "active": zeros(powerflow.nbus),
        "reactive": zeros(powerflow.nbus),
        "freq": 1.0,
        "lambda": 0.0,
        "potencia_ativa": deepcopy(powerflow.dbarraDF["potencia_ativa"]),
        "demanda_ativa": deepcopy(powerflow.dbarraDF["demanda_ativa"]),
        "demanda_reativa": deepcopy(powerflow.dbarraDF["demanda_reativa"]),
        "eigen": 1.0 * (powerflow.mask),
    }

    # Controles
    controlsol(
        powerflow,
    )

    while True:
        # Incremento do Nível de Carregamento e Geração
        increment(
            powerflow,
        )

        # Variáveis Especificadas
        scheduled(
            powerflow,
        )

        # Resíduos
        residue(
            powerflow,
        )

        # Matrizes 
        matrices(
            powerflow,
        )

        # Vetor Jacobiana-Lambda    
        powerflow.G = powerflow.jacobian.T @ powerflow.solution["eigen"][powerflow.mask].reshape((powerflow.mask.sum(), 1))

        # expansao total
        expansion(
            powerflow,
        )
        
        powerflow.canistate = concatenate(
        (
            powerflow.solution["theta"],
            powerflow.solution["voltage"],
            array([powerflow.solution["lambda"]]),
            powerflow.solution["eigen"],
        ),
        axis=0,
    )

        powerflow.funccani = concatenate(
            (
                powerflow.deltaPQY,
                array(powerflow.G).reshape(powerflow.G.shape[0],),
                array([sum(powerflow.H.T * powerflow.H) - 1]),
            ),
            axis=0,
        ).astype(float)

        # Variáveis de estado
        powerflow.statevar = solve(powerflow.jaccani, powerflow.funccani)

        # Atualização das Variáveis de estado
        update_statevar(
            powerflow,
        )

        # Incremento de iteração
        powerflow.solution["iter"] += 1

        # Condição de Divergência por iterações
        if  (norm(powerflow.statevar) > powerflow.options["CTOL"]) and (powerflow.solution["iter"] > powerflow.options["ACIT"]):
            powerflow.solution[
                "convergence"
            ] = "SISTEMA DIVERGENTE (extrapolação de número máximo de iterações)"
            break

        elif (norm(powerflow.statevar) <= powerflow.options["CTOL"]) and (
            powerflow.solution["iter"] <= powerflow.options["ACIT"]
        ):
            powerflow.solution["convergence"] = "SISTEMA CONVERGENTE"
            break


def increment(
    powerflow,
):
    """realiza incremento no nível de carregamento (e geração)

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável
    preincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy())

    # Incremento de carga
    for idxbar, _ in powerflow.dbarraDF.iterrows():
        # Incremento de Carregamento
        powerflow.dbarraDF.at[idxbar, "demanda_ativa"] = powerflow.solution[
            "demanda_ativa"
        ][idxbar] * (1 + powerflow.solution["lambda"])
        powerflow.dbarraDF.at[idxbar, "demanda_reativa"] = powerflow.solution[
            "demanda_reativa"
        ][idxbar] * (1 + powerflow.solution["lambda"])

    deltaincrement = sum(powerflow.dbarraDF["demanda_ativa"].to_numpy()) - preincrement

    # Incremento de geração
    if powerflow.codes["DGER"]:
        for _, valueger in powerflow.dgeraDF.iterrows():
            idx = valueger["numero"] - 1
            powerflow.dbarraDF.at[idx, "potencia_ativa"] = powerflow.dbarraDF[
                "potencia_ativa"
            ][idx] + (deltaincrement * valueger["fator_participacao"])

        powerflow.solution["potencia_ativa"] = deepcopy(
            powerflow.dbarraDF["potencia_ativa"]
        )


def scheduled(
    powerflow,
):
    """método para armazenamento dos parâmetros especificados

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Variável para armazenamento das potências ativa e reativa especificadas
    powerflow.pqsch = {
        "potencia_ativa_especificada": zeros(powerflow.nbus),
        "potencia_reativa_especificada": zeros(powerflow.nbus),
    }

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Potência ativa especificada
        powerflow.pqsch["potencia_ativa_especificada"][idx] += value["potencia_ativa"]
        powerflow.pqsch["potencia_ativa_especificada"][idx] -= value["demanda_ativa"]

        # Potência reativa especificada
        powerflow.pqsch["potencia_reativa_especificada"][idx] += value[
            "potencia_reativa"
        ]
        powerflow.pqsch["potencia_reativa_especificada"][idx] -= value[
            "demanda_reativa"
        ]

    # Tratamento
    powerflow.pqsch["potencia_ativa_especificada"] /= powerflow.options["BASE"]
    powerflow.pqsch["potencia_reativa_especificada"] /= powerflow.options["BASE"]

    # Variáveis especificadas de controle ativos
    if powerflow.controlcount > 0:
        controlsch(
            powerflow,
        )


def residue(
    powerflow,
):
    """cálculo de resíduos das equações diferenciáveis

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # Vetores de resíduo
    powerflow.deltaP = zeros(powerflow.nbus)
    powerflow.deltaQ = zeros(powerflow.nbus)
    V = powerflow.solution["voltage"]*exp(1j*powerflow.solution["theta"])
    I = powerflow.ybus @ V
    S = diag(V) @ conj(I)

    # Loop
    for idx, value in powerflow.dbarraDF.iterrows():
        # Tipo PV ou PQ - Resíduo Potência Ativa
        if value["tipo"] != 2:
            powerflow.deltaP[idx] -= powerflow.pqsch["potencia_ativa_especificada"][idx]
            powerflow.deltaP[idx] += S[idx].real

        # Tipo PQ - Resíduo Potência Reativa
        if (
            ("QLIM" in powerflow.control)
            or ("QLIMs" in powerflow.control)
            or ("QLIMn" in powerflow.control)
            or (value["tipo"] == 0)
        ):
            powerflow.deltaQ[idx] -= powerflow.pqsch["potencia_reativa_especificada"][
                idx
            ]
            powerflow.deltaQ[idx] += S[idx].imag

    # Concatenação de resíduos de potencia ativa e reativa em função da formulação jacobiana
    concatresidue(
        powerflow,
    )

    # Resíduos de variáveis de estado de controle
    if powerflow.controlcount > 0:
        controlres(
            powerflow,
        )
        concatresidue(
            powerflow,
        )
        powerflow.deltaPQY = concatenate((powerflow.deltaPQY, powerflow.deltaY), axis=0)
    else:
        powerflow.deltaY = array([0])


def concatresidue(
    powerflow,
):
    """concatenação de resíduos de potências ativa e reativa

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    # configuração completa
    powerflow.deltaPQY = concatenate((powerflow.deltaP, powerflow.deltaQ), axis=0)


def update_statevar(
    powerflow,
):
    """atualização das variáveis de estado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    thetavalues = sum(powerflow.maskP)
    voltagevalues = sum(powerflow.maskQ)

    # configuração reduzida
    powerflow.solution["theta"][powerflow.maskP] -= powerflow.statevar[0:(thetavalues)]
    powerflow.solution["voltage"][powerflow.maskQ] -= powerflow.statevar[
        (thetavalues) : (thetavalues + voltagevalues)
    ]

    # Atualização das variáveis de estado adicionais para controles ativos
    if powerflow.controlcount > 0:
        controlupdt(
            powerflow,
        )

    powerflow.solution["lambda"] -= powerflow.statevar[
        (thetavalues + voltagevalues + powerflow.controldim)
    ]
    powerflow.solution["eigen"][powerflow.mask] -= powerflow.statevar[
        (thetavalues + voltagevalues + powerflow.controldim + 1) :
    ]


def expansion(
    powerflow,
):
    """expansão da matriz jacobiana para o método continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.dtf = zeros([2*powerflow.nbus, 1])

    # Demanda
    for idx, value in powerflow.dbarraDF.iterrows():
        if value["tipo"] != 2:
            powerflow.dtf[idx, 0] = (
                powerflow.solution["demanda_ativa"][idx]
                - powerflow.solution["potencia_ativa"][idx]
            )
            if value["tipo"] == 0:
                powerflow.dtf[(idx + powerflow.nbus), 0] = powerflow.solution[
                    "demanda_reativa"
                ][idx]

    powerflow.dtf /= powerflow.options["BASE"]

    # reducao total
    reduction(
        powerflow,
    )

    powerflow.jaccani = concatenate(
        (powerflow.jacobian, powerflow.dtf, powerflow.dwf),
        axis=1,
    )

    powerflow.jaccani = concatenate(
        (
            powerflow.jaccani,
            concatenate(
                (powerflow.hessian, powerflow.dtg, powerflow.jacobian.T),
                axis=1,
            ),
        ),
        axis=0,
    )

    powerflow.jaccani = concatenate(
        (
            powerflow.jaccani,
            concatenate(
                (powerflow.dxh, array([0]), powerflow.dwh),
                axis=0,
            ).reshape((1, powerflow.jaccani.shape[1])),
        ),
        axis=0,
    )


def reduction(
    powerflow,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    powerflow.deltaPQY = powerflow.deltaPQY[powerflow.mask]
    # powerflow.G = powerflow.G[powerflow.mask]
    powerflow.H = powerflow.solution["eigen"][powerflow.mask]

    # powerflow.jacobian = powerflow.jacob.A[powerflow.mask, :][:, powerflow.mask]
    powerflow.dtf = powerflow.dtf[powerflow.mask]
    powerflow.dwf = zeros((powerflow.mask.shape[0], powerflow.mask.shape[0]))[
        powerflow.mask, :
    ][:, powerflow.mask]

    # powerflow.hessian = powerflow.hessian[powerflow.mask, :][:, powerflow.mask]
    powerflow.dtg = zeros((powerflow.mask.shape[0], 1))[powerflow.mask]

    powerflow.dxh = zeros((1, powerflow.mask.shape[0]))[0, powerflow.mask]
    powerflow.dwh = 2 * powerflow.solution["eigen"][powerflow.mask]


def matrices(
    powerflow,
):
    """jacobian and hessian matrices
    
    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    V = powerflow.solution["voltage"]*exp(1j*powerflow.solution["theta"])
    
    # Jacobiana
    dS_dVm, dS_dVa = dSbus_dV(powerflow.ybus, V)
    powerflow.jacobian = concatenate((concatenate((dS_dVa[powerflow.maskP,:][:,powerflow.maskP].real, dS_dVm[powerflow.maskP,:][:,powerflow.maskQ].real), axis=1), 
                                      concatenate((dS_dVa[powerflow.maskQ,:][:,powerflow.maskP].imag, dS_dVm[powerflow.maskQ,:][:,powerflow.maskQ].imag), axis=1)), 
                                      axis=0)

    # Hessiana
    Gaa1, Gav1, Gva1, Gvv1 = d2Sbus_dV2(powerflow.ybus, V, powerflow.solution["eigen"][:powerflow.nbus])
    Gaa2, Gav2, Gva2, Gvv2 = d2Sbus_dV2(powerflow.ybus, V, powerflow.solution["eigen"][powerflow.nbus:])
    
    M1 = concatenate((concatenate((Gaa1[powerflow.maskP,:][:, powerflow.maskP], Gav1[powerflow.maskP,:][:, powerflow.maskQ]), axis=1), concatenate((Gva1[powerflow.maskQ,:][:, powerflow.maskP], Gvv1[powerflow.maskQ,:][:, powerflow.maskQ]), axis=1)), axis=0)
    M2 = concatenate((concatenate((Gaa2[powerflow.maskP,:][:, powerflow.maskP], Gav2[powerflow.maskP,:][:, powerflow.maskQ]), axis=1), concatenate((Gva2[powerflow.maskQ,:][:, powerflow.maskP], Gvv2[powerflow.maskQ,:][:, powerflow.maskQ]), axis=1)), axis=0)
    powerflow.hessian = array(M1).real + array(M2).imag

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        from ctrl import controlhess, controljacsym
        controljacsym(
            powerflow,
        )
        controlhess(
            powerflow,
        )


def dSbus_dV(Ybus, V):
    """Computes partial derivatives of power injection w.r.t. voltage.

    Returns two matrices containing partial derivatives of the complex bus
    power injections w.r.t voltage magnitude and voltage angle respectively
    (for all buses). If C{Ybus} is a sparse matrix, the return values will be
    also. The following explains the expressions used to form the matrices::

        S = diag(V) * conj(Ibus) = diag(conj(Ibus)) * V

    Partials of V & Ibus w.r.t. voltage magnitudes::
        dV/dVm = diag(V / abs(V))
        dI/dVm = Ybus * dV/dVm = Ybus * diag(V / abs(V))

    Partials of V & Ibus w.r.t. voltage angles::
        dV/dVa = j * diag(V)
        dI/dVa = Ybus * dV/dVa = Ybus * j * diag(V)

    Partials of S w.r.t. voltage magnitudes::
        dS/dVm = diag(V) * conj(dI/dVm) + diag(conj(Ibus)) * dV/dVm
               = diag(V) * conj(Ybus * diag(V / abs(V)))
                                        + conj(diag(Ibus)) * diag(V / abs(V))

    Partials of S w.r.t. voltage angles::
        dS/dVa = diag(V) * conj(dI/dVa) + diag(conj(Ibus)) * dV/dVa
               = diag(V) * conj(Ybus * j * diag(V))
                                        + conj(diag(Ibus)) * j * diag(V)
               = -j * diag(V) * conj(Ybus * diag(V))
                                        + conj(diag(Ibus)) * j * diag(V)
               = j * diag(V) * conj(diag(Ibus) - Ybus * diag(V))

    For more details on the derivations behind the derivative code used
    in PYPOWER information, see:

    [TN2]  R. D. Zimmerman, "AC Power Flows, Generalized OPF Costs and
    their Derivatives using Complex Matrix Notation", MATPOWER
    Technical Note 2, February 2010.
    U{http://www.pserc.cornell.edu/matpower/TN2-OPF-Derivatives.pdf}

    @author: Ray Zimmerman (PSERC Cornell)

    ALL RIGHTS RESERVED TO RAY ZIMMERMAN
    CODE RETRIEVED FROM: https://github.com/rwl/PYPOWER
    """
    ib = range(len(V))

    if issparse(Ybus):
        Ibus = Ybus * V

        diagV = sparse((V, (ib, ib)))
        diagIbus = sparse((Ibus, (ib, ib)))
        diagVnorm = sparse((V / abs(V), (ib, ib)))
    else:
        Ibus = Ybus * asmatrix(V).T

        diagV = asmatrix(diag(V))
        diagIbus = asmatrix(diag( asarray(Ibus).flatten() ))
        diagVnorm = asmatrix(diag(V / abs(V)))

    dS_dVm = diagV * conj(Ybus * diagVnorm) + conj(diagIbus) * diagVnorm
    dS_dVa = 1j * diagV * conj(diagIbus - Ybus * diagV)

    return dS_dVm, dS_dVa


def d2Sbus_dV2(
    Ybus,
    V,
    lam,
):
    """Computes 2nd derivatives of power injection w.r.t. voltage.

    Returns 4 matrices containing the partial derivatives w.r.t. voltage angle
    and magnitude of the product of a vector C{lam} with the 1st partial
    derivatives of the complex bus power injections. Takes sparse bus
    admittance matrix C{Ybus}, voltage vector C{V} and C{nb x 1} vector of
    multipliers C{lam}. Output matrices are sparse.

    For more details on the derivations behind the derivative code used
    in PYPOWER information, see:

    [TN2]  R. D. Zimmerman, I{"AC Power Flows, Generalized OPF Costs and
    their Derivatives using Complex Matrix Notation"}, MATPOWER
    Technical Note 2, February 2010.
    U{http://www.pserc.cornell.edu/matpower/TN2-OPF-Derivatives.pdf}

    @author: Ray Zimmerman (PSERC Cornell)

    ALL RIGHTS RESERVED TO RAY ZIMMERMAN
    CODE RETRIEVED FROM: https://github.com/rwl/PYPOWER
    """
    nb = len(V)
    ib = arange(nb)
    Ibus = Ybus @ V
    diaglam = sparse((lam, (ib, ib)))
    diagV = sparse((V, (ib, ib)))

    A = sparse((lam * V, (ib, ib)))
    B = Ybus * diagV
    C = A * conj(B)
    D = Ybus.T.conj() * diagV
    E = diagV.conj() * (D * diaglam - sparse((D @ lam, (ib, ib))))
    F = C - A * sparse((conj(Ibus), (ib, ib)))
    G = sparse((ones(nb) / abs(V), (ib, ib)))

    Gaa = E + F
    Gva = 1j * G * (E - F)
    Gav = Gva.T
    Gvv = G * (C + C.T) * G

    return Gaa, Gav, Gva, Gvv