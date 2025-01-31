from tkinter import *
from tkinter import ttk

class Face_Recognition:
    def _init_(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Set the whole background to white
        self.root.configure(bg="white")

        # Create the title label
        title_lbl = Label(self.root, text="Face Recognition To Mark Attendance", font=("Arial", 30, "bold"), bg="white", fg="#4a90e2")
        title_lbl.place(relx=0.5, y=0, anchor="n", width=1530, height=45)

        # Create the label for the button instruction (same blue as title)
        instruction_lbl = Label(self.root, text="Click the button below to mark your attendance", font=("Arial", 20), bg="white", fg="#4a90e2")
        instruction_lbl.place(relx=0.5, rely=0.4, anchor="center")

        # Create a canvas for rounded button
        self.canvas = Canvas(self.root, width=300, height=100, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Draw rounded rectangle (simulating rounded button)
        self.canvas.create_rounded_rectangle = self._create_rounded_rectangle(10, 10, 300, 100, 50, outline="", fill="#4a90e2")

        # Create text inside the canvas (button text)
        self.canvas.create_text(150, 50, text="Mark Attendance", font=("Arial", 20, "bold"), fill="white")

    # Function to draw rounded rectangle
    def _create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, 
                  x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, 
                  x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, 
                  x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

if __name__ == "_main_":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()