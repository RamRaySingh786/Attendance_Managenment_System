#!/usr/bin/env python
# coding: utf-8

# In[1]:
import subprocess
import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk, messagebox
import mysql.connector
import random
import string
from AttendanceDb import *
import threading
import re

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.configure(bg="#f0f4f8")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.create_login_form()

    def create_login_form(self):
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        logo_label = tk.Label(main_frame, text="👤", font=("Arial", 48), bg="#f0f4f8", fg="#4a90e2")
        logo_label.pack(pady=(0, 20))

        title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(main_frame, text="Face Recognition Attendance System", font=title_font, bg="#f0f4f8", fg="#2c3e50")
        title_label.pack(pady=(0, 30))

        login_frame = tk.Frame(main_frame, bg="#ffffff", padx=40, pady=40, relief="flat", bd=0)
        login_frame.pack(padx=20, pady=20)
        login_frame.config(highlightbackground="#d9d9d9", highlightthickness=1)

        login_label = tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#2c3e50")
        login_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 12), bg="#ffffff", fg="#7f8c8d")
        username_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.username_entry = ttk.Entry(login_frame, font=("Helvetica", 12), width=30)
        self.username_entry.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 15))

        password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 12), bg="#ffffff", fg="#7f8c8d")
        password_label.grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.password_entry = ttk.Entry(login_frame, font=("Helvetica", 12), width=30, show="•")
        self.password_entry.grid(row=4, column=0, columnspan=2, sticky="we", pady=(0, 20))

        login_button = tk.Button(login_frame, text="LOGIN", bg="#4a90e2", fg="#ffffff", 
                                 font=("Helvetica", 12, "bold"), relief="flat", cursor="hand2",
                                 activebackground="#3a7cd5", activeforeground="#ffffff",
                                 command=self.login)
        login_button.grid(row=5, column=0, columnspan=2, sticky="we", pady=(0, 15))
        admin_login_button = tk.Button(login_frame, text="Admin Login", bg="#4a90e2", fg="#ffffff", 
                               font=("Helvetica", 12, "bold"), relief="flat", cursor="hand2",
                               activebackground="#3a7cd5", activeforeground="#ffffff", width=20,  # Width in text units (number of characters)
                               height=1 ,
                               command=self.adminn)
        admin_login_button.grid(row=6, column=0, columnspan=2, sticky="we", pady=(0, 15))
        new_faculty_button = tk.Button(login_frame, text="New Faculty Registration", 
                                       bg="#ffffff", fg="#4a90e2", font=("Helvetica", 10),
                                       relief="flat", cursor="hand2", bd=0,
                                       activeforeground="#3a7cd5", activebackground="#ffffff",
                                       command=self.new_faculty)
        new_faculty_button.grid(row=7, column=0, sticky="w")

        forgot_password_button = tk.Button(login_frame, text="Forgot Password?", 
                                           bg="#ffffff", fg="#4a90e2", font=("Helvetica", 10),
                                           relief="flat", cursor="hand2", bd=0,
                                           activeforeground="#3a7cd5", activebackground="#ffffff",
                                           command=self.forgot_password)
        forgot_password_button.grid(row=7, column=1, sticky="e")
        

        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)
    def adminn(self):
        threading.Thread(target=self.start_admin_page).start()
         
    def start_admin_page(self):
        try:
            subprocess.run(["python", "admin_login_page.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running Home_Page.py: {e}")
    def start_home_page(self):
        try:
            subprocess.run(["python", "Home_Page.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running Home_Page.py: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            conn = connect_to_db()  # Call the common DB connection function
            if conn is not None:
                my_cursor = conn.cursor()

                # Query to check if the user exists in LoginInfo
                my_cursor.execute("SELECT * FROM facultyinfo WHERE BINARY email=%s AND BINARY password=%s", (username, password))
                row = my_cursor.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Invalid Username or Password")
                else:
                    messagebox.showinfo("Success", "Welcome to the System")
                    # Start the Home_Page in a new thread
                    threading.Thread(target=self.start_home_page).start()
                conn.close()  

    def new_faculty(self):
        NewFacultyRegistration(self.root)

    def forgot_password(self):
        ForgotPassword(self.root)

class NewFacultyRegistration:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("New Faculty Registration")
        self.window.geometry("400x600")
        self.window.configure(bg="#f0f4f8")
        self.create_widgets()
    
    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#ffffff", padx=20, pady=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(frame, text="New Faculty Registration", font=("Helvetica", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Contact Number", "contact"),
            ("Institute Email ID", "email"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password"),
        ]

        for i, (label, attr) in enumerate(fields):
            tk.Label(frame, text=label, bg="#ffffff").grid(row=i+1, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i+1, column=1, sticky="ew", pady=5)
            setattr(self, attr, entry)

        tk.Label(frame, text="Security Question", bg="#ffffff").grid(row=len(fields)+1, column=0, sticky="w", pady=5)
        self.security_question = ttk.Combobox(frame, values=["Your birth place", "Your secret", "Your pet's name"],state="readonly")
        self.security_question.grid(row=len(fields)+1, column=1, sticky="ew", pady=5)

        tk.Label(frame, text="Answer", bg="#ffffff").grid(row=len(fields)+2, column=0, sticky="w", pady=5)
        self.security_answer = ttk.Entry(frame)
        self.security_answer.grid(row=len(fields)+2, column=1, sticky="ew", pady=5)

        register_button = tk.Button(frame, text="Register", command=self.register, bg="#4a90e2", fg="#ffffff")
        register_button.grid(row=len(fields)+3, column=0, columnspan=2, sticky="ew", pady=(20, 0))

        frame.columnconfigure(1, weight=1)  
    def check_email_exists(self, email):
        """ Check if the email exists in the database. """
        try:
            conn = connect_to_db()
            if conn is not None:
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT COUNT(*) FROM FacultyInfo WHERE email = %s", (email,))
                count = my_cursor.fetchone()[0]
                conn.close()
                return count > 0  # Returns True if email exists
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error due to {str(e)}")
        return False 
    def validate_fields(self):
        # Get all input data
        first_name = self.first_name.get().strip()
        last_name = self.last_name.get().strip()
        contact = self.contact.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm_password = self.confirm_password.get().strip()
        security_question = self.security_question.get().strip()
        security_answer = self.security_answer.get().strip()

        # First name and last name validation
        if not first_name.isalpha():
            messagebox.showerror("Error", "First name must contain only letters.")
            return False
        if not last_name.isalpha():
            messagebox.showerror("Error", "Last name must contain only letters.")
            return False

        # Contact number validation
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Contact number must be a valid 10-digit number.")
            return False

        # Email validation using regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return False

        # Password validation
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return False
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False

        # Security question and answer validation
        if not security_question:
            messagebox.showerror("Error", "Please select a security question.")
            return False
        if not security_answer:
            messagebox.showerror("Error", "Please provide an answer for the security question.")
            return False

        return True
    def register(self):
       if self.validate_fields():  
            email = self.email.get().strip()
            if self.check_email_exists(email):
                messagebox.showerror("Error", "This email ID is already registered.")
                return
            try:
                conn = connect_to_db()
                if conn is not None:
                    my_cursor = conn.cursor()

                    # Insert the new faculty data into FacultyInfo
                    my_cursor.execute(
                        "INSERT INTO FacultyInfo (first_name, last_name, contact_number, email, password, security_question, security_answer) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (self.first_name.get().strip(), 
                            self.last_name.get().strip(),
                            self.contact.get().strip(),
                            self.email.get().strip(),
                            self.password.get().strip(),
                            self.security_question.get().strip(),
                            self.security_answer.get().strip()
                            )
                    )
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Faculty Registered Successfully")
                    self.window.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error due to {str(e)}")

class ForgotPassword:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Forgot Password")
        self.window.geometry("400x300")
        self.window.configure(bg="#f0f4f8")
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg="#ffffff", padx=20, pady=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(frame, text="Forgot Password", font=("Helvetica", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(frame, text="Registered Email", bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.email = ttk.Entry(frame)
        self.email.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(frame, text="Security Question", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        self.security_question = ttk.Combobox(frame, values=["Your birth place", "Your secret", "Your pet's name"], state="readonly")
        self.security_question.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(frame, text="Answer", bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
        self.security_answer = ttk.Entry(frame)
        self.security_answer.grid(row=3, column=1, sticky="ew", pady=5)

        verify_button = tk.Button(frame, text="Verify", command=self.verify, bg="#4a90e2", fg="#ffffff")
        verify_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(20, 0))

        frame.columnconfigure(1, weight=1)

    def verify(self):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM FacultyInfo WHERE email = %s AND security_question = %s AND security_answer = %s", 
                           (self.email.get(), self.security_question.get(), self.security_answer.get()))
            result = cursor.fetchone()
            conn.close()

            if result:
                self.show_code_entry()
            else:
                messagebox.showerror("Error", "Invalid details. Please try again.")

    def show_code_entry(self):
        # Generate a random 4-digit code
        code = ''.join(random.choices(string.digits, k=4))
        print(f"Generated code: {code}")  # In a real app, this would be sent via email

        code_window = tk.Toplevel(self.window)
        code_window.title("Enter Verification Code")
        code_window.geometry("300x150")

        frame = tk.Frame(code_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Enter the 4-digit code sent to you:").pack()
        code_entry = ttk.Entry(frame)
        code_entry.pack(pady=10)

        def verify_code():
            if code_entry.get() == code:
                messagebox.showinfo("Success", "Code verified. You can now reset your password.")
                code_window.destroy()
                self.show_reset_password_window()
            else:
                messagebox.showerror("Error", "Invalid code. Please try again.")

        verify_button = tk.Button(frame, text="Verify Code", command=verify_code)
        verify_button.pack()

    def show_reset_password_window(self):
        # Create a new window for password reset
        reset_window = tk.Toplevel(self.window)
        reset_window.title("Reset Password")
        reset_window.geometry("300x200")

        frame = tk.Frame(reset_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="New Password:").grid(row=0, column=0, sticky="w", pady=5)
        new_password_entry = ttk.Entry(frame, show="•")
        new_password_entry.grid(row=0, column=1, pady=5, sticky="ew")

        tk.Label(frame, text="Confirm Password:").grid(row=1, column=0, sticky="w", pady=5)
        confirm_password_entry = ttk.Entry(frame, show="•")
        confirm_password_entry.grid(row=1, column=1, pady=5, sticky="ew")

        def reset_password():
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match. Please try again.")
            else:
                try:
                    # Connect to the database and update the password
                    conn = connect_to_db()
                    if conn is not None:
                        my_cursor = conn.cursor()

                        # Assuming the email and security answer were verified earlier
                        email = self.email.get()

                        # Update the password in the FacultyInfo table
                        my_cursor.execute(
                            "UPDATE FacultyInfo SET password = %s WHERE email = %s",
                            (new_password, email)
                        )
                        conn.commit()
                        conn.close()

                        messagebox.showinfo("Success", "Password reset successfully.")
                        reset_window.destroy()

                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error due to {str(e)}")

        # Reset button
        reset_button = tk.Button(frame, text="Reset Password", command=reset_password, bg="#4a90e2", fg="#ffffff")
        reset_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0))

        frame.columnconfigure(1, weight=1)
        
    

if __name__ == "__main__":
    root = tk.Tk()
    app = Login_Window(root)
    root.mainloop()

