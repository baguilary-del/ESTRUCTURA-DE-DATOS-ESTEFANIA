import math

class CalculadorDistancia:

    def __init__(self):
        self.distancias = []

    def distancia_euclidiana(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        self.distancias.append(distancia)
        return distancia

    def punto_mas_cercano(self, referencia, *puntos):
        if not puntos:
            return None
        return min(puntos, key=lambda p: self.distancia_euclidiana(referencia, p))


if __name__ == "__main__":
    calc = CalculadorDistancia()

    p_origen = (0, 0)
    p_destino = (3, 4)


    d = calc.distancia_euclidiana(p_origen, p_destino)
    print(f"Distancia entre {p_origen} y {p_destino}: {d}")

    ref = (1, 1)
    p1 = (10, 10)
    p2 = (2, 2)
    p3 = (-5, 3)

    cercano = calc.punto_mas_cercano(ref, p1, p2, p3)
    print(f"\nEl punto más cercano a {ref} es: {cercano}")
    print(calc.distancias)