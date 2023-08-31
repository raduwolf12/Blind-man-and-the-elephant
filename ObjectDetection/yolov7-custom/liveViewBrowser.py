import cv2
from flask import Flask, render_template, Response

# Initialize Flask app
app = Flask(__name__)

# Function to capture screen video
def get_screen_capture():
    while True:
        # Capture the screen video
        screen = cv2.VideoCapture(0)  # Use 0 for the default webcam, adjust if necessary
        success, frame = screen.read()

        if success:
            # Encode the frame to jpeg format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Convert the frame to bytes
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route for streaming video
@app.route('/video_feed')
def video_feed():
    return Response(get_screen_capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Default route
@app.route('/')
def index():
    return render_template('index.html')  # Create a simple HTML template to display the video

# Start the Flask app on localhost
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
