# Newton-Raphson Power-Flow 

O principal objetivo deste projeto é fornecer um código Python base para apoiar pesquisadores em estudos relacionados à análise de regime permanente de sistemas de potência.

Este é um projeto em desenvolvimento, involuntariamente influenciado por [amandapavila/GovernorPowerFlow](https://github.com/amandapavila/GovernorPowerFlow).



## Requisitos Mínimos 
---
Para funcionamento dessa metodologia, é necessário instalar as seguintes `bibliotecas de Python`:
```
numpy
pandas
```



## Leitura de Dados
---
Os Dados do Sistema de Potência em estudo devem estar organizados em um arquivo `.pwf`.

Um exemplo da leitura de dados do arquivo `.pwf` é mostrado abaixo:

> **Nota** O resto do código está omitido. Verifique este [exemplo](Exemplos/example-main.py) para ter uma experiência completa.

```Python
arqv = os.path.join('ieee14.pwf')
dbarra, dlinha = LeituraPWF(arqv=arqv)
```
- `arqv: str, obrigatória, valor padrão igual a 'None'`
    - Indica o diretório onde está localizado o arquivo de dados `.pwf` do sistema elétrico em estudo
    - Utilize a função `os.path.join()` ao referenciar o arquivo do sistema elétrico em estudo



## Matriz Admitância 
---    
Antes de inicializar o fluxo de potência, a matriz admitância (Y<sub>BARRA</sub>) necessita ser calculada. 

Esse processo ocorre dentro da chamada da classe `PowerFlow()`.

Para mais detalhes sobre o cálculo e montagem dessa matriz, [leia o código](Exemplos/flow.py).



## Formulação da Matriz Jacobiana
---
A Matriz Jacobiana pode é modelada de uma única maneira:
- `'Completa':` Configuração tradicional, vetor coluna ∆P-∆Q associado ao vetor coluna ∆θ-∆V ([Ver exemplo](Exemplos/Jacobiana/Completa-Jacobiana.md)).
    - Para equações de controle `y` adicionais, associadas a variáveis de estado `x`, a formulação é reestruturada para ∆P-∆Q-∆y associado ao vetor coluna ∆θ-∆V-∆x.


## Fluxo de Potência
---
A chamada do fluxo de potência é apresentada a seguir:

> **Nota** O resto do código é omitido. Verifique este [exemplo](Exemplos/example-main.py) para ter uma experiência completa.

```Python
PF = PowerFlow(dbarra=dbarra, dlinha=dlinha).NewtonRaphson()
```
- `dbarra: DataFrame, obrigatorio, valor padrão igual a 'None'`
    - Dados de barra obtidos na leitura do arquivo `.pwf`
- `dlinha: DataFrame, obrigatorio, valor padrão igual a 'None'`
    - Dados de linha obtidos na leitura do arquivo `.pwf`



## Relatório
---
A solução de fluxo de potência Newton-Raphson gera 2 relatórios principais:

- `'RBARRA':` Gera o Resultado de Dados de Barra em caso Convergente ou Divergente. (Consulte [exemplo](Exemplos/Relatorios/RBARRA.md) para entender como esses dados são armazenados e apresentados).

- `'RLINHA':` Gera o Resultado de Dados de Linha em caso Convergente ou Divergente. (Consulte [example](Exemplos/Reports/RLINHA.md) para entender como esses dados são armazenados e apresentados).

<!-- - `'RBARGER':` Gera apenas o Resultado de Dados de Barras Geradoras em caso Convergente ou Divergente. (Consulte [exemplo](Exemplos/Reports/RBARGER.md) para entender como esses dados são armazenados e apresentados). -->

Um exemplo da configuração da Matriz Jacobiana escolhida sendo inserida no programa principal é mostrado abaixo:

> **Nota** O resto do código é omitido. Verifique este [exemplo](Exemplos/example-main.py) para ter uma experiência completa.

```Python
Relatorio(pf=PF, rel='RBARRA RLINHA')
```
- `pf: dict, obrigatório, valor padrão igual a 'None'`
    - Repassa os resultados de convergência ou divergência do Fluxo de Potência realizado
- `rel: str, opicional, valor padrão igual a 'None'`
    - Indica a opção de relatório a ser apresentada
        - Apresentação de 1, 2 ou mesmo todas as opções de relatório
    - Os relatórios serão salvos automaticamente em pasta separada