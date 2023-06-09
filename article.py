# -*- coding: utf-8 -*-

import sys
import os
import asyncio
import aiohttp
import json
from tools.utils import timestamp_to_str

# 时间取updatetime

search_key = ['比亚迪', '半月谈']
# search_key = ['比亚迪']

cookie = 'appmsglist_action_3928503461=card; pgv_pvid=2924024080; pac_uid=0_050e9ae06ea51; tvfe_boss_uuid=890b429a39ebc7ca; RK=Gelp6pi4Xf; ptcz=66aa14b01a2ea41e402cfba10b10b07334b9709205e4229b0df45cf26d1a7997; fqm_pvqid=8197a091-1292-41b4-8874-b5719a04e115; ptui_loginuin=604328914; ua_id=jW09Y9qMMJuUgdQ1AAAAANDk3XKvP74QfmGGFt4DCq0=; wxuin=86107293996414; mm_lang=zh_CN; bizuin=3928503461; slave_bizuin=3928503461; noticeLoginFlag=1; rand_info=CAESIBzSmvFxgAEkp2j0HMB8UMPlWPpJfkzSA11Xg2M8KKc0; data_bizuin=3928503461; data_ticket=pC9OJeaD2cziYzUEwPVYGycocZ9hq8Fbf/+WnHUW8WDJ4Mb+oZYFle7ZGS8KmkTJ; slave_sid=Z2c4WHhJSm1QRGZoVzlHVVhsdmhSZ1V6MHg1VFNZbzVvSlducWRxQU03S05RcUZ2S0VUaGhPcXpaNkNhUVdyYXRJNEVoYXliN2Nza3RSM3hYd1lVYUNMaVljZnJjMVRLYlh4M1E4ZE11c1NYdHlla0VBOUxCQjR6aVFVcUY1NFYwMlNDblMwY1JXUWRIV0pv; slave_user=gh_9b10aff30334; xid=9c51c351558f379aaf37903ea2e9bc98; openid2ticket_opTQo6rYA33kqeYqkKRaa0BAPji4=qELqLOC+yqebtLDYc8pF/dplp/Z0lKhTrNy1NdHF6W0=; _clck=3928503461|1|fca|0; _clsk=1hgggzx|1686194453818|1|1|mp.weixin.qq.com/weheat-agent/payload/record; rewardsn=; wxtokenkey=777; wwapp.vid=; wwapp.cst=; wwapp.deviceid='


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
            'token': '1327459081',
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
            'token': '1327459081',
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

def parse_wexin_article(url):
    pass


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
            'token': '1327459081',
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
            'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=1327459081&lang=zh_CN',
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
        print(handle_articles_arr(articles_arr))

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