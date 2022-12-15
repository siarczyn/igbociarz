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
from unfollow import full_unfollow
from selenium.webdriver.support.ui import (
    WebDriverWait, )
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random


class insta_bot:
    """bot instance for scraping"""

    def load_config(self):
        with open(r"D:\projects\IGBOT\igbociarz\src\app\config.json") as file:

            settings = json.load(file)
        return settings

    def determine_format(self, bot):

        if (bot.find_element(By.XPATH, "//video")):
            print("video")
            print()
            bot.find_element(By.XPATH,
                             "//svg*[@aria-label='Dalej']")[0].click()
        if (bot.find_element(By.XPATH, "//svg*[@aria-label='Dalej']").length >
                1):
            print(bot.find_element(By.XPATH, "//svg*[@aria-label='Dalej']"))
            print(
                bot.find_element(By.XPATH,
                                 "//svg*[@aria-label='Dalej']")[1].click())
            print("zdjecia")
        else:
            print(
                bot.find_element(By.XPATH,
                                 "//svg*[@aria-label='Dalej']").click())
            print("zdjecie")

    def change_photo(self, bot):
        self.determine_format(bot)

    def perform_like(self, bot):
        #//*[@id="mount_0_0_5k"]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[3]/div/div/section[1]/span[1]/button/div[1]/svg
        #    photo = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/time") wersja chwilowo nie dziala
        # //*[local-name()='svg' and @data-icon='home']/*[local-name()='path']
        # /html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[3]/div/div/section[1]/span[1]/button/div[1]/svg
        #    photo1 = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/div/time") chwilowo nie dziala
        print("wejscie")
        print("wejscie")

        # wait.until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH, "//svg*[@aria-label='Lubię to!']")))[0]
        print("wejscie")
        self.small_wait()
        self.small_wait()

        photo = bot.find_element(
            By.XPATH, "//*[local-name()='svg' and @aria-label='Lubię to!']")
        self.small_wait()
        self.small_wait()

        print(photo)
        print(photo.get_attribute())
        print(photo.get_property())

        photo1 = photo.find_element(By.XPATH, '..')
        self.small_wait()

        photo2 = photo1.find_element(By.XPATH, '..')
        self.small_wait()
        print(photo.get_attribute())
        print(photo.get_property())

        print(photo1.get_attribute())
        print(photo1.get_property())

        print(photo2.get_attribute())
        print(photo2.get_property())
        action = ActionChains(bot)
        action.move_to_element(photo1)
        print("like")
        action.click()
        action.perform()

    def perform_follow(self, bot):
        # buttons = bot.find_elements_by_tag_name("button")
        # buttons[2].click()
        headers_2 = bot.find_elements_by_tag_name("h2")
        #    button = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button") wersja nie dziala
        # try:
        print("trying follow")
        button = bot.find_element(By.XPATH, "//*[contains(text(),'Obserwuj')")

        button.click()
        print("followed succesfully")

        # followbutton = bot.find_elements_by_xpath("//*[contains(text(), 'Follow')]")
        # followbutton.click()

    def small_wait(self):
        return random.randint(1, 10)

    def input_text(self, element, text):
        chars = list(text)
        for char in chars:
            sleep(random.random())
            element.send_keys(char)

    def go_to_photos(self, bot):
        # try:
        print("myslisz jeszcze?")
        # wait = WebDriverWait(bot, 60)
        # print("To")
        # target = wait.until(
        #     EC.presence_of_all_elements_located(
        #         (By.XPATH, "//*[contains(text(),'Najnowsze'")))[0]
        print("moze to?")
        target = bot.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/h2"
        )
        print(target)
        bot.execute_script("arguments[0].scrollIntoView();", target)
        print("pierwsza proba")
        actions = ActionChains(bot)
        actions.move_to_element_with_offset(target, 25, 100)
        actions.click()
        actions.perform()
        print("pierwsza done")

    def get_content(self, bot, settings):
        searchbox = bot.find_element(
            By.XPATH, "//input[@aria-label='Pole wejściowe wyszukiwania']")
        self.input_text(searchbox, '#' + settings["hashtag"])
        sleep(10)
        actions = ActionChains(bot)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        sleep(6)
        print("go to photos")
        self.go_to_photos(bot)

    def login(self, bot, settings):
        """function to enable cookies and login into account"""
        sleep(self.small_wait())
        bot.add_cookie(
{'domain': '.instagram.com', 'expiry': 1705682269, 'httpOnly': True, 'name': 'ig_did', 'path': '/', 'secure': True, 'value': '89273B4D-5CAD-4702-8629-EAD5BB229414'}

        )
        bot.add_cookie(

{'domain': '.instagram.com', 'expiry': 1705682269, 'httpOnly': False, 'name': 'mid', 'path': '/', 'secure': True, 'value': 'Y5tNXQALAAFqPw3mfZVl1O31E-_e'}

        )
        bot.add_cookie(

{'domain': '.instagram.com', 'expiry': 1702571896, 'httpOnly': False, 'name': 'csrftoken', 'path': '/', 'secure': True, 'value': 'nNtcYeGSsuJDBoEQfLOfVkmE7wGGwx06'}
        )
        cookies = bot.get_cookies()
        for cookie in cookies:
            print(cookie)
        
        bot.get("https://www.instagram.com/explore/tags/konie/")
        # sleep(120)
        wait = WebDriverWait(bot, 60)
        wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'
            )))[0].click()
        sleep(self.small_wait())

        wait.until(EC.presence_of_all_elements_located(
            (By.NAME, 'username')))[0]
        self.input_text(bot.find_element(By.NAME, 'username'),
                        settings["username"])
        self.input_text(bot.find_element(By.NAME, 'password'),
                        settings["password"])
        wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@type='submit']")))[0].click()
        print("login successful")
        cookies = bot.get_cookies()
        for cookie in cookies:
            print(cookie)
        bot.quit()
        sleep(3)
        driver = webdriver.Chrome()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.instagram.com/")

    def bot(self, bot):
        settings = self.load_config()
        # bot.get("https://www.instagram.com/")
        self.login(bot, settings)
        sleep(self.small_wait())
        # sleep(30)

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
        # Refrsh loop
        # full_unfollow(bot,15)
        while True:
            # Loop counters
            photo_interactions = 0
            # Go to hashtag & newest photo
            sleep(5)
            self.get_content(bot, settings)

            sleep(5)
            # photo count loop
            print("while")
            while photo_interactions <= 12:
                print("while")

                decision = randrange(100)
                if decision < settings["chance_of_like"]:
                    try:
                        sleep(1)
                        self.perform_like(bot)
                        print("like")
                    except:
                        print("failed like")
                        sleep(50)
                        self.get_content(bot, settings)
                        photo_interactions -= 1
                elif (decision >= settings["chance_of_like"]
                      and decision < settings["chance_of_like"] +
                      settings["chance_of_follow"]):
                    try:
                        self.perform_follow(bot)
                        print("followed")
                    except:
                        print("failed follow")
                        self.get_content(bot, settings)
                        photo_interactions -= 1
                else:
                    pass
                photo_interactions += 1
                sleep(5)
                self.change_photo(bot)
                sleep(settings["time_interval"])

    def run(self):
        options = Options()
        options.headless = True
        # service = Service(
        #     r'D:\projects\IGBOT\igbociarz\src\app\chromedriver.exe')

        # print(service)
        driver = webdriver.Chrome()
        # driver.delete_all_cookies()
        # driver = webdriver.Firefox(r"C:\Users\Siarczyn\Desktop\bot\files\geckodriver.exe")
        print("gownodupa")
        try:
            self.bot(driver)

        except:
            sleep(30)
            # driver.close()
            sleep(30)
            # self.run()


bociarz = insta_bot()
bociarz.run()
