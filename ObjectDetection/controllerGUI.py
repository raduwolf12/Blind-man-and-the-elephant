import tkinter as tk
import serial

# Establish a serial connection with the microcontroller
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the actual serial port

def set_speed():
    speed = speed_entry.get()
    try:
        speed = int(speed)
        if 0 <= speed <= 100:
            ser.write(bytes(f'S{speed}\n', 'utf-8'))
        else:
            result_label.config(text="Speed should be between 0 and 100.")
    except ValueError:
        result_label.config(text="Please enter a valid speed.")

# Create the GUI window
root = tk.Tk()
root.title("Servo Control GUI")

# Create GUI components
speed_label = tk.Label(root, text="Enter Speed (0-100):")
speed_entry = tk.Entry(root)
set_speed_button = tk.Button(root, text="Set Speed", command=set_speed)
result_label = tk.Label(root, text="")

# Place GUI components on the window
speed_label.pack()
speed_entry.pack()
set_speed_button.pack()
result_label.pack()

root.mainloop()