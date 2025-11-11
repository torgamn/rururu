# esboco funcao modulo 4
def solveGreedyKnapsack(supplies, maxCapacity):
    # supplies e uma lista de dicionarios
    # calcular a razao (utilidade/peso) para cada item
    for item in supplies:
        if item['peso'] > 0:
            item['ratio'] = item['utilidade'] / item['peso']
        else:
            item['ratio'] = float('inf') # utilidade infinita se peso zero
            
    # ordenar os itens pela razao, em ordem decrescente
    sortedSupplies = sorted(supplies, key=lambda x: x['ratio'], reverse=True)
    
    totalUtility = 0
    totalWeight = 0
    adventureBag = []
    
    # iterar pelos itens ordenados e adicionar na bolsa
    for item in sortedSupplies:
        # assumindo mochila fracionaria podemos pegar parte do item
        
        if totalWeight + item['peso'] <= maxCapacity:
            # pega o item inteiro
            totalWeight += item['peso']
            totalUtility += item['utilidade']
            adventureBag.append((item['nome'], 1.0)) # (nome, 100% do item)
            
        else:
            # pega apenas a fracao que cabe
            remainingCapacity = maxCapacity - totalWeight
            fraction = remainingCapacity / item['peso']
            
            totalWeight += remainingCapacity
            totalUtility += item['utilidade'] * fraction
            adventureBag.append((item['nome'], fraction)) # (nome, fracao do item)
            
            # a bolsa esta cheia, para o loop
            break 
            
    return (totalUtility, totalWeight, adventureBag)
