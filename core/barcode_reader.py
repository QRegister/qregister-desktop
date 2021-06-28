import time
from pyzbar.pyzbar import decode
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
camera = True
while camera:
    success, frame = cap.read()

    for code in decode(frame):
        print(code.type)
        print(code.data.decode('utf-8'))
        time.sleep(5)

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)
