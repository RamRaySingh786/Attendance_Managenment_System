#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk, messagebox
import threading
import subprocess


# username is admin@123
#password is face@123


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

        login_label = tk.Label(login_frame, text="Admin Login", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#2c3e50")
        login_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

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

        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)

    def login(self):
        # Hardcoded username and password
        correct_username = "admin@123"
        correct_password = "face@123"

        # Get entered username and password
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Check if the entered username and password match the hardcoded values
        if entered_username == correct_username and entered_password == correct_password:
            messagebox.showinfo("Login Success", "Welcome Admin!")
            is_admin = True  # Admin login
            # Start the Home_Page with the admin flag
            threading.Thread(target=self.start_home_page, args=(is_admin,)).start()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
 
    def start_home_page(self, is_admin):
        try:
            # Pass the admin flag as an argument to Home_Page.py
            if is_admin:
                subprocess.run(["python", "Home_Page.py", "--admin"], check=True)
            else:
                subprocess.run(["python", "Home_Page.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running Home_Page.py: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login_Window(root)
    root.mainloop()


# In[ ]:




