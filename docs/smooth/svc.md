# SPF-SVC

A modelagem de Compensadores Estáticos via funções sigmoides permite que o fluxo de potência trate as mudanças de regime (linear para saturação) de forma contínua e derivável. Isso elimina a necessidade de lógica discreta durante as iterações e possibilita o uso do método de **Full Newton**.

## 1. Funções Sigmoides como Chaves de Transição

As chaves sigmoides ($sw$) atuam como funções de passo suavizadas. O parâmetro de inclinação define a rapidez da transição. Para um ganho elevado, a chave assume comportamento binário (0 ou 1) quase instantaneamente ao cruzar o limite definido.

### 1.1 Parâmetros de Ajuste: SIGK, SIGA, SIGI e SIGQ

A precisão do modelo e a suavidade da transição dependem de constantes específicas, cuja aplicação varia conforme a variável de controle do SVC. Cabe ressaltar que o modelo aplicado na simulação depende estritamente do **modo de controle** inserido na **coluna C** do código de execução **DCER** informado no arquivo `.pwf`.

* **SIGK ($k$):** Define a declividade (ganho) da função. Controla quão "abrupta" é a transição entre o regime linear e a saturação.
* **SIGA ($\epsilon_\alpha$):** Parâmetro de precisão para chaves que monitoram o **ângulo de disparo** ($\alpha$).
* **SIGI ($\epsilon_i$):** Parâmetro de precisão para chaves que monitoram a **corrente** do compensador ($I_{svc}$).
* **SIGQ ($\epsilon_q$):** Parâmetro de precisão para chaves que monitoram a **potência reativa** ($Q_{svc}$).

**Valores Típicos:**
Para representar o comportamento físico com rigor numérico, utilizam-se:

> **SIGK = 1e8** | **SIGA = 1e-6** | **SIGI = 1e-6** | **SIGQ = 1e-6**

---

## 2. Modelagem por Injeção de Potência Reativa e Corrente

Ambas as metodologias baseiam-se na relação entre a variável de controle ($Q_{G,svc}$ ou $I_{svc}$) e a tensão da barra controlada ($V_m$).

### Equação de Controle Unificada ($y$)

A equação combina as três regiões operativas em uma única expressão contínua:

1. **Região Indutiva ($sw = 1$):** O SVC opera como um reator fixo em seu limite mínimo.
2. **Região Linear ($sw = 0$):** O controle de tensão atua para manter $V_m$ no valor de referência $V_{m}^{ref}$ considerando o *estatismo* ($r$).
3. **Região Capacitiva ($sw = 1$):** O SVC opera como um banco de capacitores fixo em seu limite máximo.

---

## 3. Modelagem por Ângulo de Disparo de Tiristores ($\alpha$)

Esta é a representação de maior detalhamento, onde a variável de estado é o ângulo $\alpha$ (tipicamente entre $90^\circ$ e $180^\circ$).

### A Lógica de Quatro Chaves e o *Backoff*

O uso de quatro chaves ($sw9$ a $sw12$) é uma inovação para tratar a relação inversa entre o ângulo de disparo e a tensão.

* **Chaves de Ângulo ($sw9, sw10$):** Monitoram os limites físicos dos tiristores ($\alpha_{min}, \alpha_{max}$). Utilizam o parâmetro **SIGA**.
* **Chaves de Tensão ($sw11, sw12$):** Monitoram a necessidade da rede (tensão de referência).

A rotina de **backoff** permite que o sistema identifique quando uma barra saturada deve retornar ao regime linear através do produto cruzado das chaves, garantindo que o controle só mude de estado quando ambas as condições (ângulo e tensão) forem satisfeitas simultaneamente.

---

## 4. Estrutura da Matriz Jacobiana Aumentada

A integração ao método de Newton-Raphson expande a Jacobiana de $(2N_{bus} \times 2N_{bus})$ para $(2N_{bus} + N_{svc} \times 2N_{bus} + N_{svc})$.

### Novos Termos Diferenciais

* $\frac{\partial P}{\partial x}, \frac{\partial Q}{\partial x}$: Sensibilidade da rede à variável de estado do SVC ($Q_{G,svc}, I_{svc}$ ou $\alpha$).
* $\frac{\partial y}{\partial \theta}, \frac{\partial y}{\partial V}$: Resposta da equação de controle às variações da rede.
* $\frac{\partial y}{\partial x}$: Auto-sensibilidade da equação de controle. Incorpora o estatismo ($r$) na região linear.

---

## 5. Implementação no Fluxo de Potência de Continuação (CPF)

Esta modelagem é ideal para o traçado de curvas P-V, pois permite representar com precisão os **Limites de Injeção de Reativo (LIB)**. No modelo suavizado, o LIB não é um ponto de descontinuidade, mas uma transição rápida que o método de continuação consegue contornar sem divergência numérica, provendo diagnósticos precisos sobre a margem de estabilidade de tensão.

---

**Referências:**

* **BARBOSA, J. P. P.** [Using sigmoid functions for representing limits of generators and static Var compensators and their impact on the voltage stability study, 2023](https://repositorio.ufjf.br/jspui/handle/ufjf/15471)