import sys
import time
import csv
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QImage, QPixmap
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import ImageGrab
import pandas as pd

# Global variables
object_model = None  # Variable to store the 3D model
rotation_x = 0
rotation_y = 0
zoom = -5  # Initialize the zoom level
capture_interval = 2  # Interval in seconds between captures
output_folder = ""  # Folder to save the captured images
csv_file = ""  # CSV file to store image paths and labels
label = ""  # Variable to store the label entered in the text field
image_counter = 0  # Counter for naming captured images
capture_region = None  # Region to capture (set by user)


# Function to load the 3D object
def load_3d_model(file_path):
    try:
        global object_model
        object_model = trimesh.load(file_path)
    except Exception as e:
        print(f"Error loading 3D model: {e}")
        object_model = None


# Function to draw the 3D object
def draw_3d_object():
    global rotation_x, rotation_y, zoom
    if object_model is not None:
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(0, 0, zoom)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        glBegin(GL_TRIANGLES)
        for triangle in object_model.vertices[object_model.faces]:
            for vertex in triangle:
                glVertex3fv(vertex)
        glEnd()
        glPopMatrix()


# Initialize PyOpenGL
def init_opengl():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Function to capture images and save them with labels
def capture_and_save_image():
    global image_counter, output_folder, label, capture_region
    image = QApplication.primaryScreen().grabWindow(0, *capture_region)  # Capture the specified region
    image_name = f"{label}_{image_counter}.png"
    image_path = os.path.join(output_folder, image_name)
    image.save(image_path)

    # Append image path and label to the CSV file
    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([image_path, label])

    image_counter += 1
    update_preview(image_path)


# Function to update the preview with the latest captured image
def update_preview(image_path):
    pixmap = QPixmap(image_path).scaledToWidth(400)  # Adjust the width here to make the preview image bigger
    preview_label.setPixmap(pixmap)


# Main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("3D Object Capture App")
        self.setGeometry(100, 100, 1000, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter Label:")
        self.layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setAlignment(Qt.AlignLeft)
        self.line_edit.textChanged.connect(self.update_label)
        self.layout.addWidget(self.line_edit)

        self.capture_rate_label = QLabel("Capture Rate (pictures per second):")
        self.layout.addWidget(self.capture_rate_label)

        self.capture_rate_edit = QLineEdit()
        self.capture_rate_edit.setAlignment(Qt.AlignLeft)
        self.capture_rate_edit.textChanged.connect(self.update_capture_rate)
        self.layout.addWidget(self.capture_rate_edit)

        self.capture_region_label = QLabel("Capture Region (x, y, width, height):")
        self.layout.addWidget(self.capture_region_label)

        self.capture_region_edit = QLineEdit()
        self.capture_region_edit.setAlignment(Qt.AlignLeft)
        self.capture_region_edit.textChanged.connect(self.update_capture_region)
        self.layout.addWidget(self.capture_region_edit)

        self.start_button = QPushButton("Start Capture")
        self.start_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setDisabled(True)  # Disable the stop button initially
        self.layout.addWidget(self.stop_button)

        self.capture_section_label = QLabel("Screen Capture Section:")
        self.layout.addWidget(self.capture_section_label)

        self.capture_section = QLabel()
        self.layout.addWidget(self.capture_section)

        # Add preview label to display captured images
        self.preview_label = QLabel("Preview:")
        self.layout.addWidget(self.preview_label)

        global preview_label
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(preview_label)

        self.open_gl_widget = OpenGLWidget()
        self.layout.addWidget(self.open_gl_widget)

        self.central_widget.setLayout(self.layout)

    def update_label(self):
        global label
        label = self.line_edit.text()

    def update_capture_rate(self):
        global capture_interval
        try:
            capture_rate = float(self.capture_rate_edit.text())
            if capture_rate <= 0:
                raise ValueError("Capture rate must be greater than 0.")
            capture_interval = 1 / capture_rate
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            self.capture_rate_edit.clear()

    def update_capture_region(self):
        global capture_region
        try:
            capture_region = [int(coord) for coord in self.capture_region_edit.text().split(",")]
            if len(capture_region) != 4:
                raise ValueError("Invalid capture region format. Please use 'x, y, width, height'.")
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            self.capture_region_edit.clear()

    def start_capture(self):
        global label, image_counter, output_folder, csv_file
        label = self.line_edit.text()
        image_counter = 0  # Reset the image counter
        self.start_button.setDisabled(True)
        self.stop_button.setEnabled(True)

        # Create a timestamp-based folder to store captures and CSV file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_folder = f"captures_{timestamp}"
        os.makedirs(output_folder)

        csv_file = os.path.join(output_folder, "captured_data.csv")

        # Create CSV file and add header
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Image Path", "Label"])

        # Start capturing images at the specified interval
        self.timer = QTimer(self)
        self.timer.timeout.connect(capture_and_save_image)
        self.timer.start(capture_interval * 1000)  # Convert seconds to milliseconds

    def stop_capture(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setDisabled(True)


# OpenGL widget for rendering the 3D object
class OpenGLWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(400, 400)

    def initializeGL(self):
        init_opengl()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_3d_object()


# 1,65,1625,970   valori pt capture region

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())