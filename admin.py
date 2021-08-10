import tkinter as tk
from tkinter.messagebox import showinfo
import cv2
from PIL import Image, ImageTk
import face_recognition
import requests
import json
import os
import numpy as np

class Home:
  def __init__(self, master):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.button1 = tk.Button(self.frame, text = 'Enroll', width = 25, command = self.new_window)
    self.button2 = tk.Button(self.frame, text = 'Create Lecture', width = 25, command = self.create_class)
    self.button3 = tk.Button(self.frame, text = 'Take Attendance', width = 25, command = self.take_attendance)
    self.button4 = tk.Button(self.frame, text = 'See Attendance', width = 25, command = self.see_attend)
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.button1.pack()
    self.button2.pack()
    self.button3.pack()
    self.button4.pack()
    self.quitButton.pack()
    self.frame.pack()

  def new_window(self):
    self.newWindow = tk.Toplevel(self.master)
    self.app = Enroll(self.newWindow)

  def create_class(self):
    self.newWindow = tk.Toplevel(self.master)
    self.app = createClass(self.newWindow)

  def take_attendance(self):
    os.system('python detect.py')

  def see_attend(self):
    self.newWindow = tk.Toplevel(self.master)
    self.app = seeAttend(self.newWindow)

  def close_windows(self):
    self.master.destroy()

class seeAttend:
  def __init__(self, master, output_path = "./"):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.master.title("See Attendance")
    self.panel = tk.Label(self.master)
    self.panel.grid(row=1, column=2, columnspan=2)
    self.labelClass = tk.Label(self.frame, text="Class")
    self.labelClass.grid(row=2,column=1)
    self.textClass = tk.Text(self.frame, height=1, width=25)
    self.textClass.grid(row=2,column=2)
    self.labelYear = tk.Label(self.frame, text="Year")
    self.labelYear.grid(row=3,column=1)
    self.textYear = tk.Text(self.frame, height=1, width=25)
    self.textYear.grid(row=3,column=2)
    self.labelMonth = tk.Label(self.frame, text="Month")
    self.labelMonth.grid(row=4,column=1)
    self.textMonth = tk.Text(self.frame, height=1, width=25)
    self.textMonth.grid(row=4,column=2)
    self.labelDay = tk.Label(self.frame, text="Day")
    self.labelDay.grid(row=5,column=1)
    self.textDay = tk.Text(self.frame, height=1, width=25)
    self.textDay.grid(row=5,column=2)
    self.labelStartHour = tk.Label(self.frame, text="Start Hour")
    self.labelStartHour.grid(row=6,column=1)
    self.textStartHour = tk.Text(self.frame, height=1, width=25)
    self.textStartHour.grid(row=6,column=2)
    self.labelStartMin = tk.Label(self.frame, text="Start Min")
    self.labelStartMin.grid(row=7,column=1)
    self.textStartMin = tk.Text(self.frame, height=1, width=25)
    self.textStartMin.grid(row=7,column=2)
    self.btn = tk.Button(self.frame, text="See Attendance", width = 25, command=self.see_attendance)
    self.btn.grid(row=8,column=1)
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.quitButton.grid(row=8,column=2)
    self.frame.grid(row=2,column=2)

  def see_attendance(self):
    startTime  = self.textYear.get("1.0","end-1c")+"-"+self.textMonth.get("1.0","end-1c")+"-"+self.textDay.get("1.0","end-1c")+" "+self.textStartHour.get("1.0","end-1c")+":"+self.textStartMin.get("1.0","end-1c")+":00"
    URL = "http://localhost/getattendance?class="+self.textClass.get("1.0","end-1c")+"&starttime="+startTime
    res = requests.get(url=URL)
    if res.status_code == 200:
      #print res.text
      self.newWindow = tk.Toplevel(self.master)
      self.app = listAttend(self.newWindow, data=res.text)
      #showinfo("Window", res.text)

  def close_windows(self):
    self.master.destroy()

class listAttend:
  def __init__(self, master, data, output_path = "./"):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.master.title("See Attendance")
    self.panel = tk.Label(self.master)
    self.panel.grid(row=1, column=2, columnspan=3)
    fullData = json.loads(data)
    self.labelPresent = tk.Label(self.frame, text="Present")
    self.labelPresent.grid(row=2, column=1, columnspan=2)
    self.labelPresentText = tk.Label(self.frame, text=fullData["present"])
    self.labelPresentText.grid(row=2, column=3)
    self.labelTotal= tk.Label(self.frame, text="Total")
    self.labelTotal.grid(row=3, column=1, columnspan=2)
    self.labelTotalText = tk.Label(self.frame, text=fullData["total"])
    self.labelTotalText.grid(row=3, column=3)
    self.emptyLabel = tk.Label(self.frame, text="")
    self.emptyLabel.grid(row=4, column=2, columnspan=3)
    #print data
    row = 5
    for item in fullData["students"]:
      print(item)
      self.labelLname = tk.Label(self.frame, text=item["roll"])
      self.labelLname.grid(row=row,column=1)
      self.labelLname = tk.Label(self.frame, text=item["fname"])
      self.labelLname.grid(row=row,column=2)
      self.labelLname = tk.Label(self.frame, text=item["lname"])
      self.labelLname.grid(row=row,column=3)
      row = row + 1


    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.quitButton.grid(row=row,column=2)
    self.frame.grid(row=row,column=3)

  def close_windows(self):
    self.master.destroy()

class createClass:
  def __init__(self, master, output_path = "./"):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.master.title("Create Lecture")
    self.panel = tk.Label(self.master)
    self.panel.grid(row=1, column=2, columnspan=2)
    self.labelLectName = tk.Label(self.frame, text="Lecture Name")
    self.labelLectName.grid(row=2,column=1)
    self.textLectName = tk.Text(self.frame, height=1, width=25)
    self.textLectName.grid(row=2,column=2)
    self.labelClass = tk.Label(self.frame, text="Class")
    self.labelClass.grid(row=3,column=1)
    self.textClass = tk.Text(self.frame, height=1, width=25)
    self.textClass.grid(row=3,column=2)
    self.labelYear = tk.Label(self.frame, text="Year")
    self.labelYear.grid(row=4,column=1)
    self.textYear = tk.Text(self.frame, height=1, width=25)
    self.textYear.grid(row=4,column=2)
    self.labelMonth = tk.Label(self.frame, text="Month")
    self.labelMonth.grid(row=5,column=1)
    self.textMonth = tk.Text(self.frame, height=1, width=25)
    self.textMonth.grid(row=5,column=2)
    self.labelDay = tk.Label(self.frame, text="Day")
    self.labelDay.grid(row=6,column=1)
    self.textDay = tk.Text(self.frame, height=1, width=25)
    self.textDay.grid(row=6,column=2)
    self.labelStartHour = tk.Label(self.frame, text="Start Hour")
    self.labelStartHour.grid(row=7,column=1)
    self.textStartHour = tk.Text(self.frame, height=1, width=25)
    self.textStartHour.grid(row=7,column=2)
    self.labelStartMin = tk.Label(self.frame, text="Start Min")
    self.labelStartMin.grid(row=8,column=1)
    self.textStartMin = tk.Text(self.frame, height=1, width=25)
    self.textStartMin.grid(row=8,column=2)
    self.labelEndHour = tk.Label(self.frame, text="End Hour")
    self.labelEndHour.grid(row=9,column=1)
    self.textEndHour = tk.Text(self.frame, height=1, width=25)
    self.textEndHour.grid(row=9,column=2)
    self.labelEndMin = tk.Label(self.frame, text="End Min")
    self.labelEndMin.grid(row=10,column=1)
    self.textEndMin = tk.Text(self.frame, height=1, width=25)
    self.textEndMin.grid(row=10,column=2)
    self.btn = tk.Button(self.frame, text="Create Class", width = 25, command=self.add_class)
    self.btn.grid(row=11,column=1)
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.quitButton.grid(row=11,column=2)
    self.frame.grid(row=2,column=2)

  def add_class(self):
    headers = {"Content-Type": "application/json"}
    startTime  = self.textYear.get("1.0","end-1c")+"-"+self.textMonth.get("1.0","end-1c")+"-"+self.textDay.get("1.0","end-1c")+" "+self.textStartHour.get("1.0","end-1c")+":"+self.textStartMin.get("1.0","end-1c")+":00"
    endTime  = self.textYear.get("1.0","end-1c")+"-"+self.textMonth.get("1.0","end-1c")+"-"+self.textDay.get("1.0","end-1c")+" "+self.textEndHour.get("1.0","end-1c")+":"+self.textEndMin.get("1.0","end-1c")+":00"
    data = {
    "name" : self.textLectName.get("1.0","end-1c"), 
    "class" : self.textClass.get("1.0","end-1c"), 
    "startTime" : startTime,
    "endTime"  : endTime
    }
    URL = "http://localhost/createlecture"
    res = requests.post(url=URL, data=json.dumps(data), headers=headers)
    if res.status_code == 200:
      showinfo("Window", res.text)

  def close_windows(self):
    self.master.destroy()

class Enroll:
  def __init__(self, master, output_path = "./"):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.master.title("Enroll")
    self.master.vs = cv2.VideoCapture(1)
    self.master.current_image = None
    self.panel = tk.Label(self.master)
    self.panel.grid(row=1, column=2, columnspan=2)

    self.labelFName = tk.Label(self.frame, text="First Name")
    self.labelFName.grid(row=2,column=1)
    self.textFname = tk.Text(self.frame, height=1, width=25)
    self.textFname.grid(row=2,column=2)

    self.labelLName = tk.Label(self.frame, text="Last Name")
    self.labelLName.grid(row=3,column=1)
    self.textLname = tk.Text(self.frame, height=1, width=25)
    self.textLname.grid(row=3,column=2)

    self.labelClass = tk.Label(self.frame, text="Class")
    self.labelClass.grid(row=4,column=1)
    self.textClass = tk.Text(self.frame, height=1, width=25)
    self.textClass.grid(row=4,column=2)

    self.labelRoll = tk.Label(self.frame, text="Roll")
    self.labelRoll.grid(row=5,column=1)
    self.textRoll = tk.Text(self.frame, height=1, width=25)
    self.textRoll.grid(row=5,column=2)

    self.labelUsername = tk.Label(self.frame, text="Username")
    self.labelUsername.grid(row=6,column=1)
    self.textUsername = tk.Text(self.frame, height=1, width=25)
    self.textUsername.grid(row=6,column=2)

    self.labelPassword = tk.Label(self.frame, text="Password")
    self.labelPassword.grid(row=7,column=1)
    self.textPassword = tk.Text(self.frame, height=1, width=25)
    self.textPassword.grid(row=7,column=2)
    
    self.btn = tk.Button(self.frame, text="Snapshot!", width = 25, command=self.take_snapshot)
    self.btn.grid(row=8,column=1)
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.quitButton.grid(row=8,column=2)
    self.frame.grid(row=2,column=2)
    self.video_loop()

  def video_loop(self):
    ok, frame = self.master.vs.read()
    if ok:
      key = cv2.waitKey(1000)
      self.cv2image = frame[:, :, ::-1]
      self.current_image = Image.fromarray(self.cv2image)
      imgtk = ImageTk.PhotoImage(image=self.current_image) 
      self.panel.imgtk = imgtk
      self.panel.config(image=imgtk)
    
    self.master.after(1, self.video_loop)

  def take_snapshot(self):
    self.current_image.save("click.png")
    #print self.current_image
    #print self.cv2image
    matchLoc = face_recognition.face_locations(self.cv2image)
    matchEncodes = face_recognition.face_encodings(self.cv2image, matchLoc)
    headers = {"Content-Type": "application/json"}
    enrollData = {
    "fname" : self.textFname.get("1.0","end-1c"), 
    "lname" : self.textLname.get("1.0","end-1c"), 
    "class" : self.textClass.get("1.0","end-1c"),
    "roll"  : self.textRoll.get("1.0","end-1c"),
    "image" : matchEncodes[0].tolist(),
    "username"  : self.textUsername.get("1.0","end-1c"),
    "password"  : self.textPassword.get("1.0","end-1c")
    }
    URL = "http://localhost/enroll"
    res = requests.post(url=URL, data=json.dumps(enrollData), headers=headers)
    if res.status_code == 200:
      self.close_windows()
    else:
      showinfo("Window", res.text)

  def close_windows(self):
    self.master.vs.release()
    self.master.destroy()

def main(): 
  root = tk.Tk()
  app = Home(root)
  root.mainloop()

if __name__ == '__main__':
  main()
