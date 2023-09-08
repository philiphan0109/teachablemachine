import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageGrab
import datetime
import os
import io

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doodle")

        self.canvas = tk.Canvas(root, bg="black", width=500, height=500)
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
            self.canvas.create_line((self.last_x, self.last_y, x, y), width=10, fill='white', capstyle=tk.ROUND, smooth=tk.TRUE)
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
            # Save canvas content as postscript
            ps = self.canvas.postscript(colormode='color')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            
            # Convert to RGBA for potential transparency handling (if needed in the future)
            img = img.convert("RGBA")
            
            # Convert image to white background with black drawing
            img_rgba = img.copy()
            img_rgba_data = img_rgba.getdata()
            newData = []
            for item in img_rgba_data:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img_rgba.putdata(newData)
            background = Image.new("RGB", img.size, "white")
            background.paste(img_rgba, (0, 0), img_rgba)
            
            background.save(save_path)

        self.clear_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()