import cv2
import numpy as np
import mediapipe as mp
import time

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
finish_time = start_time+6000
frame_start_time = time.time()
while cap.isOpened() and time.time() - start_time < 60:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_start_time = time.time()

    # Convert color from BGR to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
# That code works
