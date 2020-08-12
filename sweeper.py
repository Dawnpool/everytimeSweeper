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

driver = webdriver.Chrome('./chromedriver.exe')


def login(id, pw):
    driver.get("https://everytime.kr")
    driver.find_element_by_class_name('login').click()
    userid = driver.find_element_by_name('userid')
    password = driver.find_element_by_name('password')
    userid.send_keys(id)
    password.send_keys(pw)
    userid.submit()
    time.sleep(1)
    try:
        alert = driver.switch_to_alert()
        alert.accept()
        return False
    except:
        return True


def get_posts(posts):
    driver.get("https://everytime.kr/myarticle")
    time.sleep(5)
    posts = []
    driver.find_element_by_css_selector('#sheet .close').click()
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
    return posts


def delete_posts(posts):
    for post in posts:
        driver.get("https://everytime.kr" + post)
