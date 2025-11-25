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
        if not prefix:
            return []
        return self.trie.getWordsWithPrefix(prefix.lower())
