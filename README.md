# Fluxo de Potência CEPEL via Python

Ferramenta Python de código aberto projetada para auxiliar estudantes e pesquisadores na análise de **Sistemas Elétricos de Potência (SEP)** em regime permanente, com suporte à leitura de arquivos padrão CEPEL (`.pwf`, `.stb`, `.dat`, `.cdu`, `.blt`, `.sav` e `.his`).

> **REPOSITÓRIO EM DESENVOLVIMENTO.**
> Atualmente focado em simulações de fluxo de potência em regime permanente e análise de estabilidade de tensão (curva P-V).

## 🚀 Funcionalidades Implementadas

1. **Fluxo de Potência Newton-Raphson (EXLF):** Análise convencional de redes em regime permanente.
2. **Fluxo de Potência Continuado (EXIC):** Variação dinâmica de carga para traçar curvas P-V (baseado no comando `DINC`).
3. **Método Direto do Ponto de Colapso (EXPC):** Cálculo direto do limite máximo de carregamento.

---

## 🛠️ Instalação e Requisitos

O projeto utiliza bibliotecas científicas padrão. Certifique-se de ter o Python instalado e execute os comandos abaixo:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nome-do-repo.git

# Instale as dependências
pip install -r requirements.txt

```

**Bibliotecas principais:** `numpy`, `pandas`, `scipy`, `matplotlib`, `sympy`.

---

## 📂 Estrutura de Uso

### 1. Preparação dos Dados

Coloque seus arquivos `.pwf`, `.stb`, `.dat`, `.cdu`, `.blt`, `.sav` e/ou `.his` na pasta [/sistemas](sistemas/). O código fará a leitura automática a partir deste diretório.

### 2. Métodos Disponíveis

| Código | Método | Referência |
| --- | --- | --- |
| **EXLF** | Newton-Raphson Não-Linear | Convencional |
| **EXIC** | Fluxo Continuado (Previsão/Correção) | Ajjarapu & Christy (1992) |
| **EXPC** | Método Direto (Ponto de Colapso) | Canizares (1992) |

---

## 💻 Exemplo de Execução

A interface principal é feita através da classe `PowerFlow`. Abaixo, um exemplo de configuração completa:

```python
from powerflow import PowerFlow

# Configurações da simulação
config = {
    "system": "ieee14.pwf",
    "method": "EXLF",
    "control": ["FREQ", "QLIM", "SVCs"],
    "monitor": ["VMON", "PFLOW"],
    "report": ["RBAR", "RLIN", "RGER"]
}

# Execução
PowerFlow(**config)

```

---

## ⚙️ Parâmetros da Classe `PowerFlow()`

### Argumentos Principais

* `system` (str): Nome do arquivo `.pwf` dentro da pasta `/sistemas`.
* `method` (str): Escolha entre `EXLF`, `EXIC` ou `EXPC`.

### Opções de Controle (`control`)

* `'FREQ'`: Regulação primária de frequência.
* `'QLIM'`: Limites de geração de potência reativa.
* `'SVCs'`: Controle de tensão via Compensadores Estáticos.

### Monitoração e Relatórios (`monitor` & `report`)

* `'VMON'`: Magnitude de tensão nas barras.
* `'PFLOW'`: Fluxo de potência ativa nas linhas.
* `'RBAR'`: Relatório completo de dados de barra (salvo em `/sistemas`).

---

## 📖 Documentação Técnica

Para detalhes sobre a implementação das matrizes e algoritmos, consulte:

* [Cálculo da Matriz Admitância](docs/matrizes/admitancia.md)
* [Formulação da Matriz Jacobiana Reduzida](docs/matrizes/jreduzida.md)
* [Detalhes do Método de Newton-Raphson](docs/numerical/newtonraphson.md)

---

**Gostaria que eu gerasse o conteúdo de algum dos outros arquivos de documentação listados no seu projeto?**