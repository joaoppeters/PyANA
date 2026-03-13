Esta documentação técnica detalha a implementação da modelagem sigmoide para o tratamento de limites de potência reativa de geradores no projeto **PyANA**, conforme a metodologia proposta em sua dissertação (EESC-USP, 2024).

---

# Tratamento de Limites de Reativo via Funções Sigmoides (SPF-Generators)

Esta seção descreve a formulação de **Fluxo de Potência Suavizado (SPF)** aplicada aos limites de geração de potência reativa ($Q_G$). Diferente da abordagem tradicional que realiza o chaveamento de barras (PV $\leftrightarrow$ PQ), esta metodologia utiliza chaves sigmoides para manter a diferenciabilidade do sistema de equações e permitir uma transição suave entre os regimes de operação.

## 1. Nova Estrutura de Variáveis e Jacobiana

Para habilitar a suavização, a potência reativa gerada ($Q_{G,gen}$) deixa de ser uma variável dependente e passa a ser uma **variável de estado** do problema.

* **Vetor de Estado:** Expandido para incluir $Q_{G,gen}$ para cada gerador ativo.
* **Dimensão da Jacobiana:** Aumentada para $(2N_{bus} + N_{gen}) \times (2N_{bus} + N_{gen})$.
* **Abordagem Full Newton:** As novas equações de controle são incorporadas internamente na matriz Jacobiana, permitindo a solução simultânea de todo o sistema.

---

## 2. As Quatro Chaves Sigmoides

A modelagem utiliza um conjunto de quatro chaves sigmoides para definir o estado operativo do gerador. Elas monitoram tanto a geração de reativo quanto a magnitude da tensão na barra.

### Chaves de Potência Reativa ($Q_{G}$)

Monitoram se o gerador está operando dentro dos limites físicos:

* **$sw1$**: Identifica violação do limite **superior** ($Q_G \geq Q_{G}^{max}$).
* **$sw2$**: Identifica violação do limite **inferior** ($Q_G \leq Q_{G}^{min}$).

### Chaves de Tensão ($V$)

Monitoram o desvio da tensão em relação à referência ($V_{ref}$), permitindo a rotina de *backoff* (retorno ao controle de tensão):

* **$sw3$**: Relacionada ao limite superior de tensão.
* **$sw4$**: Relacionada ao limite inferior de tensão.

---

## 3. Equação de Controle Equivalente

As chaves são combinadas logicamente (utilizando lógica de tabelas de verdade) em uma única equação de controle $y$, que substitui a restrição de tensão ou reativo:

$$y = (sw1 \cdot sw3) \cdot (1 - sw2 \cdot sw4) \cdot (Q_{G,gen} - Q_{G}^{max})$$

$$+ (1 - sw1 \cdot sw3) \cdot (1 - sw2 \cdot sw4) \cdot (V - V_{ref})$$

$$+ (1 - sw1 \cdot sw3) \cdot (sw2 \cdot sw4) \cdot (Q_{G,gen} - Q_{G}^{min})$$

### Estados Operativos Resultantes

| Estado | Descrição | Resíduo Ativo ($\Delta y$) |
| --- | --- | --- |
| **1** | Violação de Limite Superior | $Q_{G}^{max} - Q_{G,gen}$ |
| **2** | *Backoff* de Limite Superior | $V_{ref} - V$ |
| **3** | Operação Normal (Controle de V) | $V_{ref} - V$ |
| **4** | *Backoff* de Limite Inferior | $V_{ref} - V$ |
| **5** | Violação de Limite Inferior | $Q_{G}^{min} - Q_{G,gen}$ |

A rotina de **backoff** é o grande diferencial: ela permite que um gerador que atingiu o limite de reativo retorne automaticamente ao modo de controle de tensão assim que as condições do sistema permitirem, sem necessidade de lógicas externas de "religa/desliga".

---

## 4. Integração na Matriz Jacobiana

A inclusão da variável $Q_{G,gen}$ e da equação de controle $y$ adiciona novos termos diferenciais à Jacobiana. A estrutura aumentada segue o padrão:

$$\begin{bmatrix} \Delta P \\ \Delta Q \\ \Delta y \end{bmatrix} = 
\begin{bmatrix} 
H & N & \frac{\partial P}{\partial Q_{G}} \\
M & L & \frac{\partial Q}{\partial Q_{G}} \\
\frac{\partial y}{\partial \theta} & \frac{\partial y}{\partial V} & \frac{\partial y}{\partial Q_{G}}
\end{bmatrix}
\begin{bmatrix} \Delta \theta \\ \Delta V \\ \Delta Q_{G} \end{bmatrix}$$

## 5. Vantagens da Metodologia

1. **Eliminação do Chaveamento de Barras:** Evita instabilidades numéricas e ciclos infinitos entre PV e PQ.
2. **Diferenciabilidade:** Essencial para métodos de continuação (`EXIC`) e métodos diretos (`EXPC`).
3. **Estabilidade de Tensão:** Permite transformar limites de indução em bifurcações sela-nó (SNB), provendo diagnósticos mais precisos sobre o colapso de tensão.

---

**Referências:**

* **PONTES, R. P.** [A full Newton approach to consider reactive power generation limits in power flow problem using sigmoid switches, 2018](https://ieeexplore.ieee.org/abstract/document/8395801)