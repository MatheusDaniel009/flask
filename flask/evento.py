import json

class Evento:
    id = 1
    def __init__(self, nome, local = ""):
        self.nome = nome
        self.local = local
        self.id = Evento.id
        Evento.id += 1
    
    def  imprime(self):
        print(f"ID do evento: {self.id}")
        print(f"Nome do Evento: {self.nome}" )
        print(f"Local do Evento: {self.local}" )
        print("-----------------\n")

    def  toJSON(self):
        return  json.dumps(self.__dict__)

    @staticmethod
    def calculo_aria_pessoa(aria):
        if 5 <= aria < 10:
            return 5
        elif 10 <= aria < 20:
            return 7
        elif aria >= 20:
            return  10
        else:
            return 0


