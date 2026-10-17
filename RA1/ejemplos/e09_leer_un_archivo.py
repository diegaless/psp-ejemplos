"""E09. La misma regla de conteo, ahora aplicada a un archivo real.
python e09_leer_un_archivo.py ../datos_prueba/01_saludo.txt
"""
from pathlib import Path
import sys
from trabajadores import contar_texto


def leer_y_contar(ruta):
    with Path(ruta).open("r", encoding="utf-8", newline=None) as fichero:
        texto = fichero.read()
    return contar_texto(texto)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Indica la ruta del .txt entre comillas.")
    try:
        palabras, caracteres = leer_y_contar(sys.argv[1])
        print(f"Palabras: {palabras}; caracteres: {caracteres}")
    except (OSError, UnicodeError) as error:
        print(f"Error de lectura: {error}", file=sys.stderr)
        raise SystemExit(1)
