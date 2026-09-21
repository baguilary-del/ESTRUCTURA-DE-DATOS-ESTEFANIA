class CodificadorCesar:

    def __init__(self):
        self.historial = {}

    def codificar_letra(self, letra, desplazamiento):
        if not letra.isalpha():
            return letra

        base = ord('A') if letra.isupper() else ord('a')
        posicion_original = ord(letra) - base
        nueva_posicion = (posicion_original + desplazamiento) % 26

        return chr(base + nueva_posicion)

    def codificar_palabra(self, palabra, desplazamiento):
        letras_codificadas = [
            self.codificar_letra(letra, desplazamiento)
            for letra in palabra
        ]
        palabra_cifrada = "".join(letras_codificadas)
        self.historial[palabra] = palabra_cifrada
        return palabra_cifrada


if __name__ == "__main__":
    codificador = CodificadorCesar()
    print( codificador.codificar_letra('a', 3))
    print( codificador.codificar_letra('z', 3))
    p1 = codificador.codificar_palabra("Python", 3)
    p2 = codificador.codificar_palabra("Cesar", 5)
    print(codificador.historial)

