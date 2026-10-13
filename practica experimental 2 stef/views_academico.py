"""Controladores del negocio académico.

Los cuatro heredan de CrudBase: el CRUD (crear, listar, buscar, actualizar,
eliminar) NO se vuelve a escribir. Cada controlador solo aporta sus reglas
propias en validar() y los métodos específicos de su negocio.
"""
from models_academico import Estudiante, Docente, Materia, Matricula
from views import CrudBase

# Utilidad compartida por los validadores (evita repetir código)
def faltantes_obligatorios(modelo, datos):
    """Devuelve el mensaje de error si falta algún campo obligatorio."""
    faltantes = [c for c in modelo.OBLIGATORIOS
                 if not str(datos.get(c, "")).strip()]
    if faltantes:
        return f"Faltan campos obligatorios: {', '.join(faltantes)}"
    return None


# =====================================================================
class EstudianteController(CrudBase):
    """LISTO como ejemplo: cópialo y guíate con él para los demás."""
    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    NOMBRE = "estudiante"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            faltantes = [c for c in self.MODELO.OBLIGATORIOS
                         if not str(datos.get(c, "")).strip()]
            if faltantes:
                return f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if "carnet" in datos and str(datos["carnet"]).strip():
            carnet = str(datos["carnet"]).strip().upper()
            usados = {r["carnet"].upper() for r in self.registros()
                      if r["id"] != id_actual}
            if carnet in usados:
                return f"El carnet {carnet} ya está registrado"
        return None


# =====================================================================
class DocenteController(CrudBase):
    MODELO = Docente
    ARCHIVO = "data/docentes.json"
    NOMBRE = "docente"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "especialidad")

    def validar(self, datos, id_actual=None):
        # Regla 1: obligatorios (solo al crear)
        if id_actual is None:
            error = faltantes_obligatorios(self.MODELO, datos)
            if error:
                return error

        # Regla 2: el email de docente es único
        if "email" in datos and str(datos["email"]).strip():
            email = str(datos["email"]).strip().lower()
            usados = {r["email"].lower() for r in self.registros()
                      if r["id"] != id_actual}
            if email in usados:
                return "Ese email ya está registrado"
        return None


# =====================================================================
class MateriaController(CrudBase):
    """AGREGACIÓN: la materia guarda solo el docente_id, no al docente."""
    MODELO = Materia
    ARCHIVO = "data/materias.json"
    NOMBRE = "materia"
    CAMPOS_BUSCABLES = ("nombre", "codigo")

    def __init__(self, docentes=None):
        super().__init__()
        self.docentes = docentes or DocenteController()

    def validar(self, datos, id_actual=None):
        # TODO 1: obligatorios cuando se crea
        if id_actual is None:
            error = faltantes_obligatorios(self.MODELO, datos)
            if error:
                return error

        # TODO 2: el código debe ser único
        if "codigo" in datos and str(datos["codigo"]).strip():
            codigo = str(datos["codigo"]).strip().upper()
            usados = {r["codigo"].upper() for r in self.registros()
                      if r["id"] != id_actual}
            if codigo in usados:
                return f"El código {codigo} ya está registrado"

        # TODO 3: si viene docente_id (no vacío), ese docente debe existir
        docente_id = datos.get("docente_id")
        if docente_id not in (None, "", "0", 0):
            try:
                docente_id = int(docente_id)
            except (TypeError, ValueError):
                return f"docente_id inválido: '{docente_id}'"
            if not self.docentes.existe(docente_id):
                return f"No existe un docente con id {docente_id}"
        return None

    def asignar_docente(self, materia_id, docente_id):
        if not self.existe(materia_id):
            return False, f"No existe materia con id {materia_id}"
        if not self.docentes.existe(docente_id):
            return False, f"No existe docente con id {docente_id}"
        return self.actualizar(materia_id, {"docente_id": docente_id})

    def materias_de_docente(self, docente_id):
        return [m for m in self.listar() if m.docente_id == docente_id]


# =====================================================================
class MatriculaController(CrudBase):
    """El equivalente académico del VentaController.

    ASOCIACIÓN con EstudianteController y MateriaController (los usa para
    validar), y COMPOSICIÓN con Nota (las notas viven dentro de la matrícula).
    """
    MODELO = Matricula
    ARCHIVO = "data/matriculas.json"
    NOMBRE = "matrícula"
    CAMPOS_BUSCABLES = ("periodo",)

    def __init__(self, estudiantes=None, materias=None):
        super().__init__()
        self.estudiantes = estudiantes or EstudianteController()
        self.materias = materias or MateriaController()

    # ---------- reglas ----------
    def validar(self, datos, id_actual=None):
        # Al actualizar, `datos` solo trae los campos que cambian: se
        # completa con lo que ya está guardado para validar la matrícula entera.
        if id_actual is None:
            error = faltantes_obligatorios(self.MODELO, datos)
            if error:
                return error
            completos = dict(datos)
        else:
            actual = next((r for r in self.registros() if r["id"] == id_actual), {})
            completos = {**actual, **datos}

        # TODO 1: el estudiante debe existir
        try:
            estudiante_id = int(completos.get("estudiante_id"))
        except (TypeError, ValueError):
            return "El estudiante_id debe ser un número"
        if not self.estudiantes.existe(estudiante_id):
            return f"No existe un estudiante con id {estudiante_id}"

        # TODO 2: la materia debe existir
        try:
            materia_id = int(completos.get("materia_id"))
        except (TypeError, ValueError):
            return "El materia_id debe ser un número"
        if not self.materias.existe(materia_id):
            return f"No existe una materia con id {materia_id}"

        # TODO 3: sin matrículas duplicadas (estudiante + materia + periodo)
        # El modelo usa "2026-1" si el periodo viene vacío: se compara igual.
        periodo = str(completos.get("periodo", "")).strip() or "2026-1"
        for r in self.registros():
            if (r["id"] != id_actual
                    and r["estudiante_id"] == estudiante_id
                    and r["materia_id"] == materia_id
                    and r["periodo"] == periodo):
                return (f"El estudiante {estudiante_id} ya está matriculado "
                        f"en la materia {materia_id} en el periodo {periodo}")
        return None

    #  notas (composición) 
    def agregar_nota(self, matricula_id, tipo, valor, peso=1):
        """Mismo patrón que VentaController: obtener -> usar el método del
        objeto -> atrapar ValueError -> volver a guardar el registro completo."""
        matricula = self.obtener(matricula_id)
        if matricula is None:
            return False, f"No existe {self.NOMBRE} con id {matricula_id}"

        try:
            nota = matricula.agregar_nota(tipo, valor, peso)
        except ValueError as excepcion:
            return False, str(excepcion)

        # El objeto vive en RAM: hay que persistirlo o la nota se pierde.
        # No se usa actualizar() porque las notas no están en CAMPOS.
        registros = self.registros()
        for indice, registro in enumerate(registros):
            if registro["id"] == matricula_id:
                registros[indice] = matricula.a_diccionario()
                break
        if not self._gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, (f"Nota agregada ({nota}). Promedio: {matricula.promedio} "
                      f"· {matricula.estado}")

    # reportes 
    def matriculas_de_estudiante(self, estudiante_id):
        return [m for m in self.listar() if m.estudiante_id == estudiante_id]

    def boletin(self, estudiante_id):
        """Texto del boletín: junta estudiante + matrículas + materias + notas."""
        estudiante = self.estudiantes.obtener(estudiante_id)
        if estudiante is None:
            return None

        matriculas = self.matriculas_de_estudiante(estudiante_id)
        lineas = [
            f"BOLETÍN · {estudiante.nombre_completo} (carnet {estudiante.carnet})",
            "-" * 56,
        ]
        if not matriculas:
            lineas.append("  Sin materias matriculadas.")
            return "\n".join(lineas)

        promedios = []
        for matricula in matriculas:
            materia = self.materias.obtener(matricula.materia_id)
            nombre = materia.nombre if materia else "materia eliminada"
            lineas.append(f"  {nombre} [{matricula.periodo}]")
            if matricula.notas:
                for nota in matricula.notas:
                    lineas.append(f"      - {nota} (peso {nota.peso:g})")
            lineas.append(f"      Promedio: {matricula.promedio:.2f}  "
                          f"→ {matricula.estado}")
            if matricula.notas:             # las "Sin notas" no cuentan
                promedios.append(matricula.promedio)

        lineas.append("-" * 56)
        if promedios:
            general = sum(promedios) / len(promedios)
            lineas.append(f"  PROMEDIO GENERAL: {general:.2f}  "
                          f"({len(promedios)} materia(s) con notas)")
        else:
            lineas.append("  PROMEDIO GENERAL: aún no hay notas registradas")
        return "\n".join(lineas)

    def reprobados(self):
        """Reporte polimórfico: estudiantes reprobados.

        Devuelve una lista de objetos (Matricula, Estudiante, Materia). Quien
        la imprima solo llama a str()/etiqueta(): cada clase se describe sola.
        """
        resultado = []
        for matricula in self.listar():
            if matricula.estado == "Reprobado":
                estudiante = self.estudiantes.obtener(matricula.estudiante_id)
                materia = self.materias.obtener(matricula.materia_id)
                resultado.append((matricula, estudiante, materia))
        return resultado
