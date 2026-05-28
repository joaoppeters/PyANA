# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def exlf(
    anarede,
):
    """chamada automatica do metodo de solucao numerico newton-raphson nao-linear

    Args
        anarede: objeto da classe PowerFlowContainer
    """
    from matrices import admittance
    from newton import newton
    from report import reportfile

    admittance(
        anarede,
    )

    newton(
        anarede,
    )

    reportfile(
        anarede,
    )


def exic(
    anarede,
):
    """chamada automatica do metodo de solucao de fluxo de potencia continuado
    utilizando predicao-correcao e solucao numerica newton-raphson nao-linear
    aplicacao do metodo desenvolvildo por V. Ajjarapu e C. Christy (1992)

    Args
        anarede: objeto da classe PowerFlowContainer
    """

    from matrices import admittance
    from continuation import prediction_correction
    from newton import newton
    from report import reportfile

    admittance(
        anarede,
    )

    newton(
        anarede,
    )

    prediction_correction(
        anarede,
    )

    reportfile(
        anarede,
    )


def expc(
    anarede,
):
    """chamada automatica do metodo de solucao do ponto de colapso
    aplicacao do metodo desenvolvido por C. Canizares et al (1998)

    Args
        anarede: objeto da classe PowerFlowContainer
    """
    from matrices import admittance
    from newton import newton
    from poc import poc
    from report import reportfile

    admittance(
        anarede,
    )

    newton(
        anarede,
    )

    poc(
        anarede,
    )

    reportfile(
        anarede,
    )


def exsi(
    anarede,
    anatem,
):
    """chamada automatica do metodo de simulacao dinâmica

    Args
        anarede: objeto da classe PowerFlowContainer
        anatem: objeto da classe PowerFlowContainer
    """
    from matrices import admittance
    from dynamic import dynamic
    from newton import newton
    from path import pathstb
    from stb import stb

    pathstb(
        anarede,
        anatem,
    )

    stb(
        anatem,
    )

    # admittance(
    #     anatem,
    # )

    # newton(
    #     anatem,
    # )

    # dynamic(
    #     anatem,
    # )


def exct(
    anarede,
):
    """chamada automatica do metodo de solucao numerico newton-raphson nao-linear
    com foco em analise de contingencias (criterio N-1)

    Args
        anarede: objeto da classe PowerFlowContainer
    """
    from matrices import admittance
    from newton import newton
    from report import reportfile

    trueDLIN = anarede.dlinDF.copy()
    anarede.exct = dict()
    # anarede.exct["convergente"] = list()
    # anarede.exct["divergente"] = list()

    if anarede.pwfblock["DCTG"]:
        pass
    else:
        print(
            f"\033[94mIniciando analise de contingencias (criterio N-1) para {trueDLIN.shape[0]} linhas...\033[00m"
        )
        anarede.nlin -= 1
        for idx, value in anarede.dlinDF.iterrows():
            print(f"Simulando contingência do circuito {value.de} - {value.para}...")
            anarede.dlinDF = anarede.dlinDF.drop(idx)
            admittance(
                anarede,
            )
            newton(
                anarede,
            )
            anarede.exct[f"{value.de} - {value.para}"] = anarede.solution.copy()
            if anarede.solution["convergence"] == "SISTEMA CONVERGENTE":
                print("\033[92mSISTEMA CONVERGENTE\033[00m")
            else:
                print("\033[91mSISTEMA DIVERGENTE\033[00m")

            anarede.dlinDF = trueDLIN.copy()

        reportfile(
            anarede,
        )
