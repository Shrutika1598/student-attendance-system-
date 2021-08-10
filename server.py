from flask import Flask, render_template, redirect, url_for,session
from flask import request
from flask import g
import json
import numpy as np
import os
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Shrutika0707"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS attendancesystem")

db = mysql.connector.connect(user='root', password='Shrutika0707', host='127.0.0.1', database='attendancesystem', buffered=True)

mycursor = db.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS attendancesystem.student(rn INT PRIMARY KEY, fname VARCHAR(100) NOT NULL, lname VARCHAR(100) NOT NULL, image BLOB NOT NULL, class VARCHAR(100) NOT NULL, username VARCHAR(100), password VARCHAR(20))")

mycursor.execute("CREATE TABLE IF NOT EXISTS attendancesystem.attend(rn INT not null, class varchar(100) NOT NULL, time datetime not null default CURRENT_TIMESTAMP)")

mycursor.execute("CREATE TABLE IF NOT EXISTS attendancesystem.lectures(lectureName varchar(100), class varchar(100), startTime datetime, endTime datetime)")

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route("/enroll", methods=["POST"])
def enroll():
  image = []
  req_data = request.get_json()
  cur = db.cursor()
  sql = "INSERT INTO student (rn, fname, lname, image, class, username, password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
  values = (int(req_data["roll"]), req_data["fname"], req_data["lname"], json.dumps(np.asarray(req_data["image"]).tolist()) , req_data["class"], req_data["username"], req_data["password"])
  #print(values)
  res = cur.execute(sql, values)
  #print(cur.lastrowid)
  db.commit()
  return "ok"

@app.route("/createlecture", methods=["POST"])
def createLecture():
  req_data = request.get_json()
  cur = db.cursor()
  tsStart = req_data["startTime"]
  tsEnd = req_data["endTime"]
  name = req_data["name"]
  classNum = req_data["class"]
  #print(tsStart, tsEnd, name, classNum)
  cur = db.cursor()
  sql = "INSERT INTO lectures (class, lectureName, startTime, endTime) VALUES (%s, %s, %s, %s)"
  values = (classNum, name, tsStart, tsEnd)
  res = cur.execute(sql, values)
  db.commit()
  return "ok"

  
@app.route("/getclass", methods=["GET"])
def getClass():
  cur = db.cursor(buffered=True,dictionary=True)
  className = request.args.get("class").encode('ascii','ignore')
  sql = "SELECT * FROM student WHERE class = %s"
  values = (className,)
  cur.execute(sql, values)
  sendRes = []
  rows = cur.fetchall()
  for row in rows:
   # print(rows)
    data = {
	    "roll" : row["rn"],
	    "fname" : row["fname"],
	    "lname" : row["lname"],
	    "image" : row["image"],
      "username" : row["username"],
      "password" : row["password"]
	  }
    sendRes.append(data)
  return json.dumps(sendRes)

@app.route("/getattendance", methods=["GET"])
def getattendance():
  cur = db.cursor(buffered=True,dictionary=True)
  className = request.args.get("class").encode('ascii','ignore')
  startTime = request.args.get("starttime").encode('ascii','ignore')
  sql = "SELECT rn, fname, lname, class from student where rn in (select rn from lectures, attend where lectures.class = %s and lectures.startTime = %s and attend.time >= lectures.startTime and attend.time < lectures.endTime)"
  values = (className, startTime,)
  cur.execute(sql, values)
  students = []
  present = 0
  rows = cur.fetchall()
  for row in rows:
    data = {
      "roll" : row["rn"],
      "fname" : row["fname"],
      "lname" : row["lname"]
    }
    present = present + 1
    students.append(data)
  
  sql = "SELECT count(*) as count from student where class = %s"
  values = (className,)
  cur.execute(sql,values)
  total = cur.fetchone()["count"]

  sendRes = {
    "students" : students,
    "total" : total,
    "present" : present
  } 
  return json.dumps(sendRes)

@app.route("/attend", methods=["POST"])
def attend():
  req_data = request.get_json()
  cur = db.cursor()
  sql = "INSERT INTO attend (rn, class) VALUES (%s, %s)"
  values = (int(req_data["rn"]), req_data["class"])
  res = cur.execute(sql, values)
  db.commit()
  return "ok"

@app.route("/login", methods=["GET"])
def login():
  return render_template("login.html")

@app.route('/authenticator/studentProfile')
def studentProfile():
    '''firstname = request.form.get('fname')
    rollno = request.form.get('rn')
    print(firstname)
    print(rollno)'''
    if 'username' in session:  
        username = session['username']
        print(username)
    mycursor= db.cursor()
    queryString = "SELECT student.rn, student.fname, student.lname, student.class, attend.time, lectures.lectureName FROM attendancesystem.lectures INNER JOIN student ON student.class = lectures.class INNER JOIN attend ON attend.class = lectures.class ORDER BY attend.time"
    mycursor.execute(queryString)
    #print(queryString)
    myresult2=mycursor.fetchall()
    #print(myresult2)    
    for line in myresult2:
      print(myresult2)
    return render_template("studentProfile.html", myresult2 = myresult2)

@app.route('/authenticator', methods=['POST'])
def authenticator():
  username = request.form.get('uname')
  password = request.form.get('password')
  #rollno = request.form.get('rollno')
  print("username", username)
  print("password", password)

  mycursor = db.cursor()
  queryString = "select * from student where username = '"+username+"' and password = '"+password+"'" 
  #print(queryString)
  mycursor.execute(queryString)

  myresult = mycursor.fetchall()
  #print(myresult)
  for line in myresult:
    return redirect(url_for("user", uname = line[1]))
  return redirect(url_for("login"))
  #return render_template("success.html",myresult = myresult

@app.route('/user/<uname>')
def user(uname):
  #print(uname)
  return render_template("success.html", name = uname)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)