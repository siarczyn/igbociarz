import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import datetime as dt
from random import randrange
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import (
    WebDriverWait, )
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random



def load_config():
    with open(r"D:\projects\IGBOT\igbociarz\src\app\config.json") as file:
        settings = json.load(file)
    return settings
def determine_format(bot):
    #photos
    try:
        next1 = bot.find_element(
            By.XPATH, "//*[local-name()='svg' and @aria-label='Dalej']")
        next2 = next1.find_element(By.XPATH, '..')
        next3 = next2.find_element(By.XPATH, '..')
        next4 = next3.find_element(By.XPATH, '..')

        next4.click()
    except:
        pass
    # if (bot.find_element(By.XPATH, "//video")):
    #     print("video")
    #     bot.find_element(
    #         By.XPATH,
    #         "//*[local-name()='svg' and @aria-label='Dalej']")[0].click()
    # if (bot.find_element(
    #         By.XPATH,
    #         "//*[local-name()='svg' and @aria-label='Dalej']]").length > 1):
    #     print(
    #         bot.find_element(
    #             By.XPATH, "//*[local-name()='svg' and @aria-label='Dalej']"))
    #     print(
    #         bot.find_element(By.XPATH,
    #                          "//svg*[@aria-label='Dalej']")[1].click())
    #     print("zdjecia")
    # else:
    #     print(
    #         bot.find_element(By.XPATH,
    #                          "//svg*[@aria-label='Dalej']"))
    #     next = bot.find_element(By.XPATH, "//svg*[@aria-label='Dalej']")
    #     next1 = next.find_element(By.XPATH, '..')
    #     next2 = next1.find_element(By.XPATH, '..')
    #     next2.click()
    #     print("zdjecie")
def change_photo( bot):
    determine_format(bot)
def perform_like( bot):
    small_wait()
    small_wait()
    photo = bot.find_element(
        By.XPATH, "//*[local-name()='svg' and @aria-label='Lubię to!']")
    small_wait()
    small_wait()
    print(photo)

    photo1 = photo.find_element(By.XPATH, '..')
    small_wait()
    photo2 = photo1.find_element(By.XPATH, '..')
    small_wait()


    action = ActionChains(bot)
    action.move_to_element(photo2)
    print("like")
    action.click()
    action.perform()
def perform_follow(bot):
    headers_2 = bot.find_elements_by_tag_name("h2")
    # try:
    print("trying follow")
    button = bot.find_element(By.XPATH, "//*[contains(text(),'Obserwuj')")
    button.click()
    print("followed succesfully")

def small_wait():
    return random.randint(1, 10)
def input_text( element, text):
    chars = list(text)
    for char in chars:
        sleep(random.random())
        element.send_keys(char)
def go_to_photos( bot):
    # try:
    target = bot.find_element(
        By.XPATH,
        "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/h2"
    )
    print(target)
    bot.execute_script("arguments[0].scrollIntoView();", target)
    actions = ActionChains(bot)
    actions.move_to_element_with_offset(target, 25, 100)
    actions.click()
    actions.perform()
def get_content( bot, settings):
    searchbox = bot.find_element(
        By.XPATH, "//input[@aria-label='Pole wejściowe wyszukiwania']")
    input_text(searchbox, '#' + settings["hashtag"])
    sleep(10)
    actions = ActionChains(bot)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    sleep(6)
    print("go to photos")
    go_to_photos(bot)

def login( bot, settings):
    """function to enable cookies and login into account"""
    sleep(small_wait())
    wait = WebDriverWait(bot, 60)
    wait.until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'
        )))[0].click()
    sleep(small_wait())
    wait.until(EC.presence_of_all_elements_located(
        (By.NAME, 'username')))[0]
    input_text(bot.find_element(By.NAME, 'username'),
                    settings["username"])
    input_text(bot.find_element(By.NAME, 'password'),
                    settings["password"])
    wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//button[@type='submit']")))[0].click()
    print("login successful")
    sleep(10)
    # login popup:
    try:
        bot.find_element(By.XPATH,
                         "//section/main/div/div/div/div/button").click()
        print("login popup")
    except:
        print("failed l")
        pass
    sleep(2)
    print("login popup")
    #notification popup
    try:
        bot.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
        ).click()
        print("notification popup")
    except:
        print("failed n")
        pass
    print("notification popup")
    sleep(2)



def bot( bot):
    settings = load_config()
    bot.get("https://www.instagram.com/")
    login(bot, settings)
    sleep(small_wait())

    # Refrsh loop
    # full_unfollow(bot,15)
    while True:
        # Loop counters
        photo_interactions = 0
        # Go to hashtag & newest photo
        sleep(5)
        get_content(bot, settings)
        sleep(5)
        # photo count loop
        print("while")
        while photo_interactions <= 12:
            print("while")
            decision = randrange(100)
            if decision < settings["chance_of_like"]:
                try:
                    sleep(1)
                    perform_like(bot)
                    print("like")
                except:
                    print("failed like")
                    sleep(50)
                    get_content(bot, settings)
                    photo_interactions -= 1
            elif (decision >= settings["chance_of_like"]
                  and decision < settings["chance_of_like"] +
                  settings["chance_of_follow"]):
                try:
                    perform_follow(bot)
                    print("followed")
                except:
                    print("failed follow")
                    get_content(bot, settings)
                    photo_interactions -= 1
            else:
                pass
            photo_interactions += 1
            sleep(5)
            change_photo(bot)
            sleep(settings["time_interval"])
def run():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    # driver.delete_all_cookies()
    # driver = webdriver.Firefox(r"C:\Users\Siarczyn\Desktop\bot\files\geckodriver.exe")
    print("gownodupa")
    try:
        bot(driver)
    except:
        sleep(30)
        # driver.close()
        sleep(30)
        # run()



run()
