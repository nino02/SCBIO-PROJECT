import tkinter as tk
from PIL import Image, ImageTk
import pyautogui

class AvatarWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Avatar")
        self.root.attributes("-topmost", True)  # Para mantener la ventana siempre en primer plano

        # Configuración de la ventana
        self.root.overrideredirect(True)  # Ocultar bordes de la ventana
        self.root.attributes("-alpha", 0.7)  # Establecer la transparencia (0.0 - completamente transparente, 1.0 - opaco)

        # Cargar las imágenes del avatar
        self.avatar_images = [Image.open(f"avatares\\avatar{i}.png") for i in range(2, 4)]  # Cambia "avatar_" por la ruta de tus imágenes
        self.avatar_index = 0
        self.avatar_label = tk.Label(self.root)
        self.avatar_label.pack()

        # Mover la ventana a la esquina de la pantalla
        screen_width, screen_height = pyautogui.size()
        self.root.geometry(f"100x100+{screen_width-110}+{screen_height-110}")

        # Iniciar la animación del avatar
        self.animate_avatar()

        # Enlazar evento de doble clic al avatar
        self.avatar_label.bind("<Double-Button-1>", self.open_close_window)

    def animate_avatar(self):
        # Cambiar la imagen del avatar cada 1 segundo
        self.avatar_index = (self.avatar_index + 1) % len(self.avatar_images)
        avatar_image = self.avatar_images[self.avatar_index]
        avatar_image = ImageTk.PhotoImage(avatar_image)
        self.avatar_label.configure(image=avatar_image)
        self.avatar_label.image = avatar_image  # Guardar una referencia para evitar que la imagen se elimine por el recolector de basura
        self.root.after(1000, self.animate_avatar)  # Llamar a esta función nuevamente después de 1000 milisegundos (1 segundo)

    def open_close_window(self, event):
        if hasattr(self, "popup"):
            self.popup.destroy()  # Si ya hay una ventana abierta, ciérrala
            del self.popup  # Elimina la referencia

        else:
            # Abre una nueva ventana con texto
            self.popup = tk.Toplevel(self.root)
            self.popup.title("Cerrar programa")
            self.popup.attributes("-topmost", True)
            self.popup.attributes("-alpha", 0.9)

            label = tk.Label(self.popup, text="¿Deseas cerrar el programa?", padx=20, pady=10)
            label.pack()

            button = tk.Button(self.popup, text="Cerrar", command=self.close_program)
            button.pack()

    def close_program(self):
        self.root.destroy()  # Cierra la ventana principal y termina el programa

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    avatar_window = AvatarWindow()
    avatar_window.run()
