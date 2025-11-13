def solveGreedyKnapsack(supplies, maxCapacity):
    # supplies e uma lista de dicionarios
    # calcular a razao (utilidade/peso) para cada item
    for item in supplies:
        if item['peso'] > 0:
            item['ratio'] = item['utilidade'] / item['peso']
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
        if totalWeight + item['peso'] <= maxCapacity:
            # pega o item inteiro
            totalWeight += item['peso']
            totalUtility += item['utilidade']
            adventureBag.append((item['nome'], 1.0)) # (nome, 100% do item)
            
        # se o item nao couber e ignorado
        # checa proximo items
            
    return (totalUtility, totalWeight, adventureBag)
