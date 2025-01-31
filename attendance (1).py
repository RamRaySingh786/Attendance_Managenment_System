#!/usr/bin/env python
# coding: utf-8

# In[23]:


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import from PIL (Python Imaging Library)
#import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        # Set the whole background to white
        self.root.configure(bg="white")
        
        main_frame = Frame(bd=4)
        main_frame.place(x=20, y=80, width=1400, height=600)

        # Create the title label
        title_lbl = Label(self.root, text="Attendance Management", font=("Arial", 30, "bold"), bg="white", fg="#4a90e2")
        title_lbl.place(relx=0.5, y=0, anchor="n", width=1530, height=45)

        # Left frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Attendance Details", fg="#4A90E2", font=("Arial", 13, "bold"))
        left_frame.place(x=10, y=10, width=600, height=590)

        # Load and resize the image
        img_left = Image.open(r"ab.jpeg")  # Ensure the path is correct
        img_left = img_left.resize((720, 130), Image.ANTIALIAS)  # Resize the image
        self.photoimg = ImageTk.PhotoImage(img_left)

        # Display the image in the label
        f_lbl = Label(left_frame, image=self.photoimg)
        f_lbl.place(x=5, y=0, width=720, height=130)

        # Left inside frame
        left_inside_frame = Frame(left_frame, bd=2, relief=RIDGE, bg="white")
        left_inside_frame.place(x=0, y=135, width=720, height=370)

        # Label and entry
        # Attendance ID
        attendanceId_label = Label(left_inside_frame, text="Attendance ID:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        attendanceId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        attendanceID_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        attendanceID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Roll label
        rollLabel = Label(left_inside_frame, text="Roll:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        rollLabel.grid(row=0, column=2, padx=4, pady=8)
        rollLabel_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        rollLabel_entry.grid(row=0, column=3, padx=4, pady=8)

        # Name label
        nameLabel = Label(left_inside_frame, text="Name:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        nameLabel.grid(row=1, column=0)
        nameLabel_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        nameLabel_entry.grid(row=1, column=1,pady=8)
        
        # Department label
        deptLabel = Label(left_inside_frame, text="Department:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        deptLabel.grid(row=1, column=2)
        deptLabel_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        deptLabel_entry.grid(row=1, column=3,pady=8)
        
        # Time label
        timeLabel = Label(left_inside_frame, text="Time:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        timeLabel.grid(row=2, column=0)
        timeLabel_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        timeLabel_entry.grid(row=2, column=1,pady=8)
        
        # Date label
        DateLabel = Label(left_inside_frame, text="Date:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        DateLabel.grid(row=2, column=2)
        DateLabel_entry = ttk.Entry(left_inside_frame, width=20, font=("Arial", 11, "bold"))
        DateLabel_entry.grid(row=2, column=3,pady=8)
        
        # Attendance label
        attendanceLabel = Label(left_inside_frame, text="Attendance Status:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        attendanceLabel.grid(row=3, column=0)

        # Attendance dropdown (combobox) with options "Present" and "Absent"
        attendanceLabel_combobox = ttk.Combobox(left_inside_frame, width=20, font=("Arial", 10),state="readonly")
        attendanceLabel_combobox['values'] = ('Present', 'Absent')  # Options for the dropdown
        attendanceLabel_combobox.grid(row=3, column=1, pady=8)

        
        #Buttons frame 
        btn_frame = Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=300,width=595,height=35)
        
        import_button = Button (btn_frame,text="Import csv", width=13,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        import_button.grid(row=0,column=0)
        
        export_button = Button (btn_frame,text="Export csv", width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        export_button.grid(row=0,column=1)
        
        update_button = Button (btn_frame,text="Update", width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        update_button.grid(row=0,column=2)
        
        reset_button = Button (btn_frame,text="Reset", width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        reset_button.grid(row=0,column=4)
        
        
        
        # Right frame
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Attendance Details", fg="#4A90E2", font=("Arial", 13, "bold"))
        right_frame.place(x=615, y=10, width=630, height=580)
        
        table_frame = Frame(right_frame,bd=2,relief=RIDGE,bg="white")
        table_frame.place(x=5,y=5,width=615,height=455)
        
        
######################## scroll bar table ##################################
        scroll_x=ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        self.AttendanceReportTable=ttk.Treeview(table_frame,column=("id","roll","name","department","time","date","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)
        
        self.AttendanceReportTable.heading("id",text="Attendance ID")
        self.AttendanceReportTable.heading("roll",text="Roll No.")
        self.AttendanceReportTable.heading("name",text="Name")
        self.AttendanceReportTable.heading("department",text="Department")
        self.AttendanceReportTable.heading("time",text="Time")
        self.AttendanceReportTable.heading("date",text="Date")
        self.AttendanceReportTable.heading("attendance",text="Attendance")
        
        self.AttendanceReportTable["show"]="headings"
        self.AttendanceReportTable.column("id",width=100)
        self.AttendanceReportTable.column("roll",width=100)
        self.AttendanceReportTable.column("name",width=100)
        self.AttendanceReportTable.column("department",width=100)
        self.AttendanceReportTable.column("time",width=100)
        self.AttendanceReportTable.column("date",width=100)
        self.AttendanceReportTable.column("attendance",width=100)
        
        
        
        
        
        
        self.AttendanceReportTable.pack(fill=BOTH,expand=1)
        
        
        
if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()


# In[ ]:




