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
    powerflow,
):
    """Método para cálculo dos Args da matriz Admitância

    Args
        powerflow:

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
        powerflow.dlinDF["resistencia"], powerflow.dlinDF["reatancia"]
    )
    Ysh = vectorize(complex)(
        0, powerflow.dbarDF["shunt_barra"] / powerflow.options["BASE"]
    )

    Ytt = Ysr + vectorize(complex)(0, powerflow.dlinDF["susceptancia"])
    Yff = Ytt / (
        vectorize(complex)(powerflow.dlinDF["tap"] * conj(powerflow.dlinDF["tap"]))
    )
    Yft = -Ysr / vectorize(complex)(conj(powerflow.dlinDF["tap"]))
    Ytf = -Ysr / vectorize(complex)(powerflow.dlinDF["tap"])

    f = (powerflow.dlinDF["de-idx"]).values
    t = (powerflow.dlinDF["para-idx"]).values

    ## connection matrix for line & from buses
    Cf = sparse(
        (ones(powerflow.nlin), (range(powerflow.nlin), f)),
        (powerflow.nlin, powerflow.nbus),
    )
    ## connection matrix for line & to buses
    Ct = sparse(
        (ones(powerflow.nlin), (range(powerflow.nlin), t)),
        (powerflow.nlin, powerflow.nbus),
    )

    ## build Yf and Yt such that Yf * V is the vector of complex branch currents injected
    ## at each branch's "from" bus, and Yt is the same for the "to" bus end
    i = r_[range(powerflow.nlin), range(powerflow.nlin)]  ## double set of row indices

    Yf = sparse((r_[Yff, Yft], (i, r_[f, t])), (powerflow.nlin, powerflow.nbus))
    Yt = sparse((r_[Ytf, Ytt], (i, r_[f, t])), (powerflow.nlin, powerflow.nbus))

    ## build Ybus
    powerflow.Yb = sparse(
        Cf.T @ Yf
        + Ct.T @ Yt
        + sparse(
            (Ysh, (range(powerflow.nbus), range(powerflow.nbus))),
            (powerflow.nbus, powerflow.nbus),
        )
    )


def matrices(
    powerflow,
):
    """jacobian and hessian matrices

    Args
        powerflow:
    """

    ## Inicialização
    V = powerflow.solution["voltage"] * exp(1j * powerflow.solution["theta"])

    # Jacobiana
    dS_dVm, dS_dVa = dSbus_dV(powerflow.Yb, V)
    A11 = (dS_dVa.A[powerflow.maskP, :][:, powerflow.maskP]).real  # dP_dAngV
    A12 = (dS_dVm.A[powerflow.maskP, :][:, powerflow.maskQ]).real  # dP_dMagV
    A21 = (dS_dVa.A[powerflow.maskQ, :][:, powerflow.maskP]).imag  # dQ_AngV
    A22 = (dS_dVm.A[powerflow.maskQ, :][:, powerflow.maskQ]).imag  # dQ_MagV
    powerflow.jacobian = concatenate(
        (concatenate((A11, A21), axis=0), concatenate((A12, A22), axis=0)), axis=1
    )

    if powerflow.controlcount > 0:
        from ctrl import controljac

        controljac(
            powerflow,
        )

    if powerflow.solution["method"] == "EXPC":
        # Vetor Jacobiana-Lambda
        powerflow.G = powerflow.jacobian.T @ powerflow.solution["eigen"][
            powerflow.mask
        ].reshape((sum(powerflow.mask), 1))
        powerflow.H = powerflow.solution["eigen"][powerflow.mask]

        # Hessiana
        Gpaa, Gpav, Gpva, Gpvv = d2Sbus_dV2(
            powerflow.Yb, V, powerflow.solution["eigen"][: powerflow.nbus]
        )
        Gqaa, Gqav, Gqva, Gqvv = d2Sbus_dV2(
            powerflow.Yb,
            V,
            powerflow.solution["eigen"][powerflow.nbus : 2 * powerflow.nbus],
        )

        M1 = concatenate(
            (
                concatenate(
                    (
                        Gpaa.A[powerflow.maskP, :][:, powerflow.maskP],
                        Gpva.A[powerflow.maskQ, :][:, powerflow.maskP],
                    ),
                    axis=0,
                ),
                concatenate(
                    (
                        Gpav.A[powerflow.maskP, :][:, powerflow.maskQ],
                        Gpvv.A[powerflow.maskQ, :][:, powerflow.maskQ],
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
                        Gqaa.A[powerflow.maskP, :][:, powerflow.maskP],
                        Gqva.A[powerflow.maskQ, :][:, powerflow.maskP],
                    ),
                    axis=0,
                ),
                concatenate(
                    (
                        Gqav.A[powerflow.maskP, :][:, powerflow.maskQ],
                        Gqvv.A[powerflow.maskQ, :][:, powerflow.maskQ],
                    ),
                    axis=0,
                ),
            ),
            axis=1,
        )

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
    powerflow,
):
    """

    Args
        powerflow:
    """

    ## Inicialização
    load2ycte = diag(
        (
            powerflow.dbarDF.demanda_ativa.values
            - 1j * powerflow.dbarDF.demanda_reativa.values
        )
        * 1e-2
        / powerflow.solution["voltage"] ** 2
    )
    powerflow.Yb.A = powerflow.Yb.A + load2ycte


def md01jacob(
    powerflow,
    generator,
    gen,
):
    """matriz jacobiana

    Args
        powerflow:
    """

    ## Inicialização
    if gen == 0:
        powerflow.jacobiangenoffright = zeros(
            (2 * powerflow.nger, 2 * (powerflow.nger + powerflow.nbus))
        )
        powerflow.jacobiangenoffdown = zeros(
            (2 * (powerflow.nger + powerflow.nbus), 2 * powerflow.nger)
        )
        powerflow.jacobiangen = zeros((2, 2))
        powerflow.jacobiangen[0, 0] = 1
        powerflow.jacobiangen[0, 1] = -powerflow.dsimDF.step.values[0] * 0.5
        powerflow.jacobiangen[1, 0] = (
            (powerflow.dsimDF.step.values[0] * 0.5 / powerflow.generator[generator][1])
            * powerflow.solution["fem"][gen]
            * powerflow.solution["voltage"][generator - 1]
            * cos(
                powerflow.solution["delta"][gen]
                - powerflow.solution["theta"][generator - 1]
            )
            / powerflow.generator[generator][3]
        )
        powerflow.jacobiangen[1, 1] = (
            1
            + powerflow.dsimDF.step.values[0]
            * 0.5
            * powerflow.generator[generator][2]
            / powerflow.generator[generator][1]
        )

    else:
        powerflow.jacobiangen = concatenate(
            (powerflow.jacobiangen, zeros((powerflow.jacobiangen.shape[0], 2))), axis=1
        )
        powerflow.jacobiangen = concatenate(
            (powerflow.jacobiangen, zeros((2, powerflow.jacobiangen.shape[1]))), axis=0
        )

        powerflow.jacobiangen[2 * gen, 2 * gen] = 1
        powerflow.jacobiangen[2 * gen, 2 * gen + 1] = (
            -powerflow.dsimDF.step.values[0] * 0.5
        )
        powerflow.jacobiangen[2 * gen + 1, 2 * gen] = (
            (powerflow.dsimDF.step.values[0] * 0.5 / powerflow.generator[generator][1])
            * powerflow.solution["fem"][gen]
            * powerflow.solution["voltage"][generator - 1]
            * cos(
                powerflow.solution["delta"][gen]
                - powerflow.solution["theta"][generator - 1]
            )
            / powerflow.generator[generator][3]
        )
        powerflow.jacobiangen[2 * gen + 1, 2 * gen + 1] = (
            1
            + powerflow.dsimDF.step.values[0]
            * 0.5
            * powerflow.generator[generator][2]
            / powerflow.generator[generator][1]
        )

    powerflow.jacobiangenoffright[2 * gen + 1, generator - 1] = (
        (-powerflow.dsimDF.step.values[0] * 0.5 / powerflow.generator[generator][1])
        * powerflow.solution["fem"][gen]
        * powerflow.solution["voltage"][generator - 1]
        * cos(
            powerflow.solution["delta"][gen]
            - powerflow.solution["theta"][generator - 1]
        )
        / powerflow.generator[generator][3]
    )
    powerflow.jacobiangenoffright[2 * gen + 1, powerflow.nbus + generator - 1] = (
        (powerflow.dsimDF.step.values[0] * 0.5 / powerflow.generator[generator][1])
        * powerflow.solution["fem"][gen]
        * sin(
            powerflow.solution["delta"][gen]
            - powerflow.solution["theta"][generator - 1]
        )
        / powerflow.generator[generator][3]
    )
    powerflow.jacobiangenoffdown[generator - 1, 2 * gen] = (
        powerflow.solution["fem"][gen]
        * powerflow.solution["voltage"][generator - 1]
        * cos(
            powerflow.solution["delta"][gen]
            - powerflow.solution["theta"][generator - 1]
        )
        / powerflow.generator[generator][3]
    )
    powerflow.jacobiangenoffdown[generator - 1 + powerflow.nbus, 2 * gen] = (
        -powerflow.solution["fem"][gen]
        * powerflow.solution["voltage"][generator - 1]
        * sin(
            powerflow.solution["delta"][gen]
            - powerflow.solution["theta"][generator - 1]
        )
        / powerflow.generator[generator][3]
    )


def jacexsi(
    powerflow,
):
    """

    Args
        powerflow:
    """

    ## Inicialização
    dS_dVm, dS_dVa = dSbus_dV(
        powerflow.Yblc,
        concatenate((powerflow.solution["fem"], powerflow.solution["voltage"]), axis=0),
    )

    powerflow.jacobian = concatenate(
        (
            concatenate((dS_dVa.A.real, dS_dVa.A.imag), axis=0),
            concatenate((dS_dVm.A.real, dS_dVm.A.imag), axis=0),
        ),
        axis=1,
    )

    powerflow.jacobiangen = concatenate(
        (
            concatenate((powerflow.jacobiangen, powerflow.jacobiangenoffright), axis=1),
            concatenate((powerflow.jacobiangenoffdown, powerflow.jacobian), axis=1),
        ),
        axis=0,
    )
