import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer, QTime

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reloj Digital")
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        # Crear el widget QLCDNumber para mostrar la hora
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)  # Establecer el número de dígitos para mostrar la hora
        self.lcd.setSegmentStyle(QLCDNumber.Flat)  # Establecer el estilo del segmento LCD

        layout.addWidget(self.lcd)
        self.setLayout(layout)

        # Crear un temporizador para actualizar la hora cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

        # Actualizar la hora inicial
        self.update_time()

    def update_time(self):
        # Obtener la hora actual del sistema
        current_time = QTime.currentTime()

        # Formatear la hora como una cadena en formato HH:mm:ss
        time_text = current_time.toString("hh:mm:ss")

        # Mostrar la hora en el widget QLCDNumber
        self.lcd.display(time_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
