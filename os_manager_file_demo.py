"""
os 模块管理文件 demo 20260508
"""

import os
import sys
import time
from pathlib import Path
def get_system_inf():
    """
    获取系统基本信息 2026-5-8
    :return:
    """
    print("======= 系统信息 ========")
    print(f"操作系统名称: {os.name}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"当前进程ID: {os.getpid()}")
    if hasattr(os, 'getppid'):
        print(f"父进程ID: {os.getppid()}")
    print(f"行分隔符: {repr(os.linesep)}")
    print(f"路径分隔符: {os.sep}")
    print(f"路径环境变量分隔符: {os.pathsep}")


"""
文件和目录操作  20260508
"""

def file_directory_operation():
    print("\n===== 文件和目录操作 =====")
    # 创建测试目录
    test_dir = "practicat_test_dir"
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
        print(f"创建目录: {test_dir}")
    # 切换到测试目录
    original_dir = os.getcwd()
    os.chdir(test_dir)
    print(f"切换到目录: {os.getcwd()}")

    # 创建测试文件
    test_files = ["file1.txt","file2.txt","file3.log"]
    for test_file_name in test_files:
        with open(test_file_name, "w", encoding= "utf-8") as f:
            f.write(f"这是测试文件: {test_file_name} 的内容。\n创建时间: {time.ctime()} \n")
        print(f"创建文件: {test_file_name}")
    # 列出目录内容
    print(f"\n目录内容")
    for item in os.listdir("."):
        item_path = os.path.join(".", item)
        if os.path.isfile(item_path):
            file_size = os.path.getsize(item_path)
            print(f"文件: {item} ({file_size} 字节)")
        elif os.path.isdir(item_path):
            print(f" 目录: {item}")

    # 获取文件信息
    for test_file_name in test_files:
        stat_info = os.stat(test_file_name)
        print(f"\n文件 {test_file_name} 信息: ")
        print(f" 大小: {stat_info.st_size} 字节")
        print(f" 创建时间: {time.ctime(stat_info.st_ctime)}")
        print(f" 修改时间: {time.ctime(stat_info.st_mtime)}")

    # 删除测试文件
    for test_file_name in test_files:
        os.remove(test_file_name)
        print(f"删除文件: {test_file_name}")

    # 切换原始目录并删除测试目录
    os.chdir(original_dir)
    os.rmdir(test_dir)
    print(f"删除目录: {test_dir}")

"""
环境变量管理 demo 20260508
"""
def environment_variables():
    """
    环境变量演示操作
    :return:
    """
    print(f"\n===== 环境变量操作 =====")
    # 显示常用环境变量
    common_env_vars = ["PATH", "HOME", "USER", "USERNAME", "TEMP", "TMP"]
    print("常用环境变量")
    for var in common_env_vars:
        value = os.environ.get(var, "未设置")
        if len(value) > 100:
            value = value[:100] + "...."
        print(f" {var}: {value}")

    # 设置和获取自定义环境变量
    custom_var = "MY_PRACTICE_VAR"
    custom_value = "HELLO , OS MOdule Practice"
    os.environ[custom_var] = custom_value
    retrieved_value = os.environ.get(custom_var)
    print(f"\n 自定义环境变量")
    print(f" 设置: {custom_var} = {custom_value}")
    print(f" 获取: {custom_var} = {retrieved_value}")


"""
路径操作 demo 2060508
"""
def path_operations():
    print(f"\n===== 路径操作练习 =====")
    # 获取当前脚本的路径信息
    script_path = os.path.abspath(__file__)
    print(f"当前脚本路径: {script_path}")
    print(f"脚本目录: {os.path.dirname(script_path)}")
    print(f"脚本文件名: {os.path.basename(script_path)}")
    print(f"文件名(无扩展名): {os.path.splitext(os.path.basename(script_path))[0]}")
    print(f"文件扩展名: {os.path.splitext(script_path)[1]}")
    # 构造路径

    test_path = os.path.join("test","subdir","file.txt")
    print(f"\n构造路径: {test_path}")
    print(f"路径是否存在: {os.path.exists(test_path)}")
    print(f"是否为文件: {os.path.isfile(test_path)}")
    print(f"是否为目录: {os.path.isdir(test_path)}")


"""
系统命令 demo 20260508
"""

def execute_system_commands():
    """
    演示系统命令相关操作 20260508
    :return:
    """
    print(f"\n===== 系统命令执行 =====")
    # 执行简单的命令系统
    print(f"执行系统命令:")
    if sys.platform.startswith("Win"):
        # windows 系统
        print(" 执行 ‘dir’ 命令: ")
        result = os.system("dir")
    else:
        # unix/linux/Mac 系统
        print(" 执行 ‘ls’ 命令:")
        result = os.system("ls")




"""
文件搜索功能 20260508
"""

def search_file(directory=".", extension=""):
    """
    在指定目录中搜索特定扩展名文件
    directory : 搜索目录,默认当前目录
    extensiont : 文件扩展名,默认为空(所有文件)
    :param directory:
    :param extension:
    :return:
    """
    print(f"\n===== 文件搜索 =====")
    print(f"在目录‘{directory}’ 中搜索扩展名为 '{extension}' 的文件")
    found_files = []
    try:
        for root,dirs,files in os.walk(directory):
            for file in files:
                if not extension or file.endswith(extension):
                    file_path = os.path.join(root,file)
                    found_files.append(file_path)
                    if len(found_files) >= 20 :
                        break
            if len(found_files) >= 20:
                break
        for i,file_path in enumerate(found_files,1):
            print(f"  {i}. {file_path}")
        if len(found_files) >=20:
            print(f" ... 还有更多文件")
        print(f"总共找到 {len(found_files)} 个文件")
    except Exception as e:
        print(f"搜索过程中出错: {e}")



"""
主程序 20260508
"""

def main():
    """
    主程序入口
    :return:
    """
    while True:
        print("\n===== os 模块练习程序 =====")
        print("1. 获取系统信息")
        print("2. 文件和目录操作")
        print("3. 环境变量操作")
        print("4. 路径操作练习")
        print("5. 执行系统命令")
        print("6. 文件搜索")
        print("7. 退出程序")
        choic = input("请选择操作 (1-7): ").strip()
        if choic == '1':
            get_system_inf()
        elif choic == '2':
            file_directory_operation()
        elif choic == '3':
            environment_variables()
        elif choic == '4':
            path_operations()
        elif choic == '5':
            execute_system_commands()
        elif choic == '6':
            direction = input("请输入搜索目录(默认当前目录): ").strip() or "."
            extension = input("请输入文件扩展名(如 .py, .txt，留空表示所有文件): ").strip()
            search_file(direction,extension)
        elif choic == '7':
            print("感谢使用OS模块练习程序!")
            break
        else:
            print("无效选项,请重新选择")




"""
运行主程序 20260508
"""
if __name__ == "__main__":
    main()
