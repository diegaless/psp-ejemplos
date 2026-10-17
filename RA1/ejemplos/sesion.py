"""Controlador de ejemplo, SIN Qt y sin hilos programados por el alumno.
El principal debe llamar a leer() periódicamente y consumir lo devuelto.
No es la solución final: recibe textos, no carpetas, ni guarda informes.
"""
import multiprocessing as mp
from queue import Empty
from time import monotonic
from uuid import uuid4
from trabajadores import analizar_textos


class SesionTextos:
    def __init__(self):
        self.activa = False
        self.procesos = []
        self.resumen = None

    def iniciar(self, textos, n=2, demora=0.0, fallo=False,
                limite=20.0):
        if self.activa:
            raise RuntimeError("Ya hay un análisis activo.")
        if n < 1 or limite <= 0 or demora < 0:
            raise ValueError("Parámetros de ejecución no válidos.")
        datos = list(enumerate(textos))
        self.ctx = mp.get_context("spawn")
        self.cola = self.ctx.Queue()
        self.parada = self.ctx.Event()
        self.identificador = uuid4().hex
        self.esperados = len(datos)
        self.recibidos = {}
        self.fines = set()
        self.procesos = []
        self.resumen = None
        self.error = ""
        self.descartar_cola = False
        self.fuerza = 0
        self.inicio = monotonic()
        self.plazo = self.inicio + limite
        self.activa = True
        n = min(n, len(datos))
        for i in range(n):
            p = self.ctx.Process(
                target=analizar_textos,
                args=(datos[i::n], self.cola, self.parada,
                      self.identificador, demora, fallo and i == 0))
            try:
                p.start()
            except Exception as error:
                self.error = f"No se pudo iniciar un trabajador: {error}"
                p.close()
                self.cancelar()
                break
            self.procesos.append(p)

    def cancelar(self):
        if self.activa:
            self.parada.set()
            self.plazo = min(self.plazo, monotonic() + 3.0)

    def leer(self):
        """Una vuelta breve: máximo 20 mensajes; nunca espera a un hijo."""
        if not self.activa:
            return []
        eventos = []
        agotada = self.descartar_cola
        if not self.descartar_cola:
            for _ in range(20):
                try:
                    mensaje = self.cola.get_nowait()
                except Empty:
                    agotada = True
                    break
                except (OSError, EOFError, ValueError) as error:
                    self.error = f"Fallo de comunicación: {error}"
                    self.descartar_cola = True
                    agotada = True
                    self.cancelar()
                    break
                if mensaje.get("analisis") != self.identificador:
                    continue
                if mensaje["tipo"] == "fin":
                    self.fines.add(mensaje["pid"])
                elif mensaje["tipo"] == "resultado":
                    self.recibidos[mensaje["id"]] = mensaje
                eventos.append(mensaje)
        vivos = [p for p in self.procesos if p.is_alive()]
        caidos = [p for p in self.procesos
                  if p.exitcode is not None and p.exitcode != 0]
        if caidos and not self.error:
            self.error = "Un trabajador terminó con error. Análisis incompleto."
            self.cancelar()
        ahora = monotonic()
        if vivos and ahora >= self.plazo:
            # Tras forzar, no leer: la cola puede quedar dañada.
            self.error = self.error or "Tiempo excedido; cierre forzado."
            self.descartar_cola = True
            self.parada.set()
            if self.fuerza == 0:
                for p in vivos:
                    p.terminate()
                self.fuerza = 1
                self.plazo = ahora + 2.0
            else:
                for p in vivos:
                    p.kill()
                self.fuerza = 2
                self.plazo = ahora + 2.0
            return eventos  # Esperamos confirmación del SO en otro turno.
        if vivos or not agotada:
            return eventos
        codigos = [p.exitcode for p in self.procesos]
        fin_correcto = len(self.fines) == len(self.procesos)
        completos = len(self.recibidos) == self.esperados
        if self.error or any(c != 0 for c in codigos) or not fin_correcto:
            estado = "error"
        elif self.parada.is_set():
            estado = "cancelado"
        elif completos:
            estado = "completado"
        else:
            estado = "error"
            self.error = "Faltan resultados aunque los procesos terminaron."
        self.resumen = {"tipo": "resumen", "estado": estado,
                        "recibidos": len(self.recibidos),
                        "esperados": self.esperados,
                        "codigos": codigos, "error": self.error}
        for p in self.procesos:
            p.join(timeout=0)
            p.close()
        self.cola.close()
        self.cola.join_thread()  # Solo los hijos han hecho put().
        self.activa = False
        eventos.append(self.resumen)
        return eventos
