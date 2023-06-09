# -*-coding: utf-8 -*-
'''
1、修改route/index.ts和vite.config.ts文件(每个项目修改的文件不同(modify_project_file不同))--!!!重要确保修改的文件内容不能出现多个search_str
2、打包到对应区域的文件夹下
'''

import os
import subprocess
import re
import traceback
import argparse
import sys
from tools.file_utils import parser_yaml
from gft.config.package_to_id import PACKAGE_TO_ID, set_item ,SAVE_PATH_TO_ID, dump_file,load_file

BASE_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))  # 当前项目路径

JSON_PATH = os.path.join(BASE_PATH, 'gft/config/path_to_id.json')

CONFIG_YAML = parser_yaml(
    os.path.join(BASE_PATH, 'gft/config/package_script.yaml'))



# app_id 和 包的完整路径对应关系：提供给selenium simular跑脚本
# SAVE_PATH_TO_ID = {} 


# 生成放置前端包的地区文件夹
def mkdir_by_region(package_path='/home/zg/Documents/gftPackage',
                    project_branch_name='compress-package-zg',
                    region_dict=CONFIG_YAML['common']['account_passwd']):
    dir_apth = os.path.join(package_path, project_branch_name)
    if not os.path.exists(dir_apth):
        os.chdir(package_path)
        os.system('mkdir {}'.format(project_branch_name))
    for region, _ in region_dict.items():
        full_path = os.path.join(dir_apth, region)
        if os.path.exists(full_path):
            assert '/home/zg/Documents/gftPackage' in full_path  # 确保不误删其它文件夹文件
            if sum([
                    os.path.isfile(os.path.join(full_path, listx))
                    for listx in os.listdir(full_path)
            ]):
                os.system('rm {}/*'.format(full_path))  # 清空目录
        else:
            os.chdir(dir_apth)
            os.system('mkdir {}'.format(region))

# 检查打包后的包数量
def check_packaged(package_path, route_dict):
    actual_count = sum([len(os.listdir(os.path.join(package_path, k))) for k in route_dict])
    sum_package = sum([len(v) for _,v in route_dict.items()])
    print('sum_package: ', sum_package)
    print('actual_count: ', actual_count)
    for region, route_list in route_dict.items():
        if len(route_list):
            region_package_path = os.path.join(package_path, region)
            print('start check "{0}" package: {1}'.format(region, route_list))
            package_count = len(os.listdir(region_package_path))
            print('package_count', package_count)
            print('len(route_list)', len(route_list))
            assert package_count == len(route_list)
            print(region_package_path)
            os.system('ls -al {} | grep zip'.format(region_package_path))
            print()


# 替换文件内容
# search_str: outDir(route/index.ts) | redirect(vite.config.ts)
def replace_content(file_path, search_str, replace_str):
    pattern = re.compile(r'(?<=\').+?(?=\')')
    lines = []
    with open(file_path, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if search_str in line:
                lines.append(pattern.sub(replace_str, line))
            else:
                lines.append(line)
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)


# 修改项目文件，生成不同前端包(包名：路由名或者app-id)
# 项目分支gft-item-servers(compress-package-zg)
# 包名（和路由名对应）
def modify_project_file(project_path, package_name):
    router_file_path = os.path.join(project_path, 'src/router/index.ts')
    vite_ts_file_path = os.path.join(project_path, 'vite.config.ts')
    replace_content(router_file_path, 'redirect', package_name)
    replace_content(vite_ts_file_path, 'outDir', package_name)

def modify_project_file_vue(project_path, package_name):
    pass
    assert 0

def modify_project_file_yc(project_path, package_name):
    vite_ts_file_path = os.path.join(project_path, 'vite.config.ts')
    replace_content(vite_ts_file_path, 'outDir', package_name)


# 打包并移动到对应地区的文件夹
def pack(project_path, package_path, package_name, project_branch_name, build_command):
    if 'compress-package-zg' == project_branch_name:
        modify_project_file(project_path, package_name)
    elif 'vue' == project_branch_name:
        modify_project_file_vue(project_path, package_name)
    elif 'yc' == project_branch_name:
        modify_project_file_yc(project_path, package_name)
    else:
        print('error!!! please input correct project name')
        return
    os.chdir(project_path)
    try:
        os.system('pwd')
        os.system('git branch')
        print('start execute build command: ', build_command)
        res = subprocess.check_output(build_command.split(), encoding='utf-8')
        # res = subprocess.check_output(['npm','run', 'build'], encoding='utf-8')
        # res = subprocess.check_output(['yarn', 'build:test'], encoding='utf-8')
        if 'Done in' in res:
            print('build success')
            if 'compress-package-zg' == project_branch_name:
                if not os.path.exists(package_name + '.zip'):
                    os.system('zip -r {0}.zip {0}/'.format(package_name))
                else:
                    print('old package: {}'.format(package_name))
                os.system('rm -rf {}'.format(package_name))
            elif 'yc' == project_branch_name:
                os.system('rm -rf {}'.format(package_name))
            os.system('mv {0}.zip {1}'.format(package_name, package_path))
            return True
    except subprocess.CalledProcessError as _:
        traceback.print_exc()
        print('build failed', package_path, package_name)
        return False


# 批量打包
def batch_pack(project_path,
               package_path,
               project_branch_name,
               build_command,
               route_dict=None):
    if not route_dict:
        project_config = CONFIG_YAML.get(project_branch_name, {})
        route_dict = project_config.get('route_dict', {})
    mkdir_by_region(package_path, project_branch_name)
    res = []
    for region, route_list in route_dict.items():
        region_package_path = os.path.join(package_path, project_branch_name,
                                           region)
        # region_package_to_id = PACKAGE_TO_ID[region]
        for route in route_list:
            # app_id = region_package_to_id[route]
            # full_path = os.path.join(region_package_path, route)
            # SAVE_PATH_TO_ID[app_id] = full_path
            set_item(region, route, region_package_path,project_branch_name)
            res.append(
                pack(project_path, region_package_path, route,
                     project_branch_name, build_command))
    assert 0 != len(res)
    if all(res):
        check_packaged(os.path.join(package_path, project_branch_name), route_dict)
        print('batch pack successed!')
    else:
        print('batch pack failed!')
    dump_file(JSON_PATH)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project',
                        help='指定项目,默认gft一件事,可选赣通分（容缺受理）:rqsl; gtf-vue:vue',
                        default='compress-package-zg')
    args = parser.parse_args()
    project_branch_name = args.project
    package_path = CONFIG_YAML['common']['package_path']
    project_path = CONFIG_YAML[project_branch_name]['project_path']
    build_command = CONFIG_YAML[project_branch_name]['build_command']
    batch_pack(project_path, package_path, project_branch_name, build_command)
    print('---', SAVE_PATH_TO_ID)
    print('load', load_file(JSON_PATH))
