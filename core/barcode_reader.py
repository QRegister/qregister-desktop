import time
from pyzbar.pyzbar import decode
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
used_codes = []

camera = True
while camera:
    success, frame = cap.read()

    for code in decode(frame):
        barcode_str = code.data.decode('utf-8')
        if barcode_str not in used_codes:
            print(code.type)
            print(barcode_str)
            used_codes.append(barcode_str)
            time.sleep(5)
        elif barcode_str in used_codes:
            pass

    cv2.imshow('QRegister Barcode Scanner', frame)
    cv2.waitKey(1)
