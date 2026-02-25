from rivendell_archive.structures.trie import Trie

class LinguisticModule:
    def __init__(self):
        self.trie = Trie()

    def indexTextData(self, textList):
        # recebe uma lista de textos e indexa palavras
        count = 0
        for text in textList:
            if not text:
                continue
                
            # separa palavras simples por espaco
            words = text.split()
            for word in words:
                # remove caracteres indesejados e mantem minusculo
                cleanWord = ''.join(filter(str.isalpha, word)).lower()
                if cleanWord:
                    self.trie.insert(cleanWord)
                    count += 1
        print(f"palantir linguistico: {count} palavras indexadas.")

    def searchPrefix(self, prefix):
        # utiliza a trie para buscar todas as palavras com este prefixo
        if prefix is None:
            return []
        return self.trie.getWordsWithPrefix(prefix.lower())

    def checkSpelling(self, word):
        # resgata todas as palavras inseridas pedindo um prefixo vazio direto na arvore
        allWords = self.trie.getWordsWithPrefix("")
        if not allWords:
            return (word, 0)
        
        bestMatch = word
        minDist = float('inf')
        
        for w in allWords:
            dist = self._levenshtein(word.lower(), w.lower())
            if dist < minDist:
                minDist = dist
                bestMatch = w
                
        return (bestMatch, minDist)

    def _levenshtein(self, s1, s2):
        # algoritmo de distancia de edicao para o corretor ortografico
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previousRow = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            currentRow = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previousRow[j + 1] + 1
                deletions = currentRow[j] + 1
                substitutions = previousRow[j] + (c1 != c2)
                currentRow.append(min(insertions, deletions, substitutions))
            previousRow = currentRow
        return previousRow[-1]
