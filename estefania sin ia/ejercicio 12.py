class SelectorRango:

    def __init__(self):
        pass

    def crear_rango(self, inicio, fin):
        return tuple(range(inicio, fin + 1))

    def elementos_en_multiples_rangos(self, *rangos):
        elementos_unicos = set()
        for inicio, fin in rangos:
            rango_tupla = self.crear_rango(inicio, fin)
            elementos_unicos.update(rango_tupla)
        return sorted(list(elementos_unicos))

if __name__ == "__main__":
    selector = SelectorRango()

    selector.crear_rango(1, 10)
    print(selector.elementos_en_multiples_rangos(1, 10))
