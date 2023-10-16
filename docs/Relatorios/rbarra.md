# Relatório de Barra - `'RBAR'`

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
|   NOME   | T |   MOD   |  ANG  |    MW   |    MVAr   |   MW   |   MVAr  |   MVAr  |

```