class equiposs:
    def __init__(self):
        self.equipos = {}

    def crear_equipo(self, nom_equipo):
        if nom_equipo not in self.equipos:
            self.equipos[nom_equipo] = []

    def agregar(self, equipo, jugador):
        if equipo not in self.equipos:
            self.crear_equipo(equipo)
            self.equipos[equipo].append(jugador)

    def mayor_integrante(self):
        if not self.equipos:
            return None
        equipo_mayor = max(self.equipos, key = lambda eq: len(self.equipos[eq]))
        return equipo_mayor

if __name__ == '__name__':
    personas = equiposs()
    personas.crear_equipo('marco')
    print(personas.mayor_integrante())
    personas.agregar('juan', 10)


