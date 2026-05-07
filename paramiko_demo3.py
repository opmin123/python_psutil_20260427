"""
20260507 SFTPClient类 完整实例
"""
#coding:utf8

import paramiko
import os
import traceback

class SshConnectError(Exception):#
   pass

class controlHost:
   def __init__(self, host, username, password, port=22, key_file='/root/.ssh/id_rsa'):##本地密钥文件路径
       self.host = host
       self.pkey = paramiko.RSAKey.from_private_key_file(key_file)
       self.ssh = controlHost.__sshConn(self.host, username, password, self.pkey, int(port)) #调用类中的静态方法__sshConn 返回ssh连接对象
       self.sftp = self.__sftpConn()


   def close(self):
       if hasattr(self.ssh, "close"):
           self.ssh.close()

   @staticmethod
   def __sshConn(host, username, password, pkey, port):
       ssh = paramiko.SSHClient()##创建一个SSH客户端client对象
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       try:
           ssh.connect(hostname=host, port=int(port), username=username, pkey=pkey) #免密登陆方式
           # print('免密登陆方式')
       except:
           try:
               ssh.connect(hostname=host, port=int(port), username=username, password=password)#密码认证
               # print('密码认证')
           except:
               raise SshConnectError("SSH Connect %s Error!" %host)
           else:
               return ssh
       else:
           return ssh

#返回sftp通道实例对象 方法
   def __sftpConn(self):
       transport = self.ssh.get_transport() #1.先ssh连上，2.再建立通道
       sftp = paramiko.SFTPClient.from_transport(transport) #创建一个已连通的SFTP客户端通道。
       return sftp


#执行命令方法
   def exeCommand(self, cmd, timeout=300):
       _, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
       try:
           channel = stdout.channel
           #print('channel',channel)
           exit_code = channel.recv_exit_status()
           #print('exit_code',exit_code)报错返回码是127，没有报错是0
           stdout = stdout.read().strip()
           stderr = stderr.read().strip()
           return {"status": 1, "stdout": stdout, "stderr": stderr, 'exit_code': exit_code}
       except:
           return {"status": 0, "stdout": stdout, "stderr": stderr, 'exit_code': 127}

#文件上传下载方法
   def sftpFile(self, localpath, remotepath, action):
       try:
           if action == 'push':
               dirname = os.path.dirname(remotepath)
               self.exeCommand("mkdir -p %s" % dirname)
               self.sftp.put(localpath, remotepath)
               return {"status": 1, "message": 'sftp %s %s success!' % (self.host, action)}
           elif action == "pull":
               dirname = os.path.dirname(localpath)
               if not os.path.exists(dirname):
                   os.makedirs(dirname)
               # if os.path.exists(localpath):
               #     os.remove(localpath)
               self.sftp.get(remotepath, localpath)
               return {"status": 1, "stdout": 'sftp %s %s success!' % (self.host, action), "stderr": ""}
       except Exception as e:
           return {"status": 0, "stderr": 'sftp %s %s failed %s' % (self.host, action, str(e)), "stdout": ""}

   @staticmethod
   def iter_local_path(abs_path):
       '''遍历本机该目录中所以的文件，并返回'''
       result = set([])
       for j in os.walk(abs_path):
           print(j)
           base_path = j[0]
           file_list = j[2]
           for k in file_list:
               p = os.path.join(base_path, k)
               result.add(p)
       return result

   def iter_remote_path(self, abs_path):
       '''获取远程主机abs_path下的所以文件'''
       result = set([])
       try:
           stat = str(self.sftp.lstat(abs_path))
           print('stat',stat)
       except FileNotFoundError:
           return result
       else:
           if stat.startswith("d"):
               file_list = self.exeCommand("ls %s" %abs_path)["stdout"].decode(encoding='utf-8').strip().splitlines()
               #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
                #Python splitlines() 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为(默认值) False，不包含换行符，如果为 True，则保留换行符。

               for j in file_list:
                   p = os.path.join(abs_path, j)
                   result.update(self.iter_remote_path(p))  #合并 并集U
           else:
               result.add(abs_path)
       return result





if __name__ == '__main__':
   x = controlHost("192.168.1.40", 'root', 'Gota34cc')

   #测试 获取本地某个目录的所有文件
   # w = x.iter_local_path("/root/test")
   # print(w)

   # 测试 获取远程主机某个目录的所有文件
   # y = x.iter_remote_path("/root/test")
   # print(y)

   # 测试 命令执行方法
   # y = x.exeCommand("uname -r")
   # print(y)

   # 测试 上传下载
   w = x.sftpFile("/tmp/ansible.txt", '/tmp/xx.txt', "push")  #将本地机器的/tmp/ansible.txt，上传至远程主机/tmp目录下并命名为xx.sh
   # w = x.sftpFile('/tmp/aaaa.py', '/tmp/xyz.py', 'pull')
   print(w)

   x.close()

