import cv2
import numpy as np
import cvui
import ultralytics
from ultralytics import YOLO
import tkinter as tk
from tkinter import filedialog

def letterbox_image(img, target_w, target_h):
    h, w = img.shape[:2]
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h))

    # create new canvas
    canvas = np.full((target_h, target_w, 3), (49, 52, 49), dtype=np.uint8)

    # center the resized image on canvas
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

ultralytics.checks()
model = YOLO("yoloTrained\last.pt")

WINDOW_NAME = 'Object Detection with YOLO'

# Load your image
detected = cv2.imread('img/detected.png')
if detected is None:
    raise FileNotFoundError("Image not found.")

# Create a frame to draw the UI
frameWidth = 1024
frameHeight = 768
frame = np.zeros((frameHeight, frameWidth, 3), np.uint8)

# Which image show (Radio buttons booleans)
img1B, img2B, img3B, img4B, img5B = [True, True], [False, False], [False, False], [False, False], [False, False] #second element is old status
imageChanged = False

# Margin and position values
xTrackBars = 20
yTrackBars = 40
trackBarsSize = 200
bottomMargin = 75
sideMargin = 25
windowWidth = frameWidth - xTrackBars*2
windowHeight = frameHeight- yTrackBars-bottomMargin - xTrackBars

# Initialize cvui
cvui.init(WINDOW_NAME)

while True:
    # Fill background
    frame[:] = (49, 52, 49)

    # Load proper test img
    if(img1B[0]):
        img = "img/1.jpg"
    if(img2B[0]):
        img = "img/2.jpg"
    if(img3B[0]):
        img = "img/3.jpg"
    if(img4B[0]):
        img = "img/4.jpg"
    if(img5B[0]):
        img = "img/5.jpg"

    yPos = yTrackBars - 20
    cvui.checkbox(frame, xTrackBars-5, yPos, 'Image 1', img1B)
    cvui.checkbox(frame, xTrackBars-5+100, yPos, 'Image 2', img2B)
    cvui.checkbox(frame, xTrackBars-5+100*2, yPos, 'Image 3', img3B)
    cvui.checkbox(frame, xTrackBars-5+100*3, yPos, 'Image 4', img4B)
    cvui.checkbox(frame, xTrackBars-5+100*4, yPos, 'Image 5', img5B)
    # Make this CheckBox to Radio Button
    if(img1B[0] != img1B[1] or img2B[0] != img2B[1] or img3B[0] != img3B[1] or img4B[0] != img4B[1] or img5B[0] != img5B[1]):
        imageChanged = True
    if(imageChanged):
        if(img1B[1] == True):
            img1B[0] = False
            img1B[1] = False
        if(img2B[1] == True):
            img2B[0] = False
            img2B[1] = False
        if(img3B[1] == True):
            img3B[0] = False
            img3B[1] = False
        if(img4B[1] == True):
            img4B[0] = False
            img4B[1] = False
        if(img5B[1] == True):
            img5B[0] = False
            img5B[1] = False

        if(img1B[0] == True):
            img1B[1] = True
        if(img2B[0] == True):
            img2B[1] = True
        if(img3B[0] == True):
            img3B[1] = True
        if(img4B[0] == True):
            img4B[1] = True
        if(img5B[0] == True):
            img5B[1] = True
        imageChanged = False

    if cvui.button(frame, xTrackBars-15+100*5, yPos-5, 'Detect'):
        print('Image button clicked!')
        
        results = model(img)
        # Get the first result’s plotted image
        annotated = results[0].plot()
        cv2.imwrite("img/detected.png", annotated)
        detected = cv2.imread('img/detected.png')

    if cvui.button(frame, xTrackBars-15+100*6, yPos-5, 'Load & Detect Custom Image'):
        print('Load Custom Image button clicked!')
        root = tk.Tk()
        root.withdraw()  # Hide the empty root window
        file = filedialog.askopenfilename( title="Select an image", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        results = model(file)
        # Get the first result’s plotted image
        annotated = results[0].plot()
        cv2.imwrite("img/detected.png", annotated)
        detected = cv2.imread('img/detected.png')

    # Show result preview inside the same window
    #preview = cv2.resize(detected, (windowWidth, windowHeight))
    preview = letterbox_image(detected, windowWidth, windowHeight)
    startY = int(yPos+70)
    startX = xTrackBars
    frame[startY:startY+windowHeight, startX:startX+windowWidth] = preview

    cvui.update()
    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(20) == 27:  # ESC to quit
        break
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()