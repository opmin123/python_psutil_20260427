"""
cpu ,内存 , 磁盘监控案例demo 2026-4-28
"""
from datetime import datetime

import psutil as p
import time
import smtplib
def cpu_memory_disk_check():
    CPU_USE_MAX_PERCENT = 80
    MEMORY_USE_MAX_PERCET = 80
    DISK_USE_MAX_PERCET = 80
    cpu_use_percet = p.cpu_percent(interval=1)
    memory_use_percet = p.virtual_memory().percent
    disk_use_percet = p.disk_usage('C:').percent

    check_alert = []
    if cpu_use_percet >= CPU_USE_MAX_PERCENT:
        check_alert.append(f"cpu使用率过高: {cpu_use_percet}%")
    if memory_use_percet >= MEMORY_USE_MAX_PERCET:
        check_alert.append(f"内存占用过高: {memory_use_percet}%")
    if disk_use_percet >= DISK_USE_MAX_PERCET:
        check_alert.append(f"磁盘使用过高: {disk_use_percet}%")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"[{timestamp}] cpu: {cpu_use_percet}% , 内存: {memory_use_percet}%, 磁盘: {disk_use_percet}%"
    print(content)
    if check_alert:
        print("警告:",":".join(check_alert))
    return check_alert
# 持续监控
if __name__ == '__main__':
    cpu_memory_disk_check()
    time.sleep(60)