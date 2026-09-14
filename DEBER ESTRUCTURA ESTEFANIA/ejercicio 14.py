class RegistroNotas:
    def __init__(self):
        self.registros = {}

    def registrar(self, estudiante, nota):
        self.registros[estudiante] = nota

    def estudiantes_aprobados(self, nota_minima):
        return [
            estudiante for estudiante, nota in self.registros.items()
            if nota >= nota_minima
        ]

    def mejor_estudiante(self):
        if not self.registros:
            return None
        mejor = max(self.registros.items(), key=lambda item: item[1])
        return mejor


rn = RegistroNotas()
rn.registrar("Ana", 95)
rn.registrar("Bob", 70)
print(rn.mejor_estudiante())