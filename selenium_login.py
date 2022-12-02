# -*- coding: utf-8 -*-

import time
from matplotlib.dates import SecondLocator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

COOKIES = {}

service = Service('/home/zg/chromedriver')

browser = webdriver.Chrome(service=service)

browser.get(
    'http://ganfutong.jiangxi.gov.cn:30014/api-gateway/common-ucenter-server/oauth2/ssologin'
)

user_name = browser.find_element(By.ID, 'loginUserName')
user_name.click()
user_name.send_keys('LAXKF')

passwd = browser.find_element(By.ID, 'password-text')
passwd.click()
passwd.send_keys('Laxkf@123456')
# browser.find_element(By.ID, 'passWord').send_keys('laxkf@123456')

login_button = browser.find_element(By.XPATH, '//div[@class="account-btn"]')

login_button.click()

print(browser.get_cookies())

print(browser.current_url)

time.sleep(3)

print(browser.current_url)

# browser.quit()


def get_cookies():
    cookies_dict = {}
    for item in browser.get_cookies():
        print(item)
        print(item['name'])
        print(item['value'])
        cookies_dict[item['name']]
    return cookies_dict
