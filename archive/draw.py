import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageGrab
import datetime
import os
import io

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doodle")

        self.canvas = tk.Canvas(root, bg="white", width=500, height=500)
        self.canvas.pack(pady=20)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_last_coordinates)

        self.label_label = tk.Label(root, text="Enter doodle label:")
        self.label_label.pack(pady=5)
        self.label_text = tk.StringVar()
        self.label_entry = tk.Entry(root, textvariable=self.label_text)
        self.label_entry.pack(pady=10)
        
        self.button_save = tk.Button(root, text="Save Doodle", command=self.save_doodle)
        self.button_save.pack(pady=20)
        
        self.last_x, self.last_y = None, None
        self.filename = 0

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            self.canvas.create_line((self.last_x, self.last_y, x, y), width=10, fill='black', capstyle=tk.ROUND, smooth=tk.TRUE)
        self.last_x, self.last_y = x, y

    def reset_last_coordinates(self, event):  
        self.last_x, self.last_y = None, None

    def clear_screen(self):
        self.canvas.delete("all")

    def generate_filename(self):
        self.filename += 1
        now = datetime.datetime.now()
        now = "{}-{}-{}-{}-{}-{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        return f"doodle{self.filename}{now}.png"
    
    def save_doodle(self):
        label = self.label_text.get().strip()  # Get the label from the entry
        if not label:
            # If the label is empty, show a warning
            tk.messagebox.showwarning("Warning", "Please enter a label before saving.")
            return

        filename = self.generate_filename()

        # Determine the path based on the label
        image_folder_path = os.path.join(os.getcwd(), 'images', label)
        
        # Ensure the directory exists; if not, create it
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        # Set initialdir to the path of the labeled folder
        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")], 
                                                initialfile=filename, 
                                                initialdir=image_folder_path)  

        if save_path:
            # Convert the canvas content to an image using postscript
            ps = self.canvas.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(save_path)
        
        self.clear_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
