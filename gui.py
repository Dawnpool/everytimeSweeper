import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sweeper as swp
from concurrent.futures import ThreadPoolExecutor
import threading

root = tk.Tk()
root.title('Everytime Sweeper')
root.geometry('350x250')
root.resizable(False, False)
posts = []
comments = []


def update_mypost_number(t1):
    while t1.is_alive():
        root.pack_slaves()[1]['text'] = '내가 쓴 글 수: ' + str(len(posts))


def update_mypost():
    t1 = threading.Thread(target=swp.get_posts, args=(posts,))
    t2 = threading.Thread(target=update_mypost_number, args=(t1,))


def delete_mypost():
    swp.delete_posts(posts)


def switch_page():
    packs = root.pack_slaves()
    packs = packs[1:]
    for pack in packs:
        pack.destroy()
    mypost_label = tk.Label(root, text="내가 쓴 글 수: ")
    mycomment_label = tk.Label(root, text="댓글 단 글 수: ")
    post_inq_button = tk.Button(root, text="내가 쓴 글 조회", command=update_mypost)
    comment_inq_button = tk.Button(root, text="내가 쓴 댓글 조회")
    post_delete_button = tk.Button(
        root, text="내가 쓴 글 모두 삭제", command=delete_mypost)
    mypost_label.pack(pady=5)
    mycomment_label.pack(pady=5)
    post_inq_button.pack()
    post_delete_button.pack()
    comment_inq_button.pack()


def attempt_login(id, password):
    login_status = swp.login(id, password)
    if login_status:
        switch_page()
    else:
        tk.messagebox.showerror('로그인 실패', '아이디와 비밀번호를 확인해주세요')


def start_page():
    title_font = tkFont.Font(size=15)
    title = tk.Label(root, text="에브리타임 글 청소기", font=title_font)

    login_label = tk.Label(root, text="아이디",)
    login_entry = tk.Entry(root)
    password_label = tk.Label(root, text="비밀번호")
    password_entry = tk.Entry(root, show='*')
    login_button = tk.Button(root, text='로그인', command=lambda: attempt_login(
        login_entry.get(), password_entry.get()))

    title.pack(pady=20)
    login_label.pack()
    login_entry.pack()
    password_label.pack(pady=(10, 0))
    password_entry.pack()
    login_button.pack(pady=(10, 0))


start_page()
root.mainloop()
