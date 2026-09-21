class calificar:
    def __init__(self):
        self.notas = []

    def validar_notas(self,notas):
        return 0 <= notas <= 100

    def cargar_notas(self, *args):
        for notas in args:
            if self.validar_notas(notas):
                self.notas.append(notas)
            return self.notas

    def promedio(self):
        if not self.notas:
            return 0.0
        return sum(self.notas) / len(self.notas)

if __name__ == "__main__":
    calificar = calificar()
    print(calificar.promedio())
    print(calificar.validar_notas([1,2,3,4,5]))
    print(calificar.cargar_notas())

