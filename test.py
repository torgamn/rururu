from rivendell_archive.structures.hash_table import HashTable
from rivendell_archive.core.api_client import getCharacters

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
        print(f"nome: {foundCharacter.get('name')}")
        print(f"raca: {foundCharacter.get('race')}")
        print(f"reino: {foundCharacter.get('realm')}")
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


if __name__ == '__main__':
    # ponto de entrada principal do teste
    testModule1()
