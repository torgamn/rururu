class BTreeNode:
    # no da arvore b
    def __init__(self, isLeaf=False):
        self.isLeaf = isLeaf
        self.keys = []      # chaves
        self.values = []    # valores
        self.children = []  # ponteiros para nos filhos

class BTree:
    
    def __init__(self, t):
        # t e o grau minimo
        self.root = BTreeNode(isLeaf=True)
        self.t = t # grau minimo

    def search(self, key):
        # busca um valor pela chave
        return self._searchRecursive(self.root, key)

    def _searchRecursive(self, node, key):
        # funcao auxiliar recursiva para a busca
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
            
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
            
        if node.isLeaf:
            return None # nao encontrado
            
        return self._searchRecursive(node.children[i], key)

    def searchRange(self, startKey, endKey):
        results = []
        self._searchRangeRecursive(self.root, startKey, endKey, results)
        return results

    def _searchRangeRecursive(self, node, startKey, endKey, results):
        i = 0
        # encontra a primeira chave no no que e >= startKey
        while i < len(node.keys) and startKey > node.keys[i]:
            i += 1
            
        if not node.isLeaf:
            # node.children[i] contem chaves < node.keys[i]
            self._searchRangeRecursive(node.children[i], startKey, endKey, results)
            
        # itera por todas as chaves e filhos restantes
        while i < len(node.keys):
            # se a chave atual esta dentro do intervalo
            if startKey <= node.keys[i] <= endKey:
                results.append((node.keys[i], node.values[i]))
                
            if endKey < node.keys[i]:
                break
                
            # desce para o proximo filho
            if not node.isLeaf:
                self._searchRangeRecursive(node.children[i+1], startKey, endKey, results)
                
            i += 1

    def insert(self, key, value):
        # insere um par (chave, valor)
        rootNode = self.root
        
        # a raiz esta cheia
        if len(rootNode.keys) == (2 * self.t - 1):
            # cria um novo no (que sera a nova raiz)
            newRoot = BTreeNode(isLeaf=False)
            self.root = newRoot
            
            newRoot.children.append(rootNode)
            
            self._splitChild(newRoot, 0)
            
            self._insertNonFull(newRoot, key, value)
        else:
            # a raiz nao esta cheia
            self._insertNonFull(rootNode, key, value)

    def _insertNonFull(self, node, key, value):
        # insere em um no que nao esta cheio
        i = len(node.keys) - 1
        
        if node.isLeaf:
            node.keys.append(None)
            node.values.append(None)
            
            # move as chaves/valores maiores para a direita
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
                
            # insere a nova chave/valor
            node.keys[i+1] = key
            node.values[i+1] = value
            
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1 # indice do filho
            
            # verifica se o filho esta cheio
            if len(node.children[i].keys) == (2 * self.t - 1):
                # se o filho esta cheio, divide ele
                self._splitChild(node, i)
                
                # decide para qual dos dois novos filhos deve descer
                if key > node.keys[i]:
                    i += 1
                    
            self._insertNonFull(node.children[i], key, value)

    def _splitChild(self, parentNode, index):
        fullChild = parentNode.children[index]
        
        newChild = BTreeNode(isLeaf=fullChild.isLeaf)
        
        # move a chave/valor do meio do fullChild para o parentNode
        middleKey = fullChild.keys[self.t - 1]
        middleValue = fullChild.values[self.t - 1]
        
        parentNode.keys.insert(index, middleKey)
        parentNode.values.insert(index, middleValue)
        
        parentNode.children.insert(index + 1, newChild)
        
        newChild.keys = fullChild.keys[self.t:]
        newChild.values = fullChild.values[self.t:]
        
        if not fullChild.isLeaf:
            newChild.children = fullChild.children[self.t:]
            
        fullChild.keys = fullChild.keys[:self.t - 1]
        fullChild.values = fullChild.values[:self.t - 1]
        fullChild.children = fullChild.children[:self.t]

    def toList(self):
        # retorna todos os itens da arvore em ordem (in-order traversal)
        # util para o modulo de relacionamentos
        items = []
        self._toListRecursive(self.root, items)
        return items

    def _toListRecursive(self, node, items):
        if not node:
            return
            
        i = 0
        while i < len(node.keys):
            if not node.isLeaf:
                self._toListRecursive(node.children[i], items)
            
            items.append((node.keys[i], node.values[i]))
            i += 1
            
        if not node.isLeaf:
            self._toListRecursive(node.children[i], items)
