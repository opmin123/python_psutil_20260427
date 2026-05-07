"""
paramiko 模块 SFTP 文件传输 20260507
"""
import paramiko as p
from paramiko import SFTPClient as SF
#创建客户端连接
client_server = p.SSHClient()
client_server.set_missing_host_key_policy(p.AutoAddPolicy)  #自动接收新主机
client_server.connect("192.168.0.15", username="root",password="123456")

sftp: SF = client_server.open_sftp()  #创建SFTP客户端

try:
    #上传文件到远程服务器
    sftp.put(localpath="C:/Users/73161/Desktop/20251205/deploy_aliyun.yaml", remotepath="/root/sftp_test/deploy_aliyun.yaml")
    print("文件上传成功")

    #远程服务器文件下载到本地
    sftp.get(remotepath="/root/subnet.env", localpath="C:/Users/73161/Desktop/20251205/download_test/subnet.env")
    print("文件下载成功")
    sftp.mkdir("/root/demo_20260507_test")
#异常捕获
except IOError as e :

    print(f"文件操作失败: {e}")
#关闭客户端连接
finally:
    sftp.close()
    client_server.close()