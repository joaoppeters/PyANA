# Fluxo de Potência CEPEL via Python (PyANA)

Ferramenta Python de código aberto projetada para auxiliar estudantes e pesquisadores na análise de **Sistemas Elétricos de Potência (SEP)** em regime permanente. O projeto foca na compatibilidade com o padrão CEPEL, permitindo a leitura de arquivos `.pwf`, `.stb`, `.dat`, `.cdu`, `.blt` e `.sav`.

> **REPOSITÓRIO EM DESENVOLVIMENTO!**
> Foco atual: Simulações de fluxo de potência convencional e análise de estabilidade de tensão (Curva P-V).

---

## 🚀 Funcionalidades Implementadas

1. **Fluxo de Potência Newton-Raphson (EXLF):** Análise convencional de redes.
2. **Fluxo de Potência Continuado (EXIC):** Traçado de curvas P-V via previsão e correção (Ajjarapu & Christy, 1992).
3. **Método Direto do Ponto de Colapso (EXPC):** Localização direta do limite de estabilidade (Canizares, 1992).

---

## 🛠️ Instalação e Requisitos

Certifique-se de ter o Python instalado e execute:

```bash
# Clone o repositório
git clone https://github.com/joaoppeters/PyANA.git

# Instale as dependências
pip install -r requirements.txt

```

**Dependências:** `matplotlib`, `numpy`, `pandas`, `scipy`, `sympy`.

---

## ⚙️ Configuração e Parâmetros

As opções de controle e monitoração são extraídas diretamente das flags e dados contidos nos arquivos **.pwf** ou **.stb**.

### 1. Opções de Controle

* **`'FREQ'`**: Regulação primária de frequência (conforme dados de gerador).
* **`'QLIM'`**: Tratamento de limites de potência reativa de geradores.

> **Modelagem por Sigmoide:** Ao ativar a opção de controle `SMTH L` no código de execução ou no `DOPC` do arquivo, o controle de `QLIM` passa a utilizar modelagem sigmóide para suavização das não-linearidades, melhorando a convergência em cenários críticos. O mesmo é válido para o caso de simulação de sistemas com código de execução `DCER` presente no arquivo `.pwf`. Para detalhes e mais informações, consulte a página de [documentação deste repositório sobre suavização](docs/smooth/sigmoid.md) e leia a [dissertação de mestrado de João P. Peters](https://repositorio.ufjf.br/jspui/handle/ufjf/15471).
> **SMTH L** No caso de ativação desta opção de controle, alterar as informações das seguintes outras opções de controle: `SIGA`, `SIGV`, `SIGQ`, `SIGI`, `SIGK` (verificar documentação).

### 2. Opções de Monitoração

As variáveis monitoradas devem ser especificadas nos códigos de execução `DMET`, `DMFL`, `DMGR`, `DMTE` e `DOPC` (com as opções de controle e execução `MOCF`, `MOCG`, `MOCT`)

---

## 💻 Exemplo de Execução

A interface principal utiliza a classe `PowerFlow`. Os argumentos de controle e monitoração devem refletir o que está configurado nos arquivos do sistema.

```python
from powerflow import PowerFlow

config = {
    "system": "ieee14.pwf",
    "method": "EXPC",           # Método Direto do Ponto de Colapso
}

PowerFlow(**config)

```

---

## 📂 Estrutura de Arquivos

* **/sistemas:** Local para armazenar os arquivos de entrada (`.pwf`, `.stb`, `.dat`, `.cdu`, `.blt` e `.sav`).
* **/docs:** Documentação técnica detalhada.
* [Cálculo da Matriz Admitância](docs/matrizes/admitancia.md)
* [Matriz Jacobiana Reduzida](docs/matrizes/jreduzida.md)
* [Matriz Jacobiana Alternada (ANAREDE)](docs/matrizes/jalternada.md)
* [Método de Newton-Raphson](docs/numerical/newtonraphson.md)
* [Modelagem Sigmóide](docs/smooth/sigmoid.md)



---

## 📖 Referências Técnicas

* **AJJARAPU, P.; CHRISTY, C.** [The continuation power flow: a tool for steady state stability analysis, 1992](https://ieeexplore.ieee.org/document/141737)
* **CANIZARES, C. A.** [Point of collapse and continuation methods for large AC/DC systems, 1993](https://ieeexplore.ieee.org/document/221241)
* **BARBOSA, J. P. P.** [Using sigmoid functions for representing limits of generators and static Var compensators and their impact on the voltage stability study, 2023](https://repositorio.ufjf.br/jspui/handle/ufjf/15471)
* **La GATTA, P. O.** [Um novo modelo para representação da regulação primária e secundária de frequência no problema de fluxo de potência e fluxo de potência ótimo, 2012](https://repositorio.ufjf.br/jspui/handle/ufjf/1937)
---