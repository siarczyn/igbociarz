import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import datetime as dt
from random import randrange
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from unfollow import full_unfollow

def load_config():
    with open('files/config.json') as file:

        settings = json.load(file)
    return settings


def arrow_right(bot):
    actions = ActionChains(bot)
    actions.send_keys(Keys.ARROW_RIGHT)
    # new=bot.find_element_by_xpath("/html/body/div[6]/div[1]/div/div/div[2]/button")
    # new.click()
    actions.perform()

def perform_like(bot):
#    photo = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/time") wersja chwilowo nie dziala
#    photo1 = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/a/div/time") chwilowo nie dziala
    photo =bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[2]/div/a/div/time")
    action = webdriver.common.action_chains.ActionChains(bot)
    action.move_to_element_with_offset(photo, -50, -50)
    print('like')
    action.click()
    action.click()
    action.perform()



def perform_follow(bot):
    # buttons = bot.find_elements_by_tag_name("button")
    # buttons[2].click()
    headers_2 = bot.find_elements_by_tag_name("h2")
#    button = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button") wersja nie dziala
    button = bot.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div")

    button.click()
    # followbutton = bot.find_elements_by_xpath("//*[contains(text(), 'Follow')]")
    # followbutton.click()
    print("jjj")
    line = "https://www.instagram.com/" + str(headers_2[2].text) + "/"
    file = open("files/to_follow.txt", 'a+')
    file.write(str(line) + "," + str(datetime.now()) + "\n")
    file.close()


def unfollow_user(bot, href):
    sleep(15)
    bot.get(href)
    sleep(10)
    following = bot.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
    following.click()
    sleep(5)
    confirmFollow = bot.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]")
    confirmFollow.click()


def get_to_unfollow():
    current_date = datetime.now()
    follow_list = []
    unfollow_list = []
    failed = []
    file = open("files/to_follow.txt", "r")
    lines = file.readlines()
    for line in lines:
        data = line.strip().split(',')
        if datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f') + dt.timedelta(days=2) < current_date:
            unfollow_list.append([datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f'), data[0]])
        else:
            follow_list.append([datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f'), data[0]])
    file.close()
    file = open("files/to_follow.txt", "w")
    for line in follow_list:
        file.write(str(line[1]) + "," + str(line[0]) + "\n")
    file.close()
    for user in unfollow_list:
        try:
            unfollow_user(bot, user[1])
        except:
            failed.append(user)
    file = open("files/failed_unfollows.txt", "a+")
    for line in failed:
        print(str(line[1]) + "," + str(line[0]) + "\n")
    file.close()

def getcontent(bot,settings):
    bot.get('https://www.instagram.com/explore/tags/' + settings['hashtag'] + '/')
    sleep(6)
    try:
        target = bot.find_element_by_xpath("/html/body/div[1]/section/main/article/h2")
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
            target = bot.find_element_by_xpath("/html/body/div[1]/section/main/article/h2")
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

def bot(bot):
    settings = load_config()
    sleep(2)
    bot.get('https://www.instagram.com/')
    sleep(2)
    accept_cookies = bot.find_element_by_xpath("/html/body/div[4]/div/div/button[1]")
    accept_cookies.click()
    sleep(4)
    #Login 

    username_input = bot.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input")
    username_input.click()
    username_input.send_keys(settings['username'])

    password_input = bot.find_element_by_xpath(
        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
    password_input.send_keys(settings['password'])

    login = bot.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
    login.click()
    print("login successful")
    sleep(6)
    #Ignore auto login and notification popups

    try:
        login_popup = bot.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        login_popup.click()
    except:
        pass
    sleep(2)
    try:
        notification_popup = bot.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")
        notification_popup.click()
    except:
        pass
    sleep(2)
    #Refrsh loop
    #full_unfollow(bot,15)
    while True:
        #Loop counters
        photo_interactions = 0
        #Go to hashtag & newest photo
        sleep(5)
        
        getcontent(bot,settings)
       
        sleep(5)
        #photo count loop
        while photo_interactions <= 12:
            decision = randrange(100)
            if decision < settings['chance_of_like']:
                try:
                    sleep(1)
                    perform_like(bot)
                    print('like')
                except:
                    print('failed like')
                    getcontent(bot,settings)
                    photo_interactions -= 1 
            elif decision >= settings['chance_of_like'] and decision< settings['chance_of_like'] + settings['chance_of_follow'] :
                try:
                    perform_follow(bot)
                    print ('followed')
                except:
                    print('failed follow')
                    getcontent(bot,settings)
                    photo_interactions -= 1 
            else:
                pass
            photo_interactions += 1
            sleep(5)
            arrow_right(bot)
            sleep(settings['time_interval'])
    


def run():
    options = Options()
    options.headless = True
    service = Service(r"files\geckodriver.exe")

    print(service)
    driver = webdriver.Firefox(service=service)
    driver.delete_all_cookies()
    #driver = webdriver.Firefox(r"C:\Users\Siarczyn\Desktop\bot\files\geckodriver.exe")   


    try:
        bot(driver)

    except:
        driver.close()
        sleep(30)
        run()

run()