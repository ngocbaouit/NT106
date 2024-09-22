import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Lưu trạng thái sẵn sàng của người chơi
players_ready = [False, False]

# Khởi tạo socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
server.bind((host, port))
server.listen(2)

# Tạo giao diện đồ họa
window = tk.Tk()
window.title("Server Status")

# Tạo widget để hiển thị log
log = scrolledtext.ScrolledText(window, width=40, height=10, state='disabled')
log.grid(row=0, column=0, padx=10, pady=10)

def update_log(message):
    log.configure(state='normal')
    log.insert(tk.END, message + "\n")
    log.configure(state='disabled')
    log.yview(tk.END)

def client_thread(conn, player):
    global players_ready
    while True:
        try:
            message = conn.recv(1024).decode()
            if message == "READY":
                players_ready[player] = True
                update_log(f"Player {player + 1} is ready")
                # Gửi thông báo đến tất cả các client
                broadcast(f"Player {player + 1} is ready")
                # Kiểm tra xem cả hai người chơi đã sẵn sàng chưa
                if all(players_ready):
                    broadcast("START")
                    update_log("Both players are ready. Starting the game...")
            elif message == "QUIT":
                break
            else:
                # Xử lý tin nhắn chat và chuyển tiếp đến tất cả các client khác
                update_log(f"Message from player {player + 1}: {message}")
                broadcast(f"Player {player + 1}: {message}")
        except:
            break

    conn.close()

def broadcast(message):
    for conn in connections:
        conn.sendall(message.encode())

def accept_connections():
    for i in range(2):
        conn, addr = server.accept()
        update_log(f"Connected by {addr}")
        connections.append(conn)
        threading.Thread(target=client_thread, args=(conn, i)).start()

# Chạy server trong một thread riêng để không block giao diện đồ họa
threading.Thread(target=accept_connections, daemon=True).start()

update_log(f"Server listening on {host}:{port}")

connections = []

window.mainloop()
