"""
遍历指定目录下的所有文件和文件名
"""
import os.path
import time


def get_directory_file_list(directory_path,dir_name):
    file_path = os.path.join(directory_path,dir_name)
    content = os.listdir(file_path)
    print(content)
    files = os.listdir(directory_path)
    #print(files)

"""
列出目录及子目录下的文件
"""
def get_dir_file_info(path):
    for root,dir,files in os.walk(path):
        for file in files:
            if os.path.isfile(file):
                print(os.listdir(file))
            else:
                print(f"所在目录: {root}")
                print(f"子目录: {dir}")
                print(f"文件: {file}")




def file_list_demo(fload_path):
    for root,dirs,files in os.walk(fload_path):
        print(f"目录: {root}")
        print(f"子目录: {dirs}")
        print(f"文件: {files}")



"""
获取文件大小及判断文件是否存在 20260512
"""

def get_file_attr_info(path,dir_name):
    """
    遍历path 路径下的文件
    :param path:
    :return:
    """
    file_paths = os.path.join(path,dir_name)
    file_list = os.listdir(file_paths)
    for file in file_list:
        full_file_path = os.path.join(file_paths,file)
        if os.path.isdir(full_file_path):
            pass
        else:
            file_inof = os.stat(full_file_path)
            file_name = os.path.basename(file)
            file_size = file_inof.st_size / 1024**2
            file_cretime = time.ctime(file_inof.st_ctime)
            #file_size = os.path.getsize(file)
            #file_cretime = os.path.getctime(file)
            print(f"文件:{file_name}的大小是: {file_size}")
            print(f"文件: {file_name} 的创建时间是: {file_cretime}")



"""
判断文件是否存在 存在就输出文件大小 和创建日期 20260512
"""

def chke_file_info(fload_path,file_name):
    file_path = os.path.join(fload_path,file_name)
    file_list = os.listdir(file_path)
    for file in file_list:
        file_path = os.path.join(fload_path,file)
        file_info = os.stat(file_path)
        if os.path.basename(file) == file_name:
            print(f"文件大小: {file_info.st_size}")
            print(f"文件创建时间: {time.ctime(file_info.st_ctime)}")
        else:
            print("您输入的文件名不在改目录下!")



def chke_file_info_new(fload_path,file_name):
    file_path = os.path.join(fload_path,file_name)
    if os.path.exists(file_path):
        file_info = os.stat(file_path)
        print(f"文件大小: {file_info.st_size}")
        print(f"文件创建时间: {time.ctime(file_info.st_ctime)}")
    else:
        print("您输入的文件名不存在改目录下")


"""
批量修改目录下的文件名 20260512
"""
def chmod_file_name(fload_path,*arg):
    file_lists = os.listdir(fload_path)
    for file in file_lists:
        if os.path.isdir(file):
            pass
        else:
            file_path = os.path.join(fload_path,file)
            file_old_name = os.path.basename(file_path)
            file_old_name_end = file_old_name.split('.')[-1]
            qz = file_old_name.split('.')[:-1]
            try:

                #file_new_name = os.path.join(qz,name_str) + '.' + file_old_name_end
                file_new_name = os.path.join(qz,*arg)
                file_new_name_2 = os.path.join(file_new_name,".")
                full_new_file_name = os.path.join(file_new_name_2,file_old_name_end)
                os.rename(file_old_name,full_new_file_name)
                print(f"文件{file_old_name} 重命名为: {file_new_name}")
            except Exception as e:
                print({e})

""" ================================== 修改参考 ======================="""
import os


def chmod_file_name_test(fload_path, *args):
    file_lists = os.listdir(fload_path)

    for file in file_lists:
        file_path = os.path.join(fload_path, file)

        if os.path.isdir(file_path):
            continue

        # 获取文件基本信息
        file_old_name = os.path.basename(file_path)
        parts = file_old_name.split('.')

        # 处理有扩展名的情况
        if len(parts) > 1:
            file_old_name_end = parts[-1]  # 扩展名
            name_without_ext = '.'.join(parts[:-1])  # 不含扩展名的名字
            #name_without_ext = file_old_name.split('.')[-1]
        else:
            file_old_name_end = ''
            name_without_ext = file_old_name

        try:
            # 拼接新文件名（args 里的内容插入到文件名中）
            if args:
                new_name_parts = [name_without_ext] + list(args) + [file_old_name_end]
                # 过滤空字符串
                new_name_parts = [p for p in new_name_parts if p]
                file_new_name = '.'.join(new_name_parts)
            else:
                file_new_name = file_old_name

            # 构建完整路径
            full_old_path = file_path
            full_new_path = os.path.join(fload_path, file_new_name)

            # 重命名
            os.rename(full_old_path, full_new_path)
            print(f"文件 {file_old_name} 重命名为: {file_new_name}")

        except Exception as e:
            print(f"错误: {e}")




get_directory_file_list('C:/Users/73161/Desktop/20260511','demo')



get_dir_file_info('C:/Users/73161/Desktop/20260511')

print("==============  os 库的walk 用法 ========")
file_list_demo('C:/Users/73161/Desktop/20260511')

print("======================获取文件属性================")
get_file_attr_info('C:/Users/73161/Desktop/20260511','demo')

print("================ 判断文件是否在指定路径目录下,存在就输出改文件的大小、和创建时间")
chke_file_info_new('C:/Users/73161/Desktop/20260511','del_log.sh')


print("=============== 批量给文件重命名  ==================")
#chmod_file_name('C:/Users/73161/Desktop/20260511','minlu')
chmod_file_name_test('C:/Users/73161/Desktop/20260511','minlu')