# -*- coding: utf-8 -*-


import sys
import inspect
import importlib
import os

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
        

if __name__ == '__main__':
    if 1 == len(sys.argv):
        print('please input execute func')
    else:
        execute_func(sys.argv[1])