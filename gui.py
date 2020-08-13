import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sweeper as swp
from concurrent.futures import ThreadPoolExecutor
import threading
import time

root = tk.Tk()
root.title('Everytime Sweeper')
root.geometry('350x250')
root.resizable(False, False)
posts = []
comments = []


def update_mypost_number(t1):
    packs = root.pack_slaves()
    target_pack = packs[1]
    loading_pack = packs[-1]
    loading_pack['text'] = '조회 중...'
    while t1.is_alive():
        target_pack['text'] = '내가 쓴 글 수: ' + str(len(posts))
        time.sleep(0.1)
    target_pack['text'] = '내가 쓴 글 수: ' + str(len(posts))
    loading_pack['text'] = '조회 완료'


def update_delete_status(t1, total_posts):
    packs = root.pack_slaves()
    status_pack = packs[-1]
    status_pack['text'] = '0/{total} 삭제 중'.format(total=total_posts)
    while t1.is_alive():
        status_pack['text'] = '{now}/{total} 삭제 중'.format(
            now=total_posts-len(posts), total=total_posts)
        time.sleep(0.1)
    status_pack['text'] = '{now}/{total} 삭제 완료'.format(
        now=total_posts-len(posts), total=total_posts)


def update_mypost():
    posts.clear()
    t1 = threading.Thread(target=swp.get_posts, args=(posts,))
    t2 = threading.Thread(target=update_mypost_number, args=(t1,))
    t1.start()
    t2.start()


def delete_mypost(except_hot):
    total_posts = len(posts)
    t1 = threading.Thread(target=swp.delete_posts, args=(posts, except_hot))
    t2 = threading.Thread(target=update_delete_status, args=(t1, total_posts))
    t1.start()
    t2.start()


def switch_page():
    packs = root.pack_slaves()
    packs = packs[1:]
    for pack in packs:
        pack.destroy()
    mypost_label = tk.Label(root, text="내가 쓴 글 수: ")
    mycomment_label = tk.Label(root, text="댓글 단 글 수: ")
    post_inq_button = tk.Button(root, text="내가 쓴 글 조회", command=update_mypost)
    comment_inq_button = tk.Button(root, text="내가 쓴 댓글 조회")
    except_hot = tk.BooleanVar()
    except_hot.set(False)
    except_hot_checkbox = tk.Checkbutton(
        root, text="HOT 게시물 제외", var=except_hot)
    post_delete_button = tk.Button(
        root, text="내가 쓴 글 모두 삭제", command=lambda: delete_mypost(except_hot.get()))
    loading_label = tk.Label(root, text='')

    mypost_label.pack(pady=5)
    mycomment_label.pack(pady=5)
    post_inq_button.pack()
    post_delete_button.pack()
    comment_inq_button.pack()
    except_hot_checkbox.pack()
    loading_label.pack()


def attempt_login(userid, password):
    login_status = swp.login(userid, password)
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
