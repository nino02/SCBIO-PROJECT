import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QTimeEdit, QDialog
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QTimer


class AvatarWindow(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time_s = time

        # Configuración de la ventana principal
        self.setWindowTitle("Avatar")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Sin bordes y siempre en primer plano
        screen_width, screen_height = pyautogui.size()
        self.move(screen_width - 128, screen_height - 128)
        self.resize(128, 128)

        # Cargar el GIF del avatar
        self.avatar_gif = QMovie("avatar.gif")
        self.avatar_label = QLabel()
        self.avatar_label.setMovie(self.avatar_gif)

        # Crear un layout vertical y agregar widgets
        layout = QVBoxLayout()
        layout.addWidget(self.avatar_label)
        self.setLayout(layout)

        # Iniciar la animación del avatar
        self.avatar_gif.start()

        # Iniciar el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_bucle)
        tiempo_rep = self.time_s // 4  # 4 niveles por defecto
        self.timer.start(tiempo_rep * 1000)

    def timer_bucle(self):
        print("Ha entrado al bucle")

    def premio(self):
        return True


class TimeSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Carga el icono directamente
        icono = QIcon("Icono\\icon.png")  # Reemplaza "ruta/al/icono.png" con la ruta real del archivo
        # Establece el icono de la ventana
        self.setWindowIcon(icono)

    def init_ui(self):
        self.setWindowTitle('Selector de Tiempo Objetivo')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        # Etiqueta para "Tiempo objetivo"
        title_label = QLabel("<h2>Tiempo objetivo</h2>")
        layout.addWidget(title_label)

        # Layout horizontal para "Horas" y "Minutos"
        time_layout = QHBoxLayout()

        # Etiqueta y selector de horas
        hour_label = QLabel("Horas:")
        self.hour_edit = QTimeEdit(self)
        self.hour_edit.setDisplayFormat("HH")
        time_layout.addWidget(hour_label)
        time_layout.addWidget(self.hour_edit)

        # Etiqueta y selector de minutos
        minute_label = QLabel("Minutos:")
        self.minute_edit = QTimeEdit(self)
        self.minute_edit.setDisplayFormat("mm")
        time_layout.addWidget(minute_label)
        time_layout.addWidget(self.minute_edit)

        layout.addLayout(time_layout)

        # Botón de aceptar
        ok_button = QPushButton('Aceptar', self)
        ok_button.clicked.connect(self.show_avatar_window)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        # Centrar la ventana en la pantalla
        screen_width, screen_height = pyautogui.size()
        window_width, window_height = self.width(), self.height()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        self.move(center_x, center_y)

    def show_avatar_window(self):
        hour = float(self.hour_edit.time().toString("HH"))
        minute = float(self.minute_edit.time().toString("mm"))
        self.hide()
        avatar_window = AvatarWindow(int(hour * 3600 + minute * 60))
        avatar_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimeSelector()
    window.show()
    sys.exit(app.exec_())
