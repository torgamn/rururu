# Relatório Técnico: O Arquivo de Rivendell

---

## 1. Introdução

O objetivo desse projeto foi desenvolver um sistema capaz de lidar com diferentes tipos de dados essenciais para a jornada da Sociedade do Anel. O objetivo consistia em processar essas informações, assim como escolher e implementar manualmente as estruturas de dados mais adequadas para cada cenário de uso, visando eficiência de tempo e espaço.

O sistema foi dividido em quatro módulos, cada um resolvendo um problema específico através de uma estrutura de dados ou algoritmo distinto.

---

## 2. Design e Estruturas Utilizadas

Para cada módulo, foi feita uma análise para determinar a melhor estrutura a ser utilizada. Abaixo mostramos essas escolhas.

### Módulo 1: O Censo da Terra-média (Cadastro de Entidades)
* **Problema:** Armazenar um catálogo de personagens e realizar consultas pontuais extremamente rápidas (ex: "O personagem X existe? Quais seus dados?").
* **Solução:** **Tabela Hash**.
* **Justificativa:** A Tabela Hash é a estrutura ideal para situações onde a velocidade de acesso é a prioridade. Transformando o nome do personagem (chave) em um índice numérico através de uma função de hash, conseguimos acessar o dado quase que instantaneamente, sem precisar percorrer uma lista.
* **Implementação:**
    * Utilizou-se tratamento de colisão por **encadeamento** (cada posição da tabela contém uma lista).
    * Foi implementado um redimensionamento dinâmico, quando a tabela fica 70% cheia, ela dobra de tamanho para manter as buscas rápidas.

### Módulo 2: O Palantír Linguístico (Análise de Idiomas)
* **Problema:** Armazenar palavras (dicionário) e fornecer funcionalidade de "autocompletar" ou buscar todas as palavras que começam com um determinado prefixo (ex: "Mith...").
* **Solução:** **Árvore Trie**.
* **Justificativa:** Uma Tabela Hash ou uma lista não seriam eficientes para realizar buscas por prefixo. Como a Trie organiza os dados de forma que palavras com o mesmo início compartilhem os mesmos nós na memória. Isso torna a busca por prefixos extremamente eficiente, dependendo apenas do tamanho da palavra buscada, e não do tamanho total do dicionário.

### Módulo 3: O Almanaque das Eras (Crônicas Históricas)
* **Problema:** Gerenciar um grande volume de eventos históricos por ano, simulando um banco de dados, com necessidade de buscas exatas e por intervalo (ex: "eventos entre o ano 1000 e 2000").
* **Solução:** **Árvore B**.
* **Justificativa:** A Árvore B é feita para minimizar operações de acesso (leitura/escrita). Ela é uma árvore balanceada e larga, onde cada nó pode conter múltiplas chaves. Isso mantém a árvore com altura baixa, garantindo que encontrar um ano ou um intervalo de anos seja bem rápido, assim como mantem os dados ordenados, o que facilita a listagem sequencial.

### Módulo 4: A Bolsa do Aventureiro (Logística)
* **Problema:** Selecionar quais itens levar na mochila dado um limite de peso, maximizando a utilidade total.
* **Solução:** **Algoritmo Guloso**.
* **Justificativa:** Foi escolhido a abordagem gulosa baseada na razão **Valor/Peso**. O algoritmo calcula quanto "valor" cada quilo de um item oferece e seleciona sempre os itens mais valiosos por quilo primeiro. Embora isso não garanta a solução ótima matemática no caso de itens indivisíveis (0/1), ela é leve e fornece uma solução excelente e rápida para o planejamento logístico imediato.

---

## 3. Análise de Complexidade (Big-O)

Abaixo apresentamos a complexidade de tempo para as operações principais implementadas:

| Estrutura / Algoritmo | Operação Principal | Complexidade Média | Pior Caso |
| :--- | :--- | :--- | :--- |
| **Tabela Hash** | Busca / Inserção | `O(1)` | `O(n)` (muitas colisões) |
| **Trie** | Busca / Inserção | `O(k)` | `O(k)` |
| **Árvore B** | Busca / Inserção | `O(\log n)` | `O(\log n)` |
| **Algoritmo Guloso** | Ordenação dos Itens | `O(n \log n)` | `O(n \log n)` |

> *Nota:* Na Trie, `k` representa o comprimento da palavra/chave.

---

## 4. Análise Amortizada (Estudo de Caso: Hash Table)

Um dos desafios de implementar estruturas dinâmicas, como a nossa Tabela Hash, é lidar com o crescimento dos dados. Realizamos aqui a **Análise Amortizada da Inserção com Redimensionamento**.

Na nossa Tabela Hash, a inserção padrão é muito rápida, `O(1)`. Porém, quando a tabela atinge seu fator de carga (70%), precisamos executar a função `_resize()`. Esta função:
1.  Cria uma nova tabela com o dobro do tamanho.
2.  Percorre a tabela antiga inteira.
3.  Reinsere todos os elementos na nova tabela.

Essa operação de resize custa `O(n)`, onde `n` é o número de elementos atuais.

### Por que a análise de Pior Caso `O(n)` é pessimista?
Se olharmos apenas para o pior caso, diríamos que inserir na tabela é lento. Mas isso não reflete a realidade, pois o redimensionamento acontece raramente.

### Análise
Imagine que começamos com uma tabela de tamanho vazio e vamos inserindo elementos. O custo é 1 (tempo constante) para cada inserção.
Quando a tabela enche (em **N** elementos), pagamos um custo alto de **N** para copiar tudo.

No entanto, a próxima vez que precisarmos duplicar, a tabela terá **2N** de capacidade. Isso significa que teremos **N** novas inserções `O(1)` antes de precisarmos pagar o custo caro novamente.

Se distribuirmos o custo total do redimensionamento entre todas as inserções que ocorreram desde o último resize, percebemos que cada inserção "paga" apenas uma pequena fração constante extra.

**Conclusão Prática:**
Apesar de ocasionalmente termos uma operação lenta de `O(n)`, ela ocorre com frequência decrescente exponencialmente. Portanto, a **Complexidade Amortizada** da inserção na nossa Tabela Hash permanece `O(1)`. Isso valida a escolha da estrutura para o Censo, garantindo performance sustentável a longo prazo.
