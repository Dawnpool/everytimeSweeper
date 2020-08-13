import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sweeper as swp
from concurrent.futures import ThreadPoolExecutor
import threading
import time

root = tk.Tk()
root.title('Everytime Sweeper')
root.geometry('400x300')
root.resizable(False, False)
posts = []
comments = []


def update_mypost_number(t1):
    grids = root.grid_slaves()
    target_grid = grids[-2]
    loading_grid = grids[0]
    loading_grid['text'] = '조회 중...'
    while t1.is_alive():
        target_grid['text'] = '내가 쓴 글 수: ' + str(len(posts))
        time.sleep(0.1)
    target_grid['text'] = '내가 쓴 글 수: ' + str(len(posts))
    loading_grid['text'] = '조회 완료'


def update_delete_status(t1, total_posts):
    grids = root.grid_slaves()
    status_grid = grids[0]
    status_grid['text'] = '0/{total} 삭제 중'.format(total=total_posts)
    while t1.is_alive():
        status_grid['text'] = '{now}/{total} 삭제 중'.format(
            now=total_posts-len(posts), total=total_posts)
        time.sleep(0.1)
    status_grid['text'] = '{now}/{total} 삭제 완료'.format(
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
    grids = root.grid_slaves()
    grids.pop()
    for grid in grids:
        grid.destroy()
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

    mypost_label.grid(row=1, column=0)
    mycomment_label.grid(row=2, column=0)
    post_inq_button.grid(row=3, column=0)
    post_delete_button.grid(row=3, column=1)
    except_hot_checkbox.grid(row=3, column=2)
    comment_inq_button.grid(row=4, column=0)
    loading_label.grid(row=5)


def attempt_login(userid, password):
    login_status = swp.login(userid, password)
    if login_status:
        switch_page()
    else:
        tk.messagebox.showerror('로그인 실패', '아이디와 비밀번호를 확인해주세요')


def start_page():
    title_font = tkFont.Font(size=10)
    title = tk.Label(root, text="에브리타임 글 청소기", font=title_font)

    login_label = tk.Label(root, text="아이디:")
    login_entry = tk.Entry(root)
    password_label = tk.Label(root, text="비밀번호:")
    password_entry = tk.Entry(root, show='*')
    login_button = tk.Button(root, text='로그인', command=lambda: attempt_login(
        login_entry.get(), password_entry.get()))

    title.grid(row=0, column=1, pady=20)
    login_label.grid(row=1, column=0)
    login_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    login_button.grid(row=3)


start_page()
root.mainloop()
