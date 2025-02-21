import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

def detect_face(on_detect_face):
    print('here')
    ret, frame = cap.read()
    if not ret:
        return
     
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.detections:
        on_detect_face('Face detected')
    on_detect_face("toto")
