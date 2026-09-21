class CombinadorListas:

    def __init__(self):
        pass

    def intercalar(self, lista1, lista2):
        resultado = []
        max_longitud = max(len(lista1), len(lista2))

        for i in range(max_longitud):
            if i < len(lista1):
                resultado.append(lista1[i])
            if i < len(lista2):
                resultado.append(lista2[i])

        return resultado

    def intercalar_multiples(self, *listas):
        if not listas:
            return []

        resultado = []
        max_longitud = max(len(l) for l in listas)

        for i in range(max_longitud):
            for lista in listas:
                if i < len(lista):
                    resultado.append(lista[i])

        return resultado


# --- PRUEBA DEL CÓDIGO ---
if __name__ == "__main__":
    combinador = CombinadorListas()
    print(combinador.intercalar())
    print(combinador.intercalar_multiples(1, 2, 3))
    print(combinador.intercalar_multiples(1, 2, 3))
