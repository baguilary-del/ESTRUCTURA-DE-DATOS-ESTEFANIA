class CombinadorListas:
    def intercalar(self, lista1, lista2):
        resultado = []
        max_len = max(len(lista1), len(lista2))
        for i in range(max_len):
            if i < len(lista1):
                resultado.append(lista1[i])
            if i < len(lista2):
                resultado.append(lista2[i])
        return resultado

    def intercalar_multiples(self, *listas):
        if not listas:
            return []
        max_len = max(len(l) for l in listas)
        resultado = []
        for i in range(max_len):
            for lista in listas:
                if i < len(lista):
                    resultado.append(lista[i])
        return resultado



cl = CombinadorListas()
print(cl.intercalar([1, 2], [3, 4]))