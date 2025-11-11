# esboco classe modulo 3
class BTreeNode:
    # no da arvore b
    def __init__(self, isLeaf=False):
        self.isLeaf = isLeaf
        self.keys = []      # chaves
        self.values = []    # valores
        self.children = []  # ponteiros

class BTree:
    
    def __init__(self, t):
        self.root = BTreeNode(isLeaf=True)
        self.t = t

    def insert(self, key, value):
        # insere um evento
        # e a operacao complexa que pode precisar de split
        # aqui ocorreria a analise amortizada
        pass

    def search(self, key):
        # busca um evento exato
        pass
        
    def searchRange(self, startKey, endKey):
        # busca eventos dentro de um intervalo de chaves (anos)
        pass
        
    def _splitChild(self, parentNode, index):
        # dividi um no filho que esta cheio
        pass
