import os
from time import sleep
import cv2
import face_recognition
from datetime import datetime
import keyboard
import csv


class Personne:
    def __init__(self, id, name, lname, image) -> None:
        self.id = id
        self.name = name
        self.lname = lname
        self.image = image
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getFaceEncodings(self):
        image = face_recognition.load_image_file(self.image)
        return face_recognition.face_encodings(image)
        
            
    pass


dir = "./ImagesAttendance/"



def loadEmp():
    employees = []
    with open('dataEmp.csv','r+')as f:
        reader_obj = csv.reader(f)
        for row in reader_obj:
            employees.append(Personne(row[0], row[1], row[2], dir + row[3]))
            
        f.close()
    return employees



def getEmp(id):
    with open('dataEmp.csv','r+')as f:
        reader_obj = csv.reader(f)
        for row in reader_obj:  
            if( row[0] == id ): return [row[0], row[1], row[2], row[3]] 


#fonction pour role de remplir le fichier csv qui concerne les presenece des employes
def markAttendance(id):
    with open('Attendance.csv', 'r+', newline='') as f:
        reader_obj = csv.reader(f)
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')

        if os.stat("Attendance.csv").st_size == 0:
            emp = getEmp(id)
            id, clockIn = emp[0], "Clock IN"
            writer = csv.writer(f)
            writer.writerow([id, dtString, clockIn])
        else:
            for row in reader_obj:
                if (row[0] == id):
                    id = row[0]
                    if row[2] == "Clock IN": clockIn = "Clock OUT"
                    if row[2] == "Clock OUT": clockIn = "Clock IN"
                else:
                    emp = getEmp(id)
                    id, clockIn = emp[0], "Clock IN"

            print("Inserted")
            writer = csv.writer(f)
            writer.writerow([id, dtString, clockIn])
cap = cv2.VideoCapture(0)

empData = []
empFE = []

for emp in loadEmp():
    empData.append(emp)
    empFE.append(emp.getFaceEncodings()[0])
     
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    if keyboard.is_pressed('q'):
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        print(encodesCurFrame)

    
    if keyboard.is_pressed('i'):
        sleep(0.2)
        matchs = face_recognition.compare_faces(empFE, encodesCurFrame[0])    
        print(matchs)
        if True in matchs:
            first_match_index = matchs.index(True)
        
        markAttendance(empData[first_match_index].getID())

    
    if keyboard.is_pressed('b'):
        quit()

    cv2.imshow('test',img)
    cv2.waitKey(1)
