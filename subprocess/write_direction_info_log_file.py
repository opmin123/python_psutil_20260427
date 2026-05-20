"""
遍历目录将目录信息写入日志问
"""
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='file_info.log',  # 日志文件名
                    filemode='w')

def get_dir_info_logs(direction):
    for root,dir,files in os.walk(direction):
        for file in files:
            file_path = os.path.join(root,file)
            file_inof = f"File: {file_path}:, Size: {os.path.getsize(file_path)} bytes"
            logging.info(file_inof)
            print(file_inof)




get_dir_info_logs("C:/Users/73161/Desktop/20260511")