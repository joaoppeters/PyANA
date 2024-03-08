import numpy as np

from sympy import Symbol, sin, cos
from sympy.functions import exp


qg = Symbol("Qg")
qmax = Symbol("Qmax")
qmin = Symbol("Qmin")
v = Symbol("V")
vesp = Symbol("Vesp")

tolq = 1e-8
tolv = 1e-8
inc = 1e10

ch1 = 1 / (1 + exp(-1 * inc * (qg - qmax + tolq)))
print(
    int(
        ch1.subs(
            {
                qg: 0.65 - tolq,
                qmax: 0.65,
            }
        )
    )
)

ch2 = 1 / (1 + exp(+1 * inc * (qg - qmin - tolq)))
print(
    int(
        ch2.subs(
            {
                qg: 0.65 - tolq,
                qmin: -99.99,
            }
        )
    )
)

ch3 = 1 / (1 + exp(+1 * inc * (v - vesp - tolv)))
print(
    int(
        ch3.subs(
            {
                vesp: 1.0,
                v: 1.0,
            }
        )
    )
)

ch4 = 1 / (1 + exp(-1 * inc * (v - vesp + tolv)))
print(
    int(
        ch4.subs(
            {
                vesp: 1.0,
                v: 1.0,
            }
        )
    )
)

# % diff(ch1) È igual a (1 - ch1) * ch1
# % mas eles apresentam a mesma resposta de formas diferentes!


y_normal = (1 - ch1 * ch3) * (1 - ch2 * ch4) * (v - vesp)
y_qmax = (ch1 * ch3) * (1 - ch2 * ch4) * (qg - qmax)
y_qmin = (1 - ch1 * ch3) * (ch2 * ch4) * (qg - qmin)


theta = Symbol("Theta")
# v = Symbol('v')
V2 = Symbol("V2")
X = Symbol("X")

# % ConstruÁ„o da Matriz Jacobiana - SEP Duas Barras Milano - PQ + VT
# % J = [ dP2/dT2  dP2/dv  dP2/dV2  dP2/dQ1
# %       dQ1/dT2  dQ1/dv  dQ1/dV2  dQ1/dQ1
# %       dQ2/dT2  dQ2/dv  dQ2/dV2  dQ2/dQ1
# %        dy/dT2   dy/dv   dy/dV2   dy/dQ1]

# % X = 0.15788 pu

# % v = 1.0000 pu
# % T1 = 0.0000 rad

# % V2 = 0.9473 pu
# % T2 = 0.3261 rad


## EQUAÇÃO DE POTÊNCIA ATIVA DA BARRA 1 - REFERÊNCIA BARRA SLACK ##
P2 = (v * V2 * sin(theta)) / X
dP2dT2 = P2.diff(theta)
dP2dT2 = dP2dT2.subs(
    {
        v: 1.0,
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dP2dv = P2.diff(v)
dP2dv = dP2dv.subs(
    {
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dP2dV2 = P2.diff(V2)
dP2dV2 = dP2dV2.subs(
    {
        v: 1.0,
        theta: -0.3261,
        X: 0.15788,
    }
)

dP2dQ1 = 0


## EQUAÇÃO DE POTÊNCIA REATIVA DA BARRA 1 - REFERÊNCIA BARRA SLACK ##
Q1 = ((v * V2 * cos(theta)) - (v * v)) / X
dQ1dT2 = Q1.diff(theta)
dQ1dT2 = dQ1dT2.subs(
    {
        v: 1.0,
        V2: 0.9473,
        theta: 0.3261,
        X: 0.15788,
    }
)

dQ1dv = Q1.diff(v)
dQ1dv = -dQ1dv.subs(
    {
        v: 1.0,
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dQ1dV2 = -Q1.diff(V2)
dQ1dV2 = dQ1dV2.subs(
    {
        v: 1.0,
        theta: -0.3261,
        X: 0.15788,
    }
)

dQ1dQ1 = -1


## EQUAÇÃO DE POTÊNCIA REATIVA DA BARRA 2 - REFERÊNCIA BARRA SLACK ##
Q2 = (-(v * V2 * cos(theta)) + (V2 * V2)) / X
dQ2dT2 = Q2.diff(theta)
dQ2dT2 = dQ2dT2.subs(
    {
        v: 1.0,
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dQ2dv = Q2.diff(v)
dQ2dv = dQ2dv.subs(
    {
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dQ2dV2 = Q2.diff(V2)
dQ2dV2 = dQ2dV2.subs(
    {
        v: 1.0,
        V2: 0.9473,
        theta: -0.3261,
        X: 0.15788,
    }
)

dQ2dQ1 = 0


## EQUAÇÕES DE CONTROLE ADICIONAIS ##
dydT2 = 0

dydv = (y_normal + y_qmax + y_qmin).diff(v)
dydv = dydv.subs(
    {
        qg: 0.650001,
        qmax: 0.65,
        qmin: -99.99,
        v: 1.0,
        vesp: 1.0,
    }
)

dydV2 = 0

dydQ1 = (y_normal + y_qmax + y_qmin).diff(qg)
dydQ1 = dydQ1.subs(
    {
        qg: 0.650001,
        qmax: 0.65,
        qmin: -99.99,
        v: 1.0,
        vesp: 1.0,
    }
)


J = np.array(
    [
        [dP2dT2, dP2dv, dP2dV2, dP2dQ1],
        [dQ1dT2, dQ1dv, dQ1dV2, dQ1dQ1],
        [dQ2dT2, dQ2dv, dQ2dV2, dQ2dQ1],
        [dydT2, int(dydv), dydV2, int(dydQ1)],
    ]
)

print(J)
