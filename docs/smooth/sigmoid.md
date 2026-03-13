# Formulação de Fluxo de Potência Suavizado (Smooth Power Flow) utilizando Funções Sigmóides

Esta documentação descreve a implementação da técnica de **Fluxo de Potência Suavizado (Smooth Power Flow - SPF) utilizando funções sigmoides**. O objetivo principal desta abordagem é transformar as descontinuidades causadas pelos limites operacionais e controles de dispositivos elétricos em funções contínuas e diferenciáveis, melhorando a convergência e a análise de estabilidade de tensão.

## 1. Visão Geral

No Fluxo de Potência (FP) tradicional, os limites operacionais (como limites de geração de reativo em barras PV) são tratados como inequações que causam mudanças discretas no tipo de barra (chaveamento PV $\leftrightarrow$ PQ). Essas descontinuidades podem causar problemas de convergência e dificultar a identificação de pontos críticos.

A formulação **SPF** propõe:

* A substituição de funções descontínuas por **funções degrau suavizadas** (*smooth step functions*).
* A modelagem de controles e saturações de dispositivos (Geradores e SVCs) por meio de **chaves sigmoides**.
* A transformação de limites de indução de carga (*Load Inducibility Boundaries - LIB*) em bifurcações sela-nó (*Saddle-Node Bifurcations - SNB*), facilitando a análise de margem de carga.

---

## 2. A Função Sigmoide

A função sigmoide é utilizada para realizar a transição suave entre dois estados operacionais (ex: 0 e 1, ou modo saturado e não-saturado).

### Definição Matemática

A equação da sigmoide implementada é:

$$sig(x) = \frac{1}{1 + e^{-slp \cdot (x - lim)}}$$

Onde:

* $x$: Variável de entrada (ex: tensão ou potência reativa).
* $slp$ (*slope*): Determina a inclinação da curva. Valores altos aproximam a função de um degrau ideal.
* $lim$ (*limite*): O ponto de inflexão onde ocorre a transição.

### Propriedade de Derivação

Para a integração na **Matriz Jacobiana**, utiliza-se a derivada da sigmoide:

$$\frac{\partial \, sig(x)}{\partial x} = slp \cdot (1 - sig(x)) \cdot sig(x)$$

---

## 3. Validade da Suavização

Para que a função sigmoide seja válida em problemas de fluxo de potência, ela deve satisfazer os critérios de uma *Smooth Step Function* (conforme Neves, 2022):

1. **Limite:** Quando $slp \rightarrow \infty$, a função deve se comportar como um degrau unitário.
2. **Continuidade:** A função deve ser $C^1$ (contínua e com primeira derivada contínua).
3. **Concavidade:** A mudança de concavidade deve ocorrer exatamente no ponto de especificação ($lim$).

O uso da sigmoide permite que o sistema de equações do fluxo de potência permaneça diferenciável em todo o domínio operacional, eliminando a necessidade de "lógica de chaveamento" brusca.

---

## 4. Processo de Implementação (Chaves Sigmoides)

A lógica para modelar dispositivos com múltiplos estados operativos (ex: Mínimo, Controle, Máximo) baseia-se em tabelas de verdade, onde as funções sigmoides atuam como variáveis lógicas $[0, 1]$.

### Exemplo: Controle Genérico

Considere um dispositivo com três estados baseados em uma variável $B$:

1. **Saturado no Mínimo:** $A = A^{min}$ se $B > B^{ref}$
2. **Em Controle:** $A^{min} < A < A^{max}$ se $B = B^{ref}$
3. **Saturado no Máximo:** $A = A^{max}$ se $B < B^{ref}$

Para modelar isso, utilizamos duas chaves sigmoides ($swa1$ e $swa2$) com comportamentos alternados. A equação de controle equivalente ($yc$) que é incorporada ao sistema não-linear é:

$$yc = swa1 \cdot yc_1 + swa2 \cdot yc_2 + (1 - swa1) \cdot (1 - swa2) \cdot yc_3$$

Onde $yc_1, yc_2, yc_3$ são as equações correspondentes a cada modo de operação.

---

## 5. Vantagens no PyANA

* **Convergência:** Redução de oscilações numéricas causadas pelo chaveamento de barras PV-PQ.
* **Estabilidade:** Permite o rastreamento da curva P-V além do ponto de máximo carregamento sem singularidades artificiais.
* **Precisão:** Mantém a acurácia da solução final enquanto fornece informações de sensibilidade (via Jacobiana) em todo o processo.

---

## 6. Referências

* **NEVES, L. S.** [Smooth Power Flow Model for Unified Voltage Stability Assessment: Theory and Computation, 2022](https://ieeexplore.ieee.org/abstract/document/9693213)
* **PONTES, R. P.** [A full Newton approach to consider reactive power generation limits in power flow problem using sigmoid switches, 2018](https://ieeexplore.ieee.org/abstract/document/8395801)
* **PETERS, J. P.** [Using sigmoid functions for representing limits of generators and static Var compensators and their impact on the voltage stability study, 2023](https://repositorio.ufjf.br/jspui/handle/ufjf/15471)