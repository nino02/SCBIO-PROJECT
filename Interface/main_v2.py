import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTimeEdit, QPushButton, QLabel, QHBoxLayout, QDialog, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap

class TimeSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Carga el icono directamente
        icono = QtGui.QIcon("Icono\\icon.png")  # Reemplaza "ruta/al/icono.png" con la ruta real del archivo
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
        self.close()
        hour = float(self.hour_edit.time().toString("HH"))
        minute = float(self.minute_edit.time().toString("mm"))
        avatar_window = AvatarWindow(hour*3600+minute*60)
        avatar_window.run()
    

    def print_time(self):
        hour = self.hour_edit.time().toString("HH")
        minute = self.minute_edit.time().toString("mm")
        print("Tiempo objetivo seleccionado:", hour + ":" + minute)

class AvatarWindow:
    def __init__(self,time):
        self.time_s = time
        self.root = tk.Tk()
        self.root.title("Avatar")
        self.root.attributes("-topmost", True)  # Para mantener la ventana siempre en primer plano

        #Configuracion de numero de niveles
        self.levels = 4
        self.current_level = 0

        # Configuración de la ventana
        self.root.overrideredirect(True)  # Ocultar bordes de la ventana

        # Cargar las imágenes del avatar
        self.avatar_images = [Image.open(f"avatares\\avatar{i}.png") for i in range(1, 6)]  # Cambia "avatar_" por la ruta de tus imágenes
        self.avatar_index = 0
        self.avatar_label = tk.Label(self.root)
        self.avatar_label.pack()

        # Mover la ventana a la esquina de la pantalla
        screen_width, screen_height = pyautogui.size()
        self.root.geometry(f"128x128+{screen_width-128}+{screen_height-128}")

        # Iniciar la animación del avatar
        self.timer()

        # Enlazar evento de doble clic al avatar
        self.avatar_label.bind("<Double-Button-1>", self.open_close_window)

    def timer(self):
        tiempo_rep = self.time_s/self.levels
        print(f"Temporizador: {self.current_level} {self.time_s} {tiempo_rep}")
        if (self.premio()):
            if(self.current_level == self.levels):
                None
            else:
                self.current_level = self.current_level + 1
                self.change_avatar(self.current_level)
                
        else:
            if(self.current_level == 1):
                None
            else:
                self.current_level = self.current_level - 1
                self.change_avatar(self.current_level)
                
        self.root.after(int(tiempo_rep)*1000, self.timer)  # Llamar a esta función nuevamente después de 1000 milisegundos (1 segundo)

    def premio(self):
        return True
    
    def change_avatar(self,level):
        self.avatar_index = level
        avatar_image = self.avatar_images[self.avatar_index]
        avatar_image = ImageTk.PhotoImage(avatar_image)
        self.avatar_label.configure(image=avatar_image)
        self.avatar_label.image = avatar_image  # Guardar una referencia para evitar que la imagen se elimine por el recolector de basura
        return
    

    def open_close_window(self, event):
        if hasattr(self, "popup"):
            self.popup.destroy()  # Si ya hay una ventana abierta, ciérrala
            del self.popup  # Elimina la referencia

        else:
            # Abre una nueva ventana con texto
            self.popup = tk.Toplevel(self.root)
            self.popup.title("Cerrar programa")
            self.popup.attributes("-topmost", True)

            label = tk.Label(self.popup, text=f"¿Deseas cerrar el programa?", padx=20, pady=10)
            label.pack()

            button = tk.Button(self.popup, text="Cerrar", command=self.close_program)
            button.pack()

    def close_program(self):
        self.root.destroy()  # Cierra la ventana principal y termina el programa
        

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimeSelector()
    window.show()
    sys.exit(app.exec_())
    
