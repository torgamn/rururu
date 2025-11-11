# esboco classe modulo 2
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False

class Trie:
    
    def __init__(self):
        # a raiz e um no vazio
        self.root = TrieNode()

    def insert(self, word):
        # insere uma palavra na trie
        pass

    def search(self, word):
        # busca por uma palavra exata
        # retorna true se a palavra existe
        pass

    def startsWith(self, prefix):
        # busca por um prefixo (autocomplete)
        # retorna true se existe alguma palavra com esse prefixo
        pass
        
    def getWordsWithPrefix(self, prefix):
        # ver mais avancada de autocomplete
        # retorna uma lista de palavras que comecam com o prefixo
        pass
