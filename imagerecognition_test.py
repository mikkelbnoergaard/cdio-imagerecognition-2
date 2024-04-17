import cv2
import numpy as np
import time

#from main import turn_360

min_radius = 5
max_radius = 15
min_distance = 5
dp = 1
param1 = 25
param2 = 23
blur_strength = 5

detection_timeout = 5
clear_interval = 10

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

circle_positions = {}
circle_history = {}
cross_positions = {}

print_interval = 5

last_print_time = time.time()
last_clear_time = time.time()

while True:
    try:
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

        frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                if radius > min_radius * 0.5:
                    
                    if center in circle_positions:
                        circle_positions[center] = radius
                        circle_history[center]["last_seen"] = frame_count
                    elif center in circle_history:
                        circle_positions[center] = radius
                        circle_history[center]["last_seen"] = frame_count
                    else:
                        circle_positions[center] = radius
                        circle_history[center] = {"radius": radius, "last_seen": frame_count}

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:  # Minimum area threshold for cross detection
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 12:  # Cross has 12 vertices
                    center = tuple(map(int, np.mean(approx, axis=0)[0]))
                    cross_positions[center] = area
                    cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)

        for center, entry in list(circle_history.items()):
            entry["last_seen"] = frame_count

            if frame_count - entry["last_seen"] >= detection_timeout:
                del circle_positions[center]
                del circle_history[center]

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                cv2.circle(frame, center, radius, (0, 0, 255), 2)

        for center, radius in circle_positions.items():
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

        cv2.imshow("Live Camera Feed", frame)

        current_time = time.time()
        if current_time - last_print_time >= print_interval:
            print("Circle Positions:")
            for idx, (center, radius) in enumerate(circle_positions.items(), start=1):
                print(f"Circle {idx}: Center {center}, Radius {radius}")
            print("")
            print("Cross positions:")
            for idx, (center) in enumerate(cross_positions.items(), start = 1):
                print(f"Cross {idx}: Position {center}")
            last_print_time = current_time

        if current_time - last_clear_time >= clear_interval:
            #turn_360()
            circle_positions.clear()
            circle_history.clear()
            cross_positions.clear()
            last_clear_time = current_time   

        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print(f"An error occurred: {e}")

cap.release()
cv2.destroyAllWindows()