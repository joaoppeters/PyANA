# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

from os.path import dirname, realpath
from datetime import datetime as dt
# from numpy import (
#     round,
# )


def savepwf(
    powerflow,
):
    """inicializacao

    Parametros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicializacao
    # Arquivo
    filedir = realpath(
        dirname(dirname(__file__)) + "/sistemas/" + powerflow.name + "-mod.pwf"
    )

    # Manipulacao
    file = open(filedir, "w")

    # Cabecalho
    writeheader(
        file,
    )

    if powerflow.codes["TITU"]:
        writetitu(
            powerflow,
            file,
        )

    if powerflow.codes["DOPC"]:
        writedopc(
            powerflow,
            file,
        )

    if powerflow.codes["DCTE"]:
        writedcte(
            powerflow,
            file,
        )

    if powerflow.codes["DAGR"]: # FAZER
        writedagr(
            powerflow,
            file,
        )

    if powerflow.codes["DBAR"]:
        writedbar(
            powerflow,
            file,
        )

    if powerflow.codes["DLIN"]:
        writedlin(
            powerflow,
            file,
        )

    if powerflow.codes["DGER"]:
        writedger(
            powerflow,
            file,
        )

    if powerflow.codes["DARE"]:
        writedare(
            powerflow,
            file,
        )

    if powerflow.codes["DGBT"]:
        writedgbt(
            powerflow,
            file,
        )

    if powerflow.codes["DGLT"]:
        writedglt(
            powerflow,
            file,
        )

    if powerflow.codes["DANC"]:
        writedanc(
            powerflow,
            file,
        )

    if powerflow.codes["DINC"]:
        writedinc(
            powerflow,
            file,
        )

    file.write("\n")
    file.write("FIM")
    file.close()


def writeheader(
    file,
):
    """

    Parâmetros
        file
        powerflow
    """

    ## Inicialização
    file.write("(")
    file.write("\n")
    file.write("( Modificacao Automatica de Dados .PWF")
    file.write("\n")
    file.write("( Joao Pedro Peters Barbosa - jpeters@usp.br")
    file.write("\n")
    file.write(
        "( Data e Hora da Gravacao: {} {}, {}  -  {}:{}:{}".format(
            dt.now().strftime("%B"),
            dt.now().strftime("%d"),
            dt.now().strftime("%Y"),
            dt.now().strftime("%H"),
            dt.now().strftime("%M"),
            dt.now().strftime("%S"),
        )
    )
    file.write("\n")
    file.write("( ")
    file.write("\n")


def writetitu(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("TITU")
    file.write("\n")
    file.write("{}".format(powerflow.titu))


def writedopc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DOPC IMPR")
    file.write("\n")
    file.write("{}".format(powerflow.dopc["ruler"]))
    for idx, value in powerflow.dopcDF.iterrows():
        file.write(f"{value['opcao']:4} {value['padrao']:1} ")

        if (idx + 1) % 10 == 0:
            file.write("\n")
            
    file.write("\n")
    file.write("99999")
    file.write("\n")


def writedcte(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DCTE")
    file.write("\n")
    file.write("{}".format(powerflow.dcte["ruler"]))
    for i, (key, value) in enumerate(powerflow.options.items()):
        file.write(f"{key:<4}  {value:6>.0e} ")

        if (i + 1) % 6 == 0:
            file.write("\n")

        if key == "VPMF":
            break
    file.write("\n")
    file.write("99999")
    file.write("\n")


def writedagr(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def writedbar(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DBAR")
    file.write("\n")
    file.write("{}".format(powerflow.dbar["ruler"]))
    for idx, value in powerflow.dbarraDF.iterrows(): 
        n = value["numero"]
        if value["operacao"] == '0':
            op = ' '
        else:
            op = str(value["operacao"])
            
        if value["estado"] == '0':
            e = ' '
        else:
            e = str(value["estado"])
        
        if value["tipo"] != 0:
            t = str(value["tipo"])
        else:
            t = ' '
            
        if value["grupo_base_tensao"] == ' 0':
            gbt = ' '
        else:
            gbt = str(value["grupo_base_tensao"])
            
        if value["grupo_limite_tensao"] == ' 0':
            glt = ' '
        else:
            glt = str(value["grupo_limite_tensao"])
            
        v = str(int(value["tensao"]))
        
        if value["tipo"] == 2:
            a = str(round(value["angulo"], 1))
        else:
            a = 4*' '
        
        if value["potencia_ativa"] == 0. and value["tipo"] == 0:
            pg = 5*' '
        else:
            pg = str(round(value["potencia_ativa"], 1))
    
        qg = 5*' '
                
        if value["potencia_reativa_minima"] == 0. and value["tipo"] == 0:
            qgn = 5*' '
        else:
            qgn = str(round(value["potencia_reativa_minima"]))
        
        if value["potencia_reativa_maxima"] == 0. and value["tipo"] == 0:
            qgx = 5*' '
        else:
            qgx = str(round(value["potencia_reativa_maxima"]))
            
        if value["barra_controlada"] == 0:
            bc = 5*' '
        else:
            bc = str(value["barra_controlada"])
            
        if value["demanda_ativa"] == 0.:
            pl = 5*' '
        else:
            pl = str(round(value["demanda_ativa"], 1))
            
        if value["demanda_reativa"] == 0.:
            ql = 5*' '
        else:
            ql = str(round(value["demanda_reativa"], 1))
        
        if value["shunt_barra"] == 0.:
            sb = 5*' '
        else:
            sb = str(round(value["shunt_barra"], 1))
        
        ar = str(value["area"])
        
        tb = str(int(value["tensao_base"]))
        
        if value["modo"] == 0.:
            m = ' '
        else:
            m = str(value["modo"])
            
        if value["agreg1"] == "0":
            a1 = 3*' '
        else:
            a1 = value["agreg1"]
            
        if value["agreg2"] == "0":
            a2 = 3*' '
        else:
            a2 = value["agreg2"]
            
        if value["agreg3"] == "0":
            a3 = 3*' '
        else:
            a3 = value["agreg3"]
            
        if value["agreg4"] == "0":
            a4 = 3*' '
        else:
            a4 = value["agreg4"]
            
        if value["agreg5"] == "0":
            a5 = 3*' '
        else:
            a5 = value["agreg5"]
            
        if value["agreg6"] == "0":
            a6 = 3*' '
        else:
            a6 = value["agreg6"]
            
        if value["agreg7"] == "0":
            a7 = 3*' '
        else:
            a7 = value["agreg7"]
            
        if value["agreg8"] == "0":
            a8 = 3*' '
        else:
            a8 = value["agreg8"]
            
        if value["agreg9"] == "0":
            a9 = 3*' '
        else:
            a9 = value["agreg9"]
            
        if value["agreg10"] == "0":
            a10 = 3*' '
        else:
            a10 = value["agreg10"]
        file.write(f"{n:>5}{op:1}{e:1}{t:1}{gbt:>2}{value['nome']:^12}{glt:>2}{v:>4}{a:<4}{pg:<5}{qg:5}{qgn:<5}{qgx:<5}{bc:<5}{pl:<5}{ql:<5}{sb:<5}{ar:>3}{tb:>4}{m:1}{a1:<3}{a2:<3}{a3:<3}{a4:<3}{a5:<3}{a6:<3}{a7:<3}{a8:<3}{a9:<3}{a10:<3}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedlin(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def writedger(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass


def writedare(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DARE")
    file.write("\n")
    file.write("{}".format(powerflow.dare["ruler"]))
    for idx, value in powerflow.dareaDF.iterrows():
        n = str(value["numero"])

        if value["intercambio_liquido"] == 0:
            il = 6*' '
        else:
            il = str(value["intercambio_liquido"])

        if value["intercambio_maximo"] == 0.:
            ix = 6*' '
        else:
            ix = str(value["intercambio_maximo"])

        if value["intercambio_minimo"] == 0.:
            im = 6*' '
        else:
            im = str(value["intercambio_minimo"])
        
        file.write(f"{n:3}    {il:>6}     {value['nome']:^35} {im:>6} {ix:>6}")
        file.write("\n")
    file.write("99999")
    file.write("\n")



def writedgbt(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DGBT")
    file.write("\n")
    file.write("{}".format(powerflow.dgbt["ruler"]))
    for idx, value in powerflow.dgbtDF.iterrows():
        file.write(f"{value['grupo']:2} {value['tensao']:>5.1f}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedglt(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DGLT")
    file.write("\n")
    file.write("{}".format(powerflow.dglt["ruler"]))
    for idx, value in powerflow.dgltDF.iterrows():
        file.write(f"{value['grupo']:2} {str(value['limite_minimo']):>5} {str(value['limite_maximo']):>5} {str(value['limite_minimo_E']):>5} {str(value['limite_maximo_E']):>5}")
        file.write("\n")
    file.write("99999")
    file.write("\n")


def writedanc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    file.write("DANC")
    file.write("\n")
    file.write("{}".format(powerflow.danc["ruler"]))
    for idx, value in powerflow.dancDF.iterrows():
        file.write(f"{value['numero']:>3d} {value['fator_carga_ativa']:>6.1f} {value['fator_carga_reativa']:>6.1f} {value['fator_shunt_barra']:>6.1f}")
        file.write("\n")
    file.write("99999")
    file.write("\n")        
    

def writedinc(
    powerflow,
    file,
):
    """

    Parâmetros
        powerflow: self do arquivo powerflow.py
    """

    ## Inicialização
    pass
