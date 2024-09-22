from customtkinter import *
from PIL import Image, ImageTk
def show_invitation_notification(title, message):
    root = CTk()
    root.title(title)
    root.geometry("850x500")  # Đặt kích thước cửa sổ là 850x500
    root.resizable(False, False)  # Khóa cửa sổ lại để ngăn người dùng thay đổi kích thước

    # Tạo và hiển thị hình ảnh nền
    background_image = CTkImage(dark_image=Image.open("./Notification/notification.png"), size=(850, 500))
    background_label = CTkLabel(root, image=background_image, text="")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Đặt hình ảnh nền để lấp đầy toàn bộ cửa sổ

    frame = CTkFrame(root)
    frame.pack(padx=10, pady=10)

    label = CTkLabel(frame, text=message, font=("Helvetica", 12))
    label.pack(padx=10, pady=10)

    button_ok = CTkButton(frame, text="OK", command=root.destroy)
    button_ok.pack(pady=10)

    # Tạo nút "Quay lại" và đặt nó ở phía trên cùng bên trái của cửa sổ
    button_back = CTkButton(root, text="Quay lại", command=root.destroy, width=70, height=30)
    button_back.place(x=10, y=10)  # Đặt nút ở vị trí (10, 10) trên cửa sổ chính

    root.mainloop()

# Sử dụng giao diện
show_invitation_notification("Lời mời tham gia trận đấu", "Bạn đã nhận được lời mời tham gia trận đấu của PongPong123")
