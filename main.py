import sys

# importacao dos modulos e parsers
from rivendell_archive.modules.census_module import CensusModule
from rivendell_archive.modules.linguistic_module import LinguisticModule
from rivendell_archive.modules.almanac_module import AlmanacModule
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack
from rivendell_archive.core.data_parser import loadSupplies

class RivendellArchiveApp:
    def __init__(self):
        print("inicializando o arquivo de rivendell...")
        
        # instanciando os modulos
        self.census = CensusModule()
        self.language = LinguisticModule()
        self.history = AlmanacModule()
        
        # carregamento inicial de dados
        self._initializeData()

    def _initializeData(self):
        # carrega hash table
        self.census.loadData()
        
        # popula o modulo de linguagem (trie) com nomes do censo
        # extrai todos os nomes da tabela hash para usar como base linguistica
        # acessamos a tabela interna apenas para popular a trie
        namesToIndex = []
        for bucket in self.census.censusData.table:
            for key, value in bucket:
                if isinstance(key, str):
                    namesToIndex.append(key)
        
        # adiciona algumas palavras elficas comuns tambem
        elvishWords = ["Mellon", "Moria", "Anduril", "Galadhrim", "Lothlorien", "Rivendell", "Mithril"]
        namesToIndex.extend(elvishWords)
        
        self.language.indexTextData(namesToIndex)
        
        # carrega historia (b-tree)
        self.history.loadDefaultEvents()

    def run(self):
        while True:
            print("\nO ARQUIVO DE RIVENDELL (MENU PRINCIPAL)")
            print("1. Consultar Censo (Personagens/Locais)")
            print("2. Decifrar Inscricao (Autocomplete)")
            print("3. Consultar Almanaque Historico (Eventos)")
            print("4. Planejar Logistica (Mochila Gulosa)")
            print("0. Sair")
            
            choice = input("escolha uma opcao: ")
            
            if choice == '1':
                self._runCensusMenu()
            elif choice == '2':
                self._runLanguageMenu()
            elif choice == '3':
                self._runHistoryMenu()
            elif choice == '4':
                self._runLogisticsMenu()
            elif choice == '0':
                print("encerrando o sistema.")
                break
            else:
                print("opcao invalida.")

    def _runCensusMenu(self):
        name = input("digite o nome do personagem para buscar: ")
        result = self.census.searchEntity(name)
        if result:
            print("\nREGISTRO ENCONTRADO")
            print(f"Nome: {result.get('name', 'N/A')}")
            print(f"Raca: {result.get('race', 'N/A')}")
            print(f"Reino: {result.get('realm', 'N/A')}")
            if 'wikiUrl' in result:
                print(f"Wiki: {result['wikiUrl']}")
        else:
            print("personagem nao encontrado no arquivo.")

    def _runLanguageMenu(self):
        prefix = input("digite o inicio da palavra (prefixo): ")
        results = self.language.searchPrefix(prefix)
        if results:
            print(f"\npalavras encontradas com '{prefix}':")
            for word in results:
                print(f"- {word}")
        else:
            print("nenhuma palavra correspondente encontrada.")

    def _runHistoryMenu(self):
        print("1. Buscar ano especifico")
        print("2. Buscar intervalo de tempo")
        subChoice = input("opcao: ")
        
        try:
            if subChoice == '1':
                year = int(input("digite o ano: "))
                event = self.history.findEventByYear(year)
                if event:
                    print(f"\nevento em {year}: {event}")
                else:
                    print("nenhum evento registrado neste ano.")
            elif subChoice == '2':
                start = int(input("ano inicial: "))
                end = int(input("ano final: "))
                results = self.history.findEventsInPeriod(start, end)
                if results:
                    print(f"\neventos entre {start} e {end}:")
                    for year, event in results:
                        print(f"[{year}] {event}")
                else:
                    print("nenhum evento encontrado neste periodo.")
        except ValueError:
            print("por favor digite apenas numeros para os anos.")

    def _runLogisticsMenu(self):
        print("carregando suprimentos...")
        supplies = loadSupplies() # carrega do csv
        
        if not supplies:
            print("erro ao carregar arquivo de suprimentos.")
            return

        try:
            capacity = float(input("digite a capacidade maxima da mochila (peso): "))
            (totalUtil, totalWeight, items) = solveGreedyKnapsack(supplies, capacity)
            
            print("\nPLANO LOGISTICO")
            print(f"capacidade maxima: {capacity}")
            print(f"peso Total ocupado: {totalWeight:.2f}")
            print(f"utilidade total: {totalUtil:.2f}")
            print("itens selecionados:")
            for name, fraction in items:
                print(f"- {name}")
                
        except ValueError:
            print("erro: valor invalido para peso.")

if __name__ == "__main__":
    app = RivendellArchiveApp()
    app.run()
