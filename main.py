import sys

# importacao dos modulos e parsers
from rivendell_archive.modules.census_module import CensusModule
from rivendell_archive.modules.linguistic_module import LinguisticModule
from rivendell_archive.modules.almanac_module import AlmanacModule
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack, solveDynamicKnapsack, optimizeBarter
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
        
        # estado da mochila atual (para o modulo de escambo)
        self.currentAdventureBag = [] 

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
            print("2. Decifrar Inscricao (Autocomplete)")
            print("3. Consultar Almanaque Historico (Eventos)")
            print("4. Planejar Logistica (Mochila)")
            print("5. Definir Objetivo da Sociedade")
            print("6. Analisar Relacoes (Personagens vs Historia)")
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
        prefix = input("Digite o inicio da palavra (prefixo): ")
        results = self.language.searchPrefix(prefix)
        if results:
            print(f"\nPalavras encontradas com '{prefix}':")
            for word in results:
                print(f"- {word}")
        else:
            print("Nenhuma palavra correspondente encontrada.")

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
        print("3. Simular Escambo em Assentamento")
        
        subChoice = input("Opcao: ")
        
        print("Carregando suprimentos...")
        supplies = loadSupplies() # carrega do csv
        
        if not supplies:
            print("Erro ao carregar arquivo de suprimentos.")
            return

        try:
            if subChoice == '1':
                # metodo guloso antigo
                capacity = float(input("Digite a capacidade maxima da mochila (peso): "))
                (totalUtil, totalWeight, items) = solveGreedyKnapsack(supplies, capacity)
                
                print("\nPLANO LOGISTICO (GULOSO)")
                print(f"Capacidade maxima: {capacity}")
                print(f"Peso Total ocupado: {totalWeight:.2f}")
                print(f"Utilidade total: {totalUtil:.2f}")
                print("Itens selecionados:")
                for name, fraction in items:
                    print(f"- {name} (Qtd: {fraction})")
                    
            elif subChoice == '2':
                # metodo programacao dinamica
                capacity = float(input("Digite a capacidade maxima da mochila (peso): "))
                (totalUtil, totalWeight, items) = solveDynamicKnapsack(supplies, capacity)
                
                # atualiza a mochila atual da aplicacao
                self.currentAdventureBag = items
                
                print("\nPLANO LOGISTICO (DINAMICO 0/1)")
                print(f"Capacidade maxima: {capacity}")
                print(f"Peso Total ocupado: {totalWeight:.2f}")
                print(f"Utilidade total: {totalUtil:.2f}")
                print("Itens selecionados:")
                for item in items:
                    print(f"- {item['name']} (Peso: {item['weight']}, Util: {item['utility']})")

            elif subChoice == '3':
                # simulacao de escambo
                if not self.currentAdventureBag:
                    print("Sua mochila esta vazia. Execute a opcao 2 primeiro para enche-la.")
                    return
                
                print(f"\nVoce entra em um mercado anao.")
                print(f"Itens na sua mochila: {len(self.currentAdventureBag)}")
                
                # itens disponiveis no mercador (mock)
                merchantOffers = [
                    {"name": "Machado de Duas Maos", "weight": 4.5, "utility": 180},
                    {"name": "Escudo de Ferro", "weight": 3.0, "utility": 90},
                    {"name": "Barril de Cerveja", "weight": 5.0, "utility": 60}, # baixa utilidade/peso
                    {"name": "Gema de Arkenstone (Replica)", "weight": 0.5, "utility": 120}
                ]
                
                print("O mercador oferece:")
                for mItem in merchantOffers:
                    print(f"- {mItem['name']} (P: {mItem['weight']}, U: {mItem['utility']})")
                
                capacity = float(input("Confirme a capacidade maxima para o transporte pos-troca: "))
                
                (newUtil, newWeight, newItems) = optimizeBarter(self.currentAdventureBag, merchantOffers, capacity)
                
                print("\n--- RESULTADO DA TROCA OTIMIZADA ---")
                print(f"Nova Utilidade Total: {newUtil} (Anterior: {sum(i['utility'] for i in self.currentAdventureBag)})")
                print("Nova composicao da mochila:")
                for item in newItems:
                    # verifica se o item veio do mercador ou ja era nosso
                    origin = "Mochila"
                    for m in merchantOffers:
                        if m['name'] == item['name']:
                            origin = "MERCADO"
                            break
                    print(f"- [{origin}] {item['name']}")
                
                # atualiza a mochila
                self.currentAdventureBag = newItems

        except ValueError:
            print("Erro: valor invalido.")

    def _runObjectiveMenu(self):
        print("\nDEFINIR PROPOSITO DA JORNADA")
        print("1. Destruir o Um Anel (Minimizar tempo/risco)")
        print("2. Explorar a Terra Media (Maximizar novos locais)")
        print("3. Visitar Locais Historicos (Foco em conhecimento)")
        print("4. Enfraquecer o Mal (Buscar combate)")
        
        try:
            choice = int(input("Escolha o objetivo prioritario (1-4): "))
            self.map.setObjective(choice)
        except ValueError:
            print("Entrada invalida.")

    def _runRelationsMenu(self):
        # gera ou atualiza as relacoes
        self.relations.buildRelations(self.census, self.history)
        
        searchName = input("\nDigite o nome de um personagem para ver sua historia (ou ENTER para voltar): ")
        if searchName:
            events = self.relations.getEntityRelations(searchName)
            if events:
                print(f"Eventos relacionados a {searchName}:")
                for evt in events:
                    print(f"- {evt}")
            else:
                print("Nenhum evento historico correlacionado encontrado.")

if __name__ == "__main__":
    app = RivendellArchiveApp()
    app.run()
