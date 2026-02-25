from rivendell_archive.structures.graph import Graph

class RelationshipModule:
    def __init__(self):
        # grafo nao direcionado para relacionar entidades e eventos
        self.relationshipGraph = Graph(isDirected=False)

    def buildRelations(self, censusModule, almanacModule):
        # constroi o grafo de relacoes cruzando dados do censo e do almanaque
        print("Analisando pergaminhos para encontrar conexoes...")
        
        # obtem todas as entidades do censo
        censusItems = censusModule.censusData.toList()
        
        # obtem todos os eventos do almanaque
        historyItems = almanacModule.chronicles.toList()
        
        connectionsCount = 0
        
        for year, description in historyItems:
            # cria um no para o evento
            eventNode = f"Evento: {year}"
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
                    
        print(f"Grafo de relacoes gerado: {connectionsCount} conexoes encontradas entre personagens e historia.")

    def getEntityRelations(self, entityName):
        # retorna eventos relacionados a uma entidade
        neighbors = self.relationshipGraph.getNeighbors(entityName)
        events = []
        seen = set() # evitar duplicatas de eventos
        
        for neighbor, weight in neighbors:
            if neighbor.startswith("Event:"):
                # deduplicacao
                if neighbor not in seen:
                    events.append(neighbor)
                    seen.add(neighbor)
                    
        return events
