# SCBIO PROJECT
## Documentación del Código

### Resumen
La clase `AvatarWindow` es una interfaz de usuario que muestra un avatar en la esquina derecha de la pantalla. Esta interfaz controla la detección de rostros y ojos en tiempo real, así como también el reconocimiento de objetos mediante YOLOv3. Además, gestiona varios estados relacionados con la atención del usuario, como la concentración, distracciones. A través de la ventana de Dashboard, el usuario puede monitorear estos estados en tiempo real.

### Funciones Principales

1. `__init__(self, time)`: Inicializa la ventana del avatar y configura las variables necesarias, como la detección de ojos, la ubicación del avatar en la pantalla, y los temporizadores para el cambio de niveles y la detección de ojos.

2. `timer_bucle(self)`: Controla el bucle que coordina el cambio de niveles del avatar.

3. `premio(self)`: Determina si se otorga un premio (nivel adicional) al usuario basándose en su nivel de concentración.

4. `change_avatar(self, level)`: Cambia la imagen del avatar según el nivel actual.

5. `ventana_dashboard(self)`: Muestra una ventana de Dashboard donde se visualiza información sobre la concentración, distracciones del usuario.

6. `on_doubleclic(self, event)`: Maneja el evento de doble clic sobre el avatar para abrir la ventana de Dashboard.

7. `on_enter(self, event)`: Cambia la opacidad del avatar cuando el cursor del mouse está sobre él.

8. `on_leave(self, event)`: Restaura la opacidad del avatar cuando el cursor del mouse deja el área del avatar.

9. `start_eye_detection(self)`: Inicia la detección de ojos mediante un hilo separado.

10. `handle_eye_detection_result(self)`: Maneja los resultados de la detección de ojos, actualizando los estados relacionados con la atención del usuario.

11. `pause_app(self)`: Pausa o reanuda la aplicación, deteniendo los temporizadores y la detección de ojos.

12. `eyedetection(self)`: Realiza la detección de rostros y ojos en tiempo real, así como también el reconocimiento de objetos, utilizando MediaPipe y YOLOv3.

Esta documentación proporciona una visión general de la funcionalidad y la estructura del código, lo que facilita su comprensión y mantenimiento por parte de otros desarrolladores.
