import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sweeper as swp
import threading
import time

# Initialize
root = tk.Tk()
root.title('Everytime Sweeper')
root.geometry('400x210')
root.resizable(False, False)
posts = []
commented_posts = []
comments = [0]

# Font setting
title_font = tkFont.Font(size=12, weight='bold', family='Ubuntu')
label_font = tkFont.Font(size=10, family='Ubuntu')


def update_commented_post():
    """Load commented posts."""
    swp.get_posts(commented_posts, for_comment=True)
    swp.count_comments(commented_posts, comments)


def update_mycomment_status(t1):
    """Update(rewrite) comment collection status on screen while collecting."""
    grids = root.grid_slaves()
    target_grid = grids[-3]
    loading_grid = grids[0]
    loading_grid['text'] = '내가 쓴 댓글 조회 중...'
    while t1.is_alive():
        target_grid['text'] = str(comments[0])
        time.sleep(0.1)
    target_grid['text'] = str(comments[0])
    loading_grid['text'] = '조회 완료'


def load_mycomment():
    """Load my comments."""
    commented_posts.clear()
    comments[0] = 0
    t1 = threading.Thread(target=update_commented_post)
    t2 = threading.Thread(target=update_mycomment_status, args=(t1,))
    t1.start()
    t2.start()


def update_mypost_status(t1):
    """Update(rewrite) post collection status on screen while collecting."""
    grids = root.grid_slaves()
    target_grid = grids[-2]
    loading_grid = grids[0]
    loading_grid['text'] = '내가 쓴 글 조회 중...'
    while t1.is_alive():
        target_grid['text'] = str(len(posts))
        time.sleep(0.1)
    target_grid['text'] = str(len(posts))
    loading_grid['text'] = '조회 완료'


def update_post_delete_status(t1, total_posts):
    """Update(rewrite) post deletion status on screen while deleting."""
    grids = root.grid_slaves()
    status_grid = grids[0]
    status_grid['text'] = '0/{total} 삭제 중'.format(total=total_posts)
    while t1.is_alive():
        status_grid['text'] = '{now}/{total} 삭제 중'.format(
            now=total_posts-len(posts), total=total_posts)
        time.sleep(0.1)
    status_grid['text'] = '{now}/{total} 삭제 완료'.format(
        now=total_posts-len(posts), total=total_posts)


def update_comment_delete_status(t1, total_comments):
    """Update(rewrite) comment deletion status on screen while deleting."""
    grids = root.grid_slaves()
    status_grid = grids[0]
    status_grid['text'] = '0/{total} 삭제 중'.format(total=total_comments)
    while t1.is_alive():
        status_grid['text'] = '{now}/{total} 삭제 중'.format(
            now=total_comments-comments[0], total=total_comments)
        time.sleep(0.1)
    status_grid['text'] = '{now}/{total} 삭제 완료'.format(
        now=total_comments-comments[0], total=total_comments)


def load_mypost():
    """
    Collect my posts.
    Threading is used for preventing gui from stopping.
    Shows collection status in real time.
    """
    posts.clear()
    t1 = threading.Thread(target=swp.get_posts, args=(posts,))
    t2 = threading.Thread(target=update_mypost_status, args=(t1,))
    t1.start()
    t2.start()


def delete_mypost(except_hot):
    """
    Delete my collected posts.
    Threading is used for preventing gui from stopping.
    Shows deletion status in real time.
    """
    total_posts = len(posts)
    t1 = threading.Thread(target=swp.delete_posts, args=(posts, except_hot))
    t2 = threading.Thread(target=update_post_delete_status,
                          args=(t1, total_posts))
    t1.start()
    t2.start()


def delete_mycomment():
    """
    Delete my comments from collected commented posts.
    Threading is used for preventing gui from stopping.
    Shows deletion status in real time.
    """
    total_comments = comments[0]
    t1 = threading.Thread(target=swp.delete_comments,
                          args=(commented_posts, comments))
    t2 = threading.Thread(
        target=update_comment_delete_status, args=(t1, total_comments))
    t1.start()
    t2.start()


def render_control_screen():
    """Render control screen which contains main functions."""
    root.unbind('<Return>')
    grids = root.grid_slaves()
    grids.pop()
    for grid in grids:
        grid.destroy()
    mypost_label = tk.Label(root, text="내가 쓴 글 수: ", font=label_font)
    mycomment_label = tk.Label(root, text="내가 쓴 댓글 수: ", font=label_font)
    mypost_number_label = tk.Label(root, text='', font=label_font)
    mycomment_number_label = tk.Label(root, text='', font=label_font)
    post_inq_button = tk.Button(
        root, text="내가 쓴 글 조회", command=load_mypost, font=label_font)
    comment_inq_button = tk.Button(
        root, text="내가 쓴 댓글 조회", command=load_mycomment, font=label_font)
    except_hot = tk.BooleanVar()
    except_hot.set(False)
    except_hot_checkbox = tk.Checkbutton(
        root, text="HOT 게시물 제외", var=except_hot)
    post_delete_button = tk.Button(
        root, text="내가 쓴 글 모두 삭제", command=lambda: delete_mypost(except_hot.get()), font=label_font)
    post_delete_warning = tk.Label(root, text="※글 조회 먼저")
    comment_delete_button = tk.Button(
        root, text="내가 쓴 댓글 모두 삭제", command=delete_mycomment, font=label_font)
    comment_delete_warning = tk.Label(root, text="※댓글 조회 먼저")
    loading_label = tk.Label(root, text='', font=label_font)

    mypost_number_label.grid(row=1, column=1, sticky='w')
    mycomment_number_label.grid(row=2, column=1, sticky='w')
    mypost_label.grid(row=1, column=0, pady=5)
    mycomment_label.grid(row=2, column=0)
    post_inq_button.grid(row=1, column=2)
    post_delete_button.grid(row=3, column=0, pady=(15, 5))
    post_delete_warning.grid(row=3, column=2, pady=(15, 5), sticky='w')
    except_hot_checkbox.grid(row=3, column=1, pady=(15, 5), sticky='w')
    comment_inq_button.grid(row=2, column=2)
    comment_delete_button.grid(row=4, column=0)
    comment_delete_warning.grid(row=4, column=1, sticky='w')
    loading_label.grid(row=5, column=1)


def attempt_login(userid, password):
    """
    Try login.
    Render the control screen if login successed,
    alert error message if login failed.
    """
    login_status = swp.login(userid, password)
    if login_status:
        render_control_screen()
    else:
        tk.messagebox.showerror('로그인 실패', '아이디와 비밀번호를 확인해주세요')


def render_first_screen():
    """Render first screen of GUI."""
    title = tk.Label(root, text="에브리타임 청소기", font=title_font)
    login_label = tk.Label(root, text="아이디:", font=label_font)
    login_entry = tk.Entry(root, font=label_font)
    password_label = tk.Label(root, text="비밀번호:", font=label_font)
    password_entry = tk.Entry(root, show='*', font=label_font)
    login_button = tk.Button(root, text='로그인', command=lambda: attempt_login(
        login_entry.get(), password_entry.get()), font=label_font)
    root.bind('<Return>', lambda event: login_button.invoke())

    title.grid(row=0, column=1, pady=20)
    login_label.grid(row=1, column=0, padx=(70, 10), pady=5)
    login_entry.grid(row=1, column=1, pady=5)
    password_label.grid(row=2, column=0, padx=(70, 10), pady=5)
    password_entry.grid(row=2, column=1, pady=5)
    login_button.grid(row=3, column=1, pady=(10, 0))


# Run
render_first_screen()
root.mainloop()
