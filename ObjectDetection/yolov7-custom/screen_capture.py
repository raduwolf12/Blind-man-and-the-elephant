import cv2
import mss
import numpy as np

def main():
    # Initialize screen capture
    with mss.mss() as sct:
        # Define monitor to capture (usually 1 is the primary monitor)
        monitor = sct.monitors[2]

        # Set the region to capture the entire screen
        capture_region = {
            "left": monitor["left"],
            "top": monitor["top"],
            "width": monitor["width"],
            "height": monitor["height"],
        }

        # Start capturing the screen
        while True:
            # Capture the screen
            screenshot = sct.grab(capture_region)
            screenshot = np.array(screenshot)

            # Display the captured frame in real-time
            cv2.imshow("Real-Time Screen Capture", screenshot)

            # Break the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Close all OpenCV windows and release resources
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
