import numpy as np
import cv2
import face_recognition
import os
import tkinter as tk
from tkinter.messagebox import showinfo
import requests
from PIL import Image, ImageTk
import json

classId = 0

class Home:
  def __init__(self, master):
    self.master = master
    self.frame = tk.Frame(self.master)
    self.labelClass = tk.Label(self.frame, text="Class")
    self.labelClass.grid(row=1,column=1)
    self.textClass = tk.Text(self.frame, height=1, width=10)
    self.textClass.grid(row=1,column=2)
    self.button1 = tk.Button(self.frame, text = 'Start', width = 25, command = self.new_window)
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.button1.grid(row=2,column=1, columnspan=2)
    self.quitButton.grid(row=3,column=1, columnspan=2)
    self.frame.grid(row=4,column=1)

  def new_window(self):
    self.newWindow = tk.Toplevel(self.master)
    self.app = Detect(self.newWindow, self.textClass.get("1.0","end-1c"))
        
  def close_windows(self):
    self.master.destroy()

class Detect:
  def __init__(self, master, cls):
    global classId
    self.master = master
    self.frame = tk.Frame(self.master)
    self.master.title("Detect")
    self.knownFaceEncode = []
    self.FNames = []
    self.LNames = []
    self.Rolls = []
    classId = cls
    URL = "http://localhost/getclass?class="+cls
    res = requests.get(url=URL)
    if res.status_code == 200:
      records = res.json()
      for record in records:
        self.knownFaceEncode.append(np.asarray(json.loads(record["image"])))
        self.FNames.append(record["fname"])
        self.LNames.append(record["lname"])
        self.Rolls.append(record["roll"])
    #Change this if camera not found
    self.master.vs = cv2.VideoCapture(1)
    self.master.current_image = None
    self.panel = tk.Label(self.master)
    self.panel.grid(row=1, column=2, columnspan=2)
    
    self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
    self.quitButton.grid(row=6,column=2)
    self.frame.grid(row=2,column=2)
    self.video_loop()
        
  def video_loop(self):
    global classId
    ok, frame = self.master.vs.read()
    if ok:
      key = cv2.waitKey(1000)
      self.cv2image = frame[:, :, ::-1]
      self.current_image = Image.fromarray(self.cv2image)
      imgtk = ImageTk.PhotoImage(image=self.current_image)
      self.panel.imgtk = imgtk
      self.panel.config(image=imgtk)
      matchLoc = face_recognition.face_locations(self.cv2image)
      matchEncodes = face_recognition.face_encodings(self.cv2image, matchLoc)
      for matchEncode in matchEncodes:
        matches = face_recognition.compare_faces(self.knownFaceEncode, matchEncode, tolerance=0.5)
        if True in matches:
          #print self.knownFaceEncode
          #print matchEncode
          #print matches
          first_match_index = matches.index(True)
          #self.current_image.save("save"+str(self.Rolls[first_match_index])+".png")
          URL = "http://localhost/attend"
          headers = {"Content-Type": "application/json"}
          data = {
            "rn" : self.Rolls[first_match_index],
            "class" : classId,
          }
          res = requests.post(url=URL, data=json.dumps(data), headers=headers)
          if res.status_code == 200:
            print (self.Rolls[first_match_index], self.FNames[first_match_index], self.LNames[first_match_index], classId)
          self.knownFaceEncode = self.knownFaceEncode[:first_match_index] + self.knownFaceEncode[first_match_index+1 :] 
          self.Rolls = self.Rolls[:first_match_index] + self.Rolls[first_match_index+1 :]
          self.FNames = self.FNames[:first_match_index] + self.FNames[first_match_index+1 :]
          self.LNames = self.LNames[:first_match_index] + self.LNames[first_match_index+1 :]
 
    self.master.after(1, self.video_loop)

  def close_windows(self):
    self.master.vs.release()
    self.master.destroy()

def main(): 
  root = tk.Tk()
  app = Home(root)
  root.mainloop()

if __name__ == '__main__':
  main()