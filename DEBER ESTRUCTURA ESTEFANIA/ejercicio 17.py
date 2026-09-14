class AgrupadorEdades:
    def __init__(self):
        self.grupos = {}

    def clasificar_edad(self, edad):
        if edad < 12:
            return "niño"
        elif edad < 18:
            return "adolescente"
        elif edad < 60:
            return "adulto"
        else:
            return "mayor"

    def agrupar_por_categoria(self, *edades):
        self.grupos = {
            "niño": [],
            "adolescente": [],
            "adulto": [],
            "mayor": []
        }
        for edad in edades:
            cat = self.clasificar_edad(edad)
            self.grupos[cat].append(edad)
        return self.grupos

    def edad_promedio_categoria(self, categoria):
        edades_cat = self.grupos.get(categoria, [])
        if not edades_cat:
            return 0.0
        return sum(edades_cat) / len(edades_cat)


ae = AgrupadorEdades()
print(ae.agrupar_por_categoria(5, 15, 30, 70))