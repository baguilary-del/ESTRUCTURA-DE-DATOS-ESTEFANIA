"""Persistencia en archivos JSON (idéntico en espíritu al de la parte 2)."""
import json
import os


class GestorJSON:
    """Lee y escribe una lista de diccionarios en un archivo JSON."""

    def __init__(self, ruta):
        self._ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

    def leer(self):
        if not os.path.exists(self._ruta):
            return []
        try:
            with open(self._ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                return json.loads(contenido) if contenido else []
        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, registros):
        try:
            with open(self._ruta, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False
