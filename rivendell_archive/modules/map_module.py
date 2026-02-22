from rivendell_archive.structures.graph import Graph
import heapq # fila de prioridade para o dijkstra

class MapModule:
    def __init__(self):
        # grafo ponderado e direcionado para o mapa da terra-media
        self.middleEarthMap = Graph(isDirected=True)
        self.currentObjective = None
        self.objectives = {
            1: {"name": "Destruir o Um Anel", "focus": "speed"},
            2: {"name": "Explorar a Terra Media", "focus": "exploration"},
            3: {"name": "Eventos Historicos", "focus": "history"},
            4: {"name": "Enfraquecer o Mal", "focus": "combat"}
        }
        
        # metadados dos locais para o sistema de confronto
        self.locationMetadata = {
            "Shire": {"malice": 0.0, "difficulty": 10},
            "Bree": {"malice": 0.1, "difficulty": 15},
            "Rivendell": {"malice": 0.05, "difficulty": 20},
            "Moria": {"malice": 0.6, "difficulty": 50},
            "Lothlorien": {"malice": 0.0, "difficulty": 25},
            "Rohan": {"malice": 0.3, "difficulty": 35},
            "Isengard": {"malice": 0.7, "difficulty": 55},
            "Gondor": {"malice": 0.4, "difficulty": 40},
            "Mordor": {"malice": 0.95, "difficulty": 80},
            "Erebor": {"malice": 0.5, "difficulty": 45}
        }

    def setObjective(self, objectiveId):
        # define o objetivo da sociedade que afetara os pesos das arestas
        if objectiveId in self.objectives:
            self.currentObjective = self.objectives[objectiveId]
            print(f"Objetivo definido: {self.currentObjective['name']}")
            print(f"Foco estrategico: {self.currentObjective['focus']}")
        else:
            print("Objetivo invalido.")

    def loadMapData(self):
        # carrega os dados geograficos (locais e rotas)
        print("Cartografia: desenhando o mapa da Terra-Media...")
        
        # vertices (locais)
        locations = list(self.locationMetadata.keys())
        
        for loc in locations:
            self.middleEarthMap.addVertex(loc)

        # arestas (rotas) - formato: (origem, destino, tempo_base_dias)
        routes = [
            ("Shire", "Bree", 4),
            ("Bree", "Rivendell", 7),
            ("Rivendell", "Moria", 5),
            ("Rivendell", "Rohan", 15), # rota longa alternativa
            ("Moria", "Lothlorien", 3),
            ("Lothlorien", "Rohan", 4),
            ("Rohan", "Isengard", 2),
            ("Rohan", "Gondor", 5),
            ("Isengard", "Rohan", 2), # volta
            ("Gondor", "Mordor", 4),
            ("Lothlorien", "Erebor", 10),
            ("Erebor", "Moria", 12)
        ]
        
        countRoutes = 0
        for source, dest, weight in routes:
            # adiciona a aresta no grafo
            self.middleEarthMap.addEdge(source, dest, weight)
            # assumindo que as rotas sao de mao dupla para simplificar a navegacao basica
            self.middleEarthMap.addEdge(dest, source, weight)
            countRoutes += 1
            
        print(f"Mapa carregado: {len(locations)} locais e {countRoutes * 2} conexoes mapeadas.")

    def findShortestPath(self, startNode, endNode):
        # milestone 2/6: algoritmo de dijkstra para menor caminho
        print(f"Calculando rota de {startNode} para {endNode}...")
        
        # fila de prioridade armazena tuplas (custo, vertice_atual, caminho_percorrido)
        queue = [(0, startNode, [])]
        visited = set()
        
        while queue:
            (cost, current, path) = heapq.heappop(queue)
            
            # se ja visitamos com um custo menor, ignora
            if current in visited:
                continue
            
            visited.add(current)
            path = path + [current]
            
            # chegou ao destino
            if current == endNode:
                return (cost, path)
            
            # explora vizinhos
            neighbors = self.middleEarthMap.getNeighbors(current)
            if neighbors:
                for neighbor, weight in neighbors:
                    if neighbor not in visited:
                        # aqui poderiamos ajustar o peso baseado no objetivo (penalidade)
                        # por enquanto usamos o peso direto (tempo)
                        heapq.heappush(queue, (cost + weight, neighbor, path))
                        
        return (float('inf'), []) # caminho nao encontrado

    def getWeightedEdge(self, weight, edgeAttributes=None):
        # metodo placeholder para calcular peso baseado no objetivo
        return weight
        
    def getLocationMetadata(self, locationName):
        # retorna metadados (malicia, dificuldade) para o modulo de confronto
        return self.locationMetadata.get(locationName, {"malice": 0.5, "difficulty": 30})
