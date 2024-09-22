from customtkinter import *
import threading
from PIL import Image
import subprocess
import pygame
from volume import modify_volume
from User import profile_info
# Thiết lập cửa sổ chính
def start_server():
    threading.Thread(target=server_thread, daemon=True).start()

def start_client():
    threading.Thread(target=client_thread, daemon=True).start()

def server_thread():
    subprocess.run(['python', './WaitingRoom/server.py'])

def client_thread():
    subprocess.run(['python', './WaitingRoom/waiting.py'])

def online():
    start_server()
    start_client()

def home(id_user, app):
    def offline_mode():
        pygame.mixer.stop()
        home_window.destroy()
        subprocess.run(['python', 'Ponggame.py'])
        subprocess.run(['python', 'main.py'])
        exit()

    def pve_mode():
        pygame.mixer.stop()
        home_window.destroy()
        subprocess.run(['python', 'PongCPU.py'])
        subprocess.run(['python', 'main.py'])
        exit()
    
    def pvp_mode():
        pygame.mixer.stop()
        home_window.destroy()
        online()

    def play_sound():
        modify_volume(home_window)
    def notification():
        subprocess.run(["python", "./Notification/notification.py"])

    def profile(id_user,window):
        
        profile_info(int(id_user), window)

    def return_home():
        btn_play.place(x=370, y=300)
        tab_personal.place(x=10, y=20)
        tab_notifications.place(x=550, y=20)
        tab_sound.place(x=720, y=20)

        btn_online.place_forget()
        btn_machine.place_forget()
        btn_offline.place_forget()
        return_label.place_forget()

    def mode_games():
        global btn_machine
        global btn_offline
        global btn_online
        global return_label

        btn_machine = CTkButton(home_window, text='MÁY',command=pve_mode, width=120, height=50, corner_radius=5, cursor="hand2")
        btn_machine.place(x=220, y=200)

        btn_offline = CTkButton(home_window, text='OFFLINE',command=offline_mode, width=120, height=50)
        btn_offline.place(x=370, y=200)

        btn_online = CTkButton(home_window, text='ONLINE',command=pvp_mode, width=120, height=50)
        btn_online.place(x=520, y=200)

        btn_play.place_forget()
        tab_notifications.place_forget()
        tab_sound.place_forget()
        tab_personal.place_forget()

        return_label = CTkButton(home_window, text='Trở về',command=return_home, width=120, height=30)
        return_label.place(x=10, y=20)

    home_window = CTkToplevel(app)
    home_window.title("PONG GAME")
    home_window.geometry("850x500")
    app.withdraw()
    
    bg_img = CTkImage(dark_image=Image.open("bgmain.jpg"), size=(850, 500))

    bg_lab = CTkLabel(home_window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    # Tạo nút 'Play'
    btn_play = CTkButton(home_window, text='PLAY', command=mode_games, fg_color='purple', width=120, height=50)
    btn_play.place(x=370, y=300)

    # Tạo các tab ở đầu cửa sổ
    tab_personal = CTkButton(home_window, text='Trang cá nhân',command=lambda:profile(id_user, home_window), width=120, height=30)
    tab_personal.place(x=10, y=20)

    tab_notifications = CTkButton(home_window, text='Thông báo',command=notification, width=120, height=30)
    tab_notifications.place(x=550, y=20)

    tab_sound = CTkButton(home_window, text='Âm thanh',command=play_sound, width=120, height=30)
    tab_sound.place(x=720, y=20)

    pygame.mixer.init()
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.play(-1)

    home_window.mainloop()
