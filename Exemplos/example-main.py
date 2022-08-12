from leitura import LeituraPWF
from flow import PowerFlow
from folderprompt import Folder
from report import Relatorio
from os import getcwd

dir = getcwd() + '/PowerFlow/Sistemas/'
Folder(dir=dir)

sistema = '2b-teste.pwf'
dbarra, dlinha = LeituraPWF()._readfile(arqv=dir + sistema)

PF = PowerFlow(dbarra=dbarra, dlinha=dlinha, dir=dir, sistema=sistema).NewtonRaphson()

Relatorio(pf=PF, rel='RBARRA RLINHA', dir=dir, sistema=sistema)