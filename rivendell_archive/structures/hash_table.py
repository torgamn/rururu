# esboco classe modulo 1
class HashTable:
    
    def __init__(self, initialCapacity=10):
        self.capacity = initialCapacity
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key):
        # metodo privado para calcular o hash da chave
        # deve retornar um indice dentro de 'self.capacity'
        # implementacao do hash
        pass

    def insert(self, key, value):
        # insere um par (chave, valor)
        # deve tratar colisoes
        # deve checar se precisa de redimensionamento
        # (aqui ocorreria a analise amortizada)
        pass

    def search(self, key):
        # busca um valor pela chave
        # deve tratar colisoes
        # retorna o valor se encontrado, ou none
        pass

    def remove(self, key):
        # remove um item pela chave
        pass
        
    def _resize(self):
        # metodo privado para redimensionar a tabelaquando o fator de carga e muito alto
        pass
