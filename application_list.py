# -*- coding: utf-8 -*-

import sys
import os

import requests
# from tools.selenium_login import get_cookies


def get_application_list(cookie_dict={}):
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "Cookie":
        "BIGipServerGanFuTong-10.4.111.186-188_193-198----30014=3278832650.15989.0000; sm2_pubk=049f969c94993656f6a486d2fe2733c8c1b82cae43a74fa3340bd49cd4f53d7227a6991d68f429f3d1a4fb0303f2e9e00c64aff0f149d2d602e6bae0c9dd86b930; access-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjU2Njg5NjYsImlhdCI6MTY2NTY1MDk2NiwidXNlcm5hbWUiOiJMQVhLRiJ9.QJqbTpwuq7Q18Y954dZEKLqxyLpa7MWlTueXCiOXf6U; login=true; userName=%E4%B9%90%E5%AE%89%E5%8E%BF%E8%B5%A3%E6%9C%8D%E9%80%9A%E5%BC%80%E5%8F%91; userId=b5b291d0d09946f2bd2b504a23733c2d"
    }
    page = 1
    url = 'http://ganfutong.jiangxi.gov.cn:30014/api-gateway/jpaas-appcenter-server/manager/back/app/list'
    payload = {"pageNo": page, 'pageSize': 9, 'type': 1}
    response = requests.post(
        url,
        data=payload,
        #  cookies=cookie_dict,
        headers=headers)

    print(response.cookies)
    print(response)


def test_input():
    count = 10
    while count > 0:
        print('begin')
        r = yield 1
        print(f'end{r}')
        print(r)
        count -= 1


def wrap():
    a = test_input()
    return [_ for _ in a]


if __name__ == '__main__':
    print(wrap())
    pass
    # print(sys.path)
    # selenium_login.get_cookies()
    # get_application_list()
    # get_cookies()
    # get_application_list(get_cookies())
