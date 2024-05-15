# Fluxo de Potência ANAREDE via Python

O objetivo deste projeto é fornecer um código Python Open-Source para `auxiliar estudantes e pesquisadores` em estudos de `análise de regime permanente de Sistemas Elétricos de Potência`. As simulações aqui realizadas dependem da leitura de dados de `arquivos ANAREDE (.pwf)`.

> **ESTE É UM REPOSITÓRIO EM DESENVOLVIMENTO.**

## Requisitos Mínimos
`Bibliotecas de Python` empregadas no projeto e necessárias para o correto funcionamento das ferramentas:
```
matplotlib
numpy
pandas
scipy
sympy
```

> **AO BAIXAR ESSE REPOSITÓRIO, RODAR O SEGUINTE COMANDO ABAIXO**
```cmd
pip install requirements.txt
```


A estrutura desse repositório está dividida em 5 etapas


## I. Leitura de Dados
Os dados do Sistema Elétrico de Potência em estudo devem estar organizados em um arquivo `.pwf`.

Utilize a pasta entitulada [sistemas](sistemas) para armazenar os arquivos `.pwf` que contém os `dados de SEPs` que pretende de estudar/analisar.

Um exemplo de inicialização de variável para leitura de dados do arquivo `.pwf` é mostrado abaixo:

```Python
system = 'ieee14.pwf'
```

> **AO INICIALIZAR A VARIÁVEL COM O NOME DO SISTEMA QUE GOSTARIA DE ANALISAR, CERTIFIQUE-SE QUE O ARQUIVO `.pwf` DESTE SISTEMA ESTÁ CONTIDO NA PASTA [sistemas](sistemas/).**



## II. Métodos de Solução
- [EXLF: Solução do Fluxo de Potência Não-Linear via Método de Newton-Raphson](docs/Metodos/newtonraphson.md)

<!-- - [Solução de Fluxo de Potência Não-Linear via Método de Gauss-Seidel](docs/Metodos/gauss-seidel.md) -->

<!-- - [Solução do Fluxo de Potência Linearizado](docs/Metodos/linear.md) -->

<!-- - [Solução de Fluxo de Potência Desacoplado](docs/Metodos/decoup.md)

- [Solução de Fluxo de Potência Desacoplado Rápido](docs/Metodos/fast-decoup.md) -->

- [EXIC: Solução do Fluxo de Potência Continuado - Previsão x Correção (AJJARAPU; CHRISTY, 1992)](docs/Metodos/continuation.md)

- [EXPC: Solução do Fluxo de Potência pelo Método Direto do cálculo do Ponto de Colapso (CANIZARES, 1992)](docs/Metodos/pointofcollapse.md)

> **OUTRAS METODOLOGIAS AINDA SERÃO IMPLEMENTADAS NESSE PROGRAMA**


### Matriz Admitância
Para mais detalhes sobre o cálculo e montagem dessa matriz, [clique aqui](docs/Admitancia/admitancia.md).


### Matriz Jacobiana
A construção da matriz jacobiana é feita de forma diferente nesse [programa](docs/Jacobiana/reduzida.md), em comparação com a do [ANAREDE](docs/Jacobiana/alternada.md). Essa última formulação não foi implementada nesse programa.


## III. Opções de Controle

## IV. Opções de Monitoração

## V. Opções de Relatório


## Conclusão
Para realizar a análise de fluxo de potência em regime permanente, `utilize a chamada da classe PowerFlow()` e passe os `parâmetros da classe` que gostaria de analisar.

```Python
from powerflow import PowerFlow

PowerFlow(
    system=system, 
    method=method, 
    control=control, 
    monitor=monitor, 
    report=report,
)
```
- `system: str, obrigatório, valor padrão ''`
    - **Variável que indica o nome do arquivo do SEP em estudo.**
    - **Utilize e adicione arquivos `.pwf` dentro da pasta [sistemas](sistemas).**

- `method: str, obrigatório, valor padrão 'EXLF'`
    - **Apenas uma opção poder ser escolhida por vez.**
    - **Opções:**
        - `'EXLF'` - [Solução do Fluxo de Potência Não-Linear via Método de Newton-Raphson](docs/Metodos/newtonraphson.md)
        <!-- - `'GAUSS'` - [soluciona o SEP através do método de Gauss-Seidel.](docs/Metodos/gauss-seidel.md) -->
        <!-- - `'LINEAR'` - [soluciona o SEP através do método de Newton Raphson Linearizado.](docs/Metodos/linear.md) -->
        <!-- - `'DECOUP'` - [soluciona o SEP através do método Desacoplado.](docs/Metodos/decoup.md)
        - `'fDECOUP'` - [soluciona o SEP através do método Desacoplado Rápido.](docs/Metodos/fast-decoup.md) -->
        - `'EXIC'` - [Solução do Fluxo de Potência Continuado - Previsão x Correção (AJJARAPU; CHRISTY, 1992)](docs/Metodos/continuation.md)
        - `'EXPC'` - [Solução do Fluxo de Potência pelo Método Direto do cálculo do Ponto de Colapso (CANIZARES, 1992)](docs/Metodos/pointofcollapse.md)

- `control: list, opcional, valor padrão list()`
    - **Os controles só serão aplicados caso seja selecionado o método de Newton-Raphson.**
    - **Opções:**
        <!-- - `'CREM'` - [controle remoto de magnitude de tensão de barras remotas.](docs/Controle/controle-remoto-tensao.md)
        - `'CST'` - [controle secundário de tensão de magnitude de tensão de barras remotas.](docs/Controle/controle-secundario-tensao.md)
        - `'CTAP'` - [controle automático de taps de transformadores em fase.](docs/Controle/controle-transformador-tap-variavel.md)
        - `'CTAPd'` - [controle automático de taps de transformadores defasadores.](docs/Controle/controle-transformador-defasador.md) -->
        - `'FREQ'` - [regulação primária de frequência.](docs/Controle/controle-regulacao-primaria-frequencia.md)
        - `'QLIM'` - [tratamento de limite de geração de potência reativa.](docs/Controle/controle-limite-potencia-reativa-geradores.md)
        - `'SVCs'` - [controle de magnitude de tensão por meio de compensador estático de potência reativa.](docs/Controle/controle-compensador-estatico-CER-SVCs.md)
        

- `monitor: list, opcional, valor padrão list()`
    - **Opções:**
        - `'PFLOW'` - [monitoramento do fluxo de potência ativa nas linhas de transmissão.](docs/Monitoramento/fluxo-potencia-ativa-LT.md)
        - `'PGMON'` - [monitoramento do fluxo de potência ativa gerado por geradores.](docs/Monitoramento/geracao-potencia-ativa-PV.md)
        - `'QGMON'` - [monitoramento do fluxo de potência reativa gerado por geradores.](docs/Monitoramento/geracao-potencia-reativa-PV.md)
        - `'VMON'` - [monitoramento da magnitude de tensão de barras do SEP.](docs/Monitoramento/tensao-barramentos.md)

- `report: list, opcional, valor padrão list()`
    - **Determina o conjunto de relatórios a serem gerados.**
    - **Apresentação de 1, 2 ou mesmo todas as opções de relatório.**
    - **Os relatórios serão salvos automaticamente em pasta gerada dentro da pasta [sistemas](/sistemas).**
    - **Opções:**
        - `'RBAR'` - [gera o relatório de Dados de Barra em caso Convergente ou Divergente.](docs/Relatorios/RBAR.md)

        - `'RLIN'` - [gera o relatório de Dados de Linha em caso Convergente ou Divergente.](docs/Relatorios/RLIN.md)

        - `'RGER'` - [gera o relatório de Dados de Barras Geradoras em caso Convergente ou Divergente.](docs/Relatorios/RGER.md)

        - `'RSVC'` - [gera o relatório de Dados de Compensadores Estáticos de Potência Reativa (SVCs) em caso Convergente ou Divergente.](docs/Relatorios/rsvc.md)


> **PASSE OS PARÂMETROS DA CLASSE `PowerFlow()` DA FORMA COMO MELHOR DESEJAR.** 

> **O CÓDIGO ABAIXO SE TRATA DE UM EXEMPLO, NÃO CONDIZ COM A REAL APLICAÇÃO PRÁTICA DEVIDO AO FATO QUE NEM TODAS AS OPÇÕES DE CONTROLE PODEM SER ATRIBUÍDAS AO MESMO TEMPO.**  

```Python
from powerflow import PowerFlow

system='ieee14.pwf', 
    
method='EXLF', 

control=['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'SVCs', 'VCTRL']

monitor=['PFLOW', 'PGMON', 'QGMON', 'VMON']
    
report=['RBAR', 'RLIN', 'RGER', 'RSVC', 'RXIC']

PowerFlow(
    system=system, 
    method=method,  
    control=control, 
    monitor=monitor, 
    report=report,
)
```
