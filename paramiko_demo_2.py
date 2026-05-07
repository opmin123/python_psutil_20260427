"""
paramkio 案例2 20260507
"""
import paramiko
import paramiko as p

hostname = "192.168.0.15"
username = "root"
password = "123456"
client_server = p.SSHClient()
#paramiko.util.log_to_file('syslogin.log')

client_server.set_missing_host_key_policy(p.AutoAddPolicy)
#client_server.load_system_host_keys("/root/.ssh/known_hosts")
client_server.connect(hostname=hostname,username=username,password='password')
stdin,stdout,stderr = client_server.exec_command("free -h")
print(stdout.read().decode('utf-8'))
client_server.close()
#client_server.set_missing_host_key_policy(p.AutoAddPolicy)
