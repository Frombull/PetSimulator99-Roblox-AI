import pyautogui
import cv2
import numpy as np

while True:
    # Take screenshot using PyAutoGUI
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to OpenCV format
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Display the screenshot in a window
    cv2.imshow('Screenshot', frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close OpenCV windows
cv2.destroyAllWindows()
