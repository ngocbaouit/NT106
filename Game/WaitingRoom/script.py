import tkinter as tk
import threading
import subprocess

def start_server():
    threading.Thread(target=server_thread, daemon=True).start()

def start_client():
    threading.Thread(target=client_thread, daemon=True).start()

def server_thread():
    subprocess.run(['python', 'server.py'])

def client_thread():
    subprocess.run(['python', 'waiting.py'])

window = tk.Tk()
window.title("Controller")

server_button = tk.Button(window, text="Start Server", command=start_server)
server_button.pack(pady=20)

client_button = tk.Button(window, text="Start Client", command=start_client)
client_button.pack(pady=20)

window.mainloop()
