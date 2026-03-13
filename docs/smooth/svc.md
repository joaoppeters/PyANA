# Modelagem Técnica Detalhada: SPF-SVC

A modelagem de Compensadores Estáticos via funções sigmoides permite que o fluxo de potência trate as mudanças de regime (linear para saturação) de forma contínua e derivável. Isso elimina a necessidade de lógica discreta durante as iterações e possibilita o uso do método de **Full Newton**.

## 1. Funções Sigmoides como Chaves de Transição

As chaves sigmoides ($sw$) atuam como funções de passo suavizadas. O parâmetro de inclinação ($slp$) define a rapidez da transição. Para um $slp$ elevado (ex: $10^8$), a chave assume comportamento binário (0 ou 1) quase instantaneamente ao cruzar o limite definido ($lim$).

### Propriedades Matemáticas:

* **Valor High (1):** Quando a variável monitorada ultrapassa o limite superior ($V > lim^{sup}$ ou $\alpha > lim^{\alpha}$).
* **Valor Low (0):** Quando a variável está abaixo do limite ou dentro da faixa de controle.
* **Diferenciabilidade:** Ao contrário de um modelo ideal de chaveamento, a sigmoide possui derivada em todos os pontos, o que é essencial para o preenchimento dos termos de sensibilidade na Matriz Jacobiana.

---

## 2. Modelagem por Injeção de Potência Reativa e Corrente

Ambas as metodologias baseiam-se na relação entre a variável de controle ($Q_{G,svc}$ ou $I_{svc}$) e a tensão da barra controlada ($V_m$).

### Equação de Controle Unificada ($y$)

A equação combina as três regiões operativas em uma única expressão contínua:

1. **Região Indutiva ($sw = 1$):** O SVC opera como um reator fixo em seu limite mínimo.
2. **Região Linear ($sw = 0$):** O controle de tensão atua para manter $V_m$ no valor de referência $V_{m}^{ref}$ considerando o *estatismo* ($r$).
3. **Região Capacitiva ($sw = 1$):** O SVC opera como um banco de capacitores fixo em seu limite máximo.

**Resíduo do Fluxo de Potência ($\Delta y$):** Durante as iterações, o objetivo é zerar $y$. Dependendo de qual chave está ativa, o algoritmo de Newton "escolhe" automaticamente qual física aplicar àquela barra sem intervenção externa.

---

## 3. Modelagem por Ângulo de Disparo de Tiristores ($\alpha$)

Esta é a representação de maior detalhamento, onde a variável de estado é o ângulo $\alpha$ (tipicamente entre $90^\circ$ e $180^\circ$).

### A Lógica de Quatro Chaves e o *Backoff*

O uso de quatro chaves ($sw9$ a $sw12$) é uma inovação para tratar a relação inversa entre o ângulo de disparo e a tensão.

* **Chaves de Ângulo ($sw9, sw10$):** Monitoram os limites físicos dos tiristores.
* **Chaves de Tensão ($sw11, sw12$):** Monitoram a necessidade da rede.

A rotina de **backoff** (Regiões 2 e 4 na Tabela 5.3) permite que o sistema identifique quando uma barra saturada deve retornar ao regime linear. Isso ocorre através do produto cruzado das chaves (ex: $sw10 \cdot (1 - sw12)$), garantindo que o controle só mude de estado quando ambas as condições (ângulo e tensão) forem satisfeitas simultaneamente.

---

## 4. Estrutura da Matriz Jacobiana Aumentada

Para integrar o SVC ao método de Newton-Raphson tradicional, a Matriz Jacobiana é expandida de $(2N_{bus} \times 2N_{bus})$ para $(2N_{bus} + N_{svc} \times 2N_{bus} + N_{svc})$.

### Novos Termos Diferenciais

Os novos blocos da matriz contêm as seguintes sensibilidades:

* **$\frac{\partial P}{\partial x}, \frac{\partial Q}{\partial x}$**: Como as potências ativa e reativa na rede variam com a mudança da variável de estado do SVC ($Q_{G,svc}, I_{svc}$ ou $\alpha$). Note que $\frac{\partial P}{\partial x}$ costuma ser zero para SVCs.
* **$\frac{\partial y}{\partial \theta}, \frac{\partial y}{\partial V}$**: Como a equação de controle do SVC responde às variações de ângulo e tensão da rede.
* **$\frac{\partial y}{\partial x}$**: A auto-sensibilidade da equação de controle. Em regiões saturadas, este termo é unitário; na região linear, ele incorpora o estatismo ($r$).

### Vantagem Numérica

Diferente de métodos que "travam" a barra como PV ou PQ e recalculam a matriz, o **SPF-SVC** mantém a estrutura da matriz constante. A transição é feita apenas pelos valores numéricos dentro dos termos de sensibilidade, o que resulta em uma convergência mais robusta, especialmente em sistemas próximos ao colapso de tensão.

---

## 5. Implementação no Fluxo de Potência de Continuação (CPF)

Esta modelagem é ideal para o traçado de curvas P-V, pois permite representar com precisão os **Limites de Injeção de Reativo (LIB)**. No modelo suavizado, o LIB não é um ponto de descontinuidade, mas uma transição rápida que o método de continuação consegue contornar sem divergência numérica.