import cv2
import numpy as np
import threading

import tkinter
from tkinter import Tk, Radiobutton, IntVar, Entry, Button, Label, StringVar, Checkbutton

import time
from datetime import datetime

import sys



###
### setting variables
###
camera = 0              # which camera to use
orientation = False     # True: scans width (horizontal), False: scans height (vertical)
mirror = True           # True: mirrors the video image, False: do nothing
duration = 10           # scan duration in seconds
filename = "{time}"     # filename to save the resulting image
closed = True           # camera wont open after closing the GUI, if this is set to True (flag for continuing)


###
### GUI operations
###
def selectOrientation():
    global orientation
    orientation = orientation_var.get()
def setMirror():
    global mirror
    mirror = mirror_var.get()

def validate(event=None):
    global duration, filename, closed
    # print(duration_var.get())
    try:
        duration = int(duration_var.get())
    except Exception as e:
        message_var.set("Duration must be integer (in seconds)!")
        return
    if not (3 <= duration <= 30):
        message_var.set("Duration must be at least 3 and at most 30!")
        return
    filename = filename_var.get()
    closed = False
    root.destroy()

root = Tk()
root.geometry("250x300")
orientation_var = IntVar()
radio1 = Radiobutton(root, text="Horizontal", variable=orientation_var, value=1, command=selectOrientation)
radio2 = Radiobutton(root, text="Vertical", variable=orientation_var, value=0, command=selectOrientation)
radio1.pack()
radio2.pack()
radio2.select()

mirror_var = IntVar()
mirror_checkbox = Checkbutton(root, text="Mirror Camera", variable=mirror_var, onvalue=1, offvalue=0, command=setMirror)
mirror_checkbox.pack(pady=(10,0))
mirror_checkbox.select()

duration_label = Label(text="Duration (seconds):"); duration_label.pack(pady=(10,0))
duration_var = StringVar()
duration_var.set("10")
duration_entry = Entry(root, textvariable=duration_var); 
duration_entry.pack()

filename_label = Label(text="Filename (to save image):"); filename_label.pack(pady=(10,0))
filename_var = StringVar()
filename_var.set("{time}")
filename_entry = Entry(root, textvariable=filename_var); 
filename_entry.pack()

message_var = StringVar()
message_var.set("Press OK to start")
message_label = Label(root, textvariable=message_var); message_label.pack(pady=(20,0))

confirm = Button(root, text="OK", width=100, height=8, bg="#6b6", command=validate); 
root.bind("<Return>", validate)
root.bind("<Escape>", lambda x: root.destroy())
confirm.pack()

root.mainloop()


if closed:      # window closed without pressing the OK button
    sys.exit()


print("> Preparing camera...")


def getTimestampString():
    return "_".join(str(datetime.now()).split(" ")).replace(":", ".")[:-7]


duration -= 3           # it lasts ~3 sec longer than given value, so decrement by 3. 
                        # (TODO: for more accurate result, use timer instead of sleep)
scan = 0
vid = cv2.VideoCapture(camera)
vid.set(3, 1920)
vid.set(4, 1080)
_, frame = vid.read()
# frame = cv2.flip(frame, 1)
h, w = frame.shape[:2]
res = frame.copy()
cpy = res.copy()

# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter("output.avi", fourcc, 30.0, (w, h))

# duration      sec  -> w            px
# 1             sec  -> w/duration   px
# duration/w    sec  -> 1            px


# helper function. provides atomicity
def read_frame():
    global vid, mirror 
    _, frame_local = vid.read()
    if mirror:
        frame_local = cv2.flip(frame_local, 1)
    return frame_local


# thread target function
def scanner():
    global w, h, duration, frame, cpy, res, scan
    print("> Started Scanning\n")

    if orientation:
        while scan < w:
            cpy = res.copy()
            cpy = cv2.rectangle(cpy, (scan, 0), (scan, h-1), (0,255,0), 1)
            res[:, scan:w] = frame[:, scan:w]
            time.sleep(duration/w)
            scan += 1
    else:
        while scan < h:
            cpy = res.copy()
            cpy = cv2.rectangle(cpy, (0, scan), (w-1, scan), (0,255,0), 1)
            res[scan:h, :] = frame[scan:h, :]
            time.sleep(duration/h)
            scan += 1


# thread target function
def displayer():
    global w, h, duration, frame, cpy, res, scan, filename
    condition = w if orientation else h

    start_time = time.time()
    
    while scan < condition:
        frame = read_frame()
        cv2.imshow("final", cpy)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        # print(scan)


    end_time = time.time()
    scan = w if orientation else h
    print("scan duration:", end_time - start_time)
    
    vid.release()
    # out.release()
    cv2.destroyAllWindows()
    if filename == "{time}":
        filename = getTimestampString()
    cv2.imwrite(filename + ".jpg", res)
    print("> Image saved.\n")



t1 = threading.Thread(target=displayer);
t2 = threading.Thread(target=scanner);

t1.start()
time.sleep(1)
t2.start()
t1.join()
t2.join()
