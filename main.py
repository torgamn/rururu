import sys

# importacao dos modulos e parsers
from rivendell_archive.modules.census_module import CensusModule
from rivendell_archive.modules.linguistic_module import LinguisticModule
from rivendell_archive.modules.almanac_module import AlmanacModule
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack, solveDynamicKnapsack, optimizeBarter, evaluateEncounter
from rivendell_archive.modules.map_module import MapModule
from rivendell_archive.modules.relationship_module import RelationshipModule
from rivendell_archive.modules.confrontation_module import ConfrontationModule
from rivendell_archive.core.data_parser import loadSupplies

class RivendellArchiveApp:
    def __init__(self):
        print("Inicializando o arquivo de Rivendell...")
        
        # instanciando os modulos
        self.census = CensusModule()
        self.language = LinguisticModule()
        self.history = AlmanacModule()
        self.map = MapModule()
        self.relations = RelationshipModule()
        self.confrontation = ConfrontationModule()
        
        # carregamento inicial de dados
        self._initializeData()
        
        # estado da mochila e objetivo atual
        self.currentAdventureBag = []
        self.maxCapacity = 0.0
        self.currentObjective = None

    def _initializeData(self):
        # carrega hash table
        self.census.loadData()
        
        namesToIndex = []
        # utiliza o metodo tolist da hash table para pegar nomes
        censusItems = self.census.censusData.toList()
        for key, value in censusItems:
            if isinstance(key, str):
                namesToIndex.append(key)
        
        # adiciona algumas palavras elficas comuns tambem
        elvishWords = ["Mellon", "Moria", "Anduril", "Galadhrim", "Lothlorien", "Rivendell", "Mithril"]
        namesToIndex.extend(elvishWords)
        
        self.language.indexTextData(namesToIndex)
        
        # carrega (b-tree)
        self.history.loadEvents()
        
        # carrega o mapa
        self.map.loadMapData()

    def run(self):
        while True:
            print("\nO ARQUIVO DE RIVENDELL (MENU PRINCIPAL)")
            print("1. Consultar Censo (Personagens)")
            print("2. Modulo Linguistico (Busca/Correcao)")
            print("3. Consultar Almanaque Historico (Eventos)")
            print("4. Planejar Logistica (Mochila/Escambo/Encontros)")
            print("5. Definir Objetivo da Sociedade")
            print("6. Analisar Relacoes (Personagens e Historia)")
            print("7. Navegacao (Mapa/Dijkstra)")
            print("8. Simular Confronto")
            print("9. Iniciar Jornada")
            print("0. Sair")
            
            choice = input("Escolha uma opção: ")
            
            if choice == '1':
                self._runCensusMenu()
            elif choice == '2':
                self._runLanguageMenu()
            elif choice == '3':
                self._runHistoryMenu()
            elif choice == '4':
                self._runLogisticsMenu()
            elif choice == '5':
                self._runObjectiveMenu()
            elif choice == '6':
                self._runRelationsMenu()
            elif choice == '7':
                self._runMapMenu()
            elif choice == '8':
                self._runConfrontationTest()
            elif choice == '9':
                self._runIntegratedJourney()
            elif choice == '0':
                print("Encerrando o sistema.")
                break
            else:
                print("Opcao invalida.")

    def _runCensusMenu(self):
        name = input("Digite o nome do personagem para buscar: ")
        result = self.census.searchEntity(name)
        if result:
            print("\nREGISTRO ENCONTRADO")
            print(f"nome: {result.get('name', 'N/A')}")
            print(f"raca: {result.get('race', 'N/A')}")
            print(f"reino: {result.get('realm', 'N/A')}")
            if 'wikiUrl' in result:
                print(f"wiki: {result['wikiUrl']}")
        else:
            print("Personagem nao encontrado.")

    def _runLanguageMenu(self):
        print("\n1. Busca por Prefixo (Autocomplete)")
        print("2. Corretor Ortografico (Levenshtein)")
        sub = input("Opcao: ")
        
        if sub == '1':
            prefix = input("Digite o inicio da palavra: ")
            results = self.language.searchPrefix(prefix)
            if results:
                print(f"\nPalavras encontradas com '{prefix}':")
                for word in results:
                    print(f"- {word}")
            else:
                print("Nenhuma palavra correspondente encontrada.")
        elif sub == '2':
            word = input("Digite a palavra para verificar: ")
            (suggestion, dist) = self.language.checkSpelling(word)
            print(f"\nentrada: {word}")
            if dist == 0:
                print("A palavra ja esta correta no dicionario elfico.")
            else:
                print(f"Sugestao: {suggestion} (distancia de correcao: {dist})")

    def _runHistoryMenu(self):
        print("1. Buscar ano especifico")
        print("2. Buscar intervalo de tempo")
        subChoice = input("Opção: ")
        
        try:
            if subChoice == '1':
                year = int(input("Digite o ano: "))
                event = self.history.findEventByYear(year)
                if event:
                    print(f"\nEvento em {year}: {event}")
                else:
                    print("Nenhum evento registrado neste ano.")
            elif subChoice == '2':
                start = int(input("Ano inicial: "))
                end = int(input("Ano final: "))
                results = self.history.findEventsInPeriod(start, end)
                if results:
                    print(f"\nEventos entre {start} e {end}:")
                    for year, event in results:
                        print(f"[{year}] {event}")
                else:
                    print("Nenhum evento encontrado neste periodo.")
        except ValueError:
            print("Digite apenas numeros para os anos.")

    def _runLogisticsMenu(self):
        print("\nModulo de Logistica")
        print("1. Otimizacao Gulosa (Mochila Fracionaria)")
        print("2. Otimizacao Avancada (Mochila 0/1 - Prog. Dinamica)")
        print("3. Simular Escambo (Troca em Assentamento)")
        print("4. Encontro na Estrada (Avaliar novo item)")
        
        subChoice = input("opcao: ")
        
        if not self.currentAdventureBag and subChoice in ['1', '2']:
            print("Carregando lista padrao de suprimentos...")
            supplies = loadSupplies()
            if not supplies:
                return
        else:
            supplies = self.currentAdventureBag
            if subChoice in ['1', '2']: 
                supplies = loadSupplies()

        try:
            if subChoice == '1':
                cap = float(input("Capacidade maxima: "))
                self.maxCapacity = cap 
                (util, weight, items) = solveGreedyKnapsack(supplies, cap)
                self.currentAdventureBag = items # agora a mochila gulosa alimenta o estado
                print(f"Mochila gulosa montada. util: {util}, peso: {weight}")
                for i in items: print(f"- {i['name']}")
                
            elif subChoice == '2':
                cap = float(input("Capacidade maxima: "))
                self.maxCapacity = cap 
                (util, weight, items) = solveDynamicKnapsack(supplies, cap)
                self.currentAdventureBag = items
                print(f"\nMochila dinamica otimizada! utilidade: {util}, peso: {weight}")
                for i in items: print(f"- {i['name']}")

            elif subChoice == '3':
                if not self.currentAdventureBag:
                    print("Mochila vazia. crie uma mochila (opcao 1 ou 2) antes.")
                    return
                
                print(f"Simulando mercado:")
                merchantOffers = [
                    {"name": "Machado de Duas Maos", "weight": 4.5, "utility": 180},
                    {"name": "Escudo de Ferro", "weight": 3.0, "utility": 90}
                ]
                print("Ofertas: machado (180 util), escudo (90 util)")
                
                (util, weight, newItems) = optimizeBarter(self.currentAdventureBag, merchantOffers, self.maxCapacity)
                self.currentAdventureBag = newItems
                print(f"Troca realizada. nova utilidade: {util}")

            elif subChoice == '4':
                if not self.currentAdventureBag:
                    print("Mochila vazia. crie uma mochila (opcao 1 ou 2) antes.")
                    return
                
                print("\nVoce encontrou um bau na estrada!")
                newItem = {"name": "Palantir Perdido", "weight": 3.0, "utility": 200}
                print(f"item: {newItem['name']} (peso: {newItem['weight']}, util: {newItem['utility']})")
                
                (kept, discarded, newBag, util, weight) = evaluateEncounter(self.currentAdventureBag, newItem, self.maxCapacity)
                
                if kept:
                    print("Decisao: pegar o item!")
                    print("Para caber no peso, voce descartou: ", [d['name'] for d in discarded])
                    self.currentAdventureBag = newBag
                else:
                    print("Decisao: deixar o item (nao vale a pena o peso/utilidade).")
                
                print(f"Status atual da mochila -> peso: {weight}/{self.maxCapacity}, util: {util}")

        except ValueError:
            print("Erro de valor.")

    def _runObjectiveMenu(self):
        print("\nDEFINIR PROPOSITO DA SOCIEDADE")
        print("1. Destruir o Anel (Rapidez)")
        print("2. Explorar a Terra Media (Novos caminhos)")
        print("3. Visitar Locais Historicos (Conhecimento)")
        print("4. Combate (Gloria e XP)")
        try:
            c = int(input("Escolha o objetivo (1-4): "))
            self.map.setObjective(c)
            self.currentObjective = c # salva o objetivo escolhido no estado
            print("\n[!] Proposito redefinido com sucesso.")
            
            if c == 1:
                print("-> Atributos alterados: pesos do grafo agora usam estritamente o fator tempo/distancia. locais de alto risco sao ignorados pelo dijkstra se a rota for rapida.")
            elif c == 2:
                print("-> Atributos alterados: rotas para locais nao descobertos ou remotos receberam reducao de custo nas arestas para incentivar a exploracao.")
            elif c == 3:
                print("-> Atributos alterados: a otimizacao de rota sera baseada na passagem por locais com a maior contagem de eventos historicos.")
            elif c == 4:
                print("-> Atributos alterados: caminhos onde batalhas ocorreram tem prioridade, recebendo descontos artificiais na distancia para atrair a rota.")
            else:
                print("-> Objetivo desconhecido selecionado.")
                self.currentObjective = None # reseta se inserido invalido
        except ValueError:
            print("Erro: Insira apenas numeros validos.")

    def _runRelationsMenu(self):
        self.relations.buildRelations(self.census, self.history)
        name = input("\nNome do personagem: ")
        if name:
            events = self.relations.getEntityRelations(name)
            for e in events: print(f"- {e}")

    def _runMapMenu(self):
        print("\nNavegacao (Dijkstra)")
        locs = list(self.map.locationMetadata.keys())
        print("Locais:", ", ".join(locs))
        
        start = input("Origem: ")
        end = input("Destino: ")
        
        (cost, path) = self.map.findShortestPath(start, end)
        
        if path:
            print(f"\nRota calculada (custo/dias: {cost}):")
            print(" -> ".join(path))
        else:
            print("Não foi possivel encontrar um caminho ou locais invalidos.")

    def _runConfrontationTest(self):
        print("\nSimulador de Confrontos")
        if not self.currentAdventureBag:
            print("Aviso: mochila vazia. o poder de combate sera baixo.")
            print("Recomendado montar a mochila no menu 4 antes.")
            
        locs = list(self.map.locationMetadata.keys())
        print("Locais disponiveis:", ", ".join(locs))
        
        targetLoc = input("Local de destino para analise: ")
        
        if targetLoc not in self.map.locationMetadata:
            print("Local invalido.")
            return

        prob = self.confrontation.calculateConfrontationProbability(targetLoc, self.map, self.history)
        triggered = self.confrontation.checkConfrontationTrigger(prob)
        
        if triggered:
            print("Inimigos a vista! preparar para o combate!")
            (victory, penalty, newBag) = self.confrontation.resolveConfrontation(self.currentAdventureBag, targetLoc, self.map)
            self.currentAdventureBag = newBag 
            print(f"Penalidade de tempo aplicada: +{penalty*100}%")
        else:
            print("Caminho seguro. nenhum confronto ocorreu.")

    def _runIntegratedJourney(self):
        print("\nA JORNADA")
        
        # validacao 1: objetivo definido
        if not self.currentObjective:
            print("A sociedade precisa de um proposito! defina o objetivo (menu 5) primeiro.")
            return
            
        # validacao 2: mochila montada
        if not self.currentAdventureBag:
            print("A sociedade esta viajando sem suprimentos! prepare a mochila (menu 4) primeiro.")
            return
            
        locs = list(self.map.locationMetadata.keys())
        print("Locais possiveis:", ", ".join(locs))
        
        start = input("Local de partida: ")
        end = input("Local de destino: ")
        
        (cost, path) = self.map.findShortestPath(start, end)
        
        if not path:
            print("Não há rotas conhecidas para este destino.")
            return
            
        print(f"\nPLANEJAMENTO DE ROTA")
        print(f"Caminho tracado: {' -> '.join(path)}")
        print(f"Estimativa otimista de viagem: {cost} dias.")
        
        totalDays = 0.0
        
        for i in range(len(path) - 1):
            currentLoc = path[i]
            nextLoc = path[i+1]
            
            print(f"\nViajando de {currentLoc} para {nextLoc}...")
            
            baseTime = 1.0 
            for neighbor, weight in self.map.middleEarthMap.getNeighbors(currentLoc):
                if neighbor == nextLoc:
                    baseTime = weight
                    break
            
            prob = self.confrontation.calculateConfrontationProbability(nextLoc, self.map, self.history)
            triggered = self.confrontation.checkConfrontationTrigger(prob)
            
            if triggered:
                print(f"EMBOSCADA A CAMINHO DE {nextLoc.upper()}")
                (victory, penaltyPercent, newBag) = self.confrontation.resolveConfrontation(self.currentAdventureBag, nextLoc, self.map)
                self.currentAdventureBag = newBag
                
                penaltyDays = baseTime * penaltyPercent
                totalDays += (baseTime + penaltyDays)
                print(f"[x] Dias decorridos no trecho: {baseTime} (base) + {penaltyDays:.1f} (penalidade/atrasos) = {baseTime + penaltyDays:.1f} dias")
            else:
                print(f"[*] Os caminhos estao quietos. viagem sem interrupcoes.")
                totalDays += baseTime
                print(f"[x] Dias decorridos no trecho: {baseTime} dias")
                
            currentUtil = sum(item['utility'] for item in self.currentAdventureBag)
            print(f"[*] Status da sociedade: {len(self.currentAdventureBag)} itens restantes (utilidade total: {currentUtil})")
            
        print(f"\nFIM DA JORNADA")
        print(f"Destino alcancado: {end}")
        print(f"Tempo total real gasto na jornada: {totalDays:.1f} dias.")

if __name__ == "__main__":
    app = RivendellArchiveApp()
    app.run()
