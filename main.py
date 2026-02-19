import sys

# importacao dos modulos e parsers
from rivendell_archive.modules.census_module import CensusModule
from rivendell_archive.modules.linguistic_module import LinguisticModule
from rivendell_archive.modules.almanac_module import AlmanacModule
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack, solveDynamicKnapsack, optimizeBarter, evaluateEncounter
from rivendell_archive.modules.map_module import MapModule
from rivendell_archive.modules.relationship_module import RelationshipModule
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
        
        # carregamento inicial de dados
        self._initializeData()
        
        # estado da mochila atual
        self.currentAdventureBag = []
        self.maxCapacity = 0.0

    def _initializeData(self):
        # carrega hash table
        self.census.loadData()
        
        namesToIndex = []
        # utiliza o novo metodo toList da hash table para pegar nomes
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
            print("1. Consultar Censo (Personagens/Locais)")
            print("2. Modulo Linguistico (Busca/Correcao)")
            print("3. Consultar Almanaque Historico (Eventos)")
            print("4. Planejar Logistica (Mochila/Escambo/Encontros)")
            print("5. Definir Objetivo da Sociedade")
            print("6. Analisar Relacoes (Personagens vs Historia)")
            print("7. Navegacao (Mapa/Dijkstra)")
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
            elif choice == '0':
                print("Encerrando o Sistema.")
                break
            else:
                print("Opção invalida.")

    def _runCensusMenu(self):
        name = input("Digite o nome do personagem para buscar: ")
        result = self.census.searchEntity(name)
        if result:
            print("\nREGISTRO ENCONTRADO")
            print(f"Nome: {result.get('name', 'N/A')}")
            print(f"Raca: {result.get('race', 'N/A')}")
            print(f"Reino: {result.get('realm', 'N/A')}")
            if 'wikiUrl' in result:
                print(f"Wiki: {result['wikiUrl']}")
        else:
            print("Personagem não encontrado no arquivo.")

    def _runLanguageMenu(self):
        print("1. Busca por Prefixo (Autocomplete)")
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
            print(f"\nEntrada: {word}")
            print(f"Sugestao: {suggestion} (Distancia: {dist})")

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
            print("Por favor digite apenas numeros para os anos.")

    def _runLogisticsMenu(self):
        print("\n--- Modulo de Logistica ---")
        print("1. Otimizacao Gulosa (Mochila Fracionaria)")
        print("2. Otimizacao Avancada (Mochila 0/1 - Prog. Dinamica)")
        print("3. Simular Escambo (Troca em Assentamento)")
        print("4. Encontro na Estrada (Avaliar novo item)")
        
        subChoice = input("Opcao: ")
        
        # so carrega se nao tivermos uma mochila carregada ou se o usuario quiser resetar
        if not self.currentAdventureBag and subChoice in ['1', '2']:
            print("Carregando lista padrao de suprimentos...")
            supplies = loadSupplies()
            if not supplies:
                return
        else:
            # usa a mochila atual para escambos e encontros
            supplies = self.currentAdventureBag
            if subChoice in ['1', '2']: # se escolher recriar, recarrega
                supplies = loadSupplies()

        try:
            if subChoice == '1':
                cap = float(input("Capacidade maxima: "))
                (util, weight, items) = solveGreedyKnapsack(supplies, cap)
                print(f"Mochila Gulosa montada. Util: {util}, Peso: {weight}")
                
            elif subChoice == '2':
                cap = float(input("Capacidade maxima: "))
                self.maxCapacity = cap # salva capacidade para usos futuros
                (util, weight, items) = solveDynamicKnapsack(supplies, cap)
                self.currentAdventureBag = items
                print(f"\nMochila Dinamica Otimizada! Utilidade: {util}, Peso: {weight}")
                for i in items: print(f"- {i['name']}")

            elif subChoice == '3':
                if not self.currentAdventureBag:
                    print("Mochila vazia. Crie uma mochila (Opcao 2) antes.")
                    return
                
                print(f"Simulando mercado em Moria...")
                merchantOffers = [
                    {"name": "Machado de Duas Maos", "weight": 4.5, "utility": 180},
                    {"name": "Escudo de Ferro", "weight": 3.0, "utility": 90}
                ]
                print("Ofertas: Machado (180 util), Escudo (90 util)")
                
                (util, weight, newItems) = optimizeBarter(self.currentAdventureBag, merchantOffers, self.maxCapacity)
                self.currentAdventureBag = newItems
                print(f"Troca realizada. Nova Utilidade: {util}")

            elif subChoice == '4':
                if not self.currentAdventureBag:
                    print("Mochila vazia. Crie uma mochila (Opcao 2) antes.")
                    return
                
                print("\nVoce encontrou um bau na estrada!")
                newItem = {"name": "Palantir Perdido", "weight": 3.0, "utility": 200}
                print(f"Item: {newItem['name']} (Peso: {newItem['weight']}, Util: {newItem['utility']})")
                
                (kept, discarded, newBag, util, weight) = evaluateEncounter(self.currentAdventureBag, newItem, self.maxCapacity)
                
                if kept:
                    print("DECISAO: Pegar o item!")
                    print("Para caber no peso, voce descartou: ", [d['name'] for d in discarded])
                    self.currentAdventureBag = newBag
                else:
                    print("DECISAO: Deixar o item (nao vale a pena o peso/utilidade).")
                
                print(f"Status Atual da Mochila -> Peso: {weight}/{self.maxCapacity}, Util: {util}")

        except ValueError:
            print("Erro de valor.")

    def _runObjectiveMenu(self):
        print("\nDEFINIR PROPOSITO")
        print("1. Destruir Anel (Rapidez)")
        print("2. Explorar (Novos locais)")
        try:
            c = int(input("Objetivo: "))
            self.map.setObjective(c)
        except: print("Erro")

    def _runRelationsMenu(self):
        self.relations.buildRelations(self.census, self.history)
        name = input("\nNome do personagem: ")
        if name:
            events = self.relations.getEntityRelations(name)
            for e in events: print(f"- {e}")

    def _runMapMenu(self):
        print("\n--- Navegacao (Dijkstra) ---")
        locs = ["Shire", "Bree", "Rivendell", "Moria", "Lothlorien", "Rohan", "Isengard", "Gondor", "Mordor", "Erebor"]
        print("Locais:", ", ".join(locs))
        
        start = input("Origem: ")
        end = input("Destino: ")
        
        (cost, path) = self.map.findShortestPath(start, end)
        
        if path:
            print(f"\nRota Calculada (Custo/Dias: {cost}):")
            print(" -> ".join(path))
        else:
            print("Nao foi possivel encontrar um caminho ou locais invalidos.")

if __name__ == "__main__":
    app = RivendellArchiveApp()
    app.run()
