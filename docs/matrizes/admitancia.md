# Matriz Admitância de Barra ($Y_{bus}$)

A **Matriz Admitância ($Y_{bus}$)** é a representação nodal dos componentes passivos de um Sistema Elétrico de Potência (SEP). Ela estabelece a relação linear entre as correntes injetadas e as tensões nas barras:

$$[I_{bus}] = [Y_{bus}] [V_{bus}]$$

No contexto deste projeto, a $Y_{bus}$ é construída a partir da leitura dos dados de linha e transformadores do arquivo `.pwf` e serve como base estática para o cálculo dos resíduos de potência e da Matriz Jacobiana nos métodos **EXLF**, **EXIC** e **EXPC**.

---

## 1. Modelagem dos Componentes

Para cada ramo conectando uma barra $i$ a uma barra $j$, o programa modela os parâmetros conforme o circuito equivalente em $\pi$.

### I. Linhas de Transmissão (LTs)

A admitância série é o inverso da impedância informada ($r + jx$):


$$y_{ij} = \frac{1}{r_{ij} + jx_{ij}} = g_{ij} + jb_{ij}$$

A susceptância capacitiva (shunt) da linha é distribuída igualmente entre as barras $i$ e $j$:


$$y_{sh,ij} = j\frac{b_{total}}{2}$$

### II. Transformadores com Tap ($a:1$)

Se o transformador possui um tap $a$ no lado da barra $i$ (barra "DE"), o modelo em $\pi$ é modificado para:

* **Admitância equivalente série:** $y_{ij} = \frac{y_{cc}}{a}$
* **Shunt no lado $i$:** $y_{sh,i} = \frac{1-a}{a^2} y_{cc}$
* **Shunt no lado $j$:** $y_{sh,j} = \frac{a-1}{a} y_{cc}$

---

## 2. Algoritmo de Montagem

A matriz $Y_{bus}$ é uma matriz complexa de dimensão $N \times N$. Sua montagem segue as seguintes regras:

### Elementos da Diagonal ($Y_{ii}$)

Representam a soma de todas as admitâncias conectadas à barra $i$, incluindo ramos incidentes e elementos shunt fixos (capacitores/reatores):

$$Y_{ii} = \sum_{j \in \Omega_i} \left( \frac{y_{ij}}{a_{ij}^2} + j\frac{b_{sh,ij}}{2} \right) + y_{shunt,fixo}$$

### Elementos Fora da Diagonal ($Y_{ij}$)

Representam a admitância de transferência negativa entre as barras:

$$Y_{ij} = Y_{ji} = -\frac{y_{ij}}{a_{ij}}$$

*Nota: Se o ramo for uma linha comum, o tap $a$ é considerado $1$.*

---

## 3. Implementação e Eficiência Numérica

No projeto, a construção da matriz utiliza as seguintes premissas:

1. **Esparsidade:** Como uma barra típica se conecta a apenas 2 ou 3 outras, a maioria dos elementos de $Y_{bus}$ é zero. O projeto utiliza estruturas de **matrizes esparsas** para otimizar a memória.
2. **Tratamento de Shunts:** Os dados de susceptância informados no `.pwf` em Mvar são convertidos para valores em *p.u.* antes da inserção na diagonal.
3. **Recálculo:** A matriz é mantida constante durante as iterações do Newton-Raphson. No entanto, se houver controle de Tap ativo (`CTAP`), a matriz é atualizada conforme o ajuste da razão de transformação.

---

## 4. Aplicação no Fluxo de Potência

A $Y_{bus}$ fornece os valores de condutância ($G_{ij}$) e susceptância ($B_{ij}$) necessários para calcular as potências injetadas em cada barra $i$:

$$P_i = V_i \sum_{j=1}^{N} V_j (G_{ij} \cos\theta_{ij} + B_{ij} \sin\theta_{ij})$$

$$Q_i = V_i \sum_{j=1}^{N} V_j (G_{ij} \sin\theta_{ij} - B_{ij} \cos\theta_{ij})$$

Onde $V$ é a magnitude da tensão e $\theta_{ij}$ é a diferença angular entre as barras $i$ e $j$.

---