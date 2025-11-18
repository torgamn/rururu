from rivendell_archive.structures.hash_table import HashTable
from rivendell_archive.core.api_client import getCharacters
from rivendell_archive.core.data_parser import loadSupplies
from rivendell_archive.modules.logistics_module import solveGreedyKnapsack
from rivendell_archive.structures.trie import Trie
from rivendell_archive.structures.b_tree import BTree # importacao adicionada

def testModule1():
    print('iniciando teste do modulo 1 (censo / hash table)')
    
    characters = getCharacters()
    
    if not characters:
        print('falha ao buscar personagens. o teste nao pode continuar')
        print('certifique-se de que a chave THE_ONE_API_KEY esta configurada')
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
        
    # buscar por um personagem que nao existe
    keyToSearch = 'Relampago Mcqueen'
    print(f'\nbuscando por: "{keyToSearch}"')
    
    foundCharacter = characterCensus.search(keyToSearch)
    
    if foundCharacter:
        print(f'erro: "{keyToSearch}" personagem encontrado, mas nao deveria existir')
    else:
        print(f'sucesso: "{keyToSearch}" nao foi encontrado, como esperado')

def testModule2():
    print('\n')
    print('iniciando teste do modulo 2 (trie)')
    
    linguisticPalantir = Trie()
    
    print('inserindo palavras na trie')
    words = ["mellon", "moria", "mordor", "minas", "mithril"] # aqui
    for word in words:
        linguisticPalantir.insert(word)
    
    print('testando busca')
    print(f'buscando "moria": {linguisticPalantir.search("moria")} (esperado: True)')
    print(f'buscando "mellon": {linguisticPalantir.search("mellon")} (esperado: True)')
    print(f'buscando "gandalf": {linguisticPalantir.search("gandalf")} (esperado: False)')
    # mor e um prefixo mas nao uma palavra inserida
    print(f'buscando "mor": {linguisticPalantir.search("mor")} (esperado: False)') 

    print('\ntestando prefixo')
    print(f'buscando prefixo "mor": {linguisticPalantir.startsWith("mor")} (esperado: True)')
    print(f'buscando prefixo "min": {linguisticPalantir.startsWith("min")} (esperado: True)')
    print(f'buscando prefixo "gal": {linguisticPalantir.startsWith("gal")} (esperado: False)')
    # uma palavra tambem e um prefixo de si mesma
    print(f'buscando prefixo "mordor": {linguisticPalantir.startsWith("mordor")} (esperado: True)')

def testModule3():
    print('\n')
    print('iniciando teste do modulo 3')
    
    historicalAlmanac = BTree(t=3) 
    
    print('inserindo eventos historicos (ano, evento)...')
    
    # dados de exemplo
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
    
    for year, event in events:
        historicalAlmanac.insert(year, event)
        
    print(f'insercao de {len(events)} eventos concluida')

    print('\niniciando teste de busca exata')
    keyToSearch = 2941
    foundEvent = historicalAlmanac.search(keyToSearch)
    if foundEvent:
        print(f'busca por {keyToSearch}: encontrado! "{foundEvent}"')
    else:
        print(f'erro: busca por {keyToSearch} falhou (esperado: Batalha dos Cinco Exercitos)')
        
    keyToSearch = 1500 # nao existe
    foundEvent = historicalAlmanac.search(keyToSearch)
    if not foundEvent:
        print(f'busca por {keyToSearch}: nao encontrado, como esperado')
    else:
        print(f'erro: busca por {keyToSearch} encontrou "{foundEvent}" (esperado: None)')

    print('\niniciando teste de busca por intervalo')
    
    # consulta por intervalo
    startYear = 1600
    endYear = 2000
    
    print(f'buscando eventos entre {startYear} e {endYear}...')
    rangeResults = historicalAlmanac.searchRange(startYear, endYear)
    
    if rangeResults:
        for year, event in rangeResults:
            print(f'- {year}: {event}')
    else:
        print('nenhum evento encontrado no intervalo')

    # outro intervalo
    startYear = 3000
    endYear = 4000
    print(f'\nbuscando eventos entre {startYear} e {endYear}')
    rangeResults = historicalAlmanac.searchRange(startYear, endYear)
    
    if rangeResults:
        for year, event in rangeResults:
            print(f'- {year}: {event}')
    else:
        print('nenhum evento encontrado no intervalo')

def testModule4():
    print('\n')
    print('iniciando teste da bolsa do aventureiro modulo 4')
    
    supplies = loadSupplies()
    
    if not supplies:
        print('falha ao carregar suprimentos.')
        print('certifique-se de que o arquivo "data/suprimentos.csv" existe.')
        return
        
    print(f'{len(supplies)} suprimentos carregados.')
    
    maxCapacity = 10.0 # capacidade maxima da bolsa
    
    print(f'calculando bolsa para capacidade maxima de: {maxCapacity}')
    
    (totalUtility, totalWeight, adventureBag) = solveGreedyKnapsack(supplies, maxCapacity)
    
    print('\nresultado da bolsa gulosa')
    print(f'utilidade total: {totalUtility:.2f}')
    print(f'peso total: {totalWeight:.2f}')
    print('itens na bolsa (item, fracao):')
    for item in adventureBag:
        print(f'- {item[0]} ({(item[1] * 100):.1f}%)')


if __name__ == '__main__':
    testModule1()
    testModule2()
    testModule3() # chamada do novo modulo de teste
    testModule4()
