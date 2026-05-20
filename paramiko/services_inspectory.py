"""
批量巡检服务器脚本
自动检测服务器各项指标,结果保存巡检日志中 2026-5-20
"""


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
服务器批量综合巡检脚本
自动检测服务器各项指标，结果保存到巡检日志
"""

import paramiko
import concurrent.futures
import socket
import platform
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, asdict
import json


@dataclass
class InspectionReport:
    """巡检报告数据类"""
    ip: str
    hostname: str
    system_version: str
    kernel_version: str
    cpu_usage: str
    memory_usage: str
    disk_usage: str
    load_average: str
    uptime: str
    network_status: str
    running_services: str
    error_logs: str
    status: str
    error: str = None


class ServerInspector:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.reports: List[InspectionReport] = []

    def _ssh_connect(self, ip: str) -> paramiko.SSHClient:
        """建立SSH连接"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            ip,
            username=self.username,
            password=self.password,
            timeout=15,
            banner_timeout=15
        )
        return client

    def _exec_command(self, client: paramiko.SSHClient, cmd: str) -> str:
        """执行命令并返回输出"""
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        return stdout.read().decode('utf-8').strip()

    def _parse_memory(self, output: str) -> str:
        """解析内存使用情况"""
        lines = output.strip().split('\n')
        for line in lines:
            if 'Mem:' in line or '内存' in line:
                parts = line.split()
                if len(parts) >= 3:
                    total = int(parts[1]) / 1024
                    used = int(parts[2]) / 1024
                    percent = (used / total * 100) if total > 0 else 0
                    return f"总内存: {total:.0f}MB, 已用: {used:.0f}MB, 使用率: {percent:.1f}%"
        return output

    def _parse_disk(self, output: str) -> str:
        """解析磁盘使用情况"""
        lines = output.strip().split('\n')
        result = []
        for line in lines:
            if '/dev/' in line and '%' in line:
                parts = line.split()
                if len(parts) >= 5:
                    disk = parts[0]
                    used_percent = parts[4]
                    result.append(f"{disk} 使用率: {used_percent}")
        return '\n'.join(result) if result else output

    def inspect_single_server(self, ip: str) -> InspectionReport:
        """巡检单台服务器"""
        report = InspectionReport(
            ip=ip,
            hostname='N/A',
            system_version='N/A',
            kernel_version='N/A',
            cpu_usage='N/A',
            memory_usage='N/A',
            disk_usage='N/A',
            load_average='N/A',
            uptime='N/A',
            network_status='N/A',
            running_services='N/A',
            error_logs='N/A',
            status='failed'
        )

        try:
            client = self._ssh_connect(ip)

            # 1. 系统信息
            uname_output = self._exec_command(client, "uname -a")
            if uname_output:
                parts = uname_output.split()
                if len(parts) >= 2:
                    report.hostname = parts[1]
                if len(parts) >= 3:
                    report.kernel_version = parts[2]

            # 2. 系统版本
            os_release = self._exec_command(client,
                "cat /etc/os-release 2>/dev/null | grep -E '^PRETTY_NAME|^NAME|^VERSION' | head -3")
            if os_release:
                report.system_version = os_release.replace('\n', ' | ')
            else:
                report.system_version = self._exec_command(client, "cat /etc/redhat-release 2>/dev/null || uname -r")

            # 3. CPU使用率
            cpu_output = self._exec_command(client,
                "top -bn1 | grep 'Cpu(s)' | awk '{print \"用户占用: \" $2 \", 系统占用: \" $4}'")
            if cpu_output:
                report.cpu_usage = cpu_output
            else:
                idle = self._exec_command(client,
                    "top -bn1 | grep 'Cpu' | awk '{print $8}' | sed 's/id,//'")
                if idle:
                    try:
                        cpu_usage = 100 - float(idle.replace('%', ''))
                        report.cpu_usage = f"CPU总占用: {cpu_usage:.1f}%"
                    except:
                        report.cpu_usage = idle

            # 4. 内存使用
            mem_output = self._exec_command(client, "free -k | grep Mem")
            if mem_output:
                report.memory_usage = self._parse_memory(mem_output)

            # 5. 磁盘使用
            disk_output = self._exec_command(client, "df -h | grep -E '^/dev/'")
            if disk_output:
                report.disk_usage = self._parse_disk(disk_output)

            # 6. 系统负载
            load_output = self._exec_command(client, "uptime")
            if load_output:
                if 'load average' in load_output.lower():
                    report.load_average = load_output.split('load average:')[1].strip()
                else:
                    report.load_average = load_output

            # 7. 开机时间
            report.uptime = self._exec_command(client, "uptime -s 2>/dev/null || who -b")

            # 8. 网络状态
            ping_result = self._exec_command(client, "ping -c 1 114.114.114.114 -W 2 | grep '1 packets'")
            if ping_result:
                report.network_status = "网络正常" if '1 received' in ping_result or '1 packets received' in ping_result else "网络异常"
            else:
                report.network_status = "网络正常"

            # 9. 运行中的关键服务
            services_output = self._exec_command(client,
                "systemctl list-units --type=service --state=running 2>/dev/null | grep -E 'nginx|mysql|redis|docker|httpd|postgresql' | head -10")
            if not services_output:
                services_output = self._exec_command(client,
                    "service --status-all 2>/dev/null | grep '\\[ + \\]' | head -10")
            report.running_services = services_output if services_output else "未检测到关键服务"

            # 10. 错误日志
            error_output = self._exec_command(client,
                "journalctl -p err --since '1 hour ago' 2>/dev/null | tail -3")
            if not error_output:
                error_output = self._exec_command(client,
                    "tail -20 /var/log/messages 2>/dev/null | grep -i error | tail -3")
            report.error_logs = error_output if error_output else "无错误日志"

            client.close()
            report.status = 'success'

        except paramiko.AuthenticationException:
            report.error = "认证失败: 用户名或密码错误"
        except paramiko.SSHException as e:
            report.error = f"SSH连接失败: {str(e)}"
        except socket.timeout:
            report.error = "连接超时"
        except Exception as e:
            report.error = f"未知错误: {str(e)}"

        return report

    def batch_inspect(self, ip_list: List[str], max_workers: int = 10) -> List[InspectionReport]:
        """批量巡检"""
        print(f"{'='*60}")
        print(f"  服务器批量巡检系统")
        print(f"  巡检时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  服务器数量: {len(ip_list)}")
        print(f"{'='*60}\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(self.inspect_single_server, ip): ip for ip in ip_list}

            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    report = future.result()
                    self.reports.append(report)
                    status_icon = "[OK]" if report.status == 'success' else "[FAIL]"
                    print(f"  {status_icon} {ip} 巡检完成")
                except Exception as e:
                    print(f"  [FAIL] {ip} 巡检异常: {str(e)}")

        return self.reports

    def print_report(self):
        """打印巡检报告"""
        success_reports = [r for r in self.reports if r.status == 'success']
        failed_reports = [r for r in self.reports if r.status == 'failed']

        print(f"\n{'='*60}")
        print(f"  巡检报告")
        print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  成功: {len(success_reports)} 台, 失败: {len(failed_reports)} 台")
        print(f"{'='*60}")

        for report in success_reports:
            print(f"\n+-- 服务器: {report.ip} ({report.hostname})")
            print(f"|-- 系统版本: {report.system_version}")
            print(f"|-- 内核版本: {report.kernel_version}")
            print(f"|-- CPU使用: {report.cpu_usage}")
            print(f"|-- 内存状态: {report.memory_usage}")
            print(f"|-- 磁盘状态:\n{self._indent_text(report.disk_usage, '|   ')}")
            print(f"|-- 系统负载: {report.load_average}")
            print(f"|-- 开机时间: {report.uptime}")
            print(f"|-- 网络状态: {report.network_status}")
            print(f"|-- 运行服务:\n{self._indent_text(report.running_services, '|   ')}")
            print(f"|-- 错误日志: {report.error_logs}")

        for report in failed_reports:
            print(f"\n+-- 服务器: {report.ip} [失败]")
            print(f"|-- 错误原因: {report.error}")

    def save_to_log(self, filename: str = None) -> str:
        """保存巡检结果到日志文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"inspection_log_{timestamp}.txt"

        success_reports = [r for r in self.reports if r.status == 'success']
        failed_reports = [r for r in self.reports if r.status == 'failed']

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("                      服务器巡检报告\n")
            f.write("=" * 70 + "\n")
            f.write(f"巡检时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"本机信息: {platform.node()} ({platform.system()} {platform.release()})\n")
            f.write(f"巡检结果: 成功 {len(success_reports)} 台, 失败 {len(failed_reports)} 台\n")
            f.write("=" * 70 + "\n\n")

            for i, report in enumerate(success_reports, 1):
                f.write(f"{'-' * 70}\n")
                f.write(f"【{i}】服务器: {report.ip}\n")
                f.write(f"{'-' * 70}\n")
                f.write(f"主机名:        {report.hostname}\n")
                f.write(f"系统版本:      {report.system_version}\n")
                f.write(f"内核版本:      {report.kernel_version}\n")
                f.write(f"CPU使用率:     {report.cpu_usage}\n")
                f.write(f"内存使用:      {report.memory_usage}\n")
                f.write(f"磁盘使用:\n{self._indent_text(report.disk_usage, '  ')}\n")
                f.write(f"系统负载:      {report.load_average}\n")
                f.write(f"开机时间:      {report.uptime}\n")
                f.write(f"网络状态:      {report.network_status}\n")
                f.write(f"运行服务:\n{self._indent_text(report.running_services, '  ')}\n")
                f.write(f"错误日志:      {report.error_logs}\n\n")

            if failed_reports:
                f.write(f"\n{'=' * 70}\n")
                f.write("巡检失败服务器\n")
                f.write(f"{'=' * 70}\n")
                for i, report in enumerate(failed_reports, 1):
                    f.write(f"  {i}. {report.ip} - {report.error}\n")

        print(f"\n[OK] 巡检日志已保存: {filename}")
        return filename

    def save_to_json(self, filename: str = None) -> str:
        """保存为JSON格式"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"inspection_report_{timestamp}.json"

        data = {
            'inspection_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'local_host': platform.node(),
            'total_servers': len(self.reports),
            'success_count': len([r for r in self.reports if r.status == 'success']),
            'failed_count': len([r for r in self.reports if r.status == 'failed']),
            'reports': [asdict(r) for r in self.reports]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[OK] JSON报告已保存: {filename}")
        return filename

    @staticmethod
    def _indent_text(text: str, indent: str) -> str:
        """为文本添加缩进"""
        return '\n'.join([f"{indent}{line}" for line in text.split('\n')])


def main():
    # ==================== 配置区域 ====================
    SERVER_IPS = [
        '192.168.0.15',
        # 添加更多服务器IP...
    ]

    SSH_USERNAME = 'root'
    SSH_PASSWORD = '123456'

    MAX_WORKERS = 10

    # =================================================

    inspector = ServerInspector(SSH_USERNAME, SSH_PASSWORD)

    inspector.batch_inspect(SERVER_IPS, MAX_WORKERS)

    inspector.print_report()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    inspector.save_to_log(f"inspection_log_{timestamp}.txt")
    inspector.save_to_json(f"inspection_report_{timestamp}.json")


if __name__ == '__main__':
    main()