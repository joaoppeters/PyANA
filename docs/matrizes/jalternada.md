# Matriz Jacobiana Alternada (Formulação ANAREDE)

Diferente da formulação por blocos ($H, N, M, L$), a **Jacobiana Alternada** organiza os resíduos e as variáveis de estado seguindo a ordem física das barras. Para cada barra $i$, as equações e variáveis são agrupadas em pares $(P_i, Q_i)$ e $(\theta_i, V_i)$.

O sistema linearizado assume a seguinte forma:

$$\begin{bmatrix} 
\vdots \\ \Delta P_i \\ \Delta Q_i \\ \vdots 
\end{bmatrix} = 
\begin{bmatrix} 
\ddots & \vdots & \vdots & \dots \\
\dots & \frac{\partial P_i}{\partial \theta_j} & \frac{\partial P_i}{\partial V_j} & \dots \\
\dots & \frac{\partial Q_i}{\partial \theta_j} & \frac{\partial Q_i}{\partial V_j} & \dots \\
\dots & \vdots & \vdots & \ddots
\end{bmatrix}
\begin{bmatrix} 
\vdots \\ \Delta \theta_j \\ \Delta V_j \\ \vdots 
\end{bmatrix}$$

---

## 1. Estrutura de Indexação

Na formulação alternada, a posição de uma barra $i$ na matriz não é dividida em duas metades distantes. Em vez disso, os elementos são organizados em submatrizes $2 \times 2$ para cada interação entre as barras $i$ e $j$:

$$J_{ij} = \begin{bmatrix} 
H_{ij} & N_{ij} \\
M_{ij} & L_{ij} 
\end{bmatrix}$$

Onde o sistema completo segue a sequência:
**Vetor de Resíduos:** $[\Delta P_1, \Delta Q_1, \Delta P_2, \Delta Q_2, \dots, \Delta P_n, \Delta Q_n]^T$
**Vetor de Correções:** $[\Delta \theta_1, \Delta V_1, \Delta \theta_2, \Delta V_2, \dots, \Delta \theta_n, \Delta V_n]^T$

---

## 2. Derivadas Parciais (Cálculo dos Elementos)

Os valores individuais baseiam-se nos elementos da **Matriz Admitância ($Y_{bus}$)**, onde $Y_{ij} = G_{ij} + jB_{ij}$.

### Elementos Fora da Diagonal ($i \neq j$)

Representam a sensibilidade entre barras distintas:

* $H_{ij} = \frac{\partial P_i}{\partial \theta_j} = V_i V_j (G_{ij} \sin \theta_{ij} - B_{ij} \cos \theta_{ij})$
* $N_{ij} = \frac{\partial P_i}{\partial V_j} = V_i (G_{ij} \cos \theta_{ij} + B_{ij} \sin \theta_{ij})$
* $M_{ij} = \frac{\partial Q_i}{\partial \theta_j} = -V_i V_j (G_{ij} \cos \theta_{ij} + B_{ij} \sin \theta_{ij})$
* $L_{ij} = \frac{\partial Q_i}{\partial V_j} = V_i (G_{ij} \sin \theta_{ij} - B_{ij} \cos \theta_{ij})$

### Elementos da Diagonal ($i = j$)

Representam a auto-sensibilidade da barra:

* $H_{ii} = \frac{\partial P_i}{\partial \theta_i} = -Q_i - B_{ii} V_i^2$
* $N_{ii} = \frac{\partial P_i}{\partial V_i} = \frac{P_i}{V_i} + G_{ii} V_i$
* $M_{ii} = \frac{\partial Q_i}{\partial \theta_i} = P_i - G_{ii} V_i^2$
* $L_{ii} = \frac{\partial Q_i}{\partial V_i} = \frac{Q_i}{V_i} - B_{ii} V_i$

---

## 3. Redução da Matriz (Slack e PV)

Mesmo no formato alternado, as restrições de barra devem ser aplicadas:

1. **Barra Slack:** As linhas e colunas referentes a $P_{slack}$, $Q_{slack}$, $\theta_{slack}$ e $V_{slack}$ são removidas (ou substituídas por uma identidade com resíduo zero), pois esses valores são fixos.
2. **Barras PV:** Como a tensão $V_i$ é controlada, a variação $\Delta V_i$ é zero e a equação de $Q_i$ é "descartada" para o cálculo do passo. Na prática, a linha de $\Delta Q_i$ e a coluna de $\Delta V_i$ são removidas da matriz de iteração.

---

## 4. Comparação: Alternada vs. Reduzida (Blocos)

| Característica | Jacobiana por Blocos (Reduzida) | Jacobiana Alternada (ANAREDE) |
| --- | --- | --- |
| **Organização** | Blocos $H, N, M, L$ separados. | Pares $P, Q$ adjacentes. |
| **Vantagem** | Mais intuitiva para cálculos teóricos. | Melhor preservação da esparsidade em bandas. |
| **Complexidade** | Simples de programar com fatiamento de arrays. | Requer indexação cuidadosa ($2i$ e $2i+1$). |
| **Uso no Projeto** | Implementada como padrão. | Citada como referência externa. |

---