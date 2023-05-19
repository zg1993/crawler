# -*- coding: utf-8 -*-
import os
import re

# package_list = ['xsecsyjshmvis']
package_list = [
    'bdcesfzydj',
    # 'fztbdcdblb',
    'fztysfywsq',
]
BASE_PATH = '/home/zg/work/gft-vue/'
path = '/home/zg/work/gft-vue/.env.production'


def modify_env_file(content):
    with open(path, encoding='utf-8', mode='w') as f:
        f.write(content)

def modify_aindex_file(ID):
    # file_path, line_number, replace_str
    replace_str = '@/routes/{}.js'.format(ID)
    print('replace_str',replace_str)
    file_path = '/home/zg/work/gft-vue/src/routes/aindex.js'
    line_number = 19
    pattern = re.compile(r'(?<=\`).+?(?=\`)')
    lines = []
    with open(file_path, 'r+', encoding='utf-8') as f:
        for index, line in enumerate(f.readlines(), 1):
            if line_number == index:
                print(line)
                lines.append(pattern.sub(replace_str, line))
                # lines.append(pattern.sub('{}'.format(route), line))
                # lines.append(pattern.sub('/{}'.format(route), line))
            else:
                lines.append(line)
    # print(lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)


def build_package(package_name):
    os.chdir(BASE_PATH)
    os.system('yarn build')
    move_command = "mv {0}.zip /home/zg/Documents/gftPackage".format(package_name)
    print(move_command)
    os.system(move_command)


for i in package_list:
    content = "VUE_APP_PROJECTNAME = " + i
    modify_env_file(content)
    modify_aindex_file(i)
    build_package(i)
