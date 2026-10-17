"""E05. python e05_lotes_y_cancelacion.py [--cancelar] [--fallo]
La pausa hace visible la parada: no se usa para medir rendimiento.
"""
import argparse
from time import sleep
from sesion import SesionTextos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cancelar", action="store_true")
    parser.add_argument("--fallo", action="store_true")
    opciones = parser.parse_args()
    sesion = SesionTextos()
    textos = ["Hola, clase", "acción útil", "", None,
              "uno dos tres", "último texto"]
    sesion.iniciar(textos, demora=0.3, fallo=opciones.fallo)
    solicitada = False
    while sesion.activa:
        for mensaje in sesion.leer():
            print(mensaje, flush=True)
        if opciones.cancelar and len(sesion.recibidos) >= 2 and not solicitada:
            sesion.cancelar()
            solicitada = True
            print("Parada solicitada; falta recoger a los hijos.")
        sleep(0.03)  # Solo consola. E08 sustituye este bucle por QTimer.
