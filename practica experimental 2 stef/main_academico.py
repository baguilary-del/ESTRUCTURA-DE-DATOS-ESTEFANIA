"""Menú del sistema académico.

Reutiliza MenuCRUD tal cual para Estudiantes, Docentes y Materias.
Solo Matrículas necesita un menú propio: MenuMatriculas(MenuCRUD).
"""
from main import MenuCRUD
from shared.herramientas import (
    imprimir_titulo, imprimir_error, imprimir_info
)
from views_academico import (
    EstudianteController, DocenteController,
    MateriaController, MatriculaController,
)

# HERENCIA + SOBRESCRITURA: un MenuCRUD con opciones extra

class MenuMatriculas(MenuCRUD):

    def __init__(self, controlador):
        super().__init__(controlador, "MATRÍCULAS")
        self._opciones["1"] = ("Matricular estudiante", self.crear)
        self._opciones["7"] = ("Agregar nota", self.agregar_nota)
        self._opciones["8"] = ("Ver boletín", self.ver_boletin)
        self._opciones["9"] = ("Reporte: estudiantes reprobados", self.ver_reprobados)

    def crear(self):
        """Sobrescribe: muestra estudiantes y materias antes de pedir los ids."""
        imprimir_titulo("MATRICULAR ESTUDIANTE")

        imprimir_info("Estudiantes:")
        for estudiante in self._controlador.estudiantes.listar():
            print(f"  {estudiante}")
        estudiante_id = self.pedir_entero("\nId del estudiante: ")

        imprimir_info("Materias:")
        for materia in self._controlador.materias.listar():
            print(f"  {materia}")
        materia_id = self.pedir_entero("\nId de la materia: ")

        if estudiante_id is None or materia_id is None:
            imprimir_error("Los ids deben ser números")
            return self.pausa()

        periodo = input("Periodo (Enter = 2026-1): ")
        self.mostrar_resultado(*self._controlador.crear({
            "estudiante_id": estudiante_id,
            "materia_id": materia_id,
            "periodo": periodo,
        }))
        self.pausa()

    def agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")
        matricula_id = self.pedir_entero("Id de la matrícula: ")
        matricula = self._controlador.obtener(matricula_id) if matricula_id else None
        if matricula is None:
            imprimir_error("No existe esa matrícula")
            return self.pausa()

        imprimir_info(matricula.etiqueta())
        imprimir_info("Tipos permitidos: deber, lección, examen")
        tipo = input("Tipo: ")
        valor = input("Valor (0 a 20): ")
        peso = input("Peso (Enter = 1): ").strip() or 1
        self.mostrar_resultado(
            *self._controlador.agregar_nota(matricula_id, tipo, valor, peso)
        )
        self.pausa()

    def ver_boletin(self):
        imprimir_titulo("BOLETÍN")
        estudiante_id = self.pedir_entero("Id del estudiante: ")
        texto = self._controlador.boletin(estudiante_id) if estudiante_id else None
        if texto is None:
            imprimir_error("No existe ese estudiante")
        else:
            print(texto)
        self.pausa()

    def ver_reprobados(self):
        imprimir_titulo("ESTUDIANTES REPROBADOS")
        reprobados = self._controlador.reprobados()
        if not reprobados:
            imprimir_info("No hay matrículas reprobadas.")
        else:
            # POLIMORFISMO: print() usa __str__ -> etiqueta() de cada clase
            for matricula, estudiante, materia in reprobados:
                print(f"  {estudiante}")
                print(f"     {materia}")
                print(f"     {matricula}")
            imprimir_info(f"Total: {len(reprobados)}")
        self.pausa()


# =====================================================================
class MenuPrincipal:

    def __init__(self):
        estudiantes = EstudianteController()
        docentes = DocenteController()
        materias = MateriaController(docentes)
        matriculas = MatriculaController(estudiantes, materias)

        self._activo = True
        self._menus = {
            "1": MenuCRUD(estudiantes, "ESTUDIANTES"),
            "2": MenuCRUD(docentes, "DOCENTES"),
            "3": MenuCRUD(materias, "MATERIAS"),
            "4": MenuMatriculas(matriculas),
        }

    def ejecutar(self):
        while self._activo:
            imprimir_titulo("SISTEMA ACADÉMICO")
            print("  1. Estudiantes")
            print("  2. Docentes")
            print("  3. Materias")
            print("  4. Matrículas")
            print("  0. Salir\n")
            tecla = input("Opción: ").strip()

            if tecla == "0":
                imprimir_info("¡Hasta luego! 👋")
                self._activo = False
            elif tecla in self._menus:
                self._menus[tecla].ejecutar()
            else:
                imprimir_error("Opción no válida")
                MenuCRUD.pausa()


if __name__ == "__main__":
    try:
        MenuPrincipal().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
