"""
将目录下的文件按扩展名分类 20260508
"""

import os
import shutil


def organize_files(directory):
    # 获取目录中的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 跳过目录
        if os.path.isdir(file_path):
            continue

        # 按文件扩展名分类
        file_ext = filename.split('.')[-1]
        ext_dir = os.path.join(directory, file_ext.upper())

        # 如果分类目录不存在,则创建
        if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

        # 移动文件到分类目录中
        shutil.move(file_path, ext_dir)


# 调用函数,将指定目录进行整理
organize_files("C:/Users/73161/Desktop/20251205")
