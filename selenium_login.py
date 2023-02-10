# -*- coding: utf-8 -*-

import time
import os
# import functools
# from matplotlib.dates import SecondLocator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException

from tools.date_utils import tt

CHROME_DRIVER_PATH = '/home/zg/chromedriver'
DOC_PATH = '/home/zg/Downloads/selenium'


class Simulator:

    def __init__(self) -> None:
        self.service = Service(CHROME_DRIVER_PATH, port=8995)
        self.browser = None

    def __enter__(self):
        self.browser = webdriver.Chrome(service=self.service)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def _find(self, xpath):
        return self.browser.find_element(By.XPATH, xpath)

    # def start_browser(self):
    #     self.browser.get('https://www.baidu.com/')
    #     js = 'window.open("https://www.douban.com");'
    #     self.browser.execute_script(js)


class GftSimular(Simulator):
    name = 'gft'
    login_url = 'http://ganfutong.jiangxi.gov.cn:30014/api-gateway/common-ucenter-server/oauth2/ssologin'
    app_list_url = 'http://ganfutong.jiangxi.gov.cn:30014/jpaas/appcenter/appmenu/application'
    account = 'LAXKF'
    passwd = 'Laxkf@123456'
    explainWord_name = 'explainWord.doc'
    pressureWord_name = 'pressureWord.doc'
    detectionWord_name = 'detectionWord.xls'
    icon = 'icon.png'

    def __init__(self) -> None:
        super(GftSimular, self).__init__()
        self.doc_path = os.path.join(DOC_PATH, self.name)

    def test_browser(self):
        self.browser = webdriver.Chrome(service=self.service)

    def resume_input(self, input_element, text):
        ActionChains(self.browser).double_click(input_element).perform()
        input_element.send_keys(text)

    def handle(self, app_id):
        self.login()
        self.app_detail_page(app_id)
        self.add_version()

    def login(self):
        self.browser.maximize_window()
        self.browser.get(self.login_url)
        account_input = self.browser.find_element(By.ID, 'loginUserName')
        passwd_input = self.browser.find_element(By.ID, 'password-text')
        login_btn = self.browser.find_element(By.XPATH,
                                              '//div[@class="account-btn"]')
        account_input.click()
        account_input.send_keys(self.account)
        passwd_input.click()
        passwd_input.send_keys(self.passwd)
        login_btn.click()

    def app_detail_page(self, app_id):
        self.browser.get(self.app_list_url)
        app_id_input = WebDriverWait(
            self.browser, timeout=10).until(lambda b: b.find_element(
                By.XPATH, '//input[@placeholder="请输入应用标识"]'))
        search_btn = self.browser.find_element(By.XPATH,
                                               '//span[text()="查 询"]/..')

        app_id_input.send_keys(app_id)
        search_btn.click()
        detail_btn = WebDriverWait(
            self.browser, timeout=10
        ).until(lambda b: b.find_element(
            By.XPATH,
            '//div[@class="ant-card-meta-title"]/div[text()="应用唯一标识：dzzzdy"]/..//button'
        ))
        detail_btn.click()
        WebDriverWait(self.browser, timeout=10).until(
            lambda b: b.find_element(By.XPATH, '//tbody[1]/tr[1]/td[1]'))
        # time.sleep(3)

    def add_version(self):
        # versionNo_input
        # explainWord_input
        # pressureWord_input
        # detectionWord_input
        # reference_input
        # updateExplain_textarea
        # doc path
        explainWord_path = os.path.join(self.doc_path, self.explainWord_name)
        pressureWord_path = os.path.join(self.doc_path, self.pressureWord_name)
        detectionWord_path = os.path.join(self.doc_path,
                                          self.detectionWord_name)
        pre_version = self._get_previous_version()
        version_text = self._count_version(pre_version)
        add_version_btn = self._find('//a[text()="版本添加"]')
        add_version_btn.click()
        submit_btn = WebDriverWait(
            self.browser, timeout=10
        ).until(lambda b: b.find_element(
            By.XPATH,
            '//button[@class="ant-btn ant-btn-primary"]/span[text()="提 交"]/..')
                )
        # show hidden file-input
        js = '''
        document.getElementById('explainWordFile').style.display = 'block';
        document.getElementById('pressureWordFile').style.display = 'block';
        document.getElementById('detectionWordFile').style.display = 'block'
        document.getElementById('zipFile').style.display = 'block'
        '''
        self.browser.execute_script(js)

        # self.browser.find_element(By.ID, 'versionNo').send_keys(version_text)
        self.browser.find_element(By.ID, 'versionNo').send_keys('2.0.0')
        self.browser.find_element(
            By.ID, 'explainWordFile').send_keys(explainWord_path)
        self.browser.find_element(
            By.ID, 'pressureWordFile').send_keys(pressureWord_path)
        self.browser.find_element(
            By.ID, 'detectionWordFile').send_keys(detectionWord_path)
        #languageType
        #zipType
        self.browser.find_element(
            By.ID, 'zipFile').send_keys('/home/zg/Documents/gftPackage/sy.zip')
        self.browser.find_element(By.ID, 'updateExplain').send_keys('test')
        submit_btn.click()
        try:
            tip = WebDriverWait(
                self.browser, timeout=10).until(lambda b: b.find_element(
                    By.XPATH,
                    '//div[@class="ant-notification-notice-description"]'.
                    format(version_text)))
            print(tip.text)
        except Exception:
            pass
        try:
            WebDriverWait(self.browser,
                          timeout=10).until(lambda b: b.find_element(
                              By.XPATH, '//tbody[1]/tr[1]/td[text()="{}"]'.
                              format(version_text)))
            print('add success')
        except Exception:
            pass

    def _count_version(self, version):
        v_list = version.split('.')
        v_list[-1] = str(int(v_list[-1]) + 1)
        return '.'.join(v_list)

    def _get_previous_version(self):
        assert 'AppDetail' in self.browser.current_url
        version_span = self.browser.find_element(By.XPATH,
                                                 '//tbody[1]/tr[1]/td[1]')
        return version_span.text


# b.find_element(By.XPATH,'//a[text()="版本添加"]')
# '//span[@class="ant-modal-confirm-title" and text()="未授权"]'
# b.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary"]/span[text()="确 定"]/..').click() 重新登录
def test(app_id='dzzzdy', max_count=0):
    failed_id_dict = {}
    failed_id = []
    count = 0
    while True:
        if (count > max_count):
            break
        try:
            with GftSimular() as s:
                s.handle(app_id)
        except Exception as e:
            print('-')
            print(count)
            if (count == max_count):
                failed_id.append(app_id)
                failed_id_dict[app_id] = e
        finally:
            count = count + 1
    print(failed_id)
    print(failed_id_dict)


if __name__ == '__main__':
    test()
    # pass

# COOKIES = {}
# user_name = browser.find_element(By.ID, 'loginUserName')
# user_name.click()
# user_name.send_keys('LAXKF')

# passwd = browser.find_element(By.ID, 'password-text')
# passwd.click()
# passwd.send_keys('Laxkf@123456')
# # browser.find_element(By.ID, 'passWord').send_keys('laxkf@123456')

# login_button = browser.find_element(By.XPATH, '//div[@class="account-btn"]')

# login_button.click()

# print(browser.get_cookies())

# print(browser.current_url)

# time.sleep(3)

# print(browser.current_url)
# time.sleep(1)
# browser.quit()

# def get_cookies():
#     cookies_dict = {}
#     for item in browser.get_cookies():
#         print(item)
#         print(item['name'])
#         print(item['value'])
#         cookies_dict[item['name']]
#     return cookies_dict
