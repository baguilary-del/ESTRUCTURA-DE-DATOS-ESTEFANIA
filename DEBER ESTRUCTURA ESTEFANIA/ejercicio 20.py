class AnalizadorPatrones:
    def __init__(self):
        self.textos_procesados = []

    def encontrar_palabras(self, texto, patron):
        palabras = texto.split()
        return [p for p in palabras if p.lower().startswith(patron.lower())]

    def agrupar_por_longitud(self, texto):
        self.textos_procesados.append(texto)
        palabras = texto.split()
        agrupadas = {}
        for palabra in palabras:
            longitud = len(palabra)
            if longitud not in agrupadas:
                agrupadas[longitud] = []
            agrupadas[longitud].append(palabra)
        return agrupadas

    def palabras_unicas(self):
        texto_completo = " ".join(self.textos_procesados)
        return set(texto_completo.split())


ap = AnalizadorPatrones()
print(ap.agrupar_por_longitud("el gato está aquí"))
