from evento import Evento

class EventoOn(Evento):
    def __init__(self, nome, _=""):
        local =f"http://discord.com/call de aulas?id={EventoOn.id}"
        super().__init__(nome, local)
        
    def  imprime(self):
        print(f"ID do evento: {self.id}")
        print(f"Nome do Evento: {self.nome}" )
        print(f"link do evento: {self.local}" )
        print("-----------------\n")