import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QTimeEdit, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer


class AvatarWindow(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time_s = time

        # Configuración de la ventana principal
        self.setWindowTitle("Avatar")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Sin bordes y siempre en primer plano
        screen_width, screen_height = pyautogui.size()
        self.move(screen_width-128, screen_height-128)
        self.resize(128,128)

        # Configuración de número de niveles
        self.levels = 4
        self.current_level = 0

        # Cargar las imágenes del avatar
        self.avatar_images = [f"avatares/avatar{i}.png" for i in range(1, 6)]  # Cambia "avatar" por la ruta de tus imágenes
        self.avatar_label = QLabel()

        # Crear un layout vertical y agregar widgets
        layout = QVBoxLayout()
        layout.addWidget(self.avatar_label)
        self.setLayout(layout)

        # Iniciar la animación del avatar
        self.timer_bucle()

        # Enlazar eventos de ratón
        self.enterEvent = self.on_enter
        self.leaveEvent = self.on_leave
        self.mouseDoubleClickEvent = self.on_doubleclic

        # Iniciar el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_bucle)
        tiempo_rep = self.time_s // self.levels
        self.timer.start(tiempo_rep*1000)

    def on_doubleclic(self,event):
        # Mostrar una ventana de diálogo con un mensaje de prueba y un botón para cerrar
        message_dialog = QDialog(self)
        message_dialog.setWindowTitle("Mensaje de Prueba")
        message_label = QLabel("Hola, este mensaje es de prueba")
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(QApplication.quit)  # Cierra la aplicación entera
        layout = QVBoxLayout()
        layout.addWidget(message_label)
        layout.addWidget(close_button)
        message_dialog.setLayout(layout)
        message_dialog.exec_()

    def timer_bucle(self):
        print(f"Ha entrado al bucle {self.current_level}")
        if self.premio():
            if self.current_level == self.levels:
                None
            else:
                self.change_avatar(self.current_level)
                self.current_level += 1
                
        else:
            if self.current_level == 1:
                None
            else:
                self.current_level -= 1
                self.change_avatar(self.current_level)

        # Llamar a esta función nuevamente después de 1000 milisegundos (1 segundo)
        #self.timerId = self.startTimer(int(tiempo_rep) * 1000)

    def premio(self):
        return True

    def change_avatar(self, level):
        avatar_image_path = self.avatar_images[level]
        avatar_pixmap = QPixmap(avatar_image_path)
        self.avatar_label.setPixmap(avatar_pixmap)

    def on_enter(self, event):
        # Cambiar la opacidad de la ventana al 80% cuando el ratón está encima
        self.setWindowOpacity(0.4)

    def on_leave(self, event):
        # Restaurar la opacidad de la ventana al 100% cuando el ratón sale
        self.setWindowOpacity(1)


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
        avatar_window = AvatarWindow(int(hour*3600+minute*60))
        avatar_window.show()

    def print_time(self):
        hour = self.hour_edit.time().toString("HH")
        minute = self.minute_edit.time().toString("mm")
        print("Tiempo objetivo seleccionado:", hour + ":" + minute)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimeSelector()
    window.show()
    sys.exit(app.exec_())
