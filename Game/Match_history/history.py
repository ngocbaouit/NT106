import mysql.connector
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

db_config = {
    'user': 'root',
    'password': '07042004',
    'host': 'localhost',
    'database': 'pong',
}

def fetch_matches(user_id):
    matches = []
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        query = ("""
            SELECT m.ID_trận, 
                   CASE 
                     WHEN m.ID_user1 = %s THEN m.ID_user2 
                     ELSE m.ID_user1 
                   END AS ID_đối_thủ,
                   CASE 
                     WHEN m.ID_user1 = %s THEN u2.Tên_người_dùng 
                     ELSE u1.Tên_người_dùng 
                   END AS Tên_đối_thủ,
                   CASE 
                     WHEN m.ID_user1 = %s THEN m.Điểm_user1 
                     ELSE m.Điểm_user2 
                   END AS Điểm_của_bạn,
                   CASE 
                     WHEN m.ID_user1 = %s THEN m.Điểm_user2 
                     ELSE m.Điểm_user1 
                   END AS Điểm_đối_thủ,
                   m.Thời_gian
            FROM matches m
            JOIN users u1 ON m.ID_user1 = u1.ID_user
            JOIN users u2 ON m.ID_user2 = u2.ID_user
            WHERE m.ID_user1 = %s OR m.ID_user2 = %s
        """)
        cursor.execute(query, (user_id, user_id, user_id, user_id, user_id, user_id))
        
        for (ID_trận, ID_đối_thủ, Tên_đối_thủ, Điểm_của_bạn, Điểm_đối_thủ, Thời_gian) in cursor:
            result = "Thắng" if Điểm_của_bạn > Điểm_đối_thủ else "Thua" if Điểm_của_bạn < Điểm_đối_thủ else "Hòa"
            matches.append((ID_đối_thủ, Tên_đối_thủ, result, Thời_gian))
        
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return matches


def create_gui(root, fetch_matches, user_id):
    root.title("Lịch sử đấu của trò chơi")
    root.geometry("800x600")
    root.resizable(False, False)

    # Nạp ảnh nền
    bg_image = Image.open("img/htsbg.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Tạo canvas và thêm ảnh nền
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.image = bg_photo  # Giữ tham chiếu đến ảnh để tránh bị garbage collected
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Tạo frame và đặt vào canvas
    frame = ttk.Frame(canvas)
    frame.pack(pady=20)
    canvas.create_window(400, 300, window=frame)

    # Nút quay lại
    back_button = ttk.Button(canvas, text="Quay lại")
    canvas.create_window(400, 20, window=back_button)

    # Cấu hình Treeview
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=40, fieldbackground="#D3D3D3")
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
    style.map("Treeview", background=[('selected', '#347083')])

    tree = ttk.Treeview(frame, columns=("Tên đối thủ", "Kết quả", "Ngày"), show="headings")
    tree.heading("Tên đối thủ", text="Tên đối thủ")
    tree.heading("Kết quả", text="Kết quả")
    tree.heading("Ngày", text="Thời gian")
    tree.column("Tên đối thủ", anchor=tk.CENTER, width=250)
    tree.column("Kết quả", anchor=tk.CENTER, width=150)
    tree.column("Ngày", anchor=tk.CENTER, width=200)

    # Thêm scrollbar vào Treeview
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(expand=True, fill=tk.BOTH)

    # Lấy dữ liệu từ cơ sở dữ liệu và điền vào Treeview
    matches = fetch_matches(user_id)
    populate_tree(tree, matches)

def populate_tree(tree, matches):
    for match in matches:
        tree.insert("", "end", text=match[0], values=match[1:])

def main():
    root = tk.Tk()
    current_user_id = 1  # Replace with the actual user ID
    create_gui(root, fetch_matches, current_user_id)
    root.mainloop()

if __name__ == "__main__":
    main()
