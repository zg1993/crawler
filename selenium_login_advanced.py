# -*- coding: utf-8 -*-

import time
import os
import traceback
import argparse
from tools.file_utils import parser_yaml
import itertools
# import functools
# from matplotlib.dates import SecondLocator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from gft.batch_pack_advanced import batch_pack
from gft.config.package_to_id import load_file

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_PATH, 'gft/config/path_to_id.json')
CONFIG_FILE_PATH = os.path.join(BASE_PATH, 'gft/config/package_script.yaml')

#common
PACKAGE_PATH = None
CHROME_DRIVER_PATH = None
DOC_PATH = None
TIMEOUT = None
ACCOUNT_PASSWD = {}

# project
PROJECT_PATH = None
BUILD_COMMAND = None
ROUTE_DICT = None


def configure_gft(file_path=CONFIG_FILE_PATH,
                  project_name='compress-package-zg'):
    global PROJECT_PATH, CHROME_DRIVER_PATH, DOC_PATH, TIMEOUT, ACCOUNT_PASSWD, PACKAGE_PATH, ROUTE_DICT, BUILD_COMMAND
    config = parser_yaml(file_path)
    # common_config
    common_config = config['common']
    PACKAGE_PATH = common_config['package_path']
    CHROME_DRIVER_PATH = common_config['chrome_driver_path']
    DOC_PATH = common_config['doc_path']
    TIMEOUT = common_config['timeout']
    ACCOUNT_PASSWD = common_config['account_passwd']
    # project_config
    project_config = config[project_name]
    PROJECT_PATH = project_config['project_path']
    BUILD_COMMAND = project_config['build_command']
    ROUTE_DICT = project_config['route_dict']


route_id_map = {
    'lhjy': 'lhjyyjslbkcltl',
    # 'qyzgtx': 'qyzgtxyjslbkzrgk',
    'losejob': 'syyjslbqjacr',
    'grcy': 'grcyyjslbqjmzv',
    'gxjy': 'gxjyyjslbserpi',
    'ygly': 'yglyyjslbygvea',
    'wykfd': 'wykcydvqsnb',
    'socialassistance': 'shjztkklq',
    'fczc': '',
    # chain
    'sy': 'syyjsltbktppz',
    'gxjychain': 'gxjyyjslbserpi',
    'grcychain': 'grcyyjslbqjmzv',
    'losejobchain': 'syyjslbqjacr',
    'zkydchain': 'zkydyjslbzczns',
    'zkydchainminority': 'ssmzzkjfyjsemhff',
    'zkydchaintaiwan': 'tjkszkjfyjszcexh',
    # 3-15
    'yglychain': 'yglyyjslbygvea',
    'qyzgtx': 'qyzgtxyjslbkzrgk',
    'qyzgtxearly': 'qyzgtqtxyjslbqbupb',
    'lhjychain': 'lhjyyjslbkcltl',
    # test
    'test': 'laxtest',
    # 4-10
    'socialAssistance': 'shjztkklq'
}


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
    explainWord_name = 'explainWord.doc'
    pressureWord_name = 'pressureWord.doc'
    detectionWord_name = 'detectionWord.xls'
    icon = 'icon.png'

    def __init__(self) -> None:
        super(GftSimular, self).__init__()
        self.doc_path = os.path.join(DOC_PATH, self.name)
        self.app_id = None
        self.package_path = None
        self.route_name = None
        self.app_name = None

    def test_browser(self):
        self.browser = webdriver.Chrome(service=self.service)

    def resume_input(self, input_element, text):
        ActionChains(self.browser).double_click(input_element).perform()
        input_element.send_keys(text)

    def test(self, *args, **kwargs):
        self.app_detail_page(*args, **kwargs)

    def script(self, *args, **kwargs):
        self.app_detail_page(*args, **kwargs)
        self.add_version()

    def script_temp(self, ID):
        self.app_detail_page(ID, ID)
        self.add_version()

    def logout(self):
        actions = ActionChains(self.browser)
        actions.move_to_element(
            self._find('//div[@class="actions-btn"]')).click()
        actions.perform()
        self._find('//span[text()="退出登录"]').click()
        WebDriverWait(self.browser, TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//div[@class="ant-modal-body"]//span[text()="确 定"]/..'
                 ))).click()
        print('-')
        # 确保退出到登录界面
        WebDriverWait(self.browser, TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@class="account-btn"]'))).click()
        print('logout')

    def login(self, account, passwd):
        self.browser.maximize_window()
        self.browser.get(self.login_url)
        WebDriverWait(self.browser,
                      timeout=TIMEOUT).until(lambda b: b.find_element(
                          By.ID, 'loginUserName')).send_keys(account)
        WebDriverWait(self.browser, timeout=TIMEOUT).until(
            lambda b: b.find_element(By.ID, 'password-text')).send_keys(passwd)
        WebDriverWait(self.browser,
                      timeout=TIMEOUT).until(lambda b: b.find_element(
                          By.XPATH, '//div[@class="account-btn"]')).click()
        # WebDriverWait(
        #     self.browser, timeout=2
        # ).until(lambda b: b.find_element(
        #     By.XPATH,
        #     '//div[text()="用户名或密码不正确，注意区分大小写" or text()="Username or password error"]'
        # ))
        try:
            WebDriverWait(self.browser, timeout=TIMEOUT).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@class="actions-btn"]'))).click()
            print('login success')
        except Exception as e:
            print('login failed', e)

    def search_page(self, app_id, package_path):
        pass

    def app_detail_page_by_name(self, app_name):
        pass

    def app_detail_page(self, app_id, package_path):
        self.app_id = app_id
        self.package_path = package_path
        self.browser.get(self.app_list_url)
        app_id_input = WebDriverWait(
            self.browser, timeout=TIMEOUT).until(lambda b: b.find_element(
                By.XPATH, '//input[@placeholder="请输入应用标识"]'))
        app_id_input.send_keys(self.app_id)
        WebDriverWait(
            self.browser, timeout=TIMEOUT
        ).until(lambda b: b.find_element(
            By.XPATH,
            '//div[@class="ant-card-meta-title"]/div[starts-with(text(), "应用唯一标识")]'
        ))
        WebDriverWait(self.browser, timeout=TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[text()="查 询"]/..'))).click()
        # detail_btn = WebDriverWait(
        #     self.browser, timeout=TIMEOUT
        # ).until(lambda b: b.find_element(
        #     By.XPATH,
        #     '//div[@class="ant-card-meta-title"]/div[text()="应用唯一标识：{}"]/..//button'
        #     .format(self.app_id)))

        detail_btn = WebDriverWait(self.browser, TIMEOUT).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//div[@class="ant-spin-container"]/div[@class="ant-row"]/div[1]//div[text()="应用唯一标识：{}"]/..//button'
                .format(self.app_id))))

        title_div = WebDriverWait(
            self.browser, TIMEOUT).until(lambda b: b.find_element(
                By.XPATH,
                '//div[text()="应用唯一标识：{}"]/../div[starts-with(text(),"应用名称：")]'
                .format(self.app_id)))
        print('---', title_div.text)
        self.app_name = title_div.text[5:]
        print(self.app_name)
        print(self.app_id)

        detail_btn.click()
        WebDriverWait(self.browser, timeout=TIMEOUT).until(
            lambda b: b.find_element(By.XPATH, '//tbody[1]/tr[1]/td[1]'))

    def perfect_app(self):
        pass
        # : e = b.find_element(By.XPATH, '//ul[@class="ant-card-actions"]//button[@class="ant-btn ant-btn-link"]/span[text()="完

    #  ...: 善应用"]/..')

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
            self.browser, timeout=TIMEOUT
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

        self.browser.find_element(By.ID, 'versionNo').send_keys(version_text)
        # self.browser.find_element(By.ID, 'versionNo').send_keys('2.0.0')
        self.browser.find_element(
            By.ID, 'explainWordFile').send_keys(explainWord_path)
        self.browser.find_element(
            By.ID, 'pressureWordFile').send_keys(pressureWord_path)
        self.browser.find_element(
            By.ID, 'detectionWordFile').send_keys(detectionWord_path)
        #languageType
        #zipType
        # self.browser.find_element(By.ID, 'zipFile').send_keys(
        #     '/home/zg/Documents/gftPackage/{}.zip'.format(d[self.app_id]))
        self.browser.find_element(
            By.ID, 'zipFile').send_keys(self.package_path + '.zip')
        self.browser.find_element(By.ID, 'updateExplain').send_keys('test')
        submit_btn.click()
        try:
            tip = WebDriverWait(
                self.browser, timeout=TIMEOUT
            ).until(lambda b: b.find_element(
                By.XPATH,
                '//div[@class="ant-notification-notice-description" or @class="ant-message-custom-content ant-message-success"]'
            ))
            # 该应用此版本号已存在
            # print(tip.text)
            if '保存成功' == tip.text:
                print('{0} 添加成功{1}'.format(self.app_name, version_text))
                self.submit_review(version_text)
            else:
                print('{0} 添加失败: {1}'.format(self.app_name, tip.text))
        except Exception as e:
            print('{0} 添加失败'.format(self.app_name))
            print(e)
            print('----')
            #local variable 'tip' referenced before assignment
            # printa(tip)

        # try:
        #     WebDriverWait(self.browser,
        #                   timeout=TIMEOUT).until(lambda b: b.find_element(
        #                       By.XPATH, '//tbody[1]/tr[1]/td[text()="{}"]'.
        #                       format(version_text)))
        #     print('add success')
        # except Exception:
        #     print('+-=')
        #     pass

    # 指定版本提交审核
    def submit_review(self, version_text):
        self.browser.refresh()
        try:
            WebDriverWait(self.browser,
                          timeout=TIMEOUT).until(lambda b: b.find_element(
                              By.XPATH, '//tbody[1]/tr[1]/td[text()="{}"]'.
                              format(version_text)))
            self._find('//tbody[1]/tr[1]//a[text()="提交审核"]').click()
            WebDriverWait(self.browser, TIMEOUT).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//div[@class="ant-modal-footer"]//button[@class="ant-btn ant-btn-primary"]/span[text()="确 定"]/..'
                ))).click()
            WebDriverWait(
                self.browser, TIMEOUT).until(lambda b: b.find_element(
                    By.XPATH,
                    '//div[@class="ant-message-notice"]//span[text()="操作成功"]'))
            # WebDriverWait(
            #     self.browser, TIMEOUT
            # ).until(lambda b: b.find_element(
            #     By.XPATH,
            #     '//div[@class="ant-modal-footer"]//button[@class="ant-btn ant-btn-primary"]'
            # )).click()
            # e = WebDriverWait(self.browser, timeout=TIMEOUT).until(
            # lambda b: b.find_element(By.XPATH, '//tbody[1]/tr[1]/td[8]"]'))
            print('提交审核成功:{0}，版本号{1}'.format(self.app_name, version_text))
        except Exception as e:
            print(e)
            print('请指定正确的版本')

    def generate_yc_setting(self, app_name):
        res = {
            'appId': '',
            'itemCode': '',
            'info': '',
            'requirement': '',
            'law': '',
            'process': '',
            'uploadMaterial': '',
            'online': '',
        }

        return res

    def _count_version(self, version):
        if (5 == len(version)):
            count = int(version.replace('.', ''))
            return '.'.join(list(str(count + 1)))
        else:
            v_list = version.split('.')
            v_list[-1] = str(int(v_list[-1]) + 1)
            return '.'.join(v_list)

    def _get_previous_version(self):
        assert 'AppDetail' in self.browser.current_url
        version_span = self.browser.find_element(By.XPATH,
                                                 '//tbody[1]/tr[1]/td[1]')
        return version_span.text


def test(region_to_packages):
    for region, packages in region_to_packages.items():
        account, passwd = ACCOUNT_PASSWD[region]
        print('login {} account: '.format(region), account, passwd)
        with GftSimular() as s:
            s.login(account, passwd)
            for app_id, packages_path in packages.items():
                s.test(app_id, packages_path)
                print(app_id, packages_path)
            time.sleep(10)


def batch_add_version_advanced(region_to_packages):
    # with GftSimular() as s:
    #     for region, packages in region_to_packages.items():
    #         account, passwd = ACCOUNT_PASSWD[region]
    #         print('login {} account: '.format(region), account, passwd)
    #         s.login(account, passwd)
    #         for app_id, packages_path in packages.items():
    #             s.script(app_id, packages_path)
    #             print(app_id, packages_path)
    #         time.sleep(10)
    #         s.logout()
    for region, packages in region_to_packages.items():
        account, passwd = ACCOUNT_PASSWD[region]
        print('login {} account: '.format(region), account, passwd)
        with GftSimular() as s:
            s.login(account, passwd)
            for app_id, packages_path in packages.items():
                s.script(app_id, packages_path)
                print(app_id, packages_path)
            time.sleep(10)


def test_login():
    with GftSimular() as s:
        for region, v in ACCOUNT_PASSWD.items():
            print(region, v)
            account, passwd = v
            s.login(account, passwd)
            s.logout()


def temp_add_version():
    print('temp add version')
    package_list = [
        'bdcesfzydj',
        # 'fztbdcdblb',
        'fztysfywsq',
    ]
    with GftSimular() as s:
        s.login('FZSKF', 'Fzskf@1234')
        for i in package_list:
            s.script_temp(i)
        time.sleep(60)


def wechat():
    return '、'.join(itertools.chain.from_iterable(
        ROUTE_DICT.values())) + '帮忙审核一下，谢谢'


if __name__ == '__main__':
    # example: python ~/work/crawler/selenium_login_advanced.py --login --project=vue
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--noPack',
        help="不打包",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--login',
        help='测试赣服通各个区县登录账号密码是否正确',
        default=False,
        action='store_true',
    )
    parser.add_argument('--project',
                        help='指定项目,默认gft一件事,可选赣通分（容缺受理）:rqsl; gtf-vue:vue',
                        default='compress-package-zg')
    args = parser.parse_args()
    configure_gft(project_name=args.project)
    if args.login:
        # test_login()
        # temp_add_version() # gft-vue 不动产办理临时使用
        # test start
        load_json = load_file(JSON_PATH)
        print('load_json:', load_json)
        if args.noPack:
            test(load_json)
        else:
            batch_pack(PROJECT_PATH, PACKAGE_PATH, args.project, BUILD_COMMAND)
            confirm = input('please "y" or "Y" continue: ')
            if confirm.lower() == 'y':
                # add version
                print('load', load_file(JSON_PATH))
                test(load_json)
                print(wechat())
            else:
                print('end')
        # end
    else:
        if args.noPack:
            load_json = load_file(JSON_PATH)
            batch_add_version_advanced(load_json)
        else:
            # package
            batch_pack(PROJECT_PATH, PACKAGE_PATH, args.project, BUILD_COMMAND)
            confirm = input('please "y" or "Y" continue: ')
            if confirm.lower() == 'y':
                # add version
                print('load', load_file(JSON_PATH))
                load_json = load_file(JSON_PATH)
                batch_add_version_advanced(load_json)
                print(wechat())
            else:
                print('end')
