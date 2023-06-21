# -*- coding: utf-8 -*-

import sys
import os
import asyncio
import aiohttp
import json
from tools.utils import timestamp_to_str, write_file
from tools.parse_html import parese_wexin_article


# 时间取updatetime

search_key = ['比亚迪', '半月谈']
# search_key = ['比亚迪']

cookie = 'appmsglist_action_3928503461=card; noticeLoginFlag=1; remember_acct=604328914@qq.com; pgv_pvid=2924024080; pac_uid=0_050e9ae06ea51; tvfe_boss_uuid=890b429a39ebc7ca; RK=Gelp6pi4Xf; ptcz=66aa14b01a2ea41e402cfba10b10b07334b9709205e4229b0df45cf26d1a7997; fqm_pvqid=8197a091-1292-41b4-8874-b5719a04e115; ptui_loginuin=604328914; ua_id=jW09Y9qMMJuUgdQ1AAAAANDk3XKvP74QfmGGFt4DCq0=; wxuin=86107293996414; mm_lang=zh_CN; noticeLoginFlag=1; _clck=3928503461|1|fch|0; uuid=1799e310d936d76a8e9552d42ab7758f; bizuin=3928503461; ticket=3055eef572556bba369cc544f4f7bb99e1db392b; ticket_id=gh_9b10aff30334; slave_bizuin=3928503461; cert=7_F0d8vKgXDe39Lj9tA4NfHvuqVEH3dp; rand_info=CAESIMsAxFdK/MOWway7z7ZCPSJoSSFMpQxnH2F+iUHSrKna; data_bizuin=3928503461; data_ticket=PSiEq6/I/t3vzOhp4NUGK0Ezjc/E++RH08n2ewNRViZqj9SfIuEQdfDwEVBWSf47; slave_sid=RHRzOVVvNURuQjlodThxNWpBNUZnNTQ2RHJySWJhVm90V056akpzcXcyempRb2N5ZDk0UTRPMTk2UGd6R1pkWnZHelhxTWtmUjdGS0MxR1M4RG1qMl9UMXREaUdKWFA2Q1lDYWNrQ2h3WXNMemxveGViMk42bG03bGU5WXRXU2RKelJ1SlcwR3BzdUFZNWZ6; slave_user=gh_9b10aff30334; xid=a157fe1897e13be796038689e3b2b6cd; openid2ticket_opTQo6rYA33kqeYqkKRaa0BAPji4=0WUhwyVFTj+fIfUWAQLLXIpR9dTD63K4FNX/8q4SSbE=; _clsk=12hhpek|1686820557642|6|1|mp.weixin.qq.com/weheat-agent/payload/record'
token = '651263457'

def print_dict(d):
    print(json.dumps(d, indent=4, ensure_ascii=False))


async def fetch(session, url, is_json=True, **kwargs):
    async with session.get(url, **kwargs) as resp:
        if resp.status != 200:
            resp.raise_for_status()
        if is_json:
            data = await resp.json()
        else:
            data = await resp.text()
        return data


async def fetch_multi_fakeid(session, search_arr, headers):
    url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
    tasks = []
    for key in search_arr:
        params = {
            'action': 'search_biz',
            'begin': '0',
            'count': '5',
            'query': key,
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        tasks.append(
            asyncio.create_task(
                fetch(session, url, headers=headers, params=params)))
    results = await asyncio.gather(*tasks)
    return results


async def init_fakeid(session, headers):
    search_res = await fetch_multi_fakeid(session, search_key, headers)
    # print('init_fakeid: ',search_res)
    fakeid_arr = []
    for index, res in enumerate(search_res):
        name = search_key[index]
        if not res.get('list'):
            print(res)
        arr = res['list']
        if len(arr):
            selected = arr[0]
            print('关键字<{0}>搜索结果：{1}'.format(name, selected['nickname']))
            print('介绍 {}'.format(selected.get('signature')))
            fakeid_arr.append(selected['fakeid'])
        else:
            print('无法搜索到 {}, 请重新确认关键字'.format(name))
    return fakeid_arr


async def fetch_multi_articles(session,
                               fakeid_arr,
                               headers,
                               article_search_key=''):
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    tasks = []
    for fakeid in fakeid_arr:
        params = {
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'fakeid': fakeid,
            'type': '9',
            'query': article_search_key,
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        tasks.append(
            asyncio.create_task(
                fetch(session, url, headers=headers, params=params)))
    results = await asyncio.gather(*tasks)
    return results


def handle_articles_arr(arrs):
    result = []
    for arr in arrs:
        articles = arr.get('app_msg_list', [])
        print('articles len', len(articles))
        for article in articles:
            update_time = article['update_time']
            title = article['title']
            link = article['link']
            cover = article['cover']
            display_time = timestamp_to_str(update_time)
            result.append({
                'update_time': update_time,
                'title': title,
                'link': link,
                'cover': cover,
                'display_time': display_time,
            })
    print('res: ', len(result))
    return result

async def parse_wexin_article(session, url, **kwargs):
    html_text = await fetch(session, url, is_json=False, **kwargs)
    new_html = parese_wexin_article(html_text)

    # path = '/home/zg/Documents/gftPackage/{}.html'.format('1.html')
    # write_file(path, html_text)



async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
        params = {
            'action': 'list_ex',
            'begin': '0',
            'count': '10',
            'fakeid': 'MjM5OTU4Nzc0Mg==',
            'type': '9',
            'query': '碳',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'cookie': cookie,
            'pragma': 'no-cache',
            'referer':
            'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN'.format(token),
            'sec-ch-ua':
            '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Linux",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        fakeid_arr = await init_fakeid(session, headers)
        print('fakeid_arr: ', fakeid_arr)
        articles_arr = await fetch_multi_articles(session, fakeid_arr, headers)
        result = handle_articles_arr(articles_arr)

        # async with session.get(url, params=search_params, headers=headers) as response:
        #     print('url', response.url)
        #     print('status: ', response.status)
        #     print('Content-type: ',response.headers['content-type'])
        #     html = await response.json()
        #     print(dir(html))
        #     print(type(html))
        #     print_dict(html)
        # print(len(html.get('app_msg_arr', [])))


if __name__ == '__main__':
    asyncio.run(main())