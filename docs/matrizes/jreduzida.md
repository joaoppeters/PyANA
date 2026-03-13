# Matriz Jacobiana Reduzida

A **Matriz Jacobiana** é o elemento central do método de Newton-Raphson. Ela representa a sensibilidade das variações de potência ativa ($P$) e reativa ($Q$) em relação às variações de ângulo ($\theta$) e magnitude de tensão ($V$).

Neste projeto, implementamos a **Jacobiana Reduzida**, que otimiza o esforço computacional ao remover equações de barras que possuem valores fixos ou restrições específicas (como a Barra Slack e Barras PV no cálculo de reativo).

---

## 1. Estrutura Geral da Matriz

A equação linearizada do passo de Newton é definida por:

$$\begin{bmatrix} \Delta P \\ \Delta Q \end{bmatrix} = [J] \begin{bmatrix} \Delta \theta \\ \Delta V \end{bmatrix} = \begin{bmatrix} H & N \\ M & L \end{bmatrix} \begin{bmatrix} \Delta \theta \\ \Delta V \end{bmatrix}$$

Onde os subblocos são as derivadas parciais:

* **H:** $\partial P / \partial \theta$
* **N:** $\partial P / \partial V$
* **M:** $\partial Q / \partial \theta$
* **L:** $\partial Q / \partial V$

---

## 2. Processo de Redução (Remoção de Linhas/Colunas)

Diferente de uma matriz completa $2N \times 2N$, a Jacobiana Reduzida remove as variáveis cujos valores já são conhecidos "a priori", evitando que a matriz se torne singular.

### I. Barra de Referência (Slack Bus)

Como o ângulo $\theta$ e a tensão $V$ são fixos na barra de referência:

* **Ação:** Remove-se a linha e a coluna correspondentes a $\Delta P_{slack}$ e $\Delta \theta_{slack}$, bem como $\Delta Q_{slack}$ e $\Delta V_{slack}$.

### II. Barras de Geração (PV)

Nestas barras, a magnitude da tensão $V$ é mantida constante pelo regulador do gerador:

* **Ação:** Remove-se a linha referente ao resíduo de potência reativa ($\Delta Q$) e a coluna referente à correção de tensão ($\Delta V$).
* **Resultado:** A barra PV contribui apenas para o bloco **H** ($\Delta P / \Delta \theta$).

### III. Resumo das Dimensões

Seja $n$ o número total de barras, $ng$ o número de barras PV e $1$ a barra Slack:

* **Ângulos ($\Delta \theta$):** $n - 1$ variáveis.
* **Tensões ($\Delta V$):** $n - 1 - ng$ variáveis.
* **Dimensão Total:** $(2n - 2 - ng) \times (2n - 2 - ng)$.

---

## 3. Formulação Matemática dos Elementos

Os elementos da matriz são calculados com base nos componentes da **Matriz Admitância ($Y_{bus}$)**, onde $Y_{ij} = G_{ij} + jB_{ij}$:

### Elementos Fora da Diagonal ($i \neq j$)

* $H_{ij} = L_{ij} = V_i V_j (G_{ij} \sin\theta_{ij} - B_{ij} \cos\theta_{ij})$
* $N_{ij} = -M_{ij} = V_i V_j (G_{ij} \cos\theta_{ij} + B_{ij} \sin\theta_{ij})$

### Elementos da Diagonal ($i = j$)

* $H_{ii} = -Q_i - B_{ii} V_i^2$
* $L_{ii} = Q_i - B_{ii} V_i^2$
* $N_{ii} = P_i + G_{ii} V_i^2$
* $M_{ii} = P_i - G_{ii} V_i^2$

---

## 4. Implementação no Código

No programa, a redução é feita através de um mapeamento de índices:

1. **Identificação:** O código varre o arquivo `.pwf` e identifica o tipo de cada barra (PQ, PV ou Slack).
2. **Mapeamento:** Cria-se um vetor de "índices ativos".
3. **Montagem:** A matriz é montada inicialmente de forma esparsa. As linhas e colunas desnecessárias não são calculadas ou são filtradas antes da inversão do sistema linear.
4. **Atualização:** Como a Jacobiana depende de $V$ e $\theta$, ela é **recalculada em cada iteração** do Newton-Raphson até que os resíduos $\Delta P$ e $\Delta Q$ estejam abaixo da tolerância especificada.

---