# -*- coding: utf-8 -*-

# encoding_test.py

import sys
import locale

print(sys.version)
print(sys.executable)

print("=== 编码测试 ===")
print("文件编码声明:", __doc__)
print("系统默认编码:", sys.getdefaultencoding())
print("标准输出编码:", sys.stdout.encoding)
print("区域设置:", locale.getpreferredencoding())
print("数字测试:", 123)
print("英文测试:", "Hello")
print("中文测试:", "你好")
print("特殊符号测试:", "★")

# # 测试文件读写
# with open("test.txt", "w", encoding="utf-8") as f:
#     f.write("Python文件读写测试")

# with open("test.txt", "r", encoding="utf-8") as f:
#     print("文件内容:", f.read())
