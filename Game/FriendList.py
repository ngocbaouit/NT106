import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")

# Connect to the database
connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)

def go_back(window, main_app, id):
    window.withdraw()
    main_app.deiconify()
    
def friend_list(id):
    # Create a new window
    window = tk.Tk()
    window.title("Danh sách bạn bè")
    window.geometry("700x380")  # Set window size

    # Nạp ảnh nền
    bg_image = Image.open("./assets/image_1.png")
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    window.bg_photo = bg_photo
    # Tạo canvas và thêm ảnh nền
    canvas = tk.Canvas(window, width=700, height=380)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Tạo frame và đặt vào canvas
    frame = ttk.Frame(canvas)
    canvas.create_window(350, 190, window=frame, anchor="center")  # Center the frame

    # Back button
    # back_btn = tk.Button(window, text='Quay lại', command=lambda: go_back(window, main_app, id), width=120, height=30,
    #                     hover_color='#FF7B81', bg_color='transparent', corner_radius=10)
    # back_btn.place(x=10, y=20)

    # Create a Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=40, fieldbackground="#D3D3D3")
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
    style.map("Treeview", background=[('selected', '#347083')])

    tree = ttk.Treeview(frame, columns=("Friend",), show="headings", height=6)
    tree.heading("Friend", text="Bạn bè")
    tree.column("Friend", anchor=tk.CENTER, width=650)

    # Thêm scrollbar vào Treeview
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(expand=True, fill=tk.BOTH)

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id_user1 FROM friends WHERE id_user2 = %s", [id])
        requests = cursor.fetchall()

        if requests:  # Check if the list is not empty
            request_id = requests[0][0]
            cursor.execute("SELECT Tên_người_dùng FROM users WHERE id_user = %s", [request_id])
            rows = cursor.fetchall()
            
            for row in rows:
                tree.insert("", tk.END, values=row)
        else:
            print("No friends found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    window.resizable(False, False)
    window.mainloop()
    