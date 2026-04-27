"""
psutil 模块 2026-4-27
"""
import datetime
import time
import psutil as p
print(p.cpu_times())
print(p.virtual_memory().used)
print(p.disk_partitions()[-1])
print(p.disk_usage("d:/"))
print(p.disk_io_counters())
print(p.net_io_counters())
print(p.net_if_addrs())
print(p.net_if_stats())

cpu_per_core = p.cpu_percent(interval=1, percpu=True)
cpu_core = p.cpu_count(logical=False)
print(cpu_core)
print(cpu_per_core)


now_time = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
print(now_time)

print("========================获取磁盘分区使用情况==================")
partitions = p.disk_partitions()
for partition in partitions:
    print(f"设备{partition.device}")
    try:
        partition_usage = p.disk_usage(partition.mountpoint)
        print(f"  总容量: {partition_usage.total / (1024 ** 3):.2f}GB")
        print(f"  已使用: {partition_usage.used / (1024 ** 3):.2f}GB")
        print(f"  使用率: {partition_usage.percent}%")
    except PermissionError:
        print("权限不足")