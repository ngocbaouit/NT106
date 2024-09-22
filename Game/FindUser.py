from customtkinter import CTk, CTkCanvas, CTkButton, CTkImage, CTkLabel, CTkTextbox, CTkEntry, CTkToplevel
import mysql.connector
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import messagebox
from Results import Result

import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env")

def go_back(window, main_app):
    window.withdraw()
    main_app.deiconify()

def Find(main_app, id1):
    def Find_user():
        global result
        # Connect to the database
        connection = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"),
                                             password=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
        cursor = connection.cursor()
        name = Name_tb.get()
        try:
            cursor.execute("SELECT * FROM users WHERE Tên_người_dùng = %s", (name,))
            result = cursor.fetchall()
            if not result:
                messagebox.showinfo("Thông báo", "Không tìm thấy người dùng")
                print("No user found")
            else:
                Result(result, window, id1)
        except Exception as e:
            print(e)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    # Main window
    window = CTkToplevel(main_app)
    window.geometry("650x350")
    window.configure(bg="#2B5955")
    window.resizable(False, False)
    window.title("Find User")
    main_app.withdraw()

    # Load and place the background image
    background_image_path = Path("img/finduser_bg.jpg")  # Replace with your image path
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((850, 450))
    background_photo = ImageTk.PhotoImage(background_image)

    canvas = CTkCanvas(window, width=650, height=350)
    canvas.create_image(0, 0, image=background_photo, anchor='nw')
    canvas.pack(fill='both', expand=True)

    Name_label = CTkLabel(window, text="User Name:", font=("OpenSans Regular", 20), bg_color='#945305')
    Name_label.place(x=120, y=120)

    Name_tb = CTkEntry(window, width=200, height=20, corner_radius=10, fg_color="#2B5955", font=("OpenSans Regular", 20))
    Name_tb.place(x=270, y=120)

    Find_btn = CTkButton(window, text="Find", height=30, width=50, command=Find_user).place(x=260, y=170)

    back_btn = CTkButton(window, text="Quay lại", width=120, height=30, command=lambda: go_back(window, main_app)).place(x=10, y=10)

    window.mainloop()
