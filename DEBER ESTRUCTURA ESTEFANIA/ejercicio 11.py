class SelectorRango:
    def crear_rango(self, inicio, fin):
        return tuple(range(inicio, fin + 1))

    def elementos_en_multiples_rangos(self, *rangos):
        resultado = []
        for rango in rangos:
            for num in rango:
                if num not in resultado:
                    resultado.append(num)
        return resultado


sr = SelectorRango()
r1 = sr.crear_rango(1, 5)
print(r1)