from datetime import datetime as dt
from os import path
from numpy import abs, degrees

class Relatorio:
    """Classe para geração de relatórios
    """

    def __init__(
        self, 
        pf: dict = None, 
        rel: str = '', 
        dir: str = '', 
        sistema: str = '',
        ):

        self.sol = pf
        self.dir = dir
        self.sistema = sistema.split(".")[0]
        
        if rel:
            rel = list(rel.split())
            self.rela = rel
            if len(rel) > 1:
                self.rela = [r.upper() for r in rel]

        if dir:
            for rela in self.rela:
                if rela == "RBARRA":
                    self.rbarra()

                if rela == "RLINHA":
                    self.rlinha()



    def rbarra(self):
        file = open(path.expanduser(self.dir + "/Resultados/RelatorioBarra/" + self.sistema + "-rbarra.txt"), "w")
        file.write(
            "{} {}, {}".format(
                dt.now().strftime("%B"), dt.now().strftime("%d"), dt.now().strftime("%Y")
            )
        )
        file.write("\n")
        file.write("-"*85)
        file.write("\n")
        file.write(" "*35 + "SISTEMA {}\n".format(self.sistema.upper()))
        file.write(" "*33 + "RELATÓRIO DE BARRAS\n")
        file.write("-"*85)
        file.write("\n")
        file.write(" "*37 + "{} iterações\n".format(self.sol['iteracoes']))
        file.write("-"*85)
        file.write("\n")
        file.write("|     BARRA    |      TENSAO     |        GERACAO      |       CARGA      |  SHUNT  |\n")
        file.write("-"*85)
        file.write("\n")
        file.write("|   NOME   | T |   MOD   |  ANG  |    MW   |    Mvar   |   MW   |   Mvar  |   Mvar  |\n")
        file.write("-"*85)
        for i in range(0, self.sol['nbus']):
            if i % 10 == 0 and i != 0:
                file.write("\n\n")
                file.write("-"*85)
                file.write("\n")
                file.write("|     BARRA    |      TENSAO     |        GERACAO      |       CARGA      |  SHUNT  |\n")
                file.write("-"*85)
                file.write("\n")
                file.write("|   NOME   | T |   MOD   |  ANG  |    MW   |    Mvar   |   MW   |   Mvar  |   Mvar  |\n")
                file.write("-"*85)

            file.write(f"\n| {self.sol['dbarra']['nome'][i]:<10}{self.sol['dbarra']['tipo'][i]:>2}{self.sol['voltage'][i]:>9.3f}{degrees(self.sol['theta'][i]):>8.1f}{self.sol['active'][i]:>11.2f}{self.sol['reactive'][i]:>11.2f}{self.sol['dbarra']['demanda_ativa'][i]:>10.2f}{self.sol['dbarra']['demanda_reativa'][i]:>9.2f}{(self.sol['voltage'][i]**2)*self.sol['dbarra']['capacitor_reator'][i]:>10.2f}  |")
            file.write("\n")
            file.write("-"*85)

        file.close()



    def rlinha(self):
        file = open(path.expanduser(self.dir + "/Resultados/RelatorioLinha/" + self.sistema + "-rlinha.txt"), "w")
        file.write(
            "{} {}, {}".format(
                dt.now().strftime("%B"), dt.now().strftime("%d"), dt.now().strftime("%Y")
            )
        )
        file.write("\n")
        file.write("-"*89)
        file.write("\n")
        file.write(" "*37 + "SISTEMA {}\n".format(self.sistema.upper()))
        file.write(" "*35 + "RELATÓRIO DE LINHAS\n")
        file.write("-"*89)
        file.write("\n")
        file.write(" "*39 + "{} iterações\n".format(self.sol['iteracoes']))
        file.write("-"*89)
        file.write("\n")
        file.write("|     BARRA      |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |\n")
        file.write("-"*89)
        file.write("\n")
        file.write("|  DE   |  PARA  |  Pkm[MW]  |  Qkm[Mvar]  |  Pmk[MW]  |  Qmk[Mvar]  |    MW   |  Mvar  |\n")
        file.write("-"*89)
        # file.write("\n")
        for i in range(0, self.sol['nlin']):
            if i % 10 == 0 and i != 0:
                file.write("\n\n")
                file.write("-"*89)
                file.write("\n")
                file.write("|     BARRA      |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |\n")
                file.write("-"*89)
                file.write("\n")
                file.write("|  DE   |  PARA  |  Pkm[MW]  |  Qkm[Mvar]  |  Pmk[MW]  |  Qmk[Mvar]  |    MW   |  Mvar  |\n")
                file.write("-"*89)

            file.write(f"\n|{self.sol['dbarra']['nome'][self.sol['dlinha']['from'][i] - 1]:>7}{self.sol['dbarra']['nome'][self.sol['dlinha']['to'][i] - 1]:>9}{self.sol['active_flow_F2'][i]:>11.3f}{self.sol['reactive_flow_F2'][i]:>12.3f}{self.sol['active_flow_2F'][i]:>14.3f}{self.sol['reactive_flow_2F'][i]:>12.3f}{abs(self.sol['active_flow_F2'][i])-abs(self.sol['active_flow_2F'][i]):>11.3f}{abs(self.sol['reactive_flow_F2'][i])-abs(self.sol['reactive_flow_2F'][i]):>9.3f} |")
            file.write("\n")
            file.write("-"*89)

        file.close()