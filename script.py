# -*- coding: utf-8 -*-
import os

# package_list = ['xsecsyjshmvis']
package_list = [
    'xsecsyjshmvis',
    'bsznbfbqz',
    'bszndgvcp',
    'bsznhcfjq',
    'bsznjtrik',
    'bsznmymmb',
    'bsznxnvkw',
    'bsznznlzx',
    'bsznzabvp',
    'bsznnjcka',
    'bsznjvjdh',
    'bszndtinu',
    'bszndggut',
    'bsznyetld',
    'bsznmlbqb',
    'shjzyjsmqsbi',
    'syyjswmyhv',
    'gllrbtyjsdmnyd',
    'gmqfjzjyfgjjgrzfdkyjsufetg',
    'gmzzzftqgjjyjsyfsfq',
]
BASE_PATH = '/home/zg/work/gft-vue/'
path = '/home/zg/work/gft-vue/.env.production'


def modify_env_file(content):
    with open(path, encoding='utf-8', mode='w') as f:
        f.write(content)


def build_package(package_name):
    os.chdir(BASE_PATH)
    os.system('yarn build')
    move_command = "mv {0}.zip ./p".format(package_name)
    print(move_command)
    os.system(move_command)


for i in package_list:
    content = "VUE_APP_PROJECTNAME = " + i
    modify_env_file(content)
    build_package(i)
