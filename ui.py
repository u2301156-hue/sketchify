import tkinter as tk
from PIL import Image, ImageTk
import os

# ----------------------------
# LOAD IMAGE
# ----------------------------

image_path = input("Enter image file name: ")

if not os.path.exists(image_path):
    print("Image not found.")
    exit()

original_image = Image.open(image_path)

# ----------------------------
# UI CLASS
# ----------------------------

class ProjectionApp:
    def __init__(self, root, image):
        self.root = root
        self.original_image = image
        self.opacity = 70

        root.title("Camera Projection UI")
        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", self.opacity / 100)

        self.frame = tk.Frame(root, bg="black")
        self.frame.pack(fill="both", expand=True)

        self.image_label = tk.Label(self.frame, bg="black")
        self.image_label.pack(expand=True)

        controls = tk.Frame(self.frame, bg="black")
        controls.pack(pady=10)

        # Transparency Slider
        self.slider = tk.Scale(
            controls,
            from_=0,
            to=100,
            orient="horizontal",
            label="Transparency",
            command=self.update_opacity
        )
        self.slider.set(self.opacity)
        self.slider.pack(padx=20)

        root.bind("<Escape>", lambda e: root.destroy())

        self.update_image()

    def update_image(self):
        img = self.original_image.copy()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img.thumbnail((screen_width, screen_height))

        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)

    def update_opacity(self, value):
        self.opacity = int(value)
        self.root.attributes("-alpha", self.opacity / 100)


# ----------------------------
# RUN UI
# ----------------------------

root = tk.Tk()
app = ProjectionApp(root, original_image)
root.mainloop()
