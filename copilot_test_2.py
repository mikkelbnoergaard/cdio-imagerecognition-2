import cv2
import numpy as np

# Parameters for color thresholding
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 20, 255])

lower_orange = np.array([5, 50, 50])
upper_orange = np.array([15, 255, 255])

# Open the video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Read the frame
    _, frame = cap.read()

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for red, white and orange colors
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Combine the masks
    mask = cv2.bitwise_or(red_mask, white_mask)
    mask = cv2.bitwise_or(mask, orange_mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the frame
    for contour in contours:
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)

    # Show the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()