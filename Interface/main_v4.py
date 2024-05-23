import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QTimeEdit, QDialog,QLCDNumber,QGridLayout
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize, QTime, QThread, pyqtSignal 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2
import numpy as np
import mediapipe as mp
import time

class EyeDetectionThread(QThread):
    result_signal = pyqtSignal(dict)
    
    def run(self):
        result = eyedetection()
        self.result_signal.emit(result)

def eyedetection():
    # MediaPipe Face Detection initialization
    mp_face_detection = mp.solutions.face_detection

    face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    # For drawing the results
    mp_drawing = mp.solutions.drawing_utils

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

    # Load YOLO
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Load COCO names
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Load Haar cascade for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Set a lower frame rate to reduce CPU usage
    #cap.set(cv2.CAP_PROP_FPS, 1)  # Set frame rate to 10 FPS

    # Dictionary to track object detection durations
    object_durations = {}
    start_time = time.time()
    previous_time = start_time

    frame_counter = 0
    while cap.isOpened() and time.time() - start_time < 120:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_start_time = time.time()

        # Convert color from BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_counter += 1

        # Skip processing for every other frame
        if frame_counter % 30 != 1:
            continue


        # Perform face detection
        results = face_detection.process(image)

        # Convert back to BGR for display
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Perform object detection with YOLO
        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Information to show on screen
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        current_time = time.time()
        detected_objects = set()

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                detected_objects.add(label)
                color = (0, 255, 0)
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Update object detection durations
        for label in detected_objects:
            if label not in object_durations:
                object_durations[label] = 0
            object_durations[label] += current_time - previous_time

        # Draw face detection results and perform eye detection
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection, drawing_spec)
                detected_objects.add('face')

                # Extract face bounding box
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                (x, y, w, h) = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                                int(bboxC.width * iw), int(bboxC.height * ih))
                roi_gray = frame[y:y + h, x:x + w]
                roi_color = image[y:y + h, x:x + w]

                # Eye detection
                eyes = eye_cascade.detectMultiScale(roi_gray)
                eye_labels = ['left eye', 'right eye']
                for i, (ex, ey, ew, eh) in enumerate(eyes):
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
                    eye_label = eye_labels[i % 2]  # Alternate between left and right eye
                    detected_objects.add(eye_label)
                    if eye_label not in object_durations:
                        object_durations[eye_label] = 0
                    object_durations[eye_label] += current_time - previous_time

        # Display the image
        cv2.imshow('MediaPipe Face, Eye Detection and YOLOv3 Object Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

        previous_time = current_time  # Reset previous_time for the next frame

    # Calculate total runtime
    total_runtime = time.time() - start_time

    out_dic = {}
    # Print object detection durations
    print("Object detection durations:")
    for label, duration in object_durations.items():
        print(f"{label}: {duration:.2f} seconds")
        out_dic[label] = duration
    #print(f"Total runtime: {total_runtime:.2f} seconds")
    print(out_dic)
    cap.release()
    cv2.destroyAllWindows()
    return out_dic
    # That code works


class AvatarWindow(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time_s = time

        # Configuración de la ventana principal
        tam_pixel = 128
        self.setWindowTitle("Avatar")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Sin bordes y siempre en primer plano
        screen_width, screen_height = pyautogui.size()
        self.move(screen_width-tam_pixel, screen_height-tam_pixel)
        self.resize(tam_pixel,tam_pixel)

        # Configuración de número de niveles
        self.levels = 4
        self.current_level = 1

        #Labels para camara
        self.eye_left = 0
        self.eye_right = 0
        self.person = 0
        self.handy = 0
        

        # Cargar las imágenes del avatar
        self.avatar_images = [f"Interface/avatares/avatar_{i}.gif" for i in range(1, 5)]  # Cambia "avatar" por la ruta de tus imágenes
        self.avatar_label = QLabel()

        # Crear un layout vertical y agregar widgets
        layout = QVBoxLayout()
        layout.addWidget(self.avatar_label)
        self.setLayout(layout)

        # Enlazar eventos de ratón
        self.enterEvent = self.on_enter
        self.leaveEvent = self.on_leave
        self.mouseDoubleClickEvent = self.on_doubleclic

        # Iniciar el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_bucle)
        self.tiempo_rep = self.time_s // self.levels
        self.timer.start(self.tiempo_rep*1000)

        # Iniciar la detección de ojos
        self.start_eye_detection()

        # Iniciar el temporizador para la detección de ojos
        self.eye_timer = QTimer(self)
        self.eye_timer.timeout.connect(self.start_eye_detection)
        self.eye_timer.start(60000)  # Ejecutar cada 1 minuto

        # Iniciar la animación del avatar
        self.change_avatar(self.current_level)

    def on_doubleclic(self, event):
        # Crear la ventana de diálogo
        dialog = QDialog(self)
        dialog.setWindowTitle("Dashboard")

        # Crear el widget QLCDNumber para mostrar la hora
        lcd = QLCDNumber()
        lcd.setDigitCount(8)  # Establecer el número de dígitos para mostrar la hora
        lcd.setSegmentStyle(QLCDNumber.Flat)  # Establecer el estilo del segmento LCD
        lcd.setFixedHeight(100)  # Establecer una altura más alta para el QLCDNumber

        # Crear la gráfica circular
        fig, ax = plt.subplots()
        labels = ['Concentrado', 'Sin mirar', 'Con el móvil', 'Comiendo']
        sizes = [0.73,0.07,0.15,0.05]
        # sizes = [max(self.eye_left,self.eye_right), (max(self.eye_left,self.eye_right)-self.handy)]
        # Aumentar el tamaño de la fuente en el gráfico
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 18})
        ax.axis('equal')
        canvas = FigureCanvas(fig)

        # Crear los botones
        button_cerrar = QPushButton("Cerrar")
        button2 = QPushButton("Botón 2")
        button_cerrar.clicked.connect(QApplication.quit)
        button2.clicked.connect(lambda: print("Botón 2 presionado"))

        # Crear el layout de la ventana de diálogo
        layout = QGridLayout()
        layout.addWidget(lcd, 0, 0, 1, 2)  # Agregar el QLCDNumber
        layout.addWidget(canvas, 1, 0, 1, 2)  # Agregar el gráfico
        layout.addWidget(button_cerrar, 2, 1)  # Agregar el botón de cerrar
        layout.addWidget(button2, 2, 0)  # Agregar el botón 2
        dialog.setLayout(layout)

        # Crear un temporizador para actualizar la hora cada segundo
        timer = QTimer(dialog)

        

        def seconds_to_hhmmss():
            self.time_crr -= 1
            seconds = self.time_crr
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")

        self.time_crr = self.time_s
        timer.timeout.connect(seconds_to_hhmmss)
        seconds = self.time_s
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        lcd.display(f"{hours:02}:{minutes:02}:{seconds:02}")
        timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

        # Mostrar la ventana de diálogo
        dialog.exec_()

        # Cerrar la gráfica al cerrar la ventana de diálogo
        plt.close(fig)

        # Obtener el tamaño de la pantalla y de la ventana
        screen_width, screen_height = pyautogui.size()
        dialog_size = dialog.size()
        window_width = dialog_size.width()
        window_height = dialog_size.height()

        # Calcular las coordenadas para la esquina inferior izquierda
        x = screen_width - window_width
        y = screen_height - window_height

        # Mover la ventana a las coordenadas calculadas
        dialog.move(x, y)



    def timer_bucle(self):
        print(f"Ha entrado al bucle {self.current_level}")
        if self.premio():
            if self.current_level == self.levels:
                None
            else:
                self.change_avatar(self.current_level)
                self.current_level += 1
                
        else:
            if self.current_level == 0:
                None
            else:
                self.current_level -= 1
                self.change_avatar(self.current_level)

        # Llamar a esta función nuevamente después de 1000 milisegundos (1 segundo)
        #self.timerId = self.startTimer(int(tiempo_rep) * 1000)

    def premio(self):
        if self.person == 0:
            return False
        print(max(self.eye_left,self.eye_right))
        print(self.handy)
        print(self.tiempo_rep)

        premio = ((max(self.eye_left,self.eye_right)-self.handy)/self.tiempo_rep) > 0.7
        self.eye_left = 0
        self.eye_right = 0
        self.person = 0
        self.handy = 0
        return premio

    def change_avatar(self, level):
        avatar_image_path = self.avatar_images[level]
    
        # Comprueba si la extensión del archivo es .gif para usar QMovie
        if avatar_image_path.endswith('.gif'):
            movie = QMovie(avatar_image_path)
            #movie.setScaledSize(QSize(128, 128))
            self.avatar_label.setMovie(movie)
            movie.start()
        else:
            avatar_pixmap = QPixmap(avatar_image_path)
            self.avatar_label.setPixmap(avatar_pixmap)

    def on_enter(self, event):
        # Cambiar la opacidad de la ventana al 80% cuando el ratón está encima
        self.setWindowOpacity(0.4)

    def on_leave(self, event):
        # Restaurar la opacidad de la ventana al 100% cuando el ratón sale
        self.setWindowOpacity(1)

    def start_eye_detection(self):
        self.eye_thread = EyeDetectionThread()
        self.eye_thread.result_signal.connect(self.handle_eye_detection_result)
        self.eye_thread.start()

    def handle_eye_detection_result(self, result):
        self.eye_left += result.get('left eye', 0)
        self.eye_right += result.get('right eye', 0)
        self.person += result.get('person', 0)
        self.handy += result.get('cell phone', 0)

        
        # Aquí puedes hacer algo con los resultados, como mostrarlos en la interfaz o guardarlos en un archivo

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
