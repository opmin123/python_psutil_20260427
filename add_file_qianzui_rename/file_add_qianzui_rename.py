"""
给知道目录下的所有文件 加上前缀 20260511
"""
import os


def batch_rename(path,prefix):
    for count , filename in enumerate(os.listdir(path)):
        old_path = os.path.join(path, filename)
        if os.path.isfile(old_path):
            name, ext = os.path.splitext(filename)
            new_name = f"{prefix}_{name}{ext}"
            new_path = os.path.join(path, new_name)
            os.rename(old_path, new_path)
        # 判断是否是目录
        elif os.path.isdir(old_path):
            batch_rename(old_path,prefix)

    print("重命名未完成!")



if __name__ == "__main__":
    batch_rename("C:/Users/73161/Desktop/20260511","minlu")
