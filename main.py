import random
import undetected_chromedriver as uc
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
from secret import login, password

IMGCOUNTER = 0
DELAY = 10


def change_user_agent(driver):

    ua = UserAgent()
    options = uc.ChromeOptions()
    useragent = ua.random
    options.add_argument(f'user-agent={useragent}')
    return driver


def start_chrome():

    options = uc.ChromeOptions()
    profile = f"C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/User Data/Profile 2"
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

    accept_all()


def emulate_human_response():

    time.sleep(random.randint(1, 3))


def click_image(image_path):

    image_path = 'images/' + image_path
    timeout = 10
    x = 0
    while (
            pyautogui.locateCenterOnScreen(
                image_path) is None and x < timeout):
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

    try:
        WebDriverWait(driver, DELAY).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="messageList"]/a')))
        emulate_human_response()
        chats = driver.find_elements(
            By.XPATH, '//div[@class="messageList"]/a')
        links = []
        for chat in chats:
            links.append(chat.get_attribute('href'))
        join_chat(driver, links)
    except:
        print('Чатов нет')


def join_chat(driver, links):

    for link in links:
        driver.get(link)
        WebDriverWait(driver, DELAY).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="log"]/div/button')))
        his_msgs = driver.find_elements(
            By.XPATH, '//div[@role="log"]/div/button')

        if his_msgs:
            # message = his_msgs[-1].find_element(
            #     By.XPATH, '../div/div/span').text
            message = his_msgs[-1].find_element(
                By.XPATH, '//span[@class="text D(ib) Va(t)"]').text
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

    emulate_human_response()


def check_couples(driver):

    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//div[@role="tabpanel"]')))
    couple_class = 'Bgc($c-ds-background-primary) recCard__img StretchedBox Bdrs(4px) Ov(h) H(100%) Pos(r)'

    couples_list = driver.find_elements(By.XPATH, f'//div[@class="{couple_class}"]')

    if len(couples_list) != 0:
        for i in range(len(couples_list)):
            driver.find_element(By.XPATH, f'//div[@class="{couple_class}"]').click()

            send_msg(driver, 'Привет')
            click_image('couples_button.png')
            emulate_human_response()
    else:
        print('Пар нет')


def download_img(driver):

    global IMGCOUNTER

    img_class = "Bdrs(8px) Bgz(cv) Bgp(c) StretchedBox"
    # person_name_class = "Fz($xl) Fw($bold)"

    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="{img_class}"]')))

    image = driver.find_element(
        By.XPATH, f'//div[@class="{img_class}"]')

    # person_name = driver.find_element(By.XPATH, f'//span[@class="{person_name_class}"]').text

    img_data = requests.get(image.value_of_css_property(
            "background-image")[5:-2]).content
    person_face_name = 'person_avatars/' + f'person_face_{IMGCOUNTER}.jpg'
    with open(person_face_name, 'wb') as handler:
        handler.write(img_data)

    print('download_img')

    IMGCOUNTER += 1

    return person_face_name


def delete_img():

    os.remove("image_name.jpg")


def get_score(driver):

    score = get_beauty_score(download_img(driver))
    return score


def match_accept(driver):

    try:
        send_msg(driver, 'Привет')
    except:
        print('No matches!')


def do_likes(driver):

    score = get_score(driver)
    print(float(score))

    if float(score) >= 2.9:
        click_image('like.png')
    else:
        click_image('dislike.png')

    print('do_likes')

    # match_accept()

    # try:
    #     # wait = WebDriverWait(driver, 1).until(
    #     #     EC.presence_of_element_located((By.XPATH, '//*[@id="q-2130158254"]/main/div/div[3]')))
    #     no_likes = driver.find_element(By.XPATH, '//*[@id="q-2130158254"]/main/div/div[3]')
    #
    #     if no_likes:
    #         click_image('no, thanks.png')
    #         click_image('dislike.png')
    # except:
    #     print('---')


def log_in_check(driver):

    time.sleep(0.5)
    site = driver.current_url
    if site == 'https://tinder.com/':
        log_in(driver, login, password)
        print('login')
    else:
        print('Вы уже авторизованы!')


def start_bot():
    # Start our tinder bot.

    driver = start_chrome()
    driver = change_user_agent(driver)
    driver.get("https://tinder.com/")
    driver.maximize_window()
    log_in_check(driver)

    return driver


def main():
    driver = start_bot()

    while True:
        # do_likes(driver)
        # check_couples(driver)
        collect_chats(driver)


if __name__ == "__main__":
    main()
