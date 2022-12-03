import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import requests
from attractive_net.AttractiveNet.test import get_beauty_score
import os
from chat_bot.answer import answer_questions


IMGCOUNTER = 0
DELAY = 30


def change_user_agent(driver):
    ua = UserAgent()
    options = uc.ChromeOptions()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    return driver


def start_chrome():
    options = uc.ChromeOptions()
    profile = "C:/Users/Nuralem/AppData/Local/Google/Chrome/User Data/Profile 1"
    options.add_argument(f'user-data-dir={profile}')
    driver = uc.Chrome(options=options)
    driver.implicitly_wait(60)
    driver.set_window_size(1920, 1080)
    return driver


def log_in(driver, email, password):
    content = '/html/body/div[1]'
    xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a'
    emulate_human_response()
    WebDriverWait(driver, DELAY).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()
    emulate_human_response()
    driver = change_user_agent(driver)
    xpath = '//*[@aria-label="Войти через Google"]'
    emulate_human_response()
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located(
        (By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()
    emulate_human_response()
    driver = change_user_agent(driver)
    driver.switch_to.window(driver.window_handles[1])

    xpath = "//input[@type='email']"
    WebDriverWait(driver, DELAY).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    emulate_human_response()
    emailfield = driver.find_element(By.XPATH, xpath)
    emailfield.send_keys(email)
    emulate_human_response()
    emailfield.send_keys(Keys.ENTER)
    emulate_human_response()
    xpath = "//input[@type='password']"
    WebDriverWait(driver, DELAY).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    driver = change_user_agent(driver)
    emulate_human_response()
    pwdfield = driver.find_element(By.XPATH, xpath)
    pwdfield.send_keys(password)
    emulate_human_response()
    pwdfield.send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[0])


def emulate_human_response():
    time.sleep(random.randint(1, 3))


def click_image(image_path):
    image_path = 'images/' + image_path
    timeout = 10
    x = 0
    while (
        pyautogui.locateCenterOnScreen(
            image_path) == None and x < timeout):
        time.sleep(0.5)
        x = x + 1
    pyautogui.click(pyautogui.locateCenterOnScreen(
        image_path, confidence=0.9))


def accept_all():
    click_image('allow_search.jpg')
    click_image('accept_conditions.jpg')
    click_image('turn_on_messages.jpg')
    click_image('block_notif.jpg')
    click_image('close_dark_theme.jpg')


def send_msg(driver, mgs):
    time.sleep(5)
    input_field = driver.find_element(
        By.XPATH, "//textarea")
    input_field.send_keys(mgs)
    driver.find_element(
        By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)


def collect_chats(driver):
    WebDriverWait(driver, DELAY).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="messageList"]/a')))
    time.sleep(3)
    chats = driver.find_elements(
        By.XPATH, '//div[@class="messageList"]/a')
    links = []
    for chat in chats:
        links.append(chat.get_attribute('href'))
    join_chat(driver, links)


def join_chat(driver, links):
    for link in links:
        driver.get(link)
        time.sleep(5)
        his_msgs = driver.find_elements(
            By.XPATH, '//div[@role="log"]/div/button')
        if (his_msgs):
            message = his_msgs[-1].find_element(
                By.XPATH, '../div/div/span').text
            try:
                with open(f"{link.split('/')[-1]}.txt", "r+") as f:
                    text = f.read()
                    if text.split(" ")[-2] != message:
                        f.write(message + " ")
                        print("новое сообщение от него:")
                        print(message)
                        q = answer_questions(message)
                        print(q)
                        send_msg(driver, q)
                    else:
                        print("Новых сообщений нет")
            except:
                with open(f"{link.split('/')[-1]}.txt", "w+") as f:
                    f.write(message + " ")
                    print("новое сообщение от него:")
                    print(message)
                    q = answer_questions(message)
                    print(q)
                    send_msg(driver, q)


def download_img(driver):
    global IMGCOUNTER
    imgs = driver.find_elements(
        By.XPATH, "//div[@role='img']")
    while (len(imgs) < 14):
        imgs = driver.find_elements(
            By.XPATH, "//div[@role='img']")
        time.sleep(0.5)

    if len(imgs) == 16:
        img_data = requests.get(imgs[4].value_of_css_property(
            "background-image")[5:-2]).content
        person_face_name = 'person_avatars/' + f'person_face{IMGCOUNTER}.jpg'
        with open(person_face_name, 'wb') as handler:
            handler.write(img_data)
        IMGCOUNTER = IMGCOUNTER + 1
        return person_face_name

    if len(imgs) == 15:
        img_data = requests.get(imgs[3].value_of_css_property(
            "background-image")[5:-2]).content
        person_face_name = 'person_avatars/' + f'person_face{IMGCOUNTER}.jpg'
        with open(person_face_name, 'wb') as handler:
            handler.write(img_data)
        IMGCOUNTER = IMGCOUNTER + 1
        return person_face_name


def delete_img():
    os.remove("image_name.jpg")


def get_score(driver):
    score = get_beauty_score(download_img(driver))
    return score


def match_accept():
    click_image("hurt.jpg")
    click_image("accept_hurt.jpg")


def do_likes(driver):
    score = get_score(driver)
    if (float(score) > 2.9):
        click_image('like.jpg')
    else:
        click_image('dislike.jpg')


def start_bot():
    # Start our tinder bot.
    driver = start_chrome()
    driver = change_user_agent(driver)
    driver.get("https://tinder.com/")
    driver.maximize_window()
    return driver


driver = start_bot()
# log_in(driver, "robotkz710@gmail.com", "secret")
# log_in(driver, "robotkz0091@gmail.com", "secret")

for i in range(10):
    do_likes(driver)

for i in range(10):
    collect_chats(driver)
