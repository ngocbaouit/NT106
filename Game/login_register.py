import mysql.connector
import secrets
import customtkinter as ctk
import bcrypt
from tkinter import messagebox
from tkinter import *
import re
from PIL import Image, ImageTk
from main import home

import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env")

app = ctk.CTk()
app.title('PONG GAME')
app.geometry('850x500')
app.config(bg='#001220')

font1 = ('Helvetica', 25, 'bold')
font2 = ('Arial', 17, 'bold')
font3 = ('Arial', 13, 'bold')
font4 = ('Arial', 13, 'bold', 'underline')

conn = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER")
                                             , password=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
cursor = conn.cursor()

# Load background image
background_image = Image.open("img/login.jpg")  # Replace with your image path
background_photo = ImageTk.PhotoImage(background_image.resize((1050, 700)))

def generate_random_two_digit_number():
    return secrets.randbelow(90) + 10

def isEmail(email):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.search(regex, email) is not None

def login_register():
    def clear_noti(signup_notification_label):
        signup_notification_label.place_forget()
        signup_button.place(x=310, y=380)
        login_label.place(x=310, y=420)
        login_button.place(x=435, y=420)

    def clear_noti1(login_noti):
        login_noti.place_forget()
        login_button2.place(x=310, y=310)
        signup_label2.place(x=310, y=350)
        signup_button2.place(x=450, y=350)

    def signup():
        global id_user
        id_user = generate_random_two_digit_number()
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        accountname = username
        global signup_notification_label
        signup_notification_label = ctk.CTkLabel(frame1, font=font3, text='', text_color='#ff0000', bg_color='#001220')

        if username != '' and password != '' and email != '':
            cursor.execute('SELECT Tên_đăng_nhập FROM USERS WHERE Tên_đăng_nhập= %s', [username,])
            if cursor.fetchone() is not None:
                signup_notification_label.configure(text='*Tên đăng nhập đã tồn tại')
                signup_notification_label.place(x=310, y=360)
                signup_button.place(x=310, y=390)
                login_label.place(x=310, y=420)
                login_button.place(x=435, y=420)
            elif not isEmail(email):
                signup_notification_label.configure(text='*Email không hợp lệ')
                signup_notification_label.place(x=310, y=360)
                signup_button.place(x=310, y=390)
                login_label.place(x=310, y=420)
                login_button.place(x=435, y=420)
            else:
                salt = bcrypt.gensalt()
                password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(password, salt)
                cursor.execute('INSERT INTO USERS (id_user, Tên_đăng_nhập, Mật_khẩu, Email, Tên_người_dùng, salt) VALUES (%s, %s, %s, %s, %s, %s)', 
                            [id_user, username, hashed_password, email, accountname, salt])
                conn.commit()
                messagebox.showinfo('Thông báo', 'Đăng ký thành công')
                login()
        else:
            signup_notification_label.configure(text='*Vui lòng nhập đầy đủ thông tin')
            signup_notification_label.place(x=310, y=360)
            signup_button.place(x=310, y=390)
            login_label.place(x=310, y=420)
            login_button.place(x=435, y=420)

        username_entry.bind('<FocusIn>', lambda event, signup_notification_label=signup_notification_label: clear_noti(signup_notification_label))
        password_entry.bind('<FocusIn>', lambda event, signup_notification_label=signup_notification_label: clear_noti(signup_notification_label))
        email_entry.bind('<FocusIn>', lambda event, signup_notification_label=signup_notification_label: clear_noti(signup_notification_label))

    def login_account():
        username = username_entry2.get()
        password = password_entry2.get()
        login_notification_label = ctk.CTkLabel(frame2, font=font3, text='', text_color='#ff0000', bg_color='#001220')

        if username != '' and password != '':
            cursor.execute('SELECT Mật_khẩu, SALT FROM USERS WHERE Tên_đăng_nhập= %s', [username,])
            result = cursor.fetchone()
            if result:
                stored_hashed_password = result[0].encode('utf-8')  # Retrieved as string
                salt = result[1].encode('utf-8')
                password = password.encode('utf-8')
                if bcrypt.hashpw(password, salt) == stored_hashed_password:
                    cursor.execute('SELECT id_user FROM USERS WHERE Tên_đăng_nhập= %s', [username,])
                    id_user = cursor.fetchall()
                    id_user = int(''.join(map(str, id_user[0])))
                    home(id_user, app)
                else:
                    login_notification_label.configure(text='*Sai mật khẩu, vui lòng nhập lại')
                    login_notification_label.place(x=310, y=300)
                    login_button2.place(x=310, y=330)
                    signup_label2.place(x=310, y=370)
                    signup_button2.place(x=450, y=370)
            else:
                login_notification_label.configure(text='*Không tồn tại tên đăng nhập')
                login_notification_label.place(x=310, y=300)
                login_button2.place(x=310, y=330)
                signup_label2.place(x=310, y=370)
                signup_button2.place(x=450, y=370)
        else:
            login_notification_label.configure(text='*Vui lòng nhập đầy đủ thông tin')
            login_notification_label.place(x=310, y=300)
            login_button2.place(x=310, y=330)
            signup_label2.place(x=310, y=370)
            signup_button2.place(x=450, y=370)

        username_entry2.bind('<FocusIn>', lambda event, login_noti=login_notification_label: clear_noti1(login_noti))
        password_entry2.bind('<FocusIn>', lambda event, login_noti=login_notification_label: clear_noti1(login_noti))

    def login():
        frame1.destroy()
        global frame2
        frame2 = ctk.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=850, height=500)
        frame2.place(x=0, y=0)

        # Set background image
        background_label2 = Label(frame2, image=background_photo)
        background_label2.place(x=0, y=0, relwidth=1, relheight=1)

        login_label2 = ctk.CTkLabel(frame2, font=font1, text='Đăng nhập', text_color='#fff', bg_color='#001220')
        login_label2.place(x=345, y=100)

        global username_entry2
        global password_entry2
        global login_button2
        global signup_label2
        global signup_button2

        username_entry2 = ctk.CTkEntry(frame2, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Tên đăng nhập', placeholder_text_color='#a3a3a3', width=200, height=50)
        username_entry2.place(x=310, y=170)

        password_entry2 = ctk.CTkEntry(frame2, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Mật khẩu', placeholder_text_color='#a3a3a3', width=200, height=50)
        password_entry2.place(x=310, y=240)

        login_button2 = ctk.CTkButton(frame2, command=login_account, font=font2, text_color='#fff', text='Đăng nhập', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5, width=200)
        login_button2.place(x=310, y=310)

        signup_label2 = ctk.CTkLabel(frame2, font=font3, text='Chưa có tài khoản ?', text_color='#fff', bg_color='#001220')
        signup_label2.place(x=310, y=350)

        signup_button2 = ctk.CTkButton(frame2, command=redirect, font=font4, text_color='#00bf77', text='Đăng ký', fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
        signup_button2.place(x=450, y=350)

    def redirect():
        frame2.destroy()
        global frame1
        frame1 = ctk.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=850, height=500)
        frame1.place(x=0, y=0)

        # Set background image
        background_label1 = Label(frame1, image=background_photo)
        background_label1.place(x=0, y=0, relwidth=1, relheight=1)

        global username_entry
        global password_entry
        global email_entry
        global signup_button
        global login_label
        global login_button

        signup_label = ctk.CTkLabel(frame1, font=font1, text='Đăng ký', text_color='#fff', bg_color='#001220')
        signup_label.place(x=360, y=100)

        username_entry = ctk.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Tên đăng nhập', placeholder_text_color='#a3a3a3', width=200, height=50)
        username_entry.place(x=310, y=170)

        password_entry = ctk.CTkEntry(frame1, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Mật khẩu', placeholder_text_color='#a3a3a3', width=200, height=50)
        password_entry.place(x=310, y=240)

        email_entry = ctk.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Email', placeholder_text_color='#a3a3a3', width=200, height=50)
        email_entry.place(x=310, y=310)

        signup_button = ctk.CTkButton(frame1, command=signup, font=font2, text_color='#fff', text='Đăng ký', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5, width=200)
        signup_button.place(x=310, y=380)

        login_label = ctk.CTkLabel(frame1, font=font3, text='Đã có tài khoản ?', text_color='#fff', bg_color='#001220')
        login_label.place(x=310, y=420)

        login_button = ctk.CTkButton(frame1, command=login, font=font4, text_color='#00bf77', text='Đăng nhập', fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
        login_button.place(x=435, y=420)

    frame1 = ctk.CTkFrame(app, bg_color='#001220', fg_color='#001220', width=850, height=500)
    frame1.place(x=0, y=0)

    # Set background image
    background_label1 = Label(frame1, image=background_photo)
    background_label1.place(x=0, y=0, relwidth=1, relheight=1)

    signup_label = ctk.CTkLabel(frame1, font=font1, text='Đăng ký', text_color='#fff', bg_color='#001220')
    signup_label.place(x=360, y=100)

    username_entry = ctk.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Tên đăng nhập', placeholder_text_color='#a3a3a3', width=200, height=50)
    username_entry.place(x=310, y=170)

    password_entry = ctk.CTkEntry(frame1, font=font2, show='*', text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Mật khẩu', placeholder_text_color='#a3a3a3', width=200, height=50)
    password_entry.place(x=310, y=240)

    email_entry = ctk.CTkEntry(frame1, font=font2, text_color='#fff', fg_color='#001a2e', bg_color='#121111', border_color='#004780', border_width=3, placeholder_text='Email', placeholder_text_color='#a3a3a3', width=200, height=50)
    email_entry.place(x=310, y=310)

    signup_button = ctk.CTkButton(frame1, command=signup, font=font2, text_color='#fff', text='Đăng ký', fg_color='#00965d', hover_color='#006e44', bg_color='#121111', cursor='hand2', corner_radius=5, width=200)
    signup_button.place(x=310, y=380)

    login_label = ctk.CTkLabel(frame1, font=font3, text='Đã có tài khoản ?', text_color='#fff', bg_color='#001220')
    login_label.place(x=310, y=420)

    login_button = ctk.CTkButton(frame1, command=login, font=font4, text_color='#00bf77', text='Đăng nhập', fg_color='#001220', hover_color='#001220', cursor='hand2', width=40)
    login_button.place(x=435, y=420)

    app.mainloop()
    return id_user

if __name__ == "__main__":
    login_register()
