# Método de Newton-Raphson para Análise de Fluxo de Potência em regime permanente (EXLF)

## 1. Visão Geral do Método Numérico

O método de **Newton-Raphson (NR)** é uma técnica numérica iterativa utilizada para encontrar as raízes de um sistema de equações não lineares $f(x) = 0$. Ele se baseia na expansão da série de Taylor de primeira ordem, aproximando a função linearmente em cada etapa para se aproximar da solução.

A fórmula iterativa fundamental é:

$$x^{(k+1)} = x^{(k)} - [J(x^{(k)})]^{-1} f(x^{(k)})$$

Onde:

* $x^{(k)}$: Vetor de variáveis desconhecidas na iteração $k$.
* $f(x^{(k)})$: Vetor de resíduos ou desvios (a diferença entre os valores desejados e calculados).
* $J(x^{(k)})$: A **Matriz Jacobiana**, que contém as derivadas parciais das funções em relação às variáveis.

---

## 2. Aplicação ao Fluxo de Potência (EXLF)

No contexto deste projeto, o método NR é o núcleo do **EXLF** (Solução de Fluxo de Potência Não Linear). O objetivo é determinar as magnitudes de tensão ($V$) e os ângulos ($\theta$) em cada barra de um Sistema Elétrico de Potência (SEP).

### As Equações de Resíduo (Mismatches)

O algoritmo resolve o balanço de potência em cada barra calculando os "desvios" de potência ativa ($\Delta P$) e potência reativa ($\Delta Q$):

* $\Delta P_i = P_{i, \text{especificado}} - P_{i, \text{calculado}}$
* $\Delta Q_i = Q_{i, \text{especificado}} - Q_{i, \text{calculado}}$

### A Jacobiana do Fluxo de Potência

A matriz Jacobiana relaciona os desvios de potência com as correções necessárias para os ângulos e magnitudes de tensão das barras:

$$\begin{bmatrix} \Delta P \\ \Delta Q \end{bmatrix} = \begin{bmatrix} \frac{\partial P}{\partial \theta} & \frac{\partial P}{\partial V} \\ \frac{\partial Q}{\partial \theta} & \frac{\partial Q}{\partial V} \end{bmatrix} \begin{bmatrix} \Delta \theta \\ \Delta V \end{bmatrix}$$

> **Nota:** Este projeto implementa uma formulação de **Matriz Jacobiana Reduzida**, que difere da versão "alternada" utilizada pelo software tradicional ANAREDE.

---

## 3. Uso no Projeto

Para realizar uma simulação utilizando este método, a classe `PowerFlow` deve ser inicializada com o argumento `method='EXLF'`.

### Exemplo de Implementação

```python
from powerflow import PowerFlow

# Define o arquivo do sistema (deve estar na pasta /sistemas)
system = 'ieee14.pwf' 

# Executa o Fluxo de Potência Newton-Raphson
PowerFlow(
    system=system, 
    method='EXLF', 
    control=['QLIM', 'SVCs'], # Controles opcionais
    monitor=['VMON', 'PFLOW'] # Monitoramentos opcionais
)

```

### Vantagens e Requisitos

* **Convergência Quadrática:** O método converge muito rapidamente se a estimativa inicial estiver próxima da solução.
* **Integração de Controles:** Diversos controles secundários, como regulação de frequência (`FREQ`) e limites de potência reativa (`QLIM`), podem ser integrados às iterações do NR.
* **Fonte de Dados:** Requer um arquivo `.pwf` válido armazenado no diretório `sistemas/`.

---