import cv2
import numpy as np

def detect_tennis_balls(frame, prev_circles=None):
    # Konverter billedet til gråskala
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Forbedre kontrasten
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)

#Anvend Gaussisk udjævning for at reducere støj
    blurred = cv2.GaussianBlur(contrast_enhanced, (15, 15), 0)

    # Anvend HoughCircles til at detektere cirkler i billedet
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=100, param2=20, minRadius=1, maxRadius=30)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, radius) in circles:
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 4)
            cv2.putText(frame, f"Center: ({x},{y})", (x-50, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#Logik for at tælle og tracke bolde
    num_circles = circles.shape[0] if circles is not None else 0
    print(f"Detekterede bolde: {num_circles}")

#Enkel tracking: Sammenlign afstand mellem tidligere og nuværende cirkler
    if prev_circles is not None and circles is not None:
        for (x, y, r) in circles:
            closest_dist = np.min(np.sqrt((prev_circles[:, 0] - x)2 + (prev_circles[:, 1] - y)2))
            if closest_dist > 50:  # Skift tærskelværdi efter behov
                print(f"Bold flyttet til: ({x},{y})")

    return frame, circles

cap = cv2.VideoCapture(1)
prev_circles = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detected_frame, prev_circles = detect_tennis_balls(frame, prev_circles)

    # Vis detekterede frames
    cv2.imshow('Detected Tennis Balls', detected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()