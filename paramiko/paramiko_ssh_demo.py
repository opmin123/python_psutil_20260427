"""
paramiko 模块SSH连接服务器 2026-5-19
"""
import paramiko.client

#priviate_key = paramiko.RSAKey.from_private_key('/root/.ssh/id_rsa')
#with open('/root/.ssh/id_rsa', 'r') as lin:
#    private_key = paramiko.RSAKey.from_private_key(f)
client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('192.168.0.20',port=22,username='root',password='root@daselearn.20')
stdin,stdout,stdrr = client.exec_command('ls -l')
resutl_content = stdout.read()
print(resutl_content)