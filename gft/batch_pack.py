# -*-coding: utf-8 -*-

import os
import subprocess
import re

ROUTER_FILE = '/home/zg/work/gft-item-services/src/router/routes/index.ts'
ROUTER_FILE_BAK = '/home/zg/work/gft-item-services/src/router/index.ts'
VITE_CONFIG = '/home/zg/work/gft-item-services/vite.config.ts'
# ROUTER_FILE = '/home/zg/work/gft-item-services/.env.development'

# ROUTE_LIST = [
#     'grcy', 'lhjy', 'lose-job', 'gxjy', 'ygly', 'social-assistance', 'sy',
#     'wykfd'
# ]
# ROUTE_LIST = ['grcy', 'lhjy', 'gxjy', 'ygly']
# ROUTE_LIST = ['sy']
ROUTE_LIST = ['sy']


def replace_content(file_path, line_number, replace_str):
    if (not os.path.exists(file_path)):
        file_path = ROUTER_FILE_BAK
        line_number = 20
    pattern = re.compile(r'(?<=\').+?(?=\')')
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


def pack(project_path, package_path, package_name):
    replace_content(ROUTER_FILE, 20, '/{}'.format(package_name))
    replace_content(VITE_CONFIG, 65, '{}'.format(package_name))
    os.chdir(project_path)
    try:
        res = subprocess.check_output(['yarn', 'build'], encoding='utf-8')
        # res = subprocess.check_output(['yarn', 'build:test'], encoding='utf-8')
        if 'Done in' in res:
            print('build success')
            os.system('zip -r {0}.zip {0}/'.format(package_name))
            os.system('rm -rf {}'.format(package_name))
            os.system('mv {0}.zip {1}'.format(package_name, package_path))
    except subprocess.CalledProcessError as e:
        print('build failed')


def batch_pack(project_path, package_path):
    for route in ROUTE_LIST:
        pack(project_path, package_path, route)


if __name__ == '__main__':
    project_path = '/home/zg/work/gft-item-services'
    package_path = '/home/zg/Documents/gftPackage'
    batch_pack(project_path, package_path)

    # pack(project_path, package_path)
    # replace_content('yyy')
