"""E02. python e02_dos_procesos.py juntos | separados
No es el benchmark final: textos sintéticos para observar dos ejecuciones.
"""
import multiprocessing as mp
import os
import re
import sys
from time import perf_counter


def contar(nombre, texto):
    inicio = perf_counter()
    total = len(re.findall(r"\b\w+\b", texto))
    fin = perf_counter()
    print(f"{nombre}: PID={os.getpid()}, palabras={total}, "
          f"inicio={inicio:.6f}, fin={fin:.6f}", flush=True)


if __name__ == "__main__": 
    modo = sys.argv[1] if len(sys.argv) > 1 else "juntos"
    if modo not in {"juntos", "separados"}:
        raise SystemExit("Usa juntos o separados.")
    ctx = mp.get_context("spawn")
    entradas = [("A", "uno dos " * 100_000),
                ("B", "tres cuatro " * 100_000)]
    procesos = [ctx.Process(target=contar, args=datos)
                for datos in entradas]
    inicio = perf_counter()
    for p in procesos:
        p.start()
        if modo == "separados":
            p.join()  # El segundo no arranca hasta que acaba el primero.
    for p in procesos:
        p.join()  # En juntos, ambos ya están iniciados.
        if p.exitcode != 0:
            raise RuntimeError(f"El trabajador terminó con {p.exitcode}")
        p.close()
    print(f"Modo {modo}; tiempo total: {perf_counter() - inicio:.3f} s")
