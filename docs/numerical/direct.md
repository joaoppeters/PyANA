# Método Direto do Ponto de Colapso (EXPC)

O método **EXPC** implementa uma abordagem direta para a determinação do **Ponto de Colapso (Point of Collapse - PoC)** em Sistemas Elétricos de Potência. Diferente do método continuado (**EXIC**), que traça a curva $P \times V$ por passos, o EXPC utiliza a formulação de Canizares (1992) para localizar o limite de estabilidade de tensão através da solução de um sistema de equações ampliado.

---

## 1. Fundamentos e Formulação Matemática

O ponto de colapso de um sistema é caracterizado matematicamente como uma bifurcação sela-nó (*saddle-node bifurcation*), onde a matriz Jacobiana do sistema torna-se singular (determinante zero).

Para evitar a divergência numérica associada à singularidade, o EXPC resolve um sistema de equações estendido que define o ponto crítico de forma única.

### O Sistema de Equações Ampliado

O problema é formulado como a busca pelas variáveis de estado $x$ (ângulos e magnitudes de tensão), o fator de carregamento crítico $\lambda_c$, e o vetor próprio à esquerda $w$:

$$\Phi(x, \lambda, w) = \begin{bmatrix} 
f(x, \lambda) \\ 
J(x, \lambda)^T w \\ 
\|w\| - 1 
\end{bmatrix} = 0$$

Onde:

* $f(x, \lambda) = 0$: Representa as equações de balanço de potência ativa e reativa em regime permanente.
* $J(x, \lambda)^T w = 0$: É a condição de singularidade. No ponto de colapso, existe um vetor próprio não nulo $w$ associado ao autovalor zero da transposta da matriz Jacobiana.
* $\|w\| - 1 = 0$: É uma equação de normalização necessária para garantir uma solução única e não trivial para o vetor $w$ (geralmente utiliza-se a norma euclidiana ou fixa-se uma componente do vetor como unitária).

### Solução via Newton-Raphson

Para resolver este sistema ampliado de dimensão $2n + 1$ (onde $n$ é o número de equações de fluxo), utiliza-se o método de Newton-Raphson, exigindo o cálculo das derivadas de segunda ordem (Hessianas) do sistema original para compor a nova matriz Jacobiana do sistema ampliado.

---

## 2. Comparativo Técnico

| Característica | EXIC (Continuado) | EXPC (Ponto de Colapso) |
| --- | --- | --- |
| **Objetivo Principal** | Traçar toda a trajetória da curva $P \times V$. | Identificar diretamente o limite máximo de carregamento. |
| **Referência Base** | Ajjarapu & Christy (1992). | Canizares (1992). |
| **Esforço Computacional** | Alto (requer múltiplas execuções de previsão e correção). | Médio/Alto (resolve um sistema de dimensões duplicadas em poucos passos). |
| **Estabilidade Numérica** | Extremamente robusto em todo o domínio. | Requer uma estimativa inicial próxima ao ponto de colapso para convergir. |

---

## 3. Aplicação no Projeto

Para executar o cálculo direto do ponto crítico, utilize o argumento `method='EXPC'`:

```python
from powerflow import PowerFlow

# Localização direta do Ponto de Colapso
PowerFlow(
    system='ieee14.pwf', 
    method='EXPC',      # Método Direto (Canizares)
)

```

> **Nota:** Devido à necessidade de uma boa estimativa inicial, é comum utilizar o resultado de algumas iterações do método **EXIC** como ponto de partida para o **EXPC**.

---

## 4. Referências Relacionadas

* [EXLF: Fluxo de Potência Não-Linear](https://www.google.com/search?q=docs/Metodos/newtonraphson.md)
* [Matriz Jacobiana Reduzida](https://www.google.com/search?q=docs/Jacobiana/reduzida.md)

---

**Deseja que eu prepare a documentação de um dos controles específicos, como o tratamento de limites de reativo (`QLIM`) ou regulação de frequência (`FREQ`)?**