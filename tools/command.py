# -*- coding: utf-8 -*-


import sys
import inspect
import importlib
import os
import re

MODULE = importlib.import_module('tools.command')

def log_switch():
    project_path = '/home/zg/work/gft-item-services'
    assert os.path.exists(os.path.join(project_path, 'index.html'))
    file_path = os.path.join(project_path, 'index0.html')
    is_test = os.path.exists(file_path)
    if is_test:
        os.rename(os.path.join(project_path,'index.html'),os.path.join(project_path,'indext.html'))
        os.rename(os.path.join(project_path,'index0.html'),os.path.join(project_path,'index.html'))
        print('restore')
    else:
        os.rename(os.path.join(project_path,'index.html'),os.path.join(project_path,'index0.html'))
        os.rename(os.path.join(project_path,'indext.html'),os.path.join(project_path,'index.html'))
        print('test log')

def execute_func(name):
    flag = False
    assert not 'execute_func'.startswith(name)
    for (func_name, func) in inspect.getmembers(MODULE, inspect.isfunction):
        abbr = func_name.split('_')[0]
        if name == func_name or name == abbr:
            flag = True
            func()
            break
    else:
        if not flag:
            print('please input correct func name')

def pattern_func():
    p = re.compile(r'(.*?)-.*?-.*?（(.*?)）', re.S)
    # p = re.compile(r'（(.*?)）', re.S)
    string = '''104-中国银行-104437073897（中国银行）103-农业银行-103437035118（农业银行）   105-建设银行-105437000100（建设银行）  102-工商银行-102437011070 （工商银行）301-交通银行-301437000012（交通银行）b34-上饶银行-313437000014（上饶银行）a73-江西银行-313437084601（江西银行） b14-赣州银行-313437028892（赣州银行） a30-九江银行-313437079913（九江银行） a09-邮政储蓄银行-403437000044（邮政储蓄银行） a29-抚州农商银行-402437010014（抚州农商银行） 309-兴业银行-309437002143（兴业银行）
    '''
    finds = re.findall(p, string)
    # print(finds)
    print(len(finds))
    res = '[\n'
    for (key, name) in finds:
        key = key.strip()
        # res += "{ text: '{0}', value: '{1}' },\n".format(name, key)
        res += "{ text: '%s', value: '%s' },\n"% (name, key)
    res +=']'
    print(res)

def downloadPic():
    path_pic = '/home/zg/Downloads/photo'
    os.chdir(path_pic)
    p = re.compile(r'\[(.*?)\]', re.S)
    count = 10384
    with open('/home/zg/Downloads/photo.txt', 'r+') as f:
        for line in f:
            url = re.findall(p, line)
            url = url[0]
            suffix = url.split('.')[-1]
            count = count + 1
            filename = str(count) + '.' + suffix
            print(filename)
            os.system('curl -o {0} "{1}"'.format(filename, url))
        

if __name__ == '__main__':
    if 1 == len(sys.argv):
        # pattern_func()
        downloadPic()
        print('please input execute func')
    else:
        execute_func(sys.argv[1])