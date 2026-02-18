from rivendell_archive.structures.graph import Graph

class RelationshipModule:
    def __init__(self):
        # grafo nao direcionado para relacionar entidades e eventos
        self.relationshipGraph = Graph(isDirected=False)

    def buildRelations(self, censusModule, almanacModule):
        # constroi o grafo de relacoes cruzando dados do censo e do almanaque
        print("Analisando pergaminhos para encontrar conexoes...")
        
        # obtem todas as entidades do censo
        # acessa os dados usando o metodo helper criado na hash table
        censusItems = censusModule.censusData.toList()
        
        # obtem todos os eventos do almanaque
        # acessa os dados usando o metodo helper criado na b-tree
        historyItems = almanacModule.chronicles.toList()
        
        connectionsCount = 0
        
        for year, description in historyItems:
            # cria um no para o evento
            eventNode = f"Event:{year}"
            self.relationshipGraph.addVertex(eventNode)
            
            # verifica se algum personagem conhecido esta na descricao do evento
            for charName, charData in censusItems:
                if not isinstance(charName, str):
                    continue
                    
                # verifica a presenca do nome no texto (busca simples)
                if charName.lower() in description.lower():
                    # adiciona o personagem como vertice se ainda nao existir
                    self.relationshipGraph.addVertex(charName)
                    
                    # cria a aresta (relacionamento)
                    self.relationshipGraph.addEdge(charName, eventNode, weight=1)
                    connectionsCount += 1
                    
        print(f"Grafo de Relacoes gerado: {connectionsCount} conexoes encontradas entre Personagens e Historia.")

    def getEntityRelations(self, entityName):
        # retorna eventos relacionados a uma entidade
        neighbors = self.relationshipGraph.getNeighbors(entityName)
        events = []
        for neighbor, weight in neighbors:
            if neighbor.startswith("Event:"):
                events.append(neighbor)
        return events
