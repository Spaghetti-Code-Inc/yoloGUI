# Program to make user interface for yolo algorithm with different functions

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk
import cv2
import random
import os

CONFIDENCE_THRESHOLD = 0.4

# Changes the model used when modelName var is changed
def changeModel(*args):
    global model, CLASS_COLOR, CLASS_NAMES
    model = YOLO(modelName.get())

    CLASS_NAMES = model.model.names
    CLASS_COLOR = []

    # Creates all of the class bounding boxes
    for name in CLASS_NAMES:
        CLASS_COLOR.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    print("Updated to Model: " + modelName.get())

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
    fileUploaded = True

# Function called that oversees all of the camera functions
def run_camera():
    global img, img_s, viewInferenceFrame, model
    global filename, inf_img

    # Get the latest frame and convert into Image
    f = vid.read()[1]
    frame = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
    output = Image.fromarray(frame, 'RGB') 

    if(viewInferenceFrame): 
        output = model.predict(output, conf=CONFIDENCE_THRESHOLD, verbose=False)  

        boxes = output[0].boxes

        for i, box in enumerate(boxes.xyxy):
            class_num = int(boxes.cls[i].item())
            name = CLASS_NAMES[class_num]
            
            # Left, Top of bounding box
            start_point = (int(box[0].item()), int(box[1].item()))
            # Right, Bottom of bounding box
            end_point = (int(box[2].item()), int(box[3].item()))
            # Gets the color of the bounding box based on the class
            color = CLASS_COLOR[class_num]

            # Draws the bounding box on the image
            frame = cv2.rectangle(frame, start_point, end_point, color, 2)
            frame = cv2.putText(frame, name,
                                (int(box[0]), int(box[1]-5)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color,
                                2, lineType=cv2.LINE_AA
                                )
            
            inf_img.append(frame)

    image = Image.fromarray(frame, 'RGB')

    # Convert image to PhotoImage
    img = ImageTk.PhotoImage(image.resize((500, 400)))
    img_s = ImageTk.PhotoImage(image.resize((100, 80)))
 
    label = Label(m)
    label.grid(row=0, column=1)
    label.imgtk = img
    label.configure(image=img)

    update_left_panel()

    # Wait for image to show up
    cv2.waitKey()

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
    global tool_bar

    left_frame = Frame(window, width=200, height=400, bg='#669aaf')
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    #left frame menu items
    left_label = Label(left_frame, image=img_s, text="Original Image", relief=RAISED,bg='#ad4b6f',fg='#FFFFFF',padx=5,pady=1).grid(row=0,column=0,padx=5,pady=5)

    # right frame, for image to be detected with
    right_frame = Frame(window, width=600,height=400,bg='#669fff')
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # add image to right frame
    tk.Button(right_frame,image=img_l, command=lambda: upload_file()).grid(row=0,column=1)

    # tool bar
    tool_bar = Frame(left_frame, width=100, height=185, bg='#669aaf')
    tool_bar.grid(row=2,column=0,padx=5,pady=5)

    # menu buttons
    cameraButton = tk.Button(tool_bar, text='Use Webcam', command=lambda:start_frame()).grid(row=0,column=0,padx=5,pady=3,ipadx=10)
    uploadButton = tk.Button(tool_bar, text='Upload Image', command= lambda:upload_file()).grid(row=1,column=0,padx=5,pady=3,ipadx=10)
    runButton = tk.Button(tool_bar, text='        Run         ', command=lambda:run_algorythm()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)
    
    # variable for detection model
    modelName = StringVar(m)
    modelName.set("yolov8n.pt")
    
    # drop down to select object detection model
    options = ["yolov8n.pt", "yolov8m.pt", 'yolo_WeaponDetection.pt']
    tk.OptionMenu(left_frame, modelName, *(options), command=changeModel).grid(row=3,column=0,padx=5,pady=3,ipadx=10)

    return window

def start_frame():
    global getFrame
    global vid
    vid = cv2.VideoCapture(cam_port)
    # Need the spaces to give it more padding
    tk.Button(tool_bar, text=' Take Picture ', command=lambda:end_frame()).grid(row=0,column=0,padx=5,pady=3,ipadx=10)
    # Changes the run button
    tk.Button(tool_bar, text='Run on Video', command=lambda:run_video_algorithm()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)

    getFrame = True

# Takes a picture of the last frame and saves it
def end_frame():
    global img, img_s, viewInferenceFrame, model
    global filename

    # Get the latest frame and convert into Image
    f = vid.read()[1]
    frame = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(frame, 'RGB')

    # Convert image to PhotoImage
    img = ImageTk.PhotoImage(image.resize((500, 400)))
    img_s = ImageTk.PhotoImage(image.resize((100, 80)))
 
    label = Label(m)
    label.grid(row=0, column=1)
    label.imgtk = img
    label.configure(image=img)

    update_left_panel()

    # Wait for image to show up
    cv2.waitKey()

    filename = "saved.jpg"
    cv2.imwrite(filename, f)
    global fileUploaded
    fileUploaded = True

    global getFrame
    getFrame = False

    # replace 'Take Picture' Button with 'Use Webcam' nad replace run button
    tk.Button(tool_bar, text='Use Webcam', command=lambda:start_frame()).grid(row=0,column=0,padx=5,pady=3,ipadx=10)
    tk.Button(tool_bar, text='        Run         ', command=lambda:run_algorythm()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)

# updates the left panel upon image upload
def update_left_panel():
    label = Label(left_frame)
    label.grid(row=0, column=0)
    label.imgtk = img_s
    label.configure(image=img_s)
    # left_label = Label(left_frame, image=img_s, text="Original Image", relief=RAISED,bg='#ad4b6f',fg='#FFFFFF',padx=5,pady=1).grid(row=0,column=0,padx=5,pady=5)

def stop_VideoInference():
    global viewInferenceFrame, inf_video, inf_img
    viewInferenceFrame = False

    save_dir = "runs\\detect_video"
    num = len(os.listdir(save_dir))
    save_dir = os.path.join(save_dir, "test" + str(num) + ".mp4")

    print("Inference images length: " + str(len(inf_img)) + ", saving to: " + save_dir)
    inf_video = cv2.VideoWriter(save_dir, cv2.VideoWriter_fourcc('m','p','4','v'), 10, (640, 480))
    for img in inf_img:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        inf_video.write(img)
    # Saves the video
    inf_video.release()
    # Resets the video stream
    inf_img = []
    
    # Changes the run button
    tk.Button(tool_bar, text='Run on Video', command=lambda:run_video_algorithm()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)

# Tells video to run inference on every frame that comes in
def run_video_algorithm():
    global viewInferenceFrame
    viewInferenceFrame = True

    tk.Button(tool_bar, text='  Stop Video   ', command=lambda:stop_VideoInference()).grid(row=2,column=0,padx=5,pady=3,ipadx=10)

# runs yolo object detection algorythm
def run_algorythm():
    # do not run the algorithm if the user is still using webcam -- Redundant Check
    if getFrame: 
        showError()
        return

    global relativePath
    # Makes sure a file is actually uploaded
    try:
        if(fileUploaded == False): return
    except:
        print("must upload image first")
        showError()
        return


    # make the prediction from the model
    global model, img_s
    results = model.predict(source=filename, save=True, conf=CONFIDENCE_THRESHOLD, verbose=False)
    
    # The directory the annotated image was saved to
    save_directory = results[0].save_dir
    relativePath = save_directory + "\\" + filename.split("/")[-1]

    # Opens image
    try: 
        img=Image.open(relativePath)
    except:
        print(relativePath + "-- Did not find")
        
    img_resized=img.resize((500,400)) # new width & height

    img=ImageTk.PhotoImage(img_resized)
 
    label = Label(m)
    label.grid(row=0, column=1)
    label.imgtk = img
    label.configure(image=img)

    # Wait for image to show up
    cv2.waitKey()

# initialize screen
m = initScreen()

# setup default image, resizes them for left and right panel respectfully
default_img_s, default_img_l = initImages("imageUpload.jpg")

# update window with panels
m = setupPanels(m, default_img_s, default_img_l)

# Pop up menu build
popup = Menu(m, tearoff=0)

popup.add_command(label="Save", command=lambda: saveImg())

# initialize the camera
cam_port = 0
vid = cv2.VideoCapture(cam_port)
getFrame = False
viewInferenceFrame = False

model = YOLO(modelName.get())

CLASS_NAMES = model.model.names
CLASS_COLOR = []

# Creates all of the class bounding boxes
for name in CLASS_NAMES:
    CLASS_COLOR.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# Where all inf images will be saved for a video
inf_img = []

# Create directories for all saved images

try: os.mkdir('runs')
except: print("Runs previously made")
try: os.mkdir('runs\\detect')
except: print("Detect images previously made")
try: os.mkdir('runs\\detect_video')
except: print("Detect video previously made")

while True:
    m.update()
    if(getFrame): run_camera()
    else: vid.release()