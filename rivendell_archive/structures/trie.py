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
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # marca o fim da palavra
        node.isEndOfWord = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                # se o caminho for quebrado a palavra nao existe
                return False
            node = node.children[char]
        
        # retorna true apenas se for o fim de uma palavra inserida
        return node.isEndOfWord

    def startsWith(self, prefix):
        # busca por um prefixo
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        # retorna true se o prefixo existe (nao importa se e fim de palavra)
        return True
        
    def getWordsWithPrefix(self, prefix):
        # encontra o no correspondente ao prefixo
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
            
        # a partir deste no faz uma busca em profundidade para encontrar todas as palavras (dfs)
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, currentPrefix, results):
        # se o no atual marca o fim de uma palavra adiciona aos resultados
        if node.isEndOfWord:
            results.append(currentPrefix)
            
        # segue busca recursiva para todos os filhos
        for char, childNode in node.children.items():
            self._dfs(childNode, currentPrefix + char, results)
