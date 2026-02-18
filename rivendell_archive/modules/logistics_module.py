def solveGreedyKnapsack(supplies, maxCapacity):
    # supplies e uma lista de dicionarios
    # este metodo resolve o problema da mochila fracionaria (pode levar parte do item)
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
            # armazena (nome, 1.0) indicando 100% do item
            adventureBag.append((item['name'], 1.0)) 
            
    return (totalUtility, totalWeight, adventureBag)

def solveDynamicKnapsack(supplies, maxCapacity):
    # nao podemos dividir itens (ou leva tudo ou nada)
    
    # como os pesos sao float precisa normalizar para usar como indice da matriz
    # multiplicamos por 10 (0.5 vira 5)
    precisionFactor = 10
    capacityInt = int(maxCapacity * precisionFactor)
    n = len(supplies)
    
    # inicializando tabela dp (matriz (n+1) x (capacityInt+1))
    # dp[i][w] armazena a utilidade maxima com os primeiros i itens e capacidade w
    dp = [[0 for _ in range(capacityInt + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = supplies[i-1]
        weightInt = int(item['weight'] * precisionFactor)
        utility = item['utility']
        
        for w in range(capacityInt + 1):
            if weightInt <= w:
                # logica padrao da mochila 0/1:
                # maximo entre (nao levar o item) e (levar o item + melhor valor com o peso restante)
                utilityWithoutItem = dp[i-1][w]
                utilityWithItem = utility + dp[i-1][w - weightInt]
                
                if utilityWithItem > utilityWithoutItem:
                    dp[i][w] = utilityWithItem
                else:
                    dp[i][w] = utilityWithoutItem
            else:
                # se o item nao cabe, mantemos o valor anterior
                dp[i][w] = dp[i-1][w]
                
    # recuperacao dos itens selecionados (backtracking na matriz)
    selectedItems = []
    w = capacityInt
    
    for i in range(n, 0, -1):
        # se o valor mudou em relacao a linha de cima, significa que o item foi incluido
        if dp[i][w] != dp[i-1][w]:
            item = supplies[i-1]
            selectedItems.append(item) # armazena o objeto item inteiro
            w -= int(item['weight'] * precisionFactor)
            
    # calcula totais finais baseados nos itens selecionados
    totalUtility = sum(item['utility'] for item in selectedItems)
    totalWeight = sum(item['weight'] for item in selectedItems)
    
    return (totalUtility, totalWeight, selectedItems)

def optimizeBarter(currentBag, merchantOffers, maxCapacity):
    # combina os itens atuais com a oferta do mercador e re-otimiza
    
    # pool de todos os itens disponiveis (meus + mercador)
    fullPool = currentBag + merchantOffers
    
    # remove duplicatas de referencias se houver, ou trata como itens unicos
    # aqui assumimos que cada item no pool e uma instancia unica
    
    # roda o algoritmo de mochila 0/1 no pool total para achar a melhor combinacao possivel
    return solveDynamicKnapsack(fullPool, maxCapacity)
