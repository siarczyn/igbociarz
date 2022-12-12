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

    def arrow_right(self, bot):
        actions = ActionChains(bot)
        actions.send_keys(Keys.ARROW_RIGHT)
        # new=bot.find_element_by_xpath("/html/body/div[6]/div[1]/div/div/div[2]/button")
        # new.click()
        actions.perform()

    def perform_like(self, bot):
        #    photo = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/time") wersja chwilowo nie dziala
        #    photo1 = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/div/time") chwilowo nie dziala
        photo = bot.find_element_by_xpath(
            "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/div/a/div/time"
        )
        action = webdriver.common.action_chains.ActionChains(bot)
        action.move_to_element_with_offset(photo, -50, -50)
        print("like")
        action.click()
        action.click()
        action.perform()

    def perform_follow(self, bot):
        # buttons = bot.find_elements_by_tag_name("button")
        # buttons[2].click()
        headers_2 = bot.find_elements_by_tag_name("h2")
        #    button = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button") wersja nie dziala
        button = bot.find_element_by_xpath(
            "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div"
        )

        button.click()
        # followbutton = bot.find_elements_by_xpath("//*[contains(text(), 'Follow')]")
        # followbutton.click()
        print("jjj")
        line = "https://www.instagram.com/" + str(headers_2[2].text) + "/"
        file = open("files/to_follow.txt", "a+")
        file.write(str(line) + "," + str(datetime.now()) + "\n")
        file.close()

    def unfollow_user(self, bot, href):
        sleep(15)
        bot.get(href)
        sleep(10)
        following = bot.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"
        )
        following.click()
        sleep(5)
        confirmFollow = bot.find_element_by_xpath(
            "/html/body/div[6]/div/div/div/div[3]/button[1]")
        confirmFollow.click()

    def small_wait(self):
        return random.randint(1, 10)

    def get_to_unfollow(self):
        current_date = datetime.now()
        follow_list = []
        unfollow_list = []
        failed = []
        file = open("files/to_follow.txt", "r")
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(",")
            if (datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S.%f") +
                    dt.timedelta(days=2) < current_date):
                unfollow_list.append([
                    datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S.%f"), data[0]
                ])
            else:
                follow_list.append([
                    datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S.%f"), data[0]
                ])
        file.close()
        file = open("files/to_follow.txt", "w")
        for line in follow_list:
            file.write(str(line[1]) + "," + str(line[0]) + "\n")
        file.close()
        for user in unfollow_list:
            try:
                self.unfollow_user(bot, user[1])
            except:
                failed.append(user)
        file = open("files/failed_unfollows.txt", "a+")
        for line in failed:
            print(str(line[1]) + "," + str(line[0]) + "\n")
        file.close()

    def getcontent(self, bot, settings):
        bot.get("https://www.instagram.com/explore/tags/" +
                settings["hashtag"] + "/")
        sleep(6)
        try:
            target = bot.find_element_by_xpath(
                "/html/body/div[1]/section/main/article/h2")
            bot.execute_script("arguments[0].scrollIntoView();", target)
            sleep(5)
            actions = ActionChains(bot)
            sleep(5)
            actions.move_to_element_with_offset(target, 0, +150)
            actions.click()
            sleep(5)
            actions.perform()
        except:
            sleep(5)
            try:
                target = bot.find_element_by_xpath(
                    "/html/body/div[1]/section/main/article/h2")
                bot.execute_script("arguments[0].scrollIntoView();", target)
                sleep(3)
                actions = ActionChains(bot)
                sleep(2)

                actions.move_to_element_with_offset(target, 0, +150)
                actions.click()
                sleep(2)
                actions.perform()
            except:
                bot(bot)

    def login(self, bot, setting):
        """function to enable cookies and login into account"""
        sleep(self.small_wait())

        wait = WebDriverWait(bot, 60)
        wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'
            )))[0].click()
        sleep(self.small_wait())

        # Login
        wait.until(EC.presence_of_all_elements_located(
            (By.NAME, 'username')))[0].send_keys(settings["username"])
        sleep(self.small_wait())

        wait.until(EC.presence_of_all_elements_located(
            (By.NAME, 'password')))[0].send_keys(settings["password"])
        sleep(self.small_wait())
        wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//button[@type='submit']")))[0].click()
        print("login successful")

    def bot(self, bot):
        settings = self.load_config()
        bot.get("https://www.instagram.com/")
        self.login(bot, settings)
        sleep(self.small_wait())

        try:
            login_popup = bot.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div/div/div/button")
            login_popup.click()
        except:
            pass
        sleep(2)
        try:
            notification_popup = bot.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[3]/button[2]")
            notification_popup.click()
        except:
            pass
        sleep(2)
        # Refrsh loop

        # full_unfollow(bot,15)
        while True:
            # Loop counters
            photo_interactions = 0
            # Go to hashtag & newest photo
            sleep(5)

            self.getcontent(bot, settings)

            sleep(5)
            # photo count loop
            while photo_interactions <= 12:
                decision = randrange(100)
                if decision < settings["chance_of_like"]:
                    try:
                        sleep(1)
                        self.perform_like(bot)
                        print("like")
                    except:
                        print("failed like")
                        self.getcontent(bot, settings)
                        photo_interactions -= 1
                elif (decision >= settings["chance_of_like"]
                      and decision < settings["chance_of_like"] +
                      settings["chance_of_follow"]):
                    try:
                        self.perform_follow(bot)
                        print("followed")
                    except:
                        print("failed follow")
                        self.getcontent(bot, settings)
                        photo_interactions -= 1
                else:
                    pass
                photo_interactions += 1
                sleep(5)
                self.arrow_right(bot)
                sleep(settings["time_interval"])

    def run(self):
        # options = Options()
        # options.headless = True
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
            driver.close()
            sleep(30)
            self.run()


bociarz = insta_bot()
bociarz.run()
