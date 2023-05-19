# -*- coding: utf-8 -*-

import time
import os
import traceback
import argparse
# import functools
# from matplotlib.dates import SecondLocator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from tools.file_utils import parser_yaml
from gft.batch_pack import batch_pack, batch_pack_rqsl

PROJECT_PATH = None
CHROME_DRIVER_PATH = None
DOC_PATH = None
PACKAGE_PATH = None

TIMEOUT = 10

# fuzhou [ "gxjychain","grcychain","losejobchain", "sy","zkydchain"]
route_id_map = {
    'lhjy': 'lhjyyjslbkcltl',
    'qyzgtx': 'qyzgtxyjslbkzrgk',
    'losejob': 'syyjslbqjacr',
    'grcy': 'grcyyjslbqjmzv',
    'gxjy': 'gxjyyjslbserpi',
    'ygly': 'yglyyjslbygvea',
    'sy': 'syyjsltbktppz',
    'wykfd': 'wykcydvqsnb',
    'socialassistance': 'shjztkklq',
    'fczc': '',
    # chain
    'gxjychain': 'gxjyyjslbserpi',
    'grcychain': 'grcyyjslbqjmzv',
    'losejobchain': 'syyjslbqjacr',
    'zkydchain': 'zkydyjslbzczns',
    # 3-15
    'yglychain': 'yglyyjslbygvea',
    'qyzgtxchain': 'qyzgtxyjslbkzrgk',
    'lhjychain': 'lhjyyjslbkcltl',
    # test
    'test': 'laxtest'
}


def configure_gft(region='fzs'):
    global PROJECT_PATH, CHROME_DRIVER_PATH, DOC_PATH, PACKAGE_PATH, TIMEOUT
    config = parser_yaml('./gft/config/package_script.yaml')
    gft_config = config['gft']  # GftSimular.name

    PROJECT_PATH = gft_config['project_path']
    CHROME_DRIVER_PATH = gft_config['chrome_driver_path']
    DOC_PATH = gft_config['doc_path']
    PACKAGE_PATH = gft_config['package_path']

    TIMEOUT = gft_config['timeout']


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
    success = []
    fail = []
    fail_checked = []

    def __init__(self) -> None:
        super(GftSimular, self).__init__()
        self.doc_path = os.path.join(DOC_PATH, self.name)
        self.app_id = None
        self.route_name = None
        self.app_name = None

    def test_browser(self):
        self.browser = webdriver.Chrome(service=self.service)

    def test(self, route_name='losejob'):
        self.login()
        for _ in range(10):
            self.app_detail_page(route_name)

    def resume_input(self, input_element, text):
        ActionChains(self.browser).double_click(input_element).perform()
        input_element.send_keys(text)

    def handle(self, route_name):
        self.login()
        res = self.app_detail_page(route_name)
        print(res)
        if res:
            res.click()
        else:
            self.add_version()

    def script(self, route_name):
        res = self.app_detail_page(route_name)
        print(res)
        if res:
            # self.perfect_app()
            print(self.route_name, '---')
        else:
            self.add_version()

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
        WebDriverWait(self.browser, timeout=TIMEOUT).until(
            lambda b: b.find_element(By.XPATH, '//span[text()="工作"]'))
        print('login success')

    def app_detail_page(self, route_name):
        self.route_name = route_name
        if not route_id_map.get(route_name):
            self.app_id = route_name
        else:
            self.app_id = route_id_map.get(route_name)
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
        status_div = WebDriverWait(self.browser, TIMEOUT).until(
            lambda b: b.find_element(By.XPATH, '//div[text()=" 状态： "]'))
        if '未完善应用' in status_div.text:
            return True
        else:
            detail_btn.click()
            WebDriverWait(self.browser, timeout=TIMEOUT).until(
                lambda b: b.find_element(By.XPATH, '//tbody[1]/tr[1]/td[1]'))
        # try:
        #     perfect_btn = WebDriverWait(self.browser, TIMEOUT).until(
        #         lambda b: b.find_element(By.XPATH, '//span[text()="完善应用"]/..'))
        #     return perfect_btn
        # except Exception as e:
        #     detail_btn.click()
        #     WebDriverWait(self.browser, timeout=TIMEOUT).until(
        #         lambda b: b.find_element(By.XPATH, '//tbody[1]/tr[1]/td[1]'))

    def perfect_app(self):
        WebDriverWait(self.browser, TIMEOUT).until(lambda b: b.find_element(
            By.XPATH, '//span[text()="完善应用"]/..')).click()
        time.sleep(2)
        submit_btn = WebDriverWait(
            self.browser, timeout=TIMEOUT
        ).until(lambda b: b.find_element(
            By.XPATH,
            '//button[@class="ant-btn ant-btn-primary"]/span[text()="提 交"]/..')
                )
        explainWord_path = os.path.join(self.doc_path, self.explainWord_name)
        pressureWord_path = os.path.join(self.doc_path, self.pressureWord_name)
        detectionWord_path = os.path.join(self.doc_path,
                                          self.detectionWord_name)
        js = '''
        document.getElementById('explainWordFile').style.display = 'block';
        document.getElementById('pressureWordFile').style.display = 'block';
        document.getElementById('detectionWordFile').style.display = 'block'
        document.getElementById('zipFile').style.display = 'block'
        '''

        self.browser.find_element(
            By.ID, 'explainWordFile').send_keys(explainWord_path)
        self.browser.find_element(
            By.ID, 'pressureWordFile').send_keys(pressureWord_path)
        self.browser.find_element(
            By.ID, 'detectionWordFile').send_keys(detectionWord_path)

        self.browser.execute_script(js)
        #languageType
        #zipType
        # self.browser.find_element(By.ID, 'zipFile').send_keys(
        #     '/home/zg/Documents/gftPackage/{}.zip'.format(d[self.app_id]))
        self.browser.find_element(By.ID, 'zipFile').send_keys(
            os.path.join(PACKAGE_PATH, self.route_name + '.zip'))
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
                print('{0} 添加成功'.format(self.app_name))
            else:
                print('{0} 添加失败: {1}'.format(self.app_name, tip.text))
        except Exception as e:
            print('{0} 添加失败'.format(self.app_name))
            self.fail.append(self.app_id)
            print(e)
            print('----')

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
        self.browser.find_element(By.ID, 'zipFile').send_keys(
            os.path.join(PACKAGE_PATH, self.route_name + '.zip'))
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
                self.fail.append(self.app_id)
                print('{0} 添加失败: {1}'.format(self.app_name, tip.text))
        except Exception as e:
            print('{0} 添加失败'.format(self.app_name))
            self.fail.append(self.app_id)
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
            self.success.append(self.app_id)
        except Exception as e:
            self.fail_checked.append(self.app_id)
            print(e)
            print('请指定正确的版本')

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
            traceback.print_exc()
            print('-')
            print(count)
            if (count == max_count):
                failed_id.append(app_id)
                failed_id_dict[app_id] = e
        finally:
            count = count + 1
    print(failed_id)
    print(failed_id_dict)


def t():
    with GftSimular() as s:
        s.test()
        time.sleep(6)


def batch_add_version():
    with GftSimular() as s:
        s.login()
        for route_name in ROUTE_LIST:
            app_id = route_id_map.get(route_name)
            if app_id:
                s.script(route_name)
        time.sleep(60)


BASE = {
    # 'lean': {
    #     'account': ['LAXKF', 'Laxkf@123456'],
    #     'route_list': [
    #         'csyyosvlc',
    #     ]
    # },
    'lean': {
        'account': ['LAXKF', 'Laxkf@123456'],
        'route_list': [
            'yzymhxxbgrqslylqco',
            'laxggcswsxksc',
            'gsbgdjnvqdf',
            'fppzhdrqslvrulw',
        ]
    },
    'guangchang': {
        'account': ['GCXKF', 'Gcxkf@123456'],
        'route_list': [
            'czwsprpsgwxkrqslvrznu',
            'lmzzscjyxkzhfrqslwnejl',
            'lszyldsprqslklqef',
            'kckckchgxjsgczyhzzszyldshrqslzkgbv',
        ]
    },
    'yihuang': {
        'account': ['YHXKF', 'Yhxkf@123456'],
        'route_list': [
            'jzgcsgxkzhfhsgxmtpwlb',
            'jsydghxkzrqsldmtld',
            'yhcsglgrwjcsdlsp',
            'yhxqxnscjsxmstbcfasp',
            'yihqxnqsq',
        ]
    },
    # 'linchuan': {
    #     'account': ['LCQKF', 'Lcqkf@123456'],
    #     'route_list': [
    #         'jszgzrdnshlb',
    #         'lmzzscjyxkzhfrqslerukr',
    #         'fgssldjefjtv',
    #         'gsfgsbgbadjrqsltckek',
    #     ]
    # },
    # 'nanfeng': {
    #     'account': ['NFXKF', 'Nfxkf@123456'],
    #     'route_list': [
    #         'nfxggcswsxksc',
    #         'xcyxszdspjysldjrqsltbqzy',
    #         'xcyxszdspjyyxdjrqsligpxx',
    #         'nfxlyzwjyzshf',
    #     ]
    # },
    # 'jinxi': {
    #     'account': ['FZJXXKF', 'Fzjxxkf@123456'],
    #     'route_list': [
    #         'jxxdtljlhsgjjxjy',
    #         'nyjxzzyhzygczfsdnjsgzrrdhdjclrqslyxpaz',
    #         'jxxtljlhsgjnj',
    #         'jsgcjgghtjhsrqslpxntr',
    #     ]
    # },
    'nancheng': {
        'account': ['FZNCXKF', 'Fzncxkf@123456'],
        'route_list': [
            # 'ncyxgsfdzsbgdj',
            # 'yxgsfddbrbgdj',
            # 'ncyxgssldj',
            # 'ncnmzyhzskydj',
        ]
    },
    'gaoxin': {
        'account': ['FZSGXKFQKF', 'Fzsgxkf@123456'],
        'route_list': [
            # 'shttfrxksplqnyw',
            # 'nzgssldjeeknd',
            # 'nzgsbgdjrofec',
            # 'nzgszxdjrqeta',
        ]
    },
}


def rqsl_batch_package():
    # route_list = ['lmzzscjyxkzhfrqslerukr']
    project_path = '/home/zg/work/gft-new-item-services'
    # package_path = os.path.join('/home/zg/Documents/gftPackage', project)
    package_path = '/home/zg/Documents/gftPackage/rqsl'
    # batch_pack_rqsl(project_path, package_path, route_list)
    sum = 0
    for region, v in BASE.items():
        route_list = v.get('route_list')

        sum = sum + len(route_list)
        if len(route_list) != 0:
            batch_pack_rqsl(project_path, package_path, route_list, region)
    print('sum: ', sum)


def rqsl_batch_add_version():
    configure_gft('gft')
    global PROJECT_PATH, PACKAGE_PATH
    PROJECT_PATH = '/home/zg/work/gft-new-item-services'
    PACKAGE_PATH = '/home/zg/Documents/gftPackage/rqsl'
    for region, v in BASE.items():
        route_list = v.get('route_list')
        account, passwd = v.get('account')
        if len(route_list) == 0:
            pass
        else:
            with GftSimular() as s:
                s.login(account, passwd)
                for route_name in route_list:
                    # app_id = route_id_map.get(route_name)
                    # if app_id:
                    s.script(route_name)
                time.sleep(10)
        print(region, '----end')
    print('success: ', s.success)
    print('fail: ', s.fail)
    print('fail_checked: ', s.fail_checked)


if __name__ == '__main__':
    pass
    # rqsl_batch_package()
    rqsl_batch_add_version()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--region',
    #                     help='指定登录区县(中文首字母缩写)，默认抚州市',
    #                     default='fzs')
    # parser.add_argument('--isPack',
    #                     help="是否打包，1打包 0不打包",
    #                     default='1',
    #                     type=int)
    # args = parser.parse_args()
    # region = args.region
    # configure_gft(region)
    # if 'lax' == region:
    #     route_id_map = {
    #         'zkydchain': 'csfzzxqmley',
    #         'grcychain': 'laxtest',
    #     }
    # resList = []
    # print('route list: ', ROUTE_LIST)
    # if args.isPack:
    #     resList = batch_pack(PROJECT_PATH, PACKAGE_PATH, ROUTE_LIST)
    # if all(resList):
    #     batch_add_version()
    #     pass
    # else:
    #     print(dict(zip(ROUTE_LIST, resList)))
