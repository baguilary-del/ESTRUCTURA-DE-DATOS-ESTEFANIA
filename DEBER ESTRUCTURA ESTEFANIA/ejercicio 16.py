class CodificadorCesar:
    def __init__(self):
        self.historial = {}

    def codificar_letra(self, letra, desplazamiento):
        if letra.isalpha():
            base = ord('a') if letra.islower() else ord('A')
            return chr((ord(letra) - base + desplazamiento) % 26 + base)
        return letra

    def codificar_palabra(self, palabra, desplazamiento):
        palabra_codificada = "".join(
            self.codificar_letra(char, desplazamiento) for char in palabra
        )
        self.historial[palabra] = palabra_codificada
        return palabra_codificada


cc = CodificadorCesar()
print(cc.codificar_palabra("hola", 3))