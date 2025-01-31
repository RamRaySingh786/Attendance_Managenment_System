import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def connect_to_db():
    try:
        # Modify the connection details as needed
        conn = mysql.connector.connect(
            host='localhost',
            username='root',
            password='',
            database='face_recognizer'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {str(e)}")
        return None
