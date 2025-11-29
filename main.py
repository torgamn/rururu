import sys

# importacao dos modulos e parsers
from rivendell_archive.modules.census_module import CensusModule
from rivendell_archive.modules.linguistic_module import LinguisticModule
from rivendell_archive.modules.almanac_module import AlmanacModule
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack
from rivendell_archive.core.data_parser import loadSupplies

class RivendellArchiveApp:
    def __init__(self):
        print("Inicializando o arquivo de Rivendell...")
        
        # instanciando os modulos
        self.census = CensusModule()
        self.language = LinguisticModule()
        self.history = AlmanacModule()
        
        # carregamento inicial de dados
        self._initializeData()

    def _initializeData(self):
        # carrega hash table
        self.census.loadData()
        
        namesToIndex = []
        for bucket in self.census.censusData.table:
            for key, value in bucket:
                if isinstance(key, str):
                    namesToIndex.append(key)
        
        # adiciona algumas palavras elficas comuns tambem
        elvishWords = ["Mellon", "Moria", "Anduril", "Galadhrim", "Lothlorien", "Rivendell", "Mithril"]
        namesToIndex.extend(elvishWords)
        
        self.language.indexTextData(namesToIndex)
        
        # carrega (b-tree)
        self.history.loadEvents()

    def run(self):
        while True:
            print("\nO ARQUIVO DE RIVENDELL (MENU PRINCIPAL)")
            print("1. Consultar Censo (Personagens/Locais)")
            print("2. Decifrar Inscricao (Autocomplete)")
            print("3. Consultar Almanaque Historico (Eventos)")
            print("4. Planejar Logistica (Mochila Gulosa)")
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
        print("Carregando suprimentos...")
        supplies = loadSupplies() # carrega do csv
        
        if not supplies:
            print("Erro ao carregar arquivo de suprimentos.")
            return

        try:
            capacity = float(input("Digite a capacidade maxima da mochila (peso): "))
            (totalUtil, totalWeight, items) = solveGreedyKnapsack(supplies, capacity)
            
            print("\nPLANO LOGISTICO")
            print(f"Capacidade maxima: {capacity}")
            print(f"Peso Total ocupado: {totalWeight:.2f}")
            print(f"Utilidade total: {totalUtil:.2f}")
            print("Itens selecionados:")
            for name, fraction in items:
                print(f"- {name}")
                
        except ValueError:
            print("Erro: valor invalido para peso.")

if __name__ == "__main__":
    app = RivendellArchiveApp()
    app.run()
