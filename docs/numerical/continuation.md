# Método de Newton-Raphson Continuado (EXIC)

O **Fluxo de Potência Continuado (Continuation Power Flow - CPF)** é uma técnica robusta utilizada para traçar a curva completa de carregamento de um sistema elétrico ($P \times V$). Ele é essencial para identificar o **Ponto de Máximo Carregamento (PMC)**, onde a Jacobiana convencional do Fluxo de Potência torna-se singular.

O processo baseia-se no esquema de **Previsão e Correção**, seguindo a metodologia de Ajjarapu e Christy (1992).

---

## 1. Formulação Matemática

No fluxo de potência convencional, o carregamento é fixo. No EXIC, as equações de balanço de potência são modificadas para incluir o fator de carregamento $\lambda$ como uma variável independente:

$$f(\theta, V, \lambda) = 0$$

As potências ativa ($P$) e reativa ($Q$) em cada barra $i$ são reformuladas como:

* $P_{i}(\theta, V, \lambda) = P_{Gi}(\lambda) - P_{Li}(\lambda) - P_{Ti}(\theta, V) = 0$
* $Q_{i}(\theta, V, \lambda) = Q_{Gi}(\lambda) - Q_{Li}(\lambda) - Q_{Ti}(\theta, V) = 0$

Onde o carregamento varia tipicamente de forma linear:

* $P_{Li} = P_{Li0} + \lambda (k_{Li} S_{base})$
* $P_{Gi} = P_{Gi0} + \lambda (k_{Gi} S_{base})$

---

## 2. As Etapas do Algoritmo

### I. Etapa de Previsão (Tangente)

Para encontrar um palpite inicial para o próximo ponto na curva, calcula-se o vetor tangente à solução atual. Derivando as equações de fluxo em relação a um parâmetro de continuação $s$:

$$\left[ \frac{\partial f}{\partial \theta} \quad \frac{\partial f}{\partial V} \quad \frac{\partial f}{\partial \lambda} \right] \begin{bmatrix} d\theta \\ dV \\ d\lambda \end{bmatrix} = 0$$

Para resolver este sistema (que possui uma variável a mais que o número de equações), fixa-se uma das componentes do vetor tangente (variável de continuação) como $\pm 1$.

### II. Etapa de Correção (Sistema Ampliado)

Após a previsão, o ponto estimado é corrigido para retornar à curva de solução real. Para evitar a singularidade da Jacobiana no PMC, o EXIC utiliza uma **equação de parametrização** adicional $g(x, \lambda) = 0$:

$$\begin{bmatrix} f(\theta, V, \lambda) \\ x_k - \eta \end{bmatrix} = 0$$

Onde $x_k$ é a variável de continuação escolhida (aquela que apresenta a maior variação no passo de previsão) e $\eta$ é o valor previsto para essa variável. O sistema resultante é:

$$\begin{bmatrix} \Delta P \\ \Delta Q \\ \Delta x_k \end{bmatrix} = \begin{bmatrix} J & f_\lambda \\ e_k & 0 \end{bmatrix} \begin{bmatrix} \Delta \theta \\ \Delta V \\ \Delta \lambda \end{bmatrix}$$

A matriz ampliada permanece não-singular mesmo no PMC, permitindo que o método ultrapasse o "nariz" da curva $P \times V$ e analise a região de estabilidade inferior.

---

## 3. Implementação no Projeto

O método é ativado através do argumento `method='EXIC'`.

```python
from powerflow import PowerFlow

# Execução do Fluxo Continuado
PowerFlow(
    system='ieee14.pwf', 
    method='EXIC',      # Algoritmo de Ajjarapu & Christy
)

```

## 4. Diferenças entre EXIC e EXPC

* **EXIC (Continuado):** Calcula toda a trajetória da curva de carregamento via passos de previsão/correção.
* **EXPC (Ponto de Colapso):** Aplica o método direto de Canizares (1992) para saltar diretamente para o ponto de singularidade, sem calcular os pontos intermediários da curva.

---