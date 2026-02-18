from rivendell_archive.structures.graph import Graph

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
        # como nao temos um arquivo de rotas, vamos simular o carregamento 
        # conectando locais classicos da terra-media com tempos base de viagem
        
        print("Cartografia: desenhando o mapa da Terra-Media...")
        
        # vertices (locais)
        locations = [
            "Shire", "Bree", "Rivendell", "Moria", "Lothlorien", 
            "Rohan", "Isengard", "Gondor", "Mordor", "Erebor"
        ]
        
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
            # o peso final pode variar futuramente com base no objetivo
            self.middleEarthMap.addEdge(source, dest, weight)
            
            # assumindo que as rotas sao de mao dupla para simplificar a navegacao basica
            # mas mantendo o grafo direcionado internamente
            self.middleEarthMap.addEdge(dest, source, weight)
            countRoutes += 1
            
        print(f"Mapa carregado: {len(locations)} locais e {countRoutes * 2} conexoes mapeadas.")

    def getWeightedEdge(self, weight, edgeAttributes=None):
        # metodo placeholder para calcular peso baseado no objetivo (milestone 2)
        # por enquanto retorna o peso base (tempo)
        return weight
