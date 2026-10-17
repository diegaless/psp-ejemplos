"""Funciones importables sin objetos de Qt. Compartidas por E05 y E08."""
import os
import re
from time import perf_counter


def contar_texto(texto):
    """Regla de la práctica V5: palabras Unicode y caracteres, no bytes."""
    if not isinstance(texto, str):
        raise TypeError("Se esperaba un texto (str).")
    return len(re.findall(r"\b\w+\b", texto)), len(texto)


def analizar_textos(lote, salida, cancelar, analisis, demora=0.0,
                    fallo=False):
    """Cada lote contiene pares (id, texto). La demora es SOLO demostrativa."""
    pid = os.getpid()
    try:
        if fallo:
            raise RuntimeError("Caída simulada para comprobar exitcode.")
        for identificador, texto in lote:
            if cancelar.is_set():
                break
            # Permite observar la cancelación. En trabajo real: demora=0.
            if demora and cancelar.wait(demora):
                break
            inicio = perf_counter()
            mensaje = {"tipo": "resultado", "analisis": analisis,
                       "id": identificador, "pid": pid}
            try:
                palabras, caracteres = contar_texto(texto)
                mensaje.update(estado="correcto", palabras=palabras,
                               caracteres=caracteres)
            except (TypeError, ValueError) as error:
                mensaje.update(estado="error", error=str(error))
            mensaje["duracion_ms"] = (perf_counter() - inicio) * 1000
            salida.put(mensaje)
    finally:
        salida.put({"tipo": "fin", "analisis": analisis, "pid": pid})
