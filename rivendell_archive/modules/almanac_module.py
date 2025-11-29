from rivendell_archive.structures.b_tree import BTree
from rivendell_archive.core.data_parser import parseCsvFile

class AlmanacModule:
    def __init__(self, t=3):
        # t define o grau minimo da arvore b
        self.chronicles = BTree(t)

    def loadEvents(self, filePath='data/events.csv'):
        # carrega os eventos historicos do arquivo csv
        # utiliza o parser padrao do sistema
        eventsData = parseCsvFile(filePath)
        
        count = 0
        if eventsData:
            for row in eventsData:
                try:
                    year = int(row['year'])
                    description = row['description']
                    
                    self.chronicles.insert(year, description)
                    count += 1
                except (ValueError, KeyError):
                    # ignora linhas mal formatadas
                    continue
            
        print(f"almanaque historico: {count} eventos registrados.")

    def findEventByYear(self, year):
        # busca exata na arvore b
        return self.chronicles.search(year)

    def findEventsInPeriod(self, startYear, endYear):
        # busca por intervalo eficiente na arvore b
        return self.chronicles.searchRange(startYear, endYear)
