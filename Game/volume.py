from customtkinter import *
from PIL import Image
import pygame

class VolumeControlLine(CTkCanvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.volume = 100
        self.create_line(20, 10, 180, 10, width=8, fill='gray')
        self.volume_indicator = self.create_rectangle(20, 5, 180, 15, fill='#6666CC')
        self.volume_text = self.create_text(200, 10, text=str(self.volume), anchor='e')

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.update_volume(event.x)

    def on_drag(self, event):
        self.update_volume(event.x)

    def update_volume(self, x):
        self.volume = max(0, min(100, (x - 20) * 100 // 160))
        self.coords(self.volume_indicator, 20, 5, 20 + (160 * self.volume // 100), 15)
        self.itemconfig(self.volume_text, text=str(self.volume))
        self.current_volume = self.set_volume(self.volume / 100)
        self.save_volume(self.volume)

    def set_volume(self, volume_level):
        pygame.mixer.music.set_volume(volume_level)

    def save_volume(self, volume):
        with open('volume_level.txt', 'w') as file:
            file.write(str(volume))

    def load_volume(self):
        try:
            with open('volume_level.txt', 'r') as file:
                self.volume = int(file.read())
                self.update_volume_indicator()
        except FileNotFoundError:
            self.volume = 100

    def update_volume_indicator(self):
        self.coords(self.volume_indicator, 20, 5, 20 + (160 * self.volume // 100), 15)
        self.itemconfig(self.volume_text, text=str(self.volume))
        self.set_volume(self.volume / 100)


# Function to handle "Quay lại" button click
def go_back(volume_window, main_app):
    volume_window.withdraw()
    main_app.deiconify()

# Create the main window
def modify_volume(main_app):
    # Create a new window for the volume control
    volume_window = CTkToplevel(main_app)
    volume_window.title("Volume Control")
    volume_window.geometry("850x500")
    main_app.withdraw()

    # Background image setup
    bg_img = CTkImage(Image.open("./Volume/bgvolume.jpg"), size=(850, 500))
    bg_lab = CTkLabel(volume_window, image=bg_img)
    bg_lab.place(x=0, y=0, relwidth=1, relheight=1)

    # Create "Quay lại" button
    back_button = CTkButton(volume_window, text="Quay lại", command=lambda: go_back(volume_window, main_app), cursor="hand2")
    back_button.place(x=10, y=10)

    # Calculate the position of VolumeControlLine to center it in the window
    canvas_width = 200
    canvas_height = 20
    x_pos = (main_app.winfo_width() - canvas_width) / 2
    y_pos = (main_app.winfo_height() - canvas_height) / 2

    # Create VolumeControlLine instance
    volume_control = VolumeControlLine(volume_window, width=canvas_width, height=canvas_height)
    volume_control.place(x=x_pos, y=y_pos)

    # Load the saved volume level
    volume_control.load_volume()

    volume_window.mainloop()