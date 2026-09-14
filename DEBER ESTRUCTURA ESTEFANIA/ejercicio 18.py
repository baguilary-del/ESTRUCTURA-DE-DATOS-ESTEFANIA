import math

class CalculadorDistancia:
    def __init__(self):
        self.distancias_calculadas = []

    def distancia_euclidiana(self, p1, p2):
        d = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        self.distancias_calculadas.append(d)
        return d

    def punto_mas_cercano(self, referencia, *puntos):
        if not puntos:
            return None
        return min(puntos, key=lambda p: self.distancia_euclidiana(referencia, p))


cd = CalculadorDistancia()
print(cd.distancia_euclidiana((0, 0), (3, 4))) 