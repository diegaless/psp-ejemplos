"""E04. El resultado vuelve por Queue, no por return ni por join."""
import multiprocessing as mp
import os
import re
from queue import Empty


def contar(texto, salida):
    salida.put({"palabras": len(re.findall(r"\b\w+\b", texto)),
                "caracteres": len(texto), "pid": os.getpid()})


if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    salida = ctx.Queue()
    p = ctx.Process(target=contar, args=("Hola, clase", salida))
    p.start()
    try:
        resultado = salida.get(timeout=5)  # Espera limitada: solo consola.
        print("Recibido:", resultado)
        p.join(timeout=5)  # Primero consumir; después esperar al productor.
        if p.is_alive() or p.exitcode != 0:
            raise RuntimeError("El trabajador no terminó correctamente.")
    except Empty:
        print("No se recibió el resultado dentro de 5 segundos.")
    finally:
        if p.is_alive():
            p.terminate()  # Rescate de esta demo; NO es cancelar normalmente.
            p.join(timeout=2)
        if p.is_alive():
            p.kill()
            p.join(timeout=2)
        if p.is_alive():
            raise RuntimeError("El SO no confirmó la parada del trabajador.")
        p.close()
        salida.close()  # No reutilizar esta cola después de una terminación forzada.
        salida.join_thread()  # El principal no ha escrito: no tiene hilo emisor.
