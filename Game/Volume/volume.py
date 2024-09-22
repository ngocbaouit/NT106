import tkinter as tk
from PIL import Image, ImageTk
class VolumeControlLine(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.volume = 0
        self.create_line(20, 10, 180, 10, width=8, fill='gray')  # Volume control line
        self.volume_indicator = self.create_rectangle(20, 5, 20, 15, fill='#6666CC')  # Initial volume indicator
        self.volume_text = self.create_text(200, 10, text=str(self.volume), anchor='e')  # Volume level text on the right
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
    
    def on_click(self, event):
        self.update_volume(event.x)
    
    def on_drag(self, event):
        self.update_volume(event.x)
    
    def update_volume(self, x):
        self.volume = max(0, min(100, (x - 20) * 100 // 160))
        self.coords(self.volume_indicator, 20, 5, 20 + (160 * self.volume // 100), 15)
        self.itemconfig(self.volume_text, text=str(self.volume))  # Update volume level text

# Function to handle "Quay lại" button click
def go_back():
    print("Go back button clicked!")  # Replace this with your desired action

# Create the main window

root = tk.Tk()
root.title("Volume Control Line Example")

# Set the size of the main window
window_width = 850
window_height = 500
root.geometry(f"{window_width}x{window_height}")

# Calculate the position of VolumeControlLine to center it in the window
canvas_width = 200  # Set a smaller width for the canvas
canvas_height = 20
x_pos = (window_width - canvas_width) / 2
y_pos = (window_height - canvas_height) / 2
bg_img = Image.open("./Volume/Volume/Volume/bgvolume.jpg")
bg_img = bg_img.resize((850, 500))
bg_img = ImageTk.PhotoImage(bg_img)
bg_lab = tk.Label(root, image=bg_img)
bg_lab.place(x=0, y=0, relwidth=1, relheight=1)
# Create "Quay lại" button
back_button = tk.Button(root, text="Quay lại", command=go_back, cursor="hand2", background="#669966", foreground="black", font=("Helvetica", 8, "bold"))
back_button.place(x=10, y=10)  # Position the button at the top left corner

# Create VolumeControlLine instance
volume_control = VolumeControlLine(root, width=canvas_width, height=canvas_height)

# Use place to position VolumeControlLine in the center of the window
volume_control.place(x=x_pos, y=y_pos)


root.mainloop()
