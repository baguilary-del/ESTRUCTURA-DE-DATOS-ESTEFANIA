class temperatura_gestor:
    def __init__(self):
        self.temperaturas = []

    def registrar(self, temperatura):
        self.temperaturas.append(float(temperatura))

    def agregar_multiples(self, *temperaturas):
        for temperatura in temperaturas:
            self.registrar(temperatura)
        return self.temperaturas

    def minima(self):
        if not self.temperaturas:
            return None
        return min(self.temperaturas)

    def maxima(self):
        if not self.temperaturas:
            return None
        return max(self.temperaturas)

    def promedio(self):
        if not self.temperaturas:
            return None
        return sum(self.temperaturas)/len(self.temperaturas)
if __name__ == "__main__":
    temperatura_gestor = temperatura_gestor()
    print(temperatura_gestor.agregar_multiples(34, 19, 25, 10))
    print(temperatura_gestor.promedio())
    print(temperatura_gestor.minima())
    print(temperatura_gestor.maxima())
