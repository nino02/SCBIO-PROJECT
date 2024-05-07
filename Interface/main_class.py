import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTimeEdit, QPushButton, QLabel, QHBoxLayout, QDialog, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap


class AvatarWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Avatar')
        self.setGeometry(800, 100, 200, 200)

        layout = QVBoxLayout()

        # Etiqueta para el avatar
        avatar_label = QLabel(self)
        pixmap = QPixmap('avatares\\avatar2.png')  # Ajusta la ruta de la imagen según la ubicación de tu archivo de avatar
        avatar_label.setPixmap(pixmap)
        layout.addWidget(avatar_label)

        self.setLayout(layout)


class TimeSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

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

    def show_avatar_window(self):
        self.hide()
        self.avatar_window = AvatarWindow()
        self.avatar_window.exec_()

    def print_time(self):
        hour = self.hour_edit.time().toString("HH")
        minute = self.minute_edit.time().toString("mm")
        print("Tiempo objetivo seleccionado:", hour + ":" + minute)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimeSelector()
    window.show()
    sys.exit(app.exec_())
