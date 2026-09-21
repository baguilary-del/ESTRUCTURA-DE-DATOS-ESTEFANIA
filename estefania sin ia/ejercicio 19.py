class Inventario:

    def __init__(self):
        self.stock = {}

    def agregar_stock(self, producto, cantidad):
        if cantidad > 0:
            self.stock[producto] = self.stock.get(producto, 0) + int(cantidad)

    def restar_stock(self, producto, cantidad):
        cant = int(cantidad)
        if producto in self.stock and self.stock[producto] >= cant:
            self.stock[producto] -= cant
            return True
        return False

    def productos_bajo_stock(self, minimo):
        return [
            prod for prod, cant in self.stock.items()
            if cant < minimo
        ]



if __name__ == "__main__":
    tienda = Inventario()

    tienda.agregar_stock("Laptops", 10)
    tienda.agregar_stock("Mouses", 5)
    tienda.agregar_stock("Teclados", 2)

    print( tienda.stock)

    # 2. Restar stock (compra exitosa)
    exito1 = tienda.restar_stock("Laptops", 3)
    exito2 = tienda.restar_stock("Teclados", 5)
    alertas = tienda.productos_bajo_stock(5)

