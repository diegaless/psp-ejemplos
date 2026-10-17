"""E08. Puente completo: 2 procesos + Queue + Event + QTimer.
Reutiliza trabajadores.py y sesion.py, explicados antes en E05.
No analiza carpetas ni guarda informes: todavía NO es la práctica final.
"""
import multiprocessing as mp
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QPushButton, QLineEdit, QPlainTextEdit)
from sesion import SesionTextos


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E08 - Ventana y dos procesos")
        self.resize(760, 460)
        self.sesion = SesionTextos()
        self.cierre_pendiente = False
        self.estado = QLabel("Preparado")
        self.iniciar = QPushButton("Analizar textos de demostración")
        self.cancelar = QPushButton("Cancelar")
        self.cancelar.setEnabled(False)
        self.campo = QLineEdit()
        self.campo.setPlaceholderText("Escribe mientras los hijos trabajan")
        self.registro = QPlainTextEdit()
        self.registro.setReadOnly(True)
        layout = QVBoxLayout(self)
        for widget in (self.estado, self.iniciar, self.cancelar,
                       self.campo, self.registro):
            layout.addWidget(widget)
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.consultar)
        self.iniciar.clicked.connect(self.arrancar)
        self.cancelar.clicked.connect(self.pedir_parada)

    def arrancar(self):
        if self.sesion.activa:
            return
        textos = ["Hola, clase", "acción útil", "", None,
                  "uno dos tres", "último texto"]
        try:
            self.sesion.iniciar(textos, demora=0.4)
        except Exception as error:
            self.estado.setText(f"No se pudo preparar el análisis: {error}")
            return
        self.registro.clear()
        self.estado.setText("Analizando... Puedes escribir abajo.")
        self.iniciar.setEnabled(False)
        self.cancelar.setEnabled(True)
        self.timer.start()

    def pedir_parada(self):
        self.sesion.cancelar()
        self.cancelar.setEnabled(False)
        self.estado.setText("Cancelación solicitada; recogiendo procesos...")

    def consultar(self):
        for mensaje in self.sesion.leer():
            self.registro.appendPlainText(str(mensaje))
        if self.sesion.activa:
            return
        self.timer.stop()
        self.cancelar.setEnabled(False)
        self.iniciar.setEnabled(True)
        resumen = self.sesion.resumen
        self.estado.setText(f"Estado: {resumen['estado']}; "
                           f"revisados: {resumen['recibidos']}")
        if self.cierre_pendiente:
            self.close()

    def closeEvent(self, evento):
        if self.sesion.activa:
            self.cierre_pendiente = True
            self.pedir_parada()
            evento.ignore()  # La ventana continúa viva y su timer sigue consultando.
        else:
            evento.accept()


if __name__ == "__main__":
    mp.freeze_support()  # Preparación habitual si después se empaqueta.
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
