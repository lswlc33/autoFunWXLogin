"""
这里写的是软件UI
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from next import make_login_qr, check_login, is_token_valid
import threading

login_qr_img = ""


def refresh_qr():
    global login_qr_img
    make_login_qr()
    login_qr_img = tk.PhotoImage(file="qr.gif")
    label.configure(image=login_qr_img)
    threading.Thread(target=check_login).start()


def check_token():
    # 登录成功提示框
    messagebox.showinfo("登录结果", is_token_valid())
    pass


app = tk.Tk()
app.title("方块兽二维码登录")
app.geometry("400x600")
app.resizable(False, False)


# 标题
label = tk.Label(app, text="方块兽二维码登录", font=("微软雅黑", 20))
label.pack(pady=15)

# 多页框架
notebook = tk.ttk.Notebook(app)
notebook.pack(fill="both", expand=True)

# 第一页
frame1 = tk.Frame(notebook, width=400, height=300)


label = tk.Label(frame1, image="", text="点击加载二维码", cursor="hand2")
label.pack(pady=15)
label.bind("<Button-1>", lambda event: refresh_qr())

label2 = tk.Label(
    frame1, text="请使用微信扫描二维码登录, 点击图片可刷新二维码", font=("微软雅黑", 12)
)
label2.pack(pady=10)

button = tk.Button(frame1, text="登录测试", command=check_token)
button.pack(pady=20)

frame1.pack(fill="both", expand=True)
notebook.add(frame1, text="身份认证")

# 第二页
frame2 = tk.Frame(notebook, width=400, height=300)
frame2.pack(fill="both", expand=True)
label3 = tk.Label(
    frame2,
    text="手机确认登录后\ntoken会自动保存在token.txt中\n并自动复制到剪贴板\n（如果你自信每次都是登录成功的\n可以跳过登录测试）",
    font=("微软雅黑", 15),
)
label3.pack(pady=15)
notebook.add(frame2, text="说明")

app.mainloop()
