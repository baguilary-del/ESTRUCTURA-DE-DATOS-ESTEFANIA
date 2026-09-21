class gestor_personas:
    def __init__(self):
        self.personas = {}

    def agregar(self, nombre,edad):
        self.personas[nombre] = int(edad)

    def mayores(self, edad_min):
        resultado = []
        for nombre, edad in self.personas.items():
            if edad > edad_min:
                resultado.append(nombre)
        return resultado

    def promedio(self):
        if not self.personas:
            return 0.0
        return sum(self.personas.values()) / len(self.personas)


if __name__ == '__main__':
    personas = gestor_personas()
    print(personas.promedio())
    print(personas.mayores(18))
    personas.agregar("marco", 15)
    print(personas.personas)
    print(personas.mayores(18))
