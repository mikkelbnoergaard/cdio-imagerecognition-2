import cv2
import numpy as np
import time

min_radius = 5
max_radius = 15
min_distance = 5
dp = 1
param1 = 20
param2 = 23
blur_strength = 5

# Timeout in frames (5 seconds * 30 FPS) - adjust for desired clear interval
detection_timeout = 5
clear_interval = 10  # Frames to wait for complete list clear (20 seconds)

cap = cv2.VideoCapture(1)

circle_positions = {}
circle_history = {}  # Dictionary to store circle history (center, radius, last_seen)

print_interval = 5

last_print_time = time.time()
last_clear_time = time.time()  # Track time for list clear

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

    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)  # Get current frame number

    # Check for new circles and update positions
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            if radius > min_radius * 0.5:
                # Check if center already exists in list or history
                if center in circle_positions:
                    circle_positions[center] = radius  # Update existing circle
                    circle_history[center]["last_seen"] = frame_count  # Update last seen frame
                elif center in circle_history:
                    # Circle reappeared after being missed, likely the same circle
                    circle_positions[center] = radius
                    circle_history[center]["last_seen"] = frame_count  # Update last seen frame
                else:
                    # New circle
                    circle_positions[center] = radius
                    circle_history[center] = {"radius": radius, "last_seen": frame_count}

    # Update last_seen for existing entries and remove timed-out circles (unchanged)
    for center, entry in list(circle_history.items()):
        entry["last_seen"] = frame_count

        if frame_count - entry["last_seen"] >= detection_timeout:
            del circle_positions[center]
            del circle_history[center]

    # Draw detected circles (for troubleshooting) - comment out if not needed
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(frame, center, radius, (0, 0, 255), 2)  # Draw detected circles in blue

    # Draw and print circle information
    for center, radius in circle_positions.items():
        cv2.circle(frame, center, radius, (0, 255, 0), 2)

    cv2.imshow("Live Camera Feed", frame)

    current_time = time.time()
    if current_time - last_print_time >= print_interval:
        print("Circle Positions:")
        for idx, (center, radius) in enumerate(circle_positions.items(), start=1):
            print(f"Circle {idx}: Center {center}, Radius {radius}")
        last_print_time = current_time

    if current_time - last_clear_time >= clear_interval:
        circle_positions.clear()  # Clear circle positions dictionary
        circle_history.clear()    # Clear circle history dictionary
        last_clear_time = current_time  # Update last clear time    

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()