class RegistroNotas:

    def __init__(self):
        self.registros = {}

    def registrar(self, estudiante, nota):
        self.registros[estudiante] = float(nota)

    def estudiantes_aprobados(self, nota_minima=70.0):
        return [
            estudiante for estudiante, nota in self.registros.items()
            if nota >= nota_minima
        ]

    def mejor_estudiante(self):
        if not self.registros:
            return None
        nombre_top = max(self.registros, key=self.registros.get)
        return nombre_top, self.registros[nombre_top]



if __name__ == "__main__":
    gestion = RegistroNotas()
    print(gestion.mejor_estudiante())
    gestion.registrar()
    print(gestion.estudiantes_aprobados())
    print(gestion.registros)

