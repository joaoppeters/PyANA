# Relatório de Linha - `'RLIN'`

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
|  DE   |  PARA  |  Pkm[MW]  |  Qkm[MVAr]  |  Pmk[MW]  |  Qmk[MVAr]  |    MW   |  MVAr  |
-----------------------------------------------------------------------------------------
```

<!-- ## Relatório de Geração (`RGERC`)
--- -->