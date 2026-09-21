class AnalizadorPatrones:

    def __init__(self):
        self.palabras_vistas = set()

    def encontrar_palabras(self, texto, patron):
        palabras = texto.lower().replace(".", "").replace(",", "").split()
        coincidencias = []
        for palabra in palabras:
            self.palabras_vistas.add(palabra)
            if palabra.startswith(patron.lower()):
                coincidencias.append(palabra)
        return coincidencias

    def agrupar_por_longitud(self, texto):
        palabras = texto.lower().replace(".", "").replace(",", "").split()
        agrupadas = {}
        for palabra in palabras:
            self.palabras_vistas.add(palabra)
            longitud = len(palabra)
            if longitud not in agrupadas:
                agrupadas[longitud] = []
            if palabra not in agrupadas[longitud]:
                agrupadas[longitud].append(palabra)
        return agrupadas

    def palabras_unicas(self):
        return self.palabras_vistas


if __name__ == "__main__":
    analizador = AnalizadorPatrones()
    print(analizador.palabras_unicas())
    print(analizador.encontrar_palabras('casa'))
    print(analizador.agrupar_por_longitud('hola'))
