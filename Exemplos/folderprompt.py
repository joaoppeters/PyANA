from os import path, mkdir

class Folder:
    """Classe para criacao de folders
    """
    
    def __init__(self, dir: str=''):
        if dir:
            dir_resultado = path.expanduser(dir + 'Resultados/')
            dir_resultado_admitancia = path.expanduser(dir_resultado + 'MatrizAdmitancia/')
            dir_resultado_barra = path.expanduser(dir_resultado + 'RelatorioBarra/')
            dir_resultado_jacobiana = path.expanduser(dir_resultado + 'MatrizJacobiana/')
            dir_resultado_linha = path.expanduser(dir_resultado + 'RelatorioLinha/')

            if path.exists(dir_resultado) is False:
                mkdir(dir_resultado)
            
            if path.exists(dir_resultado_admitancia) is False:
                mkdir(dir_resultado_admitancia)
            
            if path.exists(dir_resultado_barra) is False:
                mkdir(dir_resultado_barra)
            
            if path.exists(dir_resultado_jacobiana) is False:
                mkdir(dir_resultado_jacobiana)
            
            if path.exists(dir_resultado_linha) is False:
                mkdir(dir_resultado_linha)