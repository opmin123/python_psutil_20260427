"""
服务器 cpu,memory,disk 等资源信息监控 20260509
"""

import psutil
import time
from datetime import datetime
def get_system_info():
    """获取系统资源信息"""
    # cpu
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cont = psutil.cpu_count()
    # memory(内存)
    memory = psutil.virtual_memory()
    mem_total = memory.total / (1024**3)   #GB
    mem_used = memory.used / (1024**3)
    mem_percent = memory.percent

    # disk (磁盘)
    disk = psutil.disk_usage('/')
    disk_total = disk.total / (1024**3)
    disk_used = disk.used / (1024**3)
    disk_percent = disk.percent

    #net (网络)
    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent / (1024**2) #MB
    bytes_recv = net.bytes_recv / (1024**2)


    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": cpu_percent,
        "cpu_count": cpu_cont,
        "mem_total_gb": round(mem_total,2),
        "mem_used_gb": round(mem_used,2),
        "mem_percent": mem_percent,
        "disk_total_gb": round(disk_total,2),
        "disk_used_gb": round(disk_used,2),
        "disk_percent": disk_percent,
        "net_sent_mb": round(bytes_sent,2),
        "net_recv_mb": round(bytes_recv,2)
    }


"""
持续监控并告警 20260509
"""

def monitor(interval=5, alert_cpu=80, alert_mem=80, alert_disk=90):
    print("开始监控... (Ctrl+c 退出)")

    while True:
        sys_info = get_system_info()
        # 打印信息
        print(f"\n[{sys_info['time']}]")
        print(f"cpu: {sys_info['cpu_percent']} % ({sys_info['cpu_count']} 核)")
        print(f"内存: {sys_info['mem_used_gb']} / {sys_info['mem_total_gb']}GB ({sys_info['mem_percent']}%)")
        print(f"磁盘: {sys_info['disk_used_gb']} / {sys_info['disk_total_gb']}GB ({sys_info['disk_percent']}%)")


        # 告警检查

        alert_messages = []
        if sys_info['cpu_percent'] > alert_cpu:
            alert_messages.append(f"⚠️cpu 使用率过高: {sys_info['cpu_percent']}%")
        if sys_info['mem_percent'] > alert_mem:
            alert_messages.append(f"⚠️内存使用率过高: {sys_info['mem_percent']}%")
        if sys_info['disk_percent'] > alert_disk:
            alert_messages.append(f"⚠️磁盘使用率过高: {sys_info['disk_percent']}%")

        for alert_message in alert_messages:
            print(alert_message)

        time.sleep(interval)


if __name__ == "__main__":
    monitor()