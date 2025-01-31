#!/usr/bin/env python
# coding: utf-8

# In[27]:


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
import csv
from tkinter import filedialog

mydata=[]

class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1535x790+0+0")
        self.root.title("Face Recognition System")
        # Set the whole background to white
        self.root.configure(bg="white")
        
############################# variables #############################
        
        self.var_atten_id= StringVar()
        self.var_atten_roll= StringVar()
        self.var_atten_name= StringVar()
        self.var_atten_dep= StringVar()
        self.var_atten_time= StringVar()
        self.var_atten_date= StringVar()
        self.var_atten_attendance= StringVar()
        
        
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
        attendanceID_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_id, font=("Arial", 11, "bold"))
        attendanceID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Roll label
        rollLabel = Label(left_inside_frame, text="Roll:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        rollLabel.grid(row=0, column=2, padx=4, pady=8)
        rollLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_roll, font=("Arial", 11, "bold"))
        rollLabel_entry.grid(row=0, column=3, padx=4, pady=8)

        # Name label
        nameLabel = Label(left_inside_frame, text="Name:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        nameLabel.grid(row=1, column=0)
        nameLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_name, font=("Arial", 11, "bold"))
        nameLabel_entry.grid(row=1, column=1,pady=8)
        
        # Department label
        deptLabel = Label(left_inside_frame, text="Department:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        deptLabel.grid(row=1, column=2)
        deptLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_dep, font=("Arial", 11, "bold"))
        deptLabel_entry.grid(row=1, column=3,pady=8)
        
        # Time label
        timeLabel = Label(left_inside_frame, text="Time:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        timeLabel.grid(row=2, column=0)
        timeLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_time, font=("Arial", 11, "bold"))
        timeLabel_entry.grid(row=2, column=1,pady=8)
        
        # Date label
        DateLabel = Label(left_inside_frame, text="Date:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        DateLabel.grid(row=2, column=2)
        DateLabel_entry = ttk.Entry(left_inside_frame, width=20,textvariable=self.var_atten_date, font=("Arial", 11, "bold"))
        DateLabel_entry.grid(row=2, column=3,pady=8)
        
        # Attendance label
        attendanceLabel = Label(left_inside_frame, text="Attendance Status:", font=("Arial", 11, "bold"), bg="white", fg="#4a90e2")
        attendanceLabel.grid(row=3, column=0)

        # Attendance dropdown (combobox) with options "Present" and "Absent"
        attendanceLabel_combobox = ttk.Combobox(left_inside_frame, width=20,textvariable=self.var_atten_attendance, font=("Arial", 10))
        attendanceLabel_combobox['values'] = ('Present', 'Absent')  # Options for the dropdown
        attendanceLabel_combobox.grid(row=3, column=1, pady=8)

        
        #Buttons frame 
        btn_frame = Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=300,width=595,height=35)
        
        import_button = Button (btn_frame,text="Import csv",command=self.importCsv, width=13,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        import_button.grid(row=0,column=0)
        
        export_button = Button (btn_frame,text="Export csv",command=self.exportCsv, width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        export_button.grid(row=0,column=1)
        
        update_button = Button (btn_frame,text="Update",command=self.update_csv_record, width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
        update_button.grid(row=0,column=2)
        
        reset_button = Button (btn_frame,text="Reset",command=self.reset_data, width=14,font=("Arial",13,"bold"), bg="#4A90E2",fg="white")
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
        
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)
        
        
############################################ face data #############################################
    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END,values=i)
    
    #import csv files
    def update_csv_record(self):
        # Get updated data from entry fields
        attendance_id = self.var_atten_id.get()
        roll_no = self.var_atten_roll.get()
        name = self.var_atten_name.get()
        department = self.var_atten_dep.get()
        time = self.var_atten_time.get()
        date = self.var_atten_date.get()
        attendance = self.var_atten_attendance.get()

        # Define the path to the CSV file
        csv_file_path = 'StudentDetails.csv'

        # Read the CSV data into a list
        updated_rows = []
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == attendance_id:
                    # Update the selected row with new data
                    updated_rows.append([attendance_id, roll_no, name, department, time, date, attendance])
                else:
                    updated_rows.append(row)

        # Write the updated data back to the CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        # Refresh the table view after update
        self.fetch_student_data()
        messagebox.showinfo("Success", "Record updated successfully!")
    def importCsv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)

        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)
            
    #export csv files
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data Found to export", parent=self.root)
                return False
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")), parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                export_write=csv.writer(myfile,delimeter=",")
                for i in mydata:
                    export_write.writerow(i)
                messagebox.showinfo("Data Export","Your data Exported to"+os.path.basename(fln)+"successfully")
        except Exception as es:
                    messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)
                
    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_atten_id.set(rows[0])
        self.var_atten_roll.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_dep.set(rows[3])
        self.var_atten_time.set(rows[4])
        self.var_atten_date.set(rows[5])
        self.var_atten_attendance.set(rows[6])
    
    
    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("")        
            
        
if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()


# In[ ]:




