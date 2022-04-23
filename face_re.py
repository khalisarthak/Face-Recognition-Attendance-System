import cv2
import os
import face_recognition
import numpy as np
from datetime import datetime
now = datetime.now()

def markAttendance(name): 
    file_ = os.path.exists(f'Attendance/{now.strftime("%d-%B-%Y")}.csv')
    if not file_:
        f = open(f'Attendance/{now.strftime("%d-%B-%Y")}.csv', "w")
        f.close()
    
    with open(f'Attendance/{now.strftime("%d-%B-%Y")}.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:   
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'\n{name}, {time}')
            

path = 'student_images'
images = []
classNames = []

mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

present_files = []
for cl in mylist:
    present_files.append(os.path.splitext(cl)[0].upper())

def TakeImages():
    student_name = name.get().upper()
    if ((student_name.isalpha())):
        if student_name not in present_files:
    
            cap=cv2.VideoCapture(0)
            while True:
                ret, img= cap.read()
                img_copy = img.copy()
                try:
                    faceloc = face_recognition.face_locations(img)[0]
                    y1,x2,y2,x1 = faceloc
                    imgS = img_copy[y1-10:y2+10,x1-5:x2+5]
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                except:
                    pass
                cv2.imshow('Take Picture',img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    try:
                        cv2.imwrite(f'.\student_images\{student_name}.jpg', imgS)
                        present_files.append(student_name)
                    except:
                        pass
                    break
                
            cap.release()
            cv2.destroyAllWindows()
                   
                
            cap.release()
            cv2.destroyAllWindows()
            
def TrackImages():
    encoded_face_train = findEncodings(images)

    cap  = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

        for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper().lower()
                y1,x2,y2,x1 = faceloc
                x1 = x1*4
                y2 = y2*4
                y1 = y1*4
                x2  = x2*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(img,name.upper(), (x1+6,y2+30), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name.upper())
            else:
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, 'Not Registered', (x1 + 6, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    

import tkinter as tk
from tkinter import *
import os

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Face Recognition Attendane System")


b1 = PhotoImage(file = "back.png")
lab1 = tk.Label(window, image = b1, width=1400, height=1100)
lab1.place(x=0,y=0)

frame1 = tk.Frame(window, bg='')
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.30)

lab2 = tk.Label(frame1, image = b1, width=600, height=800)
lab2.place(x=0,y=0)

frame2 = tk.Frame(window, bg="gray")
frame2.place(relx=0.11, rely=0.50, relwidth=0.39, relheight=0.30)

lab3 = tk.Label(frame2, image = b1, width=600, height=800)
lab3.place(x=0,y=0)

frame3 = tk.Frame(window, bg="white")
frame3.place(relx=0.53, rely=0.17, relwidth=0.35, relheight=0.63)

b = PhotoImage(file = "face_rec.png")
lab = tk.Label(frame3, image = b, width=445, height=450)
lab.place(x=0,y=0)

message3 = tk.Label(window, text="Face Recognition Attendance System" ,fg="white",bg="black" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

head2 = tk.Label(frame2, text="                                   REGISTER                             ", fg="white",bg="black" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                                    LOGIN                                 ", fg="white",bg="black" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl2 = tk.Label(frame2, text="Enter Name",width=12  ,fg="white",bg="black" ,font=('times', 17, ' bold '))
lbl2.place(x=150, y=50)

name = tk.Entry(frame2,width=34 ,fg="black",font=('times', 15, ' bold ')  )
name.place(x=50, y=100)
 
takeImg = tk.Button(frame2, text="Register", command=TakeImages  ,fg="white"  ,bg="black"  ,width=28  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=50, y=150)

trackImg = tk.Button(frame1, text="Mark Attendance", command=TrackImages  ,fg="white"  ,bg="black"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Exit", command=window.destroy  ,fg="white"  ,bg="black"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=120)

window.mainloop()