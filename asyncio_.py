# -*- coding: utf-8 -*-

import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup

search_list = [i for i in range(100)]


async def request(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            # print(response.status)
            r = await response.text()
            soup = BeautifulSoup(r, 'html.parser')
            # print(soup.find)
            return soup.find('title').text


async def m():
    url = 'http://cn.bing.com/search'
    # params = {'q': '爬虫'}
    request_list = []
    for i in search_list:
        params = {}
        params['q'] = i
        request_list.append(request(url, params))
    r_list = await asyncio.gather(*request_list)
    print(r_list)


if __name__ == '__main__':

    # url = 'http://cn.bing.com/search'
    # params = {'q': '爬虫'}
    # request_list = []
    # for i in search_list:
    #     params = {}
    #     params['q'] = iz
    #     request_list.append(request(url, params))
    # r_list = await asyncio.gather(*request_list)
    # asyncio.run(m())
    # asyncio.run(request(url, params))
    pass


def fn(future):
    print('result:', future.result)
    # print('result:',future.result())


async def say_after(delay, what):
    print('-----' + what)
    await asyncio.sleep(delay)
    print(what)
    return delay + 1000


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(4, 'world'))

    print(f"started at {time.strftime('%X')}")
    # task2.add_done_callback(fn)
    # await say_after(2, 'world')
    # await say_after(1, 'hello')
    # r1 = await task2
    # r = await task1

    print(f"finished at {time.strftime('%X')}")


asyncio.run(m())
