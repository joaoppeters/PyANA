# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import os
import time


def anarede(
    batchtime,
    filedir,
):
    """execução do Anarede

    Parâmetros
        batchtime: tempo de execução do Anarede
        filepath: caminho do arquivo
        filenamecase: nome do arquivo
    """

    ## Inicialização
    # Chamada do Anarede
    os.system(
        'start C:\\CEPEL\\Anarede\\V110702\\ANAREDE.exe "{}"'.format(
            filedir
        )
    )
    time.sleep(batchtime)
    os.system("taskkill /f /im ANAREDE.exe")
