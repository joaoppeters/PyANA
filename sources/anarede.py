# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #


def exlf(
    file,
    time,
):
    """execução do Anarede

    Args
        file:
        time:
    """

    from os import system
    from time import sleep

    ## Inicialização
    # Chamada do Anarede
    system('start C:/CEPEL/Anarede/V110702/ANAREDE.exe "{}"'.format(file))

    sleep(time)
    system("taskkill /f /im ANAREDE.exe")


def exic(
    file,
):
    """

    Args
        file:
    """

    from os import system
    from time import sleep

    ## Inicialização
    # Chamada do Anarede
    system('start C:/CEPEL/Anarede/V110702/ANAREDE.exe "{}"'.format(file))

    sleep(10)
    system("taskkill /f /im ANAREDE.exe")


def exct(
    file,
):
    """

    Args
        file:
    """

    from os import system
    from time import sleep

    ## Inicialização
    # Chamada do Anarede
    system('start C:/CEPEL/Anarede/V110702/ANAREDE.exe "{}"'.format(file))

    sleep(10)
    system("taskkill /f /im ANAREDE.exe")


def exicpvct(
    file,
):
    """

    Args
        file:
    """

    from os import system
    from time import sleep

    ## Inicialização
    # Chamada do Anarede
    system('start C:/CEPEL/Anarede/V110702/ANAREDE.exe "{}"'.format(file))

    sleep(10)
    system("taskkill /f /im ANAREDE.exe")
