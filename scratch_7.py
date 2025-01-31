from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from AttendanceDb import *  # Assuming this is your custom module for attendance database
import cv2
import numpy as np
from time import strftime
from datetime import datetime
import csv
import json
import mysql.connector
import logging

class Face_Recognition:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.attendance_marked = False  # Flag to indicate if attendance has been marked
        self.new_student = True

        # Set the whole background to white
        self.root.configure(bg="white")

        # Close event handler to ensure the program exits
        # self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the title label
        title_lbl = Label(self.root, text="Face Recognition To Mark Attendance", font=("Arial", 30, "bold"), bg="white",
                          fg="#4a90e2")
        title_lbl.place(relx=0.5, y=0, anchor="n", width=1530, height=45)

        frame = Frame(self.root, bg="white", bd=5, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # Set the border color to blue
        frame.configure(highlightbackground="#4a90e2", highlightcolor="#4a90e2", highlightthickness=2)

        # Create the label for the button instruction (same blue as title)
        instruction_lbl = Label(self.root, text="Click the button below to mark your attendance", font=("Arial", 20),
                                bg="white", fg="#4a90e2")
        instruction_lbl.place(relx=0.5, rely=0.2, anchor="center")

        # Create a canvas for rounded button
        self.canvas = Canvas(self.root, width=300, height=100, bg="white", highlightthickness=0)
        self.canvas.pack(pady=300)

        # Initial button color (set to blue)
        self.button_color = "#4a90e2"

        # Draw rounded rectangle
        self.rounded_rectangle = self._create_rounded_rectangle(10, 10, 300, 100, 50, outline="",
                                                                fill=self.button_color)
        # Create text inside the canvas (button text)
        self.canvas.create_text(150, 50, text=" Mark Attendance", font=("Arial", 20, "bold"), fill="white")

        # Button click event handler
        self.canvas.bind("<Button-1>", self.button_click)

    def on_closing(self):
        self.attendance_marked = True
        self.root.destroy()

    def _create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1,
                  x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2,
                  x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2,
                  x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

        # Button click handler
    def button_click(self, event):
    # Reset flag before starting face recognition
        self.attendance_marked = False
        self.face_recog()  # Call face recognition function

    def mark_attendance(self, i, r, n, d):
        with open("StudentDetails/StudentDetails.csv", "r+", newline="\n", encoding="utf-8") as f:
            myDataList = f.readlines()
            name_list = []

            # Parse through existing records to extract IDs
            for line in myDataList:
                entry = line.split(",")  # Split by commas since it's a CSV
                name_list.append(entry[0])  # Assuming ID (i) is in the first column

            # Check if the student ID is already in the list
            if i not in name_list:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")  # Current date
                dtString = now.strftime("%H:%M:%S")  # Current time

                # Open the CSV in append mode and use csv.writer to write the new row
                with open("StudentDetails/StudentDetails.csv", "a", newline="\n", encoding="utf-8") as f_append:
                    csv_writer = csv.writer(f_append)

                    # Write the new attendance entry (ID, Roll, Name, Department, Time, Date, Status)
                    csv_writer.writerow([i, r, n, d, dtString, d1, "Present"])

    def face_recog(self):
        recorded_ids = set()
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("D:\Face-Recognition-Based-Attendance-Monitoring-System\lbph_trained_model.yml")  # Ensure this file exists and is correctly trained

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to capture video")
                break

            # Convert to grayscale and detect faces
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in features:
                face_resized = cv2.resize(gray_image[y:y + h, x:x + w], (200, 200))
                id, confidence = clf.predict(face_resized)

                conn = mysql.connector.connect(host="localhost", user="root", password="", database="face_recognizer")
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT Name FROM student WHERE Student_id=%s", (str(id),))
                n = my_cursor.fetchone()
                n = n[0] if n else "Unknown"

                my_cursor.execute("SELECT Roll FROM student WHERE Student_id=%s", (str(id),))
                r = my_cursor.fetchone()
                r = r[0] if r else "Unknown"

                my_cursor.execute("SELECT Dep FROM student WHERE Student_id=%s", (str(id),))
                d = my_cursor.fetchone()
                d = d[0] if d else "Unknown"

                print('biba')

                if confidence < 50:
                    self.new_student = False
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)

                    if id not in recorded_ids:
                        self.mark_attendance(id, r, n, d)
                        recorded_ids.add(id)
                        self.attendance_marked = True  # Stop further detection

                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.new_student = True

                conn.close()

            cv2.imshow("Welcome To Face Recognition Attendance System", img)

            if cv2.getWindowProperty("Welcome To Face Recognition Attendance System", cv2.WND_PROP_VISIBLE) < 1:
                break
            if cv2.waitKey(1) == 13 or self.attendance_marked:
                break
            # print('abc')
            print(self.attendance_marked)
            # Exit loop if attendance has been marked
            if self.attendance_marked:
                break

        video_cap.release()
        cv2.destroyAllWindows()
        if self.attendance_marked or self.new_student:
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.protocol("WM_DELETE_WINDOW", obj.on_closing)  # Bind on_closing to close event
    root.mainloop()
