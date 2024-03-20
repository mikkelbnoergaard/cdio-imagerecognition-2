import cv2
import numpy as np
import time

min_radius = 5
max_radius = 15
min_distance = 5
dp = 1
param1 = 25
param2 = 23
blur_strength = 5

cap = cv2.VideoCapture(1)

circle_positions = {}

print_interval = 5

last_print_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame from camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur_strength, blur_strength), 0)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, dp, min_distance,
                               param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            if radius > min_radius * 0.5:
                circle_positions[center] = radius

    for center, radius in circle_positions.items():
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

    cv2.imshow("Live Camera Feed", frame)

    current_time = time.time()
    if current_time - last_print_time >= print_interval:
        print("Circle Positions:")
        for idx, (center, radius) in enumerate(circle_positions.items(), start=1):
            print(f"Circle {idx}: Center {center}, Radius {radius}")
        last_print_time = current_time

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
