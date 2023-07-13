# Program to make user interface for yolo algorythm with different functions

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk
import cv2
import os
import keyboard
import time
import shutil

getFrame = False

def file_uploaded():
    fileUploaded = True
    return fileUploaded

# Basic click function, prints to console
def clicked():
    print("Clicked")

# function to open pop up menu on image click event
def popupm(b2):
     try:         
        x = b2.winfo_rootx()
        y = b2.winfo_rooty()
        popup.tk_popup(x, y, 0)
     finally:
           popup.grab_release()

#   Function to save image to users desktop
def saveImg():
    print(relativePath)
    detectedImage = ImageTk.getimage(relativePath)
    f = asksaveasfile(mode="w",initialfile = 'Untitled.jpg',
    defaultextension=".jpg",filetypes=[('Jpg Files', '*.jpg'),('Png Files', '*.png')])
    if not f:
        return
    detectedImage.save(f)

# simple function to show error
def showError():
    messagebox.showerror('Error', 'Must upload image first')

#Function called to upload image from user desktop
def upload_file():
    global filename
    f_types = [('Jpg Files', '*.jpg'),('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    show_file(filename)
    update_left_panel()
    global fileUploaded
    fileUploaded = file_uploaded()

# Function called that oversees all of the camera functions
def run_camera():
    # reading the input using the camera
    ret,frame=vid.read()

    # THE BUTTON PRESS TO CHANGE
    # Once this key is pressed getFrame is flipped
    if keyboard.is_pressed("b"):
        global getFrame
        getFrame = False
        # Needed so holding down the button does not send multiple commands
        time.sleep(.2)
    # convert color scale of frame
    bgrFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # output
    show_image(bgrFrame)
    global filename
    filename = "saved.jpg"
    cv2.imwrite(filename, frame)
    update_left_panel()
    global fileUploaded
    fileUploaded = file_uploaded()

# Function that shows the file on the screen
def show_file(filename):
    global img
    global img_s
    img=Image.open(filename)
    img_resized=img.resize((500,400)) # new width & height
    img_resized_s=img.resize((100,80)) # new width & height
    img=ImageTk.PhotoImage(img_resized)
    img_s=ImageTk.PhotoImage(img_resized_s)
    b2 =tk.Button(m,image=img) # , command=lambda: popupm(b2) 
    b2.grid(row=0,column=1)

def show_image(image):
    global img
    global img_s
    img = Image.fromarray(image, 'RGB')
    img_resized=img.resize((500,400)) # new width & height
    img_resized_s=img.resize((100,80)) # new width & height
    img=ImageTk.PhotoImage(img_resized)
    img_s=ImageTk.PhotoImage(img_resized_s)
    b2 =tk.Button(m,image=img) # using Button 
    b2.grid(row=0,column=1)


    
#initializes image, retuns image in small and large size
def initImages(source):
    imgSmall = ImageTk.PhotoImage(Image.open(source).resize((100, 80)))
    imgLarge = ImageTk.PhotoImage(Image.open(source).resize((500, 400)))
    return imgSmall, imgLarge

#initializes the window
def initScreen():
    window = tk.Tk()
    window.maxsize(680, 430)
    window.config(bg='#a0c8d7')
    window.title('YOLOv8 GUI')
    return window

# sets up te window structure with two panels
def setupPanels(window, img_s, img_l):
    # left frame, for menu
    global left_frame 
    global left_label
    global getFrame
    global modelName

    left_frame = Frame(window, width=200, height=400, bg='#669aaf')
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    #left frame menu items
    left_label = Label(left_frame, image=img_s, text="Original Image", relief=RAISED,bg='#ad4b6f',fg='#FFFFFF',padx=5,pady=1).grid(row=0,column=0,padx=5,pady=5)


    # right frame, for image to be detected with
    right_frame = Frame(window, width=600,height=400,bg='#669aaf')
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # add image to right frame
    b2 =tk.Button(right_frame,image=img_l, command=lambda: upload_file()) # using Button 
    b2.grid(row=0,column=1)


    # tool bar
    tool_bar = Frame(left_frame, width=100, height=185, bg='#669aaf')
    tool_bar.grid(row=2,column=0,padx=5,pady=5)

    # menu buttons
    cameraButton = tk.Button(tool_bar, text='Use Webcam', command=lambda:start_frame()).grid(row=0,column=0,padx=5,pady=3,ipadx=10)
    uploadButton = tk.Button(tool_bar, text='Upload Image', command= lambda:upload_file()).grid(row=1,column=0,padx=5,pady=3,ipadx=10)
    runButton = tk.Button(tool_bar, text='Run', command=lambda:run_algorythm()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)
    
    # variable for detection model
    modelName = StringVar(m)
    modelName.set("yolov8n.pt")

    # drop down to select object detection model
    modelMenu = tk.OptionMenu(left_frame, modelName, "yolov8n.pt", "other model").grid(row=3,column=0,padx=5,pady=3,ipadx=10)

    
    

    return window


def start_frame():
    global getFrame
    getFrame = True

# updates the left panel upon image upload
def update_left_panel():
    left_label = Label(left_frame, image=img_s, text="Original Image", relief=RAISED,bg='#ad4b6f',fg='#FFFFFF',padx=5,pady=1).grid(row=0,column=0,padx=5,pady=5)

# runs yolo object detection algorythm
def run_algorythm():
    global relativePath
    # Makes sure a file is actually uploaded
    try:
        print(fileUploaded)
    except:
        print("must upload image first")
        showError()
        return
    if(fileUploaded == False):
        return
    try:
        print("try to remove tree")
        shutil.rmtree("runs")
    except:
        print("No previous runs")

    # Creates the bounding box on the image
    model = YOLO(modelName.get())
    results = model.predict(source=filename, save=True)
    # finding image and saving it to a variable
    imageName = filename.split('/')
    relativePath = "runs\detect\predict\\"+str(imageName[-1])
    img=Image.open(relativePath)
    img_resized=img.resize((500,400)) # new width & height

    img=ImageTk.PhotoImage(img_resized)
    
    b2 =tk.Button(m,image=img, command=lambda: popupm(b2)) # using Button 
    b2.grid(row=0,column=1)
    
    cv2.imshow("Image", relativePath)
    # cv2.waitKey(5000)
    
# initialize screen
m = initScreen()

# setup default image, resizes them for left and right panel respectfully
default_img_s, default_img_l = initImages("imageUpload.jpg")

# update window with panels
m = setupPanels(m, default_img_s, default_img_l)
m.bind('<Escape>', lambda e: m.quit())

# Pop up menu build
popup = Menu(m, tearoff=0)

popup.add_command(label="Save", command=lambda: saveImg())



# initialize the camera
cam_port = 0
vid = cv2.VideoCapture(cam_port)
getFrame = False
while True:
    m.update()
    if(getFrame): run_camera()
    # Running at about 30 fps
    time.sleep(.0333)