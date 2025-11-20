from rivendell_archive.structures.hash_table import HashTable
from rivendell_archive.core.api_client import getCharacters
from rivendell_archive.core.data_parser import loadSupplies
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack
from rivendell_archive.structures.trie import Trie
from rivendell_archive.structures.b_tree import BTree

def testModule1():
    print('iniciando teste do modulo 1 (censo / hash table)')
    
    print('teste de redimensionamento')
    smallTable = HashTable(initialCapacity=5)
    print(f'tabela criada com capacidade: {smallTable.capacity}')
    
    testKeys = ["Frodo", "Sam", "Merry", "Pippin", "Aragorn", "Boromir", "Legolas", "Gimli"]
    print(f'inserindo {len(testKeys)} itens')
    
    for k in testKeys:
        smallTable.insert(k, {"name": k})
        
    print(f'nova capacidade da tabela: {smallTable.capacity} (esperado: > 5)')
    if smallTable.capacity > 5:
        print('tabela redimensionada corretamente')
    else:
        print('tabela nao redimensionou')
        
    # Verifica se os dados ainda estao la
    found = smallTable.search("Frodo")
    print(f'buscando "Frodo" apos resize: {found is not None}')
    print('\n')

    characters = getCharacters()
    
    if not characters:
        print('falha ao buscar personagens. verifique sua chave de API ou conexao.')
        return

    characterCensus = HashTable(initialCapacity=100) 
    
    print(f'inserindo {len(characters)} personagens na hash table...')
    for char in characters:
        if 'name' in char:
            characterCensus.insert(char['name'], char)
            
    print(f'insercao concluida. tamanho da tabela: {characterCensus.size}')
    
    print('iniciando teste de busca')
    
    keyToSearch = 'Gandalf'
    print(f'buscando por: "{keyToSearch}"')
    
    foundCharacter = characterCensus.search(keyToSearch)
    
    if foundCharacter:
        print(f'encontrado! dados:')
        print(f"  nome: {foundCharacter.get('name')}")
        print(f"  raca: {foundCharacter.get('race')}")
        print(f"  reino: {foundCharacter.get('realm')}")
    else:
        print(f'erro: "{keyToSearch}" nao foi encontrado')
        
    keyToSearch = 'Relampago Mcqueen'
    foundCharacter = characterCensus.search(keyToSearch)
    
    if not foundCharacter:
        print(f'sucesso: "{keyToSearch}" nao foi encontrado, como esperado')

def testModule2():
    print('\n')
    print('iniciando teste do modulo 2 (trie)')
    
    linguisticPalantir = Trie()
    
    print('inserindo palavras na trie...')
    words = ["mellon", "moria", "mordor", "minas", "mithril", "gondor", "gondolin"]
    for word in words:
        linguisticPalantir.insert(word)
    
    print('testando busca exata')
    print(f'buscando "moria": {linguisticPalantir.search("moria")}')
    print(f'buscando "gandalf": {linguisticPalantir.search("gandalf")}')

    print('\ntestando autocomplete (getWordsWithPrefix)')
    
    prefix = "mo"
    print(f'buscando palavras com prefixo "{prefix}":')
    results = linguisticPalantir.getWordsWithPrefix(prefix)
    print(f'resultado: {results}') 
    # esperado moria, mordor
    
    prefix = "mi"
    print(f'buscando palavras com prefixo "{prefix}":')
    results = linguisticPalantir.getWordsWithPrefix(prefix)
    print(f'resultado: {results}')
    # esperado minas, mithril

    prefix = "gon"
    print(f'buscando palavras com prefixo "{prefix}":')
    results = linguisticPalantir.getWordsWithPrefix(prefix)
    print(f'resultado: {results}')
    # esperado gondor, gondolin
    
    prefix = "xyz"
    print(f'buscando prefixo "{prefix}":')
    results = linguisticPalantir.getWordsWithPrefix(prefix)
    print(f'resultado: {results}')
    # esperado nada

def testModule3():
    print('\n')
    print('iniciando teste do modulo 3 (b-tree)')
    
    historicalAlmanac = BTree(t=3) 
    
    events = [
        (1697, "Queda de Eregion"),
        (3441, "Fim da Guerra da Ultima Alianca"),
        (1000, "Chegada dos Istari"),
        (1600, "Fundacao do Condado"),
        (2941, "Batalha dos Cinco Exercitos"),
        (3018, "Inicio da Guerra do Anel"),
        (3019, "Destruicao do Um Anel"),
        (1980, "Despertar do Balrog em Moria"),
        (2770, "Smaug ataca Erebor"),
    ]
    
    print(f'inserindo {len(events)} eventos historicos...')
    for year, event in events:
        historicalAlmanac.insert(year, event)

    print('teste de busca exata (ano 2941)...')
    foundEvent = historicalAlmanac.search(2941)
    print(f'resultado: {foundEvent}')

    print('\nteste de busca por intervalo (1500 a 2000)...')
    rangeResults = historicalAlmanac.searchRange(1500, 2000)
    for year, event in rangeResults:
        print(f'- {year}: {event}')

def testModule4():
    print('\n')
    print('iniciando teste do modulo 4 (mochila gulosa)')
    
    supplies = loadSupplies()
    
    if not supplies:
        print('falha ao carregar suprimentos.')
        return
        
    maxCapacity = 10.0
    print(f'calculando bolsa para capacidade: {maxCapacity}')
    
    (totalUtility, totalWeight, adventureBag) = solveGreedyKnapsack(supplies, maxCapacity)
    
    print(f'utilidade total: {totalUtility:.2f}')
    print(f'peso total: {totalWeight:.2f}')
    print('itens na bolsa:')
    for item in adventureBag:
        print(f'- {item[0]}')

if __name__ == '__main__':
    testModule1()
    testModule2()
    testModule3()
    testModule4()
