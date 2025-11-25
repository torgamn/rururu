from rivendell_archive.structures.b_tree import BTree

class AlmanacModule:
    def __init__(self, t=3):
        # t define o grau minimo da arvore b
        self.chronicles = BTree(t)

    def loadDefaultEvents(self):
        # carrega uma lista de eventos importantes
        # isso poderia vir de um arquivo grande
        events = [
            (1000, "chegada dos istari (magos) a terra-media"),
            (1600, "fundacao do condado pelos hobbits"),
            (1697, "queda de eregion e morte de celebrimbor"),
            (1980, "despertar do balrog em moria"),
            (2463, "smeagol (gollum) encontra o anel"),
            (2510, "eorl o jovem cavalga para o campo de celebrant (origem de rohan)"),
            (2770, "smaug o dourado ataca e toma erebor"),
            (2931, "nascimento de aragorn filho de arathorn"),
            (2941, "batalha dos cinco exercitos e morte de smaug"),
            (3001, "festa de aniversario de bilbo baggins"),
            (3018, "conselho de elrond e formacao da sociedade"),
            (3019, "destruicao do um anel e queda de sauron"),
            (3021, "partida dos portadores do anel nos portos cinzentos")
        ]
        
        for year, description in events:
            self.chronicles.insert(year, description)
            
        print(f"almanaque historico: {len(events)} eventos registrados.")

    def findEventByYear(self, year):
        # busca exata na arvore b
        return self.chronicles.search(year)

    def findEventsInPeriod(self, startYear, endYear):
        # busca por intervalo eficiente na arvore b
        return self.chronicles.searchRange(startYear, endYear)
