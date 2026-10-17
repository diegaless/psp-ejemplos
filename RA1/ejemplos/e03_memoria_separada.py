"""E03. Una lista normal enviada al hijo no es una lista compartida."""
import multiprocessing as mp


def modificar(datos):
    datos.append("hijo")
    print("Dentro del hijo:", datos, flush=True)


if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    lista = ["principal"]
    p = ctx.Process(target=modificar, args=(lista,))
    p.start()
    p.join()
    print("En el principal:", lista)
    print("Código de salida:", p.exitcode)
    p.close()
