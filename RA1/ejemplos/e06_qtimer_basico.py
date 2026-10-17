"""E06. Una etiqueta periódica. Necesita PySide6; no crea procesos."""
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLabel, QPushButton, QLineEdit)


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E06 - Aprende QTimer")
        self.ticks = 0
        self.etiqueta = QLabel("Avisos recibidos: 0")
        iniciar = QPushButton("Iniciar")
        parar = QPushButton("Detener")
        campo = QLineEdit()
        campo.setPlaceholderText("Escribe mientras avanza la etiqueta")
        layout = QVBoxLayout(self)
        for widget in (self.etiqueta, iniciar, parar, campo):
            layout.addWidget(widget)
        self.timer = QTimer(self)
        self.timer.setInterval(500)  # Milisegundos; no es un reloj exacto.
        self.timer.timeout.connect(self.actualizar)
        iniciar.clicked.connect(lambda: self.timer.start())
        parar.clicked.connect(self.timer.stop)

    def actualizar(self):
        self.ticks += 1
        self.etiqueta.setText(f"Avisos recibidos: {self.ticks}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())
