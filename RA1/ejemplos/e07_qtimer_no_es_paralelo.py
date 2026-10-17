"""E07. ANTIPATRÓN CONTROLADO: muestra por qué QTimer no evita un bloqueo.
No copies sleep() en una ventana real. La demostración bloquea 2 segundos.
"""
import sys
from time import sleep
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QPushButton
from e06_qtimer_basico import Ventana


class VentanaBloqueo(Ventana):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E07 - Demostración de un bloqueo")
        boton = QPushButton("Provocar bloqueo de 2 segundos")
        self.layout().addWidget(boton)
        boton.clicked.connect(self.programar_bloqueo)
        self.timer.start()

    def programar_bloqueo(self):
        # Diferir no significa ejecutar en paralelo.
        QTimer.singleShot(100, self.bloquear)

    def bloquear(self):
        sleep(2)  # A propósito: deja de atender escritura y temporizadores.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBloqueo()
    ventana.show()
    sys.exit(app.exec())
