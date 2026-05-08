"""
python OS 模块
"""
import os
import time

current_dir = os.getcwd()
#print(f"当前工作目录: {current_dir}")
print("当前工作目录为:", current_dir)


path_1 = os.path.join('data','software','','demo')
print(path_1)

print("当前目录下的文件和目录: ")
for item in os.listdir(current_dir):
    item_path = os.path.join(current_dir,item)
    if os.path.isfile(item_path):
        item_info = os.stat(item)
        print(f"  文件: {item}")
        print(f"  文件大小: {item_info.st_size}")
        print(f"  文件创建时间: {time.ctime(item_info.st_mtime)}")
    elif os.path.isdir(item_path):
        item_info = os.stat(item)
        print(f"  目录: {item}")
        print(f"  文件大小: {item_info.st_size}")
        print(f"  文件创建时间: {time.ctime(item_info.st_mtime)}")