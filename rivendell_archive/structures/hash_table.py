class HashTable:
    
    def __init__(self, initialCapacity=10):
        self.capacity = initialCapacity
        self.size = 0
        # cada elemento da tabela agora e uma lista
        self.table = [[] for _ in range(self.capacity)]
        # fator de carga limite
        self.loadFactorThreshold = 0.7

    def _hash(self, key):
        # implementacao do hash (soma dos valores unicode)
        hashValue = 0
        for char in str(key):
            hashValue += ord(char)
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
        
        # checa se precisa de redimensionamento (fator de carga)
        if (self.size / self.capacity) > self.loadFactorThreshold:
            self._resize()

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
        
        return None
        
    def _resize(self):
        #print(f'DEBUG redimensionando tabela de {self.capacity} para {self.capacity * 2}...')
        
        oldTable = self.table
        self.capacity *= 2 # dobra a capacidade
        self.size = 0 # reseta o tamanho (incrementa novamente nos inserts)
        self.table = [[] for _ in range(self.capacity)]
        
        # reinsere todos os itens da tabela antiga na nova
        for bucket in oldTable:
            for key, value in bucket:
                self.insert(key, value)
