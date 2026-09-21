class Tareas:
    def __init__(self):
        self.tareas = []

    def agregar_tareas(self, descripcion, prioridad):
        tarea = (descripcion, prioridad.lower())
        self.tareas.append(tarea)

    def tareas_prio(self):
        resultado = []
        for desc, prio in self.tareas:
            if prio == 'alta':
                resultado.append((desc, prio))

    def eliminar_completada(self, descripcion):
        for tarea in self.tareas:
            if tarea[0] == descripcion:
                self.tareas.remove(tarea)
                return True
        return False

if __name__ == '__main__':
    tareas = Tareas()
    print(tareas.tareas_prio())
    print(tareas.eliminar_completada('alta'))
    tareas.agregar_tareas('hecer un codigo', 'alta')
    print(tareas.tareas)