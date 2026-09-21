class AgrupadorEdades:

    def __init__(self):
        self.grupos = {
            "niño": [],
            "adolescente": [],
            "adulto": [],
            "mayor": []
        }

    def clasificar_edad(self, edad):
        if edad < 0:
            return None
        elif edad <= 12:
            return "niño"
        elif edad <= 17:
            return "adolescente"
        elif edad <= 64:
            return "adulto"
        else:
            return "mayor"

    def agrupar_por_categoria(self, *edades):
        for edad in edades:
            categoria = self.clasificar_edad(edad)
            if categoria in self.grupos:
                self.grupos[categoria].append(edad)
        return self.grupos

    def edad_promedio_categoria(self, categoria):
        cat = categoria.lower()
        if cat not in self.grupos or not self.grupos[cat]:
            return 0.0
        edades = self.grupos[cat]
        return sum(edades) / len(edades)



if __name__ == "__main__":
    agrupador = AgrupadorEdades()


    print(agrupador.clasificar_edad(8))
    print(agrupador.clasificar_edad(15))
    print(agrupador.clasificar_edad(30))
    print(agrupador.clasificar_edad(70))

