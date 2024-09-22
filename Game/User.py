from pathlib import Path
import mysql.connector
from FindUser import Find
from FriendList import friend_list
from tkinter import filedialog
# Explicit imports to satisfy Flake8
import customtkinter as ctk
from customtkinter import CTk, CTkCanvas, CTkButton, CTkImage, CTkLabel, CTkToplevel
from PIL import Image

import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env") 

new_image_path = None
HOST = os.getenv("HOST")
USER = os.getenv("USER")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")
def change_image(image_label, id, event=None):
    global new_image_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        new_image = Image.open(file_path)
        new_ctk_image = ctk.CTkImage(dark_image=new_image, size=(120, 120))
        image_label.configure(image=new_ctk_image)
        image_label.image = new_ctk_image
        new_image_path = file_path
def save_image_change(id):
    global new_image_path
    if new_image_path:
        # Update the image path in the database
        connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cursor = connection.cursor()
        cursor.execute("UPDATE USERS SET image_path = %s WHERE id_user = %s", [new_image_path, id[0],])
        connection.commit()
        cursor.close()
        connection.close()  
def go_back(window, main_app, id):
    save_image_change(id)
    window.withdraw()
    main_app.deiconify()
def find_user(window, id):
    window.withdraw()
    Find(window, id)
def profile_info(id, main_app):
    window = CTkToplevel(main_app)
    window.title("Profile")
    window.geometry("850x500")
    window.configure(bg = "#2B5955")
    main_app.withdraw()

    connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT id_user, email, Tên_người_dùng, image_path FROM USERS where id_user = %s", [id,])
    rows = cursor.fetchall()
    id_user = [row[0] for row in rows]
    email = [row[1] for row in rows]
    name = [row[2] for row in rows]
    image_path = [row[3] for row in rows]
    
    # Create the main window
    bg_img = CTkImage(dark_image=Image.open("./assets/image_1.png"), size=(850, 500))
    bg_lab = CTkLabel(window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    # Avatar
    ava_bg = CTkImage(dark_image=Image.open("./assets/image_3.png"), size=(185, 185))
    ava_bg_lab = CTkLabel(window, image=ava_bg, text="")
    ava_bg_lab.place(x=80, y=110)

    try:  
        ava = CTkImage(dark_image=Image.open(image_path[0]), size=(120, 120))
    except AttributeError:
        ava = CTkImage(dark_image=Image.open("./assets/image_4.png"), size=(120, 120))
    ava_lab = CTkLabel(window, image=ava, text="", bg_color='transparent')
    ava_lab.place(x=112, y=143)
    change_image_button = ctk.CTkButton(window, text="Change Image", command=lambda:change_image(ava_lab, id),width=120, height=20)
    change_image_button.place(x=112, y=270)
    
    # Info
    info_bg = CTkImage(dark_image=Image.open("./assets/image_2.png"), size=(400, 185))
    info_bg_lab = CTkLabel(window, image=info_bg, text="ID: " + "\t" + str(id_user[0]) + "\n\nUsername: " + str(name[0]) + "\n\nEmail:" + "\t" + str(email[0]),
                        font=("OpenSans Regular", 20), anchor='e',
                        fg_color='#FF9388', bg_color='transparent', justify='left')
    info_bg_lab.place(x=350, y=110)

    # Back button
    back_btn = CTkButton(window, text='Quay lại', command=lambda:go_back(window,main_app, id), width=120, height=30,
                        fg_color='#407777', hover_color='#FF7B81',
                        bg_color='transparent', corner_radius=10)
    back_btn.place(x=10, y=20)

    # History button
    history_btn = CTkButton(window, text='Lịch sử đấu', width=120, height=50,
                        fg_color='#407777', hover_color='#FF7B81',
                        bg_color='transparent', corner_radius=10)
    history_btn.place(x=110, y=350)

    # friend button
    
    friend_btn = CTkButton(window, text='Danh sách bạn bè', width=120, height=50,
                        fg_color='#407777', hover_color='#FF7B81',
                        bg_color='transparent', corner_radius=10, command=lambda:friend_list(window, id))
    friend_btn.place(x=370, y=350)

    find_user_btn = CTkButton(window, text='Tìm bạn bè',command=lambda:Find(window,id), width=120, height=50,
                        fg_color='#407777', hover_color='#FF7B81',
                        bg_color='transparent', corner_radius=10)
    find_user_btn.place(x=570, y=350)

    window.resizable(False, False)
    window.mainloop()