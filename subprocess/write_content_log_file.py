"""
将执行命令输出结果 写入本地日志文件中
"""
import datetime
import subprocess


def cmd_result_in_local_file(command_demo):
    #command_demo = 'dir'
    result_content = subprocess.run(command_demo,capture_output=True,text=True,shell=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #写入文件
    with open("dir_log","a") as log_file:
        log_file.write(f"{now}-command: {command_demo}\n")
        if result_content.stdout:
            log_file.write(f"STDOUT: {result_content.stdout}\n")
        if result_content.stderr:
            log_file.write(f"STDERR: {result_content.stderr}\n")


"""
一行一行读取text 文件中的主机IP 列表
"""

def readline_service_IP(file):
    try:
        with open(file,"r") as file_content:
            for lin in file_content:
                service_ip = lin.strip()
                print(f"{service_ip}\n")
    except Exception as e:
        print(e)


cmd_result_in_local_file('dir')
readline_service_IP("service_Ip.txt")


