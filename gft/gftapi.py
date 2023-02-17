# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import json
'''
基本通过事项编码:
获取基本信息(get_base_info)
获取附件信息(get_upload_material)
表单提交(submit)api
'''

t = None


async def get_base_info(session: aiohttp.ClientSession, item_code: str):
    url = 'https://gft2.fzyjszx.com/fztService/ycxt/getBaseInfo'
    params = {'itemCode': item_code}
    async with session.get(url, params=params) as resp:
        assert 200 == resp.status
        return await resp.text()


async def get_upload_meterial(session: aiohttp.ClientSession, item_code: str):
    url = 'https://gft.fzyjszx.com/fzt/business/getBusinessData'
    data = aiohttp.FormData()
    form = {
        'from':
        '1',
        'jmzfc':
        'fzmt8167',
        'appid':
        'laxyyxycsp',
        'key':
        '8f87b9ce1c8044bab20e8ea799360dcf',
        'method':
        '/fztService/ycxt/getUploadMaterial',
        'requestType':
        'get',
        'paramStr':
        json.dumps({
            'loginname': 'wdfzapp',
            'pwd': '111111a',
            'yyid': '102'
        }),
        'realParas':
        json.dumps({'itemCode': item_code}),
    }
    data.add_field('param', json.dumps(form))
    async with session.post(url, data=data) as resp:
        assert 200 == resp.status
        return await resp.text()


async def client_session():
    item_code = '361000-000201010000-GG-263-01'
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[
            get_base_info(session, item_code),
            get_upload_meterial(session, item_code)
        ])
        # resp = await get_base_info(session, item_code)


async def get_base_info_t(item_code):
    global t
    url = 'https://gft2.fzyjszx.com/fztService/ycxt/getBaseInfo'
    params = {'itemCode': item_code}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            t = await resp.text()
            return t
            # return await resp
            # return await


if __name__ == '__main__':
    code = '361000-000201010000-GG-263-01'
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(m(code))
    a = asyncio.run(client_session())
    print('--', a)
