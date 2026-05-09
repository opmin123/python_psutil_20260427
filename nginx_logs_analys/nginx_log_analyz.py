"""
nginx 日志分析 20260509
"""

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nginx 日志分析统计脚本
功能：统计 IP 访问量、状态码、访问路径、带宽使用等
"""

import re
from collections import Counter
from datetime import datetime

# Nginx 默认日志格式的正则表达式
# 格式：$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
LOG_PATTERN = re.compile(
    r'(?P<ip>[\d.]+)\s+'  # IP 地址
    r'-\s+-\s+'  # 远程用户（通常为空）
    r'$$(?P<time>[^$$]+)\]\s+'  # 时间
    r'"(?P<request>[^"]*)"\s+'  # 请求行
    r'(?P<status>\d{3})\s+'  # 状态码
    r'(?P<size>\d+)\s+'  # 响应大小
    r'"(?P<referer>[^"]*)"\s+'  # Referer
    r'"(?P<user_agent>[^"]*)"'  # User-Agent
)


def parse_log_line(line):
    """
    解析单行日志
    :param line: 日志行
    :return: 解析后的字典，解析失败返回 None
    """
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None


def analyze_log(log_file_path):
    """
    分析日志文件
    :param log_file_path: 日志文件路径
    :return: 包含所有统计数据的字典
    """
    ip_counter = Counter()  # IP 访问计数器
    status_counter = Counter()  # 状态码计数器
    path_counter = Counter()  # 请求路径计数器
    total_size = 0  # 总流量
    request_count = 0  # 总请求数
    bandwidth = 0  # 总带宽（字节）

    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed = parse_log_line(line)
            if not parsed:
                continue

            request_count += 1
            ip_counter[parsed['ip']] += 1
            status_counter[parsed['status']] += 1
            path_counter[parsed['request'].split()[1] if parsed['request'] else ''] += 1
            total_size += int(parsed.get('size', 0) or 0)

    bandwidth = total_size / (1024 * 1024)  # 转换为 MB

    return {
        'request_count': request_count,
        'bandwidth_mb': round(bandwidth, 2),
        'top_ips': ip_counter.most_common(10),
        'status_codes': dict(status_counter),
        'top_paths': path_counter.most_common(10),
    }


def print_report(stats):
    """
    打印统计报告
    :param stats: 统计数据字典
    """
    print("=" * 60)
    print("              Nginx 日志分析报告")
    print("=" * 60)

    # 基本统计
    print(f"\n📊 基本统计:")
    print(f"   总请求数: {stats['request_count']}")
    print(f"   总流量:   {stats['bandwidth_mb']} MB")

    # Top 10 IP 访问量
    print(f"\n🌐 Top 10 IP 访问量:")
    for ip, count in stats['top_ips']:
        print(f"   {ip:<15} -> {count} 次")

    # 状态码分布
    print(f"\n📋 状态码分布:")
    status_names = {
        '200': 'OK',
        '206': 'Partial Content',
        '301': 'Moved Permanently',
        '304': 'Not Modified',
        '400': 'Bad Request',
        '403': 'Forbidden',
        '404': 'Not Found',
        '500': 'Internal Server Error',
        '502': 'Bad Gateway',
        '503': 'Service Unavailable',
    }
    for code, count in sorted(stats['status_codes'].items()):
        name = status_names.get(code, 'Unknown')
        print(f"   {code} {name:<25} -> {count} 次")

    # Top 10 请求路径
    print(f"\n📁 Top 10 请求路径:")
    for path, count in stats['top_paths']:
        print(f"   {path:<40} -> {count} 次")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    log_path = 'access.log'  # 日志文件路径

    try:
        stats = analyze_log(log_path)
        print_report(stats)
    except FileNotFoundError:
        print(f"错误: 找不到日志文件 '{log_path}'")
    except Exception as e:
        print(f"错误: {e}")
