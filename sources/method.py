# !/usr/bin/env python3
# -*- coding_ctrl: utf-8 -*-

# ------------------------------------- #
# Created by: Joao Pedro Peters Barbosa #
# email: joao.peters@ieee.org           #
# ------------------------------------- #

def metodo(
    powerflow,
):
    '''chamada automática do método de solução selecionado

    Parâmetros
        powerflow: self do arquivo powerflow.py
    '''

    ## Inicialização
    # Chamada específica método de Newton-Raphson Não-Linear
    if powerflow.method == 'NEWTON':
        from admittance import admit
        from newtonraphson import newton
        
        admit(
            powerflow,
        )
        
        newton(
            powerflow,
        )

    # Chamada específica método de Gauss-Seidel
    elif powerflow.method == 'GAUSS':
        # self.gaussseidel(
        #     powerflow,
        # )
        pass

    # Chamada específica método de Newton-Raphson Linearizado
    elif powerflow.method == 'LINEAR':
        from admittance import admitlinear
        from linear import lpf

        admitlinear(
            powerflow,
        )
        
        lpf(
            powerflow,
        )

    # Chamada específica método Desacoplado
    elif powerflow.method == 'DECOUP':
        # self.decoupledpowerflow(
        #     powerflow,
        # )
        pass

    # Chamada específica método Desacoplado Rápido
    elif powerflow.method == 'fDECOUP':
        # self.fastdecoupledpowerflow(
        #     powerflow,
        # )
        pass

    # Chamada específica método Continuado
    elif powerflow.method == 'CPF':
        from admittance import admit
        from continuation import cpf
        from newtonraphson import newton
                
        admit(
            powerflow,
        )
        
        newton(
            powerflow,
        )
        
        cpf(
            powerflow,
        )

    # Chamada especifica metodo Cross-Entropy
    elif powerflow.method == 'CENT':
        from admittance import admit
        from crossentropy import cent
        
        admit(
            powerflow,
        )
        
        cent(
            powerflow,
        )

    # Chamada especifica geracao estocastica inicial de valores
    if powerflow.method == 'STOCH':
        from admittance import admit
        from stochastic import stoch
        
        admit(
            powerflow,
        )
        
        stoch(
            powerflow,
        )
        
    # Chamada especifica metodo direto (Canizares, 1993)
    if powerflow.method == 'CANI':
        from admittance import admit
        from directmethod import cani
        
        admit(
            powerflow,
        )
        
        cani(
            powerflow,
        )