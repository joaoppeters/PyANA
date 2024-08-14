# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

import os


def anarede(
    file,
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
        'start C:/CEPEL/Anarede/V110702/ANAREDE.exe "{}"'.format(
            file
        )
    )
