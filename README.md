# O Arquivo de Rivendell

> *Um sistema digital para catalogar o conhecimento da Terra-média.*

Este projeto implementa um sistema de gerenciamento de dados para a Sociedade do Anel, permitindo a catalogação de personagens, decifração de idiomas, registros históricos e planejamento logístico de suprimentos. O sistema consome dados reais via API e organiza-os por meio de estruturas de dados.

## 📋 Funcionalidades

O programa opera através de um menu interativo no terminal com quatro módulos principais:

1.  **O Censo (Busca de Entidades):** Consulta rápida de personagens (ex: Aragorn, Frodo) consumindo dados da *The One API*.
2.  **O Palantír Linguístico (Autocompletar):** Sistema de busca por prefixo para palavras e dicionários élficos.
3.  **O Almanaque das Eras (Eventos Históricos):** Banco de dados de eventos históricos com busca por ano específico ou por intervalo de tempo.
4.  **A Bolsa do Aventureiro (Logística):** Algoritmo para montar a mochila de suprimentos maximizando a utilidade dos itens dentro de um limite de peso.

## 🛠️ Pré-requisitos

* **Python 3.8+** instalado.
* Gerenciador de pacotes `pip`.
* Uma chave de API (gratuita) da [The One API](https://the-one-api.dev).

## 🚀 Instalação e Configuração

### 1. Clone ou baixe o repositório
Certifique-se de estar na pasta raiz do projeto (onde está o arquivo `main.py`).

### 2. Instale as dependências
O projeto utiliza a biblioteca `requests` para comunicação com a API.
```bash
pip install -r requirements.txt
```
---

### Definir Chave API

É necessário possuir uma chave de API da **The One API** para usar este programa.

1.  Obtenha sua chave [neste link](https://the-one-api.dev).
2.  Após obter sua chave, configure-a como uma variável de ambiente no seu terminal.

---

#### Linux / macOS

```bash
export THE_ONE_API_KEY="SUA-CHAVE-API-AQUI"
```

#### Windows (CMD)
```bash
set THE_ONE_API_KEY=SUA-CHAVE-API-AQUI
```

#### Windows (Powershell)
```bash
$env:THE_ONE_API_KEY = "SUA-CHAVE-API-AQUI"
```

**Nota Importante**: Os comandos acima definem a chave apenas para a sessão atual do terminal.

---

## 🏃‍♂️ Como Executar

Após configurar a chave, inicie a aplicação principal:

```bash
python3 main.py
```

Siga as instruções numéricas no menu para navegar entre os módulos.
