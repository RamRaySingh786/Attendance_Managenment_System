#!/usr/bin/env python
# coding: utf-8

# In[7]:
import webbrowser
import subprocess
import tkinter as tk
from tkinter import font as tkfont
from tkinter import PhotoImage  # Import PhotoImage to load images
from face_recognition import Face_Recognition
import os
import threading
import sys
from tkinter import messagebox


class IconButton(tk.Canvas):
    def __init__(self, master, icon_path, text, command, *args, **kwargs):  # Corrected to __init__
        super().__init__(master, *args, **kwargs)  # Corrected to __init__
        self.configure(bg="#4a86e8", highlightthickness=0, width=130, height=130)
        self.text = text
        self.command = command
        self.icon = PhotoImage(file=icon_path)  # Load the custom icon
        #self.draw_button()
        self.draw_icon()
        self.draw_text()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    def draw_button(self):
        # Draw rounded rectangle
        radius = 20  # Corner radius
        self.create_arc(0, 0, radius * 2, radius * 2, start=90, extent=90, fill="#4a86e8", outline="#4a86e8")
        self.create_arc(100, 0, 130, radius * 2, start=0, extent=90, fill="#4a86e8", outline="#4a86e8")
        self.create_arc(0, 100 - radius * 2, radius * 2, 130, start=180, extent=90, fill="#4a86e8", outline="#4a86e8")
        self.create_arc(100, 100 - radius * 2, 130, 130, start=270, extent=90, fill="#4a86e8", outline="#4a86e8")
        self.create_rectangle(radius, 0, 130 - radius, 130, fill="#4a86e8", outline="#4a86e8")  # Middle rectangle
        self.create_rectangle(0, radius, 130, 130 - radius, fill="#4a86e8", outline="#4a86e8")  # Middle rectangle
        
    def draw_icon(self):
        self.create_image(65, 50, image=self.icon)  # Draw the icon at the center
        

    def draw_text(self):
        self.create_text(65, 105, text=self.text, fill="white", font=("Arial", 12, "bold"), width=110, justify="center")

    def _on_click(self, event):
        self.configure(bg="#2a66c8")
        self.after(100, self._reset_color)
        self.command()

    def _on_enter(self, event):
        self.configure(bg="#3a76d8")

    def _on_leave(self, event):
        self.configure(bg="#4a86e8")

    def _reset_color(self):
        self.configure(bg="#4a86e8")

class AttendanceSystemUI:
    def __init__(self, root):  # Corrected to __init__
        self.root = root
        self.root.title("Face Recognition Attendance Management System")
        #self.root.state('zoomed')
        
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.is_admin = "--admin" in sys.argv
        self.create_widgets()

    def create_widgets(self):
        title_font = tkfont.Font(family="Arial", size=28, weight="bold")
        

        # Title
        title_label = tk.Label(self.root, text="Face Recognition Attendance\nManagement System",
                                font=title_font, bg="#f0f0f0", fg="#4a86e8")
        title_label.pack(padx=20, pady=10)  # Padding inside the frame
        if self.is_admin:
            title_label = tk.Label(self.root, text="Admin Side",
                                font=title_font, bg="#f0f0f0", fg="#4a86e8")
            title_label.pack(pady=(30, 20))
        # Frame for icon buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(expand=True)

        # Icon buttons (use the path to your icons)
        icons = [
            ("icons/Users.png", "Student\nDetails", self.student_details),
            ("icons/Camera.png", "Mark\nAttendance", self.face_detection),
            ("icons/List.png", "Attendance\nRecord", self.attendance_record),
            ("icons/Help circle.png", "Help", self.help_function)
        ]
        if self.is_admin:
            icons.insert(1, ("icons/Users.png", "Train\nData", self.train))  # Insert at position 1

        self.buttons = []
        for i, (icon_path, text, command) in enumerate(icons):
            button = IconButton(button_frame, icon_path, text, command)
            button.grid(row=0, column=i, padx=20, pady=20)
            self.buttons.append(button)

        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit,
                                width=20, height=2, font=("Arial", 14, "bold"),
                                bg="#ff6b6b", fg="white", activebackground="#ff4757",
                                activeforeground="white", relief=tk.FLAT)
        exit_button.pack(side=tk.BOTTOM, pady=40)

        # Add rounded corners to the exit button
        exit_button.bind("<Enter>", lambda e: exit_button.configure(bg="#ff4757"))
        exit_button.bind("<Leave>", lambda e: exit_button.configure(bg="#ff6b6b"))
    def st_details(self):
        try:
            subprocess.run(["python", "sm (5).py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running student.py: {e}")
    def train(self):
        # Training logic here
        # Simulating training process with a 2-second delay
        print("Training in progress...")

        # Schedule the success message after 3 seconds
        self.root.after(3000, self.show_success_message)  # 3000 milliseconds = 3 seconds

    def show_success_message(self):
        messagebox.showinfo("Training Completed", "Training completed successfully!")

    def manual_at(self):
        try:
            subprocess.run(["python", "attendance (2).py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running student.py: {e}")
    def mark_att(self):
        try:
            subprocess.run(["python", "face_recognition.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running student.py: {e}")

    def student_details(self):
        threading.Thread(target=self.st_details).start()
        self.highlight_button(0)
    def attendance_record(self):
        threading.Thread(target=self.manual_at).start()
        self.highlight_button(0)

    def face_detection(self):
        threading.Thread(target=self.mark_att).start()
        self.highlight_button(0)

    def help_function(self):
        pdf_path = os.path.abspath(r"C:\Users\Dell\Downloads\Help Manual.pdf")
        
        # Open the PDF using the default PDF viewer
        webbrowser.open_new(pdf_path)

    def highlight_button(self, index):
        for i, button in enumerate(self.buttons):
            if i == index:
                button.configure(bg="#7B68EE")
            else:
                button.configure(bg="#4a86e8")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystemUI(root)  # Pass root to the class
    root.mainloop()

