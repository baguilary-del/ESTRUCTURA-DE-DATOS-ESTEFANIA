class DivisorFinder:

    def __init__(self):
        pass

    def encontrar_divisores(self, numero):
        divisores = []
        for i in range(1, numero + 1):
            if numero % i == 0:
                divisores.append(i)
        return tuple(divisores)

    def es_perfecto(self, numero):
        if numero <= 1:
            return False
        divisores_propios = self.encontrar_divisores(numero)[:-1]
        return sum(divisores_propios) == numero

    def encontrar_multiples_divisores(self, *numeros):
        resultado = {}
        for num in numeros:
            resultado[num] = self.encontrar_divisores(num)
        return resultado



if __name__ == "__main__":
    finder = DivisorFinder()
    finder.encontrar_multiples_divisores(4, 3)
    print(finder.es_perfecto(3))
    print(finder.es_perfecto(2))
    print(finder.encontrar_divisores(12))
    diccionario_divisores = finder.encontrar_multiples_divisores(8, 15, 28)

