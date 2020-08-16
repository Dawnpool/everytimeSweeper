import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

"""
Headless Option
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=op)
"""

# Get ready for chrome web driver and set time for lenient waiting.
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(3)


def login(userid, pw):
    """Try login on browser."""
    driver.get("https://everytime.kr")
    driver.find_element_by_class_name('login').click()
    userid_entry = driver.find_element_by_name('userid')
    password_entry = driver.find_element_by_name('password')
    userid_entry.send_keys(userid)
    password_entry.send_keys(pw)
    userid_entry.submit()
    time.sleep(1)
    try:
        alert = driver.switch_to_alert()
        alert.accept()
        return False
    except:
        return True


def get_posts(posts, for_comment=False):
    """Collect my posts."""
    if for_comment:
        driver.get("https://everytime.kr/mycommentarticle")
    else:
        driver.get("https://everytime.kr/myarticle")
    time.sleep(3.5)
    try:
        driver.find_element_by_css_selector('#sheet .close').click()
    except NoSuchElementException:
        pass
    while True:
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find('div', class_='articles').find_all(
            'a', class_='article')
        for article in articles:
            href = article['href']
            posts.append(href)
        try:
            next_button = driver.find_element_by_css_selector(
                '.pagination .next')
            next_button.click()
        except NoSuchElementException:
            break


def click_delete(delete_button):
    """Click delete button"""
    delete_button.click()
    alert = driver.switch_to_alert()
    alert.accept()


def delete_posts(posts, except_hot):
    """Delete my posts depending on user's hot posts exception checkbox."""
    while posts:
        driver.get("https://everytime.kr" + posts.pop())
        delete_button = driver.find_element_by_class_name('del')
        likes_status = driver.find_element_by_css_selector('[title~="공감"]')
        likes = int(likes_status.get_attribute('innerText'))
        if except_hot:
            if likes < 10:
                click_delete(delete_button)
        else:
            click_delete(delete_button)
        time.sleep(1)


def count_comments(posts, comments):
    for post in posts:
        driver.get("https://everytime.kr" + post)
        delete_buttons = driver.find_elements_by_css_selector(
            ".comments .status .del")
        comments[0] += len(delete_buttons)


def delete_comments(posts, comments):
    """Delete my comments for each post."""
    while posts:
        driver.get("https://everytime.kr" + posts.pop())
        delete_buttons = driver.find_elements_by_css_selector(
            ".comments .status .del")
        for button in delete_buttons:
            button.click()
            alert = driver.switch_to_alert()
            alert.accept()
            comments[0] -= 1
            time.sleep(1)
