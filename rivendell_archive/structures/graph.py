class Graph:
    # estrutura de grafo ponderado e direcionado usando lista de adjacencia
    def __init__(self, isDirected=True):
        self.adjacencyList = {}
        self.isDirected = isDirected
        self.vertices = set()

    def addVertex(self, vertex):
        # adiciona um vertice ao grafo
        if vertex not in self.adjacencyList:
            self.adjacencyList[vertex] = []
            self.vertices.add(vertex)

    def addEdge(self, source, destination, weight=1.0):
        # adiciona uma aresta (com peso)
        if source not in self.adjacencyList:
            self.addVertex(source)
        if destination not in self.adjacencyList:
            self.addVertex(destination)
        
        # adiciona tupla (destino, peso) na lista do vertice de origem
        self.adjacencyList[source].append((destination, weight))
        
        # se nao for direcionado, adiciona o inverso
        if not self.isDirected:
            self.adjacencyList[destination].append((source, weight))

    def getNeighbors(self, vertex):
        # retorna lista de vizinhos (destino, peso)
        return self.adjacencyList.get(vertex, [])

    def getVertices(self):
        # retorna lista de vertices
        return list(self.vertices)
