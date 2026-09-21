# class analizar_texto:
#     def __init__(self):
#         self.palabras_unicas = set()
#         self.palabras_historial = []
#
#     def agregar_palabra(self,palabra):
#         palabra = str(palabra)
#         if palabra not in self.palabras_unicas:
#             self.palabras_unicas.add(palabra)
#             self.palabras_historial.append(palabra)
#
#     def contar_palabras(self):
#         return len(self.palabras_unicas)
#
#     def multiples_palabras(self, *args):
#         for palabra in args:
#             self.agregar_palabra(palabra)
#
# if __name__ == "__main__":
#     analizador = analizar_texto()
#
#     analizador.agregar_palabra("python")
#     analizador.agregar_palabra("python")
#     analizador.agregar_palabra("azul")
#     print(analizador.contar_palabras())
#     analizador.multiples_palabras('carro','casa','gato')
#     print(analizador.palabras_historial)

