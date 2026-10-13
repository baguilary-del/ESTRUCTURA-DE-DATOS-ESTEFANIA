"""Funciones de consola compartidas por todos los menús."""


def imprimir_titulo(texto):
    print("\n" + "=" * 50)
    print(f"  {texto}")
    print("=" * 50)


def imprimir_exito(mensaje):
    print(f"✅ {mensaje}")


def imprimir_error(mensaje):
    print(f"❌ {mensaje}")


def imprimir_info(mensaje):
    print(f"ℹ️  {mensaje}")


def confirmar(pregunta):
    return input(f"{pregunta} (s/n): ").strip().lower() in ("s", "si", "sí")
