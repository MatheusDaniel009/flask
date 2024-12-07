class Tarevas:
    id = 0
    def __init__(self, titulo, descricao, completa = False):
        self.titulo = titulo
        self.descricao = descricao
        self.completa = completa
        Tarevas.id += 1
        self.id = Tarevas.id
