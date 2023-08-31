import cv2

def process_frame(frame):
    # Add your custom processing logic here (optional)
    # Example: You can apply filters, perform object detection, etc.
    return frame

def main():
    video_file = "DemoVideo/com.unity.xr.interaction.examples-20230729-170611.mp4"  # Replace with the path to your video file
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print("Error: Could not open the video file.")
        return

    fps = 60  # Desired frames per second
    delay = int(1000 / fps)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        processed_frame = process_frame(frame)

        # Display the frame
        cv2.imshow("Video", processed_frame)

        # Press 'q' to exit the video
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()