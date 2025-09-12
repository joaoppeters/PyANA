# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os import listdir
from os.path import isfile, join
from numpy import array, reshape

directory = "C:\\Users\\JoaoPedroPetersBarbo\\Dropbox\\Profissional\\doutorado\\estudos\\totalE\\restricoes-ellen\\"
directory = "C:\\Users\\JoaoPedroPetersBarbo\\Desktop\\restricoes-ellen\\"
folder = "BD2411R2MOD\\PLT"

arquivos = [
    f
    for f in listdir(f"{directory}/{folder}")
    if (f.endswith(".PLT") or f.endswith(".plt"))
    and isfile(join(f"{directory}/{folder}", f))
]

arquivos = ["JUN25-JR-ACU3QXDMLG2.PLT"]

for arquivo in arquivos:
    try:
        print(f"Processando arquivo: {arquivo}")
        with open(f"{directory}/{folder}/{arquivo}", "r", encoding="latin-1") as file:
            lines = file.readlines()

        total_vars = int(lines[0].strip())

        start_idx = None
        end_idx = None

        for idx, line in enumerate(lines[1 : total_vars + 1]):  # começando do índice 2
            palavra = line.split()[0]

            if palavra == "PTFNT":
                if start_idx is None:
                    start_idx = idx  # marca o início
                end_idx = idx  # atualiza o fim enquanto for PTFNT
            elif start_idx is not None:
                # já começou o intervalo e achou outra palavra, então para
                break

        # start_idx = 1
        # end_idx = total_vars
        valores = []
        for idx, line in enumerate(lines[total_vars + 1 :]):
            valores.extend(line.strip().split())

        vals = array(valores, dtype=float)
        vals = reshape(a=vals, newshape=(len(valores) // total_vars, total_vars)).T

        intervalo = vals[start_idx : end_idx + 1, :]
        anatem_curtailment = []

        for i in range(intervalo.shape[0]):
            if (intervalo[i, 0] != 0.0) and (round(intervalo[i, -1], 1) == 0.0):
                anatem_curtailment.append(start_idx + i)

        qtd_0 = len(anatem_curtailment)

        print(f"Número de elementos que terminam com '0.0': {qtd_0}")
        if qtd_0:
            print(f"Índices dos elementos: {anatem_curtailment}")
            if qtd_0 > 0:
                i = 0
                while i < qtd_0:
                    print(f"{lines[anatem_curtailment[i]+1]}")
                    i += 1
            print()
    except:
        continue
    print("\n")
