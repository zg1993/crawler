
# -*- coding: UTF-8 -*-
'''
前段测试环境自动化部署
放在前段项目根目录下
gwtph-test项目标识 yaml文件配置
使用python deploy.py <gwtph-test> --branch <branch>
'''

import os
import sys
import argparse
import yaml
import subprocess
from datetime import datetime
import sys
from pathlib import Path
# 获取项目根目录（假设此代码在项目子目录中）
project_root = Path(__file__).parent.parent  # 根据实际结构调整.parent的数量

# 将项目根目录添加到系统路径
sys.path.append(str(project_root))


from tools.utils import zip_folder


BASE_PATH = os.path.dirname(__file__)
# PACKAGE_NAME = 'gwtph-web'
# SERVER_PATH = '/etc/nginx/html'
# HOSTNAME = 'serve108'


def parser_yaml():
    yaml_path = os.path.join(BASE_PATH, 'deploy.yaml')
    with open(yaml_path, 'r', encoding='utf8') as f:
        return yaml.safe_load(f.read()) 


def test_ssh_connect(server_ip='', **kwargs):
    print(server_ip)
    test_command = "ssh root@{0} echo 'connect success'".format(server_ip) 
    # test_command = 'ssh root@{0} pwd'.format('192.168.10.157') 
    c = os.system(test_command)
    if(os.system(test_command) != 0):
        return False
    return True


def build_package(branch, project_path='', package_name='', build_command='yarn build', **kwargs):
    os.chdir(project_path)
    os.system('git checkout ' + branch)
    os.system('git pull')
    print('executing: {0}'.format(build_command))
    os.system(build_command)
    if not os.path.exists('dist'):
        print('build failed')
        return False
    if( 'dist' != package_name):
        os.system('mv dist ' + package_name)
    return True


# 最多保存5份
def backup_dist(server_ip, server_deploy_path, package_dir,package_name, back_nums=5):
    backup_name = package_name + '_' + datetime.today().strftime('%m%d%H%M')
    # suf = re.sub(u'([^\u0041-\u007a])', '', file)
    # name = re.sub(u"([^\u0030-\u0039])", "", file)
    command_args = ['ssh', 'root@{}'.format(server_ip), 'ls {}'.format(server_deploy_path)]
    result_ls = subprocess.check_output(command_args, encoding='utf8')
    file_list = result_ls.split('\n')
    backup_name_list = filter(lambda i:i.startswith(package_name), file_list)
    if (len(list(backup_name_list))<5):
        backup_command = "mv {0} {1}".format(package_dir, backup_name)
    else:
        rm_file = sorted(backup_name_list)[0]
        rm_command = "rm -rf {0}".format(rm_file)
        # os.system('ssh root@' + server_ip + ' ' + rm_command)
        print(rm_command)
    # os.system('ssh root@' + server_ip + ' ' + backup_command)
    print(backup_command)

def ssh_deploy_jd(server_ip='', server_deploy_path='', package_name='', project_path='', **kwargs):
    print('compress dist/ => dist.zip')
    zip_folder(f'{project_path}/{package_name}', f'{project_path}/{package_name}.zip')
    print('ssh deploy jd')
    # scp 传输打包后的文件夹压缩包到服务器
    package_zip = os.path.join(project_path, f'{package_name}.zip')
    scp_command = f"scp -r {package_zip} root@{server_ip}:{server_deploy_path}"
    print(f'executing {scp_command}')
    os.system(scp_command)
    
    
    #解压
    # package_path = os.path.join(server_deploy_path, package_name).replace(os.sep, '/')
    ssh_remote_command = f'ssh root@{server_ip}'
    unzip_command = f"unzip -o {server_deploy_path}/{package_name}.zip -d {server_deploy_path}"
    execute_command = f'{ssh_remote_command} "{unzip_command}"'
    
    #解压前删除css js assets文件夹（打包后的文件名带hash值）
    if(project_path.endswith('page-h5')):
        delete_assets= f'rm -rf {server_deploy_path}/assets'
        execute_delete_assets_command = f'{ssh_remote_command} {delete_assets}'
        print(f'executing {execute_delete_assets_command}')
        os.system(execute_delete_assets_command)
    elif(project_path.endswith('backend-manage-system')):
        delete_css= f'rm -rf {server_deploy_path}/css'
        delete_js= f'rm -rf {server_deploy_path}/js'
        execute_delete_css_command = f'{ssh_remote_command} {delete_css}'
        execute_delete_js_command = f'{ssh_remote_command} {delete_js}'
        print(f'executing {execute_delete_css_command}')
        os.system(execute_delete_css_command)
        print(f'executing {execute_delete_js_command}')
        os.system(execute_delete_js_command)


    print(f'executing {execute_command}')
    os.system(execute_command)

    # scp 传输打包后的文件夹到服务器
    # package_dir = os.path.join(project_path, package_name)
    # scp_command = f"scp -r {package_dir} root@{server_ip}:{server_deploy_path}"
    # print(f'executing {scp_command}')
    # os.system(scp_command)
    # ssh远程命令移动文件
    # package_dir_server = os.path.join(server_deploy_path, package_name).replace(os.sep, '/')    
    # ssh_remote_command = f'ssh root@{server_ip}'
    # move_command = f"cp -rf {package_dir_server}/* {server_deploy_path}"
    # execute_command = f'{ssh_remote_command} "{move_command}"'
    # print(f'executing {execute_command}')
    # os.system(execute_command)
    pass

def ssh_deploy(server_ip='', server_deploy_path='', package_name='', project_path='', **kwargs):
    # backup
    package_dir = os.path.join(server_deploy_path, package_name)
    package_backup_dir = package_dir + '_backup'
    backup_command = "mv {0} {1}".format(package_dir, package_backup_dir)
    print('executing backup ssh command: ' + backup_command)
    backup_dist(server_ip, server_deploy_path, package_dir,package_name)
    #os.system('ssh root@' + server_ip + ' ' + backup_command)

    # scp translate
    package_dir_local = os.path.join(project_path, package_name)
    scp_command = "scp -r {0} root@{1}:{2}".format(package_dir_local, server_ip,server_deploy_path)
    print('executing scp command: ' + scp_command)

    #os.system(scp_command)

    # 删除服务器备份包
    rm_command = "rm -rf {0}".format(package_backup_dir)
    print('executing rm  ssh command: ' + rm_command)

    #os.system('ssh root@' + server_ip + ' ' + rm_command)

    print('deploy success')
    # delete local dist
    os.system('rm -rf' + ' ' + os.path.join(BASE_PATH, package_dir_local))

def deploy(project, branch):
    server_dict = parser_yaml()
    # print(server_dict)
    if (project not in server_dict):
        return print('%s not config, please add to deploy.yaml'%(project))
    deploy_info = server_dict.get(project)
    print(deploy_info)
    # if(not test_ssh_connect(**deploy_info)):
    #     return print('unable to connect {server_ip}'.format(**deploy_info))
    
    if(build_package(branch, **deploy_info)):
    # if(1):
        # ssh_deploy(**deploy_info)
        ssh_deploy_jd(**deploy_info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project', help='项目标识必填yaml文件配置')
    parser.add_argument('--branch', help='发布分支名称，默认使用dev')
    args = parser.parse_args()
    project = args.project
    branch = args.branch or 'dev'
    deploy(project, branch)