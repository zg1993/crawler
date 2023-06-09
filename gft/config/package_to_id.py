# -*- coding: utf-8 -*-

import os
import json

# 包名和应用标识的对应关系，按区县(账号)来维护(项目变化关系可能也不同)
# 这个对应关系在打好包后要确定,然后在进入详情页的时候取出使用

# /home/zg/work/gft-item-services 项目

PACKAGE_TO_ID = {
    'fuzhou': {
        'lhjy': 'lhjyyjslbkcltl',
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
        'lhjychain': 'lhjyyjslbkcltl',
        'yglychain': 'yglyyjslbygvea',
        # 3-15 事项拆分和合并
        'zkydchaincombine':'zkydyjshzwrpbm',
        'zkydchain': 'zkydyjslbzczns', # 农村二女户和独生子女对象中考加分一件事
        'zkydchainminority': 'ssmzzkjfyjsemhff', # 少数民族中考加分
        'zkydchaintaiwan': 'tjkszkjfyjszcexh', # 台籍考生中考加分
        'qyzgtxcombine':'qyzgtxyjsxshsu',
        'qyzgtx': 'qyzgtxyjslbkzrgk', # 企业职工正常退休一件事
        'qyzgtxearly': 'qyzgtqtxyjslbqbupb', # 企业职工提前退休一件事
        # test
        'test': 'laxtest',
        #公积金
        'buyHPF':'gftqgjjyjsfwlcwjn',
        'rentHPF':'zftqgjjyjsfwxsdjb',
    },
    'lean': {
        # test
        'buyHPF': 'csfzzxqmley'
    },
    'guangchang': {},
    'yihuang': {},
    'linchuan': {},
    'nanfeng': {},
    'jinxi': {},
    'nancheng': {},
    'gaoxin': {},
    'chongren': {},
    'dongxiang': {},
    'zixi': {},
    'lichuan': {},
    'donglin': {},
}

# gtf-vue项目（不动产相关）

# gft-new-yc-item项目


SAVE_PATH_TO_ID = {}

def set_item(region, route, region_package_path, project_name='compress-package-zg'):
    if 'compress-package-zg' == project_name:
        region_package_to_id = PACKAGE_TO_ID[region]
        app_id = region_package_to_id[route]
    elif 'yc' == project_name:
        app_id = route

    if region not in SAVE_PATH_TO_ID:
        SAVE_PATH_TO_ID[region] = {}
    region_dict = SAVE_PATH_TO_ID[region]
    if app_id in region_dict:
        raise KeyError('Duplicate key detected: ', app_id, region)
    else:
        full_path = os.path.join(region_package_path, route)
        region_dict[app_id] = full_path

def dump_file(file_path):
    with open(file_path, 'w') as f:
        json.dump(SAVE_PATH_TO_ID,f)

def load_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

