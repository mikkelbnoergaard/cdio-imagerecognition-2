import cv2
import numpy as np

# Function to adjust gamma
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Open the video capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Read the frame
    _, frame = cap.read()

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate the color distribution
    color_dist = np.mean(hsv[:,:,1])

    # Adjust gamma based on color distribution
    if color_dist < 60:
        frame = adjust_gamma(frame, 2)  # Increase gamma for low color images
    elif color_dist > 190:
        frame = adjust_gamma(frame, 0.5)  # Decrease gamma for high color images

    # Convert the adjusted frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for white color
    lower_white = np.array([0, 0, 212])
    upper_white = np.array([131, 255, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small or non-circular contours
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.7 < circularity < 1.5:  # Less strict circularity check for balls
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)  # Green color for balls
            elif area > 500:  # Check for larger contours for boundaries
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)  # Red color for boundaries

    # Show the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()