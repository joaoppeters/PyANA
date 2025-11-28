# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from numpy import (
    arange,
    asarray,
    asmatrix,
    concatenate,
    conj,
    cos,
    diag,
    exp,
    ones,
    r_,
    sin,
    vectorize,
    zeros,
)
from scipy.sparse import issparse, csr_matrix as sparse


def admittance(
    anarede,
):
    """Método para cálculo dos Args da matriz Admitância

    Args
        anarede:

    Builds the bus admittance matrix and branch admittance matrices.

    Returns the full bus admittance matrix (i.e. for all buses) and the
    matrices C{Yf} and C{Yt} which, when multiplied by a complex voltage
    vector, yield the vector currents injected into each line from the
    "from" and "to" buses respectively of each line. Does appropriate
    conversions to p.u.

    @see: L{makeSbus}

    @author: Ray Zimmerman (PSERC Cornell)

    ALL RIGHTS RESERVED TO RAY ZIMMERMAN
    CODE RETRIEVED FROM: https://github.com/rwl/PYPOWER
    """
    ## Inicialização
    Ysr = 1 / vectorize(complex)(
        anarede.dlinDF["resistencia"], anarede.dlinDF["reatancia"]
    )
    Ysh = vectorize(complex)(0, anarede.dbarDF["shunt_barra"] / anarede.cte["BASE"])

    Ytt = Ysr + vectorize(complex)(0, anarede.dlinDF["susceptancia"])
    Yff = Ytt / (
        vectorize(complex)(anarede.dlinDF["tap"] * conj(anarede.dlinDF["tap"]))
    )
    Yft = -Ysr / vectorize(complex)(conj(anarede.dlinDF["tap"]))
    Ytf = -Ysr / vectorize(complex)(anarede.dlinDF["tap"])

    f = (anarede.dlinDF["de-idx"]).values
    t = (anarede.dlinDF["para-idx"]).values

    ## connection matrix for line & from buses
    Cf = sparse(
        (ones(anarede.nlin), (range(anarede.nlin), f)),
        (anarede.nlin, anarede.nbus),
    )
    ## connection matrix for line & to buses
    Ct = sparse(
        (ones(anarede.nlin), (range(anarede.nlin), t)),
        (anarede.nlin, anarede.nbus),
    )

    ## build Yf and Yt such that Yf * V is the vector of complex branch currents injected
    ## at each branch's "from" bus, and Yt is the same for the "to" bus end
    i = r_[range(anarede.nlin), range(anarede.nlin)]  ## double set of row indices

    Yf = sparse((r_[Yff, Yft], (i, r_[f, t])), (anarede.nlin, anarede.nbus))
    Yt = sparse((r_[Ytf, Ytt], (i, r_[f, t])), (anarede.nlin, anarede.nbus))

    ## build Ybus
    anarede.Yb = sparse(
        Cf.T @ Yf
        + Ct.T @ Yt
        + sparse(
            (Ysh, (range(anarede.nbus), range(anarede.nbus))),
            (anarede.nbus, anarede.nbus),
        )
    )


def matrices(
    anarede,
):
    """jacobian and hessian matrices

    Args
        anarede:
    """
    ## Inicialização
    V = anarede.solution["voltage"] * exp(1j * anarede.solution["theta"])

    # Jacobiana
    dS_dVm, dS_dVa = dSbus_dV(anarede.Yb, V)
    A11 = (dS_dVa.A[anarede.maskP, :][:, anarede.maskP]).real  # dP_dAngV
    A12 = (dS_dVm.A[anarede.maskP, :][:, anarede.maskQ]).real  # dP_dMagV
    A21 = (dS_dVa.A[anarede.maskQ, :][:, anarede.maskP]).imag  # dQ_AngV
    A22 = (dS_dVm.A[anarede.maskQ, :][:, anarede.maskQ]).imag  # dQ_MagV
    anarede.jacobian = concatenate(
        (concatenate((A11, A21), axis=0), concatenate((A12, A22), axis=0)), axis=1
    )

    if anarede.controlcount > 0:
        from ctrl import controljac

        controljac(
            anarede,
        )

    if anarede.solution["method"] == "EXPC":
        # Vetor Jacobiana-Lambda
        anarede.G = anarede.jacobian.T @ anarede.solution["eigen"][
            anarede.mask
        ].reshape((sum(anarede.mask), 1))
        anarede.H = anarede.solution["eigen"][anarede.mask]

        # Hessiana
        Gpaa, Gpav, Gpva, Gpvv = d2Sbus_dV2(
            anarede.Yb, V, anarede.solution["eigen"][: anarede.nbus]
        )
        Gqaa, Gqav, Gqva, Gqvv = d2Sbus_dV2(
            anarede.Yb,
            V,
            anarede.solution["eigen"][anarede.nbus : 2 * anarede.nbus],
        )

        M1 = concatenate(
            (
                concatenate(
                    (
                        Gpaa.A[anarede.maskP, :][:, anarede.maskP],
                        Gpva.A[anarede.maskQ, :][:, anarede.maskP],
                    ),
                    axis=0,
                ),
                concatenate(
                    (
                        Gpav.A[anarede.maskP, :][:, anarede.maskQ],
                        Gpvv.A[anarede.maskQ, :][:, anarede.maskQ],
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )
        M2 = concatenate(
            (
                concatenate(
                    (
                        Gqaa.A[anarede.maskP, :][:, anarede.maskP],
                        Gqva.A[anarede.maskQ, :][:, anarede.maskP],
                    ),
                    axis=0,
                ),
                concatenate(
                    (
                        Gqav.A[anarede.maskP, :][:, anarede.maskQ],
                        Gqvv.A[anarede.maskQ, :][:, anarede.maskQ],
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

        anarede.hessian = M1.real + M2.imag

        # Submatrizes de controles ativos
        if anarede.controlcount > 0:
            from ctrl import controlhess

            controlhess(
                anarede,
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


def load2ycte(
    anarede,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    load2ycte = diag(
        (
            anarede.dbarDF.demanda_ativa.values
            - 1j * anarede.dbarDF.demanda_reativa.values
        )
        * 1e-2
        / anarede.solution["voltage"] ** 2
    )
    anarede.Yb.A = anarede.Yb.A + load2ycte


def md01jacob(
    anatem,
    generator,
    gen,
):
    """matriz jacobiana

    Args
        anarede:
    """
    ## Inicialização
    if gen == 0:
        anarede.jacobiangenoffright = zeros(
            (2 * anarede.nger, 2 * (anarede.nger + anarede.nbus))
        )
        anarede.jacobiangenoffdown = zeros(
            (2 * (anarede.nger + anarede.nbus), 2 * anarede.nger)
        )
        anarede.jacobiangen = zeros((2, 2))
        anarede.jacobiangen[0, 0] = 1
        anarede.jacobiangen[0, 1] = -anarede.dsimDF.step.values[0] * 0.5
        anarede.jacobiangen[1, 0] = (
            (anarede.dsimDF.step.values[0] * 0.5 / anarede.generator[generator][1])
            * anarede.solution["fem"][gen]
            * anarede.solution["voltage"][generator - 1]
            * cos(
                anarede.solution["delta"][gen]
                - anarede.solution["theta"][generator - 1]
            )
            / anarede.generator[generator][3]
        )
        anarede.jacobiangen[1, 1] = (
            1
            + anarede.dsimDF.step.values[0]
            * 0.5
            * anarede.generator[generator][2]
            / anarede.generator[generator][1]
        )

    else:
        anarede.jacobiangen = concatenate(
            (anarede.jacobiangen, zeros((anarede.jacobiangen.shape[0], 2))), axis=1
        )
        anarede.jacobiangen = concatenate(
            (anarede.jacobiangen, zeros((2, anarede.jacobiangen.shape[1]))), axis=0
        )

        anarede.jacobiangen[2 * gen, 2 * gen] = 1
        anarede.jacobiangen[2 * gen, 2 * gen + 1] = -anarede.dsimDF.step.values[0] * 0.5
        anarede.jacobiangen[2 * gen + 1, 2 * gen] = (
            (anarede.dsimDF.step.values[0] * 0.5 / anarede.generator[generator][1])
            * anarede.solution["fem"][gen]
            * anarede.solution["voltage"][generator - 1]
            * cos(
                anarede.solution["delta"][gen]
                - anarede.solution["theta"][generator - 1]
            )
            / anarede.generator[generator][3]
        )
        anarede.jacobiangen[2 * gen + 1, 2 * gen + 1] = (
            1
            + anarede.dsimDF.step.values[0]
            * 0.5
            * anarede.generator[generator][2]
            / anarede.generator[generator][1]
        )

    anarede.jacobiangenoffright[2 * gen + 1, generator - 1] = (
        (-anarede.dsimDF.step.values[0] * 0.5 / anarede.generator[generator][1])
        * anarede.solution["fem"][gen]
        * anarede.solution["voltage"][generator - 1]
        * cos(anarede.solution["delta"][gen] - anarede.solution["theta"][generator - 1])
        / anarede.generator[generator][3]
    )
    anarede.jacobiangenoffright[2 * gen + 1, anarede.nbus + generator - 1] = (
        (anarede.dsimDF.step.values[0] * 0.5 / anarede.generator[generator][1])
        * anarede.solution["fem"][gen]
        * sin(anarede.solution["delta"][gen] - anarede.solution["theta"][generator - 1])
        / anarede.generator[generator][3]
    )
    anarede.jacobiangenoffdown[generator - 1, 2 * gen] = (
        anarede.solution["fem"][gen]
        * anarede.solution["voltage"][generator - 1]
        * cos(anarede.solution["delta"][gen] - anarede.solution["theta"][generator - 1])
        / anarede.generator[generator][3]
    )
    anarede.jacobiangenoffdown[generator - 1 + anarede.nbus, 2 * gen] = (
        -anarede.solution["fem"][gen]
        * anarede.solution["voltage"][generator - 1]
        * sin(anarede.solution["delta"][gen] - anarede.solution["theta"][generator - 1])
        / anarede.generator[generator][3]
    )


def jacexsi(
    anatem,
):
    """

    Args
        anarede:
    """
    ## Inicialização
    dS_dVm, dS_dVa = dSbus_dV(
        anarede.Yblc,
        concatenate((anarede.solution["fem"], anarede.solution["voltage"]), axis=0),
    )

    anarede.jacobian = concatenate(
        (
            concatenate((dS_dVa.A.real, dS_dVa.A.imag), axis=0),
            concatenate((dS_dVm.A.real, dS_dVm.A.imag), axis=0),
        ),
        axis=1,
    )

    anarede.jacobiangen = concatenate(
        (
            concatenate((anarede.jacobiangen, anarede.jacobiangenoffright), axis=1),
            concatenate((anarede.jacobiangenoffdown, anarede.jacobian), axis=1),
        ),
        axis=0,
    )
