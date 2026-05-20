"""
获取服务器的系统版本和内核版本 2026-05-20
"""
import paramiko


# def get_service_version_core(service_ip):
#     client_service = paramiko.SSHClient()
#     client_service.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#     client_service.connect(service_ip,username='root',password='123456')
#     stdin,stdout,stderr = client_service.exec_command("cat /proc/version")
#     #exit_status = stdout.channel.recv_exit_status() #等待命令执行完
#     out_contetn = stdout.read().decode('utf-8')
#     print(out_contetn)
#     client_service.close()
#
#
#
# get_service_version_core('192.168.0.15')



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量获取远程服务器系统版本和内核版本
"""

import paramiko
import concurrent.futures
from typing import List, Dict, Tuple

class ServerInfoCollector:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.results = []

    def get_server_info(self, service_ip: str) -> Dict:
        """获取单台服务器信息"""
        result = {
            'ip': service_ip,
            'status': 'success',
            'system_info': '',
            'kernel_version': '',
            'hostname': '',
            'error': None
        }

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                service_ip,
                username=self.username,
                password=self.password,
                timeout=10
            )

            # 获取系统信息 (uname -a)
            stdin, stdout, stderr = client.exec_command("uname -a")
            exit_status = stdout.channel.recv_exit_status()
            result['system_info'] = stdout.read().decode('utf-8').strip()

            # 解析系统信息
            if result['system_info']:
                parts = result['system_info'].split()
                if len(parts) >= 2:
                    result['hostname'] = parts[1]
                if len(parts) >= 3:
                    result['kernel_version'] = parts[2]

            # 单独获取系统版本 (适用于 Linux)
            stdin, stdout, stderr = client.exec_command("cat /etc/os-release 2>/dev/null || cat /etc/redhat-release 2>/dev/null || uname -r")
            result['os_release'] = stdout.read().decode('utf-8').strip()

            client.close()

        except paramiko.AuthenticationException:
            result['status'] = 'failed'
            result['error'] = '认证失败，请检查用户名/密码'
        except paramiko.SSHException as e:
            result['status'] = 'failed'
            result['error'] = f'SSH连接失败: {str(e)}'
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = f'未知错误: {str(e)}'

        return result

    def batch_get_info(self, ip_list: List[str], max_workers: int = 10) -> List[Dict]:
        """批量获取服务器信息"""
        print(f"开始批量获取 {len(ip_list)} 台服务器信息...\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(self.get_server_info, ip): ip for ip in ip_list}

            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    self.results.append(result)
                except Exception as e:
                    self.results.append({
                        'ip': ip,
                        'status': 'failed',
                        'error': str(e)
                    })

        return self.results

    def print_results(self):
        """打印结果"""
        success_count = sum(1 for r in self.results if r['status'] == 'success')
        failed_count = len(self.results) - success_count

        print("=" * 80)
        print(f"查询完成: 成功 {success_count} 台, 失败 {failed_count} 台")
        print("=" * 80)

        # 成功的结果
        if success_count > 0:
            print("\n【成功】服务器信息:\n")
            for r in self.results:
                if r['status'] == 'success':
                    print(f"  IP: {r['ip']}")
                    print(f"  主机名: {r['hostname']}")
                    print(f"  内核版本: {r['kernel_version']}")
                    print(f"  完整信息: {r['system_info']}")
                    if r.get('os_release'):
                        print(f"  系统版本:\n{r['os_release']}")
                    print("-" * 40)

        # 失败的结果
        if failed_count > 0:
            print("\n【失败】服务器列表:\n")
            for r in self.results:
                if r['status'] == 'failed':
                    print(f"  IP: {r['ip']} - {r['error']}")

    def export_to_file(self, filename: str = "server_info.txt"):
        """导出结果到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("服务器系统版本和内核版本信息\n")
            f.write("=" * 80 + "\n\n")

            for r in self.results:
                if r['status'] == 'success':
                    f.write(f"IP: {r['ip']}\n")
                    f.write(f"主机名: {r['hostname']}\n")
                    f.write(f"内核版本: {r['kernel_version']}\n")
                    f.write(f"完整信息: {r['system_info']}\n")
                    if r.get('os_release'):
                        f.write(f"系统版本:\n{r['os_release']}\n")
                    f.write("-" * 40 + "\n\n")

                elif r['status'] == 'failed':
                    f.write(f"IP: {r['ip']} - {r['error']}\n\n")

        print(f"\n结果已导出到: {filename}")


def main():
    # 服务器列表
    server_ips = [
        '192.168.0.15',
        # 添加更多服务器IP...
    ]

    # SSH 连接信息
    username = 'root'
    password = '123456'

    # 创建采集器
    collector = ServerInfoCollector(username, password)

    # 批量获取信息
    collector.batch_get_info(server_ips)

    # 打印结果
    collector.print_results()

    # 导出到文件
    collector.export_to_file()


if __name__ == '__main__':
    main()
