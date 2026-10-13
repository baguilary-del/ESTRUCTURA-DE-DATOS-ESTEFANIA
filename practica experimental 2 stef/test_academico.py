"""Prueba automática de las reglas del negocio (usa una carpeta temporal)."""
import os, shutil, tempfile, sys

carpeta = tempfile.mkdtemp()
shutil.copytree(os.path.dirname(os.path.abspath(__file__)), carpeta, dirs_exist_ok=True)
os.chdir(carpeta); sys.path.insert(0, carpeta)
shutil.rmtree("data", ignore_errors=True)

from views_academico import *

E_, D_ = EstudianteController(), DocenteController()
M_ = MateriaController(D_); T_ = MatriculaController(E_, M_)
ok = lambda r, esperado, msg: print(("PASA " if r[0] == esperado else "FALLA"), "-", msg, "→", r[1])

ok(E_.crear({"nombre":"ana","apellido":"pérez","email":"ana@x.com","carnet":"A001"}), True, "crear estudiante")
ok(E_.crear({"nombre":"luis","apellido":"mora","email":"luis@x.com","carnet":"a001"}), False, "carnet duplicado (case-insens.)")
ok(E_.crear({"nombre":"luis","apellido":"mora","email":"luis@x.com","carnet":"A002"}), True, "segundo estudiante")
ok(E_.crear({"nombre":"","apellido":"x","email":"x@x.com","carnet":"A003"}), False, "obligatorios estudiante")

ok(D_.crear({"nombre":"Rosa","apellido":"Vera","email":"rosa@u.edu","titulo":"Ing.","especialidad":"programación"}), True, "crear docente")
ok(D_.crear({"nombre":"Otra","apellido":"Vera","email":"ROSA@u.edu"}), False, "email docente duplicado")
ok(D_.crear({"nombre":"Sin","apellido":"Email","email":""}), False, "obligatorios docente")

ok(M_.crear({"nombre":"estructuras de datos","codigo":"ed1","creditos":"4","docente_id":"1"}), True, "crear materia con docente")
ok(M_.crear({"nombre":"otra","codigo":"ED1","creditos":"3"}), False, "código duplicado")
ok(M_.crear({"nombre":"otra","codigo":"BD1","creditos":"3","docente_id":"99"}), False, "docente inexistente")
ok(M_.crear({"nombre":"otra","codigo":"BD1","creditos":"11"}), False, "créditos fuera de 0-10")
ok(M_.crear({"nombre":"bases de datos","codigo":"BD1","creditos":"3"}), True, "materia sin docente")
ok(M_.asignar_docente(2, 1), True, "asignar_docente")
ok(M_.asignar_docente(2, 77), False, "asignar docente inexistente")
ok(M_.asignar_docente(88, 1), False, "asignar a materia inexistente")
print("materias de docente 1:", [m.codigo for m in M_.materias_de_docente(1)])

ok(T_.crear({"estudiante_id":1,"materia_id":1,"periodo":"2026-1"}), True, "matricular")
ok(T_.crear({"estudiante_id":1,"materia_id":1,"periodo":"2026-1"}), False, "matrícula duplicada")
ok(T_.crear({"estudiante_id":1,"materia_id":1}), False, "duplicada con periodo por defecto")
ok(T_.crear({"estudiante_id":1,"materia_id":1,"periodo":"2026-2"}), True, "mismo estudiante/materia, otro periodo")
ok(T_.crear({"estudiante_id":9,"materia_id":1}), False, "estudiante inexistente")
ok(T_.crear({"estudiante_id":1,"materia_id":9}), False, "materia inexistente")
ok(T_.crear({"estudiante_id":2,"materia_id":1}), True, "matricular estudiante 2")
ok(T_.crear({"estudiante_id":2,"materia_id":2}), True, "matricular estudiante 2 en BD")

ok(T_.agregar_nota(1,"deber",18,1), True, "nota deber")
ok(T_.agregar_nota(1,"examen",15,2), True, "nota examen")
assert T_.obtener(1).promedio == 16.0, "promedio ponderado (18*1+15*2)/3 = 16"
print("PASA - promedio ponderado = 16.0")
ok(T_.agregar_nota(1,"examen",21,1), False, "nota > 20")
ok(T_.agregar_nota(1,"examen",-1,1), False, "nota < 0")
ok(T_.agregar_nota(1,"proyecto",10,1), False, "tipo inválido")
ok(T_.agregar_nota(1,"examen","abc",1), False, "nota no numérica")
ok(T_.agregar_nota(1,"examen",10,0), False, "peso 0")
ok(T_.agregar_nota(50,"examen",10,1), False, "matrícula inexistente")
ok(T_.agregar_nota(3,"examen",8,1), True, "nota baja (est.2)")

# persistencia: un controlador NUEVO lee del archivo (simula reiniciar el programa)
T2 = MatriculaController(EstudianteController(), MateriaController(DocenteController()))
assert len(T2.obtener(1).notas) == 2 and T2.obtener(1).promedio == 16.0
print("PASA - las notas sobreviven al reinicio (persistencia)")

# actualizar no borra las notas
ok(T_.actualizar(1, {"periodo": "2027-1"}), True, "actualizar periodo")
assert len(T_.obtener(1).notas) == 2; print("PASA - actualizar conserva las notas")
ok(T_.actualizar(1, {"periodo": "2026-2"}), False, "actualizar a periodo duplicado")

print(); print(T_.boletin(1)); print(); print(T_.boletin(2)); print()
print("boletín inexistente:", T_.boletin(99))
for m, e, ma in T_.reprobados(): print("REPROBADO:", e, "|", ma, "|", m)
import json; print(json.dumps(json.load(open("data/matriculas.json"))[0], ensure_ascii=False, indent=1))
