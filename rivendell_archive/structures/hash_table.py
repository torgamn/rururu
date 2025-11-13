class HashTable:
    
    def __init__(self, initialCapacity=10):
        self.capacity = initialCapacity
        self.size = 0
        # cada elemento da tabela agora e uma lista (para tratar colisoes por encadeamento)
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        # metodo privado para calcular o hash da chave
        # implementacao de hash simples (soma dos valores unicode)
        hashValue = 0
        for char in str(key):
            hashValue += ord(char)
        # deve retornar um indice dentro de self.capacity
        return hashValue % self.capacity

    def insert(self, key, value):
        # insere um par (chave, valor)
        index = self._hash(key)
        bucket = self.table[index]
        
        # checa se a chave ja existe no bucket (lista)
        for i, (existingKey, existingValue) in enumerate(bucket):
            if existingKey == key:
                # se existe, atualiza o valor e retorna
                bucket[i] = (key, value)
                return
                
        # se nao existe, adiciona o novo par (chave, valor) ao bucket
        bucket.append((key, value))
        self.size += 1
        
        # deve checar se precisa de redimensionamento (fator de carga)
        # (aqui ocorreria a analise amortizada) - deixado para depois
        # if (self.size / self.capacity) > 0.7:
        #     self._resize()
        pass

    def search(self, key):
        # busca um valor pela chave
        index = self._hash(key)
        bucket = self.table[index]
        
        # itera pelo bucket para encontrar a chave
        for existingKey, existingValue in bucket:
            if existingKey == key:
                # retorna o valor se encontrado
                return existingValue
                
        # retorna none se a chave nao for encontrada
        return None

    def remove(self, key):
        # remove um item pela chave
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (existingKey, existingValue) in enumerate(bucket):
            if existingKey == key:
                # remove o par (chave, valor) e retorna
                bucket.pop(i)
                self.size -= 1
                return existingValue
        
        # se nao encontrou, nao faz nada
        return None
        
    def _resize(self):
        # metodo privado para redimensionar a tabelaquando o fator de carga e muito alto
        pass
