# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from matplotlib import pyplot as plt
from numpy import append, array, degrees, sum

from folder import continuationfolder

def loading(
    self,
    powerflow,
):
    '''inicialização

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Criação automática de diretório
    continuationfolder(
        powerflow,
    )

    # Variáveis para geração dos gráficos de fluxo de potência continuado
    var(
        powerflow,
    )

    # # Gráficos de variáveis de estado e controle em função do carregamento
    # self.pqvt(
    #     powerflow,
    # )

    # # Gráfico de rootlocus
    # self.ruthe(powerflow,)

def var(
    self,
    powerflow,
):
    '''variáveis para geração dos gráficos de fluxo de potência continuado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variável
    powerflow.nbuspqtv = {}
    powerflow.MW = array([])
    powerflow.MVAr = array([])
    powerflow.nbuseigenvalues = array([])
    powerflow.nbuseigenvaluesPT = array([])
    powerflow.nbuseigenvaluesQV = array([])
    if 'FREQ' in powerflow.nbuscontrol:
        powerflow.nbuspqtv[
            'FREQbase' + str(powerflow.nbusoptions['FBASE'])
        ] = array([])

    # Loop de Inicialização da Variável
    for _, value in powerflow.nbusdbarraDF.iterrows():
        if value['tipo'] != 0:
            # Variável de Armazenamento de Potência Ativa
            powerflow.nbuspqtv['P-' + value['nome']] = array([])

            # Variável de Armazenamento de Potência Reativa
            powerflow.nbuspqtv['Q-' + value['nome']] = array([])

        elif (value['tipo'] == 0) and (
            ('SVCs' in powerflow.nbuscontrol)
            and (value['numero'] in powerflow.nbusdcerDF['barra'].to_numpy())
        ):
            # Variável de Armazenamento de Potência Reativa
            powerflow.nbuspqtv['Q-' + value['nome']] = array([])

        # Variável de Armazenamento de Magnitude de Tensão Corrigida
        powerflow.nbuspqtv['Vcorr-' + value['nome']] = array([])

        # Variável de Armazenamento de Defasagem Angular Corrigida
        powerflow.nbuspqtv['Tcorr-' + value['nome']] = array([])

    # Loop de Armazenamento
    for key, item in powerflow.case.items():
        # Condição
        if key == 0:
            self.aux = powerflow.nbusdbarraDF['nome'][0]  # usado no loop seguinte
            for value in range(0, item['voltage'].shape[0]):
                if powerflow.nbusdbarraDF['tipo'][value] != 0:
                    # Armazenamento de Potência Ativa
                    powerflow.nbuspqtv[
                        'P-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'P-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['active'][value],
                    )

                    # Armazenamento de Potência Reativa
                    powerflow.nbuspqtv[
                        'Q-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'Q-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['reactive'][value],
                    )

                elif (powerflow.nbusdbarraDF['tipo'][value] == 0) and (
                    ('SVCs' in powerflow.nbuscontrol)
                    and (
                        powerflow.nbusdbarraDF['numero'][value]
                        in powerflow.nbusdcerDF['barra'].to_numpy()
                    )
                ):
                    busidxcer = powerflow.nbusdcerDF.index[
                        powerflow.nbusdcerDF['barra']
                        == powerflow.nbusdbarraDF['numero'].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    powerflow.nbuspqtv[
                        'Q-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'Q-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['svc_reactive_generation'][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão
                powerflow.nbuspqtv[
                    'Vcorr-' + powerflow.nbusdbarraDF['nome'][value]
                ] = append(
                    powerflow.nbuspqtv[
                        'Vcorr-' + powerflow.nbusdbarraDF['nome'][value]
                    ],
                    item['voltage'][value],
                )

                # Variável de Armazenamento de Defasagem Angular
                powerflow.nbuspqtv[
                    'Tcorr-' + powerflow.nbusdbarraDF['nome'][value]
                ] = append(
                    powerflow.nbuspqtv[
                        'Tcorr-' + powerflow.nbusdbarraDF['nome'][value]
                    ],
                    degrees(item['theta'][value]),
                )

            # Demanda
            powerflow.MW = append(
                powerflow.MW, sum(powerflow.cpfsolution['demanda_ativa'])
            )
            powerflow.MVAr = append(
                powerflow.MVAr, sum(powerflow.cpfsolution['demanda_reativa'])
            )

            # Determinante e Autovalores
            if powerflow.cpfsolution['eigencalculation']:
                powerflow.nbuseigenvalues = append(
                    powerflow.nbuseigenvalues, item['eigenvalues']
                )
                powerflow.nbuseigenvaluesQV = append(
                    powerflow.nbuseigenvaluesQV, item['eigenvalues-QV']
                )

            # Frequência
            if 'FREQ' in powerflow.nbuscontrol:
                powerflow.nbuspqtv[
                    'FREQbase' + str(powerflow.nbusoptions['FBASE'])
                ] = append(
                    powerflow.nbuspqtv[
                        'FREQbase' + str(powerflow.nbusoptions['FBASE'])
                    ],
                    item['freq'] * powerflow.nbusoptions['FBASE'],
                )

        elif key > 0:
            for value in range(0, item['c']['voltage'].shape[0]):
                if powerflow.nbusdbarraDF['tipo'][value] != 0:
                    # Armazenamento de Potência Ativa
                    powerflow.nbuspqtv[
                        'P-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'P-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['c']['active'][value],
                    )

                    # Armazenamento de Potência Reativa
                    powerflow.nbuspqtv[
                        'Q-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'Q-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['c']['reactive'][value],
                    )

                elif (powerflow.nbusdbarraDF['tipo'][value] == 0) and (
                    ('SVCs' in powerflow.nbuscontrol)
                    and (
                        powerflow.nbusdbarraDF['numero'][value]
                        in powerflow.nbusdcerDF['barra'].to_numpy()
                    )
                ):
                    busidxcer = powerflow.nbusdcerDF.index[
                        powerflow.nbusdcerDF['barra']
                        == powerflow.nbusdbarraDF['numero'].iloc[value]
                    ].tolist()[0]

                    # Armazenamento de Potência Reativa
                    powerflow.nbuspqtv[
                        'Q-' + powerflow.nbusdbarraDF['nome'][value]
                    ] = append(
                        powerflow.nbuspqtv[
                            'Q-' + powerflow.nbusdbarraDF['nome'][value]
                        ],
                        item['c']['svc_reactive_generation'][busidxcer],
                    )

                # Armazenamento de Magnitude de Tensão Corrigida
                powerflow.nbuspqtv[
                    'Vcorr-' + powerflow.nbusdbarraDF['nome'][value]
                ] = append(
                    powerflow.nbuspqtv[
                        'Vcorr-' + powerflow.nbusdbarraDF['nome'][value]
                    ],
                    item['c']['voltage'][value],
                )

                # Variável de Armazenamento de Defasagem Angular Corrigida
                powerflow.nbuspqtv[
                    'Tcorr-' + powerflow.nbusdbarraDF['nome'][value]
                ] = append(
                    powerflow.nbuspqtv[
                        'Tcorr-' + powerflow.nbusdbarraDF['nome'][value]
                    ],
                    degrees(item['c']['theta'][value]),
                )

            # Demanda
            totalmw = sum(powerflow.cpfsolution['demanda_ativa'])
            totalmvar = sum(powerflow.cpfsolution['demanda_reativa'])
            for _, valueinc in powerflow.nbusdincDF.iterrows():
                if valueinc['tipo_incremento_1'] == 'AREA':
                    # MW
                    areamw = (1 + item['c']['step']) * sum(
                        array(
                            [
                                powerflow.cpfsolution['demanda_ativa'][idxarea]
                                for idxarea, valuearea in powerflow.nbusdbarraDF.iterrows()
                                if valuearea['area']
                                == valueinc['identificacao_incremento_1']
                            ]
                        )
                    )
                    totalmw += areamw - sum(
                        array(
                            [
                                powerflow.cpfsolution['demanda_ativa'][idxarea]
                                for idxarea, valuearea in powerflow.nbusdbarraDF.iterrows()
                                if valuearea['area']
                                == valueinc['identificacao_incremento_1']
                            ]
                        )
                    )

                    # MVAr
                    areamvar = (1 + item['c']['step']) * sum(
                        array(
                            [
                                powerflow.cpfsolution['demanda_reativa'][idxarea]
                                for idxarea, valuearea in powerflow.nbusdbarraDF.iterrows()
                                if valuearea['area']
                                == valueinc['identificacao_incremento_1']
                            ]
                        )
                    )
                    totalmvar += areamvar - sum(
                        array(
                            [
                                powerflow.cpfsolution['demanda_reativa'][idxarea]
                                for idxarea, valuearea in powerflow.nbusdbarraDF.iterrows()
                                if valuearea['area']
                                == valueinc['identificacao_incremento_1']
                            ]
                        )
                    )

                elif powerflow.nbusdincDF.loc[0, 'tipo_incremento_1'] == 'BARR':
                    # MW
                    barramw = (1 + item['c']['step']) * powerflow.cpfsolution[
                        'demanda_ativa'
                    ][
                        powerflow.nbusdincDF.loc[0, 'identificacao_incremento_1']
                        - 1
                    ]
                    totalmw += (
                        barramw
                        - powerflow.cpfsolution['demanda_ativa'][
                            powerflow.nbusdincDF.loc[
                                0, 'identificacao_incremento_1'
                            ]
                            - 1
                        ]
                    )

                    # MVAr
                    barramvar = (1 + item['c']['step']) * powerflow.cpfsolution[
                        'demanda_reativa'
                    ][
                        powerflow.nbusdincDF.loc[0, 'identificacao_incremento_1']
                        - 1
                    ]
                    totalmvar += (
                        barramvar
                        - powerflow.cpfsolution['demanda_reativa'][
                            powerflow.nbusdincDF.loc[
                                0, 'identificacao_incremento_1'
                            ]
                            - 1
                        ]
                    )

            powerflow.MW = append(powerflow.MW, totalmw)
            powerflow.MVAr = append(powerflow.MVAr, totalmvar)

            # Determinante e Autovalores
            if powerflow.cpfsolution['eigencalculation']:
                powerflow.nbuseigenvalues = append(
                    powerflow.nbuseigenvalues, item['c']['eigenvalues']
                )
                powerflow.nbuseigenvaluesQV = append(
                    powerflow.nbuseigenvaluesQV, item['c']['eigenvalues-QV']
                )

            # Frequência
            if 'FREQ' in powerflow.nbuscontrol:
                powerflow.nbuspqtv[
                    'FREQbase' + str(powerflow.nbusoptions['FBASE'])
                ] = append(
                    powerflow.nbuspqtv[
                        'FREQbase' + str(powerflow.nbusoptions['FBASE'])
                    ],
                    item['c']['freq'] * powerflow.nbusoptions['FBASE'],
                )

def pqvt(
    self,
    powerflow,
):
    '''geração e armazenamento de gráficos de variáveis de estado e controle em função do carregamento

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Geração de Gráfico
    color = 0
    for key, item in powerflow.nbuspqtv.items():
        if (key[:5] != 'Vprev') and (key[:5] != 'Tprev'):
            fig, ax = plt.subplots(nrows=1, ncols=1)

            # Variáveis
            if key[1:5] == 'c':
                busname = key[6:]
            else:
                busname = key[2:]
            if busname != self.aux:
                if key[1:5] == 'c':
                    self.aux = key[6:]
                else:
                    self.aux = key[2:]
                color += 1

            # Plot
            (line,) = ax.plot(
                powerflow.MW[: powerflow.nbuspmcidx + 1],
                item[: powerflow.nbuspmcidx + 1],
                color=f'C{color}',
                linestyle='solid',
                linewidth=2,
                alpha=0.85,
                label=busname,
                zorder=2,
            )

            if powerflow.nbusoptions['FULL']:
                (dashed,) = ax.plot(
                    powerflow.MW[
                        (powerflow.nbuspmcidx + 1) : (powerflow.nbusv2lidx)
                    ],
                    item[(powerflow.nbuspmcidx + 1) : (powerflow.nbusv2lidx)],
                    color=f'C{color}',
                    linestyle='dashed',
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                (dotted,) = ax.plot(
                    powerflow.MW[powerflow.nbusv2lidx :],
                    item[powerflow.nbusv2lidx :],
                    color=f'C{color}',
                    linestyle='dotted',
                    linewidth=2,
                    alpha=0.85,
                    label=busname,
                    zorder=2,
                )
                ax.legend([(line, dashed, dotted)], [busname])

            elif not powerflow.nbusoptions['FULL']:
                ax.legend([(line,)], [busname])

            # Labels
            # Condição de Potência Ativa
            if key[0] == 'P':
                ax.set_title('Variação da Geração de Potência Ativa')
                ax.set_ylabel('Geração de Potência Ativa [MW]')

            # Condição de Potência Reativa
            elif key[0] == 'Q':
                ax.set_title('Variação da Geração de Potência Reativa')
                ax.set_ylabel('Geração de Potência Reativa [MVAr]')

            # Magnitude de Tensão Nodal
            if key[0] == 'V':
                ax.set_title('Variação da Magnitude de Tensão do Barramento')
                ax.set_ylabel('Magnitude de Tensão do Barramento [p.u.]')

            # Defasagem Angular de Tensão Nodal
            elif key[0] == 'T':
                ax.set_title('Variação da Defasagem Angular do Barramento')
                ax.set_ylabel('Defasagem Angular do Barramento [graus]')

            # Frequência
            elif key[0] == 'F':
                ax.set_title('Variação da Frequência do SEP')
                ax.set_ylabel('Frequência [Hz]')

            ax.set_xlabel('Carregamento [MW]')
            ax.grid()

        # Save
        fig.savefig(
            powerflow.nbusdircpfsysimag + key[0] + '-' + busname + '.png', dpi=400
        )
        plt.close(fig)

def ruthe(
    self,
    powerflow,
):
    '''geração e armazenamento de gráfico rootlocus

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Variáveis
    rows = list(powerflow.case.keys())[-1]
    cols = sum(powerflow.nbusmask)
    colsP = sum(powerflow.nbusmaskP)
    colsQ = sum(powerflow.nbusmaskQ)

    # Reconfiguração
    powerflow.nbuseigenvalues = powerflow.nbuseigenvalues.reshape(
        rows, cols
    ).T.astype(dtype=complex)
    powerflow.nbuseigenvaluesPT = powerflow.nbuseigenvaluesPT.reshape(
        rows, colsP
    ).T.astype(dtype=complex)
    powerflow.nbuseigenvaluesQV = powerflow.nbuseigenvaluesQV.reshape(
        rows, colsQ
    ).T.astype(dtype=complex)

    # Geração de Gráfico - Autovalores da matriz Jacobiana Reduzida
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, cols):
        ax.scatter(
            -powerflow.nbuseigenvalues.real[eigen, 0],
            powerflow.nbuseigenvalues.imag[eigen, 0],
            marker='x',
            color=f'C{color}',
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvalues.real[eigen, :],
            powerflow.nbuseigenvalues.imag[eigen, :],
            color=f'C{color}',
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)

    ax.set_title('Autovalores da Matriz Jacobiana Reduzida')
    ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
    ax.set_xlabel(f'Eixo Real ($\sigma$)')

    # Save
    fig.savefig(
        powerflow.nbusdircpfsys
        + powerflow.nbusname
        + '-rootlocus-Jacobian.png',
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensisbilidade PT
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsP):
        ax.scatter(
            -powerflow.nbuseigenvaluesPT.real[eigen, 0],
            powerflow.nbuseigenvaluesPT.imag[eigen, 0],
            marker='x',
            color=f'C{color}',
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvaluesPT.real[eigen, :],
            powerflow.nbuseigenvaluesPT.imag[eigen, :],
            color=f'C{color}',
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)

    ax.set_title(f'Autovalores da Matriz de Sensibilidade $P\\theta$')
    ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
    ax.set_xlabel(f'Eixo Real ($\sigma$)')

    # Save
    fig.savefig(
        powerflow.nbusdircpfsys + powerflow.nbusname + '-rootlocus-PTsens.png',
        dpi=400,
    )
    plt.close(fig)

    # Geração de Gráfico - Autovalores da matriz de sensibilidade QV
    fig, ax = plt.subplots(nrows=1, ncols=1)
    color = 0
    for eigen in range(0, colsQ):
        ax.scatter(
            -powerflow.nbuseigenvaluesQV.real[eigen, 0],
            powerflow.nbuseigenvaluesQV.imag[eigen, 0],
            marker='x',
            color=f'C{color}',
            alpha=1,
            zorder=3,
        )
        ax.plot(
            -powerflow.nbuseigenvaluesQV.real[eigen, :],
            powerflow.nbuseigenvaluesQV.imag[eigen, :],
            color=f'C{color}',
            linewidth=2,
            alpha=0.85,
            zorder=2,
        )
        color += 1

    ax.axhline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)
    ax.axvline(0.0, linestyle=':', color='k', linewidth=0.75, zorder=-20)

    ax.set_title(f'Autovalores da Matriz de Sensibilidade $QV$')
    ax.set_ylabel(f'Eixo Imaginário ($j\omega$)')
    ax.set_xlabel(f'Eixo Real ($\sigma$)')

    # Save
    fig.savefig(
        powerflow.nbusdircpfsys + powerflow.nbusname + '-rootlocus-QVsens.png',
        dpi=400,
    )
    plt.close(fig)
