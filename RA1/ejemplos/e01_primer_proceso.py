"""E01. Ejecuta: python e01_primer_proceso.py (archivo, no consola interactiva)."""
import multiprocessing as mp
import os


def saludar(nombre):
    print(f"Hijo: {os.getpid()}; padre: {os.getppid()}", flush=True)
    print(f"Hola, {nombre}", flush=True)


if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=saludar, args=("Ana",)) #saludar(ana)
    print(f"Principal: {os.getpid()}", flush=True)
    p.start()
    p.join()  # Haceos esperar al padre
    print(f"Código de salida: {p.exitcode}")
    p.close()  # Libera el objeto; no detiene un proceso activo.
