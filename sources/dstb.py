# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from copy import deepcopy
from unittest.mock import DEFAULT
from numpy import nan
from os.path import dirname, exists
from pandas import DataFrame as DF

DEFAULT = ""


def darq(
    anatem,
):
    """inicialização para leitura de dados de entrada e saida de arquivos

    Args
        anatem:
    """
    ## Inicialização
    anatem.darq["tipo"] = list()
    anatem.darq["c"] = list()
    anatem.darq["nome"] = list()

    while anatem.lines[anatem.linecount].strip() not in anatem.end_block:
        if anatem.lines[anatem.linecount][0] == anatem.comment:
            pass
        else:
            anatem.darq["tipo"].append(anatem.lines[anatem.linecount][:6])
            anatem.darq["c"].append(anatem.lines[anatem.linecount][7:10])
            anatem.darq["nome"].append(anatem.lines[anatem.linecount][11:168])
        anatem.linecount += 1

    # DataFrame dos Dados de Agregadores Genericos
    anatem.darqDF = DF(data=anatem.darq)
    anatem.darq = deepcopy(anatem.darqDF)
    anatem.darqDF = anatem.darqDF.replace(r"^\s*$", "0", regex=True)
    anatem.darqDF = anatem.darqDF.astype(
        {
            "tipo": "object",
            "c": "object",
            "nome": "str",
        }
    )

    if anatem.darqDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DARQ`!\033[0m"
        )
    else:
        anatem.stbblock["DARQ"] = True


def dcar(
    anatem,
):
    """inicialização para leitura de Args A, B, C e D que estabelecem a curva de variação de carga em relação a magnitude de tensão nas barras

    Args
        anatem:
    """
    ## Inicialização (mantive sua estrutura)
    anatem.dcar["tipo_elemento_1"] = list()
    anatem.dcar["identificacao_elemento_1"] = list()
    anatem.dcar["condicao_elemento_1"] = list()
    anatem.dcar["tipo_elemento_2"] = list()
    anatem.dcar["identificacao_elemento_2"] = list()
    anatem.dcar["condicao_elemento_2"] = list()
    anatem.dcar["tipo_elemento_3"] = list()
    anatem.dcar["identificacao_elemento_3"] = list()
    anatem.dcar["condicao_elemento_3"] = list()
    anatem.dcar["tipo_elemento_4"] = list()
    anatem.dcar["identificacao_elemento_4"] = list()
    anatem.dcar["operacao"] = list()
    anatem.dcar["parametro_A"] = list()
    anatem.dcar["parametro_B"] = list()
    anatem.dcar["parametro_C"] = list()
    anatem.dcar["parametro_D"] = list()
    anatem.dcar["tensao_limite"] = list()

    # loop protegido contra estouro de índice
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        # se linha vazia ou comentário: apenas avança
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # extrai com safe_slice; use require_full=True se quiser forçar comprimento exato
        anatem.dcar["tipo_elemento_1"].append(safe_slice(line, 0, 4))
        anatem.dcar["identificacao_elemento_1"].append(safe_slice(line, 5, 10))
        anatem.dcar["condicao_elemento_1"].append(safe_slice(line, 11, 12))
        anatem.dcar["tipo_elemento_2"].append(safe_slice(line, 13, 17))
        anatem.dcar["identificacao_elemento_2"].append(safe_slice(line, 18, 23))
        anatem.dcar["condicao_elemento_2"].append(safe_slice(line, 24, 25))
        anatem.dcar["tipo_elemento_3"].append(safe_slice(line, 26, 30))
        anatem.dcar["identificacao_elemento_3"].append(safe_slice(line, 31, 36))
        anatem.dcar["condicao_elemento_3"].append(safe_slice(line, 37, 38))
        anatem.dcar["tipo_elemento_4"].append(safe_slice(line, 39, 43))
        anatem.dcar["identificacao_elemento_4"].append(safe_slice(line, 44, 49))
        anatem.dcar["operacao"].append(safe_slice(line, 50, 51))
        anatem.dcar["parametro_A"].append(safe_slice(line, 52, 55))
        anatem.dcar["parametro_B"].append(safe_slice(line, 56, 59))
        anatem.dcar["parametro_C"].append(safe_slice(line, 60, 63))
        anatem.dcar["parametro_D"].append(safe_slice(line, 64, 67))
        anatem.dcar["tensao_limite"].append(safe_slice(line, 68, 72))

        anatem.linecount += 1


def dcdu(
    anatem,
):
    """leitura de arquivo .cdu associado ao dado de entrada DARQ

    Args
        anatem:
    """
    ## Inicialização
    # proteção: se linecount for maior que número de linhas, sai
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line == "":
            # linha vazia: apenas avança
            anatem.linecount += 1
            continue

        if line[0] == anatem.comment:
            # comentário: apenas avança
            anatem.linecount += 1
            continue

        # bloco interno: lê até "FIMCDU" ou até acabar as linhas
        while (
            0 <= anatem.linecount < len(anatem.lines)
            and anatem.lines[anatem.linecount].strip() != "FIMCDU"
        ):
            line = anatem.lines[anatem.linecount].rstrip("\n")

            # comentário
            if line == "" or line[0] == anatem.comment:
                anatem.linecount += 1
                continue

            # cuidado com anatem.linecount == 0 quando acessar linha anterior
            prev_line = (
                anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
            )

            # ncdu ruler: cria novo ncdu
            if prev_line[:] in anatem.dcdu.get("ncdu_ruler", ""):
                ncdu = safe_slice(line, 0, 6)
                anatem.dcdu[ncdu] = {
                    "nome": safe_slice(line, 7, 19),
                    "defpar": list(),
                    "defpar_nome": list(),
                    "defpar_valor": list(),
                    "bloco_numero": list(),
                    "bloco_inicializacao": list(),
                    "bloco_tipo": list(),
                    "bloco_omitir": list(),
                    "bloco_subtipo": list(),
                    "bloco_sinal": list(),
                    "bloco_entrada": list(),
                    "bloco_saida": list(),
                    "bloco_parametro1": list(),
                    "bloco_parametro2": list(),
                    "bloco_parametro3": list(),
                    "bloco_parametro4": list(),
                    "bloco_limite_minimo": list(),
                    "bloco_limite_maximo": list(),
                    "defval": list(),
                    "defval_subtipo": list(),
                    "defval_variavel": list(),
                    "defval_parametro_d1": list(),
                    "defval_exclusao": list(),
                    "defval_parametro_d2": list(),
                }

            # DEFPAR
            elif prev_line[:] == anatem.dcdu.get("defpar_ruler", "") or (
                line.split()[0] == "DEFPAR" if line.split() else False
            ):
                anatem.dcdu[ncdu]["defpar"].append(safe_slice(line, 0, 6))
                anatem.dcdu[ncdu]["defpar_nome"].append(safe_slice(line, 7, 13))
                anatem.dcdu[ncdu]["defpar_valor"].append(safe_slice(line, 14, 32))

            # DEFVAL
            elif prev_line[:] == anatem.dcdu.get("defval_ruler", "") or (
                line.split()[0] == "DEFVAL" if line.split() else False
            ):
                anatem.dcdu[ncdu]["defval"].append(safe_slice(line, 0, 6))
                anatem.dcdu[ncdu]["defval_subtipo"].append(safe_slice(line, 7, 13))
                anatem.dcdu[ncdu]["defval_variavel"].append(safe_slice(line, 14, 20))
                # para parâmetros curtos, você pode exigir fatia completa: require_full=True
                anatem.dcdu[ncdu]["defval_parametro_d1"].append(
                    safe_slice(line, 21, 27, default=DEFAULT, require_full=False)
                )
                # caractere único: use slice 27:28 (seguro)
                anatem.dcdu[ncdu]["defval_exclusao"].append(safe_slice(line, 27, 28))
                anatem.dcdu[ncdu]["defval_parametro_d2"].append(
                    safe_slice(line, 28, 34)
                )

            # bloco padrão (outras linhas)
            else:
                anatem.dcdu[ncdu]["bloco_numero"].append(safe_slice(line, 0, 4))
                anatem.dcdu[ncdu]["bloco_inicializacao"].append(safe_slice(line, 4, 5))
                anatem.dcdu[ncdu]["bloco_tipo"].append(safe_slice(line, 5, 11))
                anatem.dcdu[ncdu]["bloco_omitir"].append(safe_slice(line, 11, 12))
                anatem.dcdu[ncdu]["bloco_subtipo"].append(safe_slice(line, 12, 18))
                anatem.dcdu[ncdu]["bloco_sinal"].append(safe_slice(line, 18, 19))
                anatem.dcdu[ncdu]["bloco_entrada"].append(safe_slice(line, 19, 25))
                anatem.dcdu[ncdu]["bloco_saida"].append(safe_slice(line, 26, 32))
                anatem.dcdu[ncdu]["bloco_parametro1"].append(safe_slice(line, 33, 39))
                anatem.dcdu[ncdu]["bloco_parametro2"].append(safe_slice(line, 39, 45))
                anatem.dcdu[ncdu]["bloco_parametro3"].append(safe_slice(line, 45, 51))
                anatem.dcdu[ncdu]["bloco_parametro4"].append(safe_slice(line, 51, 57))
                anatem.dcdu[ncdu]["bloco_limite_minimo"].append(
                    safe_slice(line, 58, 64)
                )
                anatem.dcdu[ncdu]["bloco_limite_maximo"].append(
                    safe_slice(line, 64, 70)
                )

            anatem.linecount += 1

        # avança além do marcador FIMCDU (se estiver dentro dos limites)
        anatem.linecount += 1
        # proteção: evita loop infinito se ultrapassar número de linhas
        if anatem.linecount >= len(anatem.lines):
            break


def dcst(
    anatem,
):
    """inicialização para leitura de dados de constantes

    Args
        anatem:
    """
    ## Inicialização
    # proteção: evita erro se linecount estiver fora do intervalo
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # comentário ou linha vazia -> apenas avança
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # prev_line seguro (quando linecount == 0, prev_line = "")
        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""

        # se a linha anterior é o ruler, cria novo registro
        if prev_line[:] == anatem.dcst.get("ruler", ""):
            nbus = safe_slice(line, 0, 4)
            anatem.dcst[nbus] = {
                "tipo": safe_slice(line, 7, 8),
                "parametro_1": safe_slice(line, 9, 17),
                "parametro_2": safe_slice(line, 18, 26),
                "parametro_3": safe_slice(line, 27, 35),
            }
            anatem.linecount += 1
            continue

        # se chegou aqui não é comentário nem ruler: apenas avança
        anatem.linecount += 1


def dcte(
    anatem,
):
    """inicialização para leitura de dados de constantes

    Args
        anatem:
    """
    ## Inicialização
    anatem.dcte["constante"] = list()
    anatem.dcte["valor_constante"] = list()

    # Proteção: garante que linecount esteja dentro do intervalo
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # pular linhas vazias e comentários
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # leitura segura usando safe_slice
        anatem.dcte["constante"].append(safe_slice(line, 0, 4))
        anatem.dcte["valor_constante"].append(safe_slice(line, 5, 11))

        anatem.linecount += 1

    # DataFrame dos Dados de Constantes
    anatem.dcteDF = DF(data=anatem.dcte)
    anatem.dcte = deepcopy(anatem.dcteDF)
    anatem.dcteDF = anatem.dcteDF.replace(r"^\s*$", "0", regex=True)
    anatem.dcteDF = anatem.dcteDF.astype(
        {
            "constante": "object",
            "valor_constante": "float",
        }
    )
    if anatem.dcteDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DCTE`!\033[0m"
        )
    else:
        anatem.stbblock["DCTE"] = True

        # substitui "0" por NaN, remove linhas sem constante e mantém a última ocorrência
        anatem.dcteDF["constante"] = anatem.dcteDF["constante"].replace(
            "0", float("nan")
        )
        anatem.dcteDF = anatem.dcteDF.dropna(axis=0, subset=["constante"])
        anatem.dcteDF = anatem.dcteDF.drop_duplicates(
            subset=["constante"], keep="last"
        ).reset_index(drop=True)


def devt(
    anatem,
):
    """inicialização para leitura de dados de eventos

    Args
        anatem:
    """
    ## Inicialização
    anatem.devt["tipo"] = list()
    anatem.devt["tempo"] = list()
    anatem.devt["elemento"] = list()
    anatem.devt["para"] = list()
    anatem.devt["ncircuito"] = list()
    anatem.devt["extremidade"] = list()
    anatem.devt["v-percentual"] = list()
    anatem.devt["v-absoluto"] = list()
    anatem.devt["grupo"] = list()
    anatem.devt["unidades"] = list()
    anatem.devt["bloco-cdu"] = list()
    anatem.devt["polaridade"] = list()
    anatem.devt["resistencia"] = list()
    anatem.devt["reatancia"] = list()
    anatem.devt["susceptancia"] = list()
    anatem.devt["defasagem"] = list()

    # loop protegido contra estouro de índice
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # pular linhas vazias e comentários
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # extrai com safe_slice; ajuste require_full=True se quiser exigir comprimento exato em algum campo
        anatem.devt["tipo"].append(safe_slice(line, 0, 4))
        anatem.devt["tempo"].append(safe_slice(line, 5, 13))
        anatem.devt["elemento"].append(safe_slice(line, 13, 19))
        anatem.devt["para"].append(safe_slice(line, 19, 24))
        anatem.devt["ncircuito"].append(safe_slice(line, 24, 26))
        anatem.devt["extremidade"].append(safe_slice(line, 26, 31))
        anatem.devt["v-percentual"].append(safe_slice(line, 32, 37))
        anatem.devt["v-absoluto"].append(safe_slice(line, 38, 44))
        anatem.devt["grupo"].append(safe_slice(line, 45, 47))
        anatem.devt["unidades"].append(safe_slice(line, 48, 51))
        anatem.devt["bloco-cdu"].append(safe_slice(line, 60, 64))
        anatem.devt["polaridade"].append(safe_slice(line, 64, 65))
        anatem.devt["resistencia"].append(safe_slice(line, 66, 72))
        anatem.devt["reatancia"].append(safe_slice(line, 73, 79))
        anatem.devt["susceptancia"].append(safe_slice(line, 80, 86))
        anatem.devt["defasagem"].append(safe_slice(line, 87, 94))

        anatem.linecount += 1

    # DataFrame dos Dados de Alteração do Nível de Carregamento
    anatem.devtDF = DF(data=anatem.devt)
    anatem.devt = deepcopy(anatem.devtDF)
    # substitui campos vazios por "0" para conversão segura
    anatem.devtDF = anatem.devtDF.replace(r"^\s*$", "0", regex=True)
    # ordena por tempo (já convertido a string "0" para float abaixo)
    anatem.devtDF = anatem.devtDF.sort_values(by=["tempo"], ascending=True)
    # converte tipos (se alguma conversão falhar levanta exceção)
    anatem.devtDF = anatem.devtDF.astype(
        {
            "tipo": "object",
            "tempo": "float",
            "elemento": "int",
            "para": "int",
            "ncircuito": "int",
            "extremidade": "int",
            "v-percentual": "float",
            "v-absoluto": "float",
            "grupo": "int",
            "unidades": "int",
            "bloco-cdu": "int",
            "polaridade": "object",
            "resistencia": "float",
            "reatancia": "float",
            "susceptancia": "float",
            "defasagem": "float",
        }
    )
    if anatem.devtDF.empty:
        # se vazio, mantém comportamento anterior (pass)
        pass
    else:
        anatem.stbblock["DEVT"] = True


def dger(
    anatem,
):
    """inicialização para leitura de dados de alteração do nível de carregamento

    Args
        anatem:
    """
    ## Inicialização
    anatem.dger["tipo_elemento_1"] = list()
    anatem.dger["identificacao_elemento_1"] = list()
    anatem.dger["condicao_1"] = list()
    anatem.dger["tipo_elemento_2"] = list()
    anatem.dger["identificacao_elemento_2"] = list()
    anatem.dger["condicao_2"] = list()
    anatem.dger["tipo_elemento_3"] = list()
    anatem.dger["identificacao_elemento_3"] = list()
    anatem.dger["condicao_3"] = list()
    anatem.dger["tipo_elemento_4"] = list()
    anatem.dger["identificacao_elemento_4"] = list()
    anatem.dger["parametro_A"] = list()
    anatem.dger["parametro_B"] = list()
    anatem.dger["parametro_C"] = list()
    anatem.dger["parametro_D"] = list()
    anatem.dger["tensao_bloqueio_potencia_ativa"] = list()
    anatem.dger["tensao_desbloqueio_potencia_ativa"] = list()
    anatem.dger["tensao_bloqueio_potencia_reativa"] = list()
    anatem.dger["tensao_desbloqueio_potencia_reativa"] = list()

    # loop protegido contra estouro de índice
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # pular linhas vazias e comentários
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # extrai com safe_slice; se quiser exigir comprimento exato para alguns campos,
        # use require_full=True nesse safe_slice específico
        anatem.dger["tipo_elemento_1"].append(safe_slice(line, 0, 4))
        anatem.dger["identificacao_elemento_1"].append(safe_slice(line, 5, 10))
        anatem.dger["condicao_1"].append(safe_slice(line, 11, 12))
        anatem.dger["tipo_elemento_2"].append(safe_slice(line, 13, 17))
        anatem.dger["identificacao_elemento_2"].append(safe_slice(line, 18, 23))
        anatem.dger["condicao_2"].append(safe_slice(line, 24, 25))
        anatem.dger["tipo_elemento_3"].append(safe_slice(line, 26, 30))
        anatem.dger["identificacao_elemento_3"].append(safe_slice(line, 31, 36))
        anatem.dger["condicao_3"].append(safe_slice(line, 37, 38))
        anatem.dger["tipo_elemento_4"].append(safe_slice(line, 39, 43))
        anatem.dger["identificacao_elemento_4"].append(safe_slice(line, 44, 49))
        anatem.dger["parametro_A"].append(safe_slice(line, 52, 55))
        anatem.dger["parametro_B"].append(safe_slice(line, 56, 59))
        anatem.dger["parametro_C"].append(safe_slice(line, 60, 63))
        anatem.dger["parametro_D"].append(safe_slice(line, 64, 67))
        anatem.dger["tensao_bloqueio_potencia_ativa"].append(safe_slice(line, 68, 73))
        anatem.dger["tensao_desbloqueio_potencia_ativa"].append(
            safe_slice(line, 74, 79)
        )
        anatem.dger["tensao_bloqueio_potencia_reativa"].append(safe_slice(line, 80, 85))
        anatem.dger["tensao_desbloqueio_potencia_reativa"].append(
            safe_slice(line, 86, 91)
        )

        anatem.linecount += 1


def dmdgmd01(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de máquina síncrona - modelo clássico

    Args
        anatem:
    """
    ## Inicialização
    # loop protegido
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # pular comentário/linha vazia
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""

        if prev_line[:] == anatem.dmdg.get("md01_ruler", ""):
            nbus = safe_slice(line, 0, 4)
            anatem.dmdg[nbus] = {
                "modelo": "MD01",
                "l_d": safe_slice(line, 7, 12),
                "resistencia_armadura": safe_slice(line, 12, 17),
                "inercia": safe_slice(line, 17, 22),
                "amortecimento": safe_slice(line, 22, 27),
                "potencia_nominal": safe_slice(line, 27, 32),
                "frequencia": safe_slice(line, 32, 34),
                "correcao_frequencia": safe_slice(line, 35, 36),
            }
            # consome esta linha e segue
            anatem.linecount += 1
            continue

        # caso não seja o início do bloco, avança
        anatem.linecount += 1


def dmdgmd02(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de máquina síncrona - MD02

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""

        if prev_line[:] == anatem.dmdg.get("md02_ruler", ""):
            # garantir existência das linhas seguintes (linha atual +2)
            line2 = (
                anatem.lines[anatem.linecount + 2].rstrip("\n")
                if (anatem.linecount + 2) < len(anatem.lines)
                else ""
            )

            nbus = safe_slice(line, 0, 4)
            anatem.dmdg[nbus] = {
                "modelo": "MD02",
                "curva_saturacao": safe_slice(line, 7, 11),
                "l_d": safe_slice(line, 12, 17),
                "l_q": safe_slice(line, 17, 22),
                "l_d_prime": safe_slice(line, 22, 27),
                "l_d_double_prime": safe_slice(line, 32, 37),
                "l_l": safe_slice(line, 37, 42),
                "tau_d0_prime": safe_slice(line, 42, 47),
                "tau_d0_double_prime": safe_slice(line, 52, 57),
                "tau_q0_double_prime": safe_slice(line, 57, 62),
                # parâmetros vindos de line+2 (segurança: line2 pode ser "")
                "resistencia_armadura": safe_slice(line2, 7, 12),
                "inercia": safe_slice(line2, 12, 17),
                "amortecimento": safe_slice(line2, 17, 22),
                "potencia_nominal": safe_slice(line2, 22, 27),
                "frequencia": safe_slice(line2, 27, 29),
                "correcao_frequencia": safe_slice(line2, 30, 31),
            }
            # consome 3 linhas (a atual + as 2 seguintes)
            anatem.linecount += 3
            continue

        anatem.linecount += 1


def dmdgmd03(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de máquina síncrona - MD03

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""

        if prev_line[:] == anatem.dmdg.get("md03_ruler", ""):
            line2 = (
                anatem.lines[anatem.linecount + 2].rstrip("\n")
                if (anatem.linecount + 2) < len(anatem.lines)
                else ""
            )

            nbus = safe_slice(line, 0, 4)
            anatem.dmdg[nbus] = {
                "modelo": "MD03",
                "curva_saturacao": safe_slice(line, 7, 11),
                "l_d": safe_slice(line, 12, 17),
                "l_q": safe_slice(line, 17, 22),
                "l_d_prime": safe_slice(line, 22, 27),
                "l_q_prime": safe_slice(line, 27, 32),
                "l_d_double_prime": safe_slice(line, 32, 37),
                "l_l": safe_slice(line, 37, 42),
                "tau_d0_prime": safe_slice(line, 42, 47),
                "tau_q0_prime": safe_slice(line, 47, 52),
                "tau_d0_double_prime": safe_slice(line, 52, 57),
                "tau_q0_double_prime": safe_slice(line, 57, 62),
                "resistencia_armadura": safe_slice(line2, 7, 12),
                "inercia": safe_slice(line2, 12, 17),
                "amortecimento": safe_slice(line2, 17, 22),
                "potencia_nominal": safe_slice(line2, 22, 27),
                "frequencia": safe_slice(line2, 27, 29),
                "correcao_frequencia": safe_slice(line2, 30, 31),
            }
            anatem.linecount += 3
            continue

        anatem.linecount += 1


def dopc(
    anatem,
):
    """inicialização para leitura de dados de código de opções de controle e execução padrão

    Args
        anatem:
    """
    ## Inicialização
    anatem.dopc["opcao"] = list()
    anatem.dopc["padrao"] = list()

    # posições (start,end,pad_index) conforme seu layout original
    pairs = [
        (0, 4, 5),
        (7, 11, 12),
        (14, 18, 19),
        (21, 25, 26),
        (28, 32, 33),
        (35, 39, 40),
        (42, 46, 47),
        (49, 53, 54),
        (56, 60, 61),
        (63, 67, 68),
    ]

    # loop protegido contra estouro de índice
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")

        # pular linha vazia ou comentário
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        # para cada posição, extrai opção e padrão; só adiciona se opção não for vazia
        for start, end, pad_idx in pairs:
            opt = safe_slice(line, start, end)
            if opt.strip() == "":
                # não há opção nesta faixa: ignora
                continue
            pad = safe_slice(
                line, pad_idx, pad_idx + 1
            )  # caractere único (pode retornar "")
            anatem.dopc["opcao"].append(opt)
            anatem.dopc["padrao"].append(pad)

        anatem.linecount += 1

    # DataFrame dos Dados de Constantes
    anatem.dopcDF = DF(data=anatem.dopc)
    anatem.dopc = deepcopy(anatem.dopcDF)
    anatem.dopcDF = anatem.dopcDF.replace(r"^\s*$", "0", regex=True)
    anatem.dopcDF = anatem.dopcDF.astype(
        {
            "opcao": "object",
            "padrao": "object",
        }
    )
    if anatem.dopcDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DOPC`!\033[0m"
        )
    else:
        anatem.stbblock["DOPC"] = True

        anatem.dopcDF["opcao"] = anatem.dopcDF["opcao"].replace("0", nan)
        anatem.dopcDF = anatem.dopcDF.dropna(axis=0, subset=["opcao"])
        anatem.dopcDF = anatem.dopcDF.drop_duplicates(
            subset=["opcao"], keep="last"
        ).reset_index(drop=True)


def drgvmd01(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md01

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md01_ruler", ""):
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD01",
                "estatismo": safe_slice(line, 7, 12),
                "estatismo_transitorio": safe_slice(line, 12, 17),
                "ganho_turbina": safe_slice(line, 17, 22),
                "vazao_noload": safe_slice(line, 22, 27),
                "cte_tempo_agua": safe_slice(line, 27, 32),
                "cte_tempo_regulador": safe_slice(line, 32, 37),
                "cte_tempo_filtragem": safe_slice(line, 37, 42),
                "cte_tempo_servomotor": safe_slice(line, 42, 47),
                "limite_minimo": safe_slice(line, 47, 52),
                "limite_maximo": safe_slice(line, 52, 57),
                "amortecimento_turbina": safe_slice(line, 57, 62),
                "amortecimento_carga": safe_slice(line, 62, 67),
                "mva_base": safe_slice(line, 67, 72),
                "mw_base": safe_slice(line, 72, 77),
            }
            anatem.linecount += 1
            continue

        anatem.linecount += 1


def drgvmd02(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md02

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] in anatem.drgv.get("md02_ruler", ""):
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD02",
                "estatismo": safe_slice(line, 7, 12),
                "cte_tempo_regulador": safe_slice(line, 12, 17),
                "cte_tempo_1": safe_slice(line, 17, 22),
                "cte_tempo_reaquecimento": safe_slice(line, 22, 27),
                "limite_minimo": safe_slice(line, 27, 32),
                "limite_maximo": safe_slice(line, 32, 37),
                "amortecimento_turbina": safe_slice(line, 37, 42),
                "tipo": safe_slice(line, 42, 43),
            }
            anatem.linecount += 1
            continue

        anatem.linecount += 1


def drgvmd03(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md03

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md03_ruler", ""):
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD03",
                "bp": safe_slice(line, 7, 12),
                "bt": safe_slice(line, 12, 17),
                "cte_tempo_v": safe_slice(line, 17, 22),
                "cte_tempo_1": safe_slice(line, 22, 27),
                "cte_tempo_2": safe_slice(line, 27, 32),
                "cte_tempo_agua": safe_slice(line, 32, 37),
                "limite_minimo": safe_slice(line, 37, 42),
                "limite_maximo": safe_slice(line, 42, 47),
                "cte_tempo_maxima": safe_slice(line, 47, 52),
                "amortecimento_turbina": safe_slice(line, 52, 57),
            }
            anatem.linecount += 1
            continue

        anatem.linecount += 1


def drgvmd04(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md04

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md04_ruler", ""):
            line2 = (
                anatem.lines[anatem.linecount + 2].rstrip("\n")
                if (anatem.linecount + 2) < len(anatem.lines)
                else ""
            )

            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD04",
                "bp": safe_slice(line, 7, 12),
                "bt": safe_slice(line, 12, 17),
                "ganho_turbina": safe_slice(line, 17, 22),
                "vazao_noload": safe_slice(line, 22, 27),
                "cte_tempo_p": safe_slice(line, 27, 32),
                "cte_tempo_y": safe_slice(line, 32, 37),
                "cte_tempo_d": safe_slice(line, 37, 42),
                "cte_tempo_s": safe_slice(line, 42, 47),
                "cte_tempo_servomotor": safe_slice(line, 47, 52),
                "cte_tempo_agua": safe_slice(line, 52, 57),
                "limite_minimo": safe_slice(line, 57, 62),
                "limite_maximo": safe_slice(line, 62, 67),
                "gmin": safe_slice(line2, 7, 12),
                "gmax": safe_slice(line2, 12, 17),
                "amortecimento_turbina": safe_slice(line2, 17, 22),
            }
            anatem.linecount += 3
            continue

        anatem.linecount += 1


def drgvmd05(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md05

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md05_ruler", ""):
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD05",
                "c1": safe_slice(line, 7, 12),
                "c2": safe_slice(line, 12, 17),
                "c3": safe_slice(line, 17, 22),
                "c8": safe_slice(line, 22, 27),
                "t3": safe_slice(line, 27, 32),
                "t4": safe_slice(line, 32, 37),
                "t5": safe_slice(line, 37, 42),
                "tc": safe_slice(line, 42, 47),
                "tmax": safe_slice(line, 47, 52),
                "amortecimento_turbina": safe_slice(line, 52, 57),
            }
            anatem.linecount += 1
            continue

        anatem.linecount += 1


def drgvmd06(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md06

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md06_ruler", ""):
            line2 = (
                anatem.lines[anatem.linecount + 2].rstrip("\n")
                if (anatem.linecount + 2) < len(anatem.lines)
                else ""
            )
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD06",
                "ganho_r": safe_slice(line, 7, 12),
                "bp": safe_slice(line, 12, 17),
                "bt": safe_slice(line, 17, 22),
                "blp": safe_slice(line, 22, 27),
                "ganho_turbina": safe_slice(line, 27, 32),
                "vazao_noload": safe_slice(line, 32, 37),
                "cte_tempo_n": safe_slice(line, 37, 42),
                "cte_tempo_v": safe_slice(line, 42, 47),
                "cte_tempo_r": safe_slice(line, 47, 52),
                "cte_tempo_servomotor": safe_slice(line, 52, 57),
                "cte_tempo_lg": safe_slice(line, 57, 62),
                "cte_tempo_d": safe_slice(line, 62, 67),
                "cte_tempo_t": safe_slice(line, 67, 72),
                "cte_tempo_lp": safe_slice(line2, 7, 12),
                "cte_tempo_agua": safe_slice(line2, 12, 17),
                "limite_minimo_1": safe_slice(line2, 17, 22),
                "limite_maximo_1": safe_slice(line2, 22, 27),
                "limite_minimo_2": safe_slice(line2, 27, 32),
                "limite_maximo_2": safe_slice(line2, 32, 37),
                "limite_minimo_3": safe_slice(line2, 37, 42),
                "limite_maximo_3": safe_slice(line2, 42, 47),
                "limite_minimo_4": safe_slice(line2, 47, 52),
                "limite_maximo_4": safe_slice(line2, 52, 57),
                "amortecimento_turbina": safe_slice(line2, 57, 62),
            }
            anatem.linecount += 3
            continue

        anatem.linecount += 1


def drgvmd07(
    anatem,
):
    """inicialização para leitura de dados de modelos predefinidos de reguladores de velocidade - modelo md07

    Args
        anatem:
    """
    ## Inicialização
    while (
        0 <= anatem.linecount < len(anatem.lines)
        and anatem.lines[anatem.linecount].strip() not in anatem.end_block
    ):
        line = anatem.lines[anatem.linecount].rstrip("\n")
        if line.strip() == "" or (len(line) > 0 and line[0] == anatem.comment):
            anatem.linecount += 1
            continue

        prev_line = anatem.lines[anatem.linecount - 1] if anatem.linecount > 0 else ""
        if prev_line[:] == anatem.drgv.get("md07_ruler", ""):
            line2 = (
                anatem.lines[anatem.linecount + 2].rstrip("\n")
                if (anatem.linecount + 2) < len(anatem.lines)
                else ""
            )
            nrgv = safe_slice(line, 0, 4)
            anatem.drgv[nrgv] = {
                "modelo": "MD07",
                "ganho_0": safe_slice(line, 7, 12),
                "ganho_5": safe_slice(line, 12, 17),
                "ganho_p1": safe_slice(line, 17, 22),
                "ganho_p2": safe_slice(line, 22, 27),
                "ganho_lp": safe_slice(line, 27, 32),
                "ganho_p": safe_slice(line, 32, 37),
                "bp": safe_slice(line, 37, 42),
                "cte_tempo_v": safe_slice(line, 42, 47),
                "cte_tempo_n": safe_slice(line, 47, 52),
                "cte_tempo_a": safe_slice(line, 52, 57),
                "cte_tempo_f": safe_slice(line, 57, 62),
                "cte_tempo_r": safe_slice(line, 62, 67),
                "cte_tempo_y": safe_slice(line, 67, 72),
                "cte_tempo_agua": safe_slice(line2, 7, 12),
                "limite_minimo": safe_slice(line2, 12, 17),
                "limite_maximo": safe_slice(line2, 17, 22),
                "cte_tempo_maxima": safe_slice(line2, 22, 27),
                "amortecimento_turbina": safe_slice(line2, 27, 32),
            }
            anatem.linecount += 3
            continue

        anatem.linecount += 1


def dsim(
    anatem,
):
    """inicialização para leitura de dados de controle de simulação

    Args
        anatem:
    """
    ## Inicialização
    anatem.dsim["tmax"] = list()
    anatem.dsim["step"] = list()
    anatem.dsim["plot"] = list()
    anatem.dsim["rela"] = list()
    anatem.dsim["freq"] = list()

    while not anatem.dsim["tmax"]:
        if anatem.lines[anatem.linecount][0] == anatem.comment:
            pass
        else:
            anatem.dsim["tmax"].append(anatem.lines[anatem.linecount][:8])
            anatem.dsim["step"].append(anatem.lines[anatem.linecount][9:14])
            anatem.dsim["plot"].append(anatem.lines[anatem.linecount][15:20])
            anatem.dsim["rela"].append(anatem.lines[anatem.linecount][21:26])
            anatem.dsim["freq"].append(anatem.lines[anatem.linecount][27:32])
        anatem.linecount += 1

    # DataFrame dos Dados de Intercâmbio de Potência Ativa entre Áreas
    anatem.dsimDF = DF(data=anatem.dsim)
    anatem.dsim = deepcopy(anatem.dsimDF)
    anatem.dsimDF = anatem.dsimDF.replace(r"^\s*$", "0", regex=True)
    anatem.dsimDF = anatem.dsimDF.astype(
        {
            "tmax": "float",
            "step": "float",
            "plot": "int",
            "rela": "int",
            "freq": "int",
        }
    )
    if anatem.dsimDF.empty:
        ## ERROR - VERMELHO
        raise ValueError(
            "\033[91mERROR: Falha na leitura de código de execução `DSIM`!\033[0m"
        )
    else:
        anatem.stbblock["DSIM"] = True


def safe_slice(
    line: str, start: int, end: int, default: str = DEFAULT, require_full: bool = False
) -> str:
    """
    Retorna line[start:end] de forma segura:
    - se start >= len(line) -> default
    - slice é seguro mesmo se end > len(line)
    - se require_full=True e a fatia for menor que (end-start) -> default
    """
    if line is None:
        return default
    L = len(line)
    if start >= L:
        return default
    val = line[start:end]
    if require_full and len(val) < (end - start):
        return default
    return val


# def dmaq(
#     anatem,
#     arquivo,
#     arquivoname,
# ):
#     """inicialização para leitura de dados

#     Args
#         anatem:
#     """
#     ## Inicialização
#     anatem.linecount = 0
#     f = open(f"{arquivo}", "r", encoding="latin-1")
#     anatem.lines = f.readlines()
#     f.close()

#     anatem.dmaq = dict()
#     anatem.dmaq["numero"] = list()
#     anatem.dmaq["grupo"] = list()
#     anatem.dmaq["percentual-ativa"] = list()
#     anatem.dmaq["percentual-reativa"] = list()
#     anatem.dmaq["unidades"] = list()
#     anatem.dmaq["gerador"] = list()
#     anatem.dmaq["tensao"] = list()
#     anatem.dmaq["user-tensao"] = list()
#     anatem.dmaq["velocidade"] = list()
#     anatem.dmaq["user-velocidade"] = list()
#     anatem.dmaq["estabilizador"] = list()
#     anatem.dmaq["user-estabilizador"] = list()
#     anatem.dmaq["reatancia-compensacao"] = list()
#     anatem.dmaq["barra-controlada"] = list()

#     anatem.linecount += 1
#     anatem.dmaq["ruler"] = anatem.lines[anatem.linecount][:]

#     # Loop de leitura de linhas do `.stb`
#     while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
#         # Dados de Arquivos de Máquina
#         while anatem.lines[anatem.linecount].strip() not in anatem.end_block:
#             if anatem.lines[anatem.linecount][0] == anatem.comment:
#                 pass
#             else:
#                 anatem.dmaq["numero"].append(anatem.lines[anatem.linecount][:5])
#                 anatem.dmaq["grupo"].append(anatem.lines[anatem.linecount][8:10])
#                 anatem.dmaq["percentual-ativa"].append(
#                     anatem.lines[anatem.linecount][11:14]
#                 )
#                 anatem.dmaq["percentual-reativa"].append(
#                     anatem.lines[anatem.linecount][15:18]
#                 )
#                 anatem.dmaq["unidades"].append(anatem.lines[anatem.linecount][19:22])
#                 anatem.dmaq["gerador"].append(anatem.lines[anatem.linecount][23:29])
#                 anatem.dmaq["tensao"].append(anatem.lines[anatem.linecount][30:36])
#                 anatem.dmaq["user-tensao"].append(anatem.lines[anatem.linecount][36])
#                 anatem.dmaq["velocidade"].append(anatem.lines[anatem.linecount][37:43])
#                 anatem.dmaq["user-velocidade"].append(
#                     anatem.lines[anatem.linecount][43]
#                 )
#                 anatem.dmaq["estabilizador"].append(
#                     anatem.lines[anatem.linecount][44:50]
#                 )
#                 anatem.dmaq["user-estabilizador"].append(
#                     anatem.lines[anatem.linecount][50]
#                 )
#                 anatem.dmaq["reatancia-compensacao"].append(
#                     anatem.lines[anatem.linecount][51:56]
#                 )
#                 anatem.dmaq["barra-controlada"].append(
#                     anatem.lines[anatem.linecount][56:61]
#                 )
#             anatem.linecount += 1
#         anatem.linecount += 1

#     ## SUCESSO NA LEITURA
#     print(f"\033[32mSucesso na leitura de arquivo `{arquivoname}`!\033[0m")

#     # DataFrame dos Dados de Agregadores Genericos
#     anatem.dmaqDF = DF(data=anatem.dmaq)
#     anatem.dmaq = deepcopy(anatem.dmaqDF)
#     anatem.dmaqDF = anatem.dmaqDF.replace(r"^\s*$", "0", regex=True)
#     anatem.dmaqDF = anatem.dmaqDF.astype(
#         {
#             "numero": "int",
#             "grupo": "int",
#             "percentual-ativa": "float",
#             "percentual-reativa": "float",
#             "unidades": "int",
#             "gerador": "int",
#             "tensao": "int",
#             "user-tensao": "object",
#             "velocidade": "int",
#             "user-velocidade": "object",
#             "estabilizador": "int",
#             "user-estabilizador": "object",
#             "reatancia-compensacao": "float",
#             "barra-controlada": "int",
#         }
#     )
#     if anatem.dmaqDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de código de execução `DMAQ`!\033[0m"
#         )
#     else:
#         anatem.stbblock["DMAQ"] = True

#         anatem.dmaqDF = anatem.dmaqDF.sort_values(by=["numero"], ascending=True)


# def blt(
#     anatem,
#     arquivo,
#     arquivoname,
# ):
#     """inicialização para leitura de dados

#     Args
#         anatem:
#     """
#     ## Inicialização
#     anatem.linecount = 0
#     f = open(f"{arquivo}", "r", encoding="latin-1")
#     anatem.lines = f.readlines()
#     f.close()

#     # # Loop de leitura de linhas do `.stb`
#     # while anatem.lines[anatem.linecount].strip() != anatem.end_archive:
#     # Dados de Arquivos de Entrada e Saida
#     while anatem.lines[anatem.linecount].strip() not in anatem.end_block:
#         if anatem.lines[anatem.linecount].strip() == "DMDG MD01":
#             anatem.linecount += 1
#             anatem.dmdg = dict()
#             anatem.dmdg["ruler"] = anatem.lines[anatem.linecount][:]
#             md01(
#                 anatem,
#             )
#             anatem.linecount -= 1
#         anatem.linecount += 1

#     ## SUCESSO NA LEITURA
#     print(f"\033[32mSucesso na leitura de arquivo `{arquivoname}`!\033[0m")


# def md01(
#     anatem,
# ):
#     """ "

#     Args
#         anatem:
#     """
#     ## Inicialização
#     anatem.dmdg["tipo"] = list()
#     anatem.dmdg["numero"] = list()
#     anatem.dmdg["l-transitoria"] = list()
#     anatem.dmdg["r-armadura"] = list()
#     anatem.dmdg["inercia"] = list()
#     anatem.dmdg["amortecimento"] = list()
#     anatem.dmdg["aparente"] = list()
#     anatem.dmdg["freq-sincrona"] = list()
#     anatem.dmdg["freq-correcao"] = list()

#     while anatem.lines[anatem.linecount].strip() not in anatem.end_block:
#         if anatem.lines[anatem.linecount][0] == anatem.comment:
#             pass
#         else:
#             anatem.dmdg["tipo"].append("MD01")
#             anatem.dmdg["numero"].append(anatem.lines[anatem.linecount][:4])
#             anatem.dmdg["l-transitoria"].append(anatem.lines[anatem.linecount][7:12])
#             anatem.dmdg["r-armadura"].append(anatem.lines[anatem.linecount][12:17])
#             anatem.dmdg["inercia"].append(anatem.lines[anatem.linecount][17:22])
#             anatem.dmdg["amortecimento"].append(anatem.lines[anatem.linecount][22:27])
#             anatem.dmdg["aparente"].append(anatem.lines[anatem.linecount][27:32])
#             anatem.dmdg["freq-sincrona"].append(anatem.lines[anatem.linecount][32:34])
#             anatem.dmdg["freq-correcao"].append(anatem.lines[anatem.linecount][35])
#         anatem.linecount += 1

#     # DataFrame dos Dados de Alteração do Nível de Carregamento
#     anatem.dmdgDF = DF(data=anatem.dmdg)
#     anatem.dmdg = deepcopy(anatem.dmdgDF)
#     anatem.dmdgDF = anatem.dmdgDF.replace(r"^\s*$", "0", regex=True)
#     anatem.dmdgDF = anatem.dmdgDF.astype(
#         {
#             "tipo": "object",
#             "numero": "int",
#             "l-transitoria": "float",
#             "r-armadura": "float",
#             "inercia": "float",
#             "amortecimento": "float",
#             "aparente": "float",
#             "freq-sincrona": "float",
#             "freq-correcao": "object",
#         }
#     )
#     if anatem.dmdgDF.empty:
#         ## ERROR - VERMELHO
#         raise ValueError(
#             "\033[91mERROR: Falha na leitura de código de execução `DMDG MD01`!\033[0m"
#         )
#     else:
#         anatem.stbblock["DMDG MD01"] = True
