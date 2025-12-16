# O Arquivo de Rivendell - Parte 2
## Cronograma de Desenvolvimento e Planejamento

Este documento detalha o plano de execução para a expansão do "Arquivo de Rivendell", focando em algoritmos de otimização (Grafos e Programação Dinâmica) e simulação de riscos.

---

## Cronograma de Entregas (Milestones)

O desenvolvimento foi dividido em 4 sprints semanais, culminando na entrega final em 25/02/2026.

### Milestone 1: A Cartografia e o Propósito
**Data de Entrega:** 03/02/2026

**Foco:** Definição da estratégia global e estruturação do Grafo (Mapa da Terra-média).

* **Definição do Objetivo da Sociedade (Módulo de Partida):**
    * Implementação do seletor de prioridade (ex: *Destruir o Anel* vs *Explorar*).
    * Definição de como essa escolha afetará os pesos das arestas no grafo futuro.
* **Módulo 6: O Mapa (Estrutura de Grafo):**
    * Implementação da estrutura de dados: **Grafo Ponderado Direcionado** (Vertices = Locais, Arestas = Rotas).
    * *Decisão de Design:* Implementação usando Lista de Adjacência para eficiência de espaço.
    * Parsing/Leitura dos dados geográficos (conectar locais carregados na Parte 1 com distâncias/tempos).
* **Módulo 3.1: Conexão de Entidades (Grafo de Relações):**
    * Criação de relacionamentos entre Personagens e Eventos Históricos (quem estava onde).

---

### Milestone 2: Caminhos e Correções
**Data de Entrega:** 11/02/2026

**Foco:** Algoritmos de busca em grafos e refinamento linguístico com Programação Dinâmica.

* **Módulo 6: Navegação (Algoritmo de Dijkstra):**
    * Implementação do algoritmo de **Dijkstra** para encontrar o Caminho de Menor Custo entre dois vértices (locais).
    * Adaptação do custo baseada na "Penalidade de Viagem".
* **Módulo 6.1: Consulta Local:**
    * Integração do Grafo com o Almanaque (B-Tree) e Censo (Hash) para listar eventos e idiomas ao chegar em um vértice.
* **Atualização do Módulo 2: O Corretor (Levenshtein):**
    * Implementação do cálculo de **Distância de Edição (Levenshtein)**.
    * Recurso de sugestão de palavras da Trie para entradas incorretas.

---

### Milestone 3: Logística Avançada e Comércio
**Data de Entrega:** 18/02/2026

**Foco:** Otimização de recursos utilizando Programação Dinâmica e Algoritmos Gulosos.

* **Módulo 4.1: O Peso da Batalha:**
    * Implementação de solução para decidir o subconjunto de itens.
* **Módulo 5.1: Encontros e Decisões:**
    * Lógica para avaliar novos itens encontrados na rota (trocar ou descartar) mantendo a otimização da mochila.
* **Módulo 5.2: A Arte do Escambo:**
    * Algoritmo para maximizar o ganho de utilidade em trocas nos assentamentos.

---

### Milestone 4: O Confronto e Análise Final
**Data de Entrega:** 25/02/2026

**Foco:** Simulação de riscos, integração total e relatório técnico.

* **Módulo 7: Sistema de Confrontos:**
    * **7.1 Probabilidade:** Implementação da Malícia, Eventos Negativos e Fator Aleatório.
    * **7.2 Mecânica:** Simulação de combate comparando *Poder de Combate da Sociedade* (baseado na utilidade dos itens) vs *Dificuldade*.
    * Aplicação de penalidades (perda de tempo ou itens) em caso de derrota/retirada.
* **Integração do Sistema:**
    * Fluxo completo: Escolha de Rota -> Cálculo de Risco -> Decisão Logística -> Viagem/Confronto -> Chegada.
* **Relatório Técnico Final:**
    * Documentação das novas estruturas (Grafos).
    * Justificativa das abordagens de Programação Dinâmica.
    * Análise de Complexidade atualizada.

---

## Requisitos Técnicos e Estruturas

Para esta etapa, as seguintes implementações manuais serão usadas:

1.  **Grafos (Adjacency List):** Para o mapa da Terra-média.
2.  **Dijkstra (com Heap/Priority Queue própria se necessário):** Para otimização de rotas.
3.  **Matriz de Programação Dinâmica:** Para a Distância de Levenshtein.
4.  **Tabela de Programação Dinâmica (Memoization ou Tabulation):** Para o problema da mochila sequencial/logística de viagem.

---
