# -*-coding: utf-8 -*-

import os
import yaml
from pypinyin import lazy_pinyin, pinyin,Style

country_to_code = {
    '市本级': '361000',
    '东乡区': '361029',
    '宜黄县': '361026',
    '资溪县': '361028',
    '临川区': '361002',
    '乐安县': '361025',
    '南城县': '361021',
    '金溪县': '361027',
    '广昌县': '361030',
    '黎川县': '361022',
    '南丰县': '361023',
    '崇仁县': '361024',
    '高新区': '361099',
    '东临新区': '361006',
}


def parser_yaml(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        return yaml.safe_load(f.read())

def parser_country_to_pinyin(INITIALS=False):
    res = {}
    # l = []
    for country, _ in country_to_code.items():
        arr = lazy_pinyin(country)
        if INITIALS:
            arr = map(lambda i:i[0], arr)
        res[country] = ''.join(arr)
        # l.append(''.join(arr))
    # print(len(set(l)) == len(l))
    return res



if __name__ == '__main__':
    print(parser_country_to_pinyin(True))
    print(parser_country_to_pinyin(False))
        
    