import requests
import os # para carregar a chave da api de forma segura

# nao deve ser colocada diretamente no codigo (tenho que ver isso ainda)
THE_ONE_API_KEY = os.environ.get('THE_ONE_API_KEY', 'TEMP_KEY')
BASE_URL = 'https://the-one-api.dev/v2'

def getHeaders():
    # retorna o cabecalho de autorizacao
    return {
        'Authorization': f'Bearer {THE_ONE_API_KEY}'
    }

def getCharacters():
    # exemplo de funcao para buscar personagens
    # character e um endpoint da the one api
    endpoint = f'{BASE_URL}/character'
    headers = getHeaders()
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        # levanta um erro http se a requisicao falhar
        response.raise_for_status() 
        
        # retorna o json processado (uma lista de personagens)
        return response.json() 
    
    except requests.exceptions.RequestException as e:
        print(f'# erro ao buscar dados da api: {e}')
        return None

# def getLocations():
