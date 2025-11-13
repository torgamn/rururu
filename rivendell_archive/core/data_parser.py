import csv

def parseCsvFile(filePath):
    # retorna uma lista de dicionarios
    data = []
    try:
        with open(filePath, mode='r', encoding='utf-8') as file:
            # dictreader le cada linha como um dicionario
            reader = csv.DictReader(file)
            
            for row in reader:
                data.append(row)
                
        return data
        
    except FileNotFoundError:
        print(f'erro: arquivo nao encontrado em {filePath}')
        return []
    except Exception as e:
        print(f'erro ao ler o arquivo csv: {e}')
        return []

# funcoes especificas podem ser criadas se necessario
def loadSupplies(filePath='data/suprimentos.csv'):
    # le e converte os valores numericos
    supplies = parseCsvFile(filePath)
    processedSupplies = []
    for item in supplies:
        try:
            # converte peso e utilidade para numeros
            item['peso'] = float(item['peso'])
            item['utilidade'] = int(item['utilidade'])
            processedSupplies.append(item)
        except (ValueError, KeyError) as e:
            print(f'aviso: pulando item mal formatado: {item} ({e})')
            
    return processedSupplies
