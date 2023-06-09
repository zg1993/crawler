# -*- coding: utf-8 -*-

import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import sys
import shutil


download_path = '/home/zg/Downloads'
read_text_path = '/home/zg/Downloads/2.txt'
# current_time_str = datetime.now().strftime('%m%d_%H%M')
current_time_str = datetime.now().strftime('%m%d')
pic_path = os.path.join(download_path, current_time_str)

def create_dir(name=current_time_str):
    os.chdir('/home/zg/Downloads')
    if os.path.exists(name):
        confirm = input('Is delete {} dir "y" or "Y" continue: '.format(name))
        if 'y' == confirm.lower():
            shutil.rmtree('./{}'.format(name))
        else:
            raise NameError('please delete {} before create dir'.format(name))
    os.mkdir(name)
    # os.rmdir(current_time_str)

async def down_img(session, url, name, pic_dir = pic_path):
    img = await session.get(url)
    content = await img.read()
    file_path = os.path.join(pic_dir, name)
    # print('file_path', file_path)
    with open(file_path, 'wb') as f:
        f.write(content)
        print('download sucess {}'.format(name) )
    return True

def read_txt(path):
    p = re.compile(r'\[(.*?)\]')
    with open(path, 'r+') as f:
        return [p.findall(line)[0] for line in f]

# print(read_txt('/home/zg/Downloads/2.txt'))

async def main(file=read_text_path):
    URL = read_txt(file)
    create_dir()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(down_img(session, img_url, str(index) + '.' + img_url.split('.')[-1])) for (index, img_url) in enumerate(URL,1)]
        done, pending = await asyncio.wait(tasks)
        all_results = [done_task.result() for done_task in done]
        print('all_results')
        if all(all_results):
            print('success')
        else:
            error_list = [URL[index] for (index, val) in enumerate(all_results) if val != True]
            print('error_list: ', error_list)
        
    

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
    # argv[1] 传文件路径下载图片
    if len(sys.argv) > 1:
        asyncio.run(main(sys.argv[1]))
    else:
        asyncio.run(main())

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


async def main1():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(4, 'world'))

    print(f"started at {time.strftime('%X')}")
    # task2.add_done_callback(fn)
    # await say_after(2, 'world')
    # await say_after(1, 'hello')
    # r1 = await task2
    # r = await task1

    print(f"finished at {time.strftime('%X')}")


# asyncio.run(m())
