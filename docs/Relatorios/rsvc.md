<!-- # Relatórios de Simulação
## Relatório de Barra (`RBARRA`)

No relatório de barras é feito um levantamento dos resultados de tensão nodal (magnitude e ângulo de fase), potência gerada ativa e reativa, potência demandada ativa e reativa, e potência reativa de equipamento elétrico shunt para todas as barras do SEP em estudo.

O relatório de barras é gerado automaticamente e é salvo no diretório `/Sistemas/Resultados/RelatorioBarra/`.

Na formulação padrão, o cabeçalho do relatório de barras é gerado da seguinte forma:

```
Mês dia, Ano
-------------------------------------------------------------------------------------
                                   SISTEMA {nome do SEP}
                                 RELATÓRIO DE BARRAS
-------------------------------------------------------------------------------------
                                     # iterações
-------------------------------------------------------------------------------------
|     BARRA    |      TENSAO     |        GERACAO      |       CARGA      |  SHUNT  |
-------------------------------------------------------------------------------------
|   NOME   | T |   MOD   |  ANG  |    MW   |    Mvar   |   MW   |   Mvar  |   Mvar  |

```

## Relatório de Linha (`RLINHA`)
No relatório de linhas é feito um levantamento dos resultados de potência ativa e reativa entre barras `k` e `m`, potência ativa e reativa entre barras `m` e `k`, assim como um levantamento de perdas de potência ativa e reativa para todas as linhas do SEP em estudo.

O relatório de linhas é gerado automaticamente e é salvo no diretório `/Sistemas/Resultados/RelatorioLinha/`.

Na formulação padrão, o cabeçalho do relatório de linha é gerado da seguinte forma:

```
Mês dia, Ano
-----------------------------------------------------------------------------------------
                                     SISTEMA {nome do SEP}
                                   RELATÓRIO DE LINHAS
-----------------------------------------------------------------------------------------
                                       # iterações
-----------------------------------------------------------------------------------------
|     BARRA      |     SENTIDO DE->PARA    |     SENTIDO PARA->DE    | PERDAS ELÉTRICAS |
-----------------------------------------------------------------------------------------
|  DE   |  PARA  |  Pkm[MW]  |  Qkm[Mvar]  |  Pmk[MW]  |  Qmk[Mvar]  |    MW   |  Mvar  |
-----------------------------------------------------------------------------------------
```

<!-- ## Relatório de Geração (`RGERAC`)
--- --> -->