#!/usr/bin/env python
# coding: utf-8

# In[84]:


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from AttendanceDb import *
import cv2
import numpy as np
from time import strftime
from datetime import datetime
import csv
import json
class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Set the whole background to white
        self.root.configure(bg="white")

        # Create the title label
        title_lbl = Label(self.root, text="Face Recognition To Mark Attendance", font=("Arial", 30, "bold"), bg="white", fg="#4a90e2")
        title_lbl.place(relx=0.5, y=0, anchor="n", width=1530, height=45)
        
        frame = Frame(self.root, bg="white", bd=5, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # Set the border color to blue
        frame.configure(highlightbackground="#4a90e2", highlightcolor="#4a90e2", highlightthickness=2)

        # Create the label for the button instruction (same blue as title)
        instruction_lbl = Label(self.root, text="Click the button below to mark your attendance", font=("Arial", 20), bg="white", fg="#4a90e2")
        instruction_lbl.place(relx=0.5, rely=0.2, anchor="center")

        # Create a canvas for rounded button
        self.canvas = Canvas(self.root, width=300, height=100, bg="white", highlightthickness=0)
        self.canvas.pack(pady=300)
        # Initial button color (set to blue)
        self.button_color = "#4a90e2"

        # Draw rounded rectangle
        self.rounded_rectangle = self._create_rounded_rectangle(10, 10, 300, 100, 50, outline="", fill=self.button_color)

        # Create text inside the canvas (button text)
        self.canvas.create_text(150,50, text=" Mark Attendance", font=("Arial", 20, "bold"), fill="white")
        
        # Button click event handler
        self.canvas.bind("<Button-1>", self.button_click)

    # Function to draw rounded rectangle
    def _create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1,
                 x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2,
                 x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2,
                 x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    # Button click handler
    def button_click(self, event):
        # Change button color on click (green on first click, then immediate blue)
        self.button_color = "#4CAF50"  # Set green color temporarily
        self.canvas.itemconfig(self.rounded_rectangle, fill=self.button_color)  # Update to green
        # Call face recognition function
        self.face_recog()
        # Schedule a function call (using `after`) to change back to blue after a short delay
        self.root.after(100, self.change_to_blue)  # Schedule change to blue after 100 milliseconds

    def change_to_blue(self):
        # Change button color back to blue
        self.button_color = "#4a90e2"
        self.canvas.itemconfig(self.rounded_rectangle, fill=self.button_color)  # Update to blue
####################################### ATTENDANCE MARK ######################################


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


            
            
############################## FACE RECOGNITION #############################     

    def face_recog(self):
        recorded_ids = set()
        with open('label_map.json', 'r') as f:
           label_map = json.load(f)
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

            coord = []

            for (x, y, w, h) in features:
                # Resize the face region to the size used during training (usually 200x200)
                face_resized = cv2.resize(gray_image[y:y+h, x:x+w], (200, 200))
                id, confidence = clf.predict(face_resized)
                print(f"Predicted ID: {id}, Confidence: {confidence}")
                print(f"Label Map: {label_map}")

                ######################## Database section ############################
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="face_recognizer")
                my_cursor = conn.cursor()

                # Fetch Name
                my_cursor.execute("select Name from student where Student_id=%s", (str(id),))
                n = my_cursor.fetchone()
                n = n[0] if n else "Unknown"

                # Fetch Roll
                my_cursor.execute("select Roll from student where Student_id=%s", (str(id),))
                r = my_cursor.fetchone()
                r = r[0] if r else "Unknown"

                # Fetch Department
                my_cursor.execute("select Dep from student where Student_id=%s", (str(id),))
                d = my_cursor.fetchone()
                d = d[0] if d else "Unknown"

                # Use confidence directly, where lower confidence means better match
                if confidence < 50:  # Face recognized
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)  # Draw green rectangle for recognized face
                    cv2.putText(img, f"Roll: {r}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                    cv2.putText(img, f"Name: {n}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                    cv2.putText(img, f"Department: {d}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 3)
                    if id not in recorded_ids:
                       self.mark_attendance(id, r, n, d)  # Call the mark_attendance function
                       recorded_ids.add(id)  

                else:  # Face not recognized
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)  # Draw red rectangle for unknown face
                    cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]
                conn.close()  # Ensure the connection is closed properly

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        # Load the face detection model and trained recognizer model
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("Trainner.yml")  # Ensure this file exists and is correctly trained

        # Start video capture
        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to capture video")
                break
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome To Face Recognition Attendance System", img)
            
            if cv2.getWindowProperty("Welcome To Face Recognition Attendance System", cv2.WND_PROP_VISIBLE) < 1:
              break
            # Break loop on 'Enter' key press
            if cv2.waitKey(1) == 13:
                break

        # Release the camera and close any open windows
        video_cap.release()
        cv2.destroyAllWindows()

            
        
        
        
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()


# In[ ]:




