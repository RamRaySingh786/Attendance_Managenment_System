#!/usr/bin/env python
# coding: utf-8

# In[23]:


from tkinter import*
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import messagebox as mess
from tkinter import PhotoImage
from PIL import Image, ImageTk
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
import time
from AttendanceDb import *
import numpy as np
import json
from tkcalendar import DateEntry
from tkinter import filedialog

class Student :
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise IOError('Error loading face cascade file')
    def __init__(self, root) :
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root. title("face Recogniton System")
        title_lbl=Label(text="Student Management System",font=("Arial",35,"bold"),fg="white",bg="#4A90E2")
        title_lbl.place(x=0,y=0,width=1530,height=75)
        main_frame=Frame(bd=4)
        main_frame.place(x=20,y=80,width=1400,height=600)
        # left_frame
        left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",fg="#4A90E2",font=("times new roman",12,"bold"))
        left_frame.place(x=10,y=10,width=650,height=590)
        
        cc_frame=LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Information",fg="#4A90E2",font=("times new roman",12,"bold"))
        cc_frame.place(x=5,y=30,width=650,height=120)

        dep_label=Label(cc_frame,width=12,bg="white",text="Department",font=("times new roman",12,"bold"))
        dep_label.grid(row=0,column=0,sticky=W,pady=10)
        self.d_combo=ttk.Combobox(cc_frame,font=("times new roman",12,"bold"),width=17,state="readonly")
        self.d_combo['values'] = (
                    "Select Department",
                    "Computer Science",
                    "Information Technology",
                    "Mechanical Engineering",
                    "Civil Engineering",
                    "Electrical Engineering",
                    "Electronics and Communication",
                    "Business Administration",
                    "Biotechnology"
                )
        self.d_combo.grid(row=0, column=1,sticky=W,pady=10)

                # Optionally, set a default value
        self.d_combo.current(0) 

        c_label = Label(cc_frame, width=10, bg="white", text="Course", font=("times new roman", 12, "bold"))
        c_label.grid(row=0, column=2, sticky=W)

        self.c_combo = ttk.Combobox(cc_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        self.c_combo['values'] = (
            "Select Course",
            "B.Sc.",
            "B.Tech",
            "M.E/M.Tech",
        )
        self.c_combo.grid(row=0, column=3, sticky=W)

        # Set default value for Course ComboBox
        self.c_combo.current(0)


        # Year Label and ComboBox
        Y_label = Label(cc_frame, width=7, bg="white", text="Year", font=("times new roman", 12, "bold"))
        Y_label.grid(row=1, column=0, sticky=W)

        
        
        # self.Y_combo = ttk.Combobox(cc_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        # self.Y_combo['values'] = (
        #     "Select Year",
        #     "First Year",
        #     "Second Year",
        #     "Third Year",
        #     "Final Year"
        # )
        # self.Y_combo.grid(row=1, column=1, sticky=W)
        # self.Y_combo = ttk.Combobox(cc_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        # self.Y_combo.grid(row=1, column=1, padx=10, sticky=W)


    
        self.c_combo.current(0)
        self.c_combo.bind("<<ComboboxSelected>>", self.update_years)
        s_label = Label(cc_frame, width=12, bg="white", text="Year", font=("times new roman", 12, "bold"))
        s_label.grid(row=1, column=1, sticky=tk.W)

        self.Y_combo = ttk.Combobox(cc_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        self.Y_combo.grid(row=1, column=1, sticky=tk.W)





        # self.Y_combo.current(0)
        self.Y_combo.bind("<<ComboboxSelected>>", self.update_semesters)
        # Semester Label and ComboBox
        s_label = Label(cc_frame, width=12, bg="white", text="Semester", font=("times new roman", 12, "bold"))
        s_label.grid(row=1, column=2, sticky=tk.W)

        self.s_combo = ttk.Combobox(cc_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        self.s_combo.grid(row=1, column=3, sticky=tk.W)

        
        self.update_years()
        self.update_semesters()

        # Run the window loop
        student_info_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Student Information", fg="#4A90E2", font=("times new roman", 12, "bold"))
        student_info_frame.place(x=5, y=160, width=650, height=400)

        # Row 1: Student ID and Student Name
        student_id_label = Label(student_info_frame, width=12, bg="white", text="Student ID", font=("times new roman", 12, "bold"))
        student_id_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.student_id_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20,validate="key", validatecommand=(root.register(lambda value: value.isdigit() or value == ""), '%P'))
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=10)

        student_name_label = Label(student_info_frame, width=12, bg="white", text="Student Name", font=("times new roman", 12, "bold"))
        student_name_label.grid(row=0, column=2, sticky=W, padx=10, pady=10)
        self.student_name_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.student_name_entry.grid(row=0, column=3, padx=10, pady=10)

        # Row 2: Class Division and Roll No
        class_division_label = Label(student_info_frame, width=12, bg="white", text="Class Division", font=("times new roman", 12, "bold"))
        class_division_label.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        
        self.class_division_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20,validate="key",validatecommand=(root.register(lambda value: value in ["", "1", "2", "3"]), '%P'))
        self.class_division_entry.grid(row=1, column=1, padx=10, pady=10)

        roll_no_label = Label(student_info_frame, width=12, bg="white", text="Roll No", font=("times new roman", 12, "bold"))
        roll_no_label.grid(row=1, column=2, sticky=W, padx=1, pady=10)
        self.roll_no_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.roll_no_entry.grid(row=1, column=3, padx=10, pady=10)

        # Row 3: Date of Birth and Email
        dob_label = Label(student_info_frame, width=12, bg="white", text="Date of Birth", font=("times new roman", 12, "bold"))
        dob_label.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.dob_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.dob_entry.grid(row=2, column=1, padx=10, pady=10)
        self.dob_entry.bind("<Button-1>", lambda event: self.open_calendar(event))

        email_label = Label(student_info_frame, width=12, bg="white", text="Email", font=("times new roman", 12, "bold"))
        email_label.grid(row=2, column=2, sticky=W, padx=0, pady=10)
        self.email_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.email_entry.grid(row=2, column=3, padx=10, pady=10)

        # Row 4: Phone Number and Address
        phone_no_label = Label(student_info_frame, width=12, bg="white", text="Phone No.", font=("times new roman", 12, "bold"))
        phone_no_label.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.phone_no_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.phone_no_entry.grid(row=3, column=1, padx=10, pady=10)

        address_label = Label(student_info_frame, width=12, bg="white", text="Address", font=("times new roman", 12, "bold"))
        address_label.grid(row=3, column=2, sticky=W, padx=1, pady=10)
        self.address_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.address_entry.grid(row=3, column=3, padx=10, pady=10)

        # Row 5: Teacher Name
        teacher_name_label = Label(student_info_frame, width=12, bg="white", text="Teacher Name", font=("times new roman", 12, "bold"))
        teacher_name_label.grid(row=4, column=0, sticky=W, padx=10, pady=10)
        self.teacher_name_entry = ttk.Entry(student_info_frame, font=("times new roman", 12, "bold"), width=20)
        self.teacher_name_entry.grid(row=4, column=1, padx=10, pady=10)

        # # Function Buttons

        # btn_frame = Frame(student_info_frame, bd=3, relief=RIDGE)
        # btn_frame.place(x=0, y=300, width=700, height=80)

        # update_btn = Button(btn_frame, text = "Update", fg="white" ,bg="#4A90E2", command=self.save_profile,
        #                     width=26, activebackground = "white" ,font=('times new roman', 15, 'bold'))
        # update_btn.grid(row=0, column=0)

        # delete_btn = Button(btn_frame, text="Delete", fg = 'white', bg = '#4A90E2', command=self.delete_profile,
        #                   width=26, font=("times new roman", 15, "bold"))
        # delete_btn.grid(row=0, column=1)



        # from tkinter import *

        # Assuming student_info_frame already exists as a parent frame
        btn_frame = Frame(student_info_frame, bd=3, relief=RIDGE)
        btn_frame.place(x=0, y=300, width=650, height=100)  # Increased height to fit two rows

        # Configure columns in btn_frame to divide the space
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        # Define common button properties
        button_font = ('times new roman', 15, 'bold')
        button_bg = "#4A90E2"
        button_fg = "white"

        # Button 1: Update (Row 0, Column 0)
        update_btn = Button(btn_frame, text="Update", fg=button_fg, bg=button_bg,
                            command=self.save_profile, width=10, activebackground="white", font=button_font)
        update_btn.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        # Button 2: Delete (Row 0, Column 1)
        delete_btn = Button(btn_frame, text="Delete", fg=button_fg, bg=button_bg,
                            command=self.delete_profile, width=10, activebackground="white", font=button_font)
        delete_btn.grid(row=0, column=1, padx=0, pady=0, sticky="ew")

        
        # Button : reset button
        reset_btn = Button(btn_frame, text="Reset", fg=button_fg, bg=button_bg,
                            command=self.reset_profile, width=10, activebackground="white", font=button_font)
        reset_btn.grid(row=0, column=2, padx=0, pady=0, sticky="ew")

        # Button 3: Take Images (Row 1, Column 0)
        takeImg = Button(btn_frame, text="Take Images", fg=button_fg, bg=button_bg,
                        command=lambda: [self.capture_images(self.student_name_entry.get()), self.train_lbph_model()],
                        width=10, activebackground="white", font=button_font)
        takeImg.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

        # Button 4: Upload Images (Row 1, Column 1)
        uploadImg = Button(btn_frame, text="Upload Images", fg=button_fg, bg=button_bg,
                   command=lambda: [self.upload_images(self.student_name_entry.get()), self.train_lbph_model()],
                   width=10, activebackground="white", font=button_font)
        uploadImg.grid(row=1, column=1, padx=0, pady=0, sticky="ew")


        # Button 5: Save Profile (Row 1, Column 2)
        trainImg = Button(btn_frame, text="Save Profile", fg=button_fg, bg=button_bg,
                        command=self.save_profile, width=10, activebackground="white", font=button_font)
        trainImg.grid(row=1, column=2, padx=0, pady=0, sticky="ew")


        # # Expand the button frame horizontally
        # btn_frame.grid_columnconfigure(0, weight=1)
        # btn_frame.grid_columnconfigure(1, weight=1)
        # btn_frame.grid_columnconfigure(2, weight=1)

        # Run the window loop
    
        # Right one
        Right_frame = LabelFrame(main_frame,bg="white",relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
        Right_frame.place(x=670,y=10,width=720,height=580)
        # Load the .png image (replace 'path_to_image.png' with the actual file path)

        img_right = Image.open(r'student.jpeg')
        img_right = img_right.resize((700, 130), Image.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)



        f_lbl = Label(Right_frame, image = self.photoimg_right)
        f_lbl.place(x=5, y=50, width = 710, height = 130)
        search_label = Label(Right_frame, text="Search:", bg='white', font=("Helvetica", 12))
        search_label.place(x=5, y=190)

        self.search_entry = Entry(Right_frame, font=("Helvetica", 12))
        self.search_entry.place(x=60, y=190, width=200)

        search_button = Button(Right_frame, text="Search",command=self.search_student, bg="#4a90e2", fg="white", font=("Helvetica", 10))
        search_button.place(x=270, y=190)


        table_frame = Frame(Right_frame,bd=2, bg = 'white', relief = RIDGE)
        table_frame.place(x = 5, y= 240, width = 640, height = 250)

        scroll_x = ttk.Scrollbar(table_frame, orient = HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient = VERTICAL)

        self.student_table = ttk.Treeview(table_frame,
                                          columns=(
                                          "dep", "course", "year", "sem", "id", "name", "div", "roll_no", "dob",
                                          "email", "phone", "address", "teacher"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)

        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)

        scroll_x.config(command = self.student_table.xview)
        scroll_y.config(command = self.student_table.yview)

        self.student_table.heading("dep", text = "Department")
        self.student_table.heading("course", text = "Course")
        self.student_table.heading("year", text = "Year")
        self.student_table.heading("sem", text = "Semester")
        self.student_table.heading("id", text = "Stud_ID")
        self.student_table.heading("name", text = "Name")
        self.student_table.heading("div", text = "Division")
        self.student_table.heading("roll_no", text = "Roll_No")
        self.student_table.heading("dob", text = "DOB")
        self.student_table.heading("email", text = "Email")
        self.student_table.heading("phone", text = "Phone")
        self.student_table.heading("address", text = "Address")
        self.student_table.heading("teacher", text = "Teacher")
        self.student_table["show"] = "headings"

        self.student_table.column("dep", width = 100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("roll_no", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.fetch_student_data()



        self.student_table.pack(fill = BOTH, expand = 0)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)


######################################################################################
    def open_calendar(self, event):
        calendar_window = Toplevel(self.root)
        calendar_window.title("Select Date of Birth")
        # Add a DateEntry widget from tkcalendar
        calendar_window.geometry(f"+{self.dob_entry.winfo_rootx()}+{self.dob_entry.winfo_rooty() + self.dob_entry.winfo_height()}")

        cal = DateEntry(calendar_window, selectmode='day', year=2000, month=1, day=1, date_pattern='yyyy-mm-dd')
        cal.grid(row=0, column=0, padx=20, pady=20)
        
    # Add a button to confirm the selection and set the date in the dob_entry
        def set_date():
                self.dob_entry.delete(0, END)  
                selected_date=cal.get_date()
                formatted_date = selected_date.strftime('%Y-%m-%d')  # Format the date to 'YYYY-MM-DD'
          
                self.dob_entry.insert(0, formatted_date)  # Insert the selected date
                calendar_window.destroy()  # Close the calendar window 
                self.validate_dob(selected_date) 
        select_button = Button(calendar_window, text="Select", command=set_date)
        select_button.grid(row=1, column=0, padx=20, pady=10)
    
        calendar_window.grab_set()
    def check_haarcascadefile():
            exists = os.path.isfile("haarcascade_frontalface_default.xml")
            if exists:
                pass
            else:
                mess._show(title='Some file missing', message='Please contact us for help')
    def update_years(self, event=None):
        # Update year options based on selected course
        selected_course = self.c_combo.get()
        
        if selected_course == "B.Sc.":
            self.Y_combo['values'] = ("Select Year", "First Year", "Second Year", "Third Year")
        elif selected_course == "M.E/M.Tech":
            self.Y_combo['values'] = ("Select Year", "First Year", "Second Year")
        elif selected_course == "B.Tech":
            self.Y_combo['values'] = ("Select Year", "First Year", "Second Year", "Third Year", "Final Year")
        else:
            self.Y_combo['values'] = ("Select Year",)

        self.Y_combo.current(0)
        self.update_semesters()  # Reset semesters based on default year selection

    def update_semesters(self, event=None):
        # Set semester options based on the selected year
        selected_year = self.Y_combo.get()

        if selected_year == "First Year":
            self.s_combo['values'] = ("Select Semester", "Semester 1", "Semester 2")
        elif selected_year == "Second Year":
            self.s_combo['values'] = ("Select Semester", "Semester 3", "Semester 4")
        elif selected_year == "Third Year":
            self.s_combo['values'] = ("Select Semester", "Semester 5", "Semester 6")
        elif selected_year == "Final Year":
            self.s_combo['values'] = ("Select Semester", "Semester 7", "Semester 8")
        else:
            self.s_combo['values'] = ("Select Semester",)

        self.s_combo.current(0)  # Reset to "Select Semester"



        # Set default value for Semester ComboBox
        # self.s_combo.current(0)
    def search_student(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            messagebox.showerror("Error", "Please enter a search term")
            return

        try:
            # Establish database connection
            connection = connect_to_db()
            cursor = connection.cursor()

            # SQL query using LIKE for searching by name or email
            query = """
                SELECT Dep, Course, Year, Semester, Student_id, Name, Division,Roll, Dob, Email, Phone, Address, Teacher
                FROM student
                WHERE name LIKE %s OR email LIKE %s
            """
            like_pattern = f"%{search_term}%"
            cursor.execute(query, (like_pattern, like_pattern))

            # Fetch all matching rows
            rows = cursor.fetchall()

            if len(rows) == 0:
                messagebox.showinfo("Info", "No records found")

            # Clear the current table data
            for row in self.student_table.get_children():
                self.student_table.delete(row)

            # Populate the table with search results
            for row in rows:
                self.student_table.insert('', 'end', values=row)

            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {str(err)}")    
    def get_cursor(self, event=""):
            # Get the selected row from the student table
            cursor_row = self.student_table.focus()
            
            # Fetch the data associated with the selected row
            content = self.student_table.item(cursor_row)
            row = content['values']

            if row:
                # Assuming the entry fields for the student form are defined similar to the names provided
                self.student_id_entry.delete(0, END)
                self.student_id_entry.insert(END, row[4])  # Student ID field
                
                self.student_name_entry.delete(0, END)
                self.student_name_entry.insert(END, row[5])  # Name field
                
                self.d_combo.set(row[0])  # Department dropdown
                
                self.c_combo.set(row[1])  # Course dropdown
                
                self.Y_combo.set(row[2])  # Year dropdown
                
                self.s_combo.set(row[3])  # Semester dropdown
                
                self.class_division_entry.delete(0, END)
                self.class_division_entry.insert(END, row[6])  # Division field
                
                self.roll_no_entry.delete(0, END)
                self.roll_no_entry.insert(END, row[7])  # Roll Number field
                
                self.dob_entry.delete(0, END)
                self.dob_entry.insert(END, row[8])  # Date of Birth field
                
                self.email_entry.delete(0, END)
                self.email_entry.insert(END, row[9])  # Email field
                
                self.phone_no_entry.delete(0, END)
                self.phone_no_entry.insert(END, row[10])  # Phone Number field
                
                self.address_entry.delete(0, END)
                self.address_entry.insert(END, row[11])  # Address field
                
                self.teacher_name_entry.delete(0, END)
                self.teacher_name_entry.insert(END, row[12])
        # Bind the get_cursor function to the Treeview            
    def assure_path_exists(path):
            dir = os.path.dirname(path)
            if not os.path.exists(dir):
                os.makedirs(dir)
    @staticmethod            
    def validate_inputs(self):
        # Validate the department
            if self.d_combo.get() == "Select Department":
                messagebox.showerror("Error", "Please select a valid Department.")
                return False
            # Validate the course
            if self.c_combo.get() == "Select Course":
                messagebox.showerror("Error", "Please select a valid Course.")
                return False
            # Validate the year
            if self.Y_combo.get() == "Select Year":
                messagebox.showerror("Error", "Please select a valid Year.")
                return False
            # Validate the semester
            if self.s_combo.get() == "Select Semester":
                messagebox.showerror("Error", "Please select a valid Semester.")
                return False
            # Validate student ID
            if self.student_id_entry.get() == "":
                messagebox.showerror("Error", "Student ID is required.")
                return False
            # Validate student name
            if self.student_name_entry.get() == "":
                messagebox.showerror("Error", "Student Name is required.")
                return False
                # Additional validation for email and phone number
            if "@" not in self.email_entry.get() or "." not in self.email_entry.get():
                    messagebox.showerror("Error", "Invalid email format")
                    return

            if not self.phone_no_entry.get().isdigit() or len(self.phone_no_entry.get()) != 10:
                    messagebox.showerror("Error", "Phone number must be 10 digits only")
                    return
            return True

    
    def fetch_student_data(self):
    # Clear any existing data in the table
            for row in self.student_table.get_children():
                self.student_table.delete(row)

            try:
                # Use the existing database connection and cursor from AttendanceDb
                connection = connect_to_db()
                cursor = connection.cursor()

                # Select all student data from the database
                query = """
                SELECT Dep, Course, Year, Semester, Student_id, Name, Division,Roll, Dob, Email, Phone, Address, Teacher
                FROM student
                """
                cursor.execute(query)
                rows = cursor.fetchall()

                # Check if data is returned
                if len(rows) != 0:
                    for row in rows:
                        # Insert data into the student_table
                        self.student_table.insert('', 'end', values=row)

                    connection.commit()
                else:
                    messagebox.showinfo("No Data", "No student records found.")

            except Exception as err:
                print("Error fetching student data from database")
                messagebox.showerror("Error", f"Error occurred: {err}")

            finally:
                # Close the cursor and connection
                cursor.close()
                connection.close()                              
    def validate_dob(self, dob):
        # Convert the selected date into a datetime objec        
        # Get the current date
        current_date = datetime.now().date()
        hundred_years_ago = current_date - timedelta(days=365 * 100)

    # Check if DOB is earlier than the current date
        if dob >= current_date:
            messagebox.showerror("Invalid Date", "Date of Birth cannot be today or a future date.")
            self.dob_entry.delete(0, END)
        elif dob < hundred_years_ago:
            messagebox.showerror("Invalid Date", "Date of Birth cannot be more than 100 years ago.")
            self.dob_entry.delete(0, END)
    def save_profile(self):
        if self.validate_inputs(self):
            # Retrieve values from instance variables
            student_id = self.student_id_entry.get()
            student_name = self.student_name_entry.get()
            department = self.d_combo.get()
            course = self.c_combo.get()
            year = self.Y_combo.get()
            semester = self.s_combo.get()
            class_division = self.class_division_entry.get()
            roll_no = self.roll_no_entry.get()
            dob = self.dob_entry.get()
            email = self.email_entry.get()
            phone_no = self.phone_no_entry.get()
            address = self.address_entry.get()
            teacher_name = self.teacher_name_entry.get()

                # Validate form data
                    # Insert data into the MySQL database
            try:
            # Use the existing database connection and cursor from AttendanceDb
                connection = connect_to_db()
                
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM student WHERE Student_id = %s", (student_id,))
                record = cursor.fetchone()

                if record:
                    # If the student ID exists, update the record
                    query = """
                    UPDATE student
                    SET Name=%s, Dep=%s, Course=%s, Year=%s, Semester=%s, Division=%s, Roll=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s
                    WHERE Student_id=%s
                    """
                    data = (student_name, department, course, year, semester, class_division, roll_no, dob, email, phone_no, address, teacher_name, student_id)
                    cursor.execute(query, data)
                    messagebox.showinfo("Success", "Profile updated successfully")
                else:
                    # If the student ID doesn't exist, insert a new record
                    query = """
                    INSERT INTO student
                    (Student_id, Name, Dep, Course, Year, Semester, Division, Roll, Dob, Email, Phone, Address, Teacher)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    data = (student_id, student_name, department, course, year, semester, class_division, roll_no, dob, email, phone_no, address, teacher_name)
                    cursor.execute(query, data)
                    messagebox.showinfo("Success", "Profile saved successfully")

                # Commit the transaction
                connection.commit()
                self.fetch_student_data()  # Refresh the table to reflect the deleted record

            except Exception as err:
                print("Here it is")
                messagebox.showerror("Error", f"Error occurred: {err}")
            finally:
            # Close the cursor and connection
                cursor.close()
                connection.close()        
    def update_profile(self):
    # Retrieve values from instance variables
            student_id = self.student_id_entry.get()
            student_name = self.student_name_entry.get()
            department = self.d_combo.get()
            course = self.c_combo.get()
            year = self.Y_combo.get()
            semester = self.s_combo.get()
            class_division = self.class_division_entry.get()
            roll_no = self.roll_no_entry.get()
            dob = self.dob_entry.get()
            email = self.email_entry.get()
            phone_no = self.phone_no_entry.get()
            address = self.address_entry.get()
            teacher_name = self.teacher_name_entry.get()

            # Validate form data if needed (you can uncomment this if you have a validate_inputs method)
            # if not self.validate_inputs(self):
            #     return

            # Update data in the MySQL database
            try:
                # Use the existing database connection and cursor from AttendanceDb
                connection = connect_to_db()
                cursor = connection.cursor()

                query = """
                UPDATE student
                SET Name=%s, Dep=%s, Course=%s, Year=%s, Semester=%s, Division=%s, Roll=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s
                WHERE Student_id=%s
                """
                data = (student_name, department, course, year, semester, class_division, roll_no, dob, email, phone_no, address, teacher_name, student_id)

                cursor.execute(query, data)

                # Commit the transaction
                connection.commit()
                self.fetch_student_data()  # Refresh the table to reflect the deleted record

                messagebox.showinfo("Success", "Profile updated successfully")
            except Exception as err:
                print("Error occurred while updating the profile")
                messagebox.showerror("Error", f"Error occurred: {err}")
            finally:
                # Close the cursor and connection
                cursor.close()
                connection.close()
    def delete_profile(self):
            # Retrieve the student ID from the entry field
            student_id = self.student_id_entry.get()

            # Validate the student ID (optional)

            # Delete data from the MySQL database
            try:
                # Use the existing database connection and cursor
                connection = connect_to_db()
                cursor = connection.cursor()

                query = "DELETE FROM student WHERE Student_id=%s"
                cursor.execute(query, (student_id,))

                # Check if any row was deleted
                if cursor.rowcount > 0:
                    connection.commit()
                    messagebox.showinfo("Success", "Profile deleted successfully")
                    self.fetch_student_data()  # Refresh the table to reflect the deleted record

                    # Now remove the row from the GUI table (self.student_table)
                    # Loop through the table and find the matching student_id
                    for row in self.student_table.get_children():
                        table_data = self.student_table.item(row)["values"]
                        if table_data[0] == student_id:  # Assuming Student_id is in the first column
                            self.student_table.delete(row)  # Delete the matching row from the table
                            break  # Exit the loop once the row is found and deleted
                else:
                    messagebox.showwarning("Warning", "No record found with that Student ID.")
            
            except Exception as err:
                print("Error occurred while deleting the profile")
                messagebox.showerror("Error", f"Error occurred: {err}")
            
            finally:
                # Close the cursor and connection
                cursor.close()
                connection.close()
                
    #reset function 
    def reset_profile(self):
        self.student_id_entry.delete(0, "end")
        self.student_name_entry.delete(0, "end")
        self.d_combo.set("Select Department")
        self.c_combo.set("Select Course")
        self.Y_combo.set("Select Year")
        self.s_combo.set("Select Semester")
        self.class_division_entry.delete(0, "end")

        self.roll_no_entry.delete(0, "end")
        self.dob_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.phone_no_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.teacher_name_entry.delete(0, "end")

        
    def upload_images(self, student_name):
        # Open file dialog to select images
        file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_paths:
            messagebox.showwarning("No Selection", "No images were selected!")
            return

        # Set up directories to save processed data
        student_dir = os.path.join("trained_students", student_name)
        os.makedirs(student_dir, exist_ok=True)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = []
        labels = []

        for file_path in file_paths:
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in detected_faces:
                faces.append(gray[y:y+h, x:x+w])
                labels.append(int(student_name))  # Assuming 'student_name' can be converted to a unique label

        if faces:
            # Train with LBPH algorithm
            lbph_model = cv2.face.LBPHFaceRecognizer_create()
            lbph_model.train(faces, np.array(labels))
            # Save model for each student
            lbph_model.save(os.path.join(student_dir, f"{student_name}_model.xml"))
            messagebox.showinfo("Success", "Images trained and model saved!")
        else:
            messagebox.showwarning("No Faces Found", "No faces were detected in the selected images.")
    
    


#     def upload_images(self, student_name):
#         # Open file dialog to select images
#         file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
#         if not file_paths:
#             messagebox.showwarning("No Selection", "No images were selected!")
#             return

#         # Set up directories to save processed data
#         student_dir = os.path.join("trained_students", student_name)
#         os.makedirs(student_dir, exist_ok=True)

#         face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         faces = []
#         labels = []

#         for file_path in file_paths:F
#             img = cv2.imread(file_path)
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

#             for idx, (x, y, w, h) in enumerate(detected_faces):
#                 face_img = gray[y:y+h, x:x+w]
#                 faces.append(face_img)
#                 labels.append(int(student_name))  # Ensure this can be converted or use a unique integer ID

#                 # Save each detected face as a separate file
#                 face_filename = os.path.join(student_dir, f"{student_name}_face_{idx}.jpg")
#                 cv2.imwrite(face_filename, face_img)

#         if faces:
#             # Train with LBPH algorithm
#             lbph_model = cv2.face.LBPHFaceRecognizer_create()
#             lbph_model.train(faces, np.array(labels))
#             # Save model for each student
#             lbph_model.save(os.path.join(student_dir, f"{student_name}_model.xml"))
#             messagebox.showinfo("Success", "Images trained and model saved!")
#         else:
#             messagebox.showwarning("No Faces Found", "No faces were detected in the selected images.")


        
        


    def capture_images(self, person_name, num_samples=101):
            print("I am here")

            # Ensure the 'TrainingImage' directory exists
            if not os.path.exists('TrainingImage'):
                os.makedirs('TrainingImage')

            # Create a folder for the person, even if 'TrainingImage' already exists
            person_folder = os.path.join('TrainingImage', person_name)
            if not os.path.exists(person_folder):
                os.makedirs(person_folder)

            # Start capturing video from webcam
            cap = cv2.VideoCapture(0)
            count = 0

            if not cap.isOpened():
                print("Failed to access the camera")
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture image")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = Student.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y + h, x:x + w]
                    count += 1
                    file_path = os.path.join(person_folder, f"{count}.jpg")
                    cv2.imwrite(file_path, face)

                    # Display the capture progress
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, f"Captured {count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.imshow("Face Capture", frame)

                # Stop capturing after reaching the number of required samples
                if count >= num_samples:
                    break

                # Exit the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the capture and close any open windows
            cap.release()
            cv2.destroyAllWindows()

            print(f"Successfully captured {count} images for {person_name}")


    # Step 2: Train the LBPH face recognition model
    def train_lbph_model(self):
                faces = []
                labels = []

                # Validate student ID
                try:
                    label_id = int(self.student_id_entry.get())  # Ensure student_id_entry exists and has a value
                except ValueError:
                    print("Error: Student ID must be a valid integer.")
                    return

                # Load existing label map if it exists, else initialize an empty one
                label_map = {}
                label_map_file = 'label_map.json'

                if os.path.exists(label_map_file):
                    try:
                        with open(label_map_file, 'r') as f:
                            label_map = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Warning: {label_map_file} is empty or contains invalid data. Initializing a new label map.")
                        label_map = {}

                # Check if the label_id already exists
                if str(label_id) in label_map:
                    print(f"Label ID {label_id} already exists for {label_map[label_id]}.")
                    return  # Exit if the label_id is already used

                # Add the new label to the label map
                person_name = self.student_name_entry.get()  # Assuming you have a way to get the student's name
                if not person_name:
                    print("Error: Student name is empty.")
                    return
                label_map[str(label_id)] = person_name  # Map label ID to person name

                # Process images for the current student
                person_folder = os.path.join('TrainingImage', person_name)
                if not os.path.exists(person_folder):
                    print(f"Error: Folder for {person_name} does not exist.")
                    return

                for image_name in os.listdir(person_folder):
                    image_path = os.path.join(person_folder, image_name)
                    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        print(f"Warning: Unable to read {image_path}. Skipping.")
                        continue

                    img_resized = cv2.resize(img, (200, 200))
                    faces.append(img_resized)
                    labels.append(label_id)

                if len(faces) == 0:
                    print(f"Error: No valid face images found for {person_name}.")
                    return

                faces = np.array(faces)
                labels = np.array(labels, dtype=np.int32)  # Ensure labels are of type int32

                # Initialize LBPH face recognizer
                recognizer = cv2.face.LBPHFaceRecognizer_create()

                # Train the recognizer on faces and labels
                recognizer.train(faces, labels)

                # Save the trained model and updated label map
                recognizer.save('Trainner.yml')
                with open('label_map.json', 'w') as f:
                    json.dump(label_map, f, indent=4)  # Save with indentation for readability

                print(f"Model trained and saved for {person_name} with ID {label_id}.")
    
    # Step 3: Predict using the trained model
    def recognize_faces(self):
    # Load the trained recognizer model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('Trainner.yml')

        # Load the label map from the file
        with open('label_map.json', 'r') as f:
            label_map = json.load(f)

        # Initialize video capture from the webcam
        cap = cv2.VideoCapture(0)

        # Load the face detection classifier (assuming it's already defined)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Establish connection to the database (assuming it's MySQL)
        conn = mysql.connector.connect(host="localhost", username="root", password="", database="face_recognizer")
        my_cursor = conn.cursor()

        while True:
            ret, frame = cap.read()  # Capture a frame from the video feed
            if not ret:
                print("Failed to capture video")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Detect faces in the frame

            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]  # Extract the detected face region
                face_resized = cv2.resize(face, (200, 200))  # Resize the face to the required size

                # Predict the label and confidence of the detected face
                label_id, confidence = recognizer.predict(face_resized)

                # Get the person's name from the label map
                name = label_map.get(str(label_id), "Unknown")

                # Fetch additional information from the database
                my_cursor.execute("select Name from student where Student_id=%s", (str(label_id),))
                n = my_cursor.fetchone()
                n = n[0] if n else "Unknown"

                my_cursor.execute("select Roll from student where Student_id=%s", (str(label_id),))
                r = my_cursor.fetchone()
                r = r[0] if r else "Unknown"

                my_cursor.execute("select Dep from student where Student_id=%s", (str(label_id),))
                d = my_cursor.fetchone()
                d = d[0] if d else "Unknown"

                # Display details if confidence is high enough
                if confidence > 80:
                    cv2.putText(frame, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(frame, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(frame, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                else:
                    # Mark the face as unknown if confidence is too low
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(frame, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                # Draw rectangle around the face and display the name/confidence
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, f"{name} ({round(confidence, 2)})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Show the video feed with recognition results
            cv2.imshow("Face Recognition", frame)

            # Exit loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

        # Close the database connection
        my_cursor.close()
        conn.close()
           

    # def TakeImages():
    #         check_haarcascadefile()
    #         columns = ['SERIAL NO.', '', 'ID', '', 'NAME','','SEMESTER']
    #         assure_path_exists("StudentDetails/")
    #         assure_path_exists("TrainingImage/")
    #         serial = 0
    #         exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    #         if exists:
    #             with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
    #                 reader1 = csv.reader(csvFile1)
    #                 for l in reader1:
    #                     serial = serial + 1
    #             serial = (serial // 2)
    #             csvFile1.close()
    #         else:
    #             with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
    #                 writer = csv.writer(csvFile1)
    #                 writer.writerow(columns)
    #                 serial = 1
    #             csvFile1.close()
    #         Id = (self.student_id_entry.get())
    #         name = (self.student_name_entry.get())
    #         if ((name.isalpha()) or (' ' in name)):
    #             cam = cv2.VideoCapture(0)
    #             harcascadePath = "haarcascade_frontalface_default.xml"
    #             detector = cv2.CascadeClassifier(harcascadePath)
    #             sampleNum = 0
    #             while (True):
    #                 ret, img = cam.read()
    #                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #                 faces = detector.detectMultiScale(gray, 1.3, 5)
    #                 for (x, y, w, h) in faces:
    #                     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #                     # incrementing sample number
    #                     sampleNum = sampleNum + 1
    #                     # saving the captured face in the dataset folder TrainingImage
    #                     cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
    #                                 gray[y:y + h, x:x + w])
    #                     # display the frame
    #                     cv2.imshow('Taking Images', img)
    #                 # wait for 100 miliseconds
    #                 if cv2.waitKey(100) & 0xFF == ord('q'):
    #                     break
    #                 # break if the sample number is morethan 100
    #                 elif sampleNum > 100:
    #                     break
    #             cam.release()
    #             cv2.destroyAllWindows()
    #             res = "Images Taken for ID : " + Id
    #             row = [serial, '', Id, '', name]
    #             with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
    #                 writer = csv.writer(csvFile)
    #                 writer.writerow(row)
    #             csvFile.close()
    #             #message1.configure(text=res)
    #         else:
    #             if (name.isalpha() == False):
    #                 res = "Enter Correct name"
    #                # message.configure(text=res)

    # def getImagesAndLabels(path):
    #         # get the path of all the files in the folder
    #         imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    #         # create empth face list
    #         faces = []
    #         # create empty ID list
    #         Ids = []
    #         # now looping through all the image paths and loading the Ids and the images
    #         for imagePath in imagePaths:
    #             # loading the image and converting it to gray scale
    #             pilImage = Image.open(imagePath).convert('L')
    #             # Now we are converting the PIL image into numpy array
    #             imageNp = np.array(pilImage, 'uint8')
    #             # getting the Id from the image
    #             ID = int(os.path.split(imagePath)[-1].split(".")[1])
    #             # extract the face from the training image sample
    #             faces.append(imageNp)
    #             Ids.append(ID)
    #         return faces, Ids

    # ###########################################################################################

    # ########################################################################################
    #         check_haarcascadefile()
    # def TrainImages():
    #         assure_path_exists("TrainingImageLabel/")
    #         recognizer = cv2.face_LBPHFaceRecognizer.create()
    #         harcascadePath = "haarcascade_frontalface_default.xml"
    #         detector = cv2.CascadeClassifier(harcascadePath)
    #         faces, ID = getImagesAndLabels("TrainingImage")
    #         try:
    #             recognizer.train(faces, np.array(ID))
    #         except:
    #             mess._show(title='No Registrations', message='Please Register someone first!!!')
    #             return 
    #         recognizer.save("TrainingImageLabel\Trainner.yml")
    #         res = "Profile Saved Successfully"
           
    #         check_haarcascadefile()
    # def TrackImages():
    #         assure_path_exists("Attendance/")
    #         assure_path_exists("StudentDetails/")
    #         for k in tv.get_children():
    #             tv.delete(k)
    #         msg = ''
    #         i = 0
    #         j = 0
    #         recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    #         exists3 = os.path.isfile(r"TrainingImageLabel\Trainner.yml")
    #         if exists3:
    #             recognizer.read(r"TrainingImageLabel\Trainner.yml")
    #         else:
    #             mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
    #             return
    #         harcascadePath = "haarcascade_frontalface_default.xml"
    #         faceCascade = cv2.CascadeClassifier(harcascadePath);

    #         cam = cv2.VideoCapture(0)
    #         font = cv2.FONT_HERSHEY_SIMPLEX
    #         col_names = ['Id', '', 'Name', '', 'Semester', '','Date', '', 'Time']
    #         exists1 = os.path.isfile(r"StudentDetails\StudentDetails.csv")
    #         if exists1:
    #             df = pd.read_csv(r"StudentDetails\StudentDetails.csv")
    #         else:
    #             mess._show(title='Details Missing', message='Students details are missing, please check!')
    #             cam.release()
    #             cv2.destroyAllWindows()
               
    #         while True:
    #             ret, im = cam.read()
    #             gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #             faces = faceCascade.detectMultiScale(gray, 1.2, 5)
    #             for (x, y, w, h) in faces:
    #                 cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
    #                 bb = 'Unknown'
    #                 serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
    #                 if (conf < 50):
    #                     ts = time.time()
    #                     date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    #                     timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%I:%M:%S %p')
    #                     aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
    #                     ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
    #                     sem = df.loc[df['SERIAL NO.'] == serial]['SEMESTER'].values
                        
    #                     ID = str(ID)[1:-1]
    #                     bb = str(aa)[2:-2]
                    
    #                     attendance = [str(ID), '', bb, '', str(sem[0]), '', str(date), '', str(timeStamp)]
                    
    #                 else:
    #                     Id = 'Unknown'
    #                     bb = str(Id)
    #             cv2.putText(im, str(bb), (x, y - 10), font, 1, (255, 255, 255), 2)
    #             cv2.imshow('Taking Attendance', im)
    #             if (cv2.waitKey(1) == ord('q')):
    #                 break
    #         ts = time.time()
    #         date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    #         exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    #         if exists:
    #             with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
    #                 writer = csv.writer(csvFile1)
    #                 writer.writerow(attendance)
    #             csvFile1.close()
    #         else:
    #             with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
    #                 writer = csv.writer(csvFile1)
    #                 writer.writerow(col_names)
    #                 writer.writerow(attendance)
    #             csvFile1.close()
    #         with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
    #             reader1 = csv.reader(csvFile1)
    #             for lines in reader1:
    #                 i = i + 1
    #                 if (i > 1):
    #                     if (i % 2 != 0):
    #                         iidd = str(lines[0]) + '   '
    #                         tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6]), str(lines[8])))
    #         csvFile1.close()
    #         cam.release()
    #         cv2.destroyAllWindows()

    # def psw():
    #         assure_path_exists("TrainingImageLabel/")
    #         exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    #         if exists1:
    #             tf = open("TrainingImageLabel\psd.txt", "r")
    #             key = tf.read()
    #         else:
    #             new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
    #             if new_pas == None:
    #                 mess._show(title='No Password Entered', message='Password not set!! Please try again')
    #             else:
    #                 tf = open("TrainingImageLabel\psd.txt", "w")
    #                 tf.write(new_pas)
    #                 mess._show(title='Password Registered', message='New password was registered successfully!!')
    #                 return
    #         password = tsd.askstring('Password', 'Enter Password', show='*')
    #         if (password == key):
    #             TrainImages()
    #         elif (password == None):
    #             pass
    #         else:
    #             mess._show(title='Wrong Password', message='You have entered wrong password')
if __name__ == "__main__":
    root=Tk ()
    obj=Student(root)
    root. mainloop ()


# In[ ]:




