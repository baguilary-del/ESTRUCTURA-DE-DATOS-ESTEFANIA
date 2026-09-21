class compras:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, nombre, precio):
        self.productos[nombre] = float(precio)

    def total_compras(self):
        return sum(self.productos.values())

    def compras_rango(self, precio_min, precio_max):
        resultado = []
        for nombre, precio in self.productos.items():
            if precio_min <= precio <= precio_max:
                resultado.append(nombre)
        return resultado

if __name__ == "__main__":
    compras = compras()
    print(compras.agregar_producto("pan", 2.50))
    print(compras.compras_rango(1.00, 3.00))
    print(compras.total_compras())

