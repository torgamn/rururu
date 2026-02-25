# Relatório Técnico: O Arquivo de Rivendell Parte 2

A implementação busca realizar todas as exigências determinadas pelo projeto. Todas as estruturas de dados e algoritmos obrigatórios (Programação Dinâmica para Distância de Edição e Mochila, Dijkstra para grafos, etc.)

---

## Decisões de Design e Implementação por Módulo

### 1. Conexão de Entidades e Eventos (Módulo 3.1)
O objetivo principal deste módulo é associar os personagens do universo aos eventos históricos em que estiveram presentes no Almanaque.
* **Estrutura Escolhida:** Grafo não direcionado (`RelationshipModule`).
* **Justificação:** Os grafos são ótimas estruturas para mapear relações em rede. Optou-se por aplicar arestas não direcionadas visto que a conexão entre um evento e um personagem é mútua e não exige ordem cronológica ou de destino na sua leitura. A pesquisa na base de dados cruza as entidades do Censo com as descrições no Almanaque para criar as arestas em tempo de execução.

### 2. Palantír Linguístico e Corretor Ortográfico (Módulo 2)
Na interpretação de dialetos antigos, inscrições parcialmente ilegíveis requerem tolerância aos erros para devolver o termo mais provável.
* **Algoritmo Escolhido:** Distância de Edição de Levenshtein (via Programação Dinâmica) combinada com a estrutura `Trie` (`LinguisticModule`).
* **Justificação:** A Programação Dinâmica garante uma resposta matematicamente exata para encontrar o menor número de modificações (inserções, remoções, substituições) entre duas palavras, otimizando o cálculo computacional. O uso sincronizado com a árvore `Trie` assegura que a sugestão corretiva vai sempre coincidir com um termo real indexado no dicionário élfico.

### 3. Logística, Escambo e Encontros (Módulos 4 e 5)
A Sociedade precisa de otimizar constantemente a sua mochila, já que o peso afeta a velocidade de viagem e o descarte de itens pode causar o fracasso em confrontos.
* **Algoritmo Escolhido:** Problema da Mochila (Knapsack Problem) resolvido com Programação Dinâmica 0/1 (`LogisticsModule`).
* **Justificação:** Ao contrário de opções gulosas (que falham na otimização global para itens indivisíveis), a abordagem por Programação Dinâmica assegura a extração máxima de utilidade respeitando de forma estrita o limite de capacidade de peso da mochila. Este algoritmo é reaproveitado sempre que surgem novos itens na estrada ou oportunidades de escambo em assentamentos como Moria, recalculando a utilidade máxima para o novo "pool" de recursos.

### 4. Navegação Otimizada no Mapa (Módulo 6)
O planeamento da viagem dita o caminho percorrido consoante o grande propósito da missão, afetando as escolhas de rota em cada intersecção.
* **Estrutura e Algoritmo Escolhidos:** Grafo Ponderado Direcionado aliado ao Algoritmo de Dijkstra (`MapModule`).
* **Justificação:** Sendo as distâncias de viagem constantes e as arestas possuidoras de pesos positivos (dias de percurso ou custo ajustado), o Algoritmo de Dijkstra é a escolha ideal e mais eficiente para encontrar o caminho ótimo entre dois vértices (ex: Rivendell a Lórien). O uso de um grafo ponderado permite também alterar os "pesos" dinamicamente com base no objetivo inicial da Sociedade (velocidade, exploração, história ou combate).

### 5. Mecânica e Risco de Confronto (Módulo 7)
Os perigos espreitam consoante a malícia da região e o seu histórico sombrio, consumindo tempo e recursos do grupo em caso de emboscada.
* **Implementação Lógica:** Cálculo de Probabilidade de Confronto (Pc) seguido por Simulação de Combate Baseado em Poder (`ConfrontationModule`).
* **Justificação:** A decisão de design focou-se na simulação tática e na integração com os módulos anteriores em vez de um minijogo complexo de batalha. O módulo lê os "Eventos Negativos" diretamente da árvore do Almanaque (Módulo 3) e o "Nível de Malícia" do Mapa (Módulo 6). O sucesso no confronto penaliza o grupo com perda de tempo e itens (1 se vitória, 3 dos melhores se derrota/retirada), forçando o Módulo de Logística (Módulo 4) a re-otimizar o inventário para as rotas seguintes. Esta abordagem circular valida todo o ecossistema do Arquivo de Rivendell.
