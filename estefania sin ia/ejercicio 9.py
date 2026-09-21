class analizador:
    def __init__(self):
        self.texto_mas_largo = ''

    def vocales(self, letra):
        return letra.lower() in 'aeiouáéíóú'

    def contar_por_tipo(self, texto):
        if len(texto) > len(self.texto_mas_largo):
            self.texto_mas_largo = texto
        conteos = {'vocales': 0, 'consonantes': 0, 'digitos': 0}
        for char in texto:
            if char.isdigit():
                conteos['digitos'] += 1
            elif char.isalpha():
                if self.solo_vocales(char):
                    conteos['vocales'] += 1
                else:
                    conteos['consonantes'] += 1
        return conteos
if __name__ == '__main__':
    analizador = analizador()
    print(analizador.texto_mas_largo)


