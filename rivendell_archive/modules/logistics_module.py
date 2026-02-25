def solveGreedyKnapsack(supplies, maxCapacity):
    # supplies e uma lista de dicionarios
    for item in supplies:
        if item['weight'] > 0:
            item['ratio'] = item['utility'] / item['weight']
        else:
            # utilidade infinita se peso zero (pegar sempre)
            item['ratio'] = float('inf') 
            
    # ordenar os itens pela razao, em ordem decrescente
    sortedSupplies = sorted(supplies, key=lambda x: x['ratio'], reverse=True)
    
    totalUtility = 0
    totalWeight = 0
    adventureBag = []
    
    for item in sortedSupplies:
        
        # verifica se o item inteiro cabe na capacidade restante
        if totalWeight + item['weight'] <= maxCapacity:
            # pega o item inteiro
            totalWeight += item['weight']
            totalUtility += item['utility']
            # armazena o dicionario do item inteiro (ESPERO QUE SEJA COMPATIVEL)
            adventureBag.append(item) 
            
    return (totalUtility, totalWeight, adventureBag)

def solveDynamicKnapsack(supplies, maxCapacity):
    # ou leva tudo ou nada
    
    # pesos sao float; normalizar para usar como indice da matriz
    precisionFactor = 10
    capacityInt = int(maxCapacity * precisionFactor)
    n = len(supplies)
    
    # inicializando tabela dp (matriz (n+1) x (capacityInt+1))
    dp = [[0 for _ in range(capacityInt + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = supplies[i-1]
        weightInt = int(item['weight'] * precisionFactor)
        utility = item['utility']
        
        for w in range(capacityInt + 1):
            if weightInt <= w:
                utilityWithoutItem = dp[i-1][w]
                utilityWithItem = utility + dp[i-1][w - weightInt]
                
                if utilityWithItem > utilityWithoutItem:
                    dp[i][w] = utilityWithItem
                else:
                    dp[i][w] = utilityWithoutItem
            else:
                dp[i][w] = dp[i-1][w]
                
    # recuperacao dos itens selecionados
    selectedItems = []
    w = capacityInt
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            item = supplies[i-1]
            selectedItems.append(item) 
            w -= int(item['weight'] * precisionFactor)
            
    totalUtility = sum(item['utility'] for item in selectedItems)
    totalWeight = sum(item['weight'] for item in selectedItems)
    
    return (totalUtility, totalWeight, selectedItems)

def optimizeBarter(currentBag, merchantOffers, maxCapacity):
    # combina os itens atuais com a oferta do mercador e re-otimiza
    fullPool = currentBag + merchantOffers
    return solveDynamicKnapsack(fullPool, maxCapacity)

def evaluateEncounter(currentBag, newItem, maxCapacity):
    # avalia se um novo item encontrado deve substituir itens atuais
    pool = currentBag + [newItem]
    
    (newUtil, newWeight, optimizedBag) = solveDynamicKnapsack(pool, maxCapacity)
    
    keptNewItem = False
    for item in optimizedBag:
        if item['name'] == newItem['name'] and item['utility'] == newItem['utility']:
            keptNewItem = True
            break
            
    discardedItems = []
    currentNames = [i['name'] for i in optimizedBag]
    
    for oldItem in currentBag:
        found = False
        for optItem in optimizedBag:
            if optItem['name'] == oldItem['name'] and optItem['utility'] == oldItem['utility']:
                found = True
                break
        if not found:
            discardedItems.append(oldItem)
            
    return (keptNewItem, discardedItems, optimizedBag, newUtil, newWeight)
