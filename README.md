# O Arquivo de Rivendell

Este repositório contém a implementação do sistema "O Arquivo de Rivendell", focado em catalogar informações cruciais para a Sociedade do Anel.

### Módulo 1: O Censo da Terra-média (Cadastro de Entidades)

* **Técnica Escolhida:** **Tabela Hash** (com tratamento de colisão por encadeamento ou endereçamento aberto).
* **Justificativa:** O requisito principal e a **velocidade de consulta primordial** (ex: "Aragorn está registrado?"). Uma Tabela Hash oferece complexidade de tempo média de **$O(1)$** para inserção, busca e remoção. Isso é o mais rápido possível. Usaremos o nome da entidade (ex: "Aragorn") como chave.

---

### Módulo 2: O Palantír Linguístico (Análise de Idiomas)

* **Técnica Escolhida:** **Árvore Trie** (Árvore de Prefixos).
* **Justificativa:** O módulo exige armazenamento eficiente de strings e buscas rápidas por palavras exatas por prefixos (autocomplete). Este é o cenário de uso clássico e perfeito para uma Trie. A busca por prefixo tem complexidade de $O(k)$, onde $k$ é o comprimento do prefixo, sendo extremamente rápida.

---

### Módulo 3: O Almanaque das Eras (Crônicas Históricas)

* **Técnica Escolhida:** **Árvore B** (ou B+).
* **Justificativa:** Volume de dados **ultrapassa a capacidade da memória principal** e o módulo deve ser otimizado para operações eficientes de **disco**, minimizando o número de acessos. A Árvore B é a estrutura de dados padrão para índices de banco de dados e sistemas de arquivos exatamente por esse motivo. Sua estrutura (alta ramificação, baixa altura) minimiza as operações de I/O de disco. Além disso, ela mantém os dados ordenados, tornando as "consultas por intervalo" (ex: "anos 1500 a 1700") muito eficientes ($O(\log n + k)$).

---

### Módulo 4: A Bolsa do Aventureiro (Planejamento Logístico)

* **Técnica Escolhida:** **Algoritmo Guloso (Greedy)**.
* **Justificativa:** O problema é uma variação do "Problema da Mochila" (Knapsack Problem). Temos itens com `peso` e `utilidade` (valor) e uma `capacidade máxima`. Queremos maximizar a utilidade total.
    * Se pudermos pegar frações de itens, este é o "Problema da Mochila Fracionária", que é resolvido otimamente por um algoritmo guloso: calcular a razão `utilidade/peso` de cada item, ordenar os itens por essa razão (do maior para o menor) e pegar o máximo possível de cada item nessa ordem.
    * Se os itens são indivisíveis, um algoritmo guloso não garante a solução ótima (que exigiria programação dinâmica), mas é uma exigência do projeto usar um algoritmo guloso. Portanto, aplicamos a estratégia gulosa (ordenar por razão `utilidade/peso`) como a solução para este módulo.
