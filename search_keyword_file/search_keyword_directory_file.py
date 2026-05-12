"""
搜索目录下 含有关键字的文件  20260512
"""
import os


def searc_in_files(directory,keyWord):
    for root,dirs,files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root,file)
            try:
                with open(file_path,'r',encoding='utf-8') as f:
                    content = f.read()
                    if  keyWord in content:
                        print(f"在文件中找到关键词: '{keyWord}':{file_path}")
            except Exception as e:
                pass
                #print(e)

