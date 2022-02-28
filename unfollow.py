from time import sleep
from datetime import datetime
import datetime as dt
from selenium.common.exceptions import NoSuchElementException


def get_followed(amount):
    print("f1")
    current_date = datetime.now()
    follow_list = []
    unfollow_list = []
    file = open("files/to_follow.txt", "r+")
    print("f2")
    lines = file.readlines()
    left = 0
    for line in lines:
        data = line.strip().split(',')
        if  datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f') + dt.timedelta(days=4) < current_date and left<amount :
            unfollow_list.append([datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f'), data[0]])
            left += 1
        else:
            follow_list.append([datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f'), data[0]])

    file.close()
    print("f3")

    file = open("files/to_follow.txt", "w+")
    for line in follow_list:
        file.write(str(line[1]) + "," + str(line[0]) + "\n")
    file.close()
    print("f4")
    return unfollow_list


def check_exists_by_xpath(xpath, bot):
    try:
        bot.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def check_status(bot, href, path):
    bot.get(href)
    print(check_exists_by_xpath(path, bot))
    return check_exists_by_xpath(path, bot)


def full_unfollow(bot, amount):
    to_unfollow = []
    print("start procedury")
    failed = []
    followed = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/div/span"

    to_unfollow = get_followed(amount)
    print(to_unfollow)
    for user in to_unfollow:
        try:
            if check_status(bot, user[1], followed):
                sleep(3)
                following = bot.find_element_by_xpath(followed)
                following.click()
                sleep(2)
                confirm_unfollow = bot.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]")
                confirm_unfollow.click()
                sleep(2)
        except:
            failed.append(user)
    file = open("files/failed_unfollows.txt", "a+")
    for line in failed:
        print(str(line[1]) + "," + str(line[0]) + "\n")
    file.close()
