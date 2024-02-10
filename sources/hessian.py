# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from ctrl import controlhess, controljacsym

def hessian(
    powerflow,
):
    """cálculo das submatrizes da matriz Hessiana

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    from numpy import array, concatenate, exp

    V = powerflow.solution["voltage"]*exp(1j*powerflow.solution["theta"])
    Gaa1, Gav1, Gva1, Gvv1 = PPd2Sbus_dV2(powerflow.ybus, V, powerflow.solution["eigen"][:powerflow.nbus])
    Gaa2, Gav2, Gva2, Gvv2 = PPd2Sbus_dV2(powerflow.ybus, V, powerflow.solution["eigen"][powerflow.nbus:])

    M1 = concatenate((concatenate((Gaa1, Gav1), axis=1), concatenate((Gva1, Gvv1), axis=1)), axis=0)
    M2 = concatenate((concatenate((Gaa2, Gav2), axis=1), concatenate((Gva2, Gvv2), axis=1)), axis=0)
    # M1 = concatenate((concatenate((Gaa1[powerflow.maskP,:][:, powerflow.maskP], Gav1[powerflow.maskP,:][:, powerflow.maskQ]), axis=1), concatenate((Gva1[powerflow.maskQ,:][:, powerflow.maskP], Gvv1[powerflow.maskQ,:][:, powerflow.maskQ]), axis=1)), axis=0)
    # M2 = concatenate((concatenate((Gaa2[powerflow.maskP,:][:, powerflow.maskP], Gav2[powerflow.maskP,:][:, powerflow.maskQ]), axis=1), concatenate((Gva2[powerflow.maskQ,:][:, powerflow.maskP], Gvv2[powerflow.maskQ,:][:, powerflow.maskQ]), axis=1)), axis=0)
    powerflow.hessian = M1.real + M2.imag

    # Submatrizes de controles ativos
    if powerflow.controlcount > 0:
        controljacsym(
            powerflow,
        )
        controlhess(
            powerflow,
        )


def PPd2Sbus_dV2(
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
    """
    from numpy import ones, conj, arange
    from scipy.sparse import csr_matrix as sparse

    nb = len(V)
    ib = arange(nb)
    Ibus = Ybus @ V
    diaglam = sparse((lam, (ib, ib)))
    diagV = sparse((V, (ib, ib)))

    A = sparse((lam * V, (ib, ib)))
    B = Ybus * diagV
    C = A * conj(B)
    D = Ybus * diagV
    E = diagV.conj() * (D * diaglam - sparse((D @ lam, (ib, ib))))
    F = C - A * sparse((conj(Ibus), (ib, ib)))
    G = sparse((ones(nb) / abs(V), (ib, ib)))

    Gaa = E + F
    Gva = 1j * G * (E - F)
    Gav = Gva.T
    Gvv = G * (C + C.T) * G

    return Gaa, Gav, Gva, Gvv