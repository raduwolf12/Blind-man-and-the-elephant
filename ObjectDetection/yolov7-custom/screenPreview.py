import os
import subprocess

# Function to apply object detection on the captured frame
def apply_object_detection():
    command = f"python detect.py --weights yolov7_custom.pt --conf 0.5 --img-size 640 --source screenshot.png --nosave --no-trace"
    subprocess.run(command, shell=True)

def main():
    # Start the screen capture script in a separate process
    capture_script = "python screen_capture.py"
    subprocess.Popen(capture_script, shell=True)

    # Apply object detection on the captured frames in real-time
    apply_object_detection()

if __name__ == "__main__":
    main()
