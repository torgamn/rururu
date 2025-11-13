import requests
import os # para carregar a chave da api de forma segura

# constante para a url base
baseUrl = 'https://the-one-api.dev/v2'

def getHeaders():
    # retorna o cabecalho de autorizacao
    # le a chave de uma variavel de ambiente por seguranca
    theOneApiKey = os.environ.get('THE_ONE_API_KEY')
    
    if not theOneApiKey:
        # erro se a chave nao estiver configurada
        print('erro: variavel de ambiente THE_ONE_API_KEY nao definida.')
        return None
        
    return {
        'Authorization': f'Bearer {theOneApiKey}'
    }

def getAllPaginatedData(endpointUrl):
    # funcao para buscar dados de um endpoint que usa paginacao
    headers = getHeaders()
    if headers is None:
        return []

    results = []
    page = 1
    
    while True:
        try:
            # adiciona o parametro de paginacao na url
            paginatedUrl = f"{endpointUrl}?page={page}"
            response = requests.get(paginatedUrl, headers=headers)
            response.raise_for_status() # levanta erro http
            
            data = response.json()
            
            # adiciona os resultados desta pagina a lista total
            results.extend(data.get('docs', []))
            
            # logica de parada da paginacao da 'the one api'
            currentPage = data.get('page', 1)
            totalPages = data.get('pages', 1)
            
            if currentPage >= totalPages:
                break # sai do loop se chegou na ultima pagina
            
            page += 1
            
        except requests.exceptions.RequestException as e:
            print(f'erro ao buscar dados da api (pagina {page}): {e}')
            return None # retorna none em caso de falha

    return results


def getCharacters():
    # exemplo de funcao para buscar todos os personagens
    # /character e um endpoint da the one api
    endpoint = f'{baseUrl}/character'
    
    print(f'buscando todos os personagens de {endpoint}...')
    characters = getAllPaginatedData(endpoint)
    print(f'{len(characters)} personagens encontrados.')
    
    return characters

# def getLocations():
