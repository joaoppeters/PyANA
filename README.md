# Fluxo de Potência ANAREDE via Python

O principal objetivo deste projeto é fornecer um código Python  para `apoiar estudantes e pesquisadores` em estudos de `análise de regime permanente de sistemas elétricos de potência`. Para isso, toma-se como base a leitura de dados de `arquivos ANAREDE (.pwf)`.



## Requisitos Mínimos
`Bibliotecas de Python` empregadas no projeto e necessárias para o correto funcionamento das ferramentas:
```
numpy
pandas
```



## Métodos de Solução
Serão desenvolvidos aqui `diferentes ferramentas para análise de SEPs em regime permanente`, como por exemplo:
- [Solução do Fluxo de Potência Não-Linear via Método de Newton-Raphson](docs/Metodos/newton-raphson.md)

<!-- - [Solução de Fluxo de Potência Não-Linear via Método de Gauss-Seidel](docs/Metodos/gauss-seidel.md) -->

- [Solução do Fluxo de Potência Linearizado](docs/Metodos/linear.md)

<!-- - [Solução de Fluxo de Potência Desacoplado](docs/Metodos/decoup.md)

- [Solução de Fluxo de Potência Desacoplado Rápido](docs/Metodos/fast-decoup.md) -->

- [Solução do Fluxo de Potência Continuado (AJJARAPU; CHRISTY, 1992)](docs/Metodos/continuation.md)

> **Para todos os efeitos, considere que este é um projeto em desenvolvimento e que tais ferramentas serão integradas em partes.**



## Leitura de Dados
Os dados do Sistema Elétrico de Potência em estudo devem estar organizados em um arquivo `.pwf`.

Utilize a pasta entitulada [sistemas](sistemas) para armazenar os arquivos `.pwf` que contém os `dados de SEP` que pretende de estudar/analisar.

Um exemplo de inicialização de variável para leitura de dados do arquivo `.pwf` é mostrado abaixo:

```Python
system = 'ieee14.pwf'
```

> **Ao inicializar a variável com o nome do sistema que gostaria de analisar, certifique-se que o arquivo `.pwf` deste sistema está contido na pasta [sistemas](sistemas/).**



## Matriz Admitância
A matriz Admitância (Y<sub>BARRA</sub>) é calculada antes da inicialização de `qualquer uma das opções de metodologias` para solução do fluxo de potência.

Para mais detalhes sobre o cálculo e montagem dessa matriz, [clique aqui](docs/Admitancia/admitancia.md).



## Formulação da Matriz Jacobiana
A Matriz Jacobiana é modelada de uma única maneira:

- `'Completa':` Vetor coluna de resíduos das `equações diferenciáveis ∆P-∆Q` associado ao vetor coluna de resíduos das `variáveis de estado ∆θ-∆V` ([Ver formulação](docs/Jacobiana/completa.md)).
    - Para `equações de controle y` adicionais, associadas a `variáveis de estado x`, essa formulação é reestruturada para associar o vetor coluna de resíduos de `equações diferenciáveis ∆P-∆Q-∆y` ao vetor coluna de resíduos de `variáveis de estado ∆θ-∆V-∆x`.

> No entanto a Matriz Jacobiana pode ser configurada nas formulações [`Alternada`](docs/Jacobiana/alternada.md) ou mesmo [`Reduzida`](docs/Jacobiana/reduzida.md) (**essas formulações não foram implementadas**).



## Fluxo de Potência
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
    - **Utilize arquivos `.pwf` presentes dentro da pasta [sistemas](sistemas).**

- `method: str, obrigatório, valor padrão 'NEWTON'`
    - **Apenas uma opção poder ser escolhida por vez.**
    - **Opções:**
        - `'NEWTON'` - [soluciona o SEP através do método de Newton-Raphson.](docs/Metodos/newton-raphson.md)
        <!-- - `'GAUSS'` - [soluciona o SEP através do método de Gauss-Seidel.](docs/Metodos/gauss-seidel.md) -->
        - `'LINEAR'` - [soluciona o SEP através do método de Newton Raphson Linearizado.](docs/Metodos/linear.md)
        <!-- - `'DECOUP'` - [soluciona o SEP através do método Desacoplado.](docs/Metodos/decoup.md)
        - `'fDECOUP'` - [soluciona o SEP através do método Desacoplado Rápido.](docs/Metodos/fast-decoup.md) -->
        - `'CPF'` - [soluciona o SEP através do método de Fluxo de Potência Continuado.](docs/Metodos/continuation.md)

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

        - `'RCPF'` - [gera o relatório do processo iterativo do Fluxo de Potência Continuado em caso Convergente ou Divergente.](docs/Relatorios/rcontinuado.md)


> **PASSE OS PARÂMETROS DA CLASSE `PowerFlow()` DA FORMA COMO MELHOR DESEJAR.** 

> **O CÓDIGO ABAIXO SE TRATA DE UM EXEMPLO, NÃO CONDIZ COM A REAL APLICAÇÃO PRÁTICA DEVIDO AO FATO QUE NEM TODAS AS OPÇÕES DE CONTROLE PODEM SER ATRIBUÍDAS AO MESMO TEMPO.**  

```Python
from powerflow import PowerFlow

system='ieee14.pwf', 
    
method='NEWTON', 

control=['CREM', 'CST', 'CTAP', 'CTAPd', 'FREQ', 'QLIM', 'SVCs', 'VCTRL']

monitor=['PFLOW', 'PGMON', 'QGMON', 'VMON']
    
report=['RBAR', 'RLIN', 'RGER', 'RSVC', 'RCPF']

PowerFlow(
    system=system, 
    method=method,  
    control=control, 
    monitor=monitor, 
    report=report,
)
```
