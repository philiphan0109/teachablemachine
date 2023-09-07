import tkinter as tk
from PIL import Image, ImageGrab, ImageTk, ImageDraw
import torch
from torchvision import transforms

# Load your trained model
model = SimpleCNN(num_classes)
model.load_state_dict(torch.load('models/my_model_name.pth'))
model.eval()

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prediction Board")

        self.canvas = tk.Canvas(root, bg="black", width=500, height=500)
        self.canvas.pack(pady=20)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_last_coordinates)
        
        self.last_x, self.last_y = None, None

        # Add Predict Button
        self.predict_button = tk.Button(root, text="Predict", command=self.predict)
        self.predict_button.pack(pady=20)
        
        # Add Label to display prediction
        self.prediction_label = tk.Label(root, text="", font=('Arial', 14))
        self.prediction_label.pack(pady=20)

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            self.canvas.create_line((self.last_x, self.last_y, x, y), width=10, fill='white', capstyle=tk.ROUND, smooth=tk.TRUE)
        self.last_x, self.last_y = x, y

    def reset_last_coordinates(self, event):  
        self.last_x, self.last_y = None, None

    def clear_screen(self):
        self.canvas.delete("all")
        self.prediction_label.config(text="")

    def predict(self):
        # Capture the current content of the canvas and save as an image
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        
        img = ImageGrab.grab(bbox=(x, y, x1, y1))
        
        # Resize and preprocess
        img_resized = img.resize((64, 64)).convert('RGB')  # Adjust this size if your model expects a different input size
        transform = transforms.Compose([
            transforms.ToTensor(),
            # Add any other transformations here, e.g., normalization if you used it during training
        ])
        
        input_tensor = transform(img_resized).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            output = model(input_tensor)
            predicted_class = output.argmax(dim=1).item()
        
        # Display prediction (assuming you have a dictionary or list called 'classes' mapping indices to labels)
        self.prediction_label.config(text=f"Predicted: {classes[predicted_class]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
