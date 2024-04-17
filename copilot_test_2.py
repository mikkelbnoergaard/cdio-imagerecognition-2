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
    # Read a frame
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

    # Define range for red color
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res_red = cv2.bitwise_and(frame, frame, mask=mask_red)

    # Find contours in the red mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw all red contours
    for contour in contours_red:
        cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)  # Red color for contours

    # Define range for white color
    lower_white = np.array([0, 0, 212])
    upper_white = np.array([131, 255, 255])

    # Threshold the HSV image to get only white colors
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res_white = cv2.bitwise_and(frame, frame, mask=mask_white)

    # Find contours in the white mask
    contours_white, _ = cv2.findContours(mask_white, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small or non-circular white contours
    for contour in contours_white:
        area = cv2.contourArea(contour)
        if area > 30:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 0.5 < circularity < 1.5:  # Less strict circularity check for balls
                cv2.drawContours(frame, [contour], -1, (255, 255, 255), 3)  # White color for balls

    # Show the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()