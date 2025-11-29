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
            # armazena (nome, 100% do item)
            adventureBag.append((item['name'], 1.0)) 
            
    return (totalUtility, totalWeight, adventureBag)
