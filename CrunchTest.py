  
# Importing modules for Tkinter 
from tkinter import *
from tkinter import filedialog
from token import LEFTSHIFT
from tokenize import Name
from PIL import Image, ImageTk

# Importing modules for mediapipe
import cv2
import numpy as np
import time
from CrunchModule import poseDetector 
direction = 0
form = 0


# Accessing Video

def camselect(cam=1, file1=NONE):
    global cap
    

    if cam:
        cap = cv2.VideoCapture(0)

    else:
        cap = cv2.VideoCapture(file1)


camselect()

detector = poseDetector()


ptime = 0  # variable for fps


def test2():
    global ptime
    global direction
    global count
    global feedback

    ret, img = cap.read() #640 x 480


    img = cv2.resize(img, (960, 640))  # width, height
    
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    
    if len(lmList) != 0:
        
        shoulder = detector.findAngle(img, 25, 23, 11,False) 
        
        if shoulder>150:
            shoulder = detector.findAngle(img, 12, 24, 26)#left

        else:
            shoulder = detector.findAngle(img, 25, 23, 11) #right


        per = np.interp(shoulder, (130, 124), (100, 0))
    

        # Check for full range of motion for the Crunch
        if per == 100:
            color = (255,0,127) # Up Colour
            feedback ='Up'
            if direction == 0:
                count += 0.5
                direction = 1
                
        
        if per == 0:
            color = (102,255,255) # Down Colour
            feedback = 'Down'
            if direction == 1:
                count += 0.5
                direction = 0
        
        # Show Feedback 
        cv2.putText(img, f'{feedback}', (750, 450), cv2.FONT_HERSHEY_PLAIN, 3,
                        color, 3)

        # Counter
        cv2.rectangle(img, (0, 380), (130, 480), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 255), 5)
    
        # FPS calculation
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS = {str(int(fps))}', (20, 370),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return rgb


# GUI Code
cap = cv2.VideoCapture('2.mp4')
detector = poseDetector()
def clear():
    global count
    count = 0
clear()


def openfile():
    file1 = filedialog.askopenfilename()
    cam = 0
    camselect(cam, file1)
    clear()


def openV1():  # Code for Opening First Video
    file1 = '1.mp4'
    cam = 0
    camselect(cam, file1)
    clear()

def openV2():  # Code for Opening Second Video
    file1 = '2.mp4'
    cam = 0
    camselect(cam, file1)
    clear()



def camvideo(): # Code for WebCam 
    cam = 1
    camselect(cam)
    clear()


def close(): # To Exit Window
    window.destroy()


# Window Creation
window = Tk()
window.configure(bg='#B0EEE6')
window.title("Crunch Counter")
width = window.winfo_screenwidth()+10
height = window.winfo_screenheight()+15
window.geometry("%dx%d" % (width, height))
window.minsize(width, height)
window.maxsize(width, height)


# Design
mainlabel = Label(window, text="Crunch Counter", font=(
    "Tahoma", 20, "bold"), bg="#98FB98", fg='black')
mainlabel.pack()
Name1 = Label(window, text="Muhammad Baqir ", font=(
    "Tahoma", 16, "bold", "italic"), bg="#98FB98", fg='black')
Name1.place(x=2,y=50)
Roll1= Label(window, text="2020-MC-27", font=(
    "Tahoma", 16, "bold", "italic"), bg="#98FB98", fg='black')
Roll1.place(x=2,y=120)
Name2 = Label(window, text="Muhammad Hammad", font=(
    "Tahoma", 16, "bold", "italic"), bg="#98FB98", fg='black')
Name2.place(x=2,y=190)
Roll2= Label(window, text="2020-MC-07", font=(
    "Tahoma", 16, "bold", "italic"), bg="#98FB98", fg='black')
Roll2.place(x=2,y=260)


# Position and Design of Frame
f1 = Frame(window, bg='#B0EEE6')
f1.pack(side=BOTTOM, fill='y', anchor='nw')

# Buttons on the Frame
livecam = Button(f1, text="Open Web Cam", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=camvideo).pack()

explore = Button(f1, text="Browse ", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=openfile).pack(padx=50)
v1 = Button(f1, text="Test Video 1", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=openV1).pack(padx=50)
v2 = Button(f1, text="Test Video 2", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=openV2).pack(padx=50)
v3 = Button(f1, text="Clear", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=clear).pack(padx=50)

Exit_Application = Button(f1, text="Exit", bg='#98FB98', fg='black', font=(
    "Tahoma", 14, "bold"), command=close).pack(pady=100)


# Video Player


label1 = Label(window, width=960, height=640)
label1.place(x=240, y=50)


def select_img():
    image = Image.fromarray(test2())
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    window.after(1, select_img)


select_img()


window.mainloop()
