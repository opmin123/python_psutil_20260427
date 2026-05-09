"""
移动 文件
"""
import os
import shutil
# source_folder = "C:/Users/73161/Desktop/20260509"
# destination_folder = "C:/Users/73161/Desktop/20260509/fenlei_file_name"
# files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
# def move_file(file):
#     try:
#         file_extensiton = os.path.splitext(file)[1][:1]
#         if not os.path.exists(os.path.join(destination_folder, file_extensiton)):
#             os.makedirs(os.path.join(destination_folder,file_extensiton))
#         shutil.move(os.path.join(source_folder,file), os.path.join(destination_folder,file_extensiton,file))
#     except Exception as e:
#         print(f"Error processing {file}: {str(e)}")
#move_file('/Users/73161/Desktop/20260509')


import os
import shutil

path = 'C:/Users/73161/Desktop/20260509'
files = os.listdir(path)
print(f"{files}")

try:
    for f in files:
        # 跳过目录，只处理文件
        file_path = os.path.join(path, f)
        if os.path.isdir(file_path):
            continue

        folder_name = f.split('.')[-1]
        folder_path = os.path.join(path, folder_name)  # 目标文件夹完整路径

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 移动文件：从原路径到目标文件夹
        shutil.move(file_path, folder_path)
except Exception as e:
    print(f"{e}")