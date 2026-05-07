"""
监控进程 案例demo 2026-4-28
"""
import psutil as p
def check_process(process_name):
    process_info = p.process_iter()
    for proc in p.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        if process_name.lower() in proc.info['name'].lower():
            memory_mb = proc.info['memory_info'].rss / (1024**2)
            print(f"进程: {proc.info['name']}")
            print(f"PID: {proc.info['pid']}")
            print(f"cpu: {proc.info['cpu_percent']}")
            print(f"内存: {memory_mb:.2f}MB")
            if memory_mb > 1024:
                print("警告：该进程内存使用过高！")



if __name__ == '__main__':
    check_process('python')
