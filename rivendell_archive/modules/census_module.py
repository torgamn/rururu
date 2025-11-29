from rivendell_archive.structures.hash_table import HashTable
from rivendell_archive.core.api_client import getCharacters

class CensusModule:
    def __init__(self):
        # inicializa a tabela hash
        self.censusData = HashTable(initialCapacity=100)
        self.isLoaded = False

    def loadData(self):
        # carrega dados da api na tabela
        print("Buscando dados do censo na api...")
        characters = getCharacters()
        
        if characters:
            count = 0
            for char in characters:
                name = char.get('name')
                if name:
                    # usa o nome da entidade como chave para busca rapida
                    self.censusData.insert(name, char)
                    count += 1
            
            self.isLoaded = True
            print(f"Sucesso: {count} entidades catalogadas no censo.")
        else:
            print("Aviso: Não foi possivel carregar dados da api (verifique a chave).")
            # carrega dados de teste se a api falhar
            self._loadMockData()

    def _loadMockData(self):
        # dados para teste caso a api falhe
        print("Carregando dados de backup...")
        mockData = [
            {"name": "Frodo Baggins", "race": "Hobbit", "realm": "Shire"},
            {"name": "Aragorn II Elessar", "race": "Human", "realm": "Gondor"},
            {"name": "Gandalf", "race": "Maiar", "realm": ""},
            {"name": "Legolas", "race": "Elf", "realm": "Woodland Realm"},
            {"name": "Gimli", "race": "Dwarf", "realm": "Erebor"}
        ]
        for char in mockData:
            self.censusData.insert(char['name'], char)
        self.isLoaded = True

    def searchEntity(self, name):
        # busca na tabela hash
        return self.censusData.search(name)
