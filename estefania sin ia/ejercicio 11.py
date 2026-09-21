class ContadorFrecuencia:

    def __init__(self):
        self.frecuencias = {}

    def agregar_elemento(self, elemento):
        self.frecuencias[elemento] = self.frecuencias.get(elemento, 0) + 1

    def frecuencia_elemento(self, elemento):
        return self.frecuencias.get(elemento, 0)

    def elemento_mas_frecuente(self):
        if not self.frecuencias:
            return None
        mas_frecuente = max(self.frecuencias, key=self.frecuencias.get)
        return mas_frecuente, self.frecuencias[mas_frecuente]


if __name__ == "__main__":
    contador = ContadorFrecuencia()
    print(contador.elemento_mas_frecuente())
    contador.agregar_elemento('a')
    contador.frecuencia_elemento('a')
    print(contador.frecuencias)