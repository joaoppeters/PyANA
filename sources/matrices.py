# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import arange, asarray, asmatrix, conj, diag, exp, ones
from scipy.sparse import issparse, csr_matrix as sparse, vstack, hstack

def matrices(
    powerflow,
):
    """jacobian and hessian matrices

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])

    # Jacobiana
    dS_dVm, dS_dVa = dSbus_dV(powerflow.Ybus, V)
    powerflow.jacobian = vstack((
        hstack((dS_dVa[powerflow.maskP,:][:,powerflow.maskP].real, dS_dVm[powerflow.maskP,:][:,powerflow.maskQ].real), format="csr",), 
        hstack((dS_dVa[powerflow.maskQ,:][:,powerflow.maskP].imag, dS_dVm[powerflow.maskQ,:][:,powerflow.maskQ].imag), format="csr",)),
        format="csr",
    )

    if powerflow.controlcount > 0:
        from ctrl import controljac

        controljac(
            powerflow,
        )

    if powerflow.solution["method"] == "CANI":
        # Vetor Jacobiana-Lambda
        powerflow.G = (
            powerflow.jacobian.T @ powerflow.solution["eigen"][powerflow.mask]
        )
        powerflow.H = powerflow.solution["eigen"][powerflow.mask]

        # Hessiana
        Gpaa, Gpav, Gpva, Gpvv = d2Sbus_dV2(
            powerflow.Ybus, V, powerflow.solution["eigen"][: powerflow.nbus]
        )
        Gqaa, Gqav, Gqva, Gqvv = d2Sbus_dV2(
            powerflow.Ybus, V, powerflow.solution["eigen"][powerflow.nbus : 2*powerflow.nbus]
        )

        
        M1 = vstack((hstack((Gpaa[powerflow.maskP,:][:, powerflow.maskP], Gpav[powerflow.maskP,:][:, powerflow.maskQ]), format="csr",), hstack((Gpva[powerflow.maskQ,:][:, powerflow.maskP], Gpvv[powerflow.maskQ,:][:, powerflow.maskQ]), format="csr",)), format="csr",)
        M2 = vstack((hstack((Gqaa[powerflow.maskP,:][:, powerflow.maskP], Gqav[powerflow.maskP,:][:, powerflow.maskQ]), format="csr",), hstack((Gqva[powerflow.maskQ,:][:, powerflow.maskP], Gqvv[powerflow.maskQ,:][:, powerflow.maskQ]), format="csr",)), format="csr",)
        powerflow.hessian = M1.real + M2.imag

        # Submatrizes de controles ativos
        if powerflow.controlcount > 0:
            from ctrl import controlhess

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
        Ibus = Ybus @ V

        diagV = sparse((V, (ib, ib)))
        diagIbus = sparse((Ibus, (ib, ib)))
        diagVnorm = sparse((V / abs(V), (ib, ib)))
    else:
        Ibus = Ybus @ asmatrix(V).T

        diagV = asmatrix(diag(V))
        diagIbus = asmatrix(diag(asarray(Ibus).flatten()))
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