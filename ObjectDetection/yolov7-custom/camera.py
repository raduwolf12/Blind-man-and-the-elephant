import cv2

def view_camera():
    # Create a VideoCapture object to access the camera (usually camera index 0 is the default built-in camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera was successfully opened
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Unable to read frame from the camera.")
            break

        # Display the frame in a window
        cv2.imshow("Camera", frame)

        # Exit the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    view_camera()
