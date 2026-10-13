# Tarea 1 · Parte 3 — Sistema académico (POO)

Estudiantes, docentes, materias, matrículas y notas, con los cuatro principios de la POO.

## Cómo ejecutarlo
```bash
python main_academico.py      # menú del sistema académico
python test_academico.py      # pruebas automáticas de todas las reglas (usa carpeta temporal)
python main.py                # (opcional) el sistema de ventas de la guía
```
Requiere Python 3.8+. Sin librerías externas. Ejecuta siempre desde esta carpeta (los JSON van en `data/`).

## Archivos
| Archivo | Qué contiene |
|---|---|
| `models.py` | `ModeloBase`, `Persona`, Cliente, Producto, Venta (de la guía) |
| `models_academico.py` | Estudiante, Docente, Materia, Nota, Matricula (de la guía + 1 corrección, ver abajo) |
| `views.py` | `CrudBase` (clase abstracta con el CRUD) + controladores de ventas |
| **`views_academico.py`** | **Los 4 controladores, todos heredan de `CrudBase`** |
| **`main_academico.py`** | **`MenuPrincipal` y `MenuMatriculas(MenuCRUD)`** |
| `shared/` | `GestorJSON` y funciones de consola |
| `docs/uml_academico.svg/.png` | **Diagrama UML** con relaciones y multiplicidad |
| `test_academico.py` | 37 comprobaciones |

## Reglas del negocio implementadas
- Carnet de estudiante único (sin distinguir mayúsculas) · email de docente único.
- Código de materia único · créditos entre 0 y 10 (en el modelo).
- No se asigna un docente inexistente (al crear, al actualizar y en `asignar_docente`).
- Estudiante y materia deben existir al matricular; sin matrícula duplicada (estudiante + materia + periodo,
  incluso cuando el periodo se deja vacío y toma el valor por defecto `2026-1`).
- Notas de 0 a 20, tipo ∈ {deber, lección, examen}, peso > 0.

## Decisiones de diseño
- `agregar_nota` no usa `actualizar()` porque `Matricula.CAMPOS` no incluye `notas`; guarda el registro
  completo con `a_diccionario()` (así la nota sobrevive al reiniciar).
- El validador de `Matricula` fusiona los cambios con el registro guardado, para validar bien en `actualizar`.
- Promedio general del boletín = media de los promedios de las materias **que ya tienen notas**.
- Reporte polimórfico elegido: **estudiantes reprobados** (menú Matrículas → 9). Solo usa `print()`/`etiqueta()`.
- En el UML, `Nota` es `0..*` (no `1..*`) porque el código permite una matrícula «Sin notas».

## Corrección al código entregado en la guía
`Nota.peso` usaba `float(valor or 1)`: un peso `0` se convertía en `1` sin error y la regla
«el peso debe ser > 0» nunca se ejecutaba. Ahora solo el valor vacío/None usa el peso por defecto.
