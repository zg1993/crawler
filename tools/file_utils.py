# -*-coding: utf-8 -*-

import os
import yaml


def parser_yaml(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        return yaml.safe_load(f.read())


if __name__ == '__main__':
    print(parser_yaml('/home/zg/work/crawler/gft/package_script.yaml'))