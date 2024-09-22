import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import socket
import threading
from PIL import ImageDraw

class ClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Phòng Chờ")

        # Cập nhật đường dẫn của avatar
        self.avatar_image = Image.open('background.jpg')
        self.avatar_image = self.avatar_image.resize((200, 200))  
        self.avatar_image = self.avatar_image.convert("RGBA")  
        self.avatar_image = self.make_circle(self.avatar_image)  
        self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)
        self.avatar_label = tk.Label(master, image=self.avatar_photo)
        self.avatar_label.pack()

        self.chat_frame = tk.Frame(master)
        self.chat_log = scrolledtext.ScrolledText(self.chat_frame, height=10, width=50, state='disabled')
        self.chat_log.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.send_button = tk.Button(self.chat_frame, text="Gửi", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        self.status_label = tk.Label(master, text="Chưa sẵn sàng")
        self.status_label.pack()

        self.ready_button = tk.Button(master, text="Sẵn sàng", command=self.send_ready, background="green", foreground="black")
        self.ready_button.pack(pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345
        self.client_socket.connect((self.host, self.port))

        threading.Thread(target=self.receive_message, daemon=True).start()

    def send_ready(self):
        self.client_socket.sendall("READY".encode())
        self.ready_button.config(state=tk.DISABLED)
        self.chat_log.config(state=tk.NORMAL) 
        # self.chat_log.insert(tk.END, f"{self.host} đã sẵn sàng!\n")  
        # self.chat_log.config(state=tk.DISABLED) 
        # self.chat_log.yview(tk.END) 
        
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.sendall(message.encode())
            self.message_entry.delete(0, tk.END)
    
    def receive_message(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            if message == "START":
                self.status_label.config(text="Bắt đầu trận đấu!")
                # Thêm logic để redirect đến PongOnl :))
            else:
                # Cập nhật chat log
                self.chat_log.config(state=tk.NORMAL)
                self.chat_log.insert(tk.END, f"{message}\n") 
                self.chat_log.config(state=tk.DISABLED)
                self.chat_log.yview(tk.END)

    def make_circle(self, image):
        width, height = image.size
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        result = Image.new("RGBA", (width, height))
        result.paste(image, (0, 0), mask=mask)
        return result

root = tk.Tk()
app = ClientApp(root)
root.mainloop()

