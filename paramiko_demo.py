"""
paramiko demo 2026-5-6
"""
import paramiko as p
from paramiko import SFTPClient as SF
client_service = p.SSHClient()
client_service.set_missing_host_key_policy(p.AutoAddPolicy())
#sftp: sftp_client = client_service.open_sftp()
try:
    client_service.connect(
        hostname="192.168.0.16",
        port = 22,
        username="root",
        password="123456"
    )
    #sftp.put(localpath="C:/Users/73161/Desktop/20251205/catalina.out",remotepath="/home/k8s_demo")
    stdin,stdout,stderr = client_service.exec_command("systemctl status docker")
    output = stdout.read().decode()
    print("服务状态:", output)
    stdin,stdout,stderr = client_service.exec_command("systemctl restart docker")
    print("重启结果:",stderr.read().decode())
except p.AuthenticationException:
    print("认证失败")
    #print(f"文件操作失败: {e}")
except p.SSHException as e:
    print(f"SSH 连接错误: {e}")
finally:
    client_service.close()
