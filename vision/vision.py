import cv2
from tkinter import filedialog
from tkinter import Tk 
import easygui

def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        easygui.msgbox("Cannot open webcam")

    ret, frame = cam.read()
    cam.release()

    if ret:
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        return image_path

    else:
        easygui.msgbox("Failed to capture image from webcam")

def choose_image():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    root.destroy()
    return file_path if file_path else None
