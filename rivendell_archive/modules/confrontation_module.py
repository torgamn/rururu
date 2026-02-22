import random

class ConfrontationModule:
    def __init__(self):
        # palavras-chave para identificar eventos negativos no almanaque
        self.negativeKeywords = [
            "batalha", "guerra", "queda", "morte", "ataque", 
            "destruicao", "fim", "traicao", "despertar", "ameaca"
        ]

    def calculateConfrontationProbability(self, locationName, mapModule, almanacModule):
        # calcula a probabilidade base de confronto (pc) para um local
        # formula: pc(l) = (100 * (malicia + 0.5 * eventos_negativos) + fator_aleatorio) / 100
        
        # 1. obtem dados do mapa (malicia)
        locData = mapModule.getLocationMetadata(locationName)
        maliceScore = locData.get("malice", 0.0)
        
        # 2. conta eventos negativos no local (almanaque)
        negativeEventsCount = self._countNegativeEvents(locationName, almanacModule)
        
        # normaliza eventos negativos (0 a 10)
        if negativeEventsCount > 10:
            negativeEventsCount = 10
            
        # 3. fator aleatorio (0 a 20)
        randomFactor = random.randint(0, 20)
        
        # calculo final
        rawChance = (100 * (maliceScore + 0.5 * negativeEventsCount) + randomFactor) / 100
        
        # garante que a probabilidade esteja entre 0 e 1
        probability = max(0.0, min(1.0, rawChance))
        
        print(f"analise de risco em {locationName}:")
        print(f"- malicia: {maliceScore}")
        print(f"- eventos historicos negativos: {negativeEventsCount}")
        print(f"- fator aleatorio: {randomFactor}")
        print(f"- probabilidade calculada (Pc): {probability:.2f} ({probability*100:.1f}%)")
        
        return probability

    def checkConfrontationTrigger(self, probability):
        # compara pc com um numero aleatorio para decidir se ocorre confronto
        roll = random.random() # 0.0 a 1.0
        print(f"rolagem do destino: {roll:.2f} (necessario <= {probability:.2f})")
        return roll <= probability

    def resolveConfrontation(self, societyBag, locationName, mapModule):
        # simula a mecanica de combate
        
        # obtem dificuldade do local
        locData = mapModule.getLocationMetadata(locationName)
        difficulty = locData.get("difficulty", 30) # padrao medio 30
        
        # calcula poder de combate da sociedade (pcsoc)
        # pcsoc = sum(utilidade) - (peso / 5)
        totalUtility = sum(item['utility'] for item in societyBag)
        totalWeight = sum(item['weight'] for item in societyBag)
        
        combatPower = totalUtility - (totalWeight / 5.0)
        
        print(f"\n--- INICIO DO CONFRONTO EM {locationName.upper()} ---")
        print(f"dificuldade do inimigo: {difficulty}")
        print(f"poder da sociedade: {combatPower:.2f} (Util: {totalUtility} - PesoPena: {totalWeight/5.0:.2f})")
        
        itemsRemoved = []
        timePenalty = 0.0
        victory = False
        
        if combatPower >= difficulty:
            print("RESULTADO: VITORIA!")
            # penalidade de vitoria: 20% do tempo (simulado aqui apenas como valor 0.2)
            # perde 1 item aleatorio de baixa utilidade
            victory = True
            timePenalty = 0.2
            
            if societyBag:
                # ordena por utilidade crescente para achar os 'menos uteis'
                # pega os 50% menos uteis para sortear a perda
                sortedBag = sorted(societyBag, key=lambda x: x['utility'])
                candidates = sortedBag[:max(1, len(sortedBag)//2)]
                lostItem = random.choice(candidates)
                
                # remove da mochila real
                societyBag.remove(lostItem)
                itemsRemoved.append(lostItem)
                print(f"baixa de batalha: {lostItem['name']} foi perdido/quebrado.")
        else:
            print("RESULTADO: DERROTA (RETIRADA ESTRATEGICA)!")
            # penalidade de derrota: 50% do tempo
            # perde 3 itens de maior utilidade
            timePenalty = 0.5
            
            if societyBag:
                # ordena por utilidade decrescente (maiores primeiro)
                sortedBag = sorted(societyBag, key=lambda x: x['utility'], reverse=True)
                
                # remove ate 3 itens
                toRemove = sortedBag[:3]
                for item in toRemove:
                    if item in societyBag:
                        societyBag.remove(item)
                        itemsRemoved.append(item)
                
                print("itens valiosos deixados para tras na fuga:")
                for i in itemsRemoved:
                    print(f"- {i['name']}")
                    
        return (victory, timePenalty, societyBag)

    def _countNegativeEvents(self, locationName, almanac):
        # helper para contar eventos negativos ligados ao local
        count = 0
        allEvents = almanac.chronicles.toList() # obtem [(ano, desc), ...]
        
        locLower = locationName.lower()
        
        for year, desc in allEvents:
            descLower = desc.lower()
            # verifica se o evento cita o local
            if locLower in descLower:
                # verifica se contem palavra chave negativa
                for keyword in self.negativeKeywords:
                    if keyword in descLower:
                        count += 1
                        break # conta apenas uma vez por evento
        return count
