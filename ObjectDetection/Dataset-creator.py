import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import trimesh

# Global variables
object_model = None  # Variable to store the 3D model
rotation_x = 0
rotation_y = 0
zoom = -5  # Initialize the zoom level

# Function to load the 3D object
def load_3d_model(file_path):
    try:
        global object_model
        object_model = trimesh.load(file_path)
    except Exception as e:
        print(f"Error loading 3D model: {e}")
        pygame.quit()
        quit()

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

# Initialize Pygame and OpenGL
def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Main function to capture images with scaling, rotation, and movement
def capture_images():
    global rotation_x, rotation_y, zoom
    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotation_x += 5
                elif event.key == pygame.K_DOWN:
                    rotation_x -= 5
                elif event.key == pygame.K_LEFT:
                    rotation_y += 5
                elif event.key == pygame.K_RIGHT:
                    rotation_y -= 5
                elif event.key == pygame.K_PAGEUP:
                    zoom += 10
                elif event.key == pygame.K_PAGEDOWN:
                    zoom -= 10

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_3d_object()
        pygame.display.flip()
        pygame.time.wait(10)

# Replace 'your_model_path' with the actual path to your STL file
model_path = 'D:\Master\ProjectOutsideOfCouseScope\XR-Interaction-Toolkit-Examples\Assets\objs\Corona.obj'
load_3d_model(model_path)
capture_images()