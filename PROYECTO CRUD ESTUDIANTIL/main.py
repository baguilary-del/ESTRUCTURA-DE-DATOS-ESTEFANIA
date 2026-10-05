from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import ClienteController, EstudianteController

class MenuClientes:
    """VISTA: muestra, pide y presenta. No decide reglas del negocio."""

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"     # atributo de clase
    ENTIDAD = "cliente"                            # para los textos del menú
    ANCHO = 85

    def __init__(self, controlador=ClienteController):
        # ATRIBUTOS DE INSTANCIA: estado de ESTE menú
        self._controlador = controlador
        self._activo = True
        # DICCIONARIO tecla -> (texto, método). Reemplaza al if/elif largo.
        self._opciones = {
            "1": (f"Crear {self.ENTIDAD}", self.crear),
            "2": ("Ver todos", self.listar),
            "3": ("Buscar", self.buscar),
            "4": ("Ver por id", self.ver_por_id),
            "5": ("Actualizar", self.actualizar),
            "6": ("Eliminar", self.eliminar),
            "7": ("Estadísticas", self.estadisticas),
            "0": ("Salir", self.salir),
        }

    # ===== ESTÁTICOS: utilidades de pantalla, no dependen del menú =====
    @staticmethod
    def pausa():
        input("\nPresione Enter para continuar...")

    @staticmethod
    def pedir_entero(etiqueta):
        """Devuelve un entero o None si el usuario escribió cualquier otra cosa."""
        try:
            return int(input(etiqueta))
        except ValueError:
            return None

    @staticmethod
    def mostrar_resultado(exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    # ===== MÉTODOS DE INSTANCIA =====
    def mostrar_tabla(self, clientes):
        print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}{'TELÉFONO':<12}")
        print("-" * self.ANCHO)
        for cliente in clientes:
            print(f"{cliente.id:<5}{cliente.nombre_completo:<25}"
                  f"{cliente.email:<28}{cliente.ciudad:<15}{cliente.telefono:<12}")
        print("-" * self.ANCHO)
        imprimir_info(f"Total: {len(clientes)} registro(s)")

    def crear(self):
        imprimir_titulo(f"CREAR NUEVO {self.ENTIDAD.upper()}")
        # Recorro la TUPLA de campos del Modelo: si el Modelo cambia, el formulario también
        datos = {}
        for campo in self._controlador.MODELO.CAMPOS:
            datos[campo] = input(f"{campo.capitalize()}: ")

        exito, mensaje = self._controlador.crear(datos)
        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    def listar(self):
        imprimir_titulo(f"LISTA DE {self.ENTIDAD.upper()}S")
        clientes = self._controlador.listar()
        if not clientes:
            imprimir_info(f"Todavía no hay registros. Use la opción 1 para crear el primero.")
        else:
            self.mostrar_tabla(clientes)
        self.pausa()

    def buscar(self):
        imprimir_titulo(f"BUSCAR {self.ENTIDAD.upper()}")
        termino = input("Texto a buscar: ")
        encontrados = self._controlador.buscar(termino)
        if not encontrados:
            imprimir_info(f"Ningún registro coincide con '{termino}'.")
        else:
            self.mostrar_tabla(encontrados)
        self.pausa()

    def ver_por_id(self):
        imprimir_titulo(f"VER {self.ENTIDAD.upper()} POR ID")
        id_cliente = self.pedir_entero("Id del registro: ")
        if id_cliente is None:
            imprimir_error("El id debe ser un número entero")
            return self.pausa()

        cliente = self._controlador.obtener(id_cliente)
        if cliente is None:
            imprimir_error(f"No existe un {self.ENTIDAD} con id {id_cliente}")
        else:
            for clave, valor in cliente.a_diccionario().items():
                print(f"  {clave.capitalize():<12}: {valor}")
            imprimir_info(f"Dominio del email: {cliente.dominio_email}")
        self.pausa()

    def actualizar(self):
        imprimir_titulo(f"ACTUALIZAR {self.ENTIDAD.upper()}")
        id_cliente = self.pedir_entero("Id del registro: ")
        if id_cliente is None:
            imprimir_error("El id debe ser un número entero")
            return self.pausa()

        cliente = self._controlador.obtener(id_cliente)
        if cliente is None:
            imprimir_error(f"No existe un {self.ENTIDAD} con id {id_cliente}")
            return self.pausa()

        imprimir_info(f"Editando a {cliente.nombre_completo}")
        print("Deje en blanco el campo que no quiera cambiar.\n")

        cambios = {}
        for campo in self._controlador.MODELO.CAMPOS:
            actual = getattr(cliente, campo)          # lee la PROPIEDAD
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

        self.mostrar_resultado(*self._controlador.actualizar(id_cliente, cambios))
        self.pausa()

    def eliminar(self):
        imprimir_titulo(f"ELIMINAR {self.ENTIDAD.upper()}")
        id_cliente = self.pedir_entero("Id del registro: ")
        if id_cliente is None:
            imprimir_error("El id debe ser un número entero")
            return self.pausa()

        cliente = self._controlador.obtener(id_cliente)
        if cliente is None:
            imprimir_error(f"No existe un {self.ENTIDAD} con id {id_cliente}")
            return self.pausa()

        imprimir_info(f"Se eliminará: {cliente}")
        if confirmar("¿Confirma la eliminación?"):
            self.mostrar_resultado(*self._controlador.eliminar(id_cliente))
        else:
            imprimir_info("Operación cancelada")
        self.pausa()

    def estadisticas(self):
        imprimir_titulo("ESTADÍSTICAS")
        datos = self._controlador.estadisticas()
        print(f"  Clientes registrados : {datos['total']}")
        print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")
        print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
        print(f"  Sin teléfono         : {len(datos['sin_telefono'])}")
        self.pausa()

    def salir(self):
        self._activo = False          # cambia el estado del objeto
        imprimir_info("¡Hasta luego! 👋")

    def mostrar_menu(self):
        imprimir_titulo(self.TITULO)
        for tecla, (texto, _metodo) in self._opciones.items():
            print(f"  {tecla}. {texto}")
        print()

    def ejecutar(self):
        """El bucle principal: vive mientras __activo sea True."""
        while self._activo:
            self.mostrar_menu()
            tecla = input("Seleccione una opción: ").strip()

            if tecla not in self._opciones:
                imprimir_error("Opción no válida")
                self.pausa()
                continue

            _texto, metodo = self._opciones[tecla]
            metodo()          # el diccionario guarda el método: aquí se ejecuta


# ======================================================================
#  TAREA: MenuEstudiantes hereda de MenuClientes
# ======================================================================
class MenuEstudiantes(MenuClientes):
    """Mismo menú, otro controlador, otra tabla y 3 opciones nuevas."""

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    ENTIDAD = "estudiante"
    ANCHO = 92

    def __init__(self):
        super().__init__(controlador=EstudianteController)   # polimorfismo: otro controlador
        # Sacamos "Salir", agregamos las nuevas y lo volvemos a poner al final
        salir = self._opciones.pop("0")
        self._opciones["8"] = ("Agregar nota", self.agregar_nota)
        self._opciones["9"] = ("Ver promedio", self.ver_promedio)
        self._opciones["10"] = ("Materias en común", self.materias_en_comun)
        self._opciones["0"] = salir

    # ===== ESTÁTICO: otra utilidad de pantalla =====
    @staticmethod
    def pedir_numero(etiqueta):
        """Devuelve int/float o None si lo escrito no es un número."""
        try:
            numero = float(input(etiqueta).replace(",", "."))
        except ValueError:
            return None
        return int(numero) if numero.is_integer() else numero

    # ===== AYUDA DE INSTANCIA =====
    def _pedir_estudiante(self):
        """Pide un id y devuelve el Estudiante, o None (ya mostró el error)."""
        id_estudiante = self.pedir_entero("Id del estudiante: ")
        if id_estudiante is None:
            imprimir_error("El id debe ser un número entero")
            return None
        estudiante = self._controlador.obtener(id_estudiante)
        if estudiante is None:
            imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return estudiante

    # ===== SOBRESCRITOS: lo que en clientes no sirve para estudiantes =====
    def mostrar_tabla(self, estudiantes):
        print(f"{'ID':<5}{'NOMBRE':<25}{'CARNET':<14}{'EMAIL':<28}{'PROMEDIO':<10}{'ESTADO':<10}")
        print("-" * self.ANCHO)
        for e in estudiantes:
            print(f"{e.id:<5}{e.nombre_completo:<25}{e.carnet:<14}"
                  f"{e.email:<28}{e.promedio:<10}{e.estado:<10}")
        print("-" * self.ANCHO)
        imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

    def ver_por_id(self):
        imprimir_titulo("VER ESTUDIANTE POR ID")
        estudiante = self._pedir_estudiante()
        if estudiante is not None:
            self._mostrar_ficha(estudiante)
        self.pausa()

    def _mostrar_ficha(self, e):
        print(f"  Nombre   : {e.nombre_completo}")
        print(f"  Carnet   : {e.carnet}")
        print(f"  Email    : {e.email}")
        print(f"  Materias : {', '.join(sorted(e.materias)) or '(ninguna)'}")
        for materia in sorted(e.materias):
            print(f"    - {materia}: {e.notas_de(materia) or 'sin notas'}")
        print(f"  Promedio : {e.promedio}  ->  {e.estado}")

    def estadisticas(self):
        imprimir_titulo("ESTADÍSTICAS")
        d = self._controlador.estadisticas()
        print(f"  Estudiantes registrados : {d['total']}")
        print(f"  Promedio general        : {d['promedio_general']}")
        print(f"  Aprobados  ({len(d['aprobados'])})        : {', '.join(d['aprobados']) or '-'}")
        print(f"  Reprobados ({len(d['reprobados'])})        : {', '.join(d['reprobados']) or '-'}")
        print(f"  Materias ofertadas      : {', '.join(d['materias']) or '-'}")
        self.pausa()

    # ===== OPCIONES NUEVAS =====
    def agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")
        estudiante = self._pedir_estudiante()
        if estudiante is None:
            return self.pausa()

        imprimir_info(f"Estudiante: {estudiante.nombre_completo}")
        materia = input("Materia: ")
        nota = self.pedir_numero("Nota (0 a 20): ")
        if nota is None:
            imprimir_error("La nota debe ser un número")
            return self.pausa()

        self.mostrar_resultado(*self._controlador.agregar_nota(estudiante.id, materia, nota))
        self.pausa()

    def ver_promedio(self):
        imprimir_titulo("PROMEDIO DE UN ESTUDIANTE")
        estudiante = self._pedir_estudiante()
        if estudiante is not None:
            self._mostrar_ficha(estudiante)
        self.pausa()

    def materias_en_comun(self):
        imprimir_titulo("MATERIAS EN COMÚN")
        id_a = self.pedir_entero("Id del primer estudiante: ")
        id_b = self.pedir_entero("Id del segundo estudiante: ")
        if id_a is None or id_b is None:
            imprimir_error("Los ids deben ser números enteros")
            return self.pausa()

        exito, resultado = self._controlador.materias_en_comun(id_a, id_b)
        if not exito:
            imprimir_error(resultado)
        elif resultado:
            imprimir_exito(f"Materias en común: {', '.join(sorted(resultado))}")
        else:
            imprimir_info("No comparten ninguna materia")
        self.pausa()


if __name__ == "__main__":
    try:
        MenuEstudiantes().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
